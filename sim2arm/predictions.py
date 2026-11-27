#!/usr/bin/env python3
"""
predictions.py -- what the slot-1 two-arm run should see, observable by observable, from the Geant4 tables
(lnl_x17, 2026-11-20).  Feeds the "Predictions" tab of the page (site/template.html) through out/predictions.json.

The ladder follows the run: cosmic nights (arms vertical, then horizontal), beam singles, beam pairs at 441 keV and
1.10 MeV.  Every number is per arm or per pair of the two-arm set-up, 11 µm Li in the built Cu hemisphere (R 11 mm,
300 µm, rim, grey flange: config dome300, runs L10 + L18; TA_CFG=ogCu200 gives the Cu ogive the 19 Nov study used), 1 µA.

Inputs
  $WORK_DATA/x17_facility_search/pred/pred_cosmic_L15v2.npz   L15 cosmic-disk muons, every event with legs in both
                                                             arms of a slot-1 pair (sim2arm/lxplus/pred_cosmic_scan.py)
  $WORK_DATA/x17_facility_search/pred/pred_gam_L18.npz        L18 8Be γ lines in the Cu hemisphere, every event with a
                                                             leg (same script, --mode single; L13 = the ogive)
  shapes_nd event tables via two_arm_nd.py (pairs: IPC, EPC, X17, cosmics after the analysis), as in the reach fits
  out/summary_rates<PASS>li11.csv (PASS=_pass4: dome300)       the reach pass's own cosmic rates after the analysis

Definitions (lnl_merge.py): a trigger LEG is SiPM bar >= 0.5 MIP AND plastic >= 0.5 MIP in one arm; an MM TRACK is a
Micromegas segment (dominant track, >= 3 steps) with its charge centroid in the active area.  The simulation's
chambers are 100 % efficient: the "× ε" numbers apply the bench efficiency EPS_MM per chamber.

    WORK_DATA=/media/ucla/work TA_EPC_RUN=L19 ~/PycharmProjects/nTof_x17/.venv/bin/python sim2arm/predictions.py

27 Nov: external conversions from run L19 (TA_EPC_RUN=L19, as the reach fits); beam rates per beam day of 18 h of beam.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

os.environ.setdefault('WORK_DATA', '/media/ucla/work')
os.environ['LI_UG'] = os.environ.get('LI_UG', '587')          # 11 µm, the recommended film
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import numpy as np            # noqa: E402

import two_arm_nd as T        # noqa: E402

sys.path.insert(0, str(HERE.parent / 'planning'))
import two_arm_estimates as TAE  # noqa: E402

#: beam rates are per BEAM DAY (TAE.BEAM_DAY_H = 18 h of CN beam, 27 Nov); cosmic nights stay per night, cosmic day rates per 24 h
BD = TAE.BEAM_DAY_H / 24.0

SN, G = T.SN, T.G
W = Path(os.environ['WORK_DATA']) / 'x17_facility_search'
PRED = W / 'pred'
OUT = HERE / 'out'
LI_UG = float(os.environ['LI_UG'])
MU_LIVE = T.MU_LIVE_DISK                  # s of live time per generated L15 muon
EPS_MM = 0.92                             # bench efficiency within 5 mm, chambers A and B (91-93 %)
SIG_T = G.TOF_SIGMA_NS                    # measured per-arm σ_t (n_TOF beam-off cosmics), 0.60 ns
PAIRS = {'vert': (2, 3), 'horiz': (0, 1), 'adj': (0, 2)}
RESP = 'LNL calibrated'
LEVEL = 'MM 15° + TOF'
NIGHT_H = 10.0                            # one cosmic night
C_MM_NS = 299.792458                      # mm/ns
rng = np.random.default_rng(20261120)
TGT = T.CFG                               # dome300 (built hemisphere) unless TA_CFG says otherwise
GAM_FILE = os.environ.get('PRED_GAM', 'pred_gam_L18.npz' if TGT == 'dome300' else 'pred_gam_L13.npz')


def r3(x, n=3):
    """round to n significant figures (JSON-friendly)."""
    if x is None or not np.isfinite(x):
        return None
    if x == 0:
        return 0.0
    return float(f'{x:.{n}g}')


def hist(x, edges, w=None, scale=1.0):
    h, _ = np.histogram(x, edges, weights=w)
    n, _ = np.histogram(x, edges)
    return dict(edges=[r3(e, 5) for e in edges], y=[r3(v * scale) for v in h], n=[int(v) for v in n])


def rel(n):
    return 1 / np.sqrt(n) if n > 0 else None


# --------------------------------------------------------------------------- cosmics
def cosmics():
    z = np.load(PRED / 'pred_cosmic_L15v2.npz')
    live = int(z['cnt_n_generated']) * MU_LIVE
    leg, mm = z['leg'], z['mm']
    trk = mm                                           # MM track (lnl_merge definition)
    out = dict(live_days=r3(live / 86400), n_muons=int(z['cnt_n_generated']))
    arms = []
    for a in range(4):
        nl, no = int(z['cnt_leg_arm'][a]), int(z['cnt_ok_arm'][a])
        arms.append(dict(arm=a, leg_hz=r3(nl / live), ok_hz=r3(no / live), frac_track=r3(no / nl),
                         frac_track_eps=r3(no / nl * EPS_MM), n_mc=nl))
    out['arms'] = arms
    edges_th = np.arange(0, 181, 5.0)
    edges_dt = np.arange(-6, 6.01, 0.25)
    edges_z = np.arange(0, 91, 5.0)
    edges_d = np.arange(0, 301, 10.0)
    pairs = {}
    for name, (i, j) in PAIRS.items():
        m = leg[:, i] & leg[:, j]
        n = int(m.sum())
        ti, tj = trk[m, i], trk[m, j]
        k0 = int((~ti & ~tj).sum())
        k1 = int((ti ^ tj).sum())
        k2 = int((ti & tj).sum())
        e = EPS_MM
        # with chamber efficiency e: a true 2-track event shows 2 (e²), 1 (2e(1-e)) or 0 ((1-e)²) tracks
        f2e = k2 * e * e / n
        f1e = (k1 * e + k2 * 2 * e * (1 - e)) / n
        rec = dict(trig_hz=r3(n / live), trig_per_day=r3(n / live * 86400), trig_per_night=r3(n / live * 3600 * NIGHT_H),
                   frac0=r3(k0 / n), frac1=r3(k1 / n), frac2=r3(k2 / n),
                   frac2_eps=r3(f2e), frac1_eps=r3(f1e), frac0_eps=r3(1 - f2e - f1e), n_mc=n)
        s = m & trk[:, i] & trk[:, j]
        ci, cj = z['c_all'][s, i].astype(float), z['c_all'][s, j].astype(float)
        cos = (ci * cj).sum(1) / (np.linalg.norm(ci, axis=1) * np.linalg.norm(cj, axis=1))
        th = np.degrees(np.arccos(np.clip(cos, -1, 1)))     # the analysis' opening angle (vertex at the spot)
        mu = z['mu_d'][s].astype(float)
        zen = np.degrees(np.arccos(np.clip(np.abs(mu[:, 2]) / np.linalg.norm(mu, axis=1), 0, 1)))
        t_i, t_j = z['t_sipm'][s, i].astype(float), z['t_sipm'][s, j].astype(float)
        sm = rng.normal(0, SIG_T, (len(t_i), 2))
        # Δt = t(second arm) - t(first arm): vertical pair lower (3) minus upper (2); horizontal −x (1) minus +x (0)
        dt_true = t_j - t_i
        dt = dt_true + sm[:, 1] - sm[:, 0]
        ok_t = np.isfinite(dt)
        d0 = z['d_dom'][s, i].astype(float)
        c0 = z['c_dom'][s, i].astype(float)
        dca_true = G.dca0(np.nan_to_num(c0), np.nan_to_num(d0, nan=1.0))
        d15 = G.smear_dir(np.nan_to_num(d0, nan=1.0), 15.0, rng)
        dca15 = G.dca0(np.nan_to_num(c0), d15)
        d3 = G.smear_dir(np.nan_to_num(d0, nan=1.0), 3.0, rng)
        dca3 = G.dca0(np.nan_to_num(c0), d3)
        sc = 86400 / live
        rec.update(n_2trk=int(s.sum()), per_day_2trk=r3(s.sum() * sc),
                   per_day_125_160=r3(((th >= 125) & (th < 160)).sum() * sc),
                   frac_125_160=r3(((th >= 125) & (th < 160)).mean()),
                   theta=hist(th, edges_th, scale=sc), zenith=hist(zen, edges_z, scale=sc),
                   dt=hist(dt[ok_t], edges_dt, scale=sc), dt_true_mean=r3(np.nanmean(dt_true)),
                   dt_true_median_abs=r3(np.nanmedian(np.abs(dt_true))),
                   dca_true=hist(dca_true, edges_d, scale=sc), dca_15=hist(dca15, edges_d, scale=sc),
                   dca_3=hist(dca3, edges_d, scale=sc),
                   frac_dca15_pass=r3((dca15 < G.seg_D(15.0)).mean()), frac_dca3_pass=r3((dca3 < G.seg_D(3.0)).mean()),
                   zen_median=r3(np.median(zen)))
        if name == 'vert':
            rec['frac_downward'] = r3((dt_true[ok_t] > 0).mean())
        pairs[name] = rec
    out['pairs'] = pairs
    out['cnt'] = dict(leg_arm=z['cnt_leg_arm'].tolist(), ok_arm=z['cnt_ok_arm'].tolist())
    return out


# --------------------------------------------------------------------------- γ singles from the target
def gamma_rates(ep):
    y = SN.yields(TGT, ep, li_ug=LI_UG)
    pps = 1e-6 / SN.OG.LR.E_CHARGE
    g0, g1, f17 = y['Y_g0'] * pps, y['Y_g1'] * pps, y['frac_17_64']
    return {18.15: g0 * (1 - f17), 17.64: g0 * f17, 15.1: g1 * (1 - f17), 14.6: g1 * f17}, y


def singles(cos):
    z = np.load(PRED / GAM_FILE)
    ngen = int(z['cnt_n_generated'])
    lines = np.array([14.6, 15.1, 17.64, 18.15])
    nline = ngen / len(lines)
    leg, mm, E, line = z['leg'], z['mm'], z['E'], z['line']
    se, nd = z['seg_e'], z['seg_n_dom']
    out = {}
    p = {}
    for L in lines:
        lm = np.isclose(line, L, atol=1e-3)
        pl = np.array([leg[lm, a].sum() / nline for a in (0, 1)]).mean()
        pt = np.array([(leg[lm, a] & mm[lm, a]).sum() / nline for a in (0, 1)]).mean()
        p[float(L)] = (pl, pt, int(leg[lm, 0].sum() + leg[lm, 1].sum()))
    out['p_leg_per_gamma'] = {str(k): r3(v[0]) for k, v in p.items()}
    out['p_track_given_leg'] = {str(k): r3(v[1] / v[0]) for k, v in p.items()}
    cos_side = np.mean([cos['arms'][a]['leg_hz'] for a in (0, 1)])
    cos_top = np.mean([cos['arms'][a]['leg_hz'] for a in (2, 3)])
    cos_side_trk = np.mean([cos['arms'][a]['ok_hz'] for a in (0, 1)])
    eds = np.arange(0, 40.01, 1.0)
    per_ep = {}
    for ep in (441.0, 1100.0):
        R, y = gamma_rates(ep)
        legs = sum(R[L] * p[L][0] for L in R)
        trks = sum(R[L] * p[L][1] for L in R)
        # single-arm energy (raw Geant4 deposit, all layers of the arm) of the beam legs, weighted per line
        w = np.zeros(len(line))
        for L in R:
            w[np.isclose(line, L, atol=1e-3)] = R[L] / nline
        hs = {}
        for tag, sel in (('leg', lambda a: leg[:, a]), ('leg_track', lambda a: leg[:, a] & mm[:, a])):
            x = np.concatenate([E[sel(a), a] for a in (0, 1)])
            ww = np.concatenate([w[sel(a)] for a in (0, 1)]) / 2
            hs[tag] = hist(x, eds, w=ww)
        per_ep[str(int(ep))] = dict(
            gamma_per_s={str(k): r3(v) for k, v in R.items()}, g0_per_s=r3(R[18.15] + R[17.64]),
            beam_leg_hz_per_uA=r3(legs), beam_track_hz_per_uA=r3(trks), frac_track=r3(trks / legs),
            frac_track_eps=r3(trks / legs * EPS_MM),
            total_leg_hz_1uA_side=r3(legs + cos_side), total_leg_hz_1uA_top=r3(legs + cos_top),
            beam_over_cosmic_side=r3(legs / cos_side), E_hist=hs,
            accidental_pairs_per_day_1uA=r3(G.TWO_TAU_S * (legs + cos_side) ** 2 * 3600 * TAE.BEAM_DAY_H))
        if ep == 1100.0:
            per_ep[str(int(ep))]['scan'] = [dict(I_uA=I, leg_hz=r3(legs * I + cos_side),
                                                 track_frac=r3((trks * I + cos_side_trk) / (legs * I + cos_side)))
                                            for I in (0.0, 0.05, 0.1, 0.2, 0.5, 1.0)]
        else:
            per_ep[str(int(ep))]['scan'] = [dict(I_uA=I, leg_hz=r3(legs * I + cos_side),
                                                 track_frac=r3((trks * I + cos_side_trk) / (legs * I + cos_side)))
                                            for I in (0.0, 0.05, 0.1, 0.2, 0.5, 1.0)]
    out['ep'] = per_ep
    out['cos_side_leg_hz'] = r3(cos_side)
    out['cos_top_leg_hz'] = r3(cos_top)
    out['cos_side_track_frac'] = r3(cos_side_trk / cos_side)
    # cosmic single-arm energy of ok arms (leg + MM track), for the same plot: L15 sel singles
    fl = sorted((W / 'sel_l15').glob('L15_cosmicdisk_ta4arm_c*_sel.npz'))
    xs, ng = [], 0
    for f in fl:
        zz = np.load(f, allow_pickle=True)
        ng += int(zz['cnt_n_generated'])
        a = zz['sg_arm']
        xs.append(zz['sg_E'][(a == 0) | (a == 1)])
    if xs:
        live = ng * MU_LIVE
        out['cos_E_hist_leg_track'] = hist(np.concatenate(xs), eds, scale=1 / live / 2)
    out['lines_gamma_per_line'] = int(nline)
    return out


# --------------------------------------------------------------------------- beam pairs
COMP = {'sig': 'X17 at R(ATOMKI)', 'M1': 'M1 IPC', 'E1': 'E1 IPC', 'g1': '15.1/14.6 MeV IPC', 'epc': 'external conversions',
        'cos': 'cosmics'}


def beam_pairs(pair='horiz'):
    T.set_pair(pair)
    SN.register_levels()
    ec = SN.window('asb', RESP)
    out = dict(ewin=list(ec), level=LEVEL, resp=RESP, pair=pair)
    eth = np.arange(0, 181, 5.0)
    eE = np.arange(0, 30.01, 0.5)
    ey = np.arange(0, 1.0001, 0.05)
    for ep in (441.0, 1100.0):
        d = {}
        for lev in ('trigger', LEVEL):
            ev = SN.collect(TGT, 'asb', ep, RESP, level=lev, I_uA=1.0, live=SN.LIVE_S2 * BD, li_ug=LI_UG,
                            erange=(3.0, 40.0))
            th, E, yy, w, comp = ev['v0']['th'], ev['v0']['E'], np.abs(ev['v0']['y']), ev['w'], ev['comp']
            win = (E > ec[0]) & (E < ec[1])
            r = {}
            for c in COMP:
                m = comp == c
                r[c] = dict(per_day=r3(w[m].sum()), per_day_gt90=r3(w[m & (th > 90)].sum()),
                            per_day_win_gt90=r3(w[m & win & (th > 90)].sum()),
                            per_day_win_125_160=r3(w[m & win & (th >= 125) & (th < 160)].sum()),
                            n_mc=int(m.sum()), n_mc_win_gt90=int((m & win & (th > 90)).sum()))
                if lev == LEVEL:
                    r[c]['theta_win'] = hist(th[m & win], eth, w=w[m & win])
                    r[c]['theta_all'] = hist(th[m], eth, w=w[m])
                    r[c]['Esum_gt90'] = hist(E[m & (th > 90)], eE, w=w[m & (th > 90)])
                    r[c]['y_win_gt90'] = hist(yy[m & win & (th > 90)], ey, w=w[m & win & (th > 90)])
            d['trigger' if lev == 'trigger' else 'ref'] = r
            d['g0_per_day'] = r3(ev['meta']['g0_per_day'])
        out[str(int(ep))] = d
    return out


def main():
    cos = cosmics()
    sg = singles(cos)
    bp = beam_pairs('horiz')
    res = dict(made='2026-11-27', beam_day_h=TAE.BEAM_DAY_H, epc_run=os.environ.get('TA_EPC_RUN', ''), target=TGT, target_name=SN.SG.SHAPES.get(TGT, (TGT,))[0], li_ug=LI_UG, eps_mm=EPS_MM, sigma_t_ns=SIG_T, night_h=NIGHT_H,
               seg_D_15=r3(G.seg_D(15.0)), seg_D_3=r3(G.seg_D(3.0)),
               cosmics=cos, singles=sg, pairs=bp, comp_names=COMP)
    # cosmics after the full analysis (E_sum window, pointing + 0.6 ns TOF): the reach pass's own numbers
    import pandas as pd
    sr = pd.read_csv(OUT / f"summary_rates{os.environ.get('PASS', '_pass4')}li11.csv")
    for name in PAIRS:
        r = sr[(sr.pair == name) & (sr.comp == 'cos') & (sr.Ep_keV == 1100.0)]
        for ew in ('win', 'none'):
            q = r[r.ewin == ew]
            if len(q):
                cos['pairs'][name][f'ref_{ew}_125_160'] = r3(float(q['125-160'].iloc[0]))
                cos['pairs'][name][f'ref_{ew}_125_160_nmc'] = int(q['nmc_125-160'].iloc[0])
                cos['pairs'][name][f'ref_{ew}_all'] = r3(float(q['all'].iloc[0]))
    # yield-free ratio: selected 441 keV pairs per beam single-arm leg (cancels the film's Li content)
    e441 = bp['441']['ref']
    sel441 = sum(e441[c]['per_day_win_gt90'] or 0 for c in ('M1', 'E1', 'g1', 'epc'))
    legs441 = sg['ep']['441']['beam_leg_hz_per_uA'] * 3600 * TAE.BEAM_DAY_H * SN.LIVE_S2
    res['ratio_pairs_per_leg_441'] = r3(sel441 / legs441)
    (OUT / 'predictions.json').write_text(json.dumps(res, ensure_ascii=False, indent=0), encoding='utf-8')
    print('wrote', OUT / 'predictions.json')
    for k, v in cos['pairs'].items():
        print(f"cosmics {k}: trig {v['trig_hz']} Hz, 0/1/2 trk {v['frac0']}/{v['frac1']}/{v['frac2']} "
              f"(×ε {v['frac0_eps']}/{v['frac1_eps']}/{v['frac2_eps']}), 2trk/day {v['per_day_2trk']}, "
              f"125-160 {v['per_day_125_160']}")
    for a in cos['arms']:
        print('cos arm', a)
    for ep, v in sg['ep'].items():
        print(f"singles {ep}: beam legs {v['beam_leg_hz_per_uA']} Hz/µA/arm, track frac {v['frac_track']}, "
              f"beam/cos {v['beam_over_cosmic_side']}, acc/day {v['accidental_pairs_per_day_1uA']}")
    for ep in ('441', '1100'):
        for lev in ('trigger', 'ref'):
            print(ep, lev, {c: (v['per_day'], v['per_day_win_gt90']) for c, v in bp[ep][lev].items()})
    print('pairs per leg at 441:', res['ratio_pairs_per_leg_441'])


if __name__ == '__main__':
    main()
