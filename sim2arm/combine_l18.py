#!/usr/bin/env python3
"""
combine_l18.py -- the L18 chunk tables (lxplus merge_loop_l18.sh) -> one merged table per sample, as shapes_nd reads them.

    rsync -a lxplus:/eos/experiment/ntof/data/x17/lnl/target/sel_l18/ $WORK_DATA/x17_facility_search/sel_l18_chunks/
    python sim2arm/combine_l18.py      ->  $WORK_DATA/x17_facility_search/sel_l18/L18_<sample>_dome300_asb_sel.npz

Chunks are concatenated with lnl_geant._combine (counters summed, rows concatenated), so a merged table is the same as
one lnl_merge.py over every part.  A sample is written only when all its chunks are there.  (lnl_x17, 2026-11-20)
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np

W = Path(os.environ.get('WORK_DATA', '/media/ucla/work')) / 'x17_facility_search'
SRC, DST = W / 'sel_l18_chunks', W / 'sel_l18'
FS = Path(os.environ.get('X17FS', Path.home() / 'PycharmProjects' / 'x17_facility_search'))
sys.path.insert(0, str(FS / 'lnl' / 'sim'))
import lnl_geant as G         # noqa: E402

#: chunks per sample (njobs / chunk size of merge_loop_l18.sh)
NCH = {'M1_18.15': 5, 'E1_18.15': 5, 'M1_15.1': 5, 'E1_15.1': 5, 'gam_8Be': 3, 'X17_m16.8': 1}


def main():
    DST.mkdir(parents=True, exist_ok=True)
    for s, n in NCH.items():
        fl = sorted(SRC.glob(f'L18_{s}_dome300_asb_c*_sel.npz'))
        out = DST / f'L18_{s}_dome300_asb_sel.npz'
        if len(fl) < n:
            print(f'{s}: {len(fl)} of {n} chunks, waiting')
            continue
        z = G._combine([dict(np.load(f, allow_pickle=True)) for f in fl])
        np.savez_compressed(out, **z)
        print(f'{s}: {len(fl)} chunks, {int(z["cnt_n_generated"]):,} generated, {len(z["reco_c"]):,} rows -> {out}')


if __name__ == '__main__':
    main()
