# Slot 1: the two-arm X17 feasibility study at LNL

Started 2026-11-18. The first beam request to the LNL PAC (call deadline **10 Dec 2026, 23:59 CET**, PAC 25–29 Jan 2027).
The data behind every table here is in `../planning/plan.py` and `../planning/two_arm_estimates.py`. The live page
is <https://dylan-neff.web.cern.ch/facilities/lnl-feasibility.html>.

---

## 0. Bottom line (2026-11-18; reach and plan updated 2026-11-19 from the Geant4 two-arm study)

- **What we ask for:** ~8 beam days on AN2000 (CN as fallback) in the second half of 2027, for an *X17 feasibility study*
  with two arms of the n_TOF MX17 apparatus around a ⁷Li target. Pierfrancesco's framing, 18 Nov: a feasibility study of
  the X17 experiment rather than a detector test, 8 days, measurement in H2 2027. He handles the informal contact with LNL.
- **Set-up:** the two best Micromegas (A ready; B needs a drift-window repair, by Stephan at CEA; new windows are optional), two SiPM walls, the
  four small 20 × 30 × 2 cm plastics with PMTs we have to find, ~24 digitizer channels, half the DREAM system from CEA.
  Everything is owned or borrowed. Cash critical for the test: **~€9k**; +€4.4k low-budget upgrade, +€8k high-budget upgrade; up to €43k more if loans fall through (§7).
- **What it proves:**
  1. the apparatus works on a proton beam: rates, live time, Micromegas occupancy, Li target;
  2. a **calibration at the 441 keV resonance** (17.64 MeV M1 pairs, no anomaly expected): ~600 selected pairs per day
     above 90° with two arms (Geant4; not the 6–12k of the first estimate), so one day;
  3. the **backgrounds measured**: cosmic nights with the arms **vertical** before the beam (the MEG II 2026 140° peak at
     full strength, every veto, the arm-to-arm time of flight), beam-induced singles, accidentals, external conversions;
  4. a first look at the 18.15 MeV pairs. **Geant4, two arms (`../sim2arm/TWO_ARM_STUDY.md`):** 5 days at 1.10 MeV,
     11 µm Li, horizontal pair: expected 90 % CL limit **0.93 × R(ATOMKI)** with the liquid cells working, **1.19 ×** as they
     ran at n_TOF, **1.78 ×** without them; MEG II's limit is 2.07 ×. An ATOMKI-size signal would show at 0.7–1.4σ: a limit,
     not a test of the claim at 3σ.
- **Why it matters:** a positive PAC answer lets us build the 2-branch full detector; results back the INFN commission
  request and the full-experiment proposal (slot 2).
- **The decisions now:** machine (AN2000 for 441 keV); target and holder; bring two liquid cells or not; spokesperson and
  GLIMOS; author list.

## 1. Pierfrancesco's guidance (e-mail, 18 Nov 2026)

- The PAC probably covers the next ~6 months; submit anyway and say we want to measure in the second half of the year.
- Ask for a **feasibility study of the X17 experiment**, not beam time for detector tests. ~8 days are due and obtainable.
- A feasibility result helps convince the collaboration and supports an economic request to "commission II" (ask which
  INFN commission and its calendar).
- After a positive PAC answer, start arranging a 2-branch full detector.
- Co-proponents to involve: Massimi, Mengoni, Gervino, Gustavino, Cosentino.
- On Dylan's set-up list: the TPCs "Stephan must fix them"; the SiPM walls are available; the scintillators exist and the
  PMTs can be found; 10–20 digitizer channels can be found, more must be borrowed, maybe a test at CAEN.

## 2. Set-up

