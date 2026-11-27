#!/usr/bin/env bash
# submit_l20.sh <run> <sample> <njobs> <nevents per sub-run> [nsub] [flavour]   (lnl_x17, 2026-11-27)
# Run L20: same-arm pairs at 441 keV (sim2arm/SAME_ARM.md).  Geometry, generator and binary of L19 (07bea64, the built
# Cu hemisphere dome300, 4 arms as built, analog); every arm track kept by twotrack_reduce.py.  Samples:
#   M1_17.64   the M1 internal pairs of the 441 keV resonance (signal-like, known)
#   gam_441    the 441 keV γ rays, 17.64 : 14.6 MeV = 1 : 0.45 (Γγ0 15.0 eV, Γγ1 6.7 eV, x17_facility_search lnl_rates.py)
#   bash submit_l20.sh L20t M1_17.64 2 5000; bash submit_l20.sh L20t gam_441 2 200000 2        # test cluster
#   bash submit_l20.sh L20 M1_17.64 20 20000 5; bash submit_l20.sh L20 gam_441 40 500000 10   # production (pairs: 5 sub-runs of 2e4;
#   one sub-run of 1e5 pairs needed ~5 GB in the reduction and was held, cluster 4767947)
set -e
RUN=$1; SMP=$2; NJ=$3; NEV=$4; NSUB=${5:-1}; FL=${6:-longlunch}
S=/afs/cern.ch/work/d/dneff/git/x17_lnl/analysis/l15
EXE=/afs/cern.ch/work/d/dneff/git/x17_lnl/MX17_Full_Geant/bin/mx17_full_sim_twoarm_07bea64
LINE_CUP="PVC:15:33:-27:-16,PVC:21:24:-165:-27,Al:20.5:40:-185:-165,SS:17.4:19.05:-620:-185,SS:31:57:-620:-585"
BASE="--target li --film Li2O:300 --backing Al:10 --holder Al:1 --chamber CFRP:0.4:25 --dump Ta:2 --spot-sigma 2"
CFG="--shape dome --film Li:1068 --dome Cu:11:300 --dome-rim 4:5 --line $LINE_CUP"
case $SMP in
  M1_17.64) GEN="--energy 17.64 --ipc 1 --ipc-multipole M1"; PFX=pairs ;;
  gam_441) GEN="--gamma-lines 17.64:1,14.6:0.45"; PFX=gammas ;;
  *) echo "unknown $SMP"; exit 1 ;;
esac
NAME=${SMP}_dome300_asb
D=/eos/experiment/ntof/data/x17/lnl/$RUN/$NAME
L=/afs/cern.ch/user/d/dneff/condor/lnl/$RUN/$NAME
mkdir -p $L/logs
printf '%s\n%s\n' "$EXE" "$BASE $GEN $CFG" > $L/args.txt
printf '%s\n%s x %s x %s %s\nargs: %s\n' "$RUN/$NAME" "$NJ" "$NSUB" "$NEV" "$PFX" "$(sed -n 2p $L/args.txt)" > $L/RUN_INFO.txt
mkdir -p $D && cp $L/RUN_INFO.txt $D/RUN_INFO.txt
python3 - "$NJ" "$NEV" "$D" "$RUN/$NAME" > $L/jobs.txt <<'PY'
import sys, random, zlib
nj, nev, d, nm = int(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4]
r = random.Random(zlib.crc32(nm.encode()))
for i in range(nj):
    print(f"job{i:04d} {r.randint(1, 2**31 - 100)} {nev} {d}")
PY
cat > $L/jobs.sub <<SUB
executable = $S/run_job_2trk.sh
arguments  = \$(tag) \$(seed) \$(nev) \$(dir) $PFX $L/args.txt $NSUB
output     = $L/logs/\$(tag).out
error      = $L/logs/\$(tag).err
log        = $L/condor.log
+JobFlavour = "$FL"
request_cpus = 1
request_memory = 3000
requirements = (OpSysAndVer =?= "AlmaLinux9")
should_transfer_files = NO
max_retries = 1
queue tag,seed,nev,dir from $L/jobs.txt
SUB
cd $L
condor_submit $L/jobs.sub | tail -1
