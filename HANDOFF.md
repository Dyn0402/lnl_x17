# Handoff

## Predictions tab: Geant4 predictions of every observable + 3D Geant4 events — updated 2026-11-20 (dylan-MS-7C84)

**Resume:** the tab is live (<https://dylan-neff.web.cern.ch/facilities/lnl-feasibility.html#predict>); next: R8 (3D render
as proposal Fig. 1, a short predictions table in §3), and the pass-3 follow-up below, which is still open.

**Done**
- `sim2arm/predictions.py` → `out/predictions.json`: cosmic nights (vertical/horizontal: legs, PAIR triggers, 2/1/0-track
  fractions × ε 0.92, θ, Δt, pointing, zenith), beam singles at 441 keV / 1.10 MeV (legs per µA, tracked fraction,
  single-arm E, accidentals), pairs at 441 keV and 1.10 MeV (trigger level and selected; θ, E_sum, |y|). Numbers and
  caveats: `sim2arm/PREDICTIONS.md`.
- lxplus `x17_lnl/analysis/l15/pred_cosmic_scan.py` (copy in `sim2arm/lxplus/`): re-scan of the L15 and L13 γ parts at
  trigger level (the merged tables keep only 2-ok-arm events). Outputs `/eos/user/d/dneff/x17/lnl_pred/`, local
  `$WORK_DATA/x17_facility_search/pred/`.
- **Run L17** (53 condor jobs, all normal termination, none retried): MX17_Full_Geant `lnl_twoarm` 10229eb (`--trajdump` also
  writes μ±; binary `bin/mx17_full_sim_twoarm_10229eb`, pushed), two-arm geometry, `submit_traj.sh` / `run_traj.sh` /
  `traj_pick.py`; outputs `/eos/experiment/ntof/data/x17/lnl/L17/`, local `$WORK_DATA/lnl_x17/L17/`.
  `sim2arm/events3d.py` → `out/events3d.json` (picked events, thinned tracks, layer extents read from the step points).
- Page: new tab from `site/predict_pane.html`, `site/predict.js`, `site/predict3d.js` (three.js 0.160 module, fat lines,
  save-PNG), inlined by `site/build_page.py`. plan.py tasks R7 (done), R8, R9.
- n_TOF cosmic factor 2.5 explained (§5 of PREDICTIONS.md): the wft track gate, not chamber hardware. Open: wall-level A–C
  0.84 vs 0.34 Hz (R9).

**Findings**
- Vertical cosmic nights: 1.89 Hz PAIR triggers (68k/night), 84 % with both tracks × ε; horizontal 0.075 Hz (25× fewer).
- Beam legs 67 Hz/µA/arm at 1.10 MeV, 124 at 441 keV (cosmics 6.8 Hz); 55 % carry a track (× ε): almost all from γ
  interactions in the Cu hemisphere wall.
- 441 keV: 665 selected pairs/day, of which 165 are external conversions resting on 3 MC events (±20 % on the total; R6).
- Only ~30 % of 441 keV IPC pairs fall in the 13–19 MeV window (the rest at 9–13 MeV after losses).

