#!/usr/bin/env python3
"""
merge_l20.py <L20 sample dir> -o <out.npz>   (lnl_x17, 2026-11-27; interactive lxplus, reads /eos directly)

Joins each sub-run's lnl_reduce part (parts_lnl/: legs, calorimetry, primary-lepton truth, the γ's first interaction)
with its twotrack_reduce part (parts_2trk/) on eventID, and keeps the events the same-arm study needs: >= 2 tracks
(n >= 3 hits) in arm 0 or arm 1 (the horizontal pair of the beam days), or, for pair runs, both primary leptons in
arms 0/1 by truth.  Only arms 0 and 1 are written.  sim2arm/same_arm.py reads the output.
"""
from __future__ import annotations

import argparse
import glob
import os

import numpy as np

ARMS = [0, 1]
LNL_KEYS = ("legs", "theta", "em_ke", "ep_ke", "em_arm", "ep_arm", "g_fvol", "g_fproc", "g_fxyz")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sample_dir")
    ap.add_argument("-o", "--out", required=True)
    a = ap.parse_args()
    files = sorted(glob.glob(os.path.join(a.sample_dir, "parts_2trk", "*.npz")))
    ngen, nfiles, out = 0, 0, {}
    for p in files:
        q = os.path.join(a.sample_dir, "parts_lnl", os.path.basename(p))
        if not os.path.exists(q):
            print("missing", q)
            continue
        T, L = np.load(p), np.load(q, allow_pickle=False)
        ngen += int(T["n_generated"].sum())
        nfiles += 1
        lev = L["eventID"]
        if len(T["eventID"]) == 0 and "em_arm" not in L.files:
            continue
        # union of events: >= 2 tracks in arm 0/1, or (pairs) both primaries in arms 0/1
        sel = set()
        if len(T["eventID"]):
            two = (T["n_trk"][:, ARMS] >= 2).any(1)
            sel |= set(T["eventID"][two].tolist())
        if "em_arm" in L.files:
            both = np.isin(L["em_arm"], ARMS) & np.isin(L["ep_arm"], ARMS)
            sel |= set(lev[both].tolist())
        if not sel:
            continue
        ev = np.array(sorted(sel), np.int64)
        row = {"eventID": ev}
        il = np.clip(np.searchsorted(lev, ev), 0, max(len(lev) - 1, 0))
        okl = (lev[il] == ev) if len(lev) else np.zeros(len(ev), bool)
        for k in LNL_KEYS + ("E_sipm", "E_plast", "E_ls"):
            if k not in L.files:
                continue
            v = L[k][il]
            if k.startswith("E_"):
                v = v[:, ARMS]
            if v.dtype.kind == "f":
                v = np.where(okl.reshape((-1,) + (1,) * (v.ndim - 1)), v, np.nan)
            elif k == "legs":
                v = np.where(okl, v, 0)
            row[k] = v
        tev = T["eventID"]
        it = np.clip(np.searchsorted(tev, ev), 0, max(len(tev) - 1, 0))
        okt = (tev[it] == ev) if len(tev) else np.zeros(len(ev), bool)
        for k in T.files:
            if k in ("eventID", "n_generated"):
                continue
            v = T[k][it][:, ARMS] if len(tev) else None
            if v is None:
                continue
            fill = np.nan if v.dtype.kind == "f" else (-1 if k in ("trk_tid", "trk_pid") else 0)
            m = okt.reshape((-1,) + (1,) * (v.ndim - 1))
            row[k] = np.where(m, v, fill).astype(v.dtype)
        row["file_id"] = np.full(len(ev), nfiles - 1, np.int32)
        for k, v in row.items():
            out.setdefault(k, []).append(v)
    keys = set.intersection(*[set(k for k in out if len(out[k]) == len(out["eventID"]))]) if out else set()
    res = {k: np.concatenate(out[k]) for k in keys}
    res["n_generated"] = np.array([ngen])
    res["n_files"] = np.array([nfiles])
    np.savez_compressed(a.out, **res)
    print(f"{a.sample_dir}: {nfiles} sub-runs, {ngen} generated, {len(res.get('eventID', []))} kept -> {a.out}")


if __name__ == "__main__":
    main()
