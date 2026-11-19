#!/usr/bin/env python3
"""
geom_syst.py -- does a wrong geometry fake (or hide) an X17 in the two-arm fit?

The reference fit (two_arm_nd.py = FEASIBILITY_SIM §19 on one arm pair) floats a cubic acceptance in θ, the M1/E1/γ₁
normalisations, the angular-resolution and E_sum scales, per-arm gains and a 2 % + 1 % Gaussian-process "unknown
structure".  Those are generic.  Here the background is distorted by a *specific* mismodelling and the linearised fit
bias is computed (lnl_nd.fisher_nd's mismodelling term): the data are the distorted background, the templates the
nominal ones, and

    bias(p) = (T F + P)^-1 T b,   b = Σ_bins g Δ / μ          (T = live days of signal running)

so 'r bias' is the fake X17 signal, in units of R(ATOMKI), that the distortion produces.

Distortions (applied to every Geant4 table at load time, through lnl_geant._combine):
  * the reconstruction origin (beam spot / target) off by d along the beam, in the pair's plane, out of it;
  * one arm (the pair's first) displaced radially or along the beam;
  * both arms' radius scaled (a global distance error);
  * a dead 10 mm band in one Micromegas (an acceptance hole: events with that arm's centroid in the band are lost).
θ' = θ + [angle(c1 - dV + dA, c2 - dV + dA') - angle(c1, c2)] from the Micromegas charge centroids (c_dom), so every
other part of the reconstruction is kept.  The selection is not redone (pointing cut, trigger): only θ moves.

    WORK_DATA=/media/ucla/work ~/PycharmProjects/nTof_x17/.venv/bin/python sim2arm/geom_syst.py --pairs horiz vert
        -> out/geom_syst.csv
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import two_arm_nd as TA      # noqa: E402

SN, G, N = TA.SN, TA.G, TA.N
BEAM = np.array([0.0, 1.0, 0.0])          # the beam axis in the Geant4 frame (arms at ±x and ±z, MM centroids r ≈ 240 mm)
DIST = None                               # the active distortion (dict) or None


def _ang(a, b):
    c = (a * b).sum(1) / np.linalg.norm(a, axis=1) / np.linalg.norm(b, axis=1)
    return np.degrees(np.arccos(np.clip(c, -1, 1)))


def distort(z):
    if DIST is None or 'c_dom1' not in z or len(z['reco_c']) == 0:
        return z
    z = dict(z)
    c1, c2 = np.asarray(z['c_dom1'], float).copy(), np.asarray(z['c_dom2'], float).copy()
    a1, a2 = np.asarray(z['a1']), np.asarray(z['a2'])
    th0 = _ang(c1, c2)
    d = DIST
    if 'dV' in d:                                     # reconstruction origin off: centroids seen from the wrong point
        c1 -= d['dV']
        c2 -= d['dV']
    if 'arm' in d:                                    # one arm displaced: its centroids are elsewhere
        for c, a in ((c1, a1), (c2, a2)):
            m = a == d['arm']
            c[m] += d['dA']
    if 'scale' in d:
        c1 *= d['scale']
        c2 *= d['scale']                              # (a common scale leaves angles unchanged: kept as a check)
    if 'rscale_arm' in d:                             # one arm's distance scaled
        for c, a in ((c1, a1), (c2, a2)):
            m = a == d['rscale_arm']
            c[m] *= d['rscale']
    reco = np.asarray(z['reco_c'], float) + (_ang(c1, c2) - th0)
    if 'band' in d:                                   # a dead band (along the beam coordinate) in one arm
        arm, lo, hi = d['band']
        for c, a in ((np.asarray(z['c_dom1'], float), a1), (np.asarray(z['c_dom2'], float), a2)):
            m = (a == arm) & (c @ BEAM >= lo) & (c @ BEAM < hi)
            reco[m] = -999.0
    z['reco_c'] = reco.astype(np.float32)
    return z


def set_pair(name):
    TA.set_pair(name)
    G._combine = lambda zs: distort(TA.combine_pair(zs))


def collect(pair, resp, level, ep=1100.0):
    set_pair(pair)
    SN.register_levels()
    ec = SN.window('asb', resp)
    an = N.analyses(ec)[SN.REF_AN]
    ev = SN.collect('ogCu200', 'asb', ep, resp, level=level, I_uA=1.0, live=SN.LIVE_S2, transplant=False, li_ug=TA.LI_UG)
    SN._drop_tables()
    return ev, an


def distortions(pair):
    p, q = TA.PAIRS[pair]
    r0 = {0: [1, 0, 0], 1: [-1, 0, 0], 2: [0, 0, 1], 3: [0, 0, -1]}
    rad = np.array(r0[p], float)                      # the first arm's outward direction
    perp = np.cross(BEAM, rad)                        # out of the pair's plane
    mm = 2.0
    out = {
        f'origin along beam {mm:g} mm': dict(dV=mm * BEAM),
        f'origin toward arm {p} {mm:g} mm': dict(dV=mm * rad),
        f'origin out of plane {mm:g} mm': dict(dV=mm * perp),
        f'arm {p} radial +{mm:g} mm': dict(arm=p, dA=mm * rad),
        f'arm {p} along beam {mm:g} mm': dict(arm=p, dA=mm * BEAM),
        f'arm {p} distance +1 %': dict(rscale_arm=p, rscale=1.01),
        f'arm {p} dead band 10 mm at centre': dict(band=(p, -5.0, 5.0)),
        f'arm {p} dead band 10 mm at +60 mm': dict(band=(p, 55.0, 65.0)),
    }
    return out


def bias_rows(pair, resp, level, days, structs):
    global DIST
    DIST = None
    ev0, an = collect(pair, resp, level)
    v0 = ev0['v0']
    bk = ev0['grp'] != 'sig'
    rows = []
    fits = {}
    for st in structs:
        F, P, names, out = N.fisher_nd(ev0, an, N.STRUCTS[st], sigma_g=SN.S.PRIOR_G, templates=True)
        fits[st] = (F, P, names, out)
    for dname, d in distortions(pair).items():
        DIST = d
        ev1, _ = collect(pair, resp, level)
        DIST = None
        assert len(ev1['w']) == len(ev0['w']), 'event lists differ: the distortion changed the selection'
        th1 = ev1['v0']['th']
        dth = (th1 - v0['th'])[bk & (th1 > 0)]
        b0 = N.Binner(an, v0, True)
        b1 = N.Binner(an, ev1['v0'], True)
        dl = b1.apply(np.where(bk, ev1['w'], 0.0)) - b0.apply(np.where(bk, ev0['w'], 0.0))   # Δμ per day
        lost = float(ev0['w'][bk & (th1 < 0)].sum() / ev0['w'][bk].sum())
        for st, (F, P, names, out) in fits.items():
            g, mu = out['g'], out['mu']
            ok = mu > mu.max() * 1e-9
            b = g[:, ok] @ (dl[ok] / mu[ok])
            chi2_day = float(dl[ok] @ (dl[ok] / mu[ok]))
            for T in days:
                C = np.linalg.inv(T * F + P)
                bias = C @ (T * b)
                sig_r = float(np.sqrt(C[0, 0]))
                # χ² of the distortion left after the fit absorbs it (how visible it is in the data)
                rows.append(dict(pair=pair, resp=resp, level=level, struct=st, distortion=dname, days=T,
                                 mean_dtheta_deg=float(np.mean(dth)) if dth.size else 0.0,
                                 rms_dtheta_deg=float(np.sqrt(np.mean(dth ** 2))) if dth.size else 0.0,
                                 lost_frac=lost, r_bias=float(bias[0]), sigma_r=sig_r, bias_over_sigma=float(bias[0]) / sig_r,
                                 chi2_raw=T * chi2_day, chi2_after=float(T * chi2_day - (T * b) @ C @ (T * b)),
                                 nbins=int(ok.sum())))
        print(f'{pair} {dname:38s} <dθ> {rows[-1]["mean_dtheta_deg"]:+.3f}°  '
              + '  '.join(f'{r["struct"]}: r {r["r_bias"]:+.3f} ({r["bias_over_sigma"]:+.2f}σ)'
                          for r in rows[-len(fits) * len(days):] if r['days'] == days[-1]), flush=True)
        SN._drop_tables()
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pairs', nargs='+', default=['horiz', 'vert'])
    ap.add_argument('--resp', default='LNL calibrated')
    ap.add_argument('--level', default='MM 15° + TOF')
    ap.add_argument('--days', nargs='+', type=float, default=[5.0])
    ap.add_argument('--structs', nargs='+', default=['none', SN.REF_STRUCT])
    ap.add_argument('--out', default=str(TA.OUT / 'geom_syst.csv'))
    a = ap.parse_args()
    rows = []
    for p in a.pairs:
        rows += bias_rows(p, a.resp, a.level, a.days, a.structs)
    pd.DataFrame(rows).to_csv(a.out, index=False)
    print('->', a.out)


if __name__ == '__main__':
    main()
