## 7. The run plan: hedge first, then five days of X17 data

### 7.1 The principle

Everything that makes the feasibility case (rates, calibration, backgrounds, the veto) is front-loaded and takes
three days at most; the X17 data fill the rest. If the apparatus misbehaves, the run is still a full feasibility study;
if it works, the last five days give a limit near the ATOMKI ratio. Nothing in the plan depends on a lucky signal.

### 7.2 Before the beam: the cosmic veto test, vertical pair (installation week, ≥ 3 nights)

Cosmics do not need the beam. With the arms **vertical** (top + bottom) and the full trigger running during the
installation and commissioning nights, the set-up records the worst case at full strength:

| what | rate (L15, per live day) | what it delivers |
|---|---|---|
| two-arm cosmic coincidences | ~1.6 × 10⁵ | the trigger and DREAM at their highest rate |
| … of which at 125–160° | ~9 × 10⁴ | the MEG II "140° peak", reproduced and measured |
| … in the E_sum window, no veto | ~1.3 × 10⁴ (liquid working) | the background the veto has to remove |
| after pointing (μ segments 3°) | ~260 | the pointing rejection, measured to a few % per night |
| after pointing + 0.3 ns TOF | ~1 | the full veto (needs σ_t ≤ 0.4 ns) |

Three measurements come out of these nights that the reach rests on and nobody has made:
- **σ_t, the arm-to-arm time of flight**: a vertical muon reaches the lower arm ~1.4 ns after the upper one; the width of
  that peak, corrected for light transit along the bar with the Micromegas hit position, is σ_t √2. With 10⁵ muons per
  night the statistics are irrelevant; the transit correction is the work. It decides between the "pointing + 0.3 ns TOF"
  and "pointing only" rows of §3.
- **The muon segment resolution**: one straight muon gives two Micromegas segments; their angle difference measures it
  directly (the bench gave ~1° per chamber; the analysis assumes 3°).
- **Each arm's gain** from the minimum-ionising peak, per hour.

Then **roll the stand 90° to the horizontal pair** for the beam (§3: equal reach if the veto works, ~10× fewer cosmics
in the window if it does not). The stand needs to roll about the beam axis (the mechanics brainstorm's split end rings).
If it cannot, choose the horizontal pair and do the veto test on the cosmic bench at home with the same two arms
stacked vertically.

### 7.3 The eight beam days

| day | E_p | what | the number it delivers |
|---|---|---|---|
| 1 | 1.10 MeV | target conditioning; current scan 0.05 → 1 µA; γ-yield reference | singles and two-arm rates vs current, DREAM live time, MM occupancy; accidentals (≲ 0.02/day in the window at 2τ = 20 ns) |
| 2 | 0.441 MeV | locate the 441 keV resonance on the arm singles; 17.64 MeV M1 IPC | ~600 pairs/day above 90° in the E_sum window (~3,000 with no E_sum cut): the absolute IPC rate, the θ shape and the E_sum peak against Geant4 to ~5 % |
| 3–7 | 1.10 MeV | the 18.15 MeV region; 30 min yield check each day | the X17 data (§3): expected limit 0.7–1.1 × R(ATOMKI) with the liquid cells |
| 8 | 1.10 MeV | ½ day with the arms adjacent (90°), then contingency | external conversions and small-angle IPC at 25–90°, several × 10³/day (§6) |
| beam off | — | cosmics in the physics geometry (horizontal) | the beam-off background template in the geometry of the data |

One energy change per day, as AN2000's self-service running prefers. The one reconfiguration during beam time (adjacent,
day 8) is optional and comes last.

### 7.4 Decision points during the run

- **After day 1:** if the two-arm rate or the DREAM live time is far from the simulation (factor 2), stay at low current
  and debug; the run becomes a commissioning run and day 2 moves.
- **After day 2:** compare the 441 keV pair rate and θ shape with Geant4. Agreement within ~10–20 % means the
  acceptance model holds and the 1.10 MeV data mean something; a larger mismatch is itself the result to report, and
  days 3–7 are used to map it (angle bins, E_sum slices, current).
- **During days 3–7:** the daily γ-yield check guards against the LiOH conversion; if the yield falls by > 30 %, change
  the film (a spare is in the plan).

### 7.5 Hardware hedges that buy the most

1. **Bring the two liquid cells.** Without them the days to 3σ go up ×2–4 (§3). Even as they ran at n_TOF they are
   better than none. (Task S5, PMTs S1.)
2. **Measure σ_t before the run** (task R4, cosmic bench): the 0.3 ns TOF is the reference level's assumption.
3. **A γ-yield monitor** (a LaBr₃ or NaI from the LNL pool, ask): the target's daily health and the γ₀ normalisation
   cross-check, independent of the arms.
4. **A stand that rolls 90° about the beam** (vertical for the cosmic test, horizontal for the beam).
5. **10–12 µm Li** against the LiOH conversion (`x17_facility_search/lnl/target/TARGET_REVIEW.md`), with a spare film.

### 7.6 What the run gives the funding proposals

- The apparatus on a proton beam: rates, live time, occupancy, measured against Geant4.
- The 17.64 MeV IPC (no anomaly expected): the measured opening-angle distribution against Geant4.
- The cosmic background in the X17 window with each veto, in the worst geometry: the answer to the MEG II critique.
- A first X17 limit at 18.15 MeV, expected at or below the ATOMKI ratio with the liquid cells (and below MEG II's).
