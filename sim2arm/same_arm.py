#!/usr/bin/env python3
"""
same_arm.py -- pairs with both leptons in one arm at 441 keV: selection, rates and background (run L20, 2026-11-27).

    python3 sim2arm/same_arm.py [--dir $WORK_DATA/lnl_x17/l20]   -> sim2arm/out/same_arm_l20.csv, _cutflow.csv, figures/same_arm_l20.png

Inputs: the merged L20 tables (lxplus/merge_l20.py) of
  M1_17.64  the M1 internal pairs (IPC) of the 17.64 MeV transition  -> the signal-like sample we want to measure;
  gam_441   the 441 keV γ rays, 17.64 : 14.6 MeV = 1 : 0.45            -> the background (external conversions etc.).
Geometry: the built Cu hemisphere (dome300), 4 arms as built; the beam days use the horizontal pair, arms 0 and 1.
Tracks are separated by Geant4 truth (twotrack_reduce.py): the selection assumes perfect pattern recognition, and the
two-track separation needed in a real TPC is shown as a cut on the centroid distance.

Selection of a same-arm pair in arm a (0 or 1), level by level:
  trig   a trigger leg in arm a (SiPM bar AND plastic >= 0.5 MIP)
  2trk   >= 2 tracks with >= 3 hits in arm a's drift gap (the two most energetic are used)
  point  both tracks point to the beam spot: DCA < 135 mm after a 15° smear of the direction (the opposite-arm
         reference, lnl_geant.seg_D(15)); variant 3°
  (E)    variant: arm calorimetry E_sipm + E_plast + E_ls > 5 MeV.  The opposite-arm 13-19 MeV window does not apply:
         one arm contains only 3-12 MeV of the pair's 16.6 MeV, and an external conversion of the same γ line has
         the same energy as an internal pair, so energy does not separate the two.
  sep    the two track centroids more than 1 cm apart (variants 0, 2 cm)
Opening angle = angle between the two centroids as seen from the beam spot (as reco_c for opposite arms).
Normalisation per beam day (18 h of beam, 1 µA, 11 µm film): 5.4e4 γ0/s (17.64 MeV) and 0.45 x that γ1 (14.6 MeV);
IPC = α(M1, 17.64) = 3.42e-3 per γ0 (x17_facility_search lnl_rates, Born).
"""
from __future__ import annotations

import argparse
import csv
import os
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "out"
BEAM_S = 18.0 * 3600     # one beam day: 18 h of CN beam (27 Nov)
G0 = 5.4e4
G1_OVER_G0 = 0.45
ALPHA_M1 = 3.4234e-3
N_IPC_DAY = ALPHA_M1 * G0 * BEAM_S
N_GAM_DAY = G0 * (1 + G1_OVER_G0) * BEAM_S
D_CUT = 135.0
E_MIN = 5.0     # MeV, raw arm deposit: one arm holds only 3-12 MeV of the 16.6 MeV pair (L20 test)
BINS = np.arange(0, 95, 5.0)


def smear_dir(d, deg, rng):
    d = d / np.linalg.norm(d, axis=-1, keepdims=True)
    a = np.where(np.abs(d[:, 0]) < 0.9, 1.0, 0.0)
    ref = np.stack([a, 1 - a, np.zeros_like(a)], 1)
    e1 = np.cross(d, ref)
    e1 /= np.linalg.norm(e1, axis=1, keepdims=True)
    e2 = np.cross(d, e1)
    th = np.radians(deg) * np.sqrt(-2 * np.log(rng.uniform(1e-12, 1, len(d))))   # Rayleigh in polar angle
    ph = rng.uniform(0, 2 * np.pi, len(d))
    s = d * np.cos(th)[:, None] + np.sin(th)[:, None] * (e1 * np.cos(ph)[:, None] + e2 * np.sin(ph)[:, None])
    return s


def dca0(c, d):
    return np.linalg.norm(np.cross(c, d), axis=-1) / np.linalg.norm(d, axis=-1)


def ang(a, b):
    c = (a * b).sum(-1) / (np.linalg.norm(a, axis=-1) * np.linalg.norm(b, axis=-1))
    return np.degrees(np.arccos(np.clip(c, -1, 1)))


