#!/usr/bin/env python3
"""
twotrack_reduce.py -- one MX17_Full_Geant ROOT file -> the strongest Micromegas tracks of each arm   (lnl_x17, 2026-11-27)

    python3 twotrack_reduce.py <run_t0.root> -o <part_2trk.npz>

For the same-arm pair study (run L20, sim2arm/SAME_ARM.md).  lnl_reduce.py keeps one segment per arm (the dominant
track, seg_reduce.py), so two tracks in one TPC cannot be rebuilt from it.  Here every charged track in each arm's drift
gas is fitted on its own (truth separation of the tracks = perfect pattern recognition):
    per (event, arm, trackID): hits n, energy E [MeV], edep-weighted centroid C [mm], PCA direction D of the
    0.5 mm-smeared hits (oriented away from the beam spot), parentID, charge q (-1 e-, +1 e+, 0 other).
Per event and arm the K = 3 most energetic tracks with n >= 3 are kept (trk_* arrays, shape (N, 4, K)), with
E_gas (all charged hits) and n_trk (tracks with n >= 3).  Only events with a track (n >= 3) in some arm are kept;
n_generated keeps the normalisation.  Legs and calorimetry are in the lnl_reduce.py part of the same sub-run (join on
eventID).
"""
from __future__ import annotations

import argparse

import numpy as np
import uproot

K = 3
NARM = 4
SMEAR_MM = 0.5
BR = ["eventID", "trackID", "parentID", "armID", "detType", "particle", "edep", "gx", "gy", "gz"]


def _s(a):
    return np.array([x.decode() if isinstance(x, bytes) else str(x) for x in a])


def process(t, rng, out):
    det = _s(t["detType"])
    prt = _s(t["particle"])
    m = (det == "DriftGas") & ~np.isin(prt, ["gamma", "neutron", "nu_e", "anti_nu_e", "opticalphoton"])
    m &= (t["armID"] >= 0) & (t["armID"] < NARM)
    if not m.any():
        return
    ev = t["eventID"][m].astype(np.int64)
    arm = t["armID"][m].astype(np.int64)
    tid = t["trackID"][m].astype(np.int64)
    pid = t["parentID"][m].astype(np.int64)
    q = np.where(prt[m] == "e-", -1, np.where(prt[m] == "e+", 1, 0)).astype(np.int8)
    e = t["edep"][m].astype(float) * 1e-6
    X = np.stack([t["gx"][m], t["gy"][m], t["gz"][m]], 1).astype(float)
    Xs = X + rng.normal(0, SMEAR_MM, X.shape)
    # arm totals
    ka = ev * NARM + arm
    ua, ia = np.unique(ka, return_inverse=True)
    Ea = np.bincount(ia, e)
    # tracks
    tmax = int(tid.max()) + 1
    kt = ka * tmax + tid
    ut, first, it = np.unique(kt, return_index=True, return_inverse=True)
    nt = len(ut)
    n = np.bincount(it, minlength=nt).astype(float)
    E = np.bincount(it, e, minlength=nt)
    w = np.maximum(E, 1e-30)
    C = np.stack([np.bincount(it, e * X[:, k], minlength=nt) for k in range(3)], 1) / w[:, None]
    mu = np.stack([np.bincount(it, Xs[:, k], minlength=nt) for k in range(3)], 1) / n[:, None]
    Xc = Xs - mu[it]
    M = np.empty((nt, 3, 3))
    for a in range(3):
        for b in range(a, 3):
            M[:, a, b] = M[:, b, a] = np.bincount(it, Xc[:, a] * Xc[:, b], minlength=nt)
    _, vecs = np.linalg.eigh(M)
    D = vecs[:, :, 2]
    sg = np.sign((D * mu).sum(1))
    sg[sg == 0] = 1
    D *= sg[:, None]
    good = n >= 3
    out.append(dict(ka=ka, ua=ua, Ea=Ea, tk=ut[good] // tmax, n=n[good], E=E[good], C=C[good], D=D[good],
                    tid=tid[first][good], pid=pid[first][good], q=q[first][good]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--seed", type=int, default=7)
    a = ap.parse_args()
    rng = np.random.default_rng(a.seed)
    f = uproot.open(a.file)
    ngen = int(f["EventTree"].num_entries)
    chunks: list = []
    carry = None
    for t in f["HitTree"].iterate(BR, library="np", step_size="200 MB"):
        if carry is not None:
            t = {k: np.concatenate([carry[k], t[k]]) for k in t}
        cut = np.searchsorted(t["eventID"], t["eventID"][-1], side="left")
        carry = {k: v[cut:] for k, v in t.items()}
        if cut:
            process({k: v[:cut] for k, v in t.items()}, rng, chunks)
    if carry is not None and len(carry["eventID"]):
        process(carry, rng, chunks)
    if chunks:
        cat = {k: np.concatenate([c[k] for c in chunks]) for k in ("ua", "Ea", "tk", "n", "E", "C", "D", "tid", "pid", "q")}
    else:
        cat = None
    if cat is None or len(cat["tk"]) == 0:
        np.savez_compressed(a.out, eventID=np.zeros(0, np.int64), n_generated=np.array([ngen]))
        print(f"twotrack_reduce: {ngen} generated, 0 kept")
        return
    evs = np.unique(cat["tk"] // NARM)
    N = len(evs)
    E_gas = np.zeros((N, NARM), np.float32)
    i = np.searchsorted(evs, cat["ua"] // NARM)
    ok = (i < N) & (evs[np.clip(i, 0, N - 1)] == cat["ua"] // NARM)
    np.add.at(E_gas, (i[ok], (cat["ua"] % NARM)[ok]), cat["Ea"][ok])
    # sort tracks by (event-arm key, -E) and keep the first K of each
    o = np.lexsort((-cat["E"], cat["tk"]))
    tk = cat["tk"][o]
    start = np.r_[True, tk[1:] != tk[:-1]]
    grp = np.cumsum(start) - 1
    rank = np.arange(len(tk)) - np.flatnonzero(start)[grp]
    n_trk = np.zeros((N, NARM), np.int16)
    ie = np.searchsorted(evs, tk // NARM)
    np.add.at(n_trk, (ie, tk % NARM), 1)
    keep = rank < K
    ie, ia, ir = ie[keep], (tk % NARM)[keep], rank[keep]
    o = o[keep]
    out = dict(eventID=evs, n_generated=np.array([ngen]), E_gas=E_gas, n_trk=n_trk)
    for k, shp, dt, fill in (("n", (), np.float32, 0), ("E", (), np.float32, 0), ("tid", (), np.int32, -1),
                             ("pid", (), np.int32, -1), ("q", (), np.int8, 0), ("C", (3,), np.float32, np.nan),
                             ("D", (3,), np.float32, np.nan)):
        arr = np.full((N, NARM, K) + shp, fill, dt)
        arr[ie, ia, ir] = cat[k][o]
        out[f"trk_{k}"] = arr
    np.savez_compressed(a.out, **out)
    print(f"twotrack_reduce: {ngen} generated, {N} kept, {(n_trk >= 2).any(1).sum()} with >= 2 tracks in an arm")


if __name__ == "__main__":
    main()
