#!/usr/bin/env bash
# merge_loop_r11.sh: merge the R11 parts (dome300, liquid right behind the SiPM wall) in fixed chunks as they arrive,
# with leg = SiPM AND (plastic OR liquid >= 1.7 MeV) (merge_chunks_r11.sh, interactive lxplus, xrdcp out).
# Every 15 min, up to 16 h; stops when every chunk exists.   (lnl_x17, 2026-11-20)
#   setsid nohup bash merge_loop_r11.sh > merge_loop_r11.log 2>&1 < /dev/null &
E=/eos/experiment/ntof/data/x17/lnl
S=/afs/cern.ch/work/d/dneff/git/x17_lnl/analysis/l15
X=root://eosexperiment.cern.ch
O=$E/target/sel_r11
LSL=1.7
mkdir -p $O
declare -A CS=([M1_18.15]=25 [E1_18.15]=25 [M1_15.1]=25 [E1_15.1]=25 [gam_8Be]=25 [X17_m16.8]=30 [cosmicdisk]=50)
declare -A NJ=([M1_18.15]=100 [E1_18.15]=100 [M1_15.1]=50 [E1_15.1]=50 [gam_8Be]=100 [X17_m16.8]=30 [cosmicdisk]=400)
want=0; for s in "${!CS[@]}"; do want=$((want + (NJ[$s] + CS[$s] - 1) / CS[$s])); done
for i in $(seq 1 64); do
  echo "$(date) pass $i"
  for s in "${!CS[@]}"; do
    bash $S/merge_chunks_r11.sh $E/R11/${s}_dome300_lsf16 $O/R11_${s}_dome300_lsf16 ${CS[$s]} ${NJ[$s]} $LSL 2>&1 | grep "complete\|chunk\|rror"
  done
  n=$(xrdfs $X ls $O 2>/dev/null | grep -c "_c[0-9]*_sel.npz")
  echo "$n of $want chunks"
  [ "$n" -ge "$want" ] && { echo "all merged"; break; }
  sleep 900
done
