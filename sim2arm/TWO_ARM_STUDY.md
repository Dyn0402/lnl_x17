# The two-arm LNL run, simulated: what 8 days can show, and how to spend them

Written 2026-11-19 (overnight study). Set-up: the slot-1 feasibility run of `../slot1_feasibility/PLAN.md`: two Micromegas
(A, B), two SiPM walls, four small 20 × 30 × 2 cm plastics, optionally two liquid cells, the Cu hemisphere target holder
(the "Cu ogive" of the simulation; Geant4 with 20 µm Li, yields also for the recommended 10–12 µm), AN2000 at 1 µA.
Slide note: <https://dylan-neff.web.cern.ch/notes/lnl-two-arm-run.html>. This replaces the ×2 scaling of
`../planning/two_arm_estimates.py` (task R1).

## 0. Bottom line (2026-11-19, Geant4)

- **Do go for a measurement, as the second half of the run, and do not promise one.** Five days at 1.10 MeV with two
  opposite arms give an expected 90 % CL limit of **0.93 × R(ATOMKI)** with the liquid cells working,
  **1.19 ×** with the liquid as it ran at n_TOF and **1.78 ×** without it (11 µm Li,
  horizontal pair, MM pointing + 0.3 ns TOF). MEG II's published limit is 2.07 × R(ATOMKI): every case beats it on
  statistics, the two with liquid cells reach the ATOMKI ratio or near it.
- **We would not see ATOMKI's signal at 3σ.** If it is there, the expected significance is 1.1–1.4σ
  (liquid as at n_TOF … working): a 3σ excess with probability 3–5 %, a 2σ hint
  with 18–27 %. Days to 3σ: 24 (23–24) and 39 (28–54).
- **Two arms cost ×2.2 in days against four** (20 µm, liquid working: 18 vs 8 d), a little worse than
  the ×2 the page assumed. The 10–12 µm film the target review asks for costs a further ×1.3 (§3).
- **The liquid cells are the biggest lever: without them the days go up ×3.7.** Bring them (task S5).
- **Geometry: opposite arms, horizontal for the beam.**
  - With pointing + 0.3 ns TOF the vertical and horizontal pairs are equal within the MC (26 vs 24 d).
  - Without sub-ns timing the horizontal pair keeps its reach (23 d with pointing only) and the vertical pair loses
    it (34 d): a horizontal muon has to cross both side arms, and after pointing the horizontal pair sees ~10× fewer
    cosmics in the window than the vertical one.
  - Turning the arms toward the 140° X17 angle costs ×1.1 (Δφ = 160°) to ×2–2.5 (140°) in days (§5). Adjacent ("perpendicular")
    arms see 25–120° and no X17; they are a background diagnostic (§6).
- **Test the veto where it is hardest, without beam:** a few nights of cosmics with the arms **vertical** during installation
  record the MEG II "140° peak" at full strength (~10⁴ cosmic pairs/day in the E_sum window, ~250 after pointing, ~1 after
  0.3 ns TOF) and measure σ_t, the muon segment angle and the arm gains (§7.2). Then roll to horizontal for the beam.
- **The 441 keV calibration is ~10× smaller than the proposal says:** ~600 selected pairs per day above 90° (two arms), not
  6–12 × 10³. One day is enough for a ~5 % check of the IPC rate and shape (§2).
- **The old cosmic sample (L4) missed the inclined muons**: it gave a horizontal pair 110 coincidences/day, the new one (L15,
  every zenith angle) ~6,000 (§4).



---

## 1. Method

### 1.1 What was re-used, and what is new

- **Re-used (no new physics):** the FEASIBILITY_SIM §19 reference fit (`x17_facility_search/lnl/target/shapes/shapes_nd.py`):
  θ × |y| × E_sum, background shape floating (S_θ 2 % + S_θy 1 %), free acceptance cubic, per-arm gains, the
  n_TOF-anchored calorimeter response, the yields of the Cu hemisphere's film at E_p, live 0.95. The Cu-hemisphere Geant4
  tables of L11 and the ×30 as-built background run L13 (both on EOS, `target/sel_l11`, `sel_l13`).
