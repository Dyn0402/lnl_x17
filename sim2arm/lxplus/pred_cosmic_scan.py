#!/usr/bin/env python3
"""
pred_cosmic_scan.py -- L15 cosmic (or L13 γ-line) parts (lnl_reduce + lnl_time) -> the trigger-level table the predictions need.

    python3 pred_cosmic_scan.py <L15 sample dir> -o pred_cosmic.npz        (interactive lxplus; reads /eos directly)

The merged L15 table (`lnl_merge.py`) keeps only events with >= 2 "ok" arms (leg + Micromegas segment in the active
area), so it cannot say how many two-arm *triggers* have 0, 1 or 2 tracks.  This scan keeps, for every event where
any two arms of the three pairs used in slot 1 (vertical 2+3, horizontal 0+1, adjacent 0+2) both have a trigger leg:
the per-arm leg / MM / energy / time / segment columns and the muon truth direction.  Also per-arm counters over all
events (legs, MM segments, both).  The selection definitions are lnl_merge.py's, unchanged.

lnl_x17 sim2arm/predictions.py reads the output (copied to $WORK_DATA/x17_facility_search/pred/).
"""
from __future__ import annotations

import argparse
import glob
import os

import numpy as np

HALF_ALONG, HALF_TRANS = 180.0, 199.7
SHIFT = np.array([15.5, -15.75, -16.35, 17.3])
TRANS_AX = np.array([2, 2, 0, 0])
PAIRS = ((2, 3), (0, 1), (0, 2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sample_dir")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--max-files", type=int, default=0)
    ap.add_argument("--mode", default="pairs", choices=("pairs", "single"),
                    help="pairs: events with legs in both arms of a slot-1 pair (cosmics); single: any leg (γ lines)")
    a = ap.parse_args()
    files = sorted(glob.glob(os.path.join(a.sample_dir, "parts_lnl", "*.npz")))
    if a.max_files:
        files = files[:a.max_files]
    cnt = dict(n_generated=0, n_files=0, leg_arm=np.zeros(4, np.int64), mm_arm=np.zeros(4, np.int64),
               ok_arm=np.zeros(4, np.int64), leg_only1=np.zeros(4, np.int64), ok_only1=np.zeros(4, np.int64))
    keep = {}
    for n, p in enumerate(files):
        z = np.load(p)
        tp = os.path.join(a.sample_dir, "parts_time", os.path.basename(p))
        T = np.load(tp) if os.path.exists(tp) else None
        cnt["n_generated"] += int(z["n_generated"].sum())
        cnt["n_files"] += 1
        ev = z["eventID"]
        N = len(ev)
        if N == 0:
            continue
        C = z["seg_c_all"].astype(float)
        arms = np.arange(4)
        trans = C[:, arms, TRANS_AX] - SHIFT[None, :]
        active = (np.abs(C[:, :, 1]) < HALF_ALONG) & (np.abs(trans) < HALF_TRANS)
        mm = (z["seg_n_dom"] >= 3) & (z["seg_e"] > 0) & active
        legs = z["legs"].astype(np.int64)
        leg = ((legs[:, None] >> arms[None, :]) & 1).astype(bool)
        ok = leg & mm
        cnt["leg_arm"] += leg.sum(0)
        cnt["mm_arm"] += mm.sum(0)
        cnt["ok_arm"] += ok.sum(0)
        one = leg.sum(1) == 1
        cnt["leg_only1"] += (leg & one[:, None]).sum(0)
        cnt["ok_only1"] += (ok & one[:, None]).sum(0)
        anyp = np.zeros(N, bool)
        for i, j in PAIRS:
            anyp |= leg[:, i] & leg[:, j]
        if a.mode == "single":
            anyp = leg.any(1)
        if not anyp.any():
            continue
        s = anyp
        t_s = np.full((N, 4), np.nan, np.float32)
        t_p = np.full((N, 4), np.nan, np.float32)
        if T is not None and len(T["ev"]):
            k = np.clip(np.searchsorted(T["ev"], ev), 0, len(T["ev"]) - 1)
            hit = T["ev"][k] == ev
            t_s[hit], t_p[hit] = T["t_sipm"][k[hit]], T["t_plast"][k[hit]]
        Earm = (z["E_sipm"] + z["E_plast"] + z["E_ls"]).astype(np.float32)
        rec = dict(leg=leg[s], mm=mm[s], E=Earm[s], E_sipm=z["E_sipm"][s], E_plast=z["E_plast"][s],
                   t_sipm=t_s[s], t_plast=t_p[s], c_all=z["seg_c_all"][s].astype(np.float32),
                   c_dom=z["seg_c_dom"][s].astype(np.float32), d_dom=z["seg_d_dom"][s].astype(np.float32),
                   mu_d=z["em_d"][s].astype(np.float32), mu_ke=z["em_ke"][s].astype(np.float32),
                   V=z["V"][s].astype(np.float32), seg_e=z["seg_e"][s].astype(np.float32),
                   seg_n_dom=z["seg_n_dom"][s].astype(np.float32), seg_fdom=z["seg_fdom"][s].astype(np.float32),
                   line=z["inv_mass"][s].astype(np.float32))
        if a.mode == "single":                  # γ lines: no segment geometry needed, keep the table small
            for k2 in ("c_all", "c_dom", "d_dom", "mu_d", "t_plast", "E_sipm", "E_plast"):
                rec.pop(k2)
        for k2, v in rec.items():
            keep.setdefault(k2, []).append(v)
        if n % 100 == 0:
            print(f"{n}/{len(files)} {p}: {N} rows, {int(s.sum())} pair-leg events", flush=True)
    out = {k: np.concatenate(v) for k, v in keep.items()}
    for k, v in cnt.items():
        out[f"cnt_{k}"] = np.asarray(v)
    np.savez_compressed(a.out, **out)
    print(f"{a.out}: {cnt['n_files']} files, {cnt['n_generated']:,} muons, {len(out['leg']):,} pair-leg events")


if __name__ == "__main__":
    main()
