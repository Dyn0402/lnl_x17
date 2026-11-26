# sim2arm: the two-arm set-up simulated (2026-11-19)

The study behind the slot-1 run plan: what two Micromegas arms can see in 8 days at LNL, which geometry to use, and
what to measure. Write-up: [`TWO_ARM_STUDY.md`](TWO_ARM_STUDY.md).

| file | what |
|---|---|
| `two_arm_nd.py` | the FEASIBILITY_SIM §19 reference fit (x17_facility_search `lnl/target/shapes/shapes_nd.py`) cut to one arm pair; tasks `reach`, `spectra` |
| `summarize.py` | tables (`out/summary_*.csv`) and figures (`out/figures/`) |
| `EPC_L19.md`, `epc_l19.py`, `combine_l19.py` | run L19: the external conversions at ×100 L18 (26 Nov); `TA_EPC_RUN=L19` adds its table to the fit |
| `run_l19.sh`, `run_l19_full.sh`, `run_l19_all.sh` | the L19 fits: reference rows + spectra; the full reach grid (tags `_pass4li11_l19`, `_pass4_l19`, read by `planning/two_arm_estimates.py`) |
| `run_l19_checks.sh` | cosmic rate × 2.5 (`TA_COS_SCALE`, tag `_pass4li11_l19_cos2p5`) and 4 µA (`_cn4li11_l19`) |
| `li_thickness.py` | the Li film scan (slot1_feasibility/LI_THICKNESS.md) |
| `lxplus/` | copies of lxplus `/afs/cern.ch/work/d/dneff/git/x17_lnl/analysis/l15/`: the condor jobs of runs L15 (`submit_l15.sh` + `run_l15.sh`, cosmics, disk generator) and L16 (`submit_ta.sh`, arms rotated about the beam), the merge scripts, the Geant4 patch notes; `TWOARM_BIN` names the binary (MX17_Full_Geant branch `lnl_twoarm`) |
| `out/` | CSVs and figures |

Data: the merged tables are on EOS (`/eos/experiment/ntof/data/x17/lnl/target/sel_l1{1,3}`, `sel_v3`, `L15/`, `L16/`); the
local copies live in `$WORK_DATA/x17_facility_search/` (laptop: `/media/dylan/data/work/...`).

```
WORK_DATA=/media/dylan/data/work ~/PycharmProjects/nTof_x17/.venv/bin/python sim2arm/two_arm_nd.py reach --pairs vert horiz adj all -j 3 --tag _pass2
WORK_DATA=/media/dylan/data/work ~/PycharmProjects/nTof_x17/.venv/bin/python sim2arm/two_arm_nd.py spectra --pairs vert horiz adj all -j 3 --tag _pass2
python3 sim2arm/summarize.py --tag _pass2
```