- **New, `two_arm_nd.py`:** every table the fit loads passes through one function (`lnl_geant._combine`); the wrapper keeps
  only events whose selected pair is the requested pair of arms. Normalisations stay per generated event, so every rate is
  per day of the two-arm set-up. Events with three or more good arms: 0 in the beam samples, 0.2 % of cosmics, so
  re-forming pairs is not needed.
- **New Geant4 (MX17_Full_Geant branch `lnl_twoarm`, worktree `…/x17_lnl/MX17_Full_Geant_twoarm`):**
  - `--arms 0,1` builds only those arms; `--arm-phi p0,p1,p2,p3` turns each arm about the beam axis (run L16, §5).
  - `--cosmic-disk R`: cosmic muons start on a disk of radius R normal to their own direction (run L15, §4).
  - Binary `bin/mx17_full_sim_twoarm_be1c1bb`. With no new option it builds the same geometry as `lnl_culiner` (checked:
    identical arm positions, no overlaps).
- **The L13 E1 18.15 MeV table** (Cu hemisphere, as built) had never been merged: one job's ROOT file was truncated by an
  EOS FUSE write on 12 Nov and its rerun was not reduced. Reduced and merged tonight (15 M pairs, 0.680 % two-arm rows per
  pair against 0.692 % in L11). It is in `sel_l13/` now, so the ×30 E1 statistics are in every fit below.

### 1.2 The arms

Arm numbers of the simulation (beam along +y, up = +z at LNL):

| arm | position | module at n_TOF |
|---|---|---|
| 0 | +x (side) | D |
| 1 | −x (side) | B |
| 2 | +z (top) | A |
| 3 | −z (bottom) | C |

Pairs: **vertical** = 2 + 3 (top and bottom), **horizontal** = 0 + 1 (left and right), **adjacent** = 0 + 2 (one side, one top;
the "perpendicular" set-up). Which physical module sits where does not matter here: the simulation's modules are the
as-built n_TOF ones, and A and B would take two of the four places.

### 1.3 Two estimators, as in FEASIBILITY_SIM §19.2

The Cu hemisphere's as-built background tables are thin. Two MC-safe estimators are quoted:
- **direct + floor:** the configuration's own tables, each bin's background floored at one MC event's worth;
- **transplant:** the configuration's angle residuals, energy scale and rates carried onto the dense Li₂O-baseline MC.

The central value below is their geometric mean, the range the two. The raw fit (no floor) is printed in the CSVs for
reference only.

### 1.4 Conversions

- Z after T days at R(ATOMKI) = 5.8 × 10⁻⁶: Z = 3 √(T / d₃), d₃ the days to 3σ.
- Expected 90 % CL upper limit with no signal: R₉₀ = 1.28 / Z(T) × R(ATOMKI). MEG II's 90 % limit at 18.1 MeV is
  1.2 × 10⁻⁵ = 2.07 × R(ATOMKI).

### 1.5 Responses and cosmic vetoes (names in the CSVs)

| CSV name | meaning |
|---|---|
| `LNL calibrated` | **liquid working**: SiPM, plastic and liquid cells calibrated at LNL rates (`lnl_calo`, LS_FIX) |
| `n_TOF as is` | **liquid as at n_TOF**: the measured n_TOF resolutions and the liquid's 67–76 % pile-up response, 10 % gain prior |
| `LNL calibrated, LS off` | **no liquid**: E_sum = SiPM bar + 2 cm plastic |
| `trigger` | no cosmic veto beyond the E_sum window |
| `MM 15° point, μ 3°` | each segment points back to the spot (15° electron segments; the muon segments 3°, as on the bench) + 20° collinearity veto |
| `MM 15° + TOF` | the FEASIBILITY_SIM reference: pointing + a 0.3 ns arm-to-arm time of flight (**assumed, never measured**) |


## 2. Rates per day

From `out/summary_rates*.csv` (the reference event tables: the Cu hemisphere's own X17, IPC and ⁸Be-γ Monte Carlo,
weighted with its film yields; cosmics L15). The signal window is 125–160°, |y| < 0.6 and the response's E_sum window.


**Pairs per day in the signal window** (125–160°, |y| < 0.6, E_sum window), liquid working, 20 µm

