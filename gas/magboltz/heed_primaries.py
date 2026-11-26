#!/usr/bin/env python3
"""heed_primaries.py -- primary clusters and electrons per cm for an 8 MeV electron in each dry candidate (HEED).
Writes gas/out/heed_primaries.json. GAS_STUDY.md §4."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mixtures import BASES, PRESSURE_TORR, TEMP_K
import ROOT
ROOT.gROOT.SetBatch(True); ROOT.gErrorIgnoreLevel = ROOT.kError
assert ROOT.gSystem.Load('libGarfield') >= 0
G = ROOT.Garfield
out = {}
for b, (comps, role) in BASES.items():
    gas = G.MediumMagboltz(); gas.SetComposition(*[x for p in comps for x in p])
    gas.SetTemperature(TEMP_K); gas.SetPressure(PRESSURE_TORR)
    box = G.SolidBox(0, 0, 0, 50, 50, 50); geo = G.GeometrySimple(); geo.AddSolid(box, gas)
    cmp = G.ComponentConstant(); cmp.SetGeometry(geo); cmp.SetElectricField(0, 0, 100)
    sen = G.Sensor(); sen.AddComponent(cmp)
    tr = G.TrackHeed(sen); tr.SetParticle('e-'); tr.SetKineticEnergy(8e6)
    L, N = 3.0, 4000; nc = ne = 0
    for i in range(N):
        tr.NewTrack(0, 0, 0, 0, 0, 0, 1)
        for c in tr.GetClusters():
            if c.z <= L: nc += 1; ne += len(c.electrons)
    out[b] = dict(clusters_per_cm=nc / N / L, electrons_per_cm=ne / N / L, role=role)
    print(f'{b:22s} {nc/N/L:6.1f} clusters/cm {ne/N/L:6.1f} e/cm', flush=True)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out', 'heed_primaries.json'), 'w'), indent=1)
