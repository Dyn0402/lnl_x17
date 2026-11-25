# The two-arm LNL run, simulated: what 8 days can show, and how to spend them

Written 2026-11-19 (overnight study); **target corrected 2026-11-20**. Set-up: the slot-1 feasibility run of
`../slot1_feasibility/PLAN.md`: two Micromegas (A, B), two SiPM walls, four small 20 × 30 × 2 cm plastics, optionally two
liquid cells, **the built Cu hemisphere** (R 11 mm, 300 µm wall, Cu rim 4 × 5 mm, on the photographed grey flange and tube;
Geant4 config `dome300`; 20 µm Li, yields also for the recommended 10–12 µm), AN2000 at 1 µA.

> **Correction, 2026-11-20.** The 19 Nov version of this study (passes 1–3) simulated the **Cu ogive** of Pierfrancesco's
> 27 Oct CAD sketch (Ø50 × 63 mm, 200 µm; config `ogCu200`, runs L11 + L13) and called it "the Cu hemisphere". The ogive
> is not built. This version uses the built hemisphere (`dome300`, runs L10 + **L18**, a new ×30 as-built run, §1.1).
> The pass-3 ogive tables stay in `out/*_pass3*` for reference (they scale the Al-ogive rows of the planning).
Slide note: <https://dylan-neff.web.cern.ch/notes/lnl-two-arm-run.html>. This replaces the ×2 scaling of
`../planning/two_arm_estimates.py` (task R1).

## 0. Bottom line (2026-11-20, Geant4, the built Cu hemisphere)

- **With the built Cu hemisphere, five days at 1.10 MeV do not beat MEG II.** Two opposite arms give an expected 90 % CL
  limit of **2.35 × R(ATOMKI)** with the liquid cells working, **3.10 ×** with the liquid as
  it ran at n_TOF and **4.32 ×** without it (11 µm Li, horizontal pair, MM pointing + 0.6 ns TOF). MEG II's
  published limit is 2.07 × R(ATOMKI). Matching it would take 6 days at 1.10 MeV with the liquid working; the ATOMKI ratio
  28 days.
- **Why:** every lepton crosses the 300 µm Cu wall (2 % X₀) or its rim. Against the Cu ogive that the 19 Nov version simulated
  by mistake, the hemisphere keeps ×0.58 of the X17 pairs in two arms, ×0.41 of them in the E_sum window (the energy sum
  drops by ~1 MeV), and its film yields ×0.58 γ₀ per proton: ×0.14 in selected signal, while the cosmics stay. Days to 3σ:
  151 (120–189) with the liquid working, 263 (215–321) as at n_TOF,
  511 without (the ogive: 25, 44, 94).
- **The target holder is now the decision.** A lighter end piece changes the run from a feasibility test into a first limit:
  the Al ogive + Cu liner (its own two-arm Geant4 tables, L12 + L13, R10_AL_OGIVE.md, 25 Nov) gives
  0.88 / 1.19 / 1.70 × R(ATOMKI)
  (liquid working / as at n_TOF / none) in the same five days, 21 / 39 / 79 days to 3σ. The earlier scaled estimate
  (0.62 / 0.81 / 1.46 ×) was optimistic. The 45° Al end cap of the target review is in the same class
  (TARGET_REVIEW.md). Ask Pierfrancesco whether either can be made for slot 1 (task T1); otherwise the run is the feasibility
  test only, and says so.
- **What the run still delivers with the hemisphere:** every rate, trigger and track fraction, the cosmic veto at full
  strength, the 441 keV calibration and the material model of the holder itself (the Predictions tab; `PREDICTIONS.md`).
  An ATOMKI-size signal would show at 0.3–0.5σ: none of that is a physics result.
- **Two arms against four:** this fit sums all pairs of the four-arm set-up, and the vertical and adjacent pairs add
  cosmics, so four arms come out at 83 d against 86 d for the horizontal pair (20 µm, liquid working).
  The four-arm number needs a fit per pair before it is quoted.
- **The 10–12 µm film costs ×1.7** in days against 20 µm (more than for the ogive: the hemisphere's beam terms
  are smaller, so the cosmics weigh more). **The liquid cells: without them ×3.4.**
- **Geometry: opposite arms, horizontal for the beam:** 151 d against 237 d for the vertical pair
  (with pointing only: 132 vs 219 d).
