#!/usr/bin/env bash
# run_traj.sh <tag> <seed> <nevents> <eos dir> <mode> <arms> <argfile>   (lnl_x17 predictions tab, 2026-11-20)
# Geant4 with --trajdump in the scratch dir; lnl_reduce + lnl_time; traj_pick.py keeps the events worth drawing;
# the small outputs go to EOS with eosio (checksummed); the ROOT file and the full trajectory CSV are deleted.
set -eo pipefail
TAG=$1; SEED=$2; NEV=$3; D=$4; MODE=$5; ARMS=$6; AF=$7
G=/afs/cern.ch/work/d/dneff/git/x17_lnl/MX17_Full_Geant
A=/afs/cern.ch/work/d/dneff/git/x17_lnl/analysis
S=$A/l15
EXE=$(sed -n 1p $AF)
ARGS=$(sed -n 2p $AF)
LCG=/cvmfs/sft.cern.ch/lcg/views/LCG_106/x86_64-el9-gcc13-opt/setup.sh
EOSIO=/afs/cern.ch/user/d/dneff/bin/eosio
cd "${_CONDOR_SCRATCH_DIR:-$PWD}"
echo "node $(hostname) tag $TAG seed $SEED n $NEV mode $MODE arms $ARMS $(date)"
P=traj_$TAG
( set +u; source $G/scripts/setup_lxplus.sh > /dev/null 2>&1
  $EXE -t 1 -n $NEV -o ./$P -s $SEED $ARGS --trajdump $NEV > $P.log 2>&1 )
tail -3 $P.log
grep -q "Run Summary" $P.log || { echo "sim did not finish"; tail -30 $P.log; exit 1; }
( set +u; source $LCG > /dev/null 2>&1
  python3 $A/lnl_reduce.py ${P}_t0.root -o ${P}_part.npz
  python3 $A/lnl_time.py ${P}_t0.root -o ${P}_time.npz
  python3 $S/traj_pick.py ${P}_traj_t0.csv ${P}_part.npz ${P}_time.npz --mode $MODE --arms $ARMS -o $P )
rm -f ${P}_t0.root ${P}_traj_t0.csv ${P}_part.npz ${P}_time.npz
$EOSIO out ${P}_traj.csv.gz $D/${P}_traj.csv.gz
$EOSIO out ${P}_evt.npz $D/${P}_evt.npz
$EOSIO out $P.log $D/logs/$P.log
rm -f ${P}_traj.csv.gz ${P}_evt.npz
echo "done $(date)"