| pair | veto | X17 at R(ATOMKI) | beam background | cosmics (MC events) | S/B |
|---|---|---|---|---|---|
| horizontal | no veto | 33.7 | 1020 | 1107.0 (2862) | 1.6 % |
| horizontal | pointing | 22.9 | 619 | 29.4 (76) | 3.5 % |
| horizontal | pointing + 1 ns TOF | 21.9 | 596 | 20.1 (52) | 3.5 % |
| horizontal | pointing + 0.3 ns TOF | 21.7 | 595 | 1.2 (3) | 3.6 % |
| vertical | no veto | 35.4 | 988 | 12804.4 (33104) | 0.3 % |
| vertical | pointing | 24.1 | 686 | 246.4 (637) | 2.6 % |
| vertical | pointing + 1 ns TOF | 23.3 | 666 | 159.4 (412) | 2.8 % |
| vertical | pointing + 0.3 ns TOF | 23.3 | 665 | 0.4 (1) | 3.5 % |


**1.10 MeV, pairs per day by opening angle** (pointing + 0.3 ns TOF, liquid working, E_sum window; in brackets: no E_sum cut)

| pair | component | 25-90° | 90-125° | 125-160° | 160-180° | all |
|---|---|---|---|---|---|---|
| horizontal | X17 at R(ATOMKI) | 0 (0) | 0 (1) | 22 (66) | 9 (25) | 31 (91) |
| horizontal | E1 IPC | 0 (0) | 10 (51) | 486 (1530) | 180 (507) | 677 (2088) |
| horizontal | M1 IPC | 0 (0) | 4 (22) | 102 (345) | 25 (82) | 131 (450) |
| horizontal | external conv. | 0 (0) | 0 (171) | 20 (1564) | 10 (179) | 29 (1914) |
| horizontal | 15.1 MeV IPC | 0 (0) | 2 (143) | 74 (3059) | 31 (999) | 107 (4201) |
| adjacent | X17 at R(ATOMKI) | 0 (2) | 3 (12) | 1 (5) | 0 (0) | 5 (19) |
| adjacent | E1 IPC | 1169 (3819) | 567 (1699) | 35 (138) | 0 (0) | 1772 (5661) |
| adjacent | M1 IPC | 737 (2480) | 222 (723) | 12 (43) | 0 (0) | 971 (3249) |
| adjacent | external conv. | 1921 (20314) | 340 (3866) | 35 (142) | 0 (0) | 2296 (24398) |
| adjacent | 15.1 MeV IPC | 255 (10209) | 98 (4096) | 7 (337) | 0 (1) | 360 (14657) |

**0.441 MeV, pairs per day by opening angle** (pointing + 0.3 ns TOF, liquid working, E_sum window; in brackets: no E_sum cut)

| pair | component | 25-90° | 90-125° | 125-160° | 160-180° | all |
|---|---|---|---|---|---|---|
| horizontal | X17 at R(ATOMKI) | 0 (0) | 0 (0) | 1 (2) | 0 (1) | 1 (3) |
| horizontal | E1 IPC | 0 (0) | 0 (1) | 14 (43) | 5 (14) | 19 (58) |
| horizontal | M1 IPC | 0 (0) | 13 (78) | 358 (1216) | 87 (284) | 458 (1578) |
| horizontal | external conv. | 0 (0) | 0 (57) | 110 (1344) | 55 (201) | 165 (1601) |
| horizontal | 15.1 MeV IPC | 0 (0) | 0 (43) | 17 (722) | 6 (220) | 23 (985) |
| adjacent | X17 at R(ATOMKI) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (1) |
| adjacent | E1 IPC | 33 (107) | 16 (47) | 1 (4) | 0 (0) | 49 (158) |
| adjacent | M1 IPC | 2522 (8499) | 759 (2497) | 39 (149) | 0 (0) | 3320 (11154) |
| adjacent | external conv. | 2282 (19992) | 285 (3824) | 56 (253) | 0 (0) | 2622 (24154) |
| adjacent | 15.1 MeV IPC | 105 (4329) | 30 (1416) | 1 (85) | 0 (0) | 137 (5836) |


- The 1.10 MeV background in the opposite pair is mostly the **E1 IPC** of direct capture, then M1 IPC, 15.1 MeV IPC and
  external conversions.
