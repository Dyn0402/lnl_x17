# The CN instead of AN2000: what changes for the slot-1 proposal

Written 2026-11-25. Dylan learned that the AN2000 beam is probably not available, so the proposal now asks for the CN.
This note says what the change does to the request, the calibration and the reach. It also records the choices made
for the proposal text (Dylan, 25 Nov): assume 1 µA, assume beam on working hours only, and request the 441 keV point
with an H₂⁺ beam without making the proposal depend on it. Later the same day (Dylan): **the allocation is 8 days in
total**, so the request is 8 working days, not the 20 of the first version of this note.

Sources: the LNL beam sheet (`x17_facility_search/lnl/refs/LNL_Beams_AN2000_CN.txt`), the 2026 CN paper
(arXiv:2605.12005, same folder), `x17_facility_search/lnl/FACILITY.md`, and the two-arm fits of `sim2arm/` (new tags
`_cn2li11`, `_cn4li11`, `_cn2alli11`, `_cn4alli11`, made by `sim2arm/run_cn.sh`).

> **Update 2026-11-26:** with the external conversions of run L19 (`sim2arm/EPC_L19.md`, 100 times the simulated
> statistics) the limits for the 46 h at 1.10 MeV are 4.3 / 5.5 / 7.2 × R(ATOMKI) (liquid working / as at n_TOF / none)
> instead of 3.8 / 5.0 / 7.0 ×, and 2.66 × instead of 2.35 × for 5 days of beam. The 441 keV day has about 70 beam pairs
> in 8 h, a third of them external conversions. The Li film thickness (±50 %) moves the 4.3 × between 6.9 × and 3.55 ×
> (`LI_THICKNESS.md`). The tables below are the 25 Nov numbers.

## 0. Result in short

1. **The 441 keV calibration is not necessarily lost.** The CN cannot run below 0.8 MV, so it cannot accelerate protons
   to 441 keV. However, an H₂⁺ ion accelerated through 0.883 MV breaks up in the target into two protons of 0.441 MeV
   each. The CN beam sheet does not list H₂⁺, so we ask for it. The proposal requests one working day of H₂⁺ and says that
   without it this day is also at 1.10 MeV.
2. **More current is not documented.** The CN beam sheet gives up to 1 µA at 0.8–2 MeV, the same as AN2000. The ~4 µA of
   the CN paper is the authorised limit of the machine, and that limit is set by neutrons. Since ⁷Li(p,n) makes no
   neutrons below 1.88 MeV, 4 µA at 1.10 MeV is a reasonable thing to ask for, but not to assume.
3. **If we got 4 µA, the reach would improve almost as if we had four times the beam time.** The fit gives
   1.08 × R(ATOMKI) after 5 days of beam with the built Cu hemisphere (2.35 × at 1 µA). For the 8-day run (46 h at
   1.10 MeV) it gives 1.7 × R(ATOMKI), against 3.8 × at 1 µA, which is below the MEG II limit (2.07 ×).
4. **The CN runs on working days, mainly in the daytime, and we have 8 days.** We assume 8 hours of beam per working day,
   so the run has 64 hours of beam, of which 46 at 1.10 MeV with the arms opposite (§4). That is about two days of beam
   instead of the five of the AN2000 plan. The expected limit with the existing holder therefore goes from 2.35 to
   **3.8 × R(ATOMKI)**, and with the lighter holder from 0.88 to 1.4 ×. The run stays a feasibility test: it measures
   the rates, the backgrounds and the cosmic rejection, which do not need the full statistics. Night running would give
   back the five days of beam, so it is the first thing to ask for.
5. **The nights become an asset.** Every night without beam the arms record cosmic rays in the geometry of the beam days,
   about 45 selected cosmic pairs per 16-hour night. This is twice the cosmic exposure of the beam hours.

## 1. The two machines, as LNL documents them

