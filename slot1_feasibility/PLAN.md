# Slot 1: the two-arm X17 feasibility study at LNL

Started 2026-11-18. The first beam request to the LNL PAC (call deadline **10 Dec 2026, 23:59 CET**, PAC 25–29 Jan 2027).
The data behind every table here is in `../planning/plan.py` and `../planning/two_arm_estimates.py`. The live page
is <https://dylan-neff.web.cern.ch/facilities/lnl-feasibility.html>.

---

## 0. Bottom line (2026-11-18; reach updated 2026-11-20: the Geant4 two-arm study with the built Cu hemisphere)

- **What we ask for:** ~8 beam days on AN2000 (CN as fallback) in the second half of 2027, for an *X17 feasibility study*
  with two arms of the n_TOF MX17 apparatus around a ⁷Li target. Pierfrancesco's framing, 18 Nov: a feasibility study of
  the X17 experiment rather than a detector test, 8 days, measurement in H2 2027. He handles the informal contact with LNL.
- **Set-up:** the two best Micromegas (A ready; B needs a drift-window repair, by Stephan at CEA; new windows are optional), two SiPM walls, the
  four small 20 × 30 × 2 cm plastics with PMTs we have to find, ~24 digitizer channels, half the DREAM system from CEA.
  Everything is owned or borrowed. Cash critical for the test: **~€9k**; +€4.4k low-budget upgrade, +€8k high-budget upgrade; up to €43k more if loans fall through (§7).
- **What it proves:**
  1. the apparatus works on a proton beam: rates, live time, Micromegas occupancy, Li target;
  2. a **calibration at the 441 keV resonance** (17.64 MeV M1 pairs, no anomaly expected): ~140 selected pairs per day
     above 90° with two arms and the built Cu hemisphere (Geant4), the rate to ~8 % in one day;
  3. the **backgrounds measured**: cosmic nights with the arms **vertical** before the beam (the MEG II 2026 140° peak at
     full strength, every veto, the arm-to-arm time of flight), beam-induced singles, accidentals, external conversions;
  4. a first look at the 18.15 MeV pairs. **Geant4, two arms (`../sim2arm/TWO_ARM_STUDY.md`):** 5 days at 1.10 MeV,
     11 µm Li, horizontal pair, **the built Cu hemisphere** (R 11 mm, 300 µm; run L18): expected 90 % CL limit
     **2.35 × R(ATOMKI)** with the liquid cells working, **3.10 ×** as they ran at n_TOF, **4.32 ×** without them; MEG II's limit
     is 2.07 ×. An ATOMKI-size signal would show at ~0.5σ. A lighter Al end piece would give ~0.6–0.8 × (estimate): the
     holder is now the decision that sets the physics reach. (The 19 Nov numbers, 0.93 / 1.19 / 1.78 ×, were for the Cu
     ogive of the 27 Oct sketch, simulated by mistake.)
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
| target | decide | LNL's pressed Li on Cu, 10–12 µm; holder: the Cu hemisphere, already built (R 11 mm, 300 µm; the 'Cu hemisphere' rows of §4 since 20 Nov); a lighter Al end piece (Al ogive + Cu liner, or a flat 45° Al cap) would cut the days ×6–15: ask PF whether one can be made |

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
on one pair of arms of the built Cu hemisphere's Geant4 tables (R 11 mm, 300 µm: L10 + L18; until 20 Nov the Cu ogive's
L11 + L13 by mistake), cosmics from every zenith angle (L15, 10 live days), 1 µA, 1.10 MeV. Range: the two MC-safe
estimators. The Al ogive has no two-arm simulation: its rows are §19.3 × the Cu ogive's simulated ratio (estimate).
Horizontal pair:

