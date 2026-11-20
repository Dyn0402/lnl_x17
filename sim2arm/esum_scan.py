#!/usr/bin/env python3
"""
esum_scan.py -- days to 3σ against the E_sum window for the built Cu hemisphere (dome300), horizontal pair,
MM 15° + TOF, 11 µm, direct and transplant (lnl_x17, 2026-11-20).  The reference windows (lnl_calo, per response)
were set on the Li₂O baseline; the hemisphere's 300 µm wall and rim move E_sum down by ~1 MeV.

    WORK_DATA=/media/ucla/work LI_UG=587 python sim2arm/esum_scan.py -j 3   -> out/esum_scan_dome300.csv
"""
from __future__ import annotations

import argparse
import multiprocessing as mp
import os
import sys
from pathlib import Path

os.environ.setdefault('LI_UG', '587')
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pandas as pd           # noqa: E402

WINDOWS = [(11, 17), (12, 18), (13, 19), (12, 19), (11, 19), (14, 19)]
RESPS = ['LNL calibrated', 'n_TOF as is']


def one(args):
    import two_arm_nd as T
    resp, win, mc = args
    T.SN.C.BEST[(T.SN.SG.DETS['asb'], resp)] = win
    r = T.task(('horiz', T.CFG, resp, 'MM 15° + TOF', mc))
    return dict(resp=resp, win=f'{win[0]}-{win[1]}', mc=mc, days_floor=r.get('days_floor1'), days_raw=r.get('days_raw'),
                cnt_days=r.get('cnt_days_kde'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-j', type=int, default=3)
    a = ap.parse_args()
    tasks = [(r, w, m) for r in RESPS for w in WINDOWS for m in ('direct', 'transplant')]
    with mp.Pool(a.j) as p:
        rows = p.map(one, tasks, chunksize=1)
    df = pd.DataFrame(rows)
    piv = df.pivot_table(index=['resp', 'win'], columns='mc', values='days_floor')
    piv['central'] = (piv['direct'] * piv['transplant']) ** 0.5
    out = Path(__file__).resolve().parent / 'out' / 'esum_scan_dome300.csv'
    df.to_csv(out, index=False)
    print(piv.round(1).to_string())
    print('wrote', out)


if __name__ == '__main__':
    main()
