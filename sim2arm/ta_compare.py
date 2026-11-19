#!/usr/bin/env python3
"""
ta_compare.py -- run L16: two arms rotated about the beam to an angle dphi between their normals (180 = opposite).
Per configuration and per sample (X17 m16.8, M1 / E1 IPC 18.15), the selected fraction per generated event in the
fit region (theta_reco >= 90 deg, the response's E_sum window, analysis level), compared with the opposite pair of the
four-arm tables (L11 + L13, horizontal pair 0-1, the same cuts).

The days of the full fit are then scaled as a counting experiment: days(dphi) ~ days(opp) * (B / B_opp) / (S / S_opp)^2,
with B the IPC sum weighted by the opposite pair's own M1 / E1 mix in the fit region at 1.10 MeV.  An estimate: the fit
uses the shapes too, the 15.1 MeV IPC and EPC are not simulated rotated.

    WORK_DATA=/media/dylan/data/work python3 sim2arm/ta_compare.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import two_arm_nd as T     # noqa: E402

import numpy as np         # noqa: E402
import pandas as pd        # noqa: E402

G, C, SN = T.G, T.C, T.SN
L16 = Path(os.environ.get('L16_SEL', T._W / 'sel_l16'))
LEVELS = ['trigger', 'MM 15° point, μ 3°', 'MM 15° + TOF']
RESPS = ['LNL calibrated', 'n_TOF as is']
SAMPLES = {'x17': 'X17_m16.8', 'M1': 'M1_18.15', 'E1': 'E1_18.15'}


def load_l16(sample, dphi):
    fl = sorted(L16.glob(f'L16_{sample}_ta{dphi}_asb_c*_sel.npz'))
    if not fl:
        return None
    z = T._COMBINE0([dict(np.load(f, allow_pickle=True)) for f in fl])
    z['ngen'] = int(z['cnt_n_generated'])
    z['name'] = f'L16_{sample}_ta{dphi}'
    z['Esum'] = z['E1'] + z['E2']
    return z


def frac(z, resp, level):
    zz = C.respond(z, 'as built', resp, seed=11)
    ec = SN.window('asb', resp)
    m = G.select(zz, level, ec) & (zz['reco_c'] >= 90)
    w = (zz['reco_c'] >= 125) & (zz['reco_c'] < 160)
    return m.sum() / z['ngen'], (m & w).sum() / z['ngen'], int(m.sum())


def main():
    T.set_pair('horiz')
    SN.register_levels()
    rows = []
    for resp in RESPS:
        C.set_response(resp, sigma_g='auto')
        ref = {k: SN.table('ogCu200', k, 'asb', resp) for k in SAMPLES}
        for level in LEVELS:
            fr = {k: frac(ref[k], resp, level) for k in SAMPLES}
            rows.append(dict(dphi='180 (4-arm tables, pair 0-1)', resp=resp, level=level,
                             **{f'f_{k}': v[0] for k, v in fr.items()}, **{f'fwin_{k}': v[1] for k, v in fr.items()},
                             **{f'n_{k}': v[2] for k, v in fr.items()}))
            for dphi in (180, 160, 140, 120):
                zs = {k: load_l16(s, dphi) for k, s in SAMPLES.items()}
                if zs['x17'] is None:
                    continue
                r = dict(dphi=str(dphi), resp=resp, level=level)
                for k, z in zs.items():
                    if z is None:
                        continue
                    v = frac(z, resp, level)
                    r.update({f'f_{k}': v[0], f'fwin_{k}': v[1], f'n_{k}': v[2]})
                rows.append(r)
    df = pd.DataFrame(rows)
    # counting scaling against the 4-arm-table opposite pair, the IPC mixed as the reference fit region at 1.10 MeV
    sp = HERE / 'out' / 'two_arm_spectra_pass1.csv'
    mixE1 = 0.83
    if sp.exists():
        s = pd.read_csv(sp)
        g = s[(s['pair'] == 'horiz') & (s['Ep_keV'] == 1100) & (s['ewin'] == 'win') & (s['level'] == 'MM 15° + TOF')
              & (s['resp'] == 'LNL calibrated') & (s['th_lo'] >= 90)]
        e1, m1 = g[g['comp'] == 'E1']['rate_per_day'].sum(), g[g['comp'] == 'M1']['rate_per_day'].sum()
        if e1 + m1 > 0:
            mixE1 = e1 / (e1 + m1)
    out = []
    for (resp, level), g in df.groupby(['resp', 'level'], sort=False):
        r0 = g.iloc[0]
        for _, r in g.iterrows():
            sx = r['f_x17'] / r0['f_x17']
            b = (mixE1 * r.get('f_E1', np.nan) / r0['f_E1'] + (1 - mixE1) * r.get('f_M1', np.nan) / r0['f_M1'])
            out.append(dict(r, S_ratio=sx, B_ratio=b, days_factor=b / sx ** 2, mixE1=mixE1))
    out = pd.DataFrame(out)
    out.to_csv(HERE / 'out' / 'ta_compare.csv', index=False)
    with pd.option_context('display.width', 250, 'display.max_columns', 20):
        print(out[['dphi', 'resp', 'level', 'f_x17', 'f_M1', 'f_E1', 'n_x17', 'n_M1', 'n_E1', 'S_ratio', 'B_ratio',
                   'days_factor']].round(5))


if __name__ == '__main__':
    main()
