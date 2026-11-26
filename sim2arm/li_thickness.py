#!/usr/bin/env python3
"""
li_thickness.py -- what a ±50 % uncertainty on the thickness and uniformity of the Li film means for the slot-1 run
(lnl_x17, 2026-11-25; write-up slot1_feasibility/LI_THICKNESS.md).

The film: metallic Li on the inside of the built Cu hemisphere (dome300), nominal 11 µm = 587 µg/cm² (TARGET_REVIEW
§4.2).  We are told that whatever target is made, its thickness and homogeneity carry ~50 %.

    python3 sim2arm/li_thickness.py yields         # -> out/li_thickness/yields_*.csv   (system python is fine)
    .../nTof_x17/.venv/bin/python sim2arm/li_thickness.py reach -j 8   # -> out/li_thickness/reach.csv (the two-arm fit)
    python3 sim2arm/li_thickness.py figs           # -> out/li_thickness/*.png

yields: x17_facility_search target_model.layered_yield (PSTAR stopping, Zahnow 1995 cross sections, the two M1
  resonances as Breit-Wigners + the direct E1 remainder), per proton:
  * uniform films 2-24 µm at E_p 1.10 MeV, and at 441 keV (H2+ day) for E_p = 441-470 keV;
  * thickness x chemistry (the outer fraction of the Li atoms turned into LiOH, review_li_conversion.py);
  * non-uniform films across the beam spot: the spot-averaged yields for a thickness distribution with the same
    mean (Gaussian rms 25 / 50 %, flat ±50 %, a fraction of the spot on bare Cu, a gamma distribution).
reach: the reference two-arm fit (two_arm_nd.task: horizontal pair, MM 15° + 0.6 ns TOF, the built Cu hemisphere,
  1 µA, 1.10 MeV) with the film's yields replaced by each scenario (the Geant4 events stay those of the 20 µm run:
  leptons do not notice 10 µm of Li, 1e-5 X0).  M1, E1, γ1 norms float in the fit, so a changed capture mix only
  costs through its shape; the cosmics do not scale with the film.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):   # one core per worker (before numpy)
    os.environ.setdefault(_v, '1')
import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / 'out' / 'li_thickness'
OUT.mkdir(parents=True, exist_ok=True)
#: TA_EPC_RUN=L19: the external conversions of run L19 (x100) in the fit; outputs reach_l19*.csv, parts_l19/
SFX = '_' + os.environ['TA_EPC_RUN'].lower() if os.environ.get('TA_EPC_RUN') else ''
FS = Path(os.environ.get('X17FS', Path.home() / 'PycharmProjects' / 'x17_facility_search'))
sys.path.insert(0, str(FS / 'lnl' / 'target'))
sys.path.insert(0, str(FS / 'lnl'))
sys.path.insert(0, str(FS / 'ill'))

RHO_LI = 0.534                       # g/cm3
UG_PER_UM = RHO_LI * 1e-4 * 1e6      # 53.4 µg/cm² per µm
T0_UM = 11.0                         # nominal film
E_CH = 1.602176634e-19
M_LI = {'Li': 6.941, 'LiOH': 23.948, 'Li2O': 29.881 / 2}


def _tm():
    import target_model as TM      # noqa: E402
    return TM


def stack(t_um, x=0.0, prod='LiOH'):
    """t_um of Li metal (before conversion); the outer fraction x of its atoms converted to prod (beam side)."""
    TM = _tm()
    li = t_um * UG_PER_UM
    lay = []
    if x > 0:
        lay.append((TM.FILMS[prod]['comp'], li * x * M_LI[prod] / M_LI['Li']))
    if x < 1:
        lay.append((TM.FILMS['Li']['comp'], li * (1 - x)))
    return lay


def yield_row(ep, t_um, x=0.0, prod='LiOH'):
    TM = _tm()
    if t_um <= 0:
        return dict(Y_g0=0.0, Y_g1=0.0, f17=0.0, f18res=0.0, fdc=0.0, frac_g1_direct=0.0, E_out_keV=ep,
                    mean_Estar=np.nan, g0_17=0.0, g0_18=0.0, g0_dc=0.0)
    r = TM.layered_yield(ep, stack(t_um, x, prod))
    r.pop('dep_keV', None)
    g0 = r['Y_g0']
    r.update(g0_17=g0 * r['f17'], g0_18=g0 * r['f18res'], g0_dc=g0 * r['fdc'])
    return r


# --------------------------------------------------------------------------- #
# thickness distributions across the beam spot (same mean thickness t̄)
# --------------------------------------------------------------------------- #
def dist(kind, tbar, n=41):
    """(t_um nodes, weights) of a thickness distribution with mean tbar over the spot."""
    if kind == 'uniform':
        return np.array([tbar]), np.array([1.0])
    if kind.startswith('gauss'):                    # gauss25, gauss50: rms in % of the mean, truncated at 0
        s = float(kind[5:]) / 100 * tbar
        t = np.linspace(max(tbar - 4 * s, 0), tbar + 4 * s, n)
        w = np.exp(-0.5 * ((t - tbar) / s) ** 2)
        w /= w.sum()
        t *= tbar / (w * t).sum()                    # keep the mean after the truncation
        return t, w
    if kind == 'flat50':                             # flat from 0.5 to 1.5 x the mean
        t = np.linspace(0.5 * tbar, 1.5 * tbar, n)
        return t, np.full(n, 1.0 / n)
    if kind.startswith('holes'):                     # holes20: 20 % of the spot on bare Cu, the rest thicker
        h = float(kind[5:]) / 100
        return np.array([0.0, tbar / (1 - h)]), np.array([h, 1 - h])
    if kind == 'gamma4':                             # a skewed film (gamma, shape 4: rms 50 %)
        k = 4.0
        t = np.linspace(0.02, 4, 200) * tbar
        w = t ** (k - 1) * np.exp(-k * t / tbar)
        w /= w.sum()
        return t, w
    raise ValueError(kind)


@__import__('functools').lru_cache(maxsize=None)
def spot_yields(ep, kind, tbar, x=0.0):
    """spot-averaged yields: the absolute γ yields add, the fractions are those of the sum."""
    t, w = dist(kind, tbar)
    acc = {}
    for ti, wi in zip(t, w):
        r = yield_row(ep, ti, x)
        for k in ('Y_g0', 'Y_g1', 'g0_17', 'g0_18', 'g0_dc'):
            acc[k] = acc.get(k, 0.0) + wi * r[k]
        acc['g1_dir'] = acc.get('g1_dir', 0.0) + wi * r['Y_g1'] * r['frac_g1_direct']
        acc['Eout_w'] = acc.get('Eout_w', 0.0) + wi * r['E_out_keV']
    g0 = acc['Y_g0']
    return dict(Y_g0=g0, Y_g1=acc['Y_g1'], f17=acc['g0_17'] / g0, f18res=acc['g0_18'] / g0, fdc=acc['g0_dc'] / g0,
                frac_g1_direct=acc['g1_dir'] / acc['Y_g1'], E_out_mean_keV=acc['Eout_w'])


def per_uc(y):
    return y / (1e-6 / E_CH)        # per µC = per 6.24e12 protons


def cmd_yields(_a):
    import pandas as pd
    rows = []
    for ep in (1100.0, 1050.0, 1150.0):
        for t in np.r_[np.arange(2, 25, 1.0), 5.5, 8.25, 13.75, 16.5]:
            r = yield_row(ep, t)
            rows.append(dict(Ep_keV=ep, li_um=t, li_ug=t * UG_PER_UM, **{k: r[k] for k in (
                'Y_g0', 'Y_g1', 'f17', 'f18res', 'fdc', 'frac_g1_direct', 'E_out_keV', 'mean_Estar')}))
    d = pd.DataFrame(rows).sort_values(['Ep_keV', 'li_um'])
    y0 = d[(d.Ep_keV == 1100) & (d.li_um == T0_UM)].Y_g0.iloc[0]
    d['g0_rel_11um'] = d.Y_g0 / y0
    d['g0_per_uC'] = per_uc(d.Y_g0)
    d.to_csv(OUT / 'yields_vs_thickness.csv', index=False)
    print('1.10 MeV, uniform metal film:')
    print(d[(d.Ep_keV == 1100) & d.li_um.isin([2, 4, 5.5, 8.25, 11, 13.75, 16.5, 20, 24])][
        ['li_um', 'g0_rel_11um', 'E_out_keV', 'f17', 'f18res', 'fdc', 'mean_Estar']].round(4).to_string(index=False))

    # 441 keV (H2+): on the narrow resonance the thick-target yield does not depend on the film
    rows = []
    for ep in (441.0, 443.0, 445.0, 450.0, 460.0, 470.0, 500.0):
        for t in (1, 2, 3, 4, 5.5, 8.25, 11, 13.75, 16.5, 20):
            r = yield_row(ep, t)
            rows.append(dict(Ep_keV=ep, li_um=t, Y_g0=r['Y_g0'], f17=r['f17'], E_out_keV=r['E_out_keV']))
    q = pd.DataFrame(rows)
    q['rel_11um'] = q.Y_g0 / q.groupby('Ep_keV').Y_g0.transform(lambda s: s.iloc[list(q.loc[s.index].li_um).index(11)])
    q.to_csv(OUT / 'yields_441.csv', index=False)
    print('\n441 keV: gamma0 yield relative to 11 µm, by E_p (rows) and thickness (columns):')
    print(q.pivot(index='Ep_keV', columns='li_um', values='rel_11um').round(3).to_string())

    # thickness x chemistry
    rows = []
    for ep in (1100.0,):
        for t in (5.5, 8.25, 11, 13.75, 16.5):
            for x in (0, 0.25, 0.5, 0.75, 1.0):
                r = yield_row(ep, t, x)
                rows.append(dict(Ep_keV=ep, li_um=t, lioh=x, E_out_keV=r['E_out_keV'], f17=r['f17'],
                                 g0_rel_11um_fresh=r['Y_g0'] / y0))
    c = pd.DataFrame(rows)
    c.to_csv(OUT / 'yields_chemistry.csv', index=False)
    print('\n1.10 MeV: 17.64 MeV share of γ0 [%] (beam exit energy, keV) by thickness x LiOH fraction')
    c['cell'] = [f'{100 * f:.1f} % ({e:.0f})' for f, e in zip(c.f17, c.E_out_keV)]
    print(c.pivot(index='li_um', columns='lioh', values='cell').to_string())

    # non-uniform films
    rows = []
    for kind in ('uniform', 'gauss25', 'gauss50', 'flat50', 'gamma4', 'holes20', 'holes50'):
        for f in (0.5, 1.0, 1.5):
            for x in (0.0, 0.5, 1.0):
                r = spot_yields(1100.0, kind, f * T0_UM, x)
                rows.append(dict(kind=kind, tbar_rel=f, tbar_um=f * T0_UM, lioh=x, **r, g0_rel_11um=r['Y_g0'] / y0))
    u = pd.DataFrame(rows)
    u.to_csv(OUT / 'yields_nonuniform.csv', index=False)
    print('\n1.10 MeV, non-uniform films (fresh metal): γ0 relative to a uniform 11 µm film, 17.64 share, E1 share')
    print(u[u.lioh == 0][['kind', 'tbar_rel', 'g0_rel_11um', 'f17', 'fdc', 'E_out_mean_keV']].round(4).to_string(index=False))
    print('\n... the same with half / all of the Li as LiOH: 17.64 share')
    print(u.pivot_table(index=['kind', 'tbar_rel'], columns='lioh', values='f17').round(4).to_string())


# --------------------------------------------------------------------------- #
# the reach
# --------------------------------------------------------------------------- #
#: (name, distribution, mean thickness / 11 µm, LiOH fraction)
SCEN = [('t0.50', 'uniform', 0.50, 0.0), ('t0.625', 'uniform', 0.625, 0.0), ('t0.75', 'uniform', 0.75, 0.0),
        ('t0.875', 'uniform', 0.875, 0.0), ('t1.00', 'uniform', 1.00, 0.0), ('t1.25', 'uniform', 1.25, 0.0),
        ('t1.50', 'uniform', 1.50, 0.0), ('t0.375', 'uniform', 0.375, 0.0), ('t1.75', 'uniform', 1.75, 0.0),
        ('t2.00', 'uniform', 2.00, 0.0),
        ('gauss50', 'gauss50', 1.0, 0.0), ('flat50', 'flat50', 1.0, 0.0), ('holes50', 'holes50', 1.0, 0.0),
        ('gamma4', 'gamma4', 1.0, 0.0),
        ('t1.50_lioh50', 'uniform', 1.5, 0.5), ('t1.50_lioh75', 'uniform', 1.5, 0.75),
        ('t1.50_lioh100', 'uniform', 1.5, 1.0), ('t1.00_lioh100', 'uniform', 1.0, 1.0),
        ('gauss50_lioh75', 'gauss50', 1.0, 0.75), ('flat50_lioh100', 'flat50', 1.0, 1.0)]
SCEN_D = {s[0]: s[1:] for s in SCEN}


def reach_task(args):
    scen, resp, mc = args
    os.environ.setdefault('WORK_DATA', '/media/ucla/work')
    sys.path.insert(0, str(HERE))
    import two_arm_nd as TA
    kind, f, x = SCEN_D[scen]
    SN = TA.SN

    def fy(film, li_ug):           # the scenario's yields in shapes_nd's film_yields format
        r = spot_yields(TA.SN.OG.EP, kind, f * T0_UM, x)
        return dict(Y_g0=r['Y_g0'], Y_g1=r['Y_g1'], f17=r['f17'], f18res=r['f18res'], fdc=r['fdc'],
                    frac_g1_direct=r['frac_g1_direct'])
    SN.film_yields_t = fy
    TA.LI_UG = f * T0_UM * UG_PER_UM          # non-None routes through film_yields_t; printed as li_ug
    r = TA.task(('horiz', 'dome300', resp, 'MM 15° + TOF', mc))
    r['scen'] = scen
    r['kind'], r['tbar_rel'], r['lioh'] = kind, f, x
    return r


def cmd_reach(a):
    import hashlib
    import pickle
    import multiprocessing as mp
    import pandas as pd
    resps = ['LNL calibrated', 'n_TOF as is', 'LNL calibrated, LS off']
    tasks = [(s, r, m) for s in (a.scen or SCEN_D) for r in resps for m in ('direct', 'transplant')]
    pdir = OUT / f'parts{SFX}'
    pdir.mkdir(exist_ok=True)

    def key(t):
        return pdir / (hashlib.md5(repr(t).encode()).hexdigest()[:16] + '.pkl')
    todo = [t for t in tasks if not key(t).exists()]
    print(f'{len(tasks)} tasks, {len(todo)} to run', flush=True)
    if todo:
        with mp.get_context('fork').Pool(a.j, maxtasksperchild=1) as pool:
            for t, r in zip(todo, pool.imap(reach_task, todo)):
                key(t).write_bytes(pickle.dumps(r))
    rows = [pickle.loads(key(t).read_bytes()) for t in tasks]
    df = pd.DataFrame(rows)
    df.to_csv(OUT / f'reach{SFX}.csv', index=False)
    print('->', OUT / f'reach{SFX}.csv')
    summarize(df)


def r90(days3, T):
    """expected 90 % CL limit in units of R(ATOMKI) after T days of beam (TWO_ARM_STUDY §1.4)."""
    return 1.28 / (3 * np.sqrt(T / days3))


def summarize(df=None):
    import pandas as pd
    if df is None:
        df = pd.read_csv(OUT / f'reach{SFX}.csv')
    g = df.pivot_table(index=['scen', 'resp'], columns='mc', values='days_floor1')
    g['central'] = np.sqrt(g['direct'] * g['transplant'])
    g = g.reset_index()
    ref = g[g.scen == 't1.00'].set_index('resp')['central']
    g['rel_t1'] = g.central / g.resp.map(ref)
    g['R90_5d'] = r90(g.central, 5.0)
    g['R90_46h'] = r90(g.central, 46 / 24)
    m = df.groupby(['scen', 'resp']).agg(S_win=('S_win', 'mean'), Bbeam_win=('Bbeam_win', 'mean'),
                                          Bcos_win=('Bcos_win', 'mean'), g0_per_day=('g0_per_day', 'first'))
    g = g.merge(m.reset_index(), on=['scen', 'resp'])
    order = {s[0]: i for i, s in enumerate(SCEN)}
    g = g.sort_values(['resp', 'scen'], key=lambda c: c.map(order) if c.name == 'scen' else c)
    g.to_csv(OUT / f'reach_summary{SFX}.csv', index=False)
    pd.set_option('display.width', 220)
    print(g.round(3).to_string(index=False))
    return g


def cmd_figs(_a):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import pandas as pd
    d = pd.read_csv(OUT / 'yields_vs_thickness.csv')
    fig, ax = plt.subplots(1, 3, figsize=(13, 3.8))
    for ep, c in ((1050, '#888'), (1100, 'k'), (1150, '#4a7')):
        s = d[d.Ep_keV == ep]
        ax[0].plot(s.li_um, s.g0_rel_11um, c=c, label=f'E_p {ep / 1e3:.2f} MeV')
        ax[1].plot(s.li_um, s.E_out_keV, c=c)
        ax[2].plot(s.li_um, 100 * s.fdc, c=c)
    for a_ in ax:
        a_.axvspan(5.5, 16.5, color='#fc3', alpha=0.25, lw=0)
        a_.axvline(11, c='#c80', lw=1)
        a_.set_xlabel('Li metal film [µm]')
    ax[0].set_ylabel('γ₀ yield / 11 µm at 1.10 MeV')
    ax[0].legend(frameon=False, fontsize=8)
    ax[1].set_ylabel('beam energy leaving the film [keV]')
    ax[1].axhline(441, c='r', lw=0.8, ls='--')
    ax[2].set_ylabel('direct (E1) share of γ₀ [%]')
    fig.tight_layout()
    fig.savefig(OUT / 'yields_vs_thickness.png', dpi=130)
    print('->', OUT / 'yields_vs_thickness.png')
    f = OUT / f'reach_summary{SFX}.csv'
    if f.exists():
        g = pd.read_csv(f)
        u = g[g.scen.str.match(r'^t[0-9.]+$')].copy()
        u['t'] = u.scen.str[1:].astype(float) * T0_UM
        fig, ax = plt.subplots(1, 2, figsize=(9.5, 3.8))
        for resp, c in (('LNL calibrated', 'k'), ('n_TOF as is', '#c80'), ('LNL calibrated, LS off', '#888')):
            s = u[u.resp == resp].sort_values('t')
            ax[0].plot(s.t, s.central, 'o-', c=c, label=resp)
            ax[1].plot(s.t, s.R90_46h, 'o-', c=c)
        for a_ in ax:
            a_.axvspan(5.5, 16.5, color='#fc3', alpha=0.25, lw=0)
            a_.set_xlabel('Li metal film [µm] (uniform)')
        ax[0].set_ylabel('days of beam to 3σ at R(ATOMKI)')
        ax[0].legend(frameon=False, fontsize=8)
        ax[1].set_ylabel('expected 90 % limit, 46 h [× R(ATOMKI)]')
        fig.tight_layout()
        fig.savefig(OUT / f'reach_vs_thickness{SFX}.png', dpi=130)
        print('->', OUT / f'reach_vs_thickness{SFX}.png')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('what', choices=['yields', 'reach', 'summary', 'figs'])
    ap.add_argument('-j', type=int, default=6)
    ap.add_argument('--scen', nargs='+')
    a = ap.parse_args()
    {'yields': cmd_yields, 'reach': cmd_reach, 'summary': lambda _: summarize(), 'figs': cmd_figs}[a.what](a)


if __name__ == '__main__':
    main()