| part | status | note |
|---|---|---|
| Micromegas A (det3) | ready | 92.9 % within 5 mm on the bench; runs as is; a new aluminised-mylar window is optional (low-budget upgrade) |
| Micromegas B (det2) | fix | 91.3 %; drift-window repair (Stephan, CEA), new window optional; runs with its existing Italian M1 cards (new CERN cards: high-budget upgrade) |
| DREAM | borrow | 4 FEUs + TCM + 32 cables from CEA; solder the TCM busy LEMO |
| SiPM walls × 2 | ready | ganged as at n_TOF: 8 channels per wall, 16 of 20 bars |
| plastics 20 × 30 × 2 cm × 4 | find PMTs | scintillators owned; PMTs went back to the lender |
| liquid cells × 2 | decide | 45 × 45 cm, one PMT each; 67–76 % pile-up at n_TOF from the γ-flash; LNL rates are far lower |
| digitizers ~24 ch | find | 16 wall + 4 PMT (+2 LS) + trigger word; one V1742 (32 ch) covers it |
| trigger | borrow | n_TOF logic for two arms: 2–3 N1081B, a dual timer, FIFOs, NIM bin |
| gas | buy | Ar/iC₄H₁₀ 95/5 premix and panel; flammable-gas rules at LNL (ask) |
| target | decide | LNL's pressed Li on Cu, 10–12 µm; holder: most likely the Cu hemisphere, already built (the 'Cu ogive' rows in §4; Dylan, 19 Nov); flat Al end cap at 45° the lighter alternative |

**Geometry (Geant4, 19 Nov, `../sim2arm/TWO_ARM_STUDY.md`).** The two arms face each other across the beam (faces at
±204 mm). Opposite arms keep 38 % of the four-arm X17 pairs per pair; adjacent arms see 25–120° and no X17; turning the
arms toward 140° costs ×1.1–2.5 in days. **Vertical** (top + bottom) for the cosmic nights before the beam: ~1.6 × 10⁵
cosmic coincidences a day, the hard test of the veto. **Horizontal** for the beam days: ~26× fewer cosmic coincidences,
and the reach holds with track pointing alone (the vertical pair needs a ≤ 0.4 ns time of flight to match it). The stand
should roll 90° about the beam.

**Channels.** 16 SiPM-wall + 4 plastic PMT (+2 liquid) + 2–3 trigger word + spares ≈ 24. This is the "10–20 channels"
Pierfrancesco can find, plus a few.

## 3. Beam request (8 days)

| day | E_p | what |
|---|---|---|
| before | — | installation nights, arms vertical: cosmic veto test, time of flight, MIP gains (≥ 3 nights) |
| 1 | 1.10 MeV | roll to horizontal; target conditioning; current scan 0.05 → 1 µA (rates, live time, occupancy) |
| 2 | 0.441 MeV | locate the resonance; 17.64 MeV IPC calibration (~600 pairs/day above 90°: rate, θ shape, energy scale) |
| 3–7 | 1.10 MeV | 18.15 MeV region (the X17 data); daily γ-yield check of the target |
| 8 | 1.10 MeV | ½ day with the arms adjacent (external conversions, small-angle IPC); contingency |
| beam off | — | cosmics in the physics geometry |

- AN2000 "self-service": one energy change per day, which fits the plan (three energies).
- 1 µA is the documented proton current at 0.8–2 MeV on both machines (and on AN2000 except the 0° line).
- **The CN cannot do day 2:** its range starts at 0.8 MV. On the CN the plan becomes 1.03/1.10 MeV only, and the
  calibration moves to the γ₁/γ₀ ratio and cosmics.

## 4. What 8 days can show (Geant4 two-arm study, 2026-11-19)

`../sim2arm/TWO_ARM_STUDY.md` (method, all geometries and vetoes) → `../planning/two_arm_estimates.py` →
`../planning/out/two_arm_reach.csv`. The FEASIBILITY_SIM §19 reference fit (θ × |y| × E_sum, background shape floating)
on one pair of arms of the Cu-hemisphere Geant4 tables (L11 + L13), cosmics from every zenith angle (L15, 10 live days),
1 µA, 1.10 MeV. Range: the two MC-safe estimators. The Al ogive has no two-arm simulation: its rows are §19.3 × the Cu
hemisphere's simulated ratio (estimate). Horizontal pair:

