#!/usr/bin/env bash
# run_l19.sh [-j N]: the two-arm fits with the external conversions of run L19 (x100 L18) added to the EPC pair
# component (TA_EPC_RUN=L19; lnl_x17 R12, 2026-11-25).  11 µm, 1 µA, the built Cu hemisphere.  New tags *_l19 only.
#   python3 sim2arm/combine_l19.py first ($WORK_DATA/x17_facility_search/sel_l19/L19_gam_8Be_dome300_asb_sel.npz)
set -e
J=${1:-8}
cd "$(dirname "$0")/.."
PY=${PY:-$HOME/PycharmProjects/nTof_x17/.venv/bin/python}
export WORK_DATA=${WORK_DATA:-/media/ucla/work} OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
R=('LNL calibrated' 'n_TOF as is' 'LNL calibrated, LS off')
TA_EPC_RUN=L19 LI_UG=587 $PY sim2arm/two_arm_nd.py reach --pairs horiz --resps "${R[@]}" --levels 'MM 15° + TOF' \
  --mcs direct transplant -j $J --tag _pass4li11_l19
TA_EPC_RUN=L19 LI_UG=587 $PY sim2arm/two_arm_nd.py spectra --pairs horiz adj --resps 'LNL calibrated' \
  --levels 'MM 15° + TOF' --eps 1100 441 -j $J --tag _pass4li11_l19
# the same without L19 for a like-for-like comparison of the spectra (pass4li11 spectra exist; reach too)
echo "run_l19 done"
