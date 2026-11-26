#!/bin/bash
# run_local.sh [workers] -- every table of mixtures.py that is not yet in gas/out/tables (desktop, ~24 min each at ncoll 5).
cd "$(dirname "$0")"
source ~/PycharmProjects/nTof_x17/garfield_sim/setup_garfield.sh >/dev/null
LOG=${LOGDIR:-$PWD/../out/logs}; mkdir -p "$LOG"
python3 -c "
import os,mixtures,json
for k in mixtures.compositions():
    f='../out/tables/'+k+'.json'
    if not (os.path.exists(f) and json.load(open(f))['ncoll']>=mixtures.NCOLL): print(k)
" | xargs -P "${1:-14}" -I{} sh -c 'nice -n 10 python3 -u drift_one.py {} > '"$LOG"'/{}.log 2>&1; echo "{} exit $?"'
