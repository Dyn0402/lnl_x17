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

<!-- RESULTS -->

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

<!-- SECTIONS 2-3: reach and rates (filled from pass 2) -->

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

<!-- 4.3 numbers by veto, from pass 2 -->

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

<!-- 6 numbers from pass 2 spectra -->

<!-- SECTION 7 -->

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
   five days with liquid cells, about MEG II's; a lighter Al end piece would reach ~0.6–0.8 ×" (§0 numbers).
2. A two-arm Geant4 run of the lighter Al end piece (Al ogive + Cu liner, or the 45° Al cap): its rows are scaled estimates (§0).
   The hemisphere's as-built MC (L10 + L18, ×30) is no longer the limitation.
3. The muon segment smearing inside the Geant4 levels, not as a wrapper (FEASIBILITY_SIM §19.6 item 4).
4. A roll angle for the stand and a 45° ("X") pair, if the mechanics prefer it (`x17_facility_search/mechanics/`):
   the L15 cosmics can be re-cut for it only after a rotated-cosmic run (the beam samples do not care).

**Files:** `two_arm_nd.py`, `ta_compare.py`, `cosmic_rates.py`, `summarize.py`, `report_tables.py`, `build_study_md.py`
(this text's numbers), `make_two_arm_deck.py` (the slide note), `run_pass.sh` (the whole grid), `lxplus/` (L15, L16 jobs).
