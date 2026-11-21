set -e
cd /home/dylan/PycharmProjects/lnl_x17
export WORK_DATA=/media/ucla/work TA_LAYOUT=lsf16
PY=$HOME/PycharmProjects/nTof_x17/.venv/bin/python
R=('LNL calibrated' 'n_TOF as is')
LI_UG=587 $PY sim2arm/two_arm_nd.py reach --pairs horiz vert --resps "${R[@]}" --levels 'MM 15° + TOF' --mcs direct transplant -j 6 --tag _r11li11
$PY sim2arm/two_arm_nd.py reach --pairs horiz vert --resps "${R[@]}" --levels 'MM 15° + TOF' --mcs direct transplant -j 6 --tag _r11
echo R11 done