| film | target | energy stack | cosmic veto | 4 arms, d to 3σ | 2 arms, d to 3σ | Z at R(ATOMKI) in 5 d | 90 % limit / R(ATOMKI) | / MEG II |
|---|---|---|---|---|---|---|---|---|
| 11 µm Li | Cu hemisphere (built) | SiPM wall + small plastics (no liquid) | MM pointing + 0.3 ns TOF | 58.7 | 86.9 (54-139) | 0.72 | 1.78 | 0.86 |
| 11 µm Li | Cu hemisphere (built) | SiPM wall + small plastics (no liquid) | MM pointing only | 67.5 | 92.3 (60-143) | 0.7 | 1.84 | 0.89 |
| 11 µm Li | Cu hemisphere (built) | + liquid as at n_TOF | MM pointing + 0.3 ns TOF | 19.3 | 38.9 (28-54) | 1.08 | 1.19 | 0.58 |
| 11 µm Li | Cu hemisphere (built) | + liquid as at n_TOF | MM pointing only | 23.3 | 38.2 (30-49) | 1.09 | 1.18 | 0.57 |
| 11 µm Li | Cu hemisphere (built) | + liquid working | MM pointing + 0.3 ns TOF | 10.6 | 23.6 (23-24) | 1.38 | 0.93 | 0.45 |
| 11 µm Li | Cu hemisphere (built) | + liquid working | MM pointing only | 13.5 | 22.9 (22-24) | 1.4 | 0.91 | 0.44 |
| 11 µm Li | Al ogive + Cu liner (lighter) | SiPM wall + small plastics (no liquid) | MM pointing + 0.3 ns TOF | 41.4 | 61.3 (35-106) | 0.86 | 1.5 | 0.72 |
| 11 µm Li | Al ogive + Cu liner (lighter) | SiPM wall + small plastics (no liquid) | MM pointing only | 41.4 | 65.1 (39-109) | 0.83 | 1.54 | 0.74 |
| 11 µm Li | Al ogive + Cu liner (lighter) | + liquid as at n_TOF | MM pointing + 0.3 ns TOF | 11.2 | 22.6 (14-37) | 1.41 | 0.91 | 0.44 |
| 11 µm Li | Al ogive + Cu liner (lighter) | + liquid as at n_TOF | MM pointing only | 11.2 | 22.2 (14-34) | 1.42 | 0.9 | 0.43 |
| 11 µm Li | Al ogive + Cu liner (lighter) | + liquid working | MM pointing + 0.3 ns TOF | 5.8 | 12.8 (10-16) | 1.87 | 0.68 | 0.33 |
| 11 µm Li | Al ogive + Cu liner (lighter) | + liquid working | MM pointing only | 5.8 | 12.5 (10-16) | 1.9 | 0.67 | 0.33 |
| 20 µm Li | Cu hemisphere (built) | SiPM wall + small plastics (no liquid) | MM pointing + 0.3 ns TOF | 43.2 | 70.1 (42-118) | 0.8 | 1.6 | 0.77 |
| 20 µm Li | Cu hemisphere (built) | SiPM wall + small plastics (no liquid) | MM pointing only | 48.1 | 65.5 (43-100) | 0.83 | 1.55 | 0.75 |
| 20 µm Li | Cu hemisphere (built) | + liquid as at n_TOF | MM pointing + 0.3 ns TOF | 14.6 | 29.9 (22-42) | 1.23 | 1.05 | 0.51 |
| 20 µm Li | Cu hemisphere (built) | + liquid as at n_TOF | MM pointing only | 16.1 | 27.9 (22-36) | 1.27 | 1.01 | 0.49 |
| 20 µm Li | Cu hemisphere (built) | + liquid working | MM pointing + 0.3 ns TOF | 8.3 | 17.9 (18-18) | 1.59 | 0.81 | 0.39 |
| 20 µm Li | Cu hemisphere (built) | + liquid working | MM pointing only | 9.8 | 16.9 (16-17) | 1.63 | 0.79 | 0.38 |
| 20 µm Li | Al ogive + Cu liner (lighter) | SiPM wall + small plastics (no liquid) | MM pointing + 0.3 ns TOF | 30.5 | 49.4 (27-90) | 0.95 | 1.34 | 0.65 |
| 20 µm Li | Al ogive + Cu liner (lighter) | SiPM wall + small plastics (no liquid) | MM pointing only | 30.5 | 46.2 (28-76) | 0.99 | 1.3 | 0.63 |
| 20 µm Li | Al ogive + Cu liner (lighter) | + liquid as at n_TOF | MM pointing + 0.3 ns TOF | 8.5 | 17.4 (10-28) | 1.61 | 0.8 | 0.39 |
| 20 µm Li | Al ogive + Cu liner (lighter) | + liquid as at n_TOF | MM pointing only | 8.5 | 16.2 (10-25) | 1.67 | 0.77 | 0.37 |
| 20 µm Li | Al ogive + Cu liner (lighter) | + liquid working | MM pointing + 0.3 ns TOF | 4.5 | 9.7 (8-12) | 2.15 | 0.6 | 0.29 |
| 20 µm Li | Al ogive + Cu liner (lighter) | + liquid working | MM pointing only | 4.5 | 9.2 (7-12) | 2.21 | 0.58 | 0.28 |

