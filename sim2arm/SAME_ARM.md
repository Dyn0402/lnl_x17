# Pairs with both leptons in one arm at 441 keV (run L20, 2026-11-27)

## 1. The question

The proposal's Acceptance paragraph says that pairs with both leptons in the same arm are useful, because the internal
pairs (IPC) are concentrated at small opening angles. Fig. 2(b) of the proposal shows about 1.6 × 10⁶ M1 internal pairs of
the 17.64 MeV transition reaching one arm in a beam day at 441 keV. That figure is geometry only: straight leptons, no copper,
no trigger, no reconstruction. The red to-do asked for a Geant4 selection of these pairs, with the holder and the trigger,
and for their background. This note gives both.

## 2. What we simulated

Run L20 uses the geometry, generator and binary of runs L18 and L19 (MX17_Full_Geant `lnl_twoarm` 07bea64): the built Cu
hemisphere (R 11 mm, 300 µm wall) with its Li film, four arms as built, no biasing. The beam days use the horizontal pair,
arms 0 and 1. There are two samples:

| sample | what | events | condor |
|---|---|---|---|
| `M1_17.64` | the M1 internal pairs of the 17.64 MeV transition | 2 × 10⁶ pairs | 20 jobs, cluster 4768191, all normal (the first cluster, 4767947, was held for memory: one sub-run of 10⁵ pairs needed ~5 GB in the reduction) |
| `gam_441` | the γ rays of the 441 keV resonance, 17.64 and 14.6 MeV in the ratio 1 : 0.45 | 2 × 10⁸ γ | 40 jobs, cluster 4767948, all normal, ≤ 2.3 GB, ≤ 1 h |

The reduction (`lxplus/twotrack_reduce.py`) keeps the three most energetic tracks in each arm's drift gap, each fitted on
its own. Geant4 tells which hits belong to which track, so the selection assumes perfect pattern recognition. The
normalisation is 5.4 × 10⁴ γ₀/s at 1 µA (11 µm film) and α(M1, 17.64 MeV) = 3.42 × 10⁻³, per beam day of 18 h.

The selection of a same-arm pair in arm 0 or 1 (`same_arm.py`):
1. a trigger in that arm (SiPM bar and plastic above 0.5 MIP);
2. at least two tracks with three or more hits in its drift gap (the two most energetic are used);
3. both tracks point to the beam spot (the opposite-arm reference cut: distance of closest approach below 135 mm after a 15°
   smear of the direction);
4. the two track centroids more than 1 cm apart.

The opening angle is the angle between the two centroids, as seen from the beam spot.

## 3. What we see

Figure `out/figures/same_arm_l20.png` shows the opening-angle distribution of the selected pairs in one beam day. The orange
line is the internal pairs. The stacked histogram is the background from the γ rays, split by where the γ ray first
interacted.

| step (per beam day) | internal pairs | γ background | of which conversions in the Cu hemisphere |
|---|---|---|---|
| truth: both leptons reach arm 0 or 1 | 8.4 × 10⁵ | | |
| trigger + 2 tracks | 3.0 × 10⁵ | 1.2 × 10⁷ | 5.5 × 10⁶ |
| + pointing (15°) | 2.2 × 10⁵ | 5.5 × 10⁶ | 4.1 × 10⁶ |
| **+ separation > 1 cm** | **2.1 × 10⁵** | **4.8 × 10⁶** | **4.0 × 10⁶** |
| + separation > 2 cm | 2.1 × 10⁵ | 4.4 × 10⁶ | 3.9 × 10⁶ |

(`out/same_arm_l20_cutflow.csv`; the Monte Carlo statistics are 36,000 selected internal pairs and 190,000 background pairs.)

This shows three things.

