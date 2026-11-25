# Slot 1: the two-arm X17 feasibility study at LNL

> **2026-11-25: the machine is now the CN** (AN2000 probably not available). The request is 8 working days (the allocation) at
> 1 µA with ~8 h of beam each (day 2 with H₂⁺ for 441 keV, else 1.10 MeV): 46 h at 1.10 MeV, 3.8 × R(ATOMKI). §3 below is the old 8-day AN2000 plan; the new one is in
> `CN_BEAM.md` and `planning/two_arm_estimates.py` BEAM_PLAN.

Started 2026-11-18. The first beam request to the LNL PAC (call deadline **10 Dec 2026, 23:59 CET**, PAC 25–29 Jan 2027).
The data behind every table here is in `../planning/plan.py` and `../planning/two_arm_estimates.py`. The live page
is <https://dylan-neff.web.cern.ch/facilities/lnl-feasibility.html>.

---

## 0. Bottom line (2026-11-18; reach updated 2026-11-20: the Geant4 two-arm study with the built Cu hemisphere)

- **What we ask for:** ~8 beam days on AN2000 (CN as fallback) in the second half of 2027 (25 Nov: now 8 working days on the CN in **June or July 2027**, §5), for an *X17 feasibility study*
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
     is 2.07 ×. An ATOMKI-size signal would show at ~0.5σ. A lighter Al end piece (Al ogive + Cu liner, Geant4 run R10, 25 Nov) gives 0.88 × with the liquid working and 1.19 × as at n_TOF: the
     holder is now the decision that sets the physics reach. (The 19 Nov numbers, 0.93 / 1.19 / 1.78 ×, were for the Cu
     ogive of the 27 Oct sketch, simulated by mistake.)
- **Why it matters:** a positive PAC answer lets us build the 2-branch full detector; results back the INFN commission
  request and the full-experiment proposal (slot 2).
- **The decisions now:** machine (AN2000 for 441 keV); target and holder; ~~bring two liquid cells or not~~ (decided 20 Nov: yes, 2 × 2 cm in new cans, `LIQUID_CELLS.md`); spokesperson and
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
| DREAM | borrow | the TCM, network card, large NIM module and DAQ PC are kept for us at CEA; 4 FEUs + 32 cables come from CEA's common pool (ask); solder the TCM busy LEMO |
| SiPM walls × 2 | ready | ganged as at n_TOF: 8 channels per wall, 16 of 20 bars |
| plastics 20 × 30 × 2 cm × 4 | find PMTs | scintillators owned; PMTs went back to the lender |
| liquid cells × 2 | make (new cans) | 45 × 45 × 2 cm, one PMT each; the liquid exists, the cans are remade (PF, 20 Nov). Thicker/wider cells to study: `LIQUID_CELLS.md` |
| digitizers ~24 ch | find | 16 wall + 4 PMT (+2 LS) + trigger word; one V1742 (32 ch) covers it |
| trigger | borrow | n_TOF logic for two arms: 2 N1081B, a dual timer, 3–4 FIFOs, NIM bin, rented from the CERN pool (hopefully); LEMO cables + Ts from n_TOF (very likely) |
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
estimators. The Al ogive + Cu liner rows are its own Geant4 tables (L12 + L13, ×30; `../sim2arm/R10_AL_OGIVE.md`, 25 Nov); until 25 Nov they were §19.3 × the Cu ogive's ratio, which was optimistic by ×1.3–2.1 in days.
Horizontal pair:

