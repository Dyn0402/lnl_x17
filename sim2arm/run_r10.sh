#!/usr/bin/env bash
# run_r10.sh [-j N]: task R10 (2026-11-25), the two-arm reach of the Al ogive + Cu liner (ogAl300cu12r8m4), with the
# pass-4 settings (L15 cosmics, sigma_t 0.6 ns).  New tags only: _pass5al<SFX> (20 µm), _pass5al<SFX>li11 (11 µm; SFX '' =
# the L12 tables alone, the first pass; R10_SFX=_l13 = L12 + L13, the x30 tables, the numbers of record), and the checks
# _pass5al_closure (dome300, must reproduce pass 4) and _pass5al_old (the §19.3 settings: 0.3 ns, L4 cosmics, 20 µm).
# Nothing of passes 1-4 is touched.  Write-up: R10_AL_OGIVE.md (r10_al_ogive.py builds its tables).
#   WORK_DATA=/media/ucla/work bash sim2arm/run_r10.sh 6            # steps 1-4, ~1 h
#   WORK_DATA=/media/ucla/work R10_STEPS="5" bash sim2arm/run_r10.sh 6   # the rest of the grid (vertical pair, other vetoes)
#   WORK_DATA=/media/ucla/work R10_STEPS="6" bash sim2arm/run_r10.sh 6   # the thin-table test (Cu ogive L11, hemisphere L10)
#   WORK_DATA=/media/ucla/work R10_STEPS="2 3" R10_SFX=_l13 bash sim2arm/run_r10.sh 6   # L12 + L13 (the L13 Al-ogive tables
#       were fetched into $WORK_DATA/x17_facility_search/lnl_sel/ on 25 Nov): tags _pass5al_l13, _pass5al_l13li11
set -e
J=${1:-6}
X=${R10_SFX:-}
# the L13 Al-ogive tables are on this disk since 25 Nov (fetched for the _l13 rerun).  Without a suffix the tags are the
# L12-only ones of the first pass, so those fits read L12 alone (TA_RUNS); with a suffix they read L12 + L13.
ALR=L12; [ -n "$X" ] && ALR=
cd "$(dirname "$0")/.."
PY=${PY:-$HOME/PycharmProjects/nTof_x17/.venv/bin/python}
export WORK_DATA=${WORK_DATA:-/media/dylan/data/work}
AL=ogAl300cu12r8m4
R=('LNL calibrated' 'n_TOF as is' 'LNL calibrated, LS off')
LV=('MM 15° + TOF' 'MM 15° point, μ 3°')
STEPS=${R10_STEPS:-1 2 3 4}
for s in $STEPS; do case $s in
1)  # closure: the built Cu hemisphere, horizontal pair, liquid working, 11 µm (pass 4: 189.5 / 120.3 d, central 151 d)
    LI_UG=587 $PY sim2arm/two_arm_nd.py reach --pairs horiz --resps 'LNL calibrated' --levels 'MM 15° + TOF' \
      --mcs direct transplant -j 2 --tag _pass5al_closure ;;
2)  LI_UG=587 TA_CFG=$AL TA_RUNS=$ALR $PY sim2arm/two_arm_nd.py reach --pairs horiz all --resps "${R[@]}" --levels "${LV[@]}" \
      --mcs direct transplant -j $J --tag _pass5al${X}li11 ;;
3)  TA_CFG=$AL TA_RUNS=$ALR $PY sim2arm/two_arm_nd.py reach --pairs horiz all --resps "${R[@]}" --levels "${LV[@]}" \
      --mcs direct transplant -j $J --tag _pass5al$X ;;
4)  # like for like with FEASIBILITY_SIM §19.3 (4.5 / 8.5 d, four arms): the old 0.3 ns time of flight and the L4 cosmics
    LNL_TOF_SIGMA_NS=0.3 COSMICS=L4 TA_CFG=$AL TA_RUNS=L12 $PY sim2arm/two_arm_nd.py reach --pairs all horiz \
      --resps 'LNL calibrated' 'n_TOF as is' --levels 'MM 15° + TOF' --mcs direct transplant -j $J --tag _pass5al_old ;;
5)  # the rest of the pass-4 grid, in separate tags so that steps 2-3 stay as they are
    L4=('trigger' 'MM 15° point, μ 3° + TOF 1 ns')
    LI_UG=587 TA_CFG=$AL TA_RUNS=$ALR $PY sim2arm/two_arm_nd.py reach --pairs horiz all --resps "${R[@]}" --levels "${L4[@]}" \
      --mcs direct -j $J --tag _pass5al${X}li11_more
    LI_UG=587 TA_CFG=$AL TA_RUNS=$ALR $PY sim2arm/two_arm_nd.py reach --pairs vert --resps "${R[@]}" --levels "${LV[@]}" \
      --mcs direct transplant -j $J --tag _pass5al${X}li11_vert ;;
6)  # what thin tables do to the two estimators: the Cu ogive on L11 alone and the Cu hemisphere on L10 alone (each the
    # size of the Al ogive's L12), to compare with passes 3 and 4 (L11 + L13, L10 + L18: x30).  11 µm, reference level.
    LI_UG=587 TA_CFG=ogCu200 TA_RUNS=L11 $PY sim2arm/two_arm_nd.py reach --pairs horiz all --resps "${R[@]}" \
      --levels 'MM 15° + TOF' --mcs direct transplant -j $J --tag _pass5al_thin_ogCu200li11
    LI_UG=587 TA_CFG=dome300 TA_RUNS=L10 $PY sim2arm/two_arm_nd.py reach --pairs horiz all --resps "${R[@]}" \
      --levels 'MM 15° + TOF' --mcs direct transplant -j $J --tag _pass5al_thin_dome300li11 ;;
esac; done
echo "run_r10 steps $STEPS done"
