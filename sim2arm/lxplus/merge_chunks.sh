#!/usr/bin/env bash
# merge_chunks.sh <eos sample dir> <out prefix> [chunk size] [ARM_PHI] [njobs]  (lnl_x17 two-arm study, 2026-11-19)
# lnl_merge_rot.py over FIXED job-number ranges: chunk c holds jobs [c*CS, (c+1)*CS), merged only when every part of
# the range has both parts_lnl and parts_time (jobs finish out of order). Skips chunks already merged. The last chunk
# may be short: njobs (default: from RUN_INFO.txt "N x ...") bounds it. Interactive lxplus; output via xrdcp.
set -e
D=$1; O=$2; CS=${3:-100}; PHI=${4:-0,0,0,0}
NJ=${5:-$(sed -n 2p $D/RUN_INFO.txt 2>/dev/null | awk '{print $1+0}')}
[ -n "$NJ" ] && [ "$NJ" -gt 0 ] || NJ=$(cat /afs/cern.ch/user/d/dneff/condor/lnl/*/$(basename $D)/jobs.txt 2>/dev/null | wc -l)
S=/afs/cern.ch/work/d/dneff/git/x17_lnl/analysis/l15
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
  ARM_PHI=$PHI python3 $S/lnl_merge_rot.py $(cat $T/chunk) -o $T/m.npz | tail -1
  xrdcp -s -f $T/m.npz $X/$out && rm -f $T/m.npz && echo "chunk $c (jobs $lo-$((hi - 1))) -> $out"
done
rm -rf $T
