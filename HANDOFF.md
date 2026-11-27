# Handoff

## Proposal v1 to Pierfrancesco; L20 same-arm study; references, γ monitor, page audit — updated 2026-11-27 (dylan-MS-7C84)

**Resume:** draft v1 is with Pierfrancesco (sent 27 Nov); next: fold in his comments, then P7 (co-proponents) and R13 (Al holder EPC).

**Goal:** get the LNL PAC proposal (deadline 10 Dec) to a version Pierfrancesco can comment on, with every number and claim
checked, and the plan page consistent with it.

**Done (27 Nov):**
- Overleaf kept in sync by git (clone `https://git.overleaf.com/6afdf0e8d237ac71ebb14b1f`, diff against `proposal/latex/`
  before each push). Dylan edits there often: five rounds of his edits were merged today (last Overleaf commit `3d69b7d`).
- Beam day = **18 h of CN beam** (`planning/two_arm_estimates.py` OPER_EFF = 0.75): 106 h at 1.10 MeV = 5.9 beam days,
  2.84 / 3.64 / 4.77 × R(ATOMKI), 260 beam days to 3σ; all figures, proposal, plan, page, x17_facility_search updated.
- Body now 5 pages (LNL submission page; the template text says 4; last 4-page version `b8c9195`); Figs. 2–4 at full text
  width; references a standard numbered list, all ten checked on INSPIRE + full texts (`proposal/REFERENCES_CHECK.md`).
- Trigger text simplified (every arm triggers; no leg/PAIR/prescale in the proposal; the prescale stays in the plan:
  DREAM 96 % live at 1.10 MeV, 88 % at 441 keV with every single).
- GLIMOS: from LNL's "Details for submission" page, not the template. Dylan set spokesperson and GLIMOS = P. Mastinu.
- γ monitor: PF's 2 cm BaF₂ in the proposal (`slot1_feasibility/GAMMA_MONITOR.md`, hand estimates); a 3″×3″ NaI is
  better; neither separates 17.64 from 18.15 MeV, so the LiOH alarm is the γ₀ yield per µC.
- **Run L20** (same-arm pairs at 441 keV, `sim2arm/SAME_ARM.md`): ~2 × 10⁵ selected same-arm IPC per beam day on
  ~5 × 10⁶ pairs from γ conversions in the Cu hemisphere (×22, every angle), θ smeared ~19°. Proposal body + abstract
  reworded: the same-arm pairs measure the holder's conversions and scattering. Also: the 12 % opposite-arm acceptance is
  geometric; with the trigger (small plastics) 0.8 % of X17 pairs remain (§7). §8: same ratio at 1.10 MeV, singles rate
  unchanged, Al holder ~×5 fewer conversions (estimates).
- Site page audited tab by tab (headless Chrome render): stale beam-day/page-limit/gas/framing text fixed; Predictions
  tab rerun with L19 and per-beam-day rates (`sim2arm/predictions.py`, `TA_EPC_RUN=L19`); bug fixed (tasks done in
  plan.py showed as unticked and late).

**In progress / where it stopped:** nothing half-done. No jobs running (L20 clusters 4767948, 4768191 finished clean;
4767947 was held for memory and removed).

**Next steps:**
1. Pierfrancesco's comments on v1 (P6). Still to ask him: BaF₂ diameter/PMT, NaI size, a digitizer channel, current
   measurement on the closed target, CN line, 4 µA, D⁺ level, the hemisphere's measured wall thickness (R14).
2. Dylan: are P3 (INFN-AAI account + Risorse IT, needed to submit on Indico) and P4 (co-proponents) done? Update plan.py.
3. P7 circulate to co-proponents; P10 talk to the LNL ⁸Be group (two red markers left in the body).
4. R13: L19-size γ run in the Al ogive + Cu liner (~5,000 core-h, test cluster first, keep every arm track as L20).
5. Consider rewording the motivation's "acceptance must be large ... MX17 was designed for these requirements": the
   two-arm run has 0.8 % for X17 pairs; the sentence fits the four-arm set-up with large plastics.
6. T5: Geant4 model of the γ monitor once the crystal size is known.

**Gotchas / decisions:**
- A pair run keeps every event: one sub-run of 10⁵ pairs needs ~5 GB in the reduction (held at 3 GB). Use sub-runs of
  2 × 10⁴ (`submit_l20.sh ... 20000 5`).
- Sourcing `MX17_Full_Geant/scripts/setup_lxplus.sh` overwrites shell variables named BASE / CFG: use other names.
- The abstract page is full: the author list will push the table footnote to page 2 (`make` now prints the abstract's
  page count).
- An energy window does not apply to same-arm pairs: one arm holds only 3–12 MeV of a 16.6 MeV pair.

**Key files & commands:**
- `sim2arm/same_arm.py --dir $WORK_DATA/lnl_x17/l20` (tables on EOS `/eos/user/d/dneff/x17/l20/`); lxplus scripts
  `sim2arm/lxplus/{submit_l20.sh,run_job_2trk.sh,twotrack_reduce.py,merge_l20.py}`.
- `WORK_DATA=/media/ucla/work TA_EPC_RUN=L19 ~/PycharmProjects/nTof_x17/.venv/bin/python sim2arm/predictions.py`
- `python3 proposal/figsrc/make_figures.py && make -C proposal/latex`; `python3 site/build_page.py`, then in
  dylan-cern-site `python3 scripts/build.py && scripts/deploy-eos.sh`.

## Gas follow-up: premixes, drift HV history, plots against drift voltage — updated 2026-11-27 (dylan-MS-7C84)

**Resume:** `gas/GAS_STUDY.md` §10–13 done; next is the bench test M5 (drift to 1200 V in Ar/CH₄/CO₂ 93/5/2 and Ar/CO₂/iC₄H₁₀ 93/5/2).

**Done**
- §10 premixes: the CERN store's non-flammable hydrocarbon premixes are Ar/CO₂/iC₄H₁₀ 93/5/2 and Ar/CH₄/CO₂ 93/5/2;
  every other candidate is a custom order (SIAD / Sapio / Air Liquide quote **(ask)**).
- §11 + `gas/hv_history/HV_HISTORY.md`: every CAEN monitor log on EOS. A held 1200 V (bench 26 Jun 4.2 h; n_TOF 3 Jul
  1.9 h), C 1200 V at n_TOF, D leaky at 1200 V, A and B clean at 1000 V. At n_TOF the drift current spiked only in
  Ar/iC₄H₁₀ 95/5 (A 0.39/h, D 2.2/h; none in 88/10/2, 80/20, 90/10): less quencher → drift discharges.
- §13: the n_TOF −2.4 %/K is the water (chain pattern A:C:D = 1:3:3, ~5 %/K of the inflow), not gas density (+0.4 %/K).
- Plots against drift voltage, 400–1200 V, only non-flammable, no-F, ≥ 3 % quencher gases (Dylan 26 Nov):
  `gas/voltage_plots.py` (v, D_T, water spread 0.1–0.5 and 0.5–1 %), `gas/compare_gases.py` (hydrocarbon gases overlaid).
- New Magboltz tables: store premixes (98/2, P5, P10, Ar/CH₄/CO₂ 93/5/2, 86/10/4).

**Next**
1. §12 result: at 1000–1200 V the two store premixes bracket the choice (Ar/CH₄/CO₂ 93/5/2 steady, D_T ~350;
   Ar/CO₂/iC₄H₁₀ 93/5/2 more quencher, D_T ~240); at 0.5–1 % water nothing is steady. Regenerate the figures with
   `python3 gas/voltage_plots.py && python3 gas/compare_gases.py`.
