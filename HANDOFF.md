# Handoff

## Hardware tab — updated 2026-11-19 (dylan-MS-7C84)

**Done**
- `planning/plan.py` HARDWARE rewritten: 30 items, each with lender (`org`, `src`), contact, state, needed-by date, diagram place,
  tasks. Cash comes from its BUDGET line (`b`), merged in `hardware_rows()`, which asserts every budget line belongs to one item.
- New **Hardware** tab: search, group by system / lender / contact / action / state / tier, action filters, sortable columns,
  totals; a row opens the full entry with its tasks and a schematic of the set-up (from above) with the item highlighted.
  The Set-up tab's old table is gone (it points to the new tab).

**Gotchas**
- Lenders, states and dates are my first fill from the plan and the n_TOF notes; most are "to ask". Correct them in `plan.py`.

## Budget windows, overview, Cu hemisphere — updated 2026-11-19 (dylan-MS-7C84)

**Done**
- Budget (Dylan): new aluminised-mylar drift windows for A and B moved to the low-budget tier (€1.25k); the repair of B's drift
  window stays critical (€0.3k). Critical €9.1k, low +€4.4k, high +€8k. `plan.py`, `slot1_feasibility/PLAN.md` §7, proposal §2.
- Overview: one-line lead with Overleaf + PDF at the top; details and the single Indico link in a box at the bottom; the call-PDF
  link is gone, the machine sheet is a small link in the box.
- Target (Dylan): the Cu hemisphere is already built, so it is the baseline: the "Cu ogive" rows of §19.3. Figure, overview reach
  (1.81 × R(ATOMKI), 0.90 × with liquid cells) and proposal sensitivity (0.9–1.8 ×) switched to it.
  Named "Cu hemisphere (built)" in `two_arm_estimates.py` and listed first, so the Beam & reach tab defaults to it.
- Risk "B not repaired" lowered to low: likely just an electrical connection on the drift (Dylan).
- Overleaf updated. Its `figures/limit_vs_days.pdf` is now a *linked file* from
  `https://dylan-neff.web.cern.ch/facilities/lnl/limit_vs_days.pdf` (the upload dialog wouldn't open): after `figures.py`, copy the
  PDF there, deploy, and press Refresh on the file in Overleaf.

## Overleaf shows the full draft — updated 2026-11-19 (dylan-MS-7C84)

**Resume:** Overleaf's main document is now `main.tex` (abstract + body, 5 pages, compiles there). Next steps unchanged (P1, P3, R1).

**Done**
- Cause: Overleaf compiles one main document and it was `abstract.tex`, so only the abstract showed. The body had also
  never compiled on Overleaf (see gotcha).
- Split `proposal/latex/`: text in `abstract_content.tex`, `body_content.tex`; `preamble.tex`; thin wrappers `abstract.tex`,
  `body.tex` (Indico) and `main.tex` (both). Uploaded to Overleaf through its own upload endpoint, main document set to `main.tex`.
  Overleaf history showed no edits there before the upload.

**Gotchas**
- revtex4 + Overleaf's newer TeX Live: `p{}`/`@{}` columns give "Extra \or". The beam-day table uses `l` columns + `\daycell`.

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
