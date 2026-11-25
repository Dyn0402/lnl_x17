#!/usr/bin/env bash
# run_job_epc.sh <tag> <seed> <nevents per sub-run> <eos sample dir> <prefix> <argfile> [nsub=10]   (lnl_x17 L19, 2026-11-25)
# The ⁸Be γ lines at high statistics.  NSUB (default 3) Geant4 sub-runs of <nevents> each (seeds seed, seed+1, ...):
# the reduction reads the whole ROOT file, ~1.5 GB of memory per 1e6 γ, so each sub-run is reduced on its own.
# Per sub-run: lnl_reduce + lnl_time + lnl_first (the primary γ's first interaction).  Then one pair table per job
# (lnl_merge_rot over the sub-runs, DROP_SG: no singles) to $D/sel/; the full parts only for the first KEEP_PARTS jobs.
# Everything in the scratch dir, out with eosio (checksummed); ROOT deleted after each sub-run.
set -eo pipefail
TAG=$1; SEED=$2; NEV=$3; D=$4; PFX=$5; AF=$6; NSUB=${7:-10}
G=/afs/cern.ch/work/d/dneff/git/x17_lnl/MX17_Full_Geant
A=/afs/cern.ch/work/d/dneff/git/x17_lnl/analysis
S=$A/l15
EXE=$(sed -n 1p $AF)
ARGS=$(sed -n 2p $AF)
LCG=/cvmfs/sft.cern.ch/lcg/views/LCG_106/x86_64-el9-gcc13-opt/setup.sh
EOSIO=/afs/cern.ch/user/d/dneff/bin/eosio
cd "${_CONDOR_SCRATCH_DIR:-$PWD}"
echo "node $(hostname) tag $TAG seed $SEED n $NSUB x $NEV $(date)"
mkdir -p parts_lnl parts_time sel
for k in $(seq 0 $((NSUB - 1))); do
  P=${PFX}_${TAG}s$k
  ( set +u; source $G/scripts/setup_lxplus.sh > /dev/null 2>&1
    $EXE -t 1 -n $NEV -o ./$P -s $((SEED + k)) $ARGS > $P.log 2>&1 )
  grep -q "Run Summary" $P.log || { echo "sim $k did not finish"; tail -30 $P.log; exit 1; }
  echo "sub-run $k: $(ls -la ${P}_t0.root | awk '{print $5}') bytes $(date +%T)"
  ( set +u; source $LCG > /dev/null 2>&1
    python3 $A/lnl_reduce.py ${P}_t0.root -o parts_lnl/${P}_t0.npz
    python3 $A/lnl_time.py ${P}_t0.root -o parts_time/${P}_t0.npz
    python3 $S/lnl_first.py ${P}_t0.root parts_lnl/${P}_t0.npz | cut -c1-200 )
  rm -f ${P}_t0.root
done
( set +u; source $LCG > /dev/null 2>&1
  DROP_SG=1 python3 $S/lnl_merge_rot.py parts_lnl/*.npz -o sel/${PFX}_${TAG}_sel.npz | head -1 )
$EOSIO out sel/${PFX}_${TAG}_sel.npz $D/sel/${PFX}_${TAG}_sel.npz
n=$((10#${TAG#job}))
if [ $n -lt ${KEEP_PARTS:-200} ]; then
  for f in parts_lnl/*.npz; do
    $EOSIO out $f $D/parts_lnl/$(basename $f)
    $EOSIO out parts_time/$(basename $f) $D/parts_time/$(basename $f)
  done
fi
tar czf logs.tgz ${PFX}_${TAG}s*.log
$EOSIO out logs.tgz $D/logs/${PFX}_${TAG}.tgz
rm -rf parts_lnl parts_time sel ${PFX}_${TAG}s*.log logs.tgz
echo "done $(date)"