- **The 441 keV calibration:** ~140 selected pairs per day above 90° (two arms; the ogive gave ~600): one day measures the
  absolute rate to ±8 %, the shape coarsely (§2).
- **Test the veto where it is hardest, without beam:** cosmic nights with the arms vertical (unchanged: the target does not
  matter for muons), then roll to horizontal.
- §4.2, §5 (rotated arms, L16) and the systematics scans (geom_syst, struct_scan, tof_scan) are still the Cu ogive's; their
  ratios carry over, their absolute days do not.



---

## 1. Method

### 1.1 What was re-used, and what is new

- **Re-used (no new physics):** the FEASIBILITY_SIM §19 reference fit (`x17_facility_search/lnl/target/shapes/shapes_nd.py`):
  θ × |y| × E_sum, background shape floating (S_θ 2 % + S_θy 1 %), free acceptance cubic, per-arm gains, the
  n_TOF-anchored calorimeter response, the yields of the Cu hemisphere's film at E_p, live 0.95. The Cu-hemisphere Geant4
  tables of L10 (`dome300`, 27 Oct) and the new ×30 as-built background run **L18** (20 Nov: M1/E1 IPC at 18.15 and
  15.1 MeV, 150 × 10⁵ pairs each; 8Be γ lines, 150 × 2 × 10⁶; X17, 30 × 10⁵; binary `mx17_full_sim_twoarm_10229eb`, the
  same hemisphere geometry as L10 line by line; on EOS `target/sel_l18`, chunks of 30–50 jobs).
- **New, `two_arm_nd.py`:** every table the fit loads passes through one function (`lnl_geant._combine`); the wrapper keeps
  only events whose selected pair is the requested pair of arms. Normalisations stay per generated event, so every rate is
  per day of the two-arm set-up. Events with three or more good arms: 0 in the beam samples, 0.2 % of cosmics, so
  re-forming pairs is not needed.
- **New Geant4 (MX17_Full_Geant branch `lnl_twoarm`, worktree `…/x17_lnl/MX17_Full_Geant_twoarm`):**
  - `--arms 0,1` builds only those arms; `--arm-phi p0,p1,p2,p3` turns each arm about the beam axis (run L16, §5).
  - `--cosmic-disk R`: cosmic muons start on a disk of radius R normal to their own direction (run L15, §4).
  - Binary `bin/mx17_full_sim_twoarm_be1c1bb`. With no new option it builds the same geometry as `lnl_culiner` (checked:
    identical arm positions, no overlaps).
- *(19 Nov, the ogive tables)* **The L13 E1 18.15 MeV table** (Cu ogive, as built) had never been merged: one job's ROOT file was truncated by an
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
| `MM 15° + TOF` | the FEASIBILITY_SIM reference: pointing + a 0.6 ns per-arm time of flight (**measured** on n_TOF beam-off cosmics, 0.52–0.64 ns: nTof_x17 `ntof_cosmics/results/ac_tof/report.html`; read by `lnl_geant.TOF_SIGMA_NS`) |


## 2. Rates per day

From `out/summary_rates*.csv` (the reference event tables: the Cu hemisphere's own X17, IPC and ⁸Be-γ Monte Carlo,
weighted with its film yields; cosmics L15). The signal window is 125–160°, |y| < 0.6 and the response's E_sum window.


**Pairs per day in the signal window** (125–160°, |y| < 0.6, E_sum window), liquid working, 20 µm

| pair | veto | X17 at R(ATOMKI) | beam background | cosmics (MC events) | S/B |
|---|---|---|---|---|---|
| horizontal | no veto | 4.8 | 101 | 1107.0 (2862) | 0.4 % |
| horizontal | pointing | 3.3 | 69 | 29.4 (76) | 3.3 % |
| horizontal | pointing + 1 ns TOF | 3.2 | 67 | 20.1 (52) | 3.6 % |
| horizontal | pointing + 0.6 ns TOF | 3.2 | 68 | 45.6 (118) | 2.8 % |
| vertical | no veto | 4.7 | 128 | 12804.4 (33104) | 0.0 % |
| vertical | pointing | 3.2 | 66 | 246.4 (637) | 1.0 % |
| vertical | pointing + 1 ns TOF | 3.1 | 65 | 159.4 (412) | 1.4 % |
| vertical | pointing + 0.6 ns TOF | 3.1 | 65 | 493.5 (1276) | 0.6 % |


