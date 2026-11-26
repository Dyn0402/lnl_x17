#!/usr/bin/env python3
"""Geometric pair acceptance of the two-arm LNL set-up against the opening angle (2026-11-26, proposal Fig. 2).

    python3 proposal/figsrc/acceptance.py      -> sim2arm/out/acceptance_geom.csv, acceptance_ipc441.csv

GEOMETRY ONLY, straight leptons from the target point: a lepton is "seen" by an arm if its line crosses the active
volume of that arm's TPC, i.e. both the entry plane (209.1 mm) and the exit plane (239.1 mm) of the drift gap fall inside
the active area (399.4 mm across the beam x 360 mm along it), with the arm shifts of the as-built Geant4 model
(sim2arm/out/events3d.json "geometry", MX17_Full_Geant lnl_twoarm). No multiple scattering in the Cu holder, no
energy threshold beyond KE > 1 MeV, no trigger: those are in the full Geant4 predictions (Fig. 3).

(a) pairs flat in opening angle: first lepton isotropic, second at angle theta with a uniform azimuth around the first.
    acceptance(theta) = P(one lepton in each arm) and P(both leptons in the same arm, either arm).
(b) M1 internal pairs of the 17.64 MeV transition (441 keV resonance), Born multipole generator of nTof_x17 through
    x17_facility_search/lnl/lnl_rates.py, normalised to 5.4e4 gamma0/s at 1 uA (proposal Table I, PREDICTIONS.md) and
    to the M1 pair coefficient alpha(17.64); pairs reaching the TPCs per 8 hours of beam.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "sim2arm" / "out"
sys.path.insert(0, str(Path.home() / "PycharmProjects" / "x17_facility_search" / "lnl"))
import lnl_rates as LR  # noqa: E402

G = json.load(open(OUT / "events3d.json"))["geometry"]
ACT = next(L for L in G["layers"] if L["k"] == "active")
R0, R1, HU, HV = ACT["r0"], ACT["r1"], ACT["u"] / 2, ACT["v"] / 2    # mm; u across the beam (z), v along the beam (y)
SHIFT = G["arm_shift"][:2]                                            # arm 0 at +x, arm 1 at -x (z offsets, mm)
GAMMA0_441 = 5.4e4          # ground-state gamma per second at 441 keV, 1 uA, 11 um film (proposal Table I text)
HOURS = 8.0


def arm_of(d):
    """d: unit directions (n,3) in the Geant4 frame (beam +y, up +z). Returns 0, 1 or -1."""
    out = np.full(len(d), -1)
    for arm, sgn in ((0, 1.0), (1, -1.0)):
        dx = d[:, 0] * sgn
        ok = dx > 0
        for r in (R0, R1):
            t = np.where(ok, r / np.where(ok, dx, 1.0), 0.0)
            ok &= (np.abs(d[:, 2] * t - SHIFT[arm]) < HU) & (np.abs(d[:, 1] * t) < HV)
        out[ok] = arm
    return out


def iso(n, rng):
    c = rng.uniform(-1, 1, n)
    p = rng.uniform(0, 2 * np.pi, n)
    s = np.sqrt(1 - c ** 2)
    return np.c_[s * np.cos(p), s * np.sin(p), c]


def at_angle(d1, th, rng):
    a = np.where(np.abs(d1[:, :1]) < 0.9, [[1.0, 0, 0]], [[0, 1.0, 0]])
    u = np.cross(d1, a)
    u /= np.linalg.norm(u, axis=1, keepdims=True)
    v = np.cross(d1, u)
    ph = rng.uniform(0, 2 * np.pi, len(d1))
    return np.cos(th)[:, None] * d1 + np.sin(th)[:, None] * (np.cos(ph)[:, None] * u + np.sin(ph)[:, None] * v)


def main(n=4_000_000):
    rng = np.random.default_rng(17)
    edges = np.arange(0, 181, 2.5)
    th = rng.uniform(0, np.pi, n)
    d1 = iso(n, rng)
    d2 = at_angle(d1, th, rng)
    a1, a2 = arm_of(d1), arm_of(d2)
    opp = (a1 >= 0) & (a2 >= 0) & (a1 != a2)
    same = (a1 >= 0) & (a1 == a2)
    deg = np.degrees(th)
    gen, _ = np.histogram(deg, edges)
    ho, _ = np.histogram(deg[opp], edges)
    hs, _ = np.histogram(deg[same], edges)
    with open(OUT / "acceptance_geom.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["th_lo", "th_hi", "n_gen", "acc_opposite", "acc_same", "err_opposite", "err_same"])
        for i in range(len(gen)):
            w.writerow([edges[i], edges[i + 1], gen[i], ho[i] / gen[i], hs[i] / gen[i],
                        np.sqrt(ho[i]) / gen[i], np.sqrt(hs[i]) / gen[i]])
    print(f"single-lepton solid angle per arm: {np.mean(arm_of(iso(n, rng)) == 0):.4f} of 4pi")
    for lo, hi in ((125, 160), (130, 150), (160, 180)):
        m = (deg >= lo) & (deg < hi)
        print(f"flat pairs {lo}-{hi}: opposite {opp[m].mean():.4f}, same {same[m].mean():.4f}")

    # (b) M1 internal pairs at 17.64 MeV
    ev = LR.ipc_vectors("M1", 8_000_000, 17.64, seed=3)
    alpha = LR._ipc_born().alpha_pair("M1", 17.64)
    wt = ev["w"] / ev["w"].sum() * alpha * GAMMA0_441 * HOURS * 3600
    b1 = arm_of(ev["p1"] / np.linalg.norm(ev["p1"], axis=1, keepdims=True))
    b2 = arm_of(ev["p2"] / np.linalg.norm(ev["p2"], axis=1, keepdims=True))
    ke = (ev["ke1"] > LR.KE_MIN) & (ev["ke2"] > LR.KE_MIN)
    o2 = ke & (b1 >= 0) & (b2 >= 0) & (b1 != b2)
    s2 = ke & (b1 >= 0) & (b1 == b2)
    e5 = np.arange(0, 181, 5.0)
    gi, _ = np.histogram(ev["theta"], e5, weights=wt)
    oi, _ = np.histogram(ev["theta"][o2], e5, weights=wt[o2])
    si, _ = np.histogram(ev["theta"][s2], e5, weights=wt[s2])
    with open(OUT / "acceptance_ipc441.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["th_lo", "th_hi", "emitted_per_8h", "opposite_per_8h", "same_per_8h"])
        for i in range(len(gi)):
            w.writerow([e5[i], e5[i + 1], gi[i], oi[i], si[i]])
    print(f"alpha(M1,17.64) = {alpha:.3e}; emitted IPC per 8 h {gi.sum():.3g}; reaching the TPCs: opposite {oi.sum():.0f}, "
          f"same arm {si.sum():.0f} (of which theta<40: {si[:8].sum():.0f}); opposite with theta>90: {oi[18:].sum():.0f}")


if __name__ == "__main__":
    main()
