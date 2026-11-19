#!/usr/bin/env bash
# run_pass.sh <tag> [-j N]: the full two-arm grid (reach direct + transplant, 20 µm and 11 µm; spectra), then the summaries.
set -e
T=${1:-_pass2}; J=${2:-6}
cd "$(dirname "$0")/.."
PY=${PY:-$HOME/PycharmProjects/nTof_x17/.venv/bin/python}
export WORK_DATA=${WORK_DATA:-/media/dylan/data/work}
L4="trigger;MM 15° point, μ 3°;MM 15° point, μ 3° + TOF 1 ns;MM 15° + TOF"
IFS=';' read -ra LV <<< "$L4"
R=('LNL calibrated' 'n_TOF as is' 'LNL calibrated, LS off')
$PY sim2arm/two_arm_nd.py reach --pairs vert horiz adj all --resps "${R[@]}" --levels "${LV[@]}" --mcs direct -j $J --tag ${T}_d
$PY sim2arm/two_arm_nd.py reach --pairs vert horiz adj all --resps "${R[@]}" --levels 'MM 15° + TOF' 'MM 15° point, μ 3°' --mcs transplant -j $J --tag ${T}_t
LI_UG=587 $PY sim2arm/two_arm_nd.py reach --pairs vert horiz all --resps "${R[@]}" --levels "${LV[@]}" --mcs direct -j $J --tag ${T}li11_d
LI_UG=587 $PY sim2arm/two_arm_nd.py reach --pairs vert horiz all --resps "${R[@]}" --levels 'MM 15° + TOF' 'MM 15° point, μ 3°' --mcs transplant -j $J --tag ${T}li11_t
$PY sim2arm/two_arm_nd.py spectra --pairs vert horiz adj all --resps 'LNL calibrated' 'n_TOF as is' --levels trigger 'MM 15° point, μ 3°' 'MM 15° + TOF' --eps 1100 441 -j $J --tag $T
LI_UG=587 $PY sim2arm/two_arm_nd.py spectra --pairs vert horiz adj --resps 'LNL calibrated' --levels 'MM 15° + TOF' --eps 1100 441 -j $J --tag ${T}li11
for s in "" li11; do
  $PY -c "import pandas as pd; pd.concat([pd.read_csv('sim2arm/out/two_arm_reach${T}${s}_d.csv'), pd.read_csv('sim2arm/out/two_arm_reach${T}${s}_t.csv')]).to_csv('sim2arm/out/two_arm_reach${T}${s}.csv', index=False)"
  $PY sim2arm/summarize.py --tag ${T}${s}
done
$PY sim2arm/cosmic_rates.py
echo "pass $T done"