**Not committed on purpose (another session's pass 3):** `planning/out/plan.json`, `two_arm_reach.csv`, the proposal
figure/PDF/zip, `TWO_ARM_STUDY.md`, `sim2arm/out/*pass3*`, the slide note. The deployed page's Beam & reach tab already
shows pass-3 rows (the build reads them); the proposal PDF on the site was left at the committed version. Finish the
"Two-arm: measured σ_t plugged in (pass 3)" steps below (check §0, fix hand-written numbers, commit).

**Gotchas**
- `pred_cosmic_scan.py` runs interactively on lxplus in ~5 min (reads /eos parts directly; allowed interactively).
- A track starting outside the 70 cm display sphere is clipped along its segment (`events3d.py`), else muons vanish.

**Key files:** `sim2arm/PREDICTIONS.md`, `sim2arm/predictions.py`, `sim2arm/events3d.py`, `site/predict*.{js,html}`.

## Two-arm: measured σ_t plugged in (pass 3), shape systematics, 441 keV — updated 2026-11-19 (dylan-MS-7C84)

**Resume:** pass 3 (σ_t 0.6 ns) runs detached on the desktop; when `after_pass _pass3 done` is in its log, check, deploy, commit.

**Goal:** every LNL number uses the measured arm-to-arm σ_t (0.6 ns per arm) instead of the assumed 0.3, and the IPC
shape systematics of the two-arm fit are understood.

**Done**
- **σ_t measured** (nTof_x17 `ntof_cosmics/ac_tof_beamoff.py`, report `ntof_cosmics/results/ac_tof/report.html`,
  machine-readable `results/ac_tof/timing.json`): beam-off A–C wall muons (2,579) show the muon's ±2.5 ns TOF as two
  peaks; **0.52–0.64 ns per arm (walls), 0.95 (plastics)**, n_TOF readout. Beam-run muons give ~6 ns (pulse fit under beam).
  The first look moved to nTof_x17 `ntof_cosmics/results/ac_tof/firstlook/`.
- x17_facility_search `lnl_geant.TOF_SIGMA_NS` now reads it (0.60; `LNL_TOF_SIGMA_NS=0.3` reproduces pass 2); helper
  `sipm_wall/measured_timing.py` for ILL / trigger_scint / sipm_wall (code defaults switched, their tables not re-run).
- Labels here say "pointing + 0.6 ns TOF"; `SIM_TAG` and the `--tag` defaults are `_pass3`; template/page text updated.
- `sim2arm/tof_scan.py`: horizontal 17.4 d (no TOF) → 17.7 at any σ_t; vertical 17.1 / 17.9 / 18.7 d at 0.3 / 0.6 / 0.7 ns
  (pointing 3° for muons). First pass-3 rows: vertical `MM 15° + TOF` (15° for muons too) at 0.6 ns is 23.3 d with
  494 cosmics/day (was ~17 d, 0.4/day at 0.3): the reference level leans on TOF, so the vertical pair suffers.
- `sim2arm/geom_syst.py`: fake X17 from 2 mm misplacements ≤ 0.01 R(ATOMKI) horizontal, ≤ 0.11 vertical; a dead 10 mm
  MM band −0.18 R (−0.4σ, 5 d). `sim2arm/struct_scan.py`: harsher unknown structure costs ≤ +1.5 d.
- 441 keV stays on opposite arms (adjacent: 39 M1 pairs/day in 125–160° against 358).

**In progress**
- `run_pass.sh _pass3 6 && after_pass.sh _pass3`, started 12:25 detached (setsid), log
  `/media/ucla/work/claude-jobs/lnl_pass3.log`, parts `sim2arm/out/parts/*_pass3*` (resumable). ~3 h. If it died, rerun
  the same command (`WORK_DATA=/media/ucla/work setsid nohup bash -c 'bash sim2arm/run_pass.sh _pass3 6 && bash
  sim2arm/after_pass.sh _pass3' > /media/ucla/work/claude-jobs/lnl_pass3.log 2>&1 &`): finished tasks are skipped.
- Until then `TWO_ARM_STUDY.md`, the proposal, `planning/out/` and the page still show the pass-2 (0.3 ns) numbers, and
  `planning/two_arm_estimates.py` fails (no `summary_reach_pass3*.csv` yet).

**Next steps**
1. When the log says done: read `sim2arm/TWO_ARM_STUDY.md` §0 (regenerated) — the reach rows and the vertical vs horizontal
   comparison change; fix any hand-written sentence in `build_study_md.py`/the template that the numbers contradict
   (e.g. "vertical and horizontal equal within the MC").
2. Update the hand-written numbers in `proposal/latex/body_content.tex` (R90 0.93/1.19 × R(ATOMKI), Z, days) and `plan.py`
   texts from `planning/out/two_arm_reach.csv`; `make -C proposal/latex`, `python3 site/build_page.py`, deploy (README),
   republish the slide note (`sim2arm/out/lnl-two-arm-run.html`, publish-note skill), commit + push; Overleaf (R5).
3. x17_facility_search: four-arm LNL tables and ILL/trigger_scint/sipm_wall outputs are still at the old σ_t (noted in
   their docs); re-run when they matter. The four-arm fit should fit each arm pair separately (it sums them now).
4. R4: σ_t with the LNL digitisers (V1742 / CFD).

**Gotchas**
- `pkill -f <pattern>` kills the calling Bash tool's own shell when its command line contains the pattern: use `[x]yz`.
- The data for the passes is now on the desktop too: `$WORK_DATA/x17_facility_search/lnl_sel` (L11, L13 ogCu200 asb) and
  `sel_l15` (L15 chunks 0–3, the ones the fits use).

**Key files**: `sim2arm/run_pass.sh`, `sim2arm/after_pass.sh`, `sim2arm/tof_scan.py`, `sim2arm/geom_syst.py`, `sim2arm/struct_scan.py`.

## Two-arm Geant4 study (R1) and the 8-day plan — updated 2026-11-19 (dylan-Yoga, overnight)

**Resume:** read `sim2arm/TWO_ARM_STUDY.md` §0 (or the note <https://dylan-neff.web.cern.ch/notes/lnl-two-arm-run.html>);
next: upload the new `proposal/latex/body_content.tex` to Overleaf (R5), then P1 with the new numbers.

**Goal (Dylan, 18 Nov night):** careful analysis and simulation of a bare-bones two-Micromegas LNL run (~8 days): can we see
something, should we go for a measurement, which geometry (vertical, horizontal, perpendicular), and a hedged run plan that
prepares the physics run and gives results for funding proposals. Liquid cells evaluated both ways; arms may be moved.

**Done**
- `sim2arm/two_arm_nd.py`: the FEASIBILITY_SIM §19 reference fit (shapes_nd) with every table cut to one arm pair; Cu
  hemisphere, L11 + L13 (incl. the L13 E1 18.15 table, never merged before: reduced + merged tonight, on EOS now).
  Grid: 4 pairs × 3 liquid states × 4 vetoes × 2 estimators × 2 films (20 µm simulated, 11 µm yields) + spectra.
- **Run L15** (1630 condor jobs, 10.0 live days): new `--cosmic-disk` generator (muons start on a disk normal to the track).
  **L4 had missed every muon steeper than ~45°**: horizontal pair 110 → 6,254 coincidences/day; vertical unchanged (162k).
- **Run L16**: new `--arms`/`--arm-phi` (rotated arms): Δφ 160° ×1.1, 140° ×2–2.5 in days. Keep the arms opposite.
- MX17_Full_Geant branch `lnl_twoarm` (3 commits, pushed; worktree `/afs/.../x17_lnl/MX17_Full_Geant_twoarm`, binary
  `bin/mx17_full_sim_twoarm_be1c1bb`). Fixed on the way: rotated placements need the frame rotation P0·Rφ⁻¹.
- Results (11 µm, horizontal, 5 d): R90 = 0.93 / 1.19 / 1.78 × R(ATOMKI) (liquid working / as at n_TOF / none); Z = 1.4 /
  1.1 / 0.7σ. Two arms = ×2.2 the four-arm days; 11 µm = ×1.3 against 20 µm. Horizontal = vertical with 0.3 ns TOF; with
  pointing only the horizontal pair holds (23 d) and the vertical drops (34 d). 1 ns TOF barely helps.
- Plan (`sim2arm/TWO_ARM_STUDY.md` §7): vertical cosmic nights before the beam (σ_t, μ segments, gains, the MEG II 140° peak),
  roll to horizontal; day 1 current scan; day 2 441 keV (~600 pairs/day above 90°); days 3–7 X17; day 8 ½ day adjacent.
- Propagated: `planning/two_arm_estimates.py` (simulation, films, geometry, veto), `figures.py`, `plan.py` (R1 done, R5, R6,
  γ monitor, stand roll, risks, questions), page reach tab (film/geometry/veto selectors) and texts, proposal body text +
  beam table + figure (`make` OK, body 4 pages), `slot1_feasibility/PLAN.md` §0, §2–4. Page + note deployed (site 28d9c61).

**Gotchas**
- `planning/two_arm_estimates.py` reads `sim2arm/out/summary_reach_pass2*.csv` (`SIM_TAG`); rerun `sim2arm/run_pass.sh`
  (~2.5 h on the laptop, 4 workers: more get OOM-killed and `multiprocessing.Pool` then hangs) and `build_study_md.py`.
- The fits used L15 chunks 0–3 (2.45 live days); the tables in §4 use all 10. Cosmic tables: `$WORK_DATA/x17_facility_search/sel_l15/`.
- lxplus scripts (L15/L16 submit, run, merge) live in `/afs/cern.ch/work/d/dneff/git/x17_lnl/analysis/l15/`; copies in `sim2arm/lxplus/` (all synced 19 Nov). Laptop `WORK_DATA` is unset: the scripts default to `/media/dylan/data/work`.
- Overleaf is NOT updated (needs the browser): upload `body_content.tex`, Refresh the linked `limit_vs_days.pdf`.
- The laptop's dylan-cern-site checkout is 42 commits behind and has another session's uncommitted files; I built and
  deployed from a clean worktree at origin/master instead and left that checkout alone.
- revtex4 and enumitem were missing on the laptop: unpacked from the Ubuntu debs into `~/texmf/tex/latex/`.

**Next steps**
1. R5: Overleaf upload; send Pierfrancesco the outline with these numbers (P1); the question on a rolling stand and a γ monitor.
2. S5: decide the liquid cells (the biggest lever). R4: σ_t on the cosmic bench.
3. R6: more as-built Cu-hemisphere MC (EPC, IPC at large angle) before the PAC talk.

## LNL page + proposal: Overleaf, budget, Cu hemisphere, Hardware tab, inventory — updated 2026-11-19 (dylan-MS-7C84)

**Resume:** page and Overleaf draft current; next: P1 (outline + questions to Pierfrancesco), P3 (INFN-AAI), R1 (two-arm re-reduction).

**Goal:** get the PAC proposal (due 10 Dec 2026) and the planning page into shape for Pierfrancesco and the co-proponents.

**Done (19 Nov)**
- **Overleaf** shows the full draft: main document `main.tex` (abstract + body, 5 pages). Text in `proposal/latex/abstract_content.tex`
  and `body_content.tex`; `abstract.tex`/`body.tex` build the two Indico PDFs; `preamble.tex`. Before, only `abstract.tex`
  compiled there. The page links Overleaf's edit link (anyone with it can edit; it is public in the repos, Dylan's choice).
- **Budget** (Dylan): new drift windows A+B → low-budget tier (€1.25k); B's drift-window repair stays critical (€0.3k).
  Critical €9.1k, low +€4.4k, high +€8k, +€42.9k if loans fail.
- **Overview**: one-line lead + Overleaf/PDF buttons on top; details and the Indico call in a box at the bottom.
- **Target** (Dylan): the Cu hemisphere is built, so it is the baseline ("Cu ogive" of FEASIBILITY_SIM §19.3). Reach now 1.81 ×
  R(ATOMKI) in 5 d, 0.90 × with liquid cells; proposal says (0.9–1.8) ×. Default target in the Beam & reach tab.
- **Risk** "B not repaired" → low (likely just an electrical connection).
- **Hardware tab**: `plan.py` HARDWARE = 31 items (lender `org`/`src`, contact, state, need-by, diagram `place`, `tasks`, budget
  line `b` → cash/tier via `hardware_rows()`, which asserts every BUDGET line belongs to one item). Search, group, filter, sort,
  totals; detail panel with tasks, inventory entries and a schematic with the item highlighted.
- **Central inventory** started in `x17_facility_search/inventory/` (21 assets: owner, location, condition, availability);
  HARDWARE items point at it with `inv=[ids]`. DAQ PC is CEA's (borrow); the network switch is Dylan's.

**Next steps**
1. P1: send Pierfrancesco the outline, the two-arm numbers and the questions (spokesperson, GLIMOS, machine, holder fit, authors).
2. P3: INFN-AAI account; R1: two-arm re-reduction of L10–L13 on lxplus, then `two_arm_estimates.py` + figure.
3. Fill the (ask) lenders/locations: `plan.py` HARDWARE (my first fill, mostly "to ask") and `x17_facility_search/inventory/inventory.py`.
4. Draft v1 by 27 Nov.

**Gotchas**
- revtex4 + Overleaf's newer TeX Live: `p{}`/`@{}` tabular columns give "Extra \or"; tables use `l` columns + `\daycell`.
- Overleaf's `figures/limit_vs_days.pdf` is a *linked file* from `https://dylan-neff.web.cern.ch/facilities/lnl/limit_vs_days.pdf`:
  after `planning/figures.py`, copy the PDF to the site's `facilities/lnl/`, deploy, then Refresh it in Overleaf. Text files were
  pushed with Overleaf's own upload endpoint from the page (JS fetch, root folder id 6afdf0e9d237ac71ebb14b7d); check Overleaf
  history for edits there first. Overleaf and the repo were identical on 19 Nov evening.
- The site repo's branch is `master`, not `main`.

**Key files & commands**
- `planning/plan.py` → `python3 site/build_page.py`; then in `~/PycharmProjects/dylan-cern-site`: `python3 scripts/build.py && scripts/deploy-eos.sh`.
- `proposal/latex/`: `make`, `make zip`. `site/template.html`: the page (Hardware tab: PLACES, hwTable2, hwDetail).

## LNL proposal page: template, Overleaf, budget tiers — updated 2026-11-18 (dylan-MS-7C84)

**Resume:** the draft is in the official LNL template and on Overleaf; the page's overview leads with Indico and closes with
Overleaf; budget split into tiers. Next steps unchanged (P1, P3, R1).

**Done**
- Templates from Indico 50487 (Chrome, the bot check passes in a real browser) → `proposal/lnl_template/`. Draft moved into them:
  `proposal/latex/abstract.tex` (1 page), `body.tex` (3¼ of **4** pages: the template's limit, stricter than the web page's 5),
  `macros.tex`. `make` → abstract.pdf, body.pdf, proposal.pdf. Old `main.tex` removed (in git history).
- Overleaf project <https://www.overleaf.com/project/6afdf0e8d237ac71ebb14b1f> (from the zip; compiles). Switch Menu → Main
  document between abstract.tex and body.tex. Not shared yet: Pierfrancesco needs an invite.
- Budget tiers (Dylan): critical €10.4k (B fix + windows, gas supply, splitters/LEMO/adapters, shipping); low-budget upgrade
  +€3.2k (low-permeation lines, sensors, switched PDU); high-budget upgrade +€8k (4 CERN M1 cards for B; B runs its Italian M1s
  for the test). Not for the proposal, for planning.
- Overview rewritten for a first-time reader: a start-here block plus Indico, the call PDF and the beam sheet; countdown, a request at a
  glance, stepper, next up, decisions; closes with Overleaf + PDF. The "what the run proves" cards moved to the Proposal tab.

**Gotchas**
- revtex4 is not in the desktop's TeX Live; it was extracted from Ubuntu's texlive-publishers into `~/texmf/tex/latex/`.
- Overleaf and `proposal/latex/` can now drift. Decide which is the master before editing in both.

## LNL PAC feasibility proposal — updated 2026-11-18 (dylan-MS-7C84)

**Resume:** proposal draft v0 and the planning page are up; next: send Pierfrancesco the outline and questions (P1), get the
INFN-AAI account (P3), run the two-arm re-reduction (R1).

**Goal (Dylan, 18 Nov):** after Pierfrancesco's reply, start a real proposal (X17 feasibility study, the most easily available
set-up), research how LNL proposals are structured, a draft for Overleaf, organise the repo for two beam slots, concrete plans and
timelines, and a cern-site page to organise the first beam time.

