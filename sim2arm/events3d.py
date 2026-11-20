#!/usr/bin/env python3
"""
events3d.py -- real Geant4 events for the 3D view of the page's Predictions tab (lnl_x17, 2026-11-20).

Run L17 (sim2arm/lxplus/submit_traj.sh, MX17_Full_Geant lnl_twoarm 10229eb, --trajdump): the slot-1 two-arm
geometry (Cu hemisphere, 20 µm Li, as built, arms 0+1 = horizontal or 2+3 = vertical), every step of every e±, γ and
μ written for each event; traj_pick.py kept the events worth drawing (both arms with a leg + MM track for pairs, a
leg for γ singles, legs in both arms for cosmics).  This script picks a few typical events per kind, thins the tracks
and writes out/events3d.json (geometry extents read from the same step points, so the drawing is the simulation's).

    python sim2arm/events3d.py            # reads $WORK_DATA/lnl_x17/L17/<sample>_a01|a23/
"""
from __future__ import annotations

import glob
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
L17 = Path(os.environ.get('WORK_DATA', '/media/ucla/work')) / 'lnl_x17' / 'L17'
OUT = HERE / 'out' / 'events3d.json'
R_MAX = 700.0             # mm: clip tracks leaving the set-up
SIG_T = 0.60

KINDS = [  # key, sample dir, label, how many, selector
    ('ipc441', 'M1_17.64_a01', '441 keV: M1 internal pair (17.64 MeV)', 2, 'pair'),
    ('ipc1100', 'E1_18.15_a01', '1.10 MeV: E1 internal pair (18.15 MeV)', 3, 'pair'),
    ('x17', 'X17_m16.8_a01', 'X17 (16.8 MeV) → e⁺e⁻, if ATOMKI is right', 2, 'x17'),
    ('gam_trk', 'gam_8Be_a01', '18.15/17.64 MeV γ: converts before the chamber (single with a track)', 2, 'gam_trk'),
    ('gam_notrk', 'gam_8Be_a01', '18.15/17.64 MeV γ: converts in the scintillators (single, no track)', 2, 'gam_notrk'),
    ('mu_h', 'cosmicdisk_a01', 'cosmic muon through both side arms (beam geometry)', 2, 'mu'),
    ('mu_v', 'cosmicdisk_a23', 'cosmic muon, arms vertical (cosmic nights)', 2, 'mu'),
]


def rdp(P, eps):
    """Ramer-Douglas-Peucker on an (n,3) polyline."""
    if len(P) < 3:
        return P
    a, b = P[0], P[-1]
    ab = b - a
    L = np.linalg.norm(ab)
    if L == 0:
        d = np.linalg.norm(P - a, axis=1)
    else:
        d = np.linalg.norm(np.cross(P - a, ab), axis=1) / L
    i = int(np.argmax(d))
    if d[i] > eps:
        return np.vstack([rdp(P[:i + 1], eps)[:-1], rdp(P[i:], eps)])
    return np.vstack([a, b])


def load(sample):
    d = L17 / sample
    evs, trs = [], []
    for f in sorted(glob.glob(str(d / '*_evt.npz'))):
        job = Path(f).name.split('_')[1]
        z = np.load(f)
        if len(z['eventID']) == 0:
            continue
        evs.append((job, {k: z[k] for k in z.files}))
        t = pd.read_csv(f.replace('_evt.npz', '_traj.csv.gz'))
        t['job'] = job
        trs.append(t)
    return evs, (pd.concat(trs) if trs else pd.DataFrame())


def arm_summary(z, i):
    E = (z['E_sipm'][i] + z['E_plast'][i] + z['E_ls'][i]).astype(float)
    c = z['seg_c_all'][i].astype(float)
    dd = z['seg_d_dom'][i].astype(float)
    cd = z['seg_c_dom'][i].astype(float)
    return dict(E=E, leg=z['leg'][i], mm=z['mm'][i], c=c, c_dom=cd, d_dom=dd, t=z['t_sipm'][i].astype(float))


def angle(c1, c2):
    return float(np.degrees(np.arccos(np.clip(c1 @ c2 / (np.linalg.norm(c1) * np.linalg.norm(c2)), -1, 1))))