| film | target | energy stack | cosmic veto | 4 arms, d to 3σ | 2 arms, d to 3σ | Z at R(ATOMKI) in 5 d | 90 % limit / R(ATOMKI) | / MEG II |
|---|---|---|---|---|---|---|---|---|
| 11 µm Li | Cu hemisphere (built) | SiPM wall + small plastics (no liquid) | MM pointing + 0.6 ns TOF | 371.8 | 510.9 (494-529) | 0.3 | 4.32 | 2.09 |
| 11 µm Li | Cu hemisphere (built) | SiPM wall + small plastics (no liquid) | MM pointing only | 323.0 | 472.0 (472-472) | 0.31 | 4.15 | 2.01 |
| 11 µm Li | Cu hemisphere (built) | + liquid as at n_TOF | MM pointing + 0.6 ns TOF | 194.5 | 262.9 (215-321) | 0.41 | 3.1 | 1.5 |
| 11 µm Li | Cu hemisphere (built) | + liquid as at n_TOF | MM pointing only | 174.5 | 226.4 (182-282) | 0.45 | 2.87 | 1.39 |
| 11 µm Li | Cu hemisphere (built) | + liquid working | MM pointing + 0.6 ns TOF | 147.6 | 151.0 (120-189) | 0.55 | 2.35 | 1.13 |
| 11 µm Li | Cu hemisphere (built) | + liquid working | MM pointing only | 135.5 | 132.3 (97-180) | 0.58 | 2.2 | 1.06 |
| 11 µm Li | Al ogive + Cu liner (lighter) | SiPM wall + small plastics (no liquid) | MM pointing + 0.6 ns TOF | 44.2 | 78.7 (61-101) | 0.76 | 1.7 | 0.82 |
| 11 µm Li | Al ogive + Cu liner (lighter) | SiPM wall + small plastics (no liquid) | MM pointing only | 49.1 | 75.9 (56-102) | 0.77 | 1.66 | 0.8 |
| 11 µm Li | Al ogive + Cu liner (lighter) | + liquid as at n_TOF | MM pointing + 0.6 ns TOF | 22.6 | 38.8 (33-45) | 1.08 | 1.19 | 0.57 |
| 11 µm Li | Al ogive + Cu liner (lighter) | + liquid as at n_TOF | MM pointing only | 21.3 | 36.9 (30-45) | 1.1 | 1.16 | 0.56 |
| 11 µm Li | Al ogive + Cu liner (lighter) | + liquid working | MM pointing + 0.6 ns TOF | 11.6 | 21.1 (20-22) | 1.46 | 0.88 | 0.42 |
| 11 µm Li | Al ogive + Cu liner (lighter) | + liquid working | MM pointing only | 10.1 | 18.7 (19-19) | 1.55 | 0.83 | 0.4 |
| 20 µm Li | Cu hemisphere (built) | SiPM wall + small plastics (no liquid) | MM pointing + 0.6 ns TOF | 217.4 | 293.0 (277-310) | 0.39 | 3.27 | 1.58 |
| 20 µm Li | Cu hemisphere (built) | SiPM wall + small plastics (no liquid) | MM pointing only | 186.4 | 259.5 (257-262) | 0.42 | 3.08 | 1.49 |
| 20 µm Li | Cu hemisphere (built) | + liquid as at n_TOF | MM pointing + 0.6 ns TOF | 103.3 | 150.8 (128-178) | 0.55 | 2.35 | 1.13 |
| 20 µm Li | Cu hemisphere (built) | + liquid as at n_TOF | MM pointing only | 94.1 | 130.2 (106-160) | 0.59 | 2.18 | 1.05 |
| 20 µm Li | Cu hemisphere (built) | + liquid working | MM pointing + 0.6 ns TOF | 82.6 | 86.5 (68-110) | 0.72 | 1.78 | 0.86 |
| 20 µm Li | Cu hemisphere (built) | + liquid working | MM pointing only | 78.6 | 77.6 (57-106) | 0.76 | 1.68 | 0.81 |
| 20 µm Li | Al ogive + Cu liner (lighter) | SiPM wall + small plastics (no liquid) | MM pointing + 0.6 ns TOF | 31.2 | 53.3 (41-70) | 0.92 | 1.4 | 0.67 |
| 20 µm Li | Al ogive + Cu liner (lighter) | SiPM wall + small plastics (no liquid) | MM pointing only | 34.2 | 51.2 (37-70) | 0.94 | 1.37 | 0.66 |
| 20 µm Li | Al ogive + Cu liner (lighter) | + liquid as at n_TOF | MM pointing + 0.6 ns TOF | 13.1 | 24.4 (21-28) | 1.36 | 0.94 | 0.46 |
| 20 µm Li | Al ogive + Cu liner (lighter) | + liquid as at n_TOF | MM pointing only | 13.1 | 23.7 (20-28) | 1.38 | 0.93 | 0.45 |
| 20 µm Li | Al ogive + Cu liner (lighter) | + liquid working | MM pointing + 0.6 ns TOF | 6.9 | 13.5 (13-14) | 1.83 | 0.7 | 0.34 |
| 20 µm Li | Al ogive + Cu liner (lighter) | + liquid working | MM pointing only | 6.2 | 12.0 (12-12) | 1.94 | 0.66 | 0.32 |

- Not a discovery run: an ATOMKI-size signal shows at 1–1.5σ with the liquid cells. Quote the limit column as "sensitivity".
- The liquid cells are the biggest lever (×3.4 in days with the hemisphere); the proposal assumes them (20 Nov). The 10–12 µm film (LiOH) costs ×1.3 against 20 µm.
- The 0.3 ns arm-to-arm TOF is not measured; the horizontal pair does not need it (pointing only gives the same days).
- 441 keV: ~140 selected pairs per day above 90° (two arms, E_sum window, built Cu hemisphere), ~1,600 without the E_sum cut (the Cu ogive gave ~600 / ~3,000).

## 5. Timeline