1. **The same-arm sample is dominated by γ rays that convert in the copper holder.** At the reference selection there are
   about 22 background pairs for each internal pair. In every 5° bin the internal pairs are between 1 % and 15 % of the
   sample (`out/same_arm_l20.csv`). The reason is simple. A 17.64 MeV γ ray converts in the 300 µm copper wall about 1.6 %
   of the time, while an internal pair is emitted in 0.34 % of the decays. A conversion pair is also narrow, so both
   leptons usually enter the same arm. The conversion pairs start in the hemisphere wall, a fraction of a millimetre from
   the Li film, and carry the same energy. Therefore no cut on pointing or energy separates them from the internal pairs.
2. **The copper smears the opening angle strongly.** An 8 MeV lepton scatters by about 12° in 300 µm of copper. The
   reconstructed opening angle of the selected internal pairs is typically 10° larger than the true one (the median), with
   a spread of about 19° (half the 16–84 % range).
3. **Two-track separation is not the limit in the simulation.** Requiring 1 cm or 2 cm between the track centroids removes
   only 0.4 % or 1.7 % of the internal pairs. The real limit is the pattern recognition in the TPC, which the simulation does not
   model. The same-arm tracks are only a few centimetres apart.

The arm calorimetry does not help either. One arm contains only 3–12 MeV of the pair's 16.6 MeV kinetic energy, so the
opposite-arm window of 13–19 MeV does not apply. Requiring more than 5 MeV in the arm keeps 80 % of the internal pairs and
82 % of the background.

## 4. What it means for the proposal

The same-arm pairs at 441 keV do **not** measure the opening-angle distribution of the internal pairs. Instead they measure,
with very large statistics (~5 × 10⁶ pairs per beam day), the γ conversions in the copper holder and the scattering of
the leptons in its wall. These are the inputs of the external-conversion background at 1.10 MeV, about 90 of the 320
selected beam pairs in the run (and task R14 asks how well Geant4 predicts them). The sample also tests the reconstruction
of two close tracks in one TPC.

Proposed wording for the Acceptance paragraph, replacing the sentence "The same-arm pairs are useful because IPC pairs are
concentrated at small angles", the Fig. 2(b) sentence and the red to-do:

> Pairs with both leptons in the same arm have opening angles below 90°. At 441 keV the Geant4 simulation predicts about
> $2\times10^5$ selected same-arm internal pairs per beam day. However, about 20 times more same-arm pairs come from γ rays
> that convert in the copper holder, and no cut separates them from the internal pairs. For this reason the same-arm pairs
> measure the external conversions in the holder and the scattering of the leptons in its wall, which shape the background
> at 1.10 MeV. They also test the reconstruction of two close tracks in one TPC (4 cm apart at θ = 10°).

## 5. Limits of this study

- The selection uses Geant4's track identities. A real TPC must separate two tracks a few centimetres apart; we have no
  measurement of how well it does.
- The background depends on the copper conversion probability and the lepton scattering in Geant4's EM physics. These are
  well known for copper, but the hemisphere's actual wall thickness is not measured (task R14 asks Pierfrancesco for it).
- The internal pairs of the γ₁ transition (14.6 MeV, 0.45 × the γ₀ rate) are not included. They add about 40 % more
  internal pairs at lower energy and do not change the conclusion.
- No accidental two-track events (two γ conversions in one drift window) are included.

## 6. Files

- `lxplus/submit_l20.sh`, `lxplus/run_job_2trk.sh`, `lxplus/twotrack_reduce.py`, `lxplus/merge_l20.py`: the condor jobs and
  the reduction (copies of lxplus `/afs/cern.ch/work/d/dneff/git/x17_lnl/analysis/l15/`).
- Data: `/eos/experiment/ntof/data/x17/lnl/L20/` (parts), merged tables `/eos/user/d/dneff/x17/l20/{M1_17.64,gam_441}.npz`
  (desktop copy `$WORK_DATA/lnl_x17/l20/`).
- `same_arm.py` → `out/same_arm_l20.csv`, `out/same_arm_l20_cutflow.csv`, `out/figures/same_arm_l20.png`.
