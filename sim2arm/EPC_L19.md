# External conversions at 100 times the statistics (run L19)

Written 2026-11-26. The selected external-conversion pairs of the two-arm study rested on 2 simulated events at 441 keV
and 4 at 1.10 MeV (run L18, 3 × 10⁸ ⁸Be γ rays). This note describes a new simulation with 100 times more γ rays, what
it shows about where these pairs come from, and what it changes for the slot-1 run (task R12).

## 0. Result in short

1. **The new run (L19) simulates 3.0 × 10¹⁰ ⁸Be γ rays in the built Cu hemisphere, 100 times L18, with the same
   geometry and generator.** L19 agrees with L18 at every selection step within the statistics of L18 (§3).
2. **The external conversions in the selected window now rest on 352 simulated events instead of 2.** At 1.10 MeV
   there are 21.3 ± 1.1 selected pairs per day (horizontal pair, liquid working, 11 µm, 1 µA). L18 gave 17, so the old
   estimate was close.
3. **At 441 keV the old estimate was wrong.** There are 74 selected external-conversion pairs per day, against 1.4 from
   L18. At 441 keV only the 17.64 MeV line is emitted, and none of the two L18 events came from that line. Therefore
   about a third of the beam pairs of the calibration day are external conversions, not M1 pairs.
4. **The external conversions look like the signal in opening angle.** Their selected spectrum peaks at 140–160°, where
   the X17 pairs are. With a well-sampled shape, the fit needs 195 days to 3σ instead of 151 (liquid working). For the
   46 hours at 1.10 MeV, the expected limit becomes **4.3 × R(ATOMKI)** instead of 3.8 × (as at n_TOF: 5.5 × instead
   of 5.0 ×; without liquid: 7.2 × instead of 7.0 ×). With 24-hour days (5 days of beam) it becomes 2.66 × instead of
   2.35 ×.
5. **The pairs start in the dome.** Of the selected-window pairs, 77 % come from a γ ray that converted in the Cu
   hemisphere wall and 10 % in its rim. In the 90° pair of day 8, 92 % come from the dome. Therefore day 8 measures
   exactly the material that makes this background in the opposite pair. Day 8 now rests on 24,000 simulated events
   and its prediction (~1,350 conversion pairs per day at 25–90°) is unchanged.

## 1. Why the old estimate was so thin

A ⁸Be γ ray that converts in the 300 µm Cu wall makes a pair that goes forward, along the γ ray. Such a pair reaches
two opposite arms only after a large scattering, so the opposite pair sees few of them. In L18, 169 events out of
3 × 10⁸ γ rays had a pair in the two horizontal arms at 125–160°. However, most of these pairs have an energy sum of
4–10 MeV, because one of the two particles carries little energy. Only 2 of the 169 reached the 13–19 MeV window.

## 2. The run

- Geant4: MX17_Full_Geant branch `lnl_twoarm`, commit 07bea64 = the L18 binary (10229eb) plus two changes that do not
  touch the geometry. The first change fills the primary γ ray's first interaction (volume, process, position) in the
  event tree. The second adds `--gamma-kill-escape`, which was tested and **not used**: killing γ rays that leave the
  target region without interacting saves only × 1.5 in CPU, because those γ rays are already cheap.
- Generator and geometry as L18 (`sim2arm/lxplus/submit_l18.sh gam_8Be`): four lines 18.15, 17.64, 15.1, 14.6 MeV with
  equal weights, isotropic, from the beam spot; the built hemisphere (R 11 mm, 300 µm, rim) on the grey flange and the
  beam line; four arms as built. The run is analog, with no biasing.
- Jobs (`sim2arm/lxplus/submit_l19.sh`, `run_job_epc.sh`): 6,000 jobs of 10 sub-runs of 5 × 10⁵ γ rays. The reduction
  reads the whole ROOT file, so a sub-run of more than ~10⁶ γ rays needs more than 3 GB (a first test with 4 × 10⁶ per
  job was held at 6 GB). Each job writes one table of its pairs (rows with two good arms, no singles) to
  `/eos/experiment/ntof/data/x17/lnl/L19/gam_8Be_dome300_asb/sel/`, and the first 200 jobs also keep their full parts.
- Condor: test cluster 4761540 (12 jobs, all clean), campaign cluster 4762099: 6,000 starts, 6,000 terminations, all
  with exit code 0, no holds, no retries. CPU efficiency 97 %, peak memory 2.3 GB (median 1.5 GB), median run time
  46 min (maximum 86 min), about 4,800 core-hours.
- Merged table: `$WORK_DATA/x17_facility_search/sel_l19/L19_gam_8Be_dome300_asb_sel.npz` (`sim2arm/combine_l19.py`),
  1.93 × 10⁶ rows.

## 3. L19 against L18

Table: two-arm pairs per 10⁹ γ rays (all four lines) at each step, before the detector response
(`out/epc_l19/steps.csv`; `sim2arm/epc_l19.py`). The raw energy sum is the deposited energy of the two arms.

| pair | step | L18 (MC events) | L19 (MC events) |
|---|---|---|---|
| horizontal | both arms | 787 (236) | 805 (24,151) |
| horizontal | 125–160° | 563 (169) | 556 (16,682) |
| horizontal | 125–160°, raw E_sum > 10 MeV | 97 (29) | 119 (3,580) |
| horizontal | 125–160°, raw E_sum 13–19 MeV | 6.7 (2) | 8.1 (243) |
| vertical | 125–160°, raw E_sum 13–19 MeV | 3.3 (1) | 8.9 (268) |
| 90° (adjacent) | 25–90° | 13,180 (3,954) | 13,277 (398,318) |