| when | what |
|---|---|
| 18 Nov – 9 Dec 2026 | proposal (§6); submit 9 Dec |
| ~18 Jan 2027 | technical-review feedback |
| 25–29 Jan 2027 | PAC (12 + 8 min talk) |
| Feb – Mar 2027 | B repaired (new windows if funded); DREAM loan agreed; PMTs, digitizers, trigger modules found; target holder designed |
| mid Feb – mid May 2027 | bench tests (trigger T1, T2, T4; MM + DREAM on cosmics from April; walls + plastics on cosmics) |
| **14 May 2027** | **go/no-go: both arms work on cosmics** |
| 17 May – 11 Jun 2027 | full chain, two arms, on cosmics; Li film conversion test on the line (by end of May) |
| 14 Jun – 2 Jul 2027 | ship, install, commission at LNL (≥ 3 vertical cosmic nights) |
| ~5 – 14 Jul 2027 | 8 beam days (the call's period ends **30 Jul 2027**) |
| Jul – Sep 2027 | results note; INFN commission request; full-experiment proposal to the next PAC |

Changed 25 Nov 2026. The January call allocates beam from 20 Feb to 30 Jul 2027 (call page; it prints 2026, a typo), and
Pierfrancesco confirmed on 25 Nov that the PAC schedules only up to July. The "second half of 2027" of 18 Nov is therefore outside
the period, and we aim for June or July. The beam dates are still a plan, not an allocation. This leaves about five months
from the PAC to the beam, so the loans (B's window, DREAM, PMTs, digitizers) must be asked in December and January. If the
go/no-go of 14 May fails, we ask LNL to move the 8 days to the next period (autumn 2027, after the August closure).

## 6. The proposal, task by task (to 10 Dec)

See `../proposal/STRUCTURE.md` for the rules, `../proposal/latex/` for the draft. The tasks P1–P11 in `plan.py`:
outline to Pierfrancesco (20 Nov), INFN-AAI account (23 Nov), co-proponents (24 Nov), draft v1 (27 Nov), to Pierfrancesco
(30 Nov), co-proponents (3 Dec), the LNL ⁸Be group (4 Dec), freeze + online forms (8 Dec), submit (9 Dec).

## 7. Budget

For our planning, not the proposal. Tiers (Dylan, 18 Nov 2026; new drift windows moved to the low tier 19 Nov; `plan.py` `TIERS`, `BUDGET`), central values.
Updated 25 Nov 2026 with the loans below.
- **Critical for the test, €7.8k**: repair of B's drift window €0.3k, gas premix + regulators + panel €3k, new cans for the 2
  liquid cells €1.5k, the CERN electronics-pool rental fee €1k (a guess), shipping €2k. The cables, Ts and adapters come from n_TOF.
  B runs with its existing (noisier) Italian M1 cards.
- **Low-budget upgrade, +€5.2k**: 50 Ω resistive splitters for the wall channels instead of Ts €0.8k, new aluminised-mylar drift windows for A and B €1.25k, low-permeation gas lines €0.4k, gas and environment sensors (slow control Tier 1) €2.5k, switched
  PDU (remote power switch) €0.3k.
- **High-budget upgrade, +€8k** (toward the final measurement): 4 CERN M1 cards for B.

**Loans and how sure we are of them (25 Nov 2026).** Each loan carries a confidence in `plan.py` (`conf`), shown on the
page's Hardware tab.
- **n_TOF's LEMO cables and Ts: very likely**, if we return them. n_TOF has about 60 cables of 16 ns, 60 of 5 ns, 20 of 2 ns,
  20 of 1 ns, and about 30 LEMO Ts (Dylan's estimate). This agrees with the n_TOF set-up, which used ~150 LEMO connections
  for four arms (`nTof_x17_DAQ/n1081b/n1081b_module_map.py` and the budget item `splitters`). The two arms need about 110
  cables, 20 Ts and ~20 adapters. The Ts also split the wall channels, as at n_TOF. For this reason the €3.8k line for
  splitters, cables and adapters leaves the critical tier; matched splitters become a low-budget upgrade.
- **The NIM modules and the DREAM LV supply: hopefully rented from the CERN electronics pool** and taken to LNL. These are
  2 N1081B, the N93B dual timer, 3–4 linear FIFOs, a NIM bin and the Wiener PL512 that powered DREAM at n_TOF. The fee,
  and whether the pool lets modules leave CERN, are questions to the pool.
- **At CEA Saclay (Dylan, 25 Nov):** the five Micromegas A–E, 4 good and 20 bad M1 cards, 4 M4 cards, 16 M2 cards, the DAQ PC
  and the DREAM core (1 TCM, 1 network card, 1 large NIM module) are kept for us. The FEUs and their cables went back into
  CEA's common pool, so we must ask for 4 FEUs and 32 cables.

Only if a loan falls through (+€62k in all): a V1742 €9.5k, 2 N1081B €14k, 3 linear FIFOs €6.9k, a NIM bin €5.1k, a VME
crate €4.8k, an N93B €2.7k, an LV supply €1.9k, the LEMO cables, Ts and adapters €5k, PMTs €6–24k. Prices from the CAEN offer
26OFC.01101 and `x17_facility_search/budget/items.py`. The hardware facts (owner, location, condition) are in the central
inventory, `x17_facility_search/inventory/INVENTORY.md`.

## 8. Risks

In `plan.py` `RISKS` and on the page. The three that would stop the run: B or DREAM not ready (ask CEA now), the AN2000
room or line not free (talk to the LNL ⁸Be group), the proposal over-selling the reach (frame it as feasibility).

## 9. Open questions

In `plan.py` `QUESTIONS`, by who answers: Pierfrancesco (spokesperson, GLIMOS, machine, target, commission calendar,
authors), the Accelerator Division (line, floor, 24 h running, flammable gas), CEA, CAEN, the LNL ⁸Be group, the plastics lender.
