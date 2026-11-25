# How an LNL PAC proposal is built

Researched 2026-11-18 from the LNL pages (sources at the bottom). The official LaTeX / Word templates are attached to
the Indico event (`agenda.infn.it/event/50487/`, behind a bot check: open it in a browser). Downloaded 2026-11-18 into
`lnl_template/` (`TemplateProposalAbstract.tex`, `TemplateProposalBody.tex`: revtex4, 12 pt, A4); the draft now lives in them
(`latex/abstract.tex`, `latex/body.tex`, shared `latex/macros.tex`). The call text adds only: "use the templates and submit only
pdf files".

## 1. The call (Jan 2027 PAC)

- Deadline **10 Dec 2026, 23:59 CET**. PAC meets **25–29 Jan 2027**, hybrid.
- CN and AN2000 are open; Tandem only on the +20 (AGATA) line. A limited number of pulsed-beam days on the CN.
- Allocation period (call page, re-read 2026-11-25): "from February 20th to July 30th, 2026", which must mean 2027.
  Pierfrancesco (18 Nov): probably ~6 months; say in the proposal that we want to measure in the second half of 2027.
  **Settled 25 Nov:** Pierfrancesco confirmed that the call schedules only up to July. The proposal now asks for **June or July 2027**
  (body, beam-time request; abstract, beam table).
- Beam questions: pacbeams@lnl.infn.it. CN/AN2000 coordinator: Anna Selva.

## 2. The document

**Abstract: one page, not counted in the body.** It must give:
1. title;
2. accelerator (AN2000, or CN);
3. experimental set-up (here: MX17, two-arm configuration);
4. spokesperson(s);
5. GLIMOS (Group Leader In Matter Of Safety);
6. all authors and affiliations;
7. a short summary.

**Body: at most 4 pages in 12 pt, tables, figures and references included.** The body template says "should not exceed 4
pages"; the LNL web page says "strictly limited to a maximum of 5 pages" (re-read 2026-11-25). We keep to 4, which
satisfies both. It must contain:
- the scientific motivation;
- the technical details of the measurement: the instrumentation, the quantities to be measured and their precision;
- the number of beam days requested, **justified by count-rate estimates**;
- (continuation experiments only) the status of earlier activities. Not us this time; slot 2 will be one.