- Not a discovery run: an ATOMKI-size signal shows at 1–1.5σ with the liquid cells. Quote the limit column as "sensitivity".
- The liquid cells are the biggest lever (×2–4 in days). The 10–12 µm film (LiOH) costs ×1.3 against 20 µm.
- The 0.3 ns arm-to-arm TOF is not measured; the horizontal pair does not need it (pointing only gives the same days).
- 441 keV: ~600 selected pairs per day above 90° (two arms, E_sum window), ~3,000 without the E_sum cut.

## 5. Timeline

| when | what |
|---|---|
| 18 Nov – 9 Dec 2026 | proposal (§6); submit 9 Dec |
| ~18 Jan 2027 | technical-review feedback |
| 25–29 Jan 2027 | PAC (12 + 8 min talk) |
| Feb – Apr 2027 | B repaired (new windows if funded); DREAM loan agreed; PMTs, digitizers, trigger modules found; target holder designed |
| Mar – Jun 2027 | bench tests (trigger T1, T2, T4; MM + DREAM on cosmics; walls + plastics on cosmics) |
| **15 Jun 2027** | **go/no-go: both arms work on cosmics** |
| Jun – Jul 2027 | full chain, two arms, on cosmics; Li film conversion test on the line |
| late Aug – mid Sep 2027 | ship, install, commission at LNL (LNL closes around mid-August: ask) |
| late Sep 2027 | 8 beam days |
| Oct – Nov 2027 | results note; full-experiment proposal to the next PAC |

The beam window is a plan, not a fact. If the INFN commission requests are due before autumn (F1), ask for June–July.

## 6. The proposal, task by task (to 10 Dec)

See `../proposal/STRUCTURE.md` for the rules, `../proposal/latex/` for the draft. The tasks P1–P11 in `plan.py`:
outline to Pierfrancesco (20 Nov), INFN-AAI account (23 Nov), co-proponents (24 Nov), draft v1 (27 Nov), to Pierfrancesco
(30 Nov), co-proponents (3 Dec), the LNL ⁸Be group (4 Dec), freeze + online forms (8 Dec), submit (9 Dec).

## 7. Budget

For our planning, not the proposal. Tiers (Dylan, 18 Nov 2026; new drift windows moved to the low tier 19 Nov; `plan.py` `TIERS`, `BUDGET`), central values:
- **Critical for the test, €9.1k**: repair of B's drift window €0.3k, gas premix + regulators + panel €3k, splitters / LEMO / adapters
  €3.8k, shipping €2k. B runs with its existing (noisier) Italian M1 cards.
- **Low-budget upgrade, +€4.4k**: new aluminised-mylar drift windows for A and B €1.25k, low-permeation gas lines €0.4k, gas and environment sensors (slow control Tier 1) €2.5k, switched
  PDU (remote power switch) €0.3k.
- **High-budget upgrade, +€8k** (toward the final measurement): 4 CERN M1 cards for B.

Only if a loan falls through: a V1742 €9.5k,
2 N1081B €14k, a VME crate €4.8k, an N93B €2.7k, PMTs €6–24k. Prices from the CAEN offer 26OFC.01101 and
`x17_facility_search/budget/items.py`.

## 8. Risks

In `plan.py` `RISKS` and on the page. The three that would stop the run: B or DREAM not ready (ask CEA now), the AN2000
room or line not free (talk to the LNL ⁸Be group), the proposal over-selling the reach (frame it as feasibility).

## 9. Open questions

In `plan.py` `QUESTIONS`, by who answers: Pierfrancesco (spokesperson, GLIMOS, machine, target, commission calendar,
authors), the Accelerator Division (line, floor, 24 h running, flammable gas), CEA, CAEN, the LNL ⁸Be group, the plastics lender.
