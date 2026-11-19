#!/usr/bin/env python3
"""tof_scan.py -- two-arm reach and cosmics against the per-arm TOF resolution sigma_t (pointing 15° for electrons,
3° for muons, + TOF cut at 2 sqrt(2) sigma_t), 1.10 MeV, LNL calibrated, Cu hemisphere, 20 µm, direct MC.
sigma_t measured on n_TOF beam-off cosmics (nTof_x17 ntof_cosmics/ac_tof_beamoff.py): 0.52-0.64 ns per arm.

    WORK_DATA=/media/ucla/work ~/PycharmProjects/nTof_x17/.venv/bin/python sim2arm/tof_scan.py horiz vert
        -> out/tof_scan_two_arm.csv"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pandas as pd            # noqa: E402

import two_arm_nd as TA        # noqa: E402

SN = TA.SN
SIGMAS = (0.3, 0.5, 0.6, 0.7, 1.0)
for s in SIGMAS:
    SN.EXTRA_LEVELS[f'MM 15° point, μ 3° + TOF {s:g} ns'] = dict(seg=15.0, tof=s, mu_seg=3.0)
LEVELS = ['MM 15° point, μ 3°'] + [f'MM 15° point, μ 3° + TOF {s:g} ns' for s in SIGMAS]
rows = []
for pair in sys.argv[1:] or ['horiz', 'vert']:
    for lv in LEVELS:
        r = TA.task((pair, 'ogCu200', 'LNL calibrated', lv, 'direct'))
        rows.append({k: r.get(k) for k in ('pair', 'level', 'days_floor1', 'S_win', 'Bbeam_win', 'Bcos_win', 'n_mc_cos_win',
                                           'Bcos_fit', 'n_mc_cos_fit')})
pd.DataFrame(rows).to_csv(TA.OUT / 'tof_scan_two_arm.csv', index=False)
print(pd.DataFrame(rows).round(2).to_string(index=False))