| | AN2000 | CN |
|---|---|---|
| Voltage | 0.2–2.0 MV | 0.8–5.5 MV. Below 3 MV part of the column is shorted, and returning to high voltage needs reconditioning (1–3 days) |
| Protons at 0.8–2 MeV | up to 1000 nA, all lines except 0° (20 nA); 150 nA "at small radius" | up to 1000 nA ("limited by radio-protection constraints"); the authorised machine limit is ~4 µA (CN paper) |
| Lines | one room, lines off a switching magnet | one hall, seven lines; full current on −15°, 0°, +15°; larger angles can drop to 30 % |
| Schedule | self-service, one energy change per day | "working days (Mon–Fri), mainly during daytime. Running beyond those hours requires authorisation" |
| Lithium | the LNL ⁸Be group's LiF targets (2023–24) | Mastinu's group runs metallic Li pressed on 300 µm Cu on the 0° line, air-cooled, safe to ~10 W |

Two consequences follow. First, we must ask for a small-angle line (−15°, 0° or +15°), or the current may be 0.3 µA.
Second, a four-week block at ~1 MV keeps the column shorted for a month, so the CN cannot serve high-energy users in
between. The PAC and the Accelerator Division will weigh that.

## 2. The 441 keV calibration on the CN

### 2.1 Why we want it

The 441 keV resonance populates the 17.64 MeV state, which decays by an M1 transition. ATOMKI saw no anomaly there, and
MEG II set R(17.6) < 1.8 × 10⁻⁶. The internal pairs of this transition therefore calibrate the acceptance, the
opening-angle response and the energy scale on a transition where no anomaly is expected. In the simulation one day of
beam gives 141 selected pairs from the beam and 68 cosmic pairs (`sim2arm/PREDICTIONS.md` §4).

### 2.2 H₂⁺ at 0.883 MV (the option in the proposal)

An H₂⁺ ion has charge 1 and mass 2. Accelerated through 0.883 MV it carries 0.883 MeV. In the first atomic layers of the
target it breaks up, and each proton carries half the energy, 0.441 MeV. The 11 µm film then contains the whole
resonance (the protons lose 0.29 MeV in the film, and the resonance is 12 keV wide). MEG II's 2023 beam was 25 % H₂⁺, and
that part of the beam reached the resonance in this way (EPJC 85, 763).

What we need from the CN:
- An H₂⁺ beam from the ion source. RF sources make H⁺, H₂⁺ and H₃⁺, and the analysing magnet selects one. The beam sheet
  lists only ¹H⁺, ²H⁺ and ⁴He⁺, so this is a question (ask).
- Up to 0.5 µA of H₂⁺, which is 1 µA of protons, the current of every 441 keV number. The beam power is 0.44 W.
- **The D⁺ admixture.** D⁺ has the same mass and charge as H₂⁺ (2.014 u against 2.016 u), so the analysing magnet passes
  it at the same voltage. A deuteron of 0.883 MeV on lithium makes neutrons in ⁷Li(d,n) (Q = +15 MeV). Natural hydrogen
  has 1.5 × 10⁻⁴ deuterium, so the D⁺ fraction is small. The proposal says only that we expect some D⁺ (Dylan, 25 Nov);
  its level is worth asking Pierfrancesco, but he may not know.

The proposal asks, as a question, whether the CN can provide H₂⁺, and plans one working day (8 h) with it. It states that without H₂⁺ this day is also at 1.10 MeV, and that the run then has no transition without an expected anomaly.

### 2.3 Options considered and not proposed

- **A thick lithium foil at 0.80 MeV.** Protons of 0.80 MeV slow down through 441 keV inside a foil thicker than about
  25 µm (the range at 0.80 MeV is ~35 µm). The foil then gives the full resonance yield. However, it also adds the direct
  capture between 0.44 and 0.80 MeV, which we estimate at 10–20 % of the resonance yield (an estimate, from the 1.03 MeV
  resonance tail). Since ATOMKI 2022 claims an anomaly in exactly this E1 direct capture, the calibration would no longer
  be on a transition without an expected anomaly. It also needs a second target and a target change in the glovebox.
- **The 11 µm film at 0.80 MeV.** The protons leave the film at about 0.62 MeV and never reach 441 keV. This is the
  off-resonance point of ATOMKI 2022: physics, not a calibration. It may belong in the slot-2 programme.