- At 441 keV the selected pairs are M1 IPC of the 17.64 MeV line plus conversions; X17 is not expected there.
- Adjacent arms see the small-angle IPC and the conversions at several thousand per day: a fast check of the material model.

## 3. Reach: days to 3σ at R(ATOMKI), and what five days give

Reference fit (FEASIBILITY_SIM §19), Cu hemisphere as built, 1 µA, 1.10 MeV, m_X = 16.8 MeV, live 0.95. Central value =
geometric mean of the two MC-safe estimators, range in brackets.


**20 µm Li (as simulated)** — days to 3σ at R(ATOMKI), 1 µA, 1.10 MeV (central; range of the two estimators)

| pair | stack | no veto | pointing | pointing + 1 ns TOF | pointing + 0.3 ns TOF |
|---|---|---|---|---|---|
| horizontal | liquid working | 23† | 17 (16–17) | 18† | 18 (18–18) |
| horizontal | liquid as at n_TOF | 27† | 28 (22–36) | 22† | 30 (22–42) |
| horizontal | no liquid | 49† | 66 (43–100) | 42† | 70 (42–118) |
| vertical | liquid working | 35† | 23 (22–25) | 20† | 20 (17–23) |
| vertical | liquid as at n_TOF | 43† | 30 (25–36) | 23† | 26 (19–34) |
| vertical | no liquid | 64† | 68 (43–107) | 41† | 56 (37–86) |
| adjacent | liquid working | 63† | 48 (32–71) | 71† | 51 (36–71) |
| adjacent | liquid as at n_TOF | 58† | 57 (49–66) | 65† | 58 (51–65) |
| adjacent | no liquid | 127† | 96 (75–123) | 121† | 76 (48–120) |
| four arms | liquid working | 17† | 10 (8–12) | 12† | 8 (7–10) |
| four arms | liquid as at n_TOF | 31† | 16 (15–17) | 17† | 15 (15–15) |
| four arms | no liquid | 45† | 48 (38–61) | 38† | 43 (32–59) |

† direct estimator only (no transplant run); compare with the direct values of the other columns (out/summary_reach*.csv, days3_direct), not with their central values.


**11 µm Li (the review’s 10–12 µm)** — days to 3σ at R(ATOMKI), 1 µA, 1.10 MeV (central; range of the two estimators)

| pair | stack | no veto | pointing | pointing + 1 ns TOF | pointing + 0.3 ns TOF |
|---|---|---|---|---|---|
| horizontal | liquid working | 35† | 23 (22–24) | 24† | 24 (23–24) |
| horizontal | liquid as at n_TOF | 44† | 38 (30–49) | 29† | 39 (28–54) |
| horizontal | no liquid | 74† | 92 (60–143) | 57† | 87 (54–139) |
| vertical | liquid working | 58† | 34 (32–35) | 30† | 26 (23–31) |
| vertical | liquid as at n_TOF | 72† | 45 (37–54) | 34† | 34 (26–45) |
| vertical | no liquid | 99† | 101 (63–162) | 59† | 78 (51–120) |
| four arms | liquid working | 30† | 14 (11–16) | 16† | 11 (9–13) |
| four arms | liquid as at n_TOF | 54† | 23 (23–24) | 24† | 19 (19–19) |
| four arms | no liquid | 66† | 68 (54–84) | 54† | 59 (44–78) |

† direct estimator only (no transplant run); compare with the direct values of the other columns (out/summary_reach*.csv, days3_direct), not with their central values.


**The vetoes compared with one estimator** (direct + floor, 20 µm, days to 3σ):

| pair | stack | no veto | pointing | pointing + 1 ns TOF | pointing + 0.3 ns TOF |
|---|---|---|---|---|---|
| horizontal | liquid working | 23 | 17 | 18 | 18 |
| horizontal | liquid as at n_TOF | 27 | 22 | 22 | 22 |
| horizontal | no liquid | 49 | 43 | 42 | 42 |
| vertical | liquid working | 35 | 22 | 20 | 17 |
| vertical | liquid as at n_TOF | 43 | 25 | 23 | 19 |
| vertical | no liquid | 64 | 43 | 41 | 37 |
| four arms | liquid working | 17 | 12 | 12 | 10 |
| four arms | liquid as at n_TOF | 31 | 17 | 17 | 15 |
| four arms | no liquid | 45 | 38 | 38 | 32 |

