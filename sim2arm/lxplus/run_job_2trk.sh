#!/usr/bin/env bash
# run_job_2trk.sh <tag> <seed> <nevents per sub-run> <eos sample dir> <prefix> <argfile> [nsub]   (lnl_x17 L20, 2026-11-27)
# Same-arm pair study (sim2arm/SAME_ARM.md).  NSUB Geant4 sub-runs (seeds seed, seed+1, ...), each reduced on its own
# in the scratch dir: lnl_reduce (legs, calorimetry, primary-lepton truth), twotrack_reduce (the 3 strongest tracks per
# arm), and for γ runs lnl_first (the γ's first interaction).  ROOT deleted after each sub-run; parts out with eosio.
set -eo pipefail
TAG=$1; SEED=$2; NEV=$3; D=$4; PFX=$5; AF=$6; NSUB=${7:-1}
G=/afs/cern.ch/work/d/dneff/git/x17_lnl/MX17_Full_Geant
A=/afs/cern.ch/work/d/dneff/git/x17_lnl/analysis
S=$A/l15
EXE=$(sed -n 1p $AF)
ARGS=$(sed -n 2p $AF)
LCG=/cvmfs/sft.cern.ch/lcg/views/LCG_106/x86_64-el9-gcc13-opt/setup.sh
EOSIO=/afs/cern.ch/user/d/dneff/bin/eosio
cd "${_CONDOR_SCRATCH_DIR:-$PWD}"
echo "node $(hostname) tag $TAG seed $SEED n $NSUB x $NEV $(date)"
mkdir -p parts_lnl parts_2trk
for k in $(seq 0 $((NSUB - 1))); do
  P=${PFX}_${TAG}s$k
  ( set +u; source $G/scripts/setup_lxplus.sh > /dev/null 2>&1
    $EXE -t 1 -n $NEV -o ./$P -s $((SEED + k)) $ARGS > $P.log 2>&1 )
  grep -q "Run Summary" $P.log || { echo "sim $k did not finish"; tail -30 $P.log; exit 1; }
  echo "sub-run $k: $(stat -c %s ${P}_t0.root) bytes $(date +%T)"
  ( set +u; source $LCG > /dev/null 2>&1
    python3 $A/lnl_reduce.py ${P}_t0.root -o parts_lnl/${P}_t0.npz
    [ "$PFX" = gammas ] && python3 $S/lnl_first.py ${P}_t0.root parts_lnl/${P}_t0.npz | cut -c1-200
    python3 $S/twotrack_reduce.py ${P}_t0.root -o parts_2trk/${P}_t0.npz --seed $((SEED + k)) )
  rm -f ${P}_t0.root
done
for f in parts_lnl/*.npz parts_2trk/*.npz; do
  $EOSIO out $f $D/$f
done
tar czf logs.tgz ${PFX}_${TAG}s*.log
$EOSIO out logs.tgz $D/logs/${PFX}_${TAG}.tgz
rm -rf parts_lnl parts_2trk ${PFX}_${TAG}s*.log logs.tgz
echo "done $(date)"