def candidates(z, seed=11):
    """one row per (event, arm) with >= 2 tracks; every column the cuts need."""
    rows = []
    rng = np.random.default_rng(seed)
    for a in (0, 1):
        m = z["n_trk"][:, a] >= 2
        if not m.any():
            continue
        C1, C2 = z["trk_C"][m, a, 0].astype(float), z["trk_C"][m, a, 1].astype(float)
        D1, D2 = z["trk_D"][m, a, 0].astype(float), z["trk_D"][m, a, 1].astype(float)
        r = dict(idx=np.flatnonzero(m), arm=np.full(m.sum(), a),
                 leg=((z["legs"][m].astype(int) >> a) & 1).astype(bool),
                 Earm=(z["E_sipm"][m, a] + z["E_plast"][m, a] + np.nan_to_num(z["E_ls"][m, a])).astype(float),
                 theta=ang(C1, C2), sep=np.linalg.norm(C1 - C2, axis=1),
                 pid1=z["trk_pid"][m, a, 0], pid2=z["trk_pid"][m, a, 1],
                 q1=z["trk_q"][m, a, 0], q2=z["trk_q"][m, a, 1])
        for deg in (15.0, 3.0):
            s1, s2 = smear_dir(D1, deg, rng), smear_dir(D2, deg, rng)
            r[f"pt{deg:g}"] = (dca0(C1, s1) < D_CUT) & (dca0(C2, s2) < D_CUT)
        rows.append(r)
    return {k: np.concatenate([r[k] for r in rows]) for k in rows[0]} if rows else {}


def _e(c):
    return c["Earm"] > E_MIN


LEVELS = [("trig + 2 tracks", lambda c: c["leg"]),
          ("+ pointing 15°", lambda c: c["leg"] & c["pt15"]),
          ("+ separation > 1 cm", lambda c: c["leg"] & c["pt15"] & (c["sep"] > 10)),
          ("+ separation > 2 cm", lambda c: c["leg"] & c["pt15"] & (c["sep"] > 20)),
          ("ref + E_arm > 5 MeV", lambda c: c["leg"] & c["pt15"] & (c["sep"] > 10) & _e(c)),
          ("ref, pointing 3°", lambda c: c["leg"] & c["pt3"] & (c["sep"] > 10))]
REF = "+ separation > 1 cm"


