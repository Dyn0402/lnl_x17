# What the two-arm run should see: Geant4 predictions, observable by observable

Written 2026-11-20. Shown on the page's **Predictions** tab
(<https://dylan-neff.web.cern.ch/facilities/lnl-feasibility.html#predict>), with a 3D view of real Geant4 events.
Code: `predictions.py` → `out/predictions.json`, `events3d.py` → `out/events3d.json`; lxplus scripts in `lxplus/`
(`pred_cosmic_scan.py`, `submit_traj.sh`, `run_traj.sh`, `traj_pick.py`).

Set-up as in `TWO_ARM_STUDY.md`: two opposite arms, Cu hemisphere, 11 µm Li (yields; the Geant4 events are the 20 µm
runs), 1 µA, liquid cells working ("LNL calibrated"), reference selection = MM 15° pointing + 0.6 ns TOF, E_sum window
13–19 MeV. A **leg** is SiPM bar AND plastic ≥ 0.5 MIP in one arm; an **MM track** is a Micromegas segment (dominant
track, ≥ 3 steps) with its centroid in the active area (`lnl_merge.py`). The simulated chambers are 100 % efficient;
"× ε" applies the bench efficiency ε = 0.92 per chamber.

## 1. Inputs

| sample | what | used for |
|---|---|---|
| L15 cosmic disk (10.0 live days, 4.89 × 10⁸ μ) | per-job parts re-scanned on lxplus (`pred_cosmic_scan.py`): every event with legs in both arms of a slot-1 pair, all per-arm columns | §2 |
| L13 8Be γ lines, Cu hemisphere (3 × 10⁸ γ) | same script, `--mode single`: every event with a leg | §3 |
| L11 + L13 pair tables via `two_arm_nd.py` / `shapes_nd.collect` | IPC, EPC, X17, cosmics after the analysis | §4–5 |
| **L17** (new, 53 condor jobs, all ended normally, no retries) | MX17_Full_Geant `lnl_twoarm` 10229eb (`--trajdump` now also writes μ±), arms 0+1 (and 2+3 for vertical muons), every step of e±, γ, μ for the kept events | the 3D view |

The merged L15 table keeps only events with two "ok" arms, so it could not give trigger-level fractions; the re-scan
does (2.2 M pair-leg events).

## 2. Cosmic nights (beam off)

| | arms vertical (2 + 3) | arms horizontal (0 + 1) |
|---|---|---|
| legs per arm | 18.1 Hz | 6.81 Hz |
| PAIR triggers (legs in both arms) | **1.89 Hz**, 68,000 per 10 h night | **0.075 Hz**, 2,690 per night (25× fewer) |
| … with MM tracks in 2 / 1 / 0 arms, ε = 1 | 99.5 / 0.5 / 0.01 % | 98.3 / 1.6 / 0.06 % |
| … × ε (0.92 per chamber) | **84 / 15 / 0.7 %** | **83 / 16 / 0.8 %** |
| two-track pairs at 125–160° | 57 % (38,700 per night) | 64 % |
| Δt between the walls (σ_t 0.6 ns per arm) | +2.3 ns (lower − upper), 100 % downward | ±2.3 ns, both signs |
| segments passing the pointing cut (one arm) | 64 % at 15°, 21 % at 3° | 72 %, 30 % |
| left in 125–160° after E_sum + pointing + TOF | 500 / day (1,293 MC) | 46 / day (120 MC) |
| muon zenith angle, median | 12° | 73° |

- A PAIR trigger with one track instead of two is a chamber that missed the muon: the 1-track fraction measures each
  chamber's efficiency in situ, night by night.
- Legs with an MM track: 44 % (side arms) and 69 % (top/bottom) at ε = 1; the rest are muons through the plastics
  that miss the active area.

## 3. Beam singles (day 1, current scan)

| at 1 µA | 441 keV | 1.10 MeV |
|---|---|---|
| γ₀ at the target (17.64 + 18.15) | 54,400 /s | 14,700 /s |
| beam legs per arm | **124 Hz** | **66.8 Hz** |
| legs per arm with cosmics | 131 Hz | 73.6 Hz |
| beam legs with an MM track (× ε) | 55 % | 55 % |
| accidental pairs (20 ns), before cuts | 30 / day | 9 / day |

- The leg probability is 1.5 × 10⁻³ per γ per arm, the same for the four lines within 5 %.
- **Where the track comes from:** in the L17 γ events, 30 of 31 single-arm legs with an MM track had the γ interact in
  the Cu hemisphere wall; 23 of 25 legs without a track converted behind the drift gap (readout PCB, support plate,
  SiPM wall). The tracked fraction (55 %) against cosmics' 40 % is a direct check of the holder's material.
- The slope (Hz per µA) is γ yield × leg probability: it measures the film's Li content.

## 4. Pairs at 441 keV (day 2) and 1.10 MeV (days 3–7)

Per day, horizontal pair. "Both tracks" = a leg and an MM track in both arms, any θ, E_sum 0–43 MeV.
"Selected" = θ > 90°, E_sum window, pointing + TOF.

| per day | 441 keV, both tracks | 441 keV, selected | 1.10 MeV, both tracks | 1.10 MeV, selected |
|---|---|---|---|---|
| M1 IPC (17.64 / 18.15) | 2,790 | 458 | 261 | 43 |
| E1 IPC (18.15) | 103 | 19 | 1,880 | 345 |
| 15.1 / 14.6 MeV IPC | 1,740 | 23 | 3,750 | 53 |
| external conversions | 3,150 (11 MC) | 165 (3 MC) | 1,710 | 0.4 |
| cosmics | 5,930 | 68 | 5,930 | 68 |
| X17 at R(ATOMKI) | 5 | 1 | 99 | **18** |
| **beam total** | **7,790** | **665** | **7,700** | **510** |

- **Selected 441 keV pairs per beam leg: 6.5 × 10⁻⁵**, independent of the Li content.
- **The external conversions at 441 keV rest on 3 simulated events** (selected) and 11 (both tracks): good to a factor
  ~2. They are ~25 % of the selected 441 keV sample, so D2 (665/day) is uncertain by about ±20 %. Task R6 (more
  as-built EPC MC) fixes it.
- Only ~30 % of the 441 keV IPC pairs land in the 13–19 MeV window: the response (energy lost in the holder and the
  chamber, partial containment) puts most of them at 9–13 MeV. The E_sum distribution itself is a prediction to check.

## 5. The n_TOF cross-check of the cosmic simulation (2026-11-20)

The 2026 n_TOF beam-off A–C muon pairs (nTof_x17 `ntof_cosmics/results/ac_rate/summary.json`, toy MC
`ntof_cosmics/ac_cosmic_rate.py`):
- the zenith shape matched (median 73.6° measured, 74.4° predicted);
- the rate, 0.063 Hz against 0.161 Hz, is low by 2.5. That factor is the reconstruction's track gate (wft x–y time
  agreement, tuned on capsule tracks): 57 % of clean A–C muons fail it in at least one arm. With quality-only tracks the
  rate is 0.11–0.17 Hz, consistent. The 2026-10-07 nTof_x17 handoff's "ε_A·ε_C ≈ 0.35 chamber efficiency" is this gate,
  not the hardware;
- **open (task R9):** the A–C wall coincidences without chambers are 0.84 Hz against 0.34 Hz predicted. Until that is
  understood, quote absolute cosmic rates with a factor ~2.5 uncertainty, and lean on ratios (A2/B2, track fractions).

## 6. Not in the simulation

Room background, beam-line activation, contaminants (¹⁹F, ¹¹B, ¹³C), neutrons (none below the 1.88 MeV ⁷Li(p,n)
threshold), the LNL hall roof (lowers the cosmic flux a little). The single-arm energy spectra are raw deposits (no
light yield, quenching, resolution); the pair E_sum and |y| plots include the response. Chamber efficiency is the bench
value, and a reconstruction gate would cut further (§5).

## 7. For the proposal (task R8)

- Fig. 1: the 3D render (Predictions tab → "save PNG"); a 1.10 MeV pair and a cosmic muon in the same set-up.
- §3: a compact predictions table with pass criteria: A2/A3 (cosmic trigger and track fractions), C1/C2 (beam singles
  and their tracked fraction), D2/D3 (the 441 keV calibration), E1.
