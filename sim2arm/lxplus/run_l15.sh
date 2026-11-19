#!/usr/bin/env bash
# L15 job (lnl_x17 two-arm study, 2026-11-19): cosmic muons with the Cu hemisphere (ogCu200) geometry, as built.
# Sim, reduce and time in the scratch dir; parts copied to EOS with eosio (checksummed); the ROOT file is deleted.
#   run_l15.sh <tag> <seed> <nevents> <eos sample dir>
set -eo pipefail
TAG=$1; SEED=$2; NEV=$3; D=$4
G=/afs/cern.ch/work/d/dneff/git/x17_lnl/MX17_Full_Geant
A=/afs/cern.ch/work/d/dneff/git/x17_lnl/analysis
EXE=$G/bin/mx17_full_sim_culiner_812488b
LCG=/cvmfs/sft.cern.ch/lcg/views/LCG_106/x86_64-el9-gcc13-opt/setup.sh
EOSIO=/afs/cern.ch/user/d/dneff/bin/eosio
LINE_OG="Al:19.05:30:-68:-63,SS:17.4:19.05:-620:-68,SS:31:57:-620:-585"
cd "${_CONDOR_SCRATCH_DIR:-$PWD}"
echo "node $(hostname) tag $TAG seed $SEED n $NEV $(date)"
P=cosmics_$TAG
( set +u; source $G/scripts/setup_lxplus.sh > /dev/null 2>&1
  $EXE -t 1 -n $NEV -o ./$P -s $SEED --target li --film Li2O:300 --backing Al:10 --holder Al:1 \
      --chamber CFRP:0.4:25 --dump Ta:2 --spot-sigma 2 --cosmic \
      --shape ogive --film Li:1068 --ogive Cu:200 --line $LINE_OG > $P.log 2>&1 )
tail -3 $P.log
grep -q "Run Summary" $P.log || { echo "sim did not finish"; exit 1; }
ls -la ${P}_t0.root
mkdir -p parts_lnl parts_time
( set +u; source $LCG > /dev/null 2>&1
  python3 $A/lnl_reduce.py ${P}_t0.root -o parts_lnl/${P}_t0.npz
  python3 $A/lnl_time.py ${P}_t0.root -o parts_time/${P}_t0.npz )
rm -f ${P}_t0.root
$EOSIO out parts_lnl/${P}_t0.npz $D/parts_lnl/${P}_t0.npz
$EOSIO out parts_time/${P}_t0.npz $D/parts_time/${P}_t0.npz
$EOSIO out $P.log $D/logs/$P.log
echo "done $(date)"