**What the template itself asks for** (`lnl_template/TemplateProposalBody.tex`, audited 2026-11-25):
- three sections: *Scientific Motivation*, *Proposed Experiment* ("which experimental setup will be used, special
  requirements, additional detectors"), *Rate Estimates and Beam Time Request*;
- "Estimates of the expected rates are required. The beam time request should specify" **beam** (ion, intensity, energy,
  pulsed or continuous), **target** (isotope, thickness, backing), **experimental setup**, **beam time** (days);
- figure captions below the figures, table captions on top of the tables, a readable character size in tables.

**AN2000 limits that the request touches** (`x17_facility_search/lnl/refs/LNL_Beams_AN2000_CN.txt`): protons to 2 MV,
"up to 1000 nA on all beamlines except the 0 deg one" (20 nA there), and "at small radius, 150 nA is achievable". Every
rate in the proposal assumes 1 µA on a ~5 mm Li spot: **confirm with the Accelerator Division** (red marker in the text).

The body since 2026-11-25 (`latex/body_content.tex`), figure-led, 4 pages:

| § | section | content |
|---|---|---|
| — | abstract page | title block, summary, the beam request table |
| 1 | Scientific Motivation | the anomaly and its status (ATOMKI, Hanoi, MEG II, PADME, the 2026 cosmic-ray paper), the four requirements, what we propose |
| 2 | Proposed Experiment | **Fig. 1** (photo at n_TOF, n_TOF run-145 tracks of two opposite arms, a Geant4 event in the two-arm set-up with the target holder); apparatus; target; **Fig. 2** (Geant4 predictions: cosmic rays, the 441 keV day, the 1.10 MeV days) and the three measurements |
| 3 | Rate Estimates and Beam Time Request | **Table I** (days and Geant4 rates); **Fig. 3** (expected limit against days; days to 3σ from this run to the full experiment); the request in the template's four bullets; readiness and safety |
| — | references | 7 entries, checked on arXiv/INSPIRE 2026-11-25 |

The figures are drawn at their print size by `figsrc/make_figures.py` from `sim2arm/out/` and `planning/out/` (run
`planning/two_arm_estimates.py` first if the reach changed); `figsrc/make_ntof_fans.py` redraws the n_TOF tracks (needs
the nTof_x17 venv and the run-145 files on `/media/dylan/data`).

## 3. Submitting

1. An active **INFN-AAI** account, then request "Risorse IT" (help: calcolo@lnl.infn.it). Do this first: it can take days.
2. Fill the online **Beam Time Request**. A report page follows.
3. From the report page, fill the **Targets Request Form** (can be refilled from the same link).
4. Keep the **confirmation e-mail**: it holds the password for later changes.
5. Upload the PDF (abstract + body) on Indico.

## 4. After submitting

- An internal **technical review** checks beam availability, intensity, energy, the target, the accelerator status, the
  set-up's readiness, radioprotection limits and accident prevention. Spokespersons hear of problems **~7 days before the
  PAC** (≈ 18 Jan 2027).
- The PAC may ask for an **oral presentation: 12 min + 8 min discussion**, hybrid.
- Then the schedule: beam calendars on the LNL site ("Calendars of accelerators"); access registration ≥ 15 days ahead,
  RP training certificate, dosimeters, a declaration of responsibility per shift and a safety data sheet for a new
  experiment; shifts to RP ≥ 3 days ahead.

## 5. What reviewers will look for (our reading, not an LNL rule)

- **Readiness.** The review checks "setup readiness": name who fixes what by when (B's drift, the DREAM loan, PMTs).
- **Count rates → days.** One table from yields to selected pairs per day to days. Ours: `../planning/out/`.
- **Safety.** A flammable premix in the hall, a lithium target (metallic Li is handled in the CN group's glovebox), HV.
- **Relation to the LNL ⁸Be group** (Marchi et al., AN2000 2023–24). The PAC knows them; say what we add (tracking,
  cosmic rejection, a large acceptance) and that we talked to them.
- **Honest reach.** It is a feasibility study; quote the expected limit, and the calibration statistics.

## 6. Overleaf

Project: <https://www.overleaf.com/project/6afdf0e8d237ac71ebb14b1f> ("lnl_x17_pac_proposal", Dylan's account, uploaded
2026-11-18 from `out/lnl_x17_pac_proposal.zip`). Since 2026-11-19 its main document is `main.tex`, which shows the abstract
page and the body as one 5-page PDF (until then it was `abstract.tex`, so Overleaf showed only the abstract). The text lives
in `abstract_content.tex` and `body_content.tex`; `abstract.tex` and `body.tex` wrap each alone for the two Indico uploads,
`preamble.tex` holds the template preamble. Share the project from Overleaf to give co-proponents access.

Overleaf's TeX Live is newer than the desktop's (2023): revtex4 (2001) breaks there on `p{}` and `@{}` tabular columns
("Extra \or"), so tables use `l` columns with `\parbox` cells.

The five figure files in `latex/figures/` (`fig1a_ntof_photo.jpg`, `fig1b_ntof_fans.png`, `fig_event.pdf`,
`fig_predictions.pdf`, `fig_reach.pdf`) are uploaded to Overleaf with the git push; `limit_vs_days.*` is no longer used
by the proposal (the page still shows it).

Floats in revtex4: a `[b]` figure goes on the current page if it fits and a `[t]` figure to the top of the next page, so
each figure is declared about a page before where it should appear. `make` prints the body's page count.

`latex/` compiles locally with `make` (abstract.pdf, body.pdf, proposal.pdf merged, main.pdf; needs revtex4, which is in
`~/texmf/tex/latex/` on the desktop, from Ubuntu's texlive-publishers). `make zip` rebuilds the upload zip. Overleaf and the
repo were identical on 2026-11-19 (no edits had been made on Overleaf). From now on they can drift: pick one as the master
(Overleaf's Git integration can be added as a remote here). 2026-11-24: synced by `git push` to
`https://git.overleaf.com/6afdf0e8d237ac71ebb14b1f` (diff Overleaf against the repo before each push: Dylan edits there).

## Sources

- Call page: <https://www.lnl.infn.it/en/call-for-pac-proposals/>; call text `Text_Call_Jan2027.pdf` (read 2026-11-18).
- Submission details: <https://www.lnl.infn.it/en/details-for-submissions/> (read 2026-11-18).
- Procedures and the vademecum: `x17_facility_search/lnl/refs/LNL_Procedures_for_users.txt`, `LNL_Vademecum_Users_2024_09.txt`.
