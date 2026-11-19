#!/usr/bin/env bash
# submit_l15.sh <sub-name> <first job> <njobs> <nevents per job>   (one log dir per submission)
set -e
NAME=$1; J0=$2; NJ=$3; NEV=$4
S=/afs/cern.ch/work/d/dneff/git/x17_lnl/analysis/l15
D=/eos/experiment/ntof/data/x17/lnl/L15/cosmic_ogCu200_asb
L=/afs/cern.ch/user/d/dneff/condor/lnl/L15/$NAME
mkdir -p $L/logs
python3 - "$J0" "$NJ" "$NEV" "$D" > $L/jobs.txt <<'PY'
import sys, random
j0, nj, nev, d = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4]
for i in range(j0, j0 + nj):
    r = random.Random(20261119 * 100003 + i)
    print(f"job{i:04d} {r.randint(1, 2**31 - 1)} {nev} {d}")
PY
cat > $L/jobs.sub <<SUB
executable = $S/run_l15.sh
arguments  = \$(tag) \$(seed) \$(nev) \$(dir)
output     = $L/logs/\$(tag).out
error      = $L/logs/\$(tag).err
log        = $L/logs/condor.log
+JobFlavour = "longlunch"
request_cpus = 1
request_memory = 6000
request_disk = 8000000
requirements = (OpSysAndVer =?= "AlmaLinux9")
should_transfer_files = NO
max_retries = 2
queue tag,seed,nev,dir from $L/jobs.txt
SUB
cd $L
condor_submit $L/jobs.sub
