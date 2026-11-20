#!/usr/bin/env bash
# merge the L15 cosmic chunks as the parts arrive (lnl_x17 two-arm study, 2026-11-19); every 20 min, up to 8 h,
# stops once every chunk of the 1630 jobs is merged.   setsid nohup bash merge_loop.sh > merge_loop.log 2>&1 < /dev/null &
E=/eos/experiment/ntof/data/x17/lnl
S=/afs/cern.ch/work/d/dneff/git/x17_lnl/analysis/l15
for i in $(seq 1 24); do
  echo "$(date) pass $i"
  bash $S/merge_chunks.sh $E/L15/cosmicdisk_ta4arm $E/target/sel_l15/L15_cosmicdisk_ta4arm 100 0,0,0,0 1630 2>&1 | grep "complete\|chunk"
  n=$(xrdfs root://eosexperiment.cern.ch ls $E/target/sel_l15 | grep -c L15_cosmicdisk_ta4arm_c)
  [ "$n" -ge 17 ] && { echo "all 17 chunks merged"; break; }
  sleep 1200
done
