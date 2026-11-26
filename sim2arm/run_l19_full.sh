#!/usr/bin/env bash
# run_l19_full.sh [-j N]: the reach grid that planning/two_arm_estimates.py reads (horizontal + vertical pair, the two
# cosmic-veto levels, 3 responses, direct + transplant, 20 µm and 11 µm), with the L19 external conversions
# (TA_EPC_RUN=L19), then the summaries.  Tags _pass4_l19 and _pass4li11_l19.  2026-11-26 (the HANDOFF's next step 2).
set -e
J=${1:-12}
cd "$(dirname "$0")/.."
PY=${PY:-$HOME/PycharmProjects/nTof_x17/.venv/bin/python}
export WORK_DATA=${WORK_DATA:-/media/ucla/work} OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 TA_EPC_RUN=L19
R=('LNL calibrated' 'n_TOF as is' 'LNL calibrated, LS off')
LV=('MM 15° + TOF' 'MM 15° point, μ 3°')
for s in li11 ""; do
  if [ "$s" = li11 ]; then export LI_UG=587; else unset LI_UG; fi
  $PY sim2arm/two_arm_nd.py reach --pairs vert horiz --resps "${R[@]}" --levels "${LV[@]}" --mcs direct -j $J --tag _pass4${s}_l19_d
  $PY sim2arm/two_arm_nd.py reach --pairs vert horiz --resps "${R[@]}" --levels "${LV[@]}" --mcs transplant -j $J --tag _pass4${s}_l19_t
  $PY -c "import pandas as pd; pd.concat([pd.read_csv('sim2arm/out/two_arm_reach_pass4${s}_l19_d.csv'), pd.read_csv('sim2arm/out/two_arm_reach_pass4${s}_l19_t.csv')]).to_csv('sim2arm/out/two_arm_reach_pass4${s}_l19.csv', index=False)"
  $PY sim2arm/summarize.py --tag _pass4${s}_l19
done
echo "run_l19_full done"
