# Handoff

## The CN instead of AN2000, 8 working days — updated 2026-11-25 (dylan-MS-7C84)

**Resume:** proposal is on the CN, 8 working days; Dylan asks Pierfrancesco the CN questions (P2), then revise the text.

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

**Resume:** `proposal/latex/main.pdf` (1 abstract page + 4 body pages) is the draft for Dylan to proof-read; on Overleaf
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

**Resume:** proposal current in `proposal/latex/` (abstract 1 page, body 4 pages), on the site and on Overleaf (pushed
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

**Resume:** done. Layout C gives no gain (LIQUID_CELLS.md §4.1); the baseline stays in the proposal. Next on the proposal:
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

**Resume:** proposal + page current; next: S8 (ask PF the liquid questions), R5 (Overleaf upload), R8 figure (3D render).

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

**Resume:** all done and live; next: ask PF for a lighter Al end piece (T1), simulate it in two arms (R10), proposal Fig. 1 (R8).

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
