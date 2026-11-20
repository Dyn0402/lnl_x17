#!/usr/bin/env bash
# submit_traj.sh <sample> <arms> <njobs> <nevents>   -- event-display trajectories, two-arm geometry (run L17)
#   sample: M1_17.64 | E1_18.15 | M1_18.15 | X17_m16.8 | gam_8Be | cosmicdisk ;  arms: 0,1 (horizontal) or 2,3 (vertical)
# lnl_x17 predictions tab, 2026-11-20.  TGT=dome300 (default; the BUILT Cu hemisphere R 11 mm, 300 µm, rim, grey flange,
# as run L18) -> run L17d; TGT=ogCu200 (the Cu ogive of the 19 Nov study, not built) -> run L17.
set -e
SMP=$1; ARMS=$2; NJ=$3; NEV=$4; FL=${5:-microcentury}
S=/afs/cern.ch/work/d/dneff/git/x17_lnl/analysis/l15
EXE=/afs/cern.ch/work/d/dneff/git/x17_lnl/MX17_Full_Geant/bin/mx17_full_sim_twoarm_10229eb
LINE_OG="Al:19.05:30:-68:-63,SS:17.4:19.05:-620:-68,SS:31:57:-620:-585"
BASE="--target li --film Li2O:300 --backing Al:10 --holder Al:1 --chamber CFRP:0.4:25 --dump Ta:2 --spot-sigma 2"
LINE_CUP="PVC:15:33:-27:-16,PVC:21:24:-165:-27,Al:20.5:40:-185:-165,SS:17.4:19.05:-620:-185,SS:31:57:-620:-585"
TGT=${TGT:-dome300}
case $TGT in
  dome300) CFG="--shape dome --film Li:1068 --dome Cu:11:300 --dome-rim 4:5 --line $LINE_CUP"; RUN=L17d ;;
  ogCu200) CFG="--shape ogive --film Li:1068 --ogive Cu:200 --line $LINE_OG"; RUN=L17 ;;
  *) echo "unknown TGT $TGT"; exit 1 ;;
esac
case $SMP in
  X17_m*) GEN="--energy 18.15 --mass ${SMP#X17_m} --ipc 0"; MODE=pair ;;
  M1_*|E1_*) GEN="--energy ${SMP#*_} --ipc 1 --ipc-multipole ${SMP%%_*}"; MODE=pair ;;
  gam_8Be) GEN="--gamma-lines 18.15:1,17.64:1"; MODE=gam ;;
  cosmicdisk) GEN="--cosmic-disk 900"; MODE=cosmic ;;
  *) echo "unknown $SMP"; exit 1 ;;
esac
NAME=${SMP}_a${ARMS/,/}
D=/eos/experiment/ntof/data/x17/lnl/$RUN/$NAME
L=/afs/cern.ch/user/d/dneff/condor/lnl/$RUN/$NAME
mkdir -p $L/logs
printf '%s\n%s\n' "$EXE" "$BASE $GEN $CFG --arms $ARMS" > $L/args.txt
python3 - "$NJ" "$NEV" "$D" "$RUN/$NAME" > $L/jobs.txt <<'PY'
import sys, random, zlib
nj, nev, d, nm = int(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4]
r = random.Random(zlib.crc32(nm.encode()))
for i in range(nj):
    print(f"job{i:03d} {r.randint(1, 2**31 - 1)} {nev} {d}")
PY
cat > $L/jobs.sub <<SUB
executable = $S/run_traj.sh
arguments  = \$(tag) \$(seed) \$(nev) \$(dir) $MODE $ARMS $L/args.txt
output     = $L/logs/\$(tag).out
error      = $L/logs/\$(tag).err
log        = $L/logs/condor.log
+JobFlavour = "$FL"
request_cpus = 1
request_memory = 4000
request_disk = 8000000
requirements = (OpSysAndVer =?= "AlmaLinux9")
should_transfer_files = NO
max_retries = 1
queue tag,seed,nev,dir from $L/jobs.txt
SUB
cd $L
condor_submit $L/jobs.sub | tail -1
