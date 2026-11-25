#!/usr/bin/env python3
"""
lnl_first.py <run_t0.root> <part.npz>   (lnl_x17 EPC run L19, 2026-11-25)

Adds the primary γ's first interaction to a reduced part (lnl_reduce.py output), joined on eventID:
    g_fvol  (U24)  logical volume of the first non-transport step ('' = never interacted, 'escaped' = killed)
    g_fproc (U12)  its process (conv, compt, phot, Rayl, photonNuclear, killed)
    g_fxyz  (N,3)  its position [mm]
MX17_Full_Geant lnl_twoarm >= 07bea64 fills first_* for --gamma-lines (before: neutrons only).  The part is rewritten
in place.  lnl_merge_rot.py passes every g_* key through for the selected (>= 2 ok arm) rows.
"""
import sys

import numpy as np
import uproot


def main():
    root, part = sys.argv[1], sys.argv[2]
    t = uproot.open(root)['EventTree']
    a = t.arrays(['eventID', 'first_vol', 'first_proc', 'first_x', 'first_y', 'first_z'], library='np')
    z = dict(np.load(part))
    ev = z['eventID']
    o = np.argsort(a['eventID'])
    eid = a['eventID'][o]
    i = np.clip(np.searchsorted(eid, ev), 0, len(eid) - 1)
    ok = eid[i] == ev
    if not ok.all():
        print(f'WARNING: {(~ok).sum()} kept events not in EventTree')
    j = o[i]

    def s(x, n):
        return np.array([v.decode() if isinstance(v, bytes) else str(v) for v in x], dtype=f'U{n}')
    z['g_fvol'] = np.where(ok, s(a['first_vol'][j], 24), '?')
    z['g_fproc'] = np.where(ok, s(a['first_proc'][j], 12), '?')
    z['g_fxyz'] = np.stack([a['first_x'][j], a['first_y'][j], a['first_z'][j]], 1).astype(np.float32)
    # every generated event's first-interaction volume, counted (for rates per volume without the kept-row bias)
    allv, cnt = np.unique(s(a['first_vol'], 24), return_counts=True)
    z['gcnt_vol'] = allv
    z['gcnt_n'] = cnt.astype(np.int64)
    np.savez_compressed(part, **z)
    print(f'{part}: first-interaction columns for {len(ev)} rows; volumes {dict(zip(allv[:8], cnt[:8]))}')


if __name__ == '__main__':
    main()
