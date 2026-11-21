#!/usr/bin/env bash
# merge_loop_r11b.sh: as merge_loop_r11.sh for run R11b (x3-4 more beam MC of the R11 layout, 21 Nov), into the same
# sel_r11/ with the R11b_ prefix; combine_r11.py adds them to the R11 tables.  Every 15 min, up to 24 h.
#   setsid nohup bash merge_loop_r11b.sh > merge_loop_r11b.log 2>&1 < /dev/null &
E=/eos/experiment/ntof/data/x17/lnl
S=/afs/cern.ch/work/d/dneff/git/x17_lnl/analysis/l15
X=root://eosexperiment.cern.ch
O=$E/target/sel_r11
LSL=1.7
mkdir -p $O
declare -A CS=([M1_18.15]=25 [E1_18.15]=25 [M1_15.1]=25 [E1_15.1]=25 [gam_8Be]=25)
declare -A NJ=([M1_18.15]=200 [E1_18.15]=200 [M1_15.1]=150 [E1_15.1]=150 [gam_8Be]=200)
want=0; for s in "${!CS[@]}"; do want=$((want + (NJ[$s] + CS[$s] - 1) / CS[$s])); done
for i in $(seq 1 96); do
  echo "$(date) pass $i"
  for s in "${!CS[@]}"; do
    bash $S/merge_chunks_r11.sh $E/R11b/${s}_dome300_lsf16 $O/R11b_${s}_dome300_lsf16 ${CS[$s]} ${NJ[$s]} $LSL 2>&1 | grep "complete\|chunk\|rror"
  done
  n=$(xrdfs $X ls $O 2>/dev/null | grep -c "R11b_.*_c[0-9]*_sel.npz")
  echo "$n of $want chunks"
  [ "$n" -ge "$want" ] && { echo "all merged"; break; }
  sleep 900
done