| film | target | energy stack | cosmic veto | 4 arms, d to 3σ | 2 arms, d to 3σ | Z at R(ATOMKI) in 5 d | 90 % limit / R(ATOMKI) | / MEG II |
|---|---|---|---|---|---|---|---|---|
| 11 µm Li | Cu hemisphere (built) | SiPM wall + small plastics (no liquid) | MM pointing + 0.6 ns TOF | 371.8 | 510.9 (494-529) | 0.3 | 4.32 | 2.09 |
| 11 µm Li | Cu hemisphere (built) | SiPM wall + small plastics (no liquid) | MM pointing only | 323.0 | 472.0 (472-472) | 0.31 | 4.15 | 2.01 |
| 11 µm Li | Cu hemisphere (built) | + liquid as at n_TOF | MM pointing + 0.6 ns TOF | 194.5 | 262.9 (215-321) | 0.41 | 3.1 | 1.5 |
| 11 µm Li | Cu hemisphere (built) | + liquid as at n_TOF | MM pointing only | 174.5 | 226.4 (182-282) | 0.45 | 2.87 | 1.39 |
| 11 µm Li | Cu hemisphere (built) | + liquid working | MM pointing + 0.6 ns TOF | 147.6 | 151.0 (120-189) | 0.55 | 2.35 | 1.13 |
| 11 µm Li | Cu hemisphere (built) | + liquid working | MM pointing only | 135.5 | 132.3 (97-180) | 0.58 | 2.2 | 1.06 |
| 11 µm Li | Al ogive + Cu liner (lighter) | SiPM wall + small plastics (no liquid) | MM pointing + 0.6 ns TOF | 42.3 | 58.8 (34-100) | 0.87 | 1.46 | 0.71 |
| 11 µm Li | Al ogive + Cu liner (lighter) | SiPM wall + small plastics (no liquid) | MM pointing only | 42.3 | 57.8 (34-97) | 0.88 | 1.45 | 0.7 |
| 11 µm Li | Al ogive + Cu liner (lighter) | + liquid as at n_TOF | MM pointing + 0.6 ns TOF | 12.4 | 18.2 (11-30) | 1.57 | 0.81 | 0.39 |
| 11 µm Li | Al ogive + Cu liner (lighter) | + liquid as at n_TOF | MM pointing only | 12.4 | 15.9 (10-24) | 1.68 | 0.76 | 0.37 |
| 11 µm Li | Al ogive + Cu liner (lighter) | + liquid working | MM pointing + 0.6 ns TOF | 6.3 | 10.4 (8-13) | 2.08 | 0.62 | 0.3 |
| 11 µm Li | Al ogive + Cu liner (lighter) | + liquid working | MM pointing only | 6.3 | 9.4 (7-12) | 2.18 | 0.59 | 0.28 |
| 20 µm Li | Cu hemisphere (built) | SiPM wall + small plastics (no liquid) | MM pointing + 0.6 ns TOF | 217.4 | 293.0 (277-310) | 0.39 | 3.27 | 1.58 |
| 20 µm Li | Cu hemisphere (built) | SiPM wall + small plastics (no liquid) | MM pointing only | 186.4 | 259.5 (257-262) | 0.42 | 3.08 | 1.49 |
| 20 µm Li | Cu hemisphere (built) | + liquid as at n_TOF | MM pointing + 0.6 ns TOF | 103.3 | 150.8 (128-178) | 0.55 | 2.35 | 1.13 |
| 20 µm Li | Cu hemisphere (built) | + liquid as at n_TOF | MM pointing only | 94.1 | 130.2 (106-160) | 0.59 | 2.18 | 1.05 |
| 20 µm Li | Cu hemisphere (built) | + liquid working | MM pointing + 0.6 ns TOF | 82.6 | 86.5 (68-110) | 0.72 | 1.78 | 0.86 |
| 20 µm Li | Cu hemisphere (built) | + liquid working | MM pointing only | 78.6 | 77.6 (57-106) | 0.76 | 1.68 | 0.81 |
| 20 µm Li | Al ogive + Cu liner (lighter) | SiPM wall + small plastics (no liquid) | MM pointing + 0.6 ns TOF | 30.5 | 43.1 (25-73) | 1.02 | 1.25 | 0.61 |
| 20 µm Li | Al ogive + Cu liner (lighter) | SiPM wall + small plastics (no liquid) | MM pointing only | 30.5 | 41.0 (25-68) | 1.05 | 1.22 | 0.59 |
| 20 µm Li | Al ogive + Cu liner (lighter) | + liquid as at n_TOF | MM pointing + 0.6 ns TOF | 8.5 | 13.5 (8-23) | 1.83 | 0.7 | 0.34 |
| 20 µm Li | Al ogive + Cu liner (lighter) | + liquid as at n_TOF | MM pointing only | 8.5 | 11.6 (7-18) | 1.97 | 0.65 | 0.32 |
| 20 µm Li | Al ogive + Cu liner (lighter) | + liquid working | MM pointing + 0.6 ns TOF | 4.5 | 7.5 (6-9) | 2.45 | 0.52 | 0.25 |
| 20 µm Li | Al ogive + Cu liner (lighter) | + liquid working | MM pointing only | 4.5 | 7.0 (5-9) | 2.54 | 0.5 | 0.24 |

- Not a discovery run: an ATOMKI-size signal shows at 1–1.5σ with the liquid cells. Quote the limit column as "sensitivity".
- The liquid cells are the biggest lever (×2–4 in days). The 10–12 µm film (LiOH) costs ×1.3 against 20 µm.
- The 0.3 ns arm-to-arm TOF is not measured; the horizontal pair does not need it (pointing only gives the same days).
- 441 keV: ~140 selected pairs per day above 90° (two arms, E_sum window, built Cu hemisphere), ~1,600 without the E_sum cut (the Cu ogive gave ~600 / ~3,000).

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