**Five days at 1.10 MeV** — expected Z if R = R(ATOMKI), expected 90 % CL limit / R(ATOMKI) (MEG II: 2.07), chance of ≥ 3σ and ≥ 2σ if ATOMKI is right; horizontal pair

| film | stack | veto | days to 3σ | Z(5 d) | R₉₀ / R(ATOMKI) | R₉₀ / MEG II | P(≥ 3σ) | P(≥ 2σ) |
|---|---|---|---|---|---|---|---|---|
| 11 µm | liquid working | pointing + 0.3 ns TOF | 24 | 1.38 | 0.93 | 0.45 | 5 % | 27 % |
| 11 µm | liquid working | pointing | 23 | 1.40 | 0.91 | 0.44 | 5 % | 27 % |
| 11 µm | liquid as at n_TOF | pointing + 0.3 ns TOF | 39 | 1.08 | 1.19 | 0.58 | 3 % | 18 % |
| 11 µm | liquid as at n_TOF | pointing | 38 | 1.09 | 1.18 | 0.57 | 3 % | 18 % |
| 11 µm | no liquid | pointing + 0.3 ns TOF | 87 | 0.72 | 1.78 | 0.86 | 1 % | 10 % |
| 11 µm | no liquid | pointing | 92 | 0.70 | 1.84 | 0.89 | 1 % | 10 % |
| 20 µm | liquid working | pointing + 0.3 ns TOF | 18 | 1.59 | 0.81 | 0.39 | 8 % | 34 % |
| 20 µm | liquid working | pointing | 17 | 1.63 | 0.79 | 0.38 | 9 % | 36 % |
| 20 µm | liquid as at n_TOF | pointing + 0.3 ns TOF | 30 | 1.23 | 1.05 | 0.51 | 4 % | 22 % |
| 20 µm | liquid as at n_TOF | pointing | 28 | 1.27 | 1.01 | 0.49 | 4 % | 23 % |
| 20 µm | no liquid | pointing + 0.3 ns TOF | 70 | 0.80 | 1.60 | 0.77 | 1 % | 12 % |
| 20 µm | no liquid | pointing | 66 | 0.83 | 1.55 | 0.75 | 1 % | 12 % |


- **Liquid cells:** working 18 d, as at n_TOF 22 d, none
  42 d (horizontal, direct). Without them E_sum is a SiPM bar plus 2 cm of plastic: the
  signal in the window drops ×6, and the γ₁ (15.1 MeV) pairs are no longer separated.
- **The time of flight matters only for the vertical pair.** Horizontal: 17 d with pointing,
  18 d with 0.3 ns TOF. Vertical: 22 d and
  17 d. A 1 ns TOF removes only a third of the remaining cosmics; it takes ≲ 0.4 ns.
- **No veto at all** costs the horizontal pair ×1.3 and
  the vertical pair ×1.6.
- **The film:** 11 µm has ~55 % of the 20 µm yield, so the beam terms fall and the cosmics do not: ×1.3
  in days for the horizontal pair, more for the vertical one where cosmics are a larger share.



## 4. Cosmics: the old sample missed the inclined muons (run L15)

### 4.1 What was wrong with L4

L4 (the only cosmic sample until tonight) starts every muon on a 3 × 3 m horizontal plane 1.5 m above the target. A muon
that reaches the target region from more than ~45° off the zenith starts outside that plane, so it is never generated.
For opposite arms on top and bottom that matters little; for two **side** arms, the only muons that cross both are close
to horizontal, and L4 has almost none of them.

`--cosmic-disk 900` (new, `lnl_twoarm`) starts each muon on a disk of radius 90 cm normal to its own direction, centred on
the target, 1.08 m upstream along the track. Zenith from the intensity cos²θ through a surface normal to the track,
θ < 89°; momentum as before (Reyna 2006 vertical spectrum; its harder spectrum at large zenith is not modelled, irrelevant
for minimum-ionising muons). Live time per muon: 60 s / (4π/3 · R²) with R in cm, for 1 cm⁻² min⁻¹ through a horizontal
surface. Same Cu-hemisphere geometry as the beam samples, all four arms built, cut to pairs like everything else.

