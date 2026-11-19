#!/usr/bin/env python3
"""
cosmic_rates.py -- two-arm cosmic coincidences per live day, per pair of arms: L4 (3 x 3 m plane, 1.5 m up) against
L15 (disk normal to each track, every zenith angle), at the table level (trigger leg + Micromegas in the active area,
any opening angle) and in the 125-160 deg band.  Also the vertical pair's opening-angle distribution (the 'MEG II peak').

    WORK_DATA=/media/dylan/data/work python3 sim2arm/cosmic_rates.py      -> out/cosmic_rates.csv, out/cosmic_theta.csv
"""
from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
W = Path(os.environ.get('WORK_DATA', '/media/dylan/data/work')) / 'x17_facility_search'
MU_LIVE_PLANE = 60.0 / (300.0 * 300.0)
MU_LIVE_DISK = 60.0 / (4 * np.pi / 3 * 90.0 ** 2)
PAIRS = {'vert': (2, 3), 'horiz': (0, 1), 'adj': (0, 2), 'adj_lo': (0, 3), 'adj_b': (1, 2), 'adj_b_lo': (1, 3)}
KEYS = ('a1', 'a2', 'reco_c', 'E1', 'E2')


def load(files, live_per_mu):
    zs = [np.load(f, allow_pickle=True) for f in files]
    z = {k: np.concatenate([np.asarray(x[k]) for x in zs]) for k in KEYS}
    ngen = sum(int(x['cnt_n_generated']) for x in zs)
    return z, ngen * live_per_mu / 86400.0


def main():
    samples = {'L4 plane': (sorted((W / 'sel_v3').glob('L4_cosmic_sel.npz')), MU_LIVE_PLANE),
               'L15 disk': (sorted({f.name: f for d in ('sel_l15', 'sel_l15.new') if (W / d).is_dir() for f in (W / d).glob(
                   'L15_cosmicdisk_ta4arm_c*_sel.npz')}.values()), MU_LIVE_DISK)}
    rows, th = [], []
    edges = np.arange(0, 181, 5.0)
    for name, (fl, lpm) in samples.items():
        if not fl:
            continue
        z, days = load(fl, lpm)
        a = np.sort(np.c_[z['a1'], z['a2']], 1)
        for p, (i, j) in PAIRS.items():
            m = (a[:, 0] == i) & (a[:, 1] == j)
            w = m & (z['reco_c'] >= 125) & (z['reco_c'] < 160)
            rows.append(dict(sample=name, pair=p, live_days=days, n_mc=int(m.sum()), per_day=m.sum() / days,
                             n_mc_125_160=int(w.sum()), per_day_125_160=w.sum() / days))
            if p in ('vert', 'horiz'):
                h = np.histogram(z['reco_c'][m], edges)[0]
                for k in range(len(h)):
                    th.append(dict(sample=name, pair=p, th_lo=edges[k], th_hi=edges[k + 1], per_day=h[k] / days,
                                   n_mc=int(h[k])))
    df = pd.DataFrame(rows)
    df.to_csv(HERE / 'out' / 'cosmic_rates.csv', index=False)
    pd.DataFrame(th).to_csv(HERE / 'out' / 'cosmic_theta.csv', index=False)
    with pd.option_context('display.width', 200):
        print(df.round(1))


if __name__ == '__main__':
    main()
