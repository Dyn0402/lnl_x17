#!/usr/bin/env bash
# run_l19_all.sh [-j N] (2026-11-26): the four-arm rows ('all' pairs) of the L19 pass, which planning/two_arm_estimates.py
# reads for the Cu hemisphere's four-arm days; merged into two_arm_reach_pass4{,li11}_l19.csv, then the summaries again.
set -e
J=${1:-12}
cd "$(dirname "$0")/.."
PY=${PY:-$HOME/PycharmProjects/nTof_x17/.venv/bin/python}
export WORK_DATA=${WORK_DATA:-/media/ucla/work} OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 TA_EPC_RUN=L19
R=('LNL calibrated' 'n_TOF as is' 'LNL calibrated, LS off')
LV=('MM 15° + TOF' 'MM 15° point, μ 3°')
for s in li11 ""; do
  if [ "$s" = li11 ]; then export LI_UG=587; else unset LI_UG; fi
  $PY sim2arm/two_arm_nd.py reach --pairs all --resps "${R[@]}" --levels "${LV[@]}" --mcs direct transplant -j $J --tag _pass4${s}_l19_all
  $PY -c "import pandas as pd; pd.concat([pd.read_csv('sim2arm/out/two_arm_reach_pass4${s}_l19_d.csv'), pd.read_csv('sim2arm/out/two_arm_reach_pass4${s}_l19_t.csv'), pd.read_csv('sim2arm/out/two_arm_reach_pass4${s}_l19_all.csv')]).to_csv('sim2arm/out/two_arm_reach_pass4${s}_l19.csv', index=False)"
  $PY sim2arm/summarize.py --tag _pass4${s}_l19
done
echo "run_l19_all done"