Two-arm coincidences per day (trigger + Micromegas in the active area, any angle):

| pair | L4 (plane) | L15 (disk) |
|---|---|---|
| vertical (top + bottom) | 162,300 | 162,317 |
| horizontal (left + right) | 110 | **6,254** |
| adjacent (the four combinations) | 5,474–27,915 | 25,291–30,446 |

(`out/cosmic_rates.csv`; L4 1.0 live day, L15 10.0 live days.) The vertical rate agrees to 0.01 %, which checks the two
normalisations against each other; the horizontal one was **×57 too low**. A horizontal pair still sees ~26× fewer cosmic
coincidences than a vertical pair, not ~1,500×. The page's "suppressed by
geometry" was right in direction and wrong in size.

L15: 1630 jobs × 3 × 10⁵ muons = 4.9 × 10⁸ muons = 10.0 live days (`/eos/experiment/ntof/data/x17/lnl/L15/cosmicdisk_ta4arm`,
merged in chunks of 100 jobs into `target/sel_l15/`).

### 4.2 What the vertical pair sees: the MEG II peak

At trigger level the vertical pair's cosmic coincidences pile up between 125° and 160° of reconstructed opening angle
(half of them), with an E_sum spread over the ⁸Be window: **this is the cosmic "bump near 140°" that the MEG II members'
2026 Geant4 study found in ATOMKI-type spectrometers** (`x17_facility_search/lnl/PHYSICS.md`). A vertical pair is the
geometry that reproduces it at full strength, which makes it the right geometry to show it can be removed.


### 4.3 Cosmics by veto (L15, liquid working, signal window, per day)

| pair | no veto | pointing | pointing + 1 ns TOF | pointing + 0.3 ns TOF |
|---|---|---|---|---|
| horizontal | 1107.0 (2862 MC) | 29.4 (76 MC) | 20.1 (52 MC) | 1.2 (3 MC) |
| vertical | 12804.4 (33104 MC) | 246.4 (637 MC) | 159.4 (412 MC) | 0.4 (1 MC) |

The fits used L15 chunks 0–3 (400 jobs, 2.45 live days: 33104 MC events in the vertical no-veto window, 76 in the horizontal pointing one); the coincidence tables of §4.1 (`out/cosmic_rates.csv`) use all of it, 10.0 live days. At the levels where cosmics matter the fits have tens to thousands of MC events; with 0.3 ns TOF, 0–7 events: there they are negligible against ~600 beam pairs either way. The vertical and four-arm cosmic tables drop rows below 40° of opening angle (memory; the fit starts at 90° with 5° smoothing), so the spectra of those two pairs show no cosmics below 40°.


## 5. Arms turned toward the X17 angle (run L16): no gain

The X17 pairs open at ~140°. With only two arms on a free frame, the arms could be placed at Δφ < 180° about the beam,
centring the acceptance on 140°. L16 builds only arms 0 and 1, each tilted up by (180° − Δφ)/2 (a "Λ"; the beam samples do
not care about the roll), X17 m16.8 (5 × 10⁵) and M1/E1 IPC at 18.15 MeV (1.5 × 10⁶ / 1 × 10⁶) per Δφ.

| Δφ | X17 two-arm acceptance | X17 in fit region (ref. level, liquid working) | IPC in fit region | days (counting scaling) |
|---|---|---|---|---|
| 180 (four-arm tables) | 1.42 % | 1.00 | 1.00 | ×1.00 |
| 180 (two arms built) | 1.45 % | 1.04 | — | — |
| 160 | 1.39 % | 1.06 | 1.26 | ×1.11 |
| 140 | 1.06 % | 0.88 | 1.58 | ×2.0 |

(`out/ta_compare.csv`; days = IPC ratio / signal ratio², the IPC weighted with the opposite pair's own E1/M1 mix; the
other responses and levels give the same pattern, ×1.06–1.15 at 160° and ×2.0–2.5 at 140°.)

- Opposite arms already accept 140° pairs: each arm spans ±40° along the beam, and the pair's opening can lie along the
  beam as well as around it.