**Done**
- Read the thread (CERN mailbox); summary `correspondence/2026-11-18_mastinu_pac.md`.
- LNL rules researched (`proposal/STRUCTURE.md`): abstract ≤ 1 page with title, accelerator, set-up, spokesperson, GLIMOS,
  authors; body ≤ 5 pages 12 pt incl. figures/refs; motivation, technical details + precision, beam days from count rates;
  Beam Time Request + Targets Request Form online; INFN-AAI account; technical review ~7 d before the PAC; 12 + 8 min talk.
- Draft `proposal/latex/main.tex` (abstract + 4 body pages, compiles), zip for Overleaf.
- `planning/plan.py` (34 tasks, 23 phases, hardware, budget, risks, questions), `two_arm_estimates.py`, `figures.py`.
- `slot1_feasibility/PLAN.md`, `slot2_physics/PLAN.md`.
- Page `facilities/lnl-feasibility.html` (9 tabs: overview + countdown, Gantt + deadline calendar, set-up view along the beam,
  beam days + reach calculator, tasks, proposal, budget, risks + questions, slot 2).

**Findings**
- Two opposite arms, 5 d at 1.10 MeV: expected 90 % limit 1.5–1.8 × R(ATOMKI) (walls + plastics), 0.8–0.9 × with two liquid
  cells. ×2 scaling of FEASIBILITY_SIM §19.3, not simulated.
