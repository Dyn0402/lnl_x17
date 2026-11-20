#!/usr/bin/env python3
"""leg_layout.py -- which scintillator layout behind the SiPM wall gives the most pairs (2026-11-20).

    ~/PycharmProjects/nTof_x17/.venv/bin/python sim2arm/leg_layout.py   # -> sim2arm/out/leg_layout.csv (~1 min)

A SCALING ESTIMATE, not Geant4. It reuses the geometric leg toy of x17_facility_search lnl/plastic_size.py
(FEASIBILITY_SIM.md §9: straight leptons from the spot, Highland kicks, a kinetic-energy threshold; both free numbers
fitted to the Geant4 X17 pair-tags as built and with big plastics: T_MM = 0.03 X0, E_TH = 5.25 MeV, calib.csv).

A leg = a lepton through the MM active area AND a read-out SiPM bar AND one of the leg detectors of the layout.
Only the horizontal pair (arms 0 + 1) is counted. Days to 3 sigma scale as B/S^2 with S = X17 and B = M1/E1 IPC
in 125-155 deg (counting); the reach at fixed time as sqrt(days). Cosmics, the E_sum window, the energy response
and the plastics' position behind 2 cm of liquid are NOT in the toy: they are what the Geant4 run must add.

Layouts (depths behind the MM window face, from SimConfig.hh / plastic_size.py):
  * SiPM wall back at 145 mm; plastics now at ~206 mm; liquid cell now ~270 mm (12.3-12.7 cm behind the SiPM back).
  * Swapped: liquid cell front 5 mm behind the SiPM wall, its mid-plane at ~165 mm; the plastics stay at ~206 mm
    (the 2.1 cm cell, bulged ~1.3 cm per face, fits the 6.1-6.5 cm gap).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path.home() / 'PycharmProjects/x17_facility_search/lnl'))
import plastic_size as ps  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / 'out'
T_MM, E_TH = 0.03, 5.25          # ps calib.csv (fit)

D_PL = ps.PLASTIC_DW_ASBUILT      # plastics (per arm)
D_LS_NOW = ps.SIPM_BACK_DW + 125.0 + 10.0
D_LS_SWAP = ps.SIPM_BACK_DW + 5.0 + 15.0
LS = (225.0, 225.0)               # liquid cell half-sizes u, v (45 x 45 cm)


def inside(L, depth, hu, hv, gap=0.0):
    u, v = L.at_plastic(depth)
    au = np.abs(u)
    return (au >= gap) & (au < hu) & (np.abs(v) < hv)


DET = {
    'plastics 2 x 20x30 (as now)': lambda L: inside(L, D_PL, 200.6, 150.2, 1.5),
    'plastics 3 x 20x30 = 60(u) x 30(v)': lambda L: inside(L, D_PL, 300.0, 150.0),
    'plastics 3 x 30x20 = 30(u) x 60(v)': lambda L: inside(L, D_PL, 150.0, 300.0),
    'liquid 45x45, where it is now (~47 cm)': lambda L: inside(L, D_LS_NOW, *LS),
    'liquid 45x45, right behind the SiPM wall (~37 cm)': lambda L: inside(L, D_LS_SWAP, *LS),
    'liquid 60x60, right behind the SiPM wall': lambda L: inside(L, D_LS_SWAP, 300.0, 300.0),
}

LAYOUTS = [
    ('A', 'as now: leg = SiPM x plastics (2 x 20x30); liquid behind, energy only', ['plastics 2 x 20x30 (as now)']),
    ('B', 'as now, but the liquid also forms a leg (SiPM x (plastic OR liquid))',
     ['plastics 2 x 20x30 (as now)', 'liquid 45x45, where it is now (~47 cm)']),
    ('C', 'swapped: liquid right behind the SiPM wall, 2 plastics behind; leg = SiPM x (liquid OR plastic)',
     ['liquid 45x45, right behind the SiPM wall (~37 cm)', 'plastics 2 x 20x30 (as now)']),
    ('C1', 'swapped, leg = SiPM x liquid only', ['liquid 45x45, right behind the SiPM wall (~37 cm)']),
    ('D', 'swapped + 3 plastics 60(u) x 30(v) behind; leg = SiPM x (liquid OR plastic)',
     ['liquid 45x45, right behind the SiPM wall (~37 cm)', 'plastics 3 x 20x30 = 60(u) x 30(v)']),
    ('D2', 'swapped + 3 plastics 30(u) x 60(v) behind; leg = SiPM x (liquid OR plastic)',
     ['liquid 45x45, right behind the SiPM wall (~37 cm)', 'plastics 3 x 30x20 = 30(u) x 60(v)']),
    ('E', 'plastics only, 3 x 20x30 = 60 x 30, no liquid in the leg', ['plastics 3 x 20x30 = 60(u) x 30(v)']),
    ('F', 'wider liquid 60x60 right behind the SiPM wall (LIQUID_CELLS.md §3)', ['liquid 60x60, right behind the SiPM wall']),
]


def leg(L, dets):
    ok = L.mm & (L.ke > E_TH) & ps.sipm_ok(L, 20)
    any_det = np.zeros(len(ok), bool)
    for d in dets:
        any_det |= DET[d](L)
    return ok & any_det


def main():
    OUT.mkdir(exist_ok=True)
    N = 2_000_000
    S = {k: ps.Sample(k, N, 10 + i, T_MM) for i, k in enumerate(('X17', 'M1', 'E1'))}
    yields = pd.read_csv(ps.HERE / 'out' / 'yields.csv').set_index('scenario').loc['ATOMKI 2016 anomaly']
    alpha = pd.read_csv(ps.HERE / 'out' / 'ipc_alpha.csv').set_index(['W_MeV', 'multipole']).alpha_pair
    w = {'M1': (yields.frac_18_15_res + yields.frac_17_64) * alpha[(18.15, 'M1')],
         'E1': yields.frac_direct * alpha[(18.15, 'E1')]}

    def counts(dets):
        r = np.random.default_rng(77)
        out = {}
        for k, s in S.items():
            horiz = ((s.L[0].arm == 0) & (s.L[1].arm == 1)) | ((s.L[0].arm == 1) & (s.L[1].arm == 0))
            m = s.mm2 & horiz & leg(s.L[0], dets) & leg(s.L[1], dets)
            out[k] = (m.mean(), ps.window_counts(s, m, r))
        return out

    rows = []
    for key, name, dets in LAYOUTS:
        c = counts(dets)
        rows.append(dict(layout=key, what=name, pair_tag_x17=c['X17'][0], s_win=c['X17'][1],
                         b_win=w['M1'] * c['M1'][1] + w['E1'] * c['E1'][1]))
    df = pd.DataFrame(rows)
    ref = df.iloc[0]
    df['x17_rel'] = df.s_win / ref.s_win
    df['ipc_rel'] = df.b_win / ref.b_win
    df['days_rel'] = df.ipc_rel / df.x17_rel ** 2
    df['r90_rel'] = np.sqrt(df.days_rel)
    # applied to the Geant4 hemisphere reach (TWO_ARM_STUDY §0: 151 d to 3 sigma, 2.35 x R(ATOMKI) in 5 d, liquid working)
    df['days_3sigma_est'] = 151 * df.days_rel
    df['r90_5d_est'] = 2.35 * df.r90_rel
    df.to_csv(OUT / 'leg_layout.csv', index=False)
    pd.set_option('display.width', 220)
    print(df[['layout', 'what', 'pair_tag_x17', 'x17_rel', 'ipc_rel', 'days_rel', 'days_3sigma_est', 'r90_5d_est']]
          .to_string(index=False, float_format=lambda v: f'{v:.3g}'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