**1.10 MeV, pairs per day by opening angle** (pointing + 0.6 ns TOF, liquid working, E_sum window; in brackets: no E_sum cut)

| pair | component | 25-90° | 90-125° | 125-160° | 160-180° | all |
|---|---|---|---|---|---|---|
| horizontal | X17 at R(ATOMKI) | 0 (0) | 0 (0) | 3 (22) | 2 (9) | 5 (32) |
| horizontal | E1 IPC | 0 (0) | 4 (22) | 65 (443) | 19 (138) | 87 (603) |
| horizontal | M1 IPC | 0 (0) | 1 (5) | 9 (80) | 2 (22) | 12 (107) |
| horizontal | external conv. | 0 (0) | 0 (78) | 31 (1297) | 0 (204) | 31 (1580) |
| horizontal | 15.1 MeV IPC | 0 (0) | 0 (43) | 3 (847) | 0 (256) | 4 (1146) |
| adjacent | X17 at R(ATOMKI) | 0 (2) | 1 (7) | 0 (2) | 0 (0) | 1 (11) |
| adjacent | E1 IPC | 194 (1488) | 81 (590) | 5 (47) | 0 (0) | 280 (2126) |
| adjacent | M1 IPC | 91 (713) | 26 (202) | 1 (13) | 0 (0) | 118 (928) |
| adjacent | external conv. | 2366 (36005) | 248 (5590) | 0 (251) | 0 (0) | 2645 (41985) |
| adjacent | 15.1 MeV IPC | 16 (3674) | 6 (1365) | 0 (102) | 0 (0) | 22 (5143) |

**0.441 MeV, pairs per day by opening angle** (pointing + 0.6 ns TOF, liquid working, E_sum window; in brackets: no E_sum cut)

| pair | component | 25-90° | 90-125° | 125-160° | 160-180° | all |
|---|---|---|---|---|---|---|
| horizontal | X17 at R(ATOMKI) | 0 (0) | 0 (0) | 0 (1) | 0 (1) | 0 (2) |
| horizontal | E1 IPC | 0 (0) | 0 (1) | 3 (24) | 1 (7) | 5 (32) |
| horizontal | M1 IPC | 0 (0) | 3 (50) | 106 (874) | 25 (249) | 135 (1174) |
| horizontal | external conv. | 0 (0) | 0 (252) | 2 (2119) | 0 (535) | 2 (2907) |
| horizontal | 15.1 MeV IPC | 0 (0) | 0 (27) | 2 (421) | 0 (117) | 2 (565) |
| adjacent | X17 at R(ATOMKI) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (1) |
| adjacent | E1 IPC | 10 (80) | 4 (32) | 0 (3) | 0 (0) | 15 (114) |
| adjacent | M1 IPC | 933 (7312) | 265 (2088) | 12 (124) | 0 (0) | 1211 (9530) |
| adjacent | external conv. | 5969 (69914) | 455 (10835) | 0 (367) | 0 (0) | 6424 (81204) |
| adjacent | 15.1 MeV IPC | 10 (2932) | 3 (934) | 0 (59) | 0 (0) | 13 (3926) |


- The 1.10 MeV background in the opposite pair is mostly the **E1 IPC** of direct capture, then M1 IPC, 15.1 MeV IPC and
  external conversions.
- At 441 keV the selected pairs are M1 IPC of the 17.64 MeV line plus conversions; X17 is not expected there.
- Adjacent arms see the small-angle IPC and the conversions at several thousand per day: a fast check of the material model.

## 3. Reach: days to 3σ at R(ATOMKI), and what five days give

Reference fit (FEASIBILITY_SIM §19), the built Cu hemisphere (dome300, L10 + L18) as built, 1 µA, 1.10 MeV, m_X = 16.8 MeV, live 0.95. Central value =
geometric mean of the two MC-safe estimators, range in brackets.


**20 µm Li (as simulated)** — days to 3σ at R(ATOMKI), 1 µA, 1.10 MeV (central; range of the two estimators)

