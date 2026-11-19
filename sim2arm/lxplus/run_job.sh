#!/usr/bin/env bash
# run_job.sh <tag> <seed> <nevents> <eos sample dir> <prefix> <argfile> (lnl_x17 two-arm study, 2026-11-19)
# Geant4 in the scratch dir, then lnl_reduce + lnl_time there; parts to EOS with eosio (checksummed); ROOT deleted.
set -eo pipefail
TAG=$1; SEED=$2; NEV=$3; D=$4; PFX=$5; AF=$6
G=/afs/cern.ch/work/d/dneff/git/x17_lnl/MX17_Full_Geant
A=/afs/cern.ch/work/d/dneff/git/x17_lnl/analysis
EXE=$(sed -n 1p $AF)
ARGS=$(sed -n 2p $AF)
LCG=/cvmfs/sft.cern.ch/lcg/views/LCG_106/x86_64-el9-gcc13-opt/setup.sh
EOSIO=/afs/cern.ch/user/d/dneff/bin/eosio
cd "${_CONDOR_SCRATCH_DIR:-$PWD}"
echo "node $(hostname) tag $TAG seed $SEED n $NEV $(date)"
P=${PFX}_$TAG
( set +u; source $G/scripts/setup_lxplus.sh > /dev/null 2>&1
  $EXE -t 1 -n $NEV -o ./$P -s $SEED $ARGS > $P.log 2>&1 )
tail -3 $P.log
grep -q "Run Summary" $P.log || { echo "sim did not finish"; tail -30 $P.log; exit 1; }
mkdir -p parts_lnl parts_time
( set +u; source $LCG > /dev/null 2>&1
  python3 $A/lnl_reduce.py ${P}_t0.root -o parts_lnl/${P}_t0.npz
  python3 $A/lnl_time.py ${P}_t0.root -o parts_time/${P}_t0.npz )
rm -f ${P}_t0.root
$EOSIO out parts_lnl/${P}_t0.npz $D/parts_lnl/${P}_t0.npz
$EOSIO out parts_time/${P}_t0.npz $D/parts_time/${P}_t0.npz
$EOSIO out $P.log $D/logs/$P.log
echo "done $(date)"
