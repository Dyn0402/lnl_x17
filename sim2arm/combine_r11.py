#!/usr/bin/env python3
"""
combine_r11.py -- the R11 chunk tables (lxplus merge_loop_r11.sh) -> one merged table per beam sample, as shapes_nd reads
them; the cosmic chunks stay chunks (two_arm_nd.load_cos reads them by glob with TA_LAYOUT=lsf16).

    rsync -a lxplus:/eos/experiment/ntof/data/x17/lnl/target/sel_r11/ $WORK_DATA/x17_facility_search/sel_r11_chunks/
    python sim2arm/combine_r11.py   ->  $WORK_DATA/x17_facility_search/sel_r11/R11_<sample>_dome300_asb_sel.npz
                                        + R11_cosmicdisk_dome300_lsf16_c*_sel.npz (copied)

R11 = the built Cu hemisphere (dome300) with the liquid cell right behind the SiPM wall (--ls-front 1.6), leg = SiPM AND
(plastic OR liquid >= 1.7 MeV).  The beam tables are named like the L18 ones (dome300_asb) so that shapes_nd.files()
finds them through RUNS['dome300'] = ['R11'].  (lnl_x17, 2026-11-20)
"""
from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

import numpy as np

W = Path(os.environ.get('WORK_DATA', '/media/ucla/work')) / 'x17_facility_search'
SRC, DST = W / 'sel_r11_chunks', W / 'sel_r11'
FS = Path(os.environ.get('X17FS', Path.home() / 'PycharmProjects' / 'x17_facility_search'))
sys.path.insert(0, str(FS / 'lnl' / 'sim'))
import lnl_geant as G         # noqa: E402

#: chunks per sample (njobs / chunk size of merge_loop_r11.sh)
NCH = {'M1_18.15': 4, 'E1_18.15': 4, 'M1_15.1': 2, 'E1_15.1': 2, 'gam_8Be': 4, 'X17_m16.8': 1}
NCOS = 8
#: R11b (21 Nov): x3-4 more beam MC of the same layout (merge_loop_r11b.sh, prefix R11b_), added to the R11 tables.
#: R11B=0 builds the R11-only tables (the 21 Nov result).
NCH_B = {'M1_18.15': 8, 'E1_18.15': 8, 'M1_15.1': 6, 'E1_15.1': 6, 'gam_8Be': 8}
USE_B = os.environ.get('R11B', '1') != '0'


def main():
    DST.mkdir(parents=True, exist_ok=True)
    for s, n in NCH.items():
        fl = sorted(SRC.glob(f'R11_{s}_dome300_lsf16_c*_sel.npz'))
        out = DST / f'R11_{s}_dome300_asb_sel.npz'
        if len(fl) < n:
            print(f'{s}: {len(fl)} of {n} chunks, waiting')
            continue
        if USE_B and s in NCH_B:
            fb = sorted(SRC.glob(f'R11b_{s}_dome300_lsf16_c*_sel.npz'))
            if len(fb) < NCH_B[s]:
                print(f'{s}: R11b {len(fb)} of {NCH_B[s]} chunks, waiting')
                continue
            fl += fb
        z = G._combine([dict(np.load(f, allow_pickle=True)) for f in fl])
        np.savez_compressed(out, **z)
        print(f'{s}: {len(fl)} chunks, {int(z["cnt_n_generated"]):,} generated, {len(z["reco_c"]):,} rows -> {out}')
    cos = sorted(SRC.glob('R11_cosmicdisk_dome300_lsf16_c*_sel.npz'))
    for f in cos:
        shutil.copy2(f, DST / f.name)
    print(f'cosmics: {len(cos)} of {NCOS} chunks copied')


if __name__ == '__main__':
    main()
