#!/usr/bin/env python3
"""
traj_pick.py -- keep the trajectory-dump rows of the events worth drawing (lnl_x17 predictions tab, 2026-11-20).

    python3 traj_pick.py <traj.csv> <part.npz> <time.npz> --mode pair|gam|cosmic --arms 0,1 -o <prefix>

Inputs are one job's outputs: MX17_Full_Geant --trajdump CSV, lnl_reduce.py part, lnl_time.py part.  An arm is
"ok" as in lnl_merge.py (trigger leg + Micromegas segment in the active area).
  pair   : both arms ok                         (IPC / X17 pairs seen as the analysis sees them)
  gam    : a leg in one of the arms             (γ singles; with or without a Micromegas segment)
  cosmic : a leg in both arms                   (two-arm cosmic triggers)
Writes <prefix>_traj.csv.gz (rows of the kept events) and <prefix>_evt.npz (their reduced rows + arm times).
"""
from __future__ import annotations

import argparse

import numpy as np
import pandas as pd

HALF_ALONG, HALF_TRANS = 180.0, 199.7
SHIFT = np.array([15.5, -15.75, -16.35, 17.3])
TRANS_AX = np.array([2, 2, 0, 0])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("traj")
    ap.add_argument("part")
    ap.add_argument("time")
    ap.add_argument("--mode", required=True, choices=("pair", "gam", "cosmic"))
    ap.add_argument("--arms", default="0,1")
    ap.add_argument("--max", type=int, default=40)
    ap.add_argument("-o", "--out", required=True)
    a = ap.parse_args()
    i, j = (int(x) for x in a.arms.split(","))
    z = dict(np.load(a.part))
    z.pop("n_generated", None)
    ev = z["eventID"]
    C = z["seg_c_all"].astype(float)
    arms = np.arange(4)
    trans = C[:, arms, TRANS_AX] - SHIFT[None, :]
    active = (np.abs(C[:, :, 1]) < HALF_ALONG) & (np.abs(trans) < HALF_TRANS)
    mm = (z["seg_n_dom"] >= 3) & (z["seg_e"] > 0) & active
    leg = ((z["legs"].astype(np.int64)[:, None] >> arms[None, :]) & 1).astype(bool)
    ok = leg & mm
    if a.mode == "pair":
        m = ok[:, i] & ok[:, j]
    elif a.mode == "gam":
        m = leg[:, i] | leg[:, j]
    else:
        m = leg[:, i] & leg[:, j]
    keep = ev[m][:a.max]
    T = np.load(a.time)
    t_s = np.full((len(ev), 4), np.nan, np.float32)
    if len(T["ev"]):
        k = np.clip(np.searchsorted(T["ev"], ev), 0, len(T["ev"]) - 1)
        hit = T["ev"][k] == ev
        t_s[hit] = T["t_sipm"][k[hit]]
    sel = np.isin(ev, keep)
    out = {k2: v[sel] for k2, v in z.items()}
    out.update(mm=mm[sel], leg=leg[sel], t_sipm=t_s[sel])
    np.savez_compressed(a.out + "_evt.npz", **out)
    kept = set(int(x) for x in keep)
    parts = []
    for ch in pd.read_csv(a.traj, chunksize=2_000_000):
        parts.append(ch[ch.eventID.isin(kept)])
    df = pd.concat(parts) if parts else pd.DataFrame()
    df.to_csv(a.out + "_traj.csv.gz", index=False, float_format="%.6g")
    print(f"{a.mode} arms {i},{j}: {len(ev)} reduced rows, {int(m.sum())} pass, kept {len(kept)} events, "
          f"{len(df)} trajectory rows")


if __name__ == "__main__":
    main()
