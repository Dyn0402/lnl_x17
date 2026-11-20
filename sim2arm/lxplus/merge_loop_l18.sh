#!/usr/bin/env bash
# merge_loop_l18.sh: merge the L18 parts (the built Cu hemisphere, dome300) in fixed chunks as they arrive
# (merge_chunks.sh, interactive lxplus, xrdcp out); then the trigger-level γ scan for the Predictions tab.
# Every 15 min, up to 16 h; stops when every chunk exists.   (lnl_x17, 2026-11-20)
#   setsid nohup bash merge_loop_l18.sh > merge_loop_l18.log 2>&1 < /dev/null &
E=/eos/experiment/ntof/data/x17/lnl
S=/afs/cern.ch/work/d/dneff/git/x17_lnl/analysis/l15
X=root://eosexperiment.cern.ch
O=$E/target/sel_l18
mkdir -p $O /eos/user/d/dneff/x17/lnl_pred
declare -A CS=([M1_18.15]=30 [E1_18.15]=30 [M1_15.1]=30 [E1_15.1]=30 [gam_8Be]=50 [X17_m16.8]=30)
declare -A NJ=([M1_18.15]=150 [E1_18.15]=150 [M1_15.1]=150 [E1_15.1]=150 [gam_8Be]=150 [X17_m16.8]=30)
want=0; for s in "${!CS[@]}"; do want=$((want + (NJ[$s] + CS[$s] - 1) / CS[$s])); done
for i in $(seq 1 64); do
  echo "$(date) pass $i"
  for s in "${!CS[@]}"; do
    bash $S/merge_chunks.sh $E/L18/${s}_dome300_asb $O/L18_${s}_dome300_asb ${CS[$s]} 0,0,0,0 ${NJ[$s]} 2>&1 | grep "complete\|chunk\|rror"
  done
  G=/eos/user/d/dneff/x17/lnl_pred/pred_gam_L18.npz
  ng=$(xrdfs $X ls $E/L18/gam_8Be_dome300_asb/parts_lnl 2>/dev/null | wc -l)
  if [ "$ng" -ge 150 ] && [ ! -e $G ]; then
    ( source /cvmfs/sft.cern.ch/lcg/views/LCG_106/x86_64-el9-gcc13-opt/setup.sh > /dev/null 2>&1
      python3 $S/pred_cosmic_scan.py $E/L18/gam_8Be_dome300_asb --mode single -o $G | tail -1 )
  fi
  n=$(xrdfs $X ls $O 2>/dev/null | grep -c "_c[0-9]*_sel.npz")
  echo "$n of $want chunks"
  [ "$n" -ge "$want" ] && [ -e $G ] && { echo "all merged"; break; }
  sleep 900
done
