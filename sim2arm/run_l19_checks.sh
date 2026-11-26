#!/usr/bin/env bash
# run_l19_checks.sh [-j N] (2026-11-26): two checks on the L19 reference fit (horizontal pair, 11 µm, built Cu hemisphere):
#  1. the cosmic-ray rate x 2.5 (TA_COS_SCALE; R9: n_TOF beam-off wall coincidences are 2.5 x the toy MC), tag _pass4li11_l19_cos2p5
#  2. 4 µA (TA_IUA=4) with the L19 external conversions, tag _cn4li11_l19 (the 25 Nov 1.7 x used L18)
set -e
J=${1:-8}
cd "$(dirname "$0")/.."
PY=${PY:-$HOME/PycharmProjects/nTof_x17/.venv/bin/python}
export WORK_DATA=${WORK_DATA:-/media/ucla/work} OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 TA_EPC_RUN=L19 LI_UG=587
R=('LNL calibrated' 'n_TOF as is' 'LNL calibrated, LS off')
TA_COS_SCALE=2.5 $PY sim2arm/two_arm_nd.py reach --pairs horiz --resps "${R[@]}" --levels 'MM 15° + TOF' 'MM 15° point, μ 3°' \
  --mcs direct transplant -j $J --tag _pass4li11_l19_cos2p5
$PY sim2arm/summarize.py --tag _pass4li11_l19_cos2p5
TA_IUA=4 $PY sim2arm/two_arm_nd.py reach --pairs horiz --resps "${R[@]}" --levels 'MM 15° + TOF' \
  --mcs direct transplant -j $J --tag _cn4li11_l19
$PY sim2arm/summarize.py --tag _cn4li11_l19
echo "run_l19_checks done"