2. Ethane T_ci 7.6 % is recalled; check ISO 10156 Table 2.
3. Bench test M5: drift scan to 1000–1200 V in each candidate gas; log the water and the temperature through a day.

**Gotchas**
- A wait loop `while pgrep -f run_local.sh` matches itself and never ends; use a PID instead.
- Per-table Magboltz logs go to `$WORK_DATA/lnl_x17/gas_logs` (`LOGDIR=` for `run_local.sh`), not the repo.

## Pierfrancesco's answers: the CN runs 24/24, all numbers in beam days — updated 2026-11-27 (dylan-MS-7C84)

**Resume:** everything now counts beam days (24 h at 80 % efficiency, 19.2 h of beam); next: answer PF's γ-energy and GLIMOS questions.

**Done:**
- PF's reply (CERN thread "LNL PAC Proposal Call Dec 10", 26 Nov) summarised in `correspondence/2026-11-26_mastinu_cn_answers.md`:
  24/24 incl. weekends; spot FWHM below 5 mm; 70 L liquid; γ monitor = a 2 cm BaF₂ or a NaI(Tl); D⁺ number to come;
  GLIMOS unknown to him; CN line and 4 µA not answered.
- Beam days (Dylan: 80 % operator efficiency as a safety factor): `planning/two_arm_estimates.py` OPER_EFF, BEAM_DAY_H,
  H441/H110/RUN_BEAM_DAYS (single source; the fits' days of 24 h are converted with `beam_days()`). Day plan unchanged:
  113 h = 5.9 beam days at 1.10 MeV opposite. Limits 2.75 / 3.5 / 4.6 × (was 4.3 / 5.5 / 7.2), Al 0.90 / 1.22 ×,
  244 beam days to 3σ; 441 keV beam day ~170 beam + 54 cosmic pairs (9 %); 1.10 MeV ~340 + 320 (8 %); X17 adds 13.
- Proposal: abstract (8 beam days, 2.7–4.6 ×, table footnote), body (one-sentence definition in "Use of the beam time",
  all counts, request "8 beam days (about 150 hours of beam)", γ-monitor todo). Body still exactly 4 pages.
- Figures: Fig. 2(b) per beam day; Fig. 3 (b)/(c) "1 beam day" / "5.9 beam days"; Fig. 4 in beam days with a LINEAR x
  axis in (a) (0–30), legend moved, arrows in (b) redrawn between rows (HANDOFF item 1 of the entry below).
- plan.py: questions (hours answered, liquid, γ monitor, D⁺, GLIMOS, spot), risk "fewer beam hours" lowered to low/med,
  risks and tasks re-numbered; page template in beam days (reach table, slider default 5.9, chart, banner).
- CN_BEAM.md top update with the old/new table; PLAN.md banner; README read-first; LIQUID_CELLS 70 L.
- x17_facility_search FACILITY.md + dashboard (EXTRA + LOG), site rebuilt and deployed (dylan-cern-site 9f33507).
- Fig. 2 (Dylan, later): the X17 region 125–160° as a light red band with dashed edges in BOTH panels (caption says so).
  An 'emitted, flat' grey area in (a) was tried and removed at Dylan's request. Site redeployed (82a06bc).

**Not touched:** dated study records (`sim2arm/TWO_ARM_STUDY.md`, `EPC_L19.md`, `LI_THICKNESS.md`) keep their days of 24 h.
Not pushed to Overleaf. The uncommitted gas files (`gas/voltage_plots.py`, `gas/figures/*_vs_Vdrift*`, `mixtures.py`) are
another session's and were left alone.

**Next steps:**
1. Reply to PF: γ energies (17.64 / 18.15 MeV and 478 keV) for the monitor choice; the GLIMOS is asked for on LNL's "Details for submission" page (not in the .tex template);
   still ask the line and 4 µA.
2. Dylan proof-reads the changed sentences (`git diff HEAD~1 -- proposal/latex/`), then Overleaf (re-clone, diff first).
3. With 4 µA the run would reach ~1.3 × (below MEG II): decide whether the proposal mentions it.

## Proposal reframed as a test and calibration run; e-mail to Pierfrancesco — updated 2026-11-26 (dylan-MS-7C84)

**Resume:** proposal is now a test/calibration run with Figs. 2 (acceptance) and 4 (road); next: fix Fig. 4, send PF e-mail.

**Goal (Dylan, 26 Nov):** the run cannot compete with MEG II, so the proposal presents it as a test and calibration
run. Its aim: the measured opening-angle distributions agree with Geant4, so that a four-arm physics run can be
proposed for late 2027 with confidence. A coherent, easy read rather than everything we have worked on.

**Done:**
- Abstract and body rewritten (`proposal/latex/abstract_content.tex`, `body_content.tex`; abstract 1 page, body 4):
  new title, "Aim of the run", n_TOF tracks as first evidence, measurements framed as tests of the simulation,
  "What counts as success". Dropped: Li-thickness detail, liquid-cell variants, Al-holder claims in the text, Table I
  (folded into "Use of the beam time"; the table is in commit 22e1f5f). Dylan's D+ sentence kept.
- New Fig. 2 (`proposal/figsrc/acceptance.py` → `sim2arm/out/acceptance_geom.csv`, `acceptance_ipc441.csv`;
  `fig_acceptance()` in make_figures.py): geometric acceptance vs opening angle, one lepton per arm (~12 % at
  125–160°, 21 % near 180°) and both in one arm (below 90°); 441 keV M1 IPC reaching the TPCs per 8 h: 7e5 same arm,
  1.6e4 opposite arms. GEOMETRY ONLY (straight leptons, no Cu scattering, no trigger). Needs the nTof_x17 venv
  (pandas, ipc_born via x17_facility_search/lnl/lnl_rates.py).
- New Fig. 4 "road to the physics run" (`fig_road()`): limit vs days and days to 3σ: this run 195 d, Al holder 21 d,
  four arms 12 d, large plastics ~1 d (estimate), with what this run tests. Old fig_reach kept in the script, not used.
- E-mail draft to Pierfrancesco in the CERN mailbox Drafts (hub draft id 2806, reply to the "LNL PAC Proposal Call
  Dec 10" thread); copy in `correspondence/2026-11-26_DRAFT_email_mastinu_questions.md`. Dylan is rewriting it.
  H2+ and 4 µA are in a "to confirm" section (PF already said both should be possible).

**In progress / where it stopped:** nothing half-done. Not on Overleaf, site page not redeployed (the page still has
the old framing).

**Next steps:**
1. Fig. 4 (Dylan): fix the arrow placement in panel (b); count days consistently as 8-hour days (46 h = 5.75 days,
   not 1.92); linear x axis in panel (a). [Done 26 Nov evening, in beam days of 19.2 h instead: see the entry above.] Re-check the 4-page fit after.
2. Dylan sends the e-mail. Points discussed for it: CN lines (7 lines; full current only on −15°, 0°, +15°; PF's
   Li targets run on 0°); the spot (LNL: 2–8 mm FWHM; our sims σ = 2 mm Gaussian; the Li disc is Ø 6–8 mm, so 13–32 %
   of a σ = 2 mm beam misses it); "Commission II" (probably an INFN CSN; ask which and the deadline).
3. When PF confirms H2+ and 4 µA: mark both answered in `planning/plan.py` QUESTIONS, decide whether the proposal asks
   up to 4 µA (2.0 × instead of 4.3 × in the 46 h), rebuild page and redeploy.
4. Same-arm pairs: a Geant4 selection with the holder and a single-arm trigger (red to-do in the text); check the DREAM
   live time (298 µs per event) with a single-arm trigger at 441 keV (218 Hz legs per arm).
5. R13 still open: Fig. 4's Al-holder steps rest on 2 simulated holder conversions; run it or mark them estimates.
6. Push to Overleaf (re-clone, diff first; Overleaf = commit 7320379 text before this rewrite), then site page.

**Gotchas / decisions:**
- Body is exactly 4 pages in draft mode; any added sentence needs a cut. Fig. heights: Fig. 1 4.25 cm, Fig. 2 1.6 in,
  Fig. 3 1.75 in, Fig. 4 1.8 in.
- `make_figures.py road` prints the days and the "beats MEG II / excludes ATOMKI" days (this run: 8.3 / 35.6 d of 24 h).

**Key files & commands:**
- `~/PycharmProjects/nTof_x17/.venv/bin/python proposal/figsrc/acceptance.py` (Fig. 2 inputs)
- `python3 proposal/figsrc/make_figures.py [event acc pred road photos]`, then `make -C proposal/latex && make -C proposal/latex zip`

## Micromegas gas study for LNL — updated 2026-11-26 (dylan-MS-7C84)

**Resume:** `gas/GAS_STUDY.md` is done; the choice waits on the bench test M5 and on how dry the gas can be kept.

**Done**
- Drift limit from the n_TOF run configs: A (det3) sparked at 800 V (run_51, 17 Jul), ran 550–600 V, then 700 V for all four
  in production (runs 77–162). Design ≤ 700 V on B (31.3 mm gap) = 224 V/cm; 800 V = 256 V/cm stretch.
- ISO 10156:2017 (Tci iC₄H₁₀ 3.4, CH₄ 8.7; K Ar 0.55, CO₂ 1.5, CF₄ 2): Ar/iso ≤ 1.9 % (98/2 flammable), NSW 93/5/2 just non-flammable, P10 flammable.
- Magboltz, 141 tables on the desktop (18 mixtures × water 0–1.5 %, 200 ppm O₂ point, 303 K check), HEED primaries.
  Result: water moves the v peak up; only Ar/iC₄H₁₀ 98.2/1.8 and Ar/CH₄ 96/4 peak inside the window at 0.1–0.5 % water
  (spread 7–8 % at ~175 V/cm), at the cost of D_T ~520–570 µm/√cm. 93/5/2 spreads 39 %. No gas is stable at 0.5–1 % water.
- plan.py: gas item, L2, LNL question, gas lines → critical, new task M5 (bench test), new risk (drift limit / water).

**Next**
1. M5: ask CEA whether the bench can run our premix; gain/spark + drift scans in 98.2/1.8 (or CH₄ 96/4) and 96.5/2/1.5.
2. Simulate the effect of D_T 250 vs 550 µm/√cm on the angle resolution (MX17 response sim).
3. Supplier quote for a certified 98.2/1.8 premix (below the 1.9 % limit) and Ar/CH₄ 96/4.

**Gotchas**
- `gas/magboltz/run_local.sh` needs nTof_x17 `garfield_sim/setup_garfield.sh`; it skips tables already in `gas/out/tables`.
- The operating field in `analyze.py` minimises the spread over a water band, with v ≥ 16.5 µm/ns (32 DREAM samples).

## Plan and proposal reworked for L19 and the Li film; loose threads — updated 2026-11-26 (dylan-MS-7C84)

**Resume:** proposal/plan/page reworked for L19 + Li film; next: decide R13 (Al-holder EPC run) before the 8 Dec freeze.

**Goal (Dylan, 26 Nov):** rework the plan and the affected parts of the proposal with what runs L19 (external
conversions ×100) and the Li-thickness study taught us, and list the other loose threads to study more carefully.

**Done:**
- Full L19 reach grid (`sim2arm/run_l19_full.sh`, `run_l19_all.sh`; tags `_pass4li11_l19`, `_pass4_l19`): horizontal,
  vertical, four arms, both veto levels, 11 and 20 µm. `planning/two_arm_estimates.py` reads it (`SIM_TAG`), so the page
  tables and Fig. 3 are on L19. Reference row reproduced (195 / 320 / 551 d).
- Checks (`sim2arm/run_l19_checks.sh`, `TA_COS_SCALE` knob added to `two_arm_nd.py`): cosmic rate × 2.5 → 230 d, 4.7 ×
  in the 46 h (beam background dominates the fit region, 825 vs 72 pairs/day); muon segments 3° instead of 15° → 184 d
  (closes the old Fig. 2 "which level" gotcha: it costs 6 %); 4 µA → 2.0 × (was 1.7 ×). `sim2arm/EPC_L19.md` §8.
- Proposal: 4.3 / 5.5 / 7.2 ×; ~200 d to 3σ; 441 keV day ~70 beam pairs (a third external conversions), rate to 14 %;
  1.10 MeV: ~140 beam pairs, EPC ~40 and signal-like, day 8 measures them; rates "for a film of 11 µm, known to ~50 %",
  thickness from the 1.10 MeV / 441 keV yield ratio; 6.9 / 3.6 × for a film 0.5 / 1.5 × as thick; Al holder "about a
  factor of 9"; Table I; abstract 4.3–7.2 ×. Fig. 2 from the L19 spectra (EPC drawn with its own shape), Fig. 3 legend
  headroom; both figures ~0.15 in shorter and several phrases tightened to keep the body at 4 pages.
- plan.py: R13, R14, T4 new; R9, R12, P5, the H₂⁺ / hours / hemisphere / liquid-cell risks and the 4 µA question updated.
  CN_BEAM.md §4 table on L19, PLAN.md banner, README; x17_facility_search FACILITY.md + dashboard (LOG line). Site deployed.

**Loose threads (Dylan asked):**
1. **R13, Al holder EPC** — the proposal's "factor of 9", "about 20 days", "1.4–1.9 ×" rest on 2 simulated conversions;
   L19 showed the Cu conversions are signal-like. An L19-size run of `ogAl300cu12r8m4` (~5,000 core-h, test cluster
   first, condor-campaign skill) before 8 Dec, or soften the Al claims.
2. **R14, Geant4 model of opposite-arm conversions** — now the largest beam component in the fit region (308/825 per
   day); they need a large-angle scatter in the 300 µm Cu. Day 8 checks the dome rate, not that tail; the 441 keV day
   checks it only with H₂⁺. Not needed for the proposal; before the run.
3. **T4, day-1 film check** — thresholds and the LaBr₃ efficiency at 478 keV and 17–18 MeV.
4. Small: R9 cosmic normalisation (now shown to cost ≤ 18 % in days); the LiOH conversion rate is unknown (T2's test).

**In progress / where it stopped:** nothing half-done. No jobs running (local or condor). Dylan has not yet read the
tightened proposal text: the phrases shortened to keep 4 pages are listed in the commit diff of cb517b3
(`git show cb517b3 -- proposal/latex/body_content.tex`), e.g. the Fig. 3 caption, "We estimate about a day …",
"(45 selected pairs)", "with a 25 times lower cosmic-ray trigger rate".

**Next steps:**
1. Dylan: proof-read body §II (2)–(3), §III (rates paragraph, Expected sensitivity) and Fig. 2/3 in Overleaf.
2. R13: Dylan to say yes/no. If yes: L19-style run of `ogAl300cu12r8m4` with the `condor-campaign` skill (test
   cluster, `sim2arm/lxplus/submit_l19.sh` as the template, ~5,000 core-h), then `TA_CFG=ogAl300cu12r8m4 TA_EPC_RUN=…`
   fits (see `run_r10.sh`) and `two_arm_estimates.py` (`AL_TAGS`). If no: soften the Al sentences (Target ¶ "factor of
   9", Expected sensitivity "about 20 days", "1.4 to 1.9 ×", abstract "1.4–1.9 ×").
3. Send PF the questions already in plan.py (film IBA mapping, film change time, LaBr₃, 4 µA → 2.0 ×, nights → 2.66 ×).
4. R14 and T4 before the run (not for the proposal).

**Gotchas:**
- Body page budget: exactly 4 pages in draft mode (red todos shown) with no slack; any added sentence needs a cut.
  Figures are now 1.85 in (Fig. 2) and 1.9 in (Fig. 3) tall in `make_figures.py`; Fig. 3(a) ylim goes to 30 to clear
  the legend.
- `make_figures.py` Fig. 2(a) still takes the vertical cosmic rows from `two_arm_spectra_pass4li11.csv` (the L19 spectra
  have no vertical pair); cosmics do not depend on the γ run.
- `two_arm_nd` with `-j 14` on the 'all' pair died silently once while the gas session ran 16 Magboltz jobs; `-j 6` worked.
- Overleaf clone for this session was `$CLAUDE_JOB_DIR/tmp/overleaf` (temporary): re-clone next time, diff first.
- `gas/` is another session's (untracked); not touched.

**Key files & commands:**
- `proposal/latex/body_content.tex`, `abstract_content.tex`; `make -C proposal/latex && make -C proposal/latex zip`
- `proposal/figsrc/make_figures.py` (Fig. 2 from `sim2arm/out/two_arm_spectra_pass4li11_l19.csv`, Fig. 3 from
  `planning/out/two_arm_reach.csv`)
- `planning/two_arm_estimates.py` (`SIM_TAG = "_pass4{film}_l19"`), `planning/plan.py` (R13, R14, T4)
- `sim2arm/EPC_L19.md` §8, `slot1_feasibility/LI_THICKNESS.md` §8, `slot1_feasibility/CN_BEAM.md` §4
- Refit: `sim2arm/run_l19_full.sh 12 && sim2arm/run_l19_all.sh 6` (~15 min), then `python3 planning/two_arm_estimates.py`,
  `python3 proposal/figsrc/make_figures.py`, `python3 site/build_page.py`, site `scripts/build.py && scripts/deploy-eos.sh`
- Overleaf: `git clone https://git.overleaf.com/6afdf0e8d237ac71ebb14b1f`; last push e7c1990 (= repo cb517b3 text)

## External conversions at ×100 (L19) and the Li film's ±50 % — updated 2026-11-26 (dylan-MS-7C84)

**Resume:** both studies are done and written up. Next: Dylan decides the proposal wording (suggestions in
`sim2arm/EPC_L19.md` §7, not applied because the proposal is also being edited on Overleaf and in another session), then
redraw Fig. 2 from `sim2arm/out/two_arm_spectra_pass4li11_l19.csv` and replace the limits.

**Goal (Dylan, 25 Nov):** a better simulation of the external conversions, which rested on 2 MC events; and the
implications of a Li film whose thickness and homogeneity are known only to ~50 %.

**Done:**
- **Run L19** (`sim2arm/EPC_L19.md`): 3.0e10 ⁸Be γ in the built hemisphere (×100 L18, analog), MX17_Full_Geant
  `lnl_twoarm` 07bea64 (records the γ's first interaction; `--gamma-kill-escape` exists but is not used). Cluster 4762099:
  6,000 jobs × 10 sub-runs of 5e5, all exit 0, no holds or retries, 97 % CPU, 2.3 GB peak, ~4,800 core-h. Per-job pair
  tables on EOS `lnl/L19/gam_8Be_dome300_asb/sel/`; merged `$WORK_DATA/x17_facility_search/sel_l19/` (`combine_l19.py`).
  - L19 agrees with L18 at every step. Selected EPC: 21/day at 1.10 MeV (L18 17), **74/day at 441 keV (L18 1.4)**;
    signal-like θ shape (peaks 140–160°). Fit (`TA_EPC_RUN=L19`, `run_l19.sh`): 195 d to 3σ (was 151), **46 h: 4.3 / 5.5 /
    7.2 × R(ATOMKI)** (was 3.8 / 5.0 / 7.0), 5 d: 2.66 ×. 87 % of the opposite pairs start in the Cu dome, 10 % the rim.
- **Li thickness** (`slot1_feasibility/LI_THICKNESS.md`, `sim2arm/li_thickness.py`): yields ∝ t; 46 h limit (with L19)
  6.9 / 4.3 / 3.55 × at 0.5 / 1 / 1.5 × 11 µm; unevenness at the right mean +3–18 % in days; unevenness + LiOH reaches
  441 keV (36 % of γ₀ from 17.64 at ±50 % spread and half converted; days ×2.3–4.5). In-situ thickness from the
  1.10 MeV / 441 keV γ₀ yield ratio (441 yield independent of t above ~4 µm) and 478 keV PIGE. Kept 10–12 µm nominal.
- plan.py (risk, 2 questions, T3, R12), PREDICTIONS.md and CN_BEAM.md banners, page headline, x17_facility_search
  FACILITY / README / dashboard; page and survey deployed.

**Next steps:**
1. Proposal: limits 3.8/5.0/7.0 → 4.3/5.5/7.2 ×; "about 35 ... large uncertainty" → "about 40"; Fig. 2 caption and
   redraw; the 441 keV day (~70 beam pairs in 8 h, a third EPC); one sentence on the film thickness (EPC_L19 §7).
2. `planning/two_arm_estimates.py` and the page tables still read pass 4 (L18 EPC). A full L19 pass (all pairs, all
   vetoes: `two_arm_nd.py reach` with `TA_EPC_RUN=L19`, then `summarize.py`) would make them consistent.
3. Questions to PF/LNL (in plan.py): IBA mapping of the films, film-change time, LaBr₃ for 17.64/18.15 and 478 keV.
4. The Al ogive's EPC was not rerun (R10 rests on 2 events); ~5,000 core-h if the Al holder becomes the plan.

**Gotchas:**
- `lnl_reduce.py` needs ~2 GB per 5e5 γ (it reads the whole ROOT file): keep sub-runs ≤ 5e5 per 3 GB core.
- `li_thickness.py` must pin BLAS threads before numpy (fixed); `TA_EPC_RUN=L19` gives `reach*_l19` outputs.
- L19's tables have no singles (`DROP_SG`); `two_arm_nd` combines only common keys and keeps L18 for singles.
- Test outputs of removed clusters remain on EOS: `lnl/L19t`, `L19t2` (partial), `L19t3` (12 jobs). Safe to delete.

## The run moves to June or July 2027 — updated 2026-11-25 (dylan-MS-7C84)

**Resume:** LNL slot 1: the call allocates 20 Feb – 30 Jul 2027, so the proposal asks for June or July 2027 and the plan was moved forward ~10 weeks.

**Done:**
- Confirmed: the call page says "from February 20th to July 30th, 2026" (typo for 2027); the call PDF gives no period.
  Pierfrancesco said the same in the 25 Nov call (`correspondence/2026-11-25_mastinu_call_period.md`).
- Proposal: beam-time request "in June or July 2027, since both arms will be tested together on cosmic rays by the end of May
  2027"; abstract table "CN, June or July 2027"; B's window repair "February and March 2027". Body still 4 pages. Pushed to Overleaf.
- `planning/plan.py`: go/no-go 14 May; full chain 17 May – 11 Jun; install 14 Jun – 2 Jul; beam ~5–14 Jul; the 30 Jul end of
  period as a hard milestone; task and hardware need-dates moved (bench hardware by 1 Apr); new risk "not ready by July"
  (fallback: the next period, autumn 2027). Page, PLAN.md §5, README, STRUCTURE.md; x17_facility_search FACILITY.md,
  lnl/README.md, dashboard. Site deployed.

- Proposal edits after Dylan's read (25 Nov): the fit sentence (θ, asymmetry, E_sum, a few % shape freedom) moved from
  measurement (3) to the start of "Expected sensitivity", as the method of the projected limits; the TPC resolution is
  "around 1° for cosmic-ray muons". Dylan's own Overleaf edits kept (D⁺ contamination sentence, 92 % efficiency).

**Next steps:**
1. Ask PF: June or July preferred for the CN; what happens if we slip past July.
2. The loans now need answers in Dec–Jan (B's window by March, DREAM from mid-Feb, PMTs/digitizers by end Feb).
3. Open, left as is (Dylan, 25 Nov): "Readiness and safety" is not asked for by the template (only the four request
   bullets are); it pre-answers the technical review. Option: fold chamber status into Apparatus and the neutron/γ/gas
   lines into the "Experimental setup" bullet.

**Gotchas / decisions:**
- Fig. 2(b, c) use level "MM 15° + TOF": cosmic muons are smeared by 15° like electrons (the FEASIBILITY_SIM §19 artefact),
  so the grey cosmic band is conservative; "MM 15° point, μ 3°" would cut it by 89 %. Not checked: which level the 3.8 ×
  limit uses.
- Dylan edits in Overleaf: always `git pull` the Overleaf clone and edit *that* copy, then copy back to the repo. Copying
  the repo file over Overleaf once erased his D⁺ edit (restored).
- dylan-cern-site's branch is `master`, not `main`.

## Budget and inventory: loans from n_TOF and CERN, the hardware at CEA — updated 2026-11-25 (dylan-MS-7C84)

**Resume:** LNL slot-1 budget/inventory; epool read (25 Nov): pool rental 285 CHF/month × ~2 months → €0.6k; scintillator DAQ options in the pool (CERN_EPOOL.md §4); critical €7.4k. Next: ask the pool about LNL; choose the digitizer (LNL V1742 or 4 × DT5730SB).

**Goal:** a detailed slot-1 budget and the central hardware inventory: what we own, borrow or rent, how sure we are of each
loan, and what it costs if a loan falls through.

**Done:**
- Central inventory (`x17_facility_search/inventory/inventory.py` → `INVENTORY.md`): Micromegas A–E (E = det4) at CEA;
  4 good + 20 bad M1, 4 M4, 16 M2 cards; DAQ PC and DREAM core (TCM, network card, large NIM module) "held for MX17" at
  CEA; FEUs + cables back in CEA's common pool; n_TOF's LEMO cables (~60 × 16 ns, 60 × 5 ns, 20 × 2 ns, 20 × 1 ns, Dylan's
  estimate; ~150 connections in the n_TOF module map agree) and ~30 Ts; the Wiener PL512 (DREAM LV).
- `planning/plan.py`: `conf` per loan (`LOAN_CONF`): LEMO cables, Ts and adapters from n_TOF **very likely**; 2 N1081B, N93B,
  3–4 FIFOs, NIM bin, PL512 **hopefully** rented from the CERN pool and taken to LNL; walls, plastics, holder, DAQ PC agreed.
  Fallback (loan-tier) lines for each. Critical €10.6k → **€7.8k** (incl. a €1k CERN rental-fee guess); resistive splitters
  a low-tier upgrade (€0.8k); every loan fails +€62k.
- Page: Hardware tab shows the confidence; Budget tab has a new "Borrowed, rented or provided by others" table + tiles.
- `budget/items.py`: Lean rents the N1081Bs/FIFOs and borrows the LEMO set: €103k → €58.3k. All deployed.

**In progress / where it stopped:**
- Done 25 Nov: epool read with Claude in Chrome. Nothing is issued to Dylan now (14 rentals, all returned by 13 Aug). Catalogue fees
  in `x17_facility_search/inventory/CERN_EPOOL.md`; budget line updated (€1.6k, was a €1k guess). No Wiener PL512 in the pool;
  Dylan rented a Delta SM3545-D (35 V/45 A) 25 Mar–13 Aug on T299563: is that the DREAM LV? (ask)

**Next steps:**
1. (done 25 Nov) epool fees → inventory + BUDGET. LV = Delta SM3545-D (Dylan). Rental ~2 months, for the feasibility study only; the physics run (winter 2027) gets its own plan. Still to ask: may rented modules go to LNL?
2. Ask: CERN pool (off-site rental to LNL, fee), n_TOF (LEMO loan dates), CEA (is the large NIM module a NIM bin? 4 FEUs +
   32 cables from the pool). Count the n_TOF cables by length. Write down what the M2 and M4 cards are.
3. Rate the 9 loans still without a confidence (DREAM FEUs, PMTs, digitizers, VME, HV, Li films, line, stand, γ monitor).

**Gotchas / decisions:**
- Digitizer: the V1742 from LNL stays the choice (Dylan, 25 Nov: "definitely ideal"); the CERN-pool options
  (4 × DT5730SB etc., `x17_facility_search/inventory/CERN_EPOOL.md` §4) are kept in mind as the fallback.
- epool: the rentals list shows a fee of 0 for returned items; fees come from the catalogue. Reading the site's login
  token through JS was blocked (permission check); use the UI pages and read the table DOM instead.
- Adapters and Ts come from n_TOF (Dylan, 25 Nov), so no connector line is critical; T-splitting the walls as at n_TOF.
- `nTof_x17_DAQ/n1081b/n1081b_module_map.py` `_module1()` raises NameError (`sect`) when called alone (not fixed, other repo).
- Another session works in `sim2arm/` here: commit by path only.

**Key files & commands:**
- `planning/plan.py` (HARDWARE, LOAN_CONF, BUDGET, QUESTIONS); `site/template.html` (`loans()`, budget tab)
- `python3 site/build_page.py`, then in dylan-cern-site `python3 scripts/build.py && scripts/deploy-eos.sh`
- x17_facility_search: `python3 inventory/inventory.py`, `python3 budget/build_budget.py` (copy `budget/out/budget.html` to the site)

## The CN instead of AN2000, 8 working days — updated 2026-11-25 (dylan-MS-7C84)

**Resume:** LNL slot-1 budget/inventory; epool read (25 Nov): pool rental 285 CHF/month × ~2 months → €0.6k; scintillator DAQ options in the pool (CERN_EPOOL.md §4); critical €7.4k. Next: ask the pool about LNL; choose the digitizer (LNL V1742 or 4 × DT5730SB).

**Goal:** AN2000 is probably not available and the allocation is 8 days. Rewrite the slot-1 PAC proposal (deadline
10 Dec) for the CN, at 1 µA and working hours only, with the 441 keV point asked for (H₂⁺) but not relied on.

**Done:**
- Proposal (`proposal/latex/`, Overleaf, page): "CN ACCELERATOR"; 8 working days, 8 h of beam each (assumed): day 1
  current scan + 1.10 MeV, day 2 H₂⁺ at 0.883 MV for 441 keV (asked as a question; "we expect some D⁺"; else 1.10 MeV),
  days 3–7 at 1.10 MeV, day 8 arms at 90°. 46 h at 1.10 MeV ≈ 1.9 days of beam ("day of beam" = 24 h, defined in §II).
- Numbers (scaled as 1/√hours from the pass-4 / R10 fits): limit 3.8 / 5.0 / 7.0 × R(ATOMKI) (liquid working / as at
  n_TOF / none), 1.4–1.9 × with the Al holder; ~130 beam + 130 cosmic pairs (rate to 12 %), X17 adds 5; 441 keV: 46 + 23
  pairs in 8 h (18 %); ~45 selected cosmic pairs per night.
- Fits at 2 and 4 µA (`sim2arm/run_cn.sh`; `two_arm_nd.py` reads `TA_IUA`; `sim2arm/out/two_arm_reach_cn*.csv`), 5 days of
  beam: hemisphere 2.35 / 1.58 / 1.08 ×, Al ogive 0.88 / 0.60 / 0.42 ×. For the 46 h: 4 µA gives 1.7 × (hemisphere).
- `slot1_feasibility/CN_BEAM.md` (the analysis: machines, H₂⁺, current, hours, the 8-day table); plan.py questions and
  risks; `two_arm_estimates.py` BEAM_PLAN; README, PLAN.md banner, page; x17_facility_search FACILITY.md, lnl/README.md,
  dashboard. Page and survey deployed.

**Next steps:**
1. Pierfrancesco: night running (24 h days → 2.35 ×), >1 µA (4 µA → 1.7 ×), H₂⁺ on the CN (and D⁺ level, may have no
   answer), which line (full current only on −15°/0°/+15°), hours per working day.
2. Update the proposal with the answers; with 24 h days restore the 5-days-of-beam numbers (set `H110`, `H441` in
   `proposal/figsrc/make_figures.py`).

**Gotchas / decisions:**
- Day 8 (arms at 90°) kept rather than more 1.10 MeV (3.8 → 3.5 ×): external conversions rest on 2 MC events (±70 %).
- Rejected for 441 keV: a thick Li foil at 0.80 MeV (adds 10–20 % E1 direct capture, where ATOMKI 2022 claims X17).
- To fit 4 pages: figures at 92 % width, "15 % lower with bench efficiency" only in the Table I caption, "(1.1 W)" and
  the [line, spot, floor] todo removed (still in plan.py).
- `two_arm_estimates.DAYS_ON_RES` stays 5 (csv columns `*_5d`); the page notes the reach tables are for 5 days of beam.
- Overleaf: clone `https://git.overleaf.com/6afdf0e8d237ac71ebb14b1f`, diff against `proposal/latex/` before editing.

**Key files & commands:**
- `slot1_feasibility/CN_BEAM.md`, `proposal/latex/{abstract,body}_content.tex` (`make` prints the page count)
- `python3 proposal/figsrc/make_figures.py`; `python3 planning/plan.py`; `python3 site/build_page.py`, then in
  dylan-cern-site `python3 scripts/build.py && scripts/deploy-eos.sh`

## Proposal audited against the LNL call and rebuilt around figures — updated 2026-11-25 (dylan-MS-7C84)

**Resume:** LNL slot-1 budget/inventory; epool read (25 Nov): pool rental 285 CHF/month × ~2 months → €0.6k; scintillator DAQ options in the pool (CERN_EPOOL.md §4); critical €7.4k. Next: ask the pool about LNL; choose the digitizer (LNL V1742 or 4 × DT5730SB).
and on the page. Next: Dylan's read, then the open items below to Pierfrancesco (P6).

**Goal (Dylan, 25 Nov):** audit the beam-use proposal against what LNL asks, clean up the presentation, make it
figure-heavy, get it close to ready.

**What the audit found (rules: `proposal/STRUCTURE.md` §1–2, re-read from the LNL pages on 25 Nov)**
- The template wants three sections (Scientific Motivation / Proposed Experiment / Rate Estimates and Beam Time Request),
  the request as beam / target / set-up / days, figure captions below and table captions above. The old draft had five
  sections, captions beside the figures and under the tables. Fixed.
- Body length: the template says 4 pages, the LNL submission page "strictly" 5. Kept to 4.
- The call's allocation period is 20 Feb – 30 Jul 2027 (the page prints 2026); we ask for the second half of 2027.
- AN2000: "up to 1000 nA on all beamlines except 0°", but "150 nA at small radius". Every rate assumes 1 µA.
- The abstract page still needs the GLIMOS, the author list and Dylan's affiliation (red markers).

**Done**
- **Figures** (`proposal/figsrc/make_figures.py`, drawn at print size from `sim2arm/out/` and `planning/out/`):
  Fig. 1 = photo of MX17 at n_TOF + the run-145 tracks of arms A and C (`make_ntof_fans.py`, real data, 15,930 tracks) +
  a Geant4 event of the two-arm set-up with the target holder (from `events3d.json`: X17 event 1238, muon 6819);
  Fig. 2 = Geant4 predictions (cosmic rays before/after the vetoes, the 441 keV day, the five 1.10 MeV days);
  Fig. 3 = expected limit against days + days to 3σ from this run to the full experiment. One table (days + rates).
- **Text** rewritten in Dylan's style around the figures; references checked on arXiv/INSPIRE (MEG II now EPJC 85, 763;
  PADME JHEP 11 (2025) 007; Hanoi Universe 10, 168; n_TOF set-up NIM A 1072, 170087). The reference list is run-in
  (`\cite` is redefined in `macros.tex` to print the number of `\label{ref:key}`), which saves three lines.
- **Two independent reviews** (a referee read and a number audit against the tables) and their fixes:
  - the 1.10 MeV days are now justified by what they measure (the pair rate in the signal region to 8 %, the E1 and
    external-conversion backgrounds that the 441 keV day does not test), not by the limit; the text says the run does
    not improve on MEG II;
  - **the pair rates and the reach assume fully efficient chambers** (only the track fractions carry ε = 0.92): with
    ε² the pairs are 15 % lower (2.35 → ~2.55 × R(ATOMKI), an arithmetic scaling). Said in the Table I caption and text;
  - "loses about 1 MeV" is the pair's energy sum, not each lepton; the opening angle is smeared by 24° (σ68,
    SHAPES_GEANT.md); 15 % (not 14 %) of X17 pairs in the E_sum window; the leg coincidence is 20 ns (the PAIR window
    50 ns); the resonance is at 1.03 MeV; day 8 at 11 µm gives ~1,500 conversions per day, not "several thousand";
  - the cosmic rate is 25× lower at trigger level (12× after selection); absolute cosmic rates carry the factor 2.5 of
    PREDICTIONS §5; the external conversions in the window rest on 2 MC events (87 in 5 d, ±70 %);
  - the light-holder numbers are labelled as scaling estimates everywhere. **The audit thinks they may be optimistic
    by ~×1.8** (the §19.3 base used σ_t 0.3 ns and the L4 cosmics; a like-for-like scaling gives ~19 d, 0.83 ×).
- **The 478 keV line of ⁷Li(p,p′γ)**, which the simulation does not have (`slot1_feasibility/GAMMA_478_ESTIMATE.md`, a
  literature estimate): ~10⁷ γ/s at 1.10 MeV and 1 µA (±30 %, Taskaev 2021 / Mateus 2002), none at 441 keV (threshold
  0.546 MeV); it cannot make a leg; a few kHz of singles per Micromegas, ~20 kHz above 100 keV per scintillator layer,
  ~0.8 µSv/h at 1 m. One sentence in the proposal. The same note: fluorine in the lithium is the contaminant to ask
  about (¹⁹F(p,αγ): 10⁻³ F per Li would add 20 % of the 17–18 MeV γ yield).
- plan.py: P5 active, R8 done, three new questions (beam spot at 1 µA, the allocation period, 4 or 5 pages).

- **R10 done (25 Nov, `sim2arm/R10_AL_OGIVE.md`): the lighter holder (Al ogive + Cu liner) simulated in two arms** from
  its own tables (L12 + the ×30 L13, fetched from EOS): 21.1 d to 3σ and **0.88 × R(ATOMKI)** in 5 d with the liquid
  working, 1.19 × as at n_TOF, 1.70 × without (11 µm, horizontal). The old scaling (10.4 d, 0.62 ×) was optimistic.
  Four arms, same fit: 11.6 / 22.6 d (not the 4.5 / 8.5 d of §19.3, made on thin tables). `two_arm_estimates.py` now
  reads these rows (`AL_TAGS`); proposal text, abstract and Fig. 3 use them ("0.9 to 1.2 ×", "about 20 days",
  "about 12 days with four arms", "about a day with large plastics", the last one still a scaling).
- **R10 propagated (25 Nov, later session):** the 0.6–0.8 × estimate is replaced by the simulated 0.88–1.19 × in
  `site/template.html`, `plan.py` (R10 done, risk text, T1), `slot1_feasibility/PLAN.md` (§1 and the §4 table, rebuilt
  from `planning/out/two_arm_reach.csv`), `sim2arm/TWO_ARM_STUDY.md` (§0, §7, §9), and x17_facility_search
  `lnl/FACILITY.md`, `lnl/README.md` (new read-first block) and `survey/dashboard.py` (EXTRA + LOG). Page and survey
  rebuilt and deployed. Overleaf checked: identical to `proposal/latex/`.
- The site repo's branch is `master` (origin also has a stale `main`): push `master`.

**Open items for Dylan / Pierfrancesco (red in the PDF)**
1. GLIMOS, authors and affiliations; one sentence after talking to the LNL ⁸Be group.
2. Is a beam day 24 h on AN2000 in self-service? All "per day" numbers assume 24 h.
3. 1 µA on a ~5 mm spot on a line that is not 0°?
4. The γ monitor (LaBr₃ or NaI) for the normalisation; installation time in the hall (~2 weeks assumed).
5. Whether a lighter holder can exist for this run; the flammable-gas rules; the liquid's type and flash point.
6. Second half of 2027 against the 20 Feb – 30 Jul allocation period.
7. Fig. 1b shows n_TOF data (already in the MPGD26 proceedings): check that the collaboration is fine with it here.

**Gotchas**
- The body is exactly 4 pages with about three lines of slack. `make` prints the page count.
- revtex4 floats: `[b]` goes on the current page if it fits, `[t]` to the top of the next page.
- `figures/limit_vs_days.*` is no longer used by the proposal (the page still shows it).
- `make_ntof_fans.py` needs the nTof_x17 venv and the run-145 files; its paths are repointed in the script
  (`/media/dylan/data/x17/sept26_prelim/…`).

## Proposal rewritten in Dylan's style, beam request table — updated 2026-11-24 (dylan-MS-7C84)

**Resume:** LNL slot-1 budget/inventory; epool read (25 Nov): pool rental 285 CHF/month × ~2 months → €0.6k; scintillator DAQ options in the pool (CERN_EPOOL.md §4); critical €7.4k. Next: ask the pool about LNL; choose the digitizer (LNL V1742 or 4 × DT5730SB).
2026-11-24 through Overleaf's git: `git clone https://git.overleaf.com/6afdf0e8d237ac71ebb14b1f`). Next: S8 (questions to
PF), R8 (Fig. 1 render).

- Overleaf had two edits by Dylan (19 Nov): spokesperson = P. Mastinu (body; now also the abstract) and a todo asking for the
  beam request as a template table (done). Before editing here, clone Overleaf and diff it against the repo first.
- `figures/limit_vs_days.pdf` on Overleaf is now an uploaded file, no longer linked from the site.

- Abstract and body prose rewritten per `nTof_x17/papers/WRITING_STYLE.md` (one claim per sentence, terms defined, R_ATOMKI
  defined once, MEG II quoted as 2.07 × R_ATOMKI). Numbers: Cu hemisphere pass 4 (TWO_ARM_STUDY §0, PREDICTIONS.md).
- Changed claims: §1's four-arm light-holder reach was "one to two weeks / about a day" (that was the Cu ogive); now
  "about 5 to 9 days as built, less than a day with large plastics" (Al ogive + Cu liner, FEASIBILITY_SIM §19.3, at the
  old σ_t 0.3 ns). Abstract (iv) now quotes 2.35 × and 0.6–0.8 × (estimate). Table II caption said "three energies": two.
- Beam request table at the bottom of the abstract page, template style (|c| columns, hlines): p, 0.441 MeV 1 day /
  1.10 MeV 7 days, ≤ 1 µA, continuous, metallic Li 10–12 µm on Cu 300 µm (backing = the hemisphere: confirm with PF).
- To fit 4 pages: Fig. 1 and Fig. 2 captions beside the figures, tables and references in \footnotesize, a −0.6 cm before
  the references.

## R11: Geant4 of the liquid cell right behind the SiPM wall — updated 2026-11-21 23:50 (dylan-MS-7C84)

**Resume:** LNL slot-1 budget/inventory; epool read (25 Nov): pool rental 285 CHF/month × ~2 months → €0.6k; scintillator DAQ options in the pool (CERN_EPOOL.md §4); critical €7.4k. Next: ask the pool about LNL; choose the digitizer (LNL V1742 or 4 × DT5730SB).
S8 (questions to PF), R5 (Overleaf), R8 (Fig. 1).

- R11 (830 jobs) + R11b (900 jobs, ×3–4 beam MC; clusters 4712563–4712567), all clean (001 = 005, exit 0).
- Horizontal, 11 µm, LNL calibrated: direct 284 d (raw 266) against 189 d for pass 4; transplant 47 d is not valid here
  (86 % of the arm energy in the liquid, the transplant keeps the baseline's energy shapes). R11-only: 197 / 43 d, so the
  thin MC was optimistic. Acceptance ×2.5 (toy ×4.2), cosmics ×3.5, γ₁ ×7 in the signal region.
- Outputs `sim2arm/out/summary_reach_r11li11.csv`, `_r11.csv`; R11-only `*_r11*only.csv`; diagnostics `sim2arm/r11_diag.py`.
- The fit cache `sim2arm/out/parts/<what><tag>/` is keyed by the task, not the tables: clear it when the tables change.
- EPC uses the configuration's own gam_8Be (`tp_epc='own'`); L3 is only the baseline's.
- Not simulated: a higher liquid leg threshold, a cosmic veto. Tables on `$WORK_DATA/x17_facility_search/sel_r11/`
  (chunks on EOS `lnl/target/sel_r11/`).

## Liquid cells in the baseline, predictions table in the proposal — updated 2026-11-20 (dylan-MS-7C84)

**Resume:** LNL slot-1 budget/inventory; epool read (25 Nov): pool rental 285 CHF/month × ~2 months → €0.6k; scintillator DAQ options in the pool (CERN_EPOOL.md §4); critical €7.4k. Next: ask the pool about LNL; choose the digitizer (LNL V1742 or 4 × DT5730SB).

- **PF's e-mail of 20 Nov** (`correspondence/2026-11-20_mastinu_target_liquid.md`): the Cu hemisphere works ("at least for
  the forward angles"), an engineering thesis on the holder is requested; the liquid exists, the cans must be remade,
  PMTs are short; "4 cm in parallel or 2 cm in series" to discuss.
- **Decided (Dylan):** the proposal assumes two 45 × 45 × 2 cm liquid cells in new cans = the simulated "liquid working"
  row (2.35 × R(ATOMKI) in 5 d). Proposal: abstract, Fig. 1 label/caption, Arms paragraph, §3 item 4, §5 (wide liquid
  as the alternative to big plastics), target paragraph (holder study at LNL). Body still 4 pages.
- **New Table I in §3:** Geant4 predictions (PREDICTIONS.md §2–4) with what each checks. The 3D Fig. 1 of R8 is not done
  (needs the PNG saved from the Predictions tab in a browser).
- **`slot1_feasibility/LIQUID_CELLS.md`:** thickness (PF's options), and a volume budget for wider cells within ~60 L
  (2 arms: 70 × 70 × 5 or 80 × 80 × 4 cm; 4 arms: ~60 × 60 × 3 cm) against the §9 acceptance toy. **All estimates.**
- plan.py: S5 done; S6 (thickness Geant4 scan), S7 (oversized-cell Geant4, replace big plastics?), S8 (questions to PF),
  S9 (remake cans); hardware `ls` → make, budget line "New cans" €1.5k (**a guess**); risk; questions; T1 note. Page:
  reach headline and default stack now "liquid working"; set-up view shows the liquid cell by default.
- x17_facility_search: FACILITY.md, inventory `ls`, dashboard LOG (survey redeployed).
- Overleaf is still behind `proposal/latex/` (R5).

## Two-arm study on the built Cu hemisphere + Predictions tab — updated 2026-11-20 (dylan-MS-7C84)

**Resume:** LNL slot-1 budget/inventory; epool read (25 Nov): pool rental 285 CHF/month × ~2 months → €0.6k; scintillator DAQ options in the pool (CERN_EPOOL.md §4); critical €7.4k. Next: ask the pool about LNL; choose the digitizer (LNL V1742 or 4 × DT5730SB).

**Goal:** a slot-1 two-arm reach and a set of Geant4 predictions for every observable of the run, with the target holder
that actually exists, for the LNL PAC proposal (deadline 10 Dec) and the page.

**Done:**
- **Predictions tab** (page `#predict`, `sim2arm/PREDICTIONS.md`): cosmic nights (trigger, 2/1/0-track fractions × ε 0.92,
  θ, Δt, pointing, zenith), beam singles, 441 keV and 1.10 MeV spectra; a three.js view of real Geant4 events (run L17d,
  `--trajdump`, μ added in MX17_Full_Geant `lnl_twoarm` 10229eb) with a save-PNG button. Code: `sim2arm/predictions.py`,
  `sim2arm/events3d.py`, `site/predict_pane.html`, `site/predict.js`, `site/predict3d.js` (inlined by `site/build_page.py`).
- **The target was wrong:** the 19 Nov study (passes 1–3) used the Cu **ogive** of the 27 Oct sketch (`ogCu200`), labelled
  "Cu hemisphere". Redone with the built hemisphere (`dome300`: R 11 mm, 300 µm, rim, grey flange; Dylan caught it):
  - **Run L18** (`sim2arm/lxplus/submit_l18.sh`, `run_job.sh`, eosio staging): ×30 as-built MC, 780 jobs, all clean. Merged
    `/eos/.../lnl/target/sel_l18/` (chunks) → `$WORK_DATA/x17_facility_search/sel_l18/` (`sim2arm/combine_l18.py`).
  - Pass `_pass4` (`TA_CFG=dome300`, default now): 11 µm, horizontal, pointing + 0.6 ns TOF: **151 / 263 / 511 d** to 3σ
    (liquid working / as at n_TOF / none) → R90(5 d) **2.35 / 3.10 / 4.32 × R(ATOMKI)**; MEG II 2.07 ×. Ogive: 25 / 44 / 94 d.
    Al ogive + Cu liner (scaled from the ogive pass 3, estimate): 0.62 / 0.81 / 1.46 ×.
  - Rewritten: TWO_ARM_STUDY §0, section7_plan.md, PREDICTIONS.md, slot1_feasibility/PLAN.md, proposal abstract + body,
    plan.py (T1, R6 done, R7–R10, risk), page, slide note (republished), x17_facility_search FACILITY/README/dashboard.
- n_TOF beam-off cosmic factor 2.5 = the wft track gate (57 % of clean A–C muons fail it), not the chambers (PREDICTIONS §5).

**In progress / where it stopped:** nothing running. Overleaf is behind `proposal/latex/` (edited here).

**Next steps:**
1. T1: ask Pierfrancesco whether a lighter Al end piece (Al ogive + Cu liner, or the flat 45° Al cap) can be made for slot 1.
2. R10: two-arm Geant4 of that end piece, as L18 (`submit_l18.sh` with its geometry string; add a `CFG` in `two_arm_nd`).
3. R8: proposal Fig. 1 = the 3D render (Predictions tab → target/3D view → save PNG); a short predictions table in §3.
4. R5: upload `proposal/latex/` to Overleaf.
5. R9: n_TOF A–C wall coincidences 0.84 Hz vs 0.34 Hz predicted (nTof_x17 `ntof_cosmics/ac_cosmic_rate.py`).
6. Carried over from pass 3: x17_facility_search four-arm LNL tables and ILL/trigger_scint/sipm_wall outputs are still at the
   old σ_t; the four-arm fit sums pairs (fit per pair before quoting); R4 (σ_t with the LNL digitisers).

**Gotchas / decisions:**
- CERN condor sets RequestCpus from RequestMemory at submit (6 GB → 2 CPUs); editing memory later does not change it. These
  jobs peak < 1 GB and run 0.3–0.7 h: ask 4 GB, `longlunch`. With a poor user priority, 6-GB `workday` jobs sat idle 2 h.
- E_sum window scan for the hemisphere (`sim2arm/esum_scan.py`): ±10 %, reference windows kept.
- §4.2, §5 (L16 rotated arms), geom_syst, struct_scan, tof_scan are still the ogive's (ratios carry over).
- The L15 cosmics were simulated with the ogive in place (irrelevant for muons crossing the arms).
- `pred_cosmic_scan.py` (trigger-level rescan) runs interactively on lxplus in ~5 min; outputs `/eos/user/d/dneff/x17/lnl_pred/`.
- `events3d.py` clips tracks on a 70 cm sphere along the segment (else the muons vanish); target outline from the step points.

**Key files & commands:**
- `WORK_DATA=/media/ucla/work bash sim2arm/run_pass.sh _pass4 6 && bash sim2arm/after_pass.sh _pass4` — the reach (~3 h)
- `WORK_DATA=/media/ucla/work ~/PycharmProjects/nTof_x17/.venv/bin/python sim2arm/predictions.py` (then `events3d.py`)
- `python3 site/build_page.py`, then in dylan-cern-site `python3 scripts/build.py && scripts/deploy-eos.sh`

## Two-arm Geant4 study (R1) and the 8-day plan — updated 2026-11-19 (dylan-Yoga, overnight)

**Resume:** LNL slot-1 budget/inventory; epool read (25 Nov): pool rental 285 CHF/month × ~2 months → €0.6k; scintillator DAQ options in the pool (CERN_EPOOL.md §4); critical €7.4k. Next: ask the pool about LNL; choose the digitizer (LNL V1742 or 4 × DT5730SB).
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

**Resume:** LNL slot-1 budget/inventory; epool read (25 Nov): pool rental 285 CHF/month × ~2 months → €0.6k; scintillator DAQ options in the pool (CERN_EPOOL.md §4); critical €7.4k. Next: ask the pool about LNL; choose the digitizer (LNL V1742 or 4 × DT5730SB).

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

**Resume:** LNL slot-1 budget/inventory; epool read (25 Nov): pool rental 285 CHF/month × ~2 months → €0.6k; scintillator DAQ options in the pool (CERN_EPOOL.md §4); critical €7.4k. Next: ask the pool about LNL; choose the digitizer (LNL V1742 or 4 × DT5730SB).
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

**Resume:** LNL slot-1 budget/inventory; epool read (25 Nov): pool rental 285 CHF/month × ~2 months → €0.6k; scintillator DAQ options in the pool (CERN_EPOOL.md §4); critical €7.4k. Next: ask the pool about LNL; choose the digitizer (LNL V1742 or 4 × DT5730SB).
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