- AN2000 rather than CN (441 keV calibration needs < 0.8 MV).
- A horizontal arm pair suppresses two-arm cosmics by geometry; a vertical pair is the hard test of the veto. Decide.
- ~24 scintillator channels for two arms: about what Pierfrancesco can find.

**Next steps**
1. P1: outline + two-arm numbers + questions (spokesperson, GLIMOS, machine, target, liquid cells, orientation, authors) to Pierfrancesco.
2. P3: INFN-AAI account + Risorse IT; download the LNL template from Indico 50487 in a browser.
3. R1: two-arm re-reduction of L10–L13 on lxplus (reduce only, no new Geant4), then update `two_arm_estimates.py` and the figure.
4. Draft v1 by 27 Nov; Pierfrancesco 30 Nov; co-proponents 3 Dec; submit 9 Dec.

**Gotchas**
- Indico (agenda.infn.it) sits behind an Anubis bot check: open it in a browser, don't script it.
- Task ticks on the page are per browser (localStorage); the plan's status is `plan.py`.
- The beam window (late Sep 2027) is our plan, not an allocation. If the INFN commission requests are due in summer, ask for Jun–Jul.

**Key files:** `slot1_feasibility/PLAN.md`, `proposal/latex/main.tex`, `planning/plan.py`, `site/build_page.py`.
