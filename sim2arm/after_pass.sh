#!/usr/bin/env bash
# after_pass.sh <tag>: regenerate everything downstream of a two-arm pass (run_pass.sh <tag>): the study text, the
# planning reach rows, the proposal figure and PDF, the page.  Deploy and commit are left to a person/session.
set -x
T=${1:-_pass3}
cd "$(dirname "$0")/.."
PY=${PY:-$HOME/PycharmProjects/nTof_x17/.venv/bin/python}
$PY sim2arm/report_tables.py --tag $T > sim2arm/out/tables${T}.md
$PY sim2arm/build_study_md.py --tag $T
$PY planning/two_arm_estimates.py
$PY planning/figures.py
make -C proposal/latex && make -C proposal/latex zip
$PY sim2arm/make_two_arm_deck.py --tag $T
python3 site/build_page.py
echo "after_pass $T done"