Every row agrees within 2σ of the L18 statistics. Figure `out/epc_l19/esum.png` shows the raw energy sum of the opposite
pairs at 125–160° in both runs.

## 4. Where the pairs come from

The primary γ ray's first interaction (`out/epc_l19/volumes.csv`):

| sample | Cu dome | Cu rim | beam-line tube | elsewhere (arms, air) |
|---|---|---|---|---|
| all γ rays that interact anywhere (9.5 %) | 23 % | 11 % | 11 % | 55 % |
| horizontal pair, 125–160° | 87 % | 10 % | 1.5 % | 1 % |
| horizontal pair, 125–160°, raw E_sum 13–19 MeV | 77 % | | | ~15 % (scintillators, PCBs) |
| 90° pair, 25–90° | 92 % | 6 % | 1.5 % | < 1 % |

98 % of the opposite-pair events begin with a pair conversion (`conv`), the rest with a Compton scattering. In the raw
energy window about 15 % of the events start in the arms' own scintillators or readout boards. The pointing cut removes
most of those, since their tracks do not point to the target.

## 5. What changes in the fit and the predictions

The fit is the reference two-arm fit (`two_arm_nd.py`, horizontal pair, MM 15° pointing + 0.6 ns TOF, 11 µm, 1 µA) with
the L19 table added to the external-conversion pair component (`TA_EPC_RUN=L19`; `sim2arm/run_l19.sh`, tags
`_pass4li11_l19`). The singles keep L18's table, and the two-arm fit does not use them.

**Selected pairs per day, horizontal pair, liquid working** (θ > 90°, E_sum window, pointing + TOF; in brackets, the
number of simulated events)

| per day | 441 keV, L18 | 441 keV, L19 | 1.10 MeV, L18 | 1.10 MeV, L19 |
|---|---|---|---|---|
| M1 IPC | 133 | 133 | 8 | 8 |
| E1 IPC | 5 | 5 | 42 | 42 |
| external conversions | **1.4 (2)** | **74 (352)** | **17 (2)** | **21.3 (352)** |
| cosmic rays | 68 | 68 | 68 | 68 |
| X17 at R(ATOMKI) | 0.2 | 0.2 | 2.7 | 2.7 |

Figure: `out/epc_l19/` and the spectra table `out/two_arm_spectra_pass4li11_l19.csv` (5° bins). In the external
conversions at 1.10 MeV, 72 % of the selected pairs lie at 130–160°.

**Days to 3σ at R(ATOMKI) and expected limits** (horizontal pair, 11 µm, 1 µA)

| response | L18 direct / transplant / central | L19 direct / transplant / central | R₉₀ 46 h, L18 → L19 | R₉₀ 5 d, L18 → L19 |
|---|---|---|---|---|
| liquid working | 189 / 120 / 151 | 241 / 158 / **195** | 3.8 → **4.3 ×** | 2.35 → **2.66 ×** |
| liquid as at n_TOF | 321 / 215 / 263 | 371 / 276 / **320** | 5.0 → **5.5 ×** | 3.1 → **3.4 ×** |
| no liquid | 494 / 529 / 511 | 555 / 547 / **551** | 7.0 → **7.2 ×** | 4.3 → **4.5 ×** |

The external conversions in the fit region grow from 252 to 308 per day, and their MC events from 49 to 4,870. The two
estimators now differ by × 1.5, as for the other components.

## 6. Consequences for the run plan

1. **The 441 keV day measures M1 and external conversions together.** In 8 hours it gives about 44 M1 pairs, 25
   external-conversion pairs, 2 E1 pairs and 23 cosmic pairs. The beam pair rate is then measured to about 14 % (was
   18 %), but a third of it is external conversion. Since the external conversions are tied to the M1 normalisation in
   the fit, this is a direct test of the holder's material model at the 17.64 MeV line.
2. **Day 8 (arms at 90°) is worth keeping.** It measures the same dome conversions at ~60 times the opposite-pair rate.
   The external conversions are now the second-largest beam background at 1.10 MeV and have a signal-like shape, so
   knowing their rate to a few per cent matters more than before.
3. **The 46 h at 1.10 MeV contain about 80 E1, 41 external-conversion, 16 M1 and 3 γ₁ pairs** (140 beam pairs) and 130
   cosmic pairs. An X17 at R(ATOMKI) adds 5.
4. **The lighter Al holder (R10) was not rerun.** R10 found its external conversions to be a 2 % effect, on 2 simulated
   events. Because the shape here turned out signal-like, an L19-size run of that holder (~5,000 core-hours) would be
   the next check if the Al holder becomes the plan.

## 7. Proposal text (suggested, not applied: the proposal is being edited in another session and on Overleaf)

1. §III (3), "external conversions ... (about 35, with a large uncertainty from the simulation statistics)" →
   "external conversions, which are γ rays that convert in the target holder (about 40)".
2. Fig. 2 caption: drop "The external conversions are drawn with their shape before the energy cut, since too few
   simulated ones pass it." and redraw Fig. 2 from `out/two_arm_spectra_pass4li11_l19.csv`.
3. The limits: 3.8 / 5.0 / 7.0 × → 4.3 / 5.5 / 7.2 × R(ATOMKI) for the 46 h (2.35 → 2.66 × for 5 days of beam),
   wherever they appear (abstract, Fig. 3, Table I, CN_BEAM.md §4).
4. The 441 keV day: "46 + 23 pairs in 8 h" → "about 70 beam pairs (a third of them external conversions) and 23
   cosmic pairs".