| pair | stack | no veto | pointing | pointing + 1 ns TOF | pointing + 0.6 ns TOF |
|---|---|---|---|---|---|
| horizontal | liquid working | 148† | 78 (57–106) | 109† | 86 (68–110) |
| horizontal | liquid as at n_TOF | 181† | 130 (106–160) | 158† | 151 (128–178) |
| horizontal | no liquid | 259† | 260 (257–262) | 261† | 293 (277–310) |
| vertical | liquid working | 262† | 125 (103–151) | 129† | 131 (111–156) |
| vertical | liquid as at n_TOF | 330† | 230 (197–269) | 232† | 234 (195–281) |
| vertical | no liquid | 352† | 313 (292–335) | 267† | 313 (289–339) |
| adjacent | liquid working | 896† | 351 (137–898) | 742† | 317 (131–766) |
| adjacent | liquid as at n_TOF | 742† | 327 (137–780) | 790† | 340 (147–788) |
| adjacent | no liquid | 1528† | 620 (268–1433) | 1279† | 620 (297–1295) |
| four arms | liquid working | 152† | 79 (47–132) | 127† | 83 (48–143) |
| four arms | liquid as at n_TOF | 156† | 94 (62–142) | 138† | 103 (67–159) |
| four arms | no liquid | 186† | 186 (148–234) | 217† | 217 (180–263) |

† direct estimator only (no transplant run); compare with the direct values of the other columns (out/summary_reach*.csv, days3_direct), not with their central values.


**11 µm Li (the review’s 10–12 µm)** — days to 3σ at R(ATOMKI), 1 µA, 1.10 MeV (central; range of the two estimators)

| pair | stack | no veto | pointing | pointing + 1 ns TOF | pointing + 0.6 ns TOF |
|---|---|---|---|---|---|
| horizontal | liquid working | 292† | 132 (97–180) | 180† | 151 (120–189) |
| horizontal | liquid as at n_TOF | 326† | 226 (182–282) | 275† | 263 (215–321) |
| horizontal | no liquid | 452† | 472 (472–472) | 475† | 511 (494–529) |
| vertical | liquid working | 548† | 219 (179–268) | 226† | 237 (193–290) |
| vertical | liquid as at n_TOF | 654† | 425 (380–475) | 414† | 426 (361–501) |
| vertical | no liquid | 695† | 534 (497–574) | 452† | 537 (496–581) |
| four arms | liquid working | 295† | 135 (81–227) | 216† | 148 (85–256) |
| four arms | liquid as at n_TOF | 308† | 174 (116–263) | 254† | 194 (126–301) |
| four arms | no liquid | 329† | 323 (257–405) | 380† | 372 (308–450) |

† direct estimator only (no transplant run); compare with the direct values of the other columns (out/summary_reach*.csv, days3_direct), not with their central values.


**The vetoes compared with one estimator** (direct + floor, 20 µm, days to 3σ):

| pair | stack | no veto | pointing | pointing + 1 ns TOF | pointing + 0.6 ns TOF |
|---|---|---|---|---|---|
| horizontal | liquid working | 148 | 106 | 109 | 110 |
| horizontal | liquid as at n_TOF | 181 | 160 | 158 | 178 |
| horizontal | no liquid | 259 | 257 | 261 | 277 |
| vertical | liquid working | 262 | 151 | 129 | 156 |
| vertical | liquid as at n_TOF | 330 | 269 | 232 | 281 |
| vertical | no liquid | 352 | 292 | 267 | 289 |
| four arms | liquid working | 152 | 132 | 127 | 143 |
| four arms | liquid as at n_TOF | 156 | 142 | 138 | 159 |
| four arms | no liquid | 186 | 234 | 217 | 263 |

**Five days at 1.10 MeV** — expected Z if R = R(ATOMKI), expected 90 % CL limit / R(ATOMKI) (MEG II: 2.07), chance of ≥ 3σ and ≥ 2σ if ATOMKI is right; horizontal pair

