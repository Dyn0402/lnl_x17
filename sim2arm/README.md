# sim2arm: the two-arm set-up simulated (2026-11-19)

The study behind the slot-1 run plan: what two Micromegas arms can see in 8 days at LNL, which geometry to use, and
what to measure. Write-up: [`TWO_ARM_STUDY.md`](TWO_ARM_STUDY.md).

| file | what |
|---|---|
| `two_arm_nd.py` | the FEASIBILITY_SIM §19 reference fit (x17_facility_search `lnl/target/shapes/shapes_nd.py`) cut to one arm pair; tasks `reach`, `spectra` |
| `summarize.py` | tables (`out/summary_*.csv`) and figures (`out/figures/`) |
| `lxplus/` | the condor jobs of runs L15 (cosmics, disk generator) and L16 (arms rotated about the beam), the Geant4 patch notes |
| `out/` | CSVs and figures |

Data: the merged tables are on EOS (`/eos/experiment/ntof/data/x17/lnl/target/sel_l1{1,3}`, `sel_v3`, `L15/`, `L16/`); the
local copies live in `$WORK_DATA/x17_facility_search/` (laptop: `/media/dylan/data/work/...`).

```
WORK_DATA=/media/dylan/data/work ~/PycharmProjects/nTof_x17/.venv/bin/python sim2arm/two_arm_nd.py reach --pairs vert horiz adj all -j 3 --tag _pass2
WORK_DATA=/media/dylan/data/work ~/PycharmProjects/nTof_x17/.venv/bin/python sim2arm/two_arm_nd.py spectra --pairs vert horiz adj all -j 3 --tag _pass2
python3 sim2arm/summarize.py --tag _pass2
```
