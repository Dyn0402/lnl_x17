#!/usr/bin/env bash
# redo_part.sh <eos root file> <eos sample dir>: reduce + time one finished sim file in scratch (eosio staging)
set -eo pipefail
F=$1; D=$2
A=/afs/cern.ch/work/d/dneff/git/x17_lnl/analysis
EOSIO=/afs/cern.ch/user/d/dneff/bin/eosio
cd "${_CONDOR_SCRATCH_DIR:-$PWD}"
s=$(basename $F .root)
$EOSIO in $F .
mkdir -p pl pt
( set +u; source /cvmfs/sft.cern.ch/lcg/views/LCG_106/x86_64-el9-gcc13-opt/setup.sh > /dev/null 2>&1
  python3 $A/lnl_reduce.py $s.root -o pl/$s.npz
  python3 $A/lnl_time.py $s.root -o pt/$s.npz )
rm -f $s.root
$EOSIO out pl/$s.npz $D/parts_lnl/$s.npz
$EOSIO out pt/$s.npz $D/parts_time/$s.npz
echo done
