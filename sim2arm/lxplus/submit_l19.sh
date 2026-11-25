#!/usr/bin/env bash
# submit_l19.sh <run> <njobs> <nevents> [flavour] [max_materialize] [cfg]   (lnl_x17, 2026-11-25)
# Run L19: the ⁸Be γ lines (external conversions, EPC) at high statistics.  The selected EPC pairs of the slot-1
# two-arm fit rested on 2 (441 keV) and 4 (1.10 MeV) MC events of L18 (3e8 γ).  Same geometry and generator as L18
# (submit_l18.sh gam_8Be), analog (no biasing), binary 07bea64 = 10229eb + the γ's first interaction in EventTree.
#   bash submit_l19.sh L19t3 12 500000 longlunch          # test cluster (10 sub-runs of 5e5 per job: 5e6 γ; the reduction needs ~2.2 GB per 5e5)
#   bash submit_l19.sh L19 6000 500000 longlunch 900      # x100 L18 (3.0e10 γ)
# DRY=1: write the submit file only (for condor_budget size --submit).
# cfg: dome300 (default, the built Cu hemisphere) or alog (the Al ogive + Cu liner of R10).
set -e
RUN=$1; NJ=$2; NEV=$3; FL=${4:-longlunch}; MM=${5:-1000}; CFGN=${6:-dome300}; NSUB=${NSUB:-10}
S=/afs/cern.ch/work/d/dneff/git/x17_lnl/analysis/l15
EXE=/afs/cern.ch/work/d/dneff/git/x17_lnl/MX17_Full_Geant/bin/mx17_full_sim_twoarm_07bea64
LINE_CUP="PVC:15:33:-27:-16,PVC:21:24:-165:-27,Al:20.5:40:-185:-165,SS:17.4:19.05:-620:-185,SS:31:57:-620:-585"
BASE="--target li --film Li2O:300 --backing Al:10 --holder Al:1 --chamber CFRP:0.4:25 --dump Ta:2 --spot-sigma 2"
case $CFGN in
  dome300) CFG="--shape dome --film Li:1068 --dome Cu:11:300 --dome-rim 4:5 --line $LINE_CUP" ;;
  *) echo "unknown cfg $CFGN"; exit 1 ;;
esac
GEN="--gamma-lines 18.15:1,17.64:1,15.1:1,14.6:1"; PFX=gammas
NAME=gam_8Be_${CFGN}_asb
D=/eos/experiment/ntof/data/x17/lnl/$RUN/$NAME
L=/afs/cern.ch/user/d/dneff/condor/lnl/$RUN/$NAME
mkdir -p $L/logs
printf '%s\n%s\n' "$EXE" "$BASE $GEN $CFG" > $L/args.txt
printf '%s\n%s x %s %s\nargs: %s\n' "$RUN/$NAME" "$NJ" "$NEV" "$PFX" "$(sed -n 2p $L/args.txt)" > $L/RUN_INFO.txt
mkdir -p $D && cp $L/RUN_INFO.txt $D/RUN_INFO.txt
python3 - "$NJ" "$NEV" "$D" "$RUN/$NAME" > $L/jobs.txt <<'PY'
import sys, random, zlib
nj, nev, d, nm = int(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4]
r = random.Random(zlib.crc32(nm.encode()))
for i in range(nj):
    print(f"job{i:04d} {r.randint(1, 2**31 - 100)} {nev} {d}")
PY
cat > $L/jobs.sub <<SUB
executable = $S/run_job_epc.sh
arguments  = \$(tag) \$(seed) \$(nev) \$(dir) $PFX $L/args.txt $NSUB
output     = $L/logs/\$(tag).out
error      = $L/logs/\$(tag).err
log        = $L/condor.log
+JobFlavour = "$FL"
request_cpus = 1
request_memory = 2700
requirements = (OpSysAndVer =?= "AlmaLinux9")
should_transfer_files = NO
max_retries = 2
max_materialize = $MM
queue tag,seed,nev,dir from $L/jobs.txt
SUB
cd $L
[ -n "$DRY" ] && { echo "DRY: $L/jobs.sub written"; exit 0; }
condor_submit $L/jobs.sub | tail -1
