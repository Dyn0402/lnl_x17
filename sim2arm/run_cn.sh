#!/usr/bin/env bash
# run_cn.sh [-j N]: the two-arm reach at 2 and 4 µA (2026-11-25: CN instead of AN2000).  Horizontal pair, 11 µm, reference
# veto, the built Cu hemisphere (dome300) and the Al ogive + Cu liner (L12 + L13).  New tags _cn<I>[al]li11 only.
set -e
J=${1:-6}
cd "$(dirname "$0")/.."
PY=${PY:-$HOME/PycharmProjects/nTof_x17/.venv/bin/python}
export WORK_DATA=${WORK_DATA:-/media/ucla/work}
R=('LNL calibrated' 'n_TOF as is' 'LNL calibrated, LS off')
for I in 4 2; do
  TA_IUA=$I LI_UG=587 $PY sim2arm/two_arm_nd.py reach --pairs horiz --resps "${R[@]}" --levels 'MM 15° + TOF' \
    --mcs direct transplant -j $J --tag _cn${I}li11
  TA_IUA=$I LI_UG=587 TA_CFG=ogAl300cu12r8m4 $PY sim2arm/two_arm_nd.py reach --pairs horiz --resps "${R[@]}" \
    --levels 'MM 15° + TOF' --mcs direct transplant -j $J --tag _cn${I}alli11
done
echo "run_cn done"
