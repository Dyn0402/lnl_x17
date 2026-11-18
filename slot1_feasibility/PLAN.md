# Slot 1: the two-arm X17 feasibility study at LNL

Started 2026-11-18. The first beam request to the LNL PAC (call deadline **10 Dec 2026, 23:59 CET**, PAC 25–29 Jan 2027).
The data behind every table here is in `../planning/plan.py` and `../planning/two_arm_estimates.py`. The live page
is <https://dylan-neff.web.cern.ch/facilities/lnl-feasibility.html>.

---

## 0. Bottom line (2026-11-18)

- **What we ask for:** ~8 beam days on AN2000 (CN as fallback) in the second half of 2027, for an *X17 feasibility study*
  with two arms of the n_TOF MX17 apparatus around a ⁷Li target. Pierfrancesco's framing, 18 Nov: a feasibility study of
  the X17 experiment rather than a detector test, 8 days, measurement in H2 2027. He handles the informal contact with LNL.
- **Set-up:** the two best Micromegas (A ready; B needs a drift fix and a window, by Stephan at CEA), two SiPM walls, the
  four small 20 × 30 × 2 cm plastics with PMTs we have to find, ~24 digitizer channels, half the DREAM system from CEA.
  Everything is owned or borrowed. Cash needed: **~€22k** (€15–30k), plus up to €43k of contingencies if loans fall through.
- **What it proves:**
  1. the apparatus works on a proton beam: rates, live time, Micromegas occupancy, Li target;
  2. a **calibration at the 441 keV resonance** (17.64 MeV M1 pairs, no anomaly expected): 12–24k selected pairs in 2 days;
  3. the **backgrounds measured**: cosmics with beam off, with and without the track-based veto (the MEG II 2026 point
     about ATOMKI-type spectrometers), beam-induced singles and accidentals;
  4. a first look at the 18.15 MeV pairs. **Scaling estimate (not simulated):** 5 days at 1.10 MeV give an expected 90 % CL
     limit of 1.5–1.8 × R(ATOMKI) with the SiPM walls and small plastics alone, already near MEG II's 1.2×10⁻⁵. With two
     liquid cells, even as they ran at n_TOF, it is 0.8–0.9 × R(ATOMKI): the feasibility run could test the ATOMKI claim.
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
| Micromegas A (det3) | ready | 92.9 % within 5 mm on the bench; new aluminised-mylar window only |
| Micromegas B (det2) | fix | 91.3 %; drift fix + window (Stephan, CEA); 4 new CERN M1 cards to replace the noisy Italian ones |
| DREAM | borrow | 4 FEUs + TCM + 32 cables from CEA; solder the TCM busy LEMO |
| SiPM walls × 2 | ready | ganged as at n_TOF: 8 channels per wall, 16 of 20 bars |
| plastics 20 × 30 × 2 cm × 4 | find PMTs | scintillators owned; PMTs went back to the lender |
| liquid cells × 2 | decide | 45 × 45 cm, one PMT each; 67–76 % pile-up at n_TOF from the γ-flash; LNL rates are far lower |
| digitizers ~24 ch | find | 16 wall + 4 PMT (+2 LS) + trigger word; one V1742 (32 ch) covers it |
| trigger | borrow | n_TOF logic for two arms: 2–3 N1081B, a dual timer, FIFOs, NIM bin |
| gas | buy | Ar/iC₄H₁₀ 95/5 premix and panel; flammable-gas rules at LNL (ask) |
| target | decide | LNL's pressed Li on Cu, 10–12 µm; holder: flat Al end cap at 45° (proposed 11 Nov) or the Cu ogive |

**Geometry.** The two arms face each other across the beam (opposite arms of the pinwheel, faces at ±204 mm). The X17
pairs at ~135–140° and the large-angle IPC are seen through opposite arms; adjacent arms see 25–92° pairs and no X17.
So two opposite arms keep the X17 physics, at about half the rate.

**Channels.** 16 SiPM-wall + 4 plastic PMT (+2 liquid) + 2–3 trigger word + spares ≈ 24. This is the "10–20 channels"
Pierfrancesco can find, plus a few.

## 3. Beam request (8 days)