| film | stack | veto | days to 3σ | Z(5 d) | R₉₀ / R(ATOMKI) | R₉₀ / MEG II | P(≥ 3σ) | P(≥ 2σ) |
|---|---|---|---|---|---|---|---|---|
| 11 µm | liquid working | pointing + 0.6 ns TOF | 151 | 0.55 | 2.35 | 1.13 | 1 % | 7 % |
| 11 µm | liquid working | pointing | 132 | 0.58 | 2.20 | 1.06 | 1 % | 8 % |
| 11 µm | liquid as at n_TOF | pointing + 0.6 ns TOF | 263 | 0.41 | 3.10 | 1.50 | 0 % | 6 % |
| 11 µm | liquid as at n_TOF | pointing | 226 | 0.45 | 2.87 | 1.39 | 1 % | 6 % |
| 11 µm | no liquid | pointing + 0.6 ns TOF | 511 | 0.30 | 4.32 | 2.09 | 0 % | 4 % |
| 11 µm | no liquid | pointing | 472 | 0.31 | 4.15 | 2.01 | 0 % | 5 % |
| 20 µm | liquid working | pointing + 0.6 ns TOF | 86 | 0.72 | 1.78 | 0.86 | 1 % | 10 % |
| 20 µm | liquid working | pointing | 78 | 0.76 | 1.68 | 0.81 | 1 % | 11 % |
| 20 µm | liquid as at n_TOF | pointing + 0.6 ns TOF | 151 | 0.55 | 2.35 | 1.13 | 1 % | 7 % |
| 20 µm | liquid as at n_TOF | pointing | 130 | 0.59 | 2.18 | 1.05 | 1 % | 8 % |
| 20 µm | no liquid | pointing + 0.6 ns TOF | 293 | 0.39 | 3.27 | 1.58 | 0 % | 5 % |
| 20 µm | no liquid | pointing | 260 | 0.42 | 3.08 | 1.49 | 0 % | 6 % |


- **Liquid cells:** working 110 d, as at n_TOF 178 d, none
  277 d (horizontal, direct). Without them E_sum is a SiPM bar plus 2 cm of plastic: the
  signal in the window drops several-fold, and the γ₁ (15.1 MeV) pairs are no longer separated.
- **The time of flight matters only for the vertical pair.** Horizontal: 106 d with pointing,
  110 d with 0.6 ns TOF. Vertical: 151 d and
  156 d. A 1 ns TOF removes only a third of the remaining cosmics; it takes ≲ 0.4 ns.
- **No veto at all** costs the horizontal pair ×1.4 and
  the vertical pair ×1.7.
- **The film:** 11 µm has ~55 % of the 20 µm yield, so the beam terms fall and the cosmics do not: ×1.7
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
surface. All four arms built, cut to pairs like everything else. The L15 muons were simulated with the Cu ogive in place
(the target is irrelevant for muons crossing the arms).

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

| pair | no veto | pointing | pointing + 1 ns TOF | pointing + 0.6 ns TOF |
|---|---|---|---|---|
| horizontal | 1107.0 (2862 MC) | 29.4 (76 MC) | 20.1 (52 MC) | 45.6 (118 MC) |
| vertical | 12804.4 (33104 MC) | 246.4 (637 MC) | 159.4 (412 MC) | 493.5 (1276 MC) |

The fits used L15 chunks 0–3 (400 jobs, 2.45 live days: 33104 MC events in the vertical no-veto window, 76 in the horizontal pointing one); the coincidence tables of §4.1 (`out/cosmic_rates.csv`) use all of it, 2.5 live days. At the levels where cosmics matter the fits have tens to thousands of MC events. The vertical and four-arm cosmic tables drop rows below 40° of opening angle (memory; the fit starts at 90° with 5° smoothing), so the spectra of those two pairs show no cosmics below 40°.


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
| 1.10 MeV | E1 IPC | 194 | 87 |
| 1.10 MeV | M1 IPC | 91 | 12 |
| 1.10 MeV | external conversions | 2366 | 31 |
| 1.10 MeV | 15.1 MeV IPC | 16 | 4 |
| 0.441 MeV | E1 IPC | 10 | 5 |
| 0.441 MeV | M1 IPC | 933 | 135 |
| 0.441 MeV | external conversions | 5969 | 2 |
| 0.441 MeV | 15.1 MeV IPC | 10 | 2 |

(pairs per day, pointing + 0.6 ns TOF, liquid working, E_sum window, 20 µm.) Half a day of adjacent running gives ~1,000 conversion pairs at 25–90°: the external-conversion model of the Cu wall, which carries ~20 % of the background in the X17 fit and rests on a few hundred MC events, gets a direct measurement. It also checks the opening-angle response away from the X17 window and the trigger with two arms at 90°, which is half the pair combinations of the four-arm experiment.

## 7. The run plan: hedge first, then five days of X17 data

### 7.1 The principle

