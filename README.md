# lnl_x17: the MX17 X17 experiment at INFN Legnaro

Started 2026-11-18. Two beam slots at LNL, on ⁷Li(p,e⁺e⁻)⁸Be with the n_TOF MX17 apparatus:

1. **Slot 1, the feasibility study** (`slot1_feasibility/`): two opposite arms, 8 working days on the CN in June or July 2027 (was 8 days on AN2000, and H2 2027, until 25 Nov). Proposal to the
   Jan 2027 PAC, **deadline 10 Dec 2026, 23:59 CET**.
2. **Slot 2, the physics experiment** (`slot2_physics/`): four arms with big plastics, a later PAC.

The physics, detector and reach studies behind this repo are in `~/PycharmProjects/x17_facility_search/lnl/` (and `budget/`,
`daq_trigger/`, `slow_control/`). The detector lives in MX17_Full_Geant / MX17_Geant. This repo holds the plan, the proposal
and the page; it does not duplicate those studies.

**Live page (unlisted):** <https://dylan-neff.web.cern.ch/facilities/lnl-feasibility.html>

## Read this first (2026-11-18, reach updated 2026-11-19)

- **25 Nov: June or July 2027, not H2 2027.** The January call allocates beam from 20 Feb to 30 Jul 2027 (the call page prints
  2026). Pierfrancesco confirmed it on 25 Nov. Plan: both arms on cosmics by 14 May, install at LNL from 14 Jun, beam ~5–14 Jul
  (`slot1_feasibility/PLAN.md` §5, `correspondence/2026-11-25_mastinu_call_period.md`).
- **25 Nov: the CN, not AN2000** (AN2000 probably not available). The allocation is 8 days. The proposal asks 8 working days at 1 µA,
  assuming 8 h of beam per working day: day 1 scan + 1.10 MeV, day 2 H₂⁺ at 0.883 MV for 441 keV (else 1.10 MeV), days 3–7
  at 1.10 MeV, day 8 adjacent. That is 46 h at 1.10 MeV: 3.8 × R(ATOMKI) (2.35 × needs 120 h). Implications and the 2/4 µA fits: `slot1_feasibility/CN_BEAM.md`.

- Pierfrancesco (18 Nov): ask for an **X17 feasibility study**, ~8 days, measure in H2 2027 (changed 25 Nov to June–July, see above); he does the informal contact;
  co-proponents Massimi, Mengoni, Gervino, Gustavino, Cosentino (`correspondence/2026-11-18_mastinu_pac.md`).
- Set-up: Micromegas A (ready) + B (drift fix by Stephan), 2 SiPM walls, 4 small plastics (PMTs to find), ~24 digitizer channels,
  half of DREAM. Cash ~€8k critical for the test (+€5k low-, +€8k high-budget upgrades) if every loan comes through. 25 Nov: LEMO cables + Ts
  from n_TOF (very likely), NIM modules + DREAM LV rented from the CERN pool (hopefully); `slot1_feasibility/PLAN.md` §7.
- **Geant4 two-arm study (19 Nov, `sim2arm/TWO_ARM_STUDY.md`, note
  <https://dylan-neff.web.cern.ch/notes/lnl-two-arm-run.html>):** 5 days at 1.10 MeV, 11 µm Li, horizontal pair: expected 90 %
  limit **0.93 × R(ATOMKI)** with the liquid cells working, **1.19 ×** as at n_TOF, **1.78 ×** without them (MEG II: 2.07 ×). An
  ATOMKI-size signal would show at 0.7–1.4σ: a limit, not a 3σ test. Plan: cosmic nights with the arms **vertical** before the
  beam (the veto test), **horizontal** for the beam days, opposite arms (turning them in costs time), 441 keV for one day
  (~600 pairs/day, not 6–12k), ½ day adjacent for external conversions. Bring the liquid cells (×2–4 in days).
- **Liquid cells in (PF, 20 Nov):** the proposal assumes two 45 × 45 × 2 cm cells in new cans (2.35 × R(ATOMKI) in 5 d with the built
  hemisphere, 4.3 × without). Thicker (4 cm, 2 + 2 in series) and wider cells from ~60 L: `slot1_feasibility/LIQUID_CELLS.md`, S6–S8.
- ~~AN2000, not CN~~ (superseded 25 Nov): the CN starts at 0.8 MV; 441 keV only with an H₂⁺ beam (CN_BEAM.md §2).
- Next: P1 (outline + questions to Pierfrancesco), P3 (INFN-AAI account), R5 (proposal text from sim2arm, Overleaf), draft v1 by 27 Nov.

## Map

| path | what |
|---|---|
| `slot1_feasibility/PLAN.md` | the feasibility study: set-up, beam days, reach, timeline, budget, risks |
| `slot1_feasibility/LIQUID_CELLS.md` | the liquid cells: 2 × 2 cm baseline (20 Nov), thicker or wider ones from ~60 L |
| `slot2_physics/PLAN.md` | the full experiment, outline and hand-over |
| `proposal/STRUCTURE.md` | how an LNL PAC proposal is built (rules, submission, review) |
| `proposal/latex/` | the draft in the LNL template: `main.tex` (both parts), text in `abstract_content.tex` + `body_content.tex` (`make`, `make zip`); on [Overleaf](https://www.overleaf.com/project/6afdf0e8d237ac71ebb14b1f) |
| `proposal/lnl_template/` | the official LNL templates from Indico 50487 |
| `planning/plan.py` | **single source** of tasks, phases, milestones, hardware, budget, questions, risks → `planning/out/plan.json` |
| `sim2arm/` | the Geant4 two-arm study: `TWO_ARM_STUDY.md`, the fit cut to one arm pair, L15/L16 condor jobs, the slide note |
| `sim2arm/PREDICTIONS.md` | Geant4 predictions of every observable of the run and the 3D event view (page tab "Predictions"): `predictions.py`, `events3d.py`, run L17 |
| `planning/two_arm_estimates.py` | the two-arm reach rows from `sim2arm/out/summary_reach_pass2*.csv` → `planning/out/two_arm_reach.csv`, `beam_days.csv` |
| `proposal/figsrc/make_figures.py` | the proposal figures at print size (`proposal/latex/figures/fig_event`, `fig_predictions`, `fig_reach`, the n_TOF photo); `make_ntof_fans.py` redraws the n_TOF run-145 tracks |
| `planning/figures.py` | the reach figure of the page (`proposal/latex/figures/limit_vs_days.*`; no longer in the proposal) |
| `site/template.html`, `site/build_page.py` | the page: build, copy into dylan-cern-site |
| `correspondence/` | short summaries of the e-mails that set decisions |

## Update the page

```
python3 planning/two_arm_estimates.py && python3 planning/figures.py   # if the reach changed
python3 proposal/figsrc/make_figures.py      # the proposal figures (after a new pass or reach table)
make -C proposal/latex && make -C proposal/latex zip   # if the proposal changed
WORK_DATA=/media/ucla/work ~/PycharmProjects/nTof_x17/.venv/bin/python sim2arm/predictions.py   # Predictions tab numbers
WORK_DATA=/media/ucla/work ~/PycharmProjects/nTof_x17/.venv/bin/python sim2arm/events3d.py      # its 3D events (L17)
python3 site/build_page.py                   # writes into ~/PycharmProjects/dylan-cern-site
cd ~/PycharmProjects/dylan-cern-site && python3 scripts/build.py && scripts/deploy-eos.sh
```
