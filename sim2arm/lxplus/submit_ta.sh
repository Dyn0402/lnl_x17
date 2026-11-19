#!/usr/bin/env bash
# submit_ta.sh <run> <sample> <dphi> <njobs> <nevents> [flavour]  -- one sample of the two-arm rotated geometry
#   arms 0,1 (+-x) tilted up by alpha = (180 - dphi)/2 ("Lambda": bisector +z), arms 2,3 not built.
set -e
RUN=$1; SMP=$2; DPHI=$3; NJ=$4; NEV=$5; FL=${6:-workday}
S=/afs/cern.ch/work/d/dneff/git/x17_lnl/analysis/l15
EXE=/afs/cern.ch/work/d/dneff/git/x17_lnl/MX17_Full_Geant/bin/$(cat $S/TWOARM_BIN)
AL=$( [ "$DPHI" = "4arm" ] && echo x || python3 -c "print(f'{(180-$DPHI)/2:g}')")
GEOM="--arms 0,1 --arm-phi -$AL,$AL,0,0"
[ "$AL" = "0" ] && GEOM="--arms 0,1"
[ "$DPHI" = "4arm" ] && GEOM=""
LINE_OG="Al:19.05:30:-68:-63,SS:17.4:19.05:-620:-68,SS:31:57:-620:-585"
BASE="--target li --film Li2O:300 --backing Al:10 --holder Al:1 --chamber CFRP:0.4:25 --dump Ta:2 --spot-sigma 2"
CFG="--shape ogive --film Li:1068 --ogive Cu:200 --line $LINE_OG"
case $SMP in
  X17_m*) GEN="--energy 18.15 --mass ${SMP#X17_m} --ipc 0"; PFX=pairs ;;
  M1_*|E1_*) GEN="--energy ${SMP#*_} --ipc 1 --ipc-multipole ${SMP%%_*}"; PFX=pairs ;;
  gam_8Be) GEN="--gamma-lines 18.15:1,17.64:1,15.1:1,14.6:1"; PFX=gammas ;;
  cosmic) GEN="--cosmic"; PFX=cosmics ;;
  cosmicdisk) GEN="--cosmic-disk 900"; PFX=cosmics ;;
  *) echo "unknown $SMP"; exit 1 ;;
esac
NAME=${SMP}_ta${DPHI}
D=/eos/experiment/ntof/data/x17/lnl/$RUN/$NAME
L=/afs/cern.ch/user/d/dneff/condor/lnl/$RUN/$NAME
mkdir -p $L/logs
printf '%s\n%s\n' "$EXE" "$BASE $GEN $CFG $GEOM" > $L/args.txt
printf '%s\n%s x %s %s\nargs: %s\n' "$RUN/$NAME" "$NJ" "$NEV" "$PFX" "$(sed -n 2p $L/args.txt)" > $L/RUN_INFO.txt
python3 - "$NJ" "$NEV" "$D" "$RUN/$NAME" > $L/jobs.txt <<'PY'
import sys, random, zlib
nj, nev, d, nm = int(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4]
r = random.Random(zlib.crc32(nm.encode()))
for i in range(nj):
    print(f"job{i:04d} {r.randint(1, 2**31 - 1)} {nev} {d}")
PY
cat > $L/jobs.sub <<SUB
executable = $S/run_job.sh
arguments  = \$(tag) \$(seed) \$(nev) \$(dir) $PFX $L/args.txt
output     = $L/logs/\$(tag).out
error      = $L/logs/\$(tag).err
log        = $L/logs/condor.log
+JobFlavour = "$FL"
request_cpus = 1
request_memory = 6000
request_disk = 8000000
requirements = (OpSysAndVer =?= "AlmaLinux9")
should_transfer_files = NO
max_retries = 2
queue tag,seed,nev,dir from $L/jobs.txt
SUB
cd $L
condor_submit $L/jobs.sub | tail -1
