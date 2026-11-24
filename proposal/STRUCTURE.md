# How an LNL PAC proposal is built

Researched 2026-11-18 from the LNL pages (sources at the bottom). The official LaTeX / Word templates are attached to
the Indico event (`agenda.infn.it/event/50487/`, behind a bot check: open it in a browser). Downloaded 2026-11-18 into
`lnl_template/` (`TemplateProposalAbstract.tex`, `TemplateProposalBody.tex`: revtex4, 12 pt, A4); the draft now lives in them
(`latex/abstract.tex`, `latex/body.tex`, shared `latex/macros.tex`). The call text adds only: "use the templates and submit only
pdf files".

## 1. The call (Jan 2027 PAC)

- Deadline **10 Dec 2026, 23:59 CET**. PAC meets **25–29 Jan 2027**, hybrid.
- CN and AN2000 are open; Tandem only on the +20 (AGATA) line. A limited number of pulsed-beam days on the CN.
- The call does not state the allocation period. Pierfrancesco (18 Nov): probably ~6 months; say in the proposal that we
  want to measure in the second half of 2027.
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
pages"; the LNL web page says 5. We keep to 4. It must contain:
- the scientific motivation;
- the technical details of the measurement: the instrumentation, the quantities to be measured and their precision;
- the number of beam days requested, **justified by count-rate estimates**;
- (continuation experiments only) the status of earlier activities. Not us this time; slot 2 will be one.

Our section plan (`latex/body.tex`), with the page budget planned before the move (now 3¼ pages in the template):

| § | section | pages |
|---|---|---|
| — | abstract page | 1 (separate) |
| 1 | Scientific motivation: the ⁸Be anomaly, its status (ATOMKI, Hanoi, MEG II, the 2026 cosmic-ray critique), what a tracking spectrometer adds | 1.1 |
| 2 | The MX17 apparatus and the two-arm set-up: n_TOF 2026, Micromegas TPC + SiPM wall + plastics, trigger, DAQ, target | 1.0 |
| 3 | Measurements and precision: rates and live time, 441 keV calibration, backgrounds, the 18.15 MeV region | 1.0 |
| 4 | Beam request and count rates: the day-by-day table, rates, what each day yields | 0.9 |
| 5 | From feasibility to the full experiment; requirements and safety (floor, line, flammable gas) | 0.5 |
| — | references | 0.5 |

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

On Overleaf `figures/limit_vs_days.pdf` is a linked file from `https://dylan-neff.web.cern.ch/facilities/lnl/limit_vs_days.pdf`
(copy the new PDF to the site's `facilities/lnl/`, deploy, then Refresh it in Overleaf).

`latex/` compiles locally with `make` (abstract.pdf, body.pdf, proposal.pdf merged, main.pdf; needs revtex4, which is in
`~/texmf/tex/latex/` on the desktop, from Ubuntu's texlive-publishers). `make zip` rebuilds the upload zip. Overleaf and the
repo were identical on 2026-11-19 (no edits had been made on Overleaf). From now on they can drift: pick one as the master
(Overleaf's Git integration can be added as a remote here). 2026-11-24: synced by `git push` to
`https://git.overleaf.com/6afdf0e8d237ac71ebb14b1f` (diff Overleaf against the repo before each push: Dylan edits there).

## Sources

- Call page: <https://www.lnl.infn.it/en/call-for-pac-proposals/>; call text `Text_Call_Jan2027.pdf` (read 2026-11-18).
- Submission details: <https://www.lnl.infn.it/en/details-for-submissions/> (read 2026-11-18).
- Procedures and the vademecum: `x17_facility_search/lnl/refs/LNL_Procedures_for_users.txt`, `LNL_Vademecum_Users_2024_09.txt`.
