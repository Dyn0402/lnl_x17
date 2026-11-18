# lnl_x17: the MX17 X17 experiment at INFN Legnaro

Started 2026-11-18. Two beam slots at LNL, on ⁷Li(p,e⁺e⁻)⁸Be with the n_TOF MX17 apparatus:

1. **Slot 1, the feasibility study** (`slot1_feasibility/`): two opposite arms, ~8 days on AN2000 in H2 2027. Proposal to the
   Jan 2027 PAC, **deadline 10 Dec 2026, 23:59 CET**.
2. **Slot 2, the physics experiment** (`slot2_physics/`): four arms with big plastics, a later PAC.

The physics, detector and reach studies behind this repo are in `~/PycharmProjects/x17_facility_search/lnl/` (and `budget/`,
`daq_trigger/`, `slow_control/`). The detector lives in MX17_Full_Geant / MX17_Geant. This repo holds the plan, the proposal
and the page; it does not duplicate those studies.

**Live page (unlisted):** <https://dylan-neff.web.cern.ch/facilities/lnl-feasibility.html>

## Read this first (2026-11-18)

- Pierfrancesco (18 Nov): ask for an **X17 feasibility study**, ~8 days, measure in H2 2027; he does the informal contact;
  co-proponents Massimi, Mengoni, Gervino, Gustavino, Cosentino (`correspondence/2026-11-18_mastinu_pac.md`).
- Set-up: Micromegas A (ready) + B (drift fix by Stephan), 2 SiPM walls, 4 small plastics (PMTs to find), ~24 digitizer channels,
  half of DREAM. Cash ~€10k critical for the test (+€3k low-, +€8k high-budget upgrades) if every loan comes through.
- **Scaling estimate** (`planning/two_arm_estimates.py`): 5 days at 1.10 MeV give an expected 90 % CL limit of 1.5–1.8 × R(ATOMKI)
  with walls + plastics, near MEG II's limit; **0.8–0.9 × with two liquid cells**. Replace with the two-arm re-reduction (task R1).
- AN2000, not CN: the CN starts at 0.8 MV, so no 441 keV calibration there.
- Next: P1 (outline + questions to Pierfrancesco), P3 (INFN-AAI account), R1, draft v1 by 27 Nov.

## Map

| path | what |
|---|---|
| `slot1_feasibility/PLAN.md` | the feasibility study: set-up, beam days, reach, timeline, budget, risks |
| `slot2_physics/PLAN.md` | the full experiment, outline and hand-over |
| `proposal/STRUCTURE.md` | how an LNL PAC proposal is built (rules, submission, review) |
| `proposal/latex/` | the draft in the LNL template: `abstract.tex`, `body.tex` (`make`, `make zip`); on [Overleaf](https://www.overleaf.com/project/6afdf0e8d237ac71ebb14b1f) |
| `proposal/lnl_template/` | the official LNL templates from Indico 50487 |
| `planning/plan.py` | **single source** of tasks, phases, milestones, hardware, budget, questions, risks → `planning/out/plan.json` |
| `planning/two_arm_estimates.py` | two-arm reach scaling → `planning/out/two_arm_reach.csv`, `beam_days.csv` |
| `planning/figures.py` | the proposal figure (`proposal/latex/figures/limit_vs_days.*`) |
| `site/template.html`, `site/build_page.py` | the page: build, copy into dylan-cern-site |
| `correspondence/` | short summaries of the e-mails that set decisions |

## Update the page

```
python3 planning/figures.py                  # if the reach changed
make -C proposal/latex && make -C proposal/latex zip   # if the proposal changed
python3 site/build_page.py                   # writes into ~/PycharmProjects/dylan-cern-site
cd ~/PycharmProjects/dylan-cern-site && python3 scripts/build.py && scripts/deploy-eos.sh
```