def gam_class(z, c):
    """origin of a γ-sample candidate: the two tracks are the primary γ's conversion pair (by its first interaction
    volume), or anything else (Compton electrons, a conversion lepton + a delta ray, ...)."""
    i = c["idx"]
    pair = (c["pid1"] == 1) & (c["pid2"] == 1) & (c["q1"] * c["q2"] == -1)
    vol = z["g_fvol"][i]
    proc = z["g_fproc"][i]
    out = np.full(len(i), "other (Compton, δ rays)", dtype=object)
    conv = pair & (proc == "conv")
    groups = {"Cu hemisphere": ("LiTarget_",),
              "chamber wall + beam line": ("Chamber", "BeamLine", "Line"),
              "TPC (frame, window, cathode, gas, PCB)": ("Drift", "Window", "GasFrame", "GasWindow", "PCB", "Mesh",
                                                         "Cathode")}
    out[conv] = "conversion, elsewhere"
    for g, keys in groups.items():
        hit = conv & np.array([any(v.startswith(k) or k in v for k in keys) for v in vol])
        out[hit] = f"conversion in {g}"
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=os.path.join(os.environ.get("WORK_DATA", "/media/ucla/work"), "lnl_x17", "l20"))
    a = ap.parse_args()
    zi, zg = np.load(f"{a.dir}/M1_17.64.npz"), np.load(f"{a.dir}/gam_441.npz")
    wi, wg = N_IPC_DAY / zi["n_generated"][0], N_GAM_DAY / zg["n_generated"][0]
    ci, cg = candidates(zi), candidates(zg)
    # IPC candidates must be the true pair: both primaries (parentID 0) of opposite charge
    ci_true = (ci["pid1"] == 0) & (ci["pid2"] == 0) & (ci["q1"] * ci["q2"] == -1)
    cls = gam_class(zg, cg)
    print(f"IPC: {zi['n_generated'][0]:.3g} generated (weight {wi:.3g}/day); γ: {zg['n_generated'][0]:.3g} "
          f"(weight {wg:.3g}/day)")
    truth_same = (np.isin(zi["em_arm"], [0, 1]) & (zi["em_arm"] == zi["ep_arm"]))
    print(f"IPC with both leptons in arm 0 or 1 (truth, first drift-gap hit): {truth_same.sum() * wi:.3g} per day")
    flow = []
    for name, f in LEVELS:
        si, sg = f(ci), f(cg)
        row = dict(level=name, ipc_day=(si & ci_true).sum() * wi, ipc_other_day=(si & ~ci_true).sum() * wi,
                   ipc_mc=int((si & ci_true).sum()), gam_day=sg.sum() * wg, gam_mc=int(sg.sum()))
        for k in sorted(set(cls)):
            row[f"gam: {k}"] = (sg & (cls == k)).sum() * wg
        flow.append(row)
        print(f"  {name:22s} IPC {row['ipc_day']:9.4g}/day ({row['ipc_mc']} MC)   γ bkg {row['gam_day']:9.4g}/day "
              f"({row['gam_mc']} MC)")
    keys = sorted({k for r in flow for k in r}, key=lambda k: (k != "level", k))
    with open(OUT / "same_arm_l20_cutflow.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        for r in flow:
            w.writerow({k: (f"{v:.4g}" if isinstance(v, float) else v) for k, v in r.items()})
    # opening-angle spectra at the reference level
    f = dict(LEVELS)[REF]
    si, sg = f(ci) & ci_true, f(cg)
    hi = np.histogram(ci["theta"][si], BINS)[0] * wi
    hg = {k: np.histogram(cg["theta"][sg & (cls == k)], BINS)[0] * wg for k in sorted(set(cls))}
    with open(OUT / "same_arm_l20.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["theta_lo", "theta_hi", "ipc_day", "ipc_mc"] + [f"gam: {k}" for k in hg] + ["gam_mc"])
        ni = np.histogram(ci["theta"][si], BINS)[0]
        ng = np.histogram(cg["theta"][sg], BINS)[0]
        for j in range(len(BINS) - 1):
            w.writerow([BINS[j], BINS[j + 1], f"{hi[j]:.4g}", ni[j]] + [f"{hg[k][j]:.4g}" for k in hg] + [ng[j]])
    # θ resolution of the IPC pairs (reco centroids vs truth)
    d = ci["theta"][si] - zi["theta"][ci["idx"][si]]
    if len(d) > 2:
            print(f"IPC θ_reco - θ_true at {REF}: median {np.median(d):+.2f}°, 68 % half-width "
              f"{0.5 * (np.percentile(d, 84) - np.percentile(d, 16)):.2f}°")
    plot(hi, hg, flow)


def plot(hi, hg, flow):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "serif", "font.size": 8, "axes.spines.top": False, "axes.spines.right": False})
    fig, ax = plt.subplots(figsize=(7.4, 2.9), constrained_layout=True)
    x = np.repeat(BINS, 2)[1:-1]
    cols = {"conversion in Cu hemisphere": "#8c564b", "conversion in TPC (frame, window, cathode, gas, PCB)": "#9467bd",
            "conversion in chamber wall + beam line": "#bcbd22", "conversion, elsewhere": "#7f7f7f",
            "other (Compton, δ rays)": "#c7c7c7"}
    bottom = np.zeros(len(BINS) - 1)
    for k, h in hg.items():
        if h.sum() == 0:
            continue
        ax.bar(BINS[:-1], h, width=5, bottom=bottom, align="edge", color=cols.get(k, "#aaaaaa"), lw=0,
               label=f"γ: {k}")
        bottom += h
    ax.plot(x, np.repeat(hi, 2), color="#e8692b", lw=1.6, label="M1 internal pairs, 17.64 MeV")
    ax.set_yscale("log")
    ax.set_xlim(0, 90)
    ax.set_xlabel("opening angle θ (deg), both leptons in one arm")
    ax.set_ylabel("pairs per 5° per beam day")
    ax.set_title("Same-arm pairs at 441 keV, 1 µA, after trigger, pointing 15°, separation > 1 cm", fontsize=8)
    ax.legend(fontsize=6.5, frameon=False, loc="upper left", bbox_to_anchor=(1.01, 1.0))
    (OUT / "figures").mkdir(exist_ok=True)
    fig.savefig(OUT / "figures" / "same_arm_l20.png", dpi=200)
    print("wrote", OUT / "figures" / "same_arm_l20.png")


if __name__ == "__main__":
    main()