- Turning the arms in brings in the IPC, which rises steeply toward small angles, faster than the signal.
- The 180° row with only two arms built matches the four-arm tables (1.45 vs 1.42 %), a check of the two-arm cut.
- **Keep the arms opposite.**

## 6. Adjacent ("perpendicular") arms: a diagnostic, not a physics geometry

Adjacent arms see opening angles of 25–120°: no X17 to speak of (the 3σ days are 50–100, and that only from the X17 tail
the Cu hemisphere smears below 120°). What they see well:


| E_p | component | adjacent, 25–90° | opposite (horizontal), all angles |
|---|---|---|---|
| 1.10 MeV | E1 IPC | 1169 | 677 |
| 1.10 MeV | M1 IPC | 737 | 131 |
| 1.10 MeV | external conversions | 1921 | 29 |
| 1.10 MeV | 15.1 MeV IPC | 255 | 107 |
| 0.441 MeV | E1 IPC | 33 | 19 |
| 0.441 MeV | M1 IPC | 2522 | 458 |
| 0.441 MeV | external conversions | 2282 | 165 |
| 0.441 MeV | 15.1 MeV IPC | 105 | 23 |

(pairs per day, pointing + 0.3 ns TOF, liquid working, E_sum window, 20 µm.) Half a day of adjacent running gives ~1,000 conversion pairs at 25–90°: the external-conversion model of the Cu wall, which carries ~20 % of the background in the X17 fit and rests on a few hundred MC events, gets a direct measurement. It also checks the opening-angle response away from the X17 window and the trigger with two arms at 90°, which is half the pair combinations of the four-arm experiment.

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


## 8. Caveats

- **Thin Monte Carlo** is still the main limitation of the as-built Cu-hemisphere numbers: the two estimators differ by up
  to ×2 in a few rows (the range quoted). The EPC (external conversions in the 200 µm Cu wall) rests on a few hundred MC
  events in the opposite pairs; vertical and horizontal pairs differ by ×2–3 in EPC in the window, which is MC noise.
- **TOF σ_t = 0.3 ns** (the reference level) is assumed. The "pointing only" rows do not need it; the vertical-pair cosmic
  nights measure it.
- **The muon segment resolution** (3° in the "pointing" level, the bench value) is not in the Geant4 smearing itself; it
  is applied to the cosmic sample only.
- **Air showers** (several particles at once) are not simulated. Two shower particles reaching two opposite side arms at
  the same time pass the time of flight but not the pointing (a near-vertical track in a vertical Micromegas plane misses
  the spot by ≥ 20 cm); the measured beam-off rate in the physics geometry is the check.
- **The roll of the pair** (horizontal vs vertical) is simulated with arms 0–1 and 2–3, which are different modules (their
  liquid cells sit differently): part of the ±10 % between the two pairs' beam numbers is that, part is MC noise.
- **20 µm Li film** as simulated; the review recommends 10–12 µm (51–61 % of the yield: ×1.6–2 in days, `TARGET_REVIEW.md`).
- The 441 keV numbers reuse the 18.15 MeV M1 table with the 17.64 MeV yields (as `shapes_nd` does).

## 9. Next

1. Proposal text (task R5): the reach rows of §3, the 441 keV rate of §2, the vertical-cosmics test of §7.2, Fig. from
   `planning/figures.py`. The sensitivity sentence: "expected 90 % CL limit 0.8–1.3 × R(ATOMKI) in five days with liquid
   cells, below MEG II's limit" (§0 numbers).
2. More as-built MC for the Cu hemisphere (task R6): the EPC and the IPC at large angles in the opposite pairs, ×5.
3. The muon segment smearing inside the Geant4 levels, not as a wrapper (FEASIBILITY_SIM §19.6 item 4).
4. A roll angle for the stand and a 45° ("X") pair, if the mechanics prefer it (`x17_facility_search/mechanics/`):
   the L15 cosmics can be re-cut for it only after a rotated-cosmic run (the beam samples do not care).

**Files:** `two_arm_nd.py`, `ta_compare.py`, `cosmic_rates.py`, `summarize.py`, `report_tables.py`, `build_study_md.py`
(this text's numbers), `make_two_arm_deck.py` (the slide note), `run_pass.sh` (the whole grid), `lxplus/` (L15, L16 jobs).