Everything that makes the feasibility case (rates, calibration, backgrounds, the veto) is front-loaded and takes
three days at most; the X17 data fill the rest. If the apparatus misbehaves, the run is still a full feasibility study;
if it works, the last five days give a first limit: with the built Cu hemisphere ~2.4 × R(ATOMKI) at best, about MEG II's
level; with a lighter Al end piece ~0.9–1.2 × (Geant4, R10_AL_OGIVE.md). Nothing in the plan depends on a lucky signal.

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
| 2 | 0.441 MeV | locate the 441 keV resonance on the arm singles; 17.64 MeV M1 IPC | ~140 pairs/day above 90° in the E_sum window with the built Cu hemisphere (~1,600 with no E_sum cut; the ogive gave ~600): the absolute IPC rate to ~8 % in a day, the θ shape and the E_sum peak against Geant4 |
| 3–7 | 1.10 MeV | the 18.15 MeV region; 30 min yield check each day | the X17 data (§3): expected limit 2.4 / 3.1 × R(ATOMKI) with the liquid working / as at n_TOF (built Cu hemisphere); 0.9 / 1.2 × with a lighter Al end piece (Geant4, R10) |
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
- A first X17 limit at 18.15 MeV: with the built Cu hemisphere about MEG II's (2.4 × R(ATOMKI), liquid working); below the
  ATOMKI ratio only with a lighter Al end piece (estimate).


## 8. Caveats

- **Thin Monte Carlo** is still the main limitation of the as-built Cu-hemisphere numbers: the two estimators differ by up
  to ×2 in a few rows (the range quoted). The EPC (external conversions in the 200 µm Cu wall) rests on a few hundred MC
  events in the opposite pairs; vertical and horizontal pairs differ by ×2–3 in EPC in the window, which is MC noise.
- **TOF σ_t = 0.6 ns per arm** (the reference level) is measured with the n_TOF readout (0.52–0.64 ns); the LNL digitisers are still to check (R4). The "pointing only" rows do not need it; the vertical-pair cosmic
  nights measure it.
- **The muon segment resolution** (3° in the "pointing" level, the bench value) is not in the Geant4 smearing itself; it
  is applied to the cosmic sample only.
- **Air showers** (several particles at once) are not simulated. Two shower particles reaching two opposite side arms at
  the same time pass the time of flight but not the pointing (a near-vertical track in a vertical Micromegas plane misses
  the spot by ≥ 20 cm); the measured beam-off rate in the physics geometry is the check.
- **The roll of the pair** (horizontal vs vertical) is simulated with arms 0–1 and 2–3, which are different modules (their
  liquid cells sit differently): part of the ±10 % between the two pairs' beam numbers is that, part is MC noise.
- **20 µm Li film** as simulated; the review recommends 10–12 µm (51–61 % of the yield: ×1.7 in days for the hemisphere, §0; `TARGET_REVIEW.md`).
- The 441 keV numbers reuse the 18.15 MeV M1 table with the 17.64 MeV yields (as `shapes_nd` does).

## 9. Next

1. Proposal text (task R5): the reach rows of §3, the 441 keV rate of §2, the vertical-cosmics test of §7.2, Fig. from
   `planning/figures.py`. The sensitivity sentence with the built hemisphere: "expected 90 % CL limit 2.4 × R(ATOMKI) in
   five days with liquid cells, about MEG II's; a lighter Al end piece would reach about R(ATOMKI) (0.9–1.2 ×)" (§0 numbers).
2. ~~A two-arm Geant4 run of the lighter Al end piece~~: done 25 Nov for the Al ogive + Cu liner (R10_AL_OGIVE.md). The 45° Al cap is not simulated in two arms.
   The hemisphere's as-built MC (L10 + L18, ×30) is no longer the limitation.
3. The muon segment smearing inside the Geant4 levels, not as a wrapper (FEASIBILITY_SIM §19.6 item 4).
4. A roll angle for the stand and a 45° ("X") pair, if the mechanics prefer it (`x17_facility_search/mechanics/`):
   the L15 cosmics can be re-cut for it only after a rotated-cosmic run (the beam samples do not care).

**Files:** `two_arm_nd.py`, `ta_compare.py`, `cosmic_rates.py`, `summarize.py`, `report_tables.py`, `build_study_md.py`
(this text's numbers), `make_two_arm_deck.py` (the slide note), `run_pass.sh` (the whole grid), `lxplus/` (L15, L16 jobs).