### 2.4 What remains without the 441 keV point

- The energy scale comes from the energy sum of the 18.15 MeV pairs at 1.10 MeV, and from the cosmic-ray MIP peaks.
- The opening-angle response comes from the cosmic-ray tracks (pointing and straightness) and from the day with the arms
  at 90°. However, the angular shape is then tested only on a mixture of M1, E1 and external conversions.

## 3. The beam current

### 3.1 What the fit gives at 2 and 4 µA

We ran the reference fit (FEASIBILITY_SIM §19, two arms, horizontal pair, 11 µm Li, pointing + 0.6 ns TOF) at 2 and
4 µA by setting `TA_IUA` in `sim2arm/two_arm_nd.py`. Every beam component scales with the current, and the cosmic rays do
not. The central value is the geometric mean of the direct and transplant estimators, as in pass 4. "Days" are days of
beam (24 h).

| holder | liquid cells | 1 µA: days to 3σ | R90(5 d) / R(ATOMKI) | 2 µA: days | R90 | 4 µA: days | R90 |
|---|---|---|---|---|---|---|---|
| Cu hemisphere (built) | design response | 151 | 2.35 | 68 | 1.58 | 32 | **1.08** |
| Cu hemisphere (built) | as at n_TOF | 263 | 3.10 | 117 | 2.06 | 53 | 1.39 |
| Cu hemisphere (built) | none | 511 | 4.32 | 226 | 2.87 | 100 | 1.91 |
| Al ogive + Cu liner | design response | 21.1 | 0.88 | 10.0 | 0.60 | 4.8 | **0.42** |
| Al ogive + Cu liner | as at n_TOF | 38.8 | 1.19 | 17.9 | 0.81 | 8.5 | 0.56 |
| Al ogive + Cu liner | none | 78.7 | 1.70 | 37.7 | 1.17 | 18.2 | 0.81 |

MEG II's limit is 2.07 × R(ATOMKI). So at 4 µA the built hemisphere with working liquid cells would set a limit about
half of MEG II's in 5 days of beam, and the run would no longer be only a feasibility test.

The days fall almost as 1/I because the background in the fit is 91–94 % beam-induced at 1 µA (cosmic share: 9 % for
the hemisphere, 6 % for the Al ogive, with the liquid cells working). A hand scaling, days ∝ (I·B_beam + B_cos) / (I²(B_beam
+ B_cos)), gives 35 d and 5.1 d at 4 µA, close to the fit's 32 d and 4.8 d.

### 3.2 What else changes at 4 µA

- **Rates.** Beam legs go from 67 to ~270 Hz per arm. The DAQ plan already covers this: at 4 µA with a single-arm
  prescale of 20 the DREAM live time is 93 % (`x17_facility_search/daq_trigger/PLAN.md` §2.2).
- **Accidentals** scale as I². They go from 9 to ~140 pairs per day before cuts, and stay negligible in the window.
- **The 478 keV line** goes to ~4 × 10⁷ γ/s: ~4× the Micromegas singles (a few kHz → ~10–20 kHz) and ~3 µSv/h at 1 m
  (`GAMMA_478_ESTIMATE.md`, scaled).
- **Heat.** 4.4 W in the target. Mastinu's air-cooled Cu cup holds ~10 °C per W, so the film would sit about 45 °C above
  room temperature, well below the 180 °C at which lithium melts (estimate; the hemisphere is not the same cup).
- **Film wear.** Four times the charge per day on the same spot. The daily γ-yield check measures it.

### 3.3 Combined with working hours

At 8 hours of beam per working day, 4 µA gives 32 µA·h per working day, against 24 µA·h for a 24-hour day at 1 µA. So
4 µA on working hours would recover more than the beam lost to the night. For the 8-day run (46 h at 1.10 MeV, central
fit at 4 µA: 31.9 days to 3σ) the expected limit would be 1.7 × R(ATOMKI) with the built hemisphere, and about 0.7 ×
with the Al ogive (4.8 days to 3σ).

## 4. Working hours and the request: 8 working days