def tracks(t):
    out = []
    for (tid, pid, part), g in t.groupby(['trackID', 'parentID', 'particle']):
        g = g.sort_values('istep')
        P = np.vstack([g[['pre_x', 'pre_y', 'pre_z']].values[:1], g[['post_x', 'post_y', 'post_z']].values])
        r = np.linalg.norm(P, axis=1)
        if (r > R_MAX).any():                     # keep the stretch inside R_MAX, ends pulled onto the sphere
            ins = np.nonzero(r <= R_MAX)[0]
            if len(ins) == 0:
                continue
            i0, i1 = max(ins[0] - 1, 0), min(ins[-1] + 1, len(P) - 1)
            P = P[i0:i1 + 1].copy()
            for k, kin in ((0, 1), (-1, -2)):    # move the outside end along its segment onto the sphere
                if len(P) > 1 and np.linalg.norm(P[k]) > R_MAX:
                    a, b = P[kin], P[k]
                    d = b - a
                    qa, qb, qc = d @ d, 2 * a @ d, a @ a - R_MAX ** 2
                    t = (-qb + np.sqrt(max(qb * qb - 4 * qa * qc, 0))) / (2 * qa)
                    P[k] = a + min(max(t, 0), 1) * d
        ke0 = float(g.ke_pre_MeV.iloc[0])
        length = float(np.linalg.norm(np.diff(P, axis=0), axis=1).sum())
        edep = float(g.edep_MeV.sum())
        keep = pid == 0 or (part in ('e-', 'e+') and (ke0 > 0.1 or length > 8)) or (part == 'gamma' and ke0 > 0.2) \
            or part.startswith('mu')
        if not keep or len(P) < 2:
            continue
        P = rdp(P, 0.6 if part != 'gamma' else 0.1)
        out.append(dict(id=int(tid), parent=int(pid), p=part, ke=round(ke0, 3), edep=round(edep, 3),
                        v0=str(g.volume.iloc[0]), proc=str(g.process.iloc[-1]),
                        pts=np.round(P, 1).tolist()))
    return out


def pick(kind, sel, evs, t, n, arms):
    rows = []
    for job, z in evs:
        for i, eid in enumerate(z['eventID']):
            a0, a1 = arms
            A = arm_summary(z, i)
            tt = t[(t.job == job) & (t.eventID == eid)]
            if tt.empty:
                continue
            th = angle(A['c'][a0], A['c'][a1]) if A['mm'][a0] and A['mm'][a1] else None
            Es = A['E'][a0] + A['E'][a1]
            score = None
            if sel in ('pair', 'x17'):
                if th is None:
                    continue
                tt = float(z['theta'][i])          # true opening angle: prefer pairs that did not migrate much
                score = -abs(th - 140) - 0.5 * abs(th - tt) - (0 if 12 < Es < 20 else 30)
            elif sel == 'gam_trk':
                one = [a for a in arms if A['leg'][a]]
                if len(one) != 1 or not A['mm'][one[0]]:
                    continue
                score = A['E'][one[0]]
            elif sel == 'gam_notrk':
                one = [a for a in arms if A['leg'][a]]
                if len(one) != 1 or A['mm'][one[0]]:
                    continue
                score = A['E'][one[0]]
            elif sel == 'mu':
                if not (A['leg'][a0] and A['leg'][a1] and A['mm'][a0] and A['mm'][a1]):
                    continue
                score = -abs((th or 0) - 140) if th else -99
            rows.append((score, job, int(eid), i, z, th, Es))
    rows.sort(key=lambda r: -r[0])
    picked = []
    for score, job, eid, i, z, th, Es in rows[:n]:
        A = arm_summary(z, i)
        tt = t[(t.job == job) & (t.eventID == eid)]
        arm_info = []
        for a in arms:
            seg = None
            if A['mm'][a] and np.isfinite(A['c_dom'][a]).all():
                seg = dict(c=np.round(A['c_dom'][a], 1).tolist(), d=np.round(A['d_dom'][a], 4).tolist())
            arm_info.append(dict(arm=int(a), leg=bool(A['leg'][a]), mm=bool(A['mm'][a]),
                                 E_sipm=round(float(z['E_sipm'][i][a]), 2), E_plast=round(float(z['E_plast'][i][a]), 2),
                                 E_ls=round(float(z['E_ls'][i][a]), 2), E=round(float(A['E'][a]), 2),
                                 t=None if not np.isfinite(A['t'][a]) else round(float(A['t'][a]), 3), seg=seg))
        V = z['V'][i].astype(float)
        picked.append(dict(kind=kind, job=job, eventID=eid, theta_reco=None if th is None else round(th, 1),
                           Esum=round(float(Es), 2), vertex=np.round(V, 1).tolist(),
                           truth=dict(type=int(z['event_type'][i]), E=round(float(z['inv_mass'][i]), 3),
                                      theta=round(float(z['theta'][i]), 1), em_ke=round(float(z['em_ke'][i]), 2),
                                      ep_ke=round(float(z['ep_ke'][i]), 2)),
                           arms=arm_info, tracks=tracks(tt)))
    return picked


