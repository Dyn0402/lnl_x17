# Handoff

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
