#!/usr/bin/env python3
"""drift_one.py <key> [ncoll] -- one Magboltz transport table for the LNL gas study (gas/GAS_STUDY.md §3).

Mixtures and conditions come from mixtures.py (the single source). Writes gas/out/tables/<key>.json with
v, D_L, D_T, Townsend alpha and attachment eta on a 60-point log grid 40-600 V/cm. Run inside
nTof_x17/garfield_sim/setup_garfield.sh (Garfield pin 927e5c21).
"""
import os, sys, json, time, ctypes
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mixtures import compositions, PRESSURE_TORR, TEMP_K, E_MIN, E_MAX, N_GRID, NCOLL

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out', 'tables')


def transport(gas, e):
    vx, vy, vz = ctypes.c_double(0.), ctypes.c_double(0.), ctypes.c_double(0.)
    gas.ElectronVelocity(0., 0., -e, 0., 0., 0., vx, vy, vz)
    eta, alpha = ctypes.c_double(0.), ctypes.c_double(0.)
    gas.ElectronAttachment(0., 0., -e, 0., 0., 0., eta)
    gas.ElectronTownsend(0., 0., -e, 0., 0., 0., alpha)
    dl, dt = ctypes.c_double(0.), ctypes.c_double(0.)
    gas.ElectronDiffusion(0., 0., -e, 0., 0., 0., dl, dt)
    return dict(E_Vcm=float(e), v_um_per_ns=float(vz.value * 1e4), eta_per_cm=float(eta.value),
                alpha_per_cm=float(alpha.value), dL_sqrtcm=float(dl.value), dT_sqrtcm=float(dt.value))


def main():
    key = sys.argv[1]
    ncoll = int(sys.argv[2]) if len(sys.argv) > 2 else NCOLL
    spec = compositions()[key]
    import ROOT
    ROOT.PyConfig.IgnoreCommandLineOptions = True
    ROOT.gROOT.SetBatch(True)
    ROOT.gErrorIgnoreLevel = ROOT.kError
    assert ROOT.gSystem.Load('libGarfield') >= 0
    import numpy as np
    gas = ROOT.Garfield.MediumMagboltz()
    comps = spec['comps']
    if len(comps) > 6:
        raise SystemExit('Magboltz takes at most 6 components')
    gas.SetComposition(*[x for pair in comps for x in pair])
    gas.SetTemperature(spec.get('T', TEMP_K))
    gas.SetPressure(spec.get('p', PRESSURE_TORR))
    gas.SetFieldGrid(E_MIN, E_MAX, N_GRID, True)
    t0 = time.time()
    print(f'{key}: {comps} ncoll={ncoll}', flush=True)
    gas.GenerateGasTable(ncoll)
    # the table's own nodes, plus a fine interpolated grid
    nodes = [transport(gas, float(e)) for e in np.logspace(np.log10(E_MIN), np.log10(E_MAX), N_GRID)]
    fine = [transport(gas, float(e)) for e in np.logspace(np.log10(E_MIN), np.log10(E_MAX), 60)]
    os.makedirs(OUT, exist_ok=True)
    out = os.path.join(OUT, f'{key}.json')
    json.dump(dict(key=key, **{k: v for k, v in spec.items() if k != 'comps'}, comps=comps,
                   pressure_torr=spec.get('p', PRESSURE_TORR), temp_K=spec.get('T', TEMP_K), ncoll=ncoll,
                   garfield_pin=os.environ.get('MX17_GARFIELD_PIN'), minutes=(time.time() - t0) / 60,
                   nodes=nodes, points=fine), open(out, 'w'), indent=1)
    print(f'{key}: done in {(time.time()-t0)/60:.1f} min -> {out}', flush=True)


if __name__ == '__main__':
    main()
