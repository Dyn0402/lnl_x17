#!/usr/bin/env bash
# merge_chunks_r11.sh <eos sample dir> <out prefix> <chunk size> <njobs> <LS_LEG MeV>  (lnl_x17 R11, 2026-11-20)
# merge_chunks.sh with the R11 merge (r11/lnl_merge_rot.py: leg = SiPM AND (plastic OR E_ls >= LS_LEG)).
set -e
D=$1; O=$2; CS=$3; NJ=$4; LSL=$5
R=/afs/cern.ch/work/d/dneff/git/x17_lnl/analysis/r11
source /cvmfs/sft.cern.ch/lcg/views/LCG_106/x86_64-el9-gcc13-opt/setup.sh > /dev/null 2>&1
T=$(mktemp -d /tmp/dneff_mc.XXXX)
X=root://eosexperiment.cern.ch
xrdfs $X ls $D/parts_lnl | xargs -n1 basename | sort > $T/l
xrdfs $X ls $D/parts_time | xargs -n1 basename | sort > $T/t
comm -12 $T/l $T/t > $T/both
pfx=$(head -1 $T/both | sed 's/_job[0-9]*_t0.npz//')
nc=$(( (NJ + CS - 1) / CS ))
echo "$(wc -l < $T/both) of $NJ parts complete; $nc chunks of $CS"
for c in $(seq 0 $((nc - 1))); do
  out=${O}_c$(printf %03d $c)_sel.npz
  xrdfs $X stat $out > /dev/null 2>&1 && continue
  lo=$((c * CS)); hi=$(( (c + 1) * CS < NJ ? (c + 1) * CS : NJ ))
  : > $T/chunk; miss=0
  for j in $(seq $lo $((hi - 1))); do
    f=${pfx}_job$(printf %04d $j)_t0.npz
    if grep -qx "$f" $T/both; then echo "$D/parts_lnl/$f" >> $T/chunk; else miss=1; break; fi
  done
  [ $miss = 0 ] || continue
  LS_LEG=$LSL ARM_PHI=0,0,0,0 python3 $R/lnl_merge_rot.py $(cat $T/chunk) -o $T/m.npz | tail -1
  xrdcp -s -f $T/m.npz $X/$out && rm -f $T/m.npz && echo "chunk $c (jobs $lo-$((hi - 1))) -> $out"
done
rm -rf $T