The allocation is 8 days (Dylan, 25 Nov). The proposal assumes 8 hours of beam per working day (ask). One day of beam
(24 h) therefore takes three working days.

| working day | E_p | what | hours at 1.10 MeV (opposite arms) |
|---|---|---|---|
| 1 | 1.10 MeV | current scan (~2 h), then the 18.15 MeV region | 6 |
| 2 | 0.441 MeV (H₂⁺) | 17.64 MeV calibration: 46 beam + 23 cosmic pairs, the rate to ~18 % | 0 (8 if no H₂⁺) |
| 3–7 | 1.10 MeV | 18.15 MeV region | 40 |
| 8 | 1.10 MeV | arms at 90° (~500 pairs): external conversions | 0 |
| nights | — | cosmics, physics geometry, ~45 selected pairs per night | — |

The run has 46 hours at 1.10 MeV with the arms opposite (54 without H₂⁺). In 46 hours the simulation gives about 130
selected pairs from the beam (80 E1, 35 external conversions, 16 M1) and 130 cosmic pairs, so the pair rate in the
signal region is measured to about 12 %. An X17 at R(ATOMKI) would add 5 pairs.

Expected 90 % CL limit (two arms, horizontal pair, 11 µm Li; R90 ∝ 1/√hours):

| | 46 h (the request) | 54 h (no H₂⁺) | 120 h (24-hour days) |
|---|---|---|---|
| Cu hemisphere, liquid working | 3.8 × | 3.5 × | 2.35 × |
| Cu hemisphere, liquid as at n_TOF | 5.0 × | 4.6 × | 3.1 × |
| Cu hemisphere, no liquid | 7.0 × | 6.4 × | 4.3 × |
| Al ogive + Cu liner, liquid working | 1.4 × | 1.3 × | 0.88 × |
| Al ogive + Cu liner, as at n_TOF | 1.9 × | 1.8 × | 1.19 × |

We considered dropping the day with the arms at 90° to gain 8 hours at 1.10 MeV (3.8 → 3.5 ×). We kept it, because the
external conversions in the window rest on 2 simulated events (±70 %), and that day measures them at six times the rate
of the opposite pair. For a feasibility test that measurement is worth more than a 10 % better limit.

## 5. What changed in the proposal (25 Nov)

- Abstract page: "CN ACCELERATOR", 8 working days, and a beam table with protons at 1.10 MeV (7 days) and H₂⁺ at
  0.883 MV (1 day, else 1.10 MeV). Limits 3.8–7.0 × (1.4–1.9 × with the lighter holder) for the 46 h at 1.10 MeV.
- Body: the CN in §I; "days of beam" defined in §II; the H₂⁺ route and the fall-back in measurement (2); Table I in
  working days; the hours assumption and the cosmic nights in §III; the request as 8 working days; Fig. 2(b) 8 h at
  441 keV, Fig. 2(c) 46 h at 1.10 MeV, Fig. 3 "requested" at 1.9 days of beam; the numbers of (2), (3) and the
  sensitivity paragraph for 8 h and 46 h. To stay on 4 pages,
  the figures are at 92 % width and the sentence on the 15 % efficiency loss is left to the Table I caption.
- Fig. 2 and Fig. 3 labels say "days of beam".
- `planning/plan.py` (questions, risks, P2, hardware line), `two_arm_estimates.py` BEAM_PLAN, the page.

## 6. Questions (in `planning/plan.py`)

For Pierfrancesco:
1. Is 8 hours of beam per working day what the CN gives? Nights, weekends? (24-hour days: 3.8 → 2.35 × R(ATOMKI).)
2. Can the CN give more than 1 µA at 1.10 MeV, given no neutrons below 1.88 MeV? (§3: 2.35 → 1.08 × R(ATOMKI).)
3. Does the target holder fit a CN line end, and which line (−15°, 0°, +15°)?

For the Accelerator Division:
4. H₂⁺ at 0.883 MV, up to 0.5 µA, and its D⁺ content.
5. Night running at ~1 MV for the 8 days (it would give back the five days of beam).
