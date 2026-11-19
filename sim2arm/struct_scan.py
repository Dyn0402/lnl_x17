#!/usr/bin/env python3
"""struct_scan.py -- two-arm days to 3σ (1.10 MeV, LNL calibrated, MM 15° + TOF, Cu hemisphere) against the size and
correlation length of the unknown-structure nuisance (lnl_nd.STRUCTS).  -> out/struct_scan_two_arm.csv
    WORK_DATA=/media/ucla/work ~/PycharmProjects/nTof_x17/.venv/bin/python sim2arm/struct_scan.py horiz vert"""
import sys; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parent))
import geom_syst as GS
import pandas as pd
SN,N=GS.SN,GS.N
N.STRUCTS['S_θ 2 %, ℓ/2 + S_θy 1 %']=[('S_θ',0.02,0.5),('S_θy',0.01)]
N.STRUCTS['S_θ 5 % + S_θy 2 %']=[('S_θ',0.05),('S_θy',0.02)]
rows=[]
for pair in sys.argv[1:]:
    ev,an=GS.collect(pair,'LNL calibrated','MM 15° + TOF')
    for st in ['none','S_θ 2 % + S_θy 1 %','S_θ 2 %, ℓ/2 + S_θy 1 %','S_θ 5 % + S_θy 2 %','S_θ 5 %, ℓ/2','S_θy 5 %, ℓ/2']:
        _,_,names,out=SN.templates(ev,an,st)
        d=SN.days_from(out,names,mu_floor=SN.mu_floor_of(ev,an,SN.FLOOR))
        rows.append(dict(pair=pair,struct=st,days3=d)); print(pair,st,round(d,2),flush=True)
pd.DataFrame(rows).to_csv(str(GS.TA.OUT / 'struct_scan_two_arm.csv'),index=False)
