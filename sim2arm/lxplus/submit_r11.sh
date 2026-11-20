#!/usr/bin/env bash
# submit_r11.sh <run> <sample> <njobs> <nevents> [flavour]   (lnl_x17 R11, 2026-11-20)
# R11: the built Cu hemisphere (dome300, as L18) with the liquid cell moved RIGHT BEHIND THE SiPM WALL
# (--ls-front 1.6: flat slab front 1.6 cm behind the SiPM container back, all arms; the n_TOF can, 45 x 45 x 2.1 cm,
# 6.5 L, faces bulged 1.25 cm; the plastics stay where they are, 6.1-6.5 cm behind the SiPM wall). Four arms, so every
# pair can be cut. The leg (SiPM AND (plastic OR liquid)) is formed at merge time (r11/lnl_merge.py --ls-leg).
#   bash submit_r11.sh R11t X17_m16.8 2 2000          # smoke test
#   for s in M1_18.15 E1_18.15; do bash submit_r11.sh R11 $s 100 100000; done
#   for s in M1_15.1 E1_15.1; do bash submit_r11.sh R11 $s 50 100000; done
#   bash submit_r11.sh R11 gam_8Be 100 2000000; bash submit_r11.sh R11 X17_m16.8 30 100000
#   bash submit_r11.sh R11 cosmicdisk 400 300000
set -e
RUN=$1; SMP=$2; NJ=$3; NEV=$4; FL=${5:-longlunch}
S=/afs/cern.ch/work/d/dneff/git/x17_lnl/analysis/l15
EXE=/afs/cern.ch/work/d/dneff/git/x17_lnl/MX17_Full_Geant/bin/mx17_full_sim_twoarm_5e526a8
LINE_CUP="PVC:15:33:-27:-16,PVC:21:24:-165:-27,Al:20.5:40:-185:-165,SS:17.4:19.05:-620:-185,SS:31:57:-620:-585"
BASE="--target li --film Li2O:300 --backing Al:10 --holder Al:1 --chamber CFRP:0.4:25 --dump Ta:2 --spot-sigma 2"
CFG="--shape dome --film Li:1068 --dome Cu:11:300 --dome-rim 4:5 --line $LINE_CUP --ls-front 1.6"
case $SMP in
  X17_m*) GEN="--energy 18.15 --mass ${SMP#X17_m} --ipc 0"; PFX=pairs ;;
  M1_*|E1_*) GEN="--energy ${SMP#*_} --ipc 1 --ipc-multipole ${SMP%%_*}"; PFX=pairs ;;
  gam_8Be) GEN="--gamma-lines 18.15:1,17.64:1,15.1:1,14.6:1"; PFX=gammas ;;
  cosmicdisk) GEN="--cosmic-disk 900"; PFX=cosmics ;;
  *) echo "unknown $SMP"; exit 1 ;;
esac
NAME=${SMP}_dome300_lsf16
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
    print(f"job{i:04d} {r.randint(1, 2**31 - 1)} {nev} {d}")
PY
cat > $L/jobs.sub <<SUB
executable = $S/run_job_r11.sh
arguments  = \$(tag) \$(seed) \$(nev) \$(dir) $PFX $L/args.txt
output     = $L/logs/\$(tag).out
error      = $L/logs/\$(tag).err
log        = $L/logs/condor.log
+JobFlavour = "$FL"
request_cpus = 1
request_memory = 4000
request_disk = 8000000
requirements = (OpSysAndVer =?= "AlmaLinux9")
should_transfer_files = NO
max_retries = 2
queue tag,seed,nev,dir from $L/jobs.txt
SUB
cd $L
condor_submit $L/jobs.sub | tail -1