| day | E_p | what |
|---|---|---|
| 1 | 1.10 MeV | target conditioning; current scan 0.05 → 1 µA (rates, live time, occupancy) |
| 2–3 | 0.441 MeV | locate the resonance on the γ yield; 17.64 MeV IPC calibration (resolution, acceptance, energy scale) |
| 4–8 | 1.10 MeV | 18.15 MeV region; daily γ-yield check of the target; day 8 = contingency or 0.80 MeV |
| nights / weekend | — | beam-off cosmics with the full trigger |

- AN2000 "self-service": one energy change per day, which fits the plan (three energies).
- 1 µA is the documented proton current at 0.8–2 MeV on both machines (and on AN2000 except the 0° line).
- **The CN cannot do day 2–3:** its range starts at 0.8 MV. On the CN the plan becomes 1.03/1.10 MeV only, and the
  calibration moves to the γ₁/γ₀ ratio and cosmics.

## 4. What 8 days can show (scaling estimate, 2026-11-18)

`../planning/two_arm_estimates.py` → `../planning/out/two_arm_reach.csv`. The four-arm Geant4 reach of
`x17_facility_search/lnl/FEASIBILITY_SIM.md` §19.3 (reference fit, 3σ at R(ATOMKI), 1 µA, 1.10 MeV, MM 15° + 0.3 ns TOF)
×2 in days for two arms (range ×1.7–2.5). Five days at 1.10 MeV:

| target | energy stack | 4 arms, d to 3σ | 2 arms, d to 3σ | Z at R(ATOMKI) in 5 d | expected 90 % limit / R(ATOMKI) | / MEG II |
|---|---|---|---|---|---|---|
| Al ogive + Cu liner | SiPM + small plastics | 30.5 | 61 (48–82) | 0.86 | 1.49 | 0.72 |
| | + liquid as at n_TOF | 8.5 | 17 (12–25) | 1.63 | 0.79 | 0.38 |
| | + liquid repaired | 4.5 | 9 (6–14) | 2.24 | 0.57 | 0.28 |
| Cu ogive | SiPM + small plastics | 45 | 90 (68–125) | 0.71 | 1.81 | 0.88 |
| | + liquid as at n_TOF | 11 | 22 (15–35) | 1.43 | 0.90 | 0.43 |
| | + liquid repaired | 6 | 12 (8–20) | 1.94 | 0.66 | 0.32 |

Caveats:
- Statistics plus the fitted background-shape freedom of the reference fit, nothing more. The 0.3 ns arm-to-arm TOF is not
  measured; with track pointing alone the days are ×1.5–2 (§19.4 there).
- The ×2 is geometry reasoning. Task R1 replaces it with a two-arm re-reduction of the L10–L13 tables (no new Geant4).
- Not a discovery run, and the proposal must not read like one. The limit column is what we quote as "sensitivity".
- 441 keV: 6–12k selected pairs per day at 1 µA with two arms (half of §19.5's four-arm 12–24k).

## 5. Timeline

| when | what |
|---|---|
| 18 Nov – 9 Dec 2026 | proposal (§6); submit 9 Dec |
| ~18 Jan 2027 | technical-review feedback |
| 25–29 Jan 2027 | PAC (12 + 8 min talk) |
| Feb – Apr 2027 | B fixed, windows; DREAM loan agreed; PMTs, digitizers, trigger modules found; target holder designed |
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

Cash with everything borrowed: **€21.6k central** (`plan.py` `BUDGET`): 4 M1 cards €8k, B fix + windows €1.6k, gas €3.4k,
slow control €2.5k, splitters and cables €3.8k, PDU, shipping €2k. Contingencies if loans fall through: a V1742 €9.5k,
2 N1081B €14k, a VME crate €4.8k, an N93B €2.7k, PMTs €6–24k. Prices from the CAEN offer 26OFC.01101 and
`x17_facility_search/budget/items.py`.

## 8. Risks

In `plan.py` `RISKS` and on the page. The three that would stop the run: B or DREAM not ready (ask CEA now), the AN2000
room or line not free (talk to the LNL ⁸Be group), the proposal over-selling the reach (frame it as feasibility).

## 9. Open questions

In `plan.py` `QUESTIONS`, by who answers: Pierfrancesco (spokesperson, GLIMOS, machine, target, commission calendar,
authors), the Accelerator Division (line, floor, 24 h running, flammable gas), CEA, CAEN, the LNL ⁸Be group, the plastics lender.
