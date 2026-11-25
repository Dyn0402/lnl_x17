#!/usr/bin/env python3
"""
combine_l19.py -- the L19 per-job pair tables (run_job_epc.sh, DROP_SG) -> one table as shapes_nd reads it.

    rsync/xrdcp lxplus:/eos/experiment/ntof/data/x17/lnl/L19/gam_8Be_dome300_asb/sel/ -> $WORK_DATA/x17_facility_search/sel_l19_jobs/<run>/
    python3 sim2arm/combine_l19.py [--run L19] [--min-jobs N]
        -> $WORK_DATA/x17_facility_search/sel_l19/L19_gam_8Be_dome300_asb_sel.npz

Counters (cnt_*, gcnt_n by volume) are summed, rows concatenated (lnl_geant._combine), so the table is the same as one
lnl_merge_rot.py over every part, without the singles.  L19t2 (the test cluster, same seeds scheme, other seeds) can be
added with --run L19 L19t2.  (lnl_x17, 2026-11-25)
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path

import numpy as np

W = Path(os.environ.get('WORK_DATA', '/media/ucla/work')) / 'x17_facility_search'


def combine(zs):
    keys = set(zs[0]).intersection(*map(set, zs[1:])) if len(zs) > 1 else set(zs[0])
    vols = sorted({str(v) for z in zs for v in z.get('gcnt_vol', [])})
    out = {}
    for k in keys:
        if k in ('gcnt_vol', 'gcnt_n'):
            continue
        if k == 'cnt_lines':
            out[k] = zs[0][k]
        elif k.startswith('cnt_'):
            out[k] = sum(np.asarray(z[k]) for z in zs)
        else:
            out[k] = np.concatenate([z[k] for z in zs])
    if vols:
        n = dict.fromkeys(vols, 0)
        for z in zs:
            for v, c in zip(z['gcnt_vol'], z['gcnt_n']):
                n[str(v)] += int(c)
        out['gcnt_vol'] = np.array(vols, dtype='U24')
        out['gcnt_n'] = np.array([n[v] for v in vols], np.int64)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', nargs='+', default=['L19'])
    ap.add_argument('--cfg', default='dome300')
    ap.add_argument('--min-jobs', type=int, default=1)
    a = ap.parse_args()
    fl = []
    for r in a.run:
        fl += sorted((W / 'sel_l19_jobs' / r).glob('*_sel.npz'))
    if len(fl) < a.min_jobs:
        raise SystemExit(f'{len(fl)} job tables, fewer than {a.min_jobs}')
    zs = [dict(np.load(f)) for f in fl]
    z = combine(zs)
    dst = W / 'sel_l19'
    dst.mkdir(parents=True, exist_ok=True)
    out = dst / f'L19_gam_8Be_{a.cfg}_asb_sel.npz'
    np.savez_compressed(out, **z)
    print(f'{len(fl)} job tables, {int(z["cnt_n_generated"]):,} γ generated, {len(z["reco_c"]):,} rows -> {out}')


if __name__ == '__main__':
    main()