def geometry():
    """Extents of the arm layers (arm 0, +x, G4 frame: beam +y, up +z), read from L17 step points; the
    other arms are the same stack rotated, with their pinwheel shifts (lnl_merge.SHIFT)."""
    return dict(
        frame='Geant4: beam +y, up +z, mm',
        arm_shift=[15.5, -15.75, -16.35, 17.3],
        layers=[  # name, inner, outer distance from the beam axis, transverse size, along-beam size
            dict(k='mylar', r0=204.0, r1=204.1, u=420, v=400),
            dict(k='drift', r0=209.1, r1=239.1, u=399.4, v=394),
            dict(k='active', r0=209.1, r1=239.1, u=399.4, v=360),
            dict(k='pcb', r0=239.1, r1=245.8, u=440, v=432),
            dict(k='support', r0=245.8, r1=253.8, u=440, v=466),
            dict(k='sipm', r0=330.0, r1=333.0, u=400, v=470, bars=16),
            dict(k='plastic', r0=414.2, r1=434.2, u=197, v=300, n=2, gap=3),
            dict(k='ls', r0=460.6, r1=502.8, u=451, v=451),
        ],
        # Cu hemisphere ("ogive") wall profile, r(y) in mm, y from the base flange to the tip (L17 dome points)
        dome=[[-63.0, 25.0], [-60.0, 24.1], [-55.0, 21.9], [-50.0, 21.1], [-35.0, 15.2], [-25.0, 10.7],
              [-20.0, 10.0], [-15.0, 8.6], [-10.0, 6.5], [-5.0, 4.3], [-2.0, 2.6], [0.0, 0.0]],
        beamline=[dict(r0=19.05, r1=30.0, y0=-68, y1=-63, m='Al'), dict(r0=17.4, r1=19.05, y0=-620, y1=-68, m='SS'),
                  dict(r0=31.0, r1=57.0, y0=-620, y1=-585, m='SS')])


def gam_origin(evs, t):
    """Where the primary γ of a single-arm beam leg first interacted, split by 'MM track or not'."""
    import collections
    cnt = {'track': collections.Counter(), 'no_track': collections.Counter()}
    for job, z in evs:
        for i, e in enumerate(z['eventID']):
            arms = [a for a in (0, 1) if z['leg'][i][a]]
            if len(arms) != 1:
                continue
            g = t[(t.job == job) & (t.eventID == e) & (t.parentID == 0) & (t.particle == 'gamma')].sort_values('istep')
            g = g[~g.process.isin(['Transportation', 'CoupledTransportation'])]
            v = g.volume.iloc[0] if len(g) else 'none'
            grp = ('Cu hemisphere' if v.startswith('LiTarget') else 'chamber window/cathode/gas' if v in (
                'GasWindow_Mylar', 'GasWindow_Al', 'DriftCathode_Kapton', 'DriftCathode_Cu', 'DriftGas', 'WindowGapGas')
                else 'chamber readout PCB/support' if v.startswith(('PCB', 'Micromesh', 'Resist', 'Support', 'GasFrame', 'AmpGas'))
                else 'SiPM wall' if v == 'PlasticScint' else 'plastics/liquid' if v.startswith(('BackScint', 'Liq', 'LS'))
                else 'air' if v == 'World' else v)
            cnt['track' if z['mm'][i][arms[0]] else 'no_track'][grp] += 1
    return {k: dict(c.most_common()) for k, c in cnt.items()}


def main():
    res = dict(made='2026-11-20', run='L17', g4='MX17_Full_Geant lnl_twoarm 10229eb, Cu hemisphere, as built',
               geometry=geometry(), kinds={k: lab for k, _, lab, _, _ in KINDS}, events=[])
    cache = {}
    for key, sample, label, n, sel in KINDS:
        if sample not in cache:
            cache[sample] = load(sample) if (L17 / sample).is_dir() else ([], pd.DataFrame())
        evs, t = cache[sample]
        arms = (2, 3) if sample.endswith('a23') else (0, 1)
        if not evs:
            print('no events yet for', sample)
            continue
        p = pick(key, sel, evs, t, n, arms)
        print(f'{key}: {len(p)} picked of', sum(len(z["eventID"]) for _, z in evs),
              [(e['theta_reco'], e['Esum'], len(e['tracks'])) for e in p])
        res['events'] += p
        if key == 'gam_trk':
            res['gam_origin'] = gam_origin(evs, t)
            print('γ singles, first interaction:', res['gam_origin'])
    OUT.write_text(json.dumps(res, separators=(',', ':')), encoding='utf-8')
    print('wrote', OUT, f'{OUT.stat().st_size / 1e6:.2f} MB')


if __name__ == '__main__':
    main()
