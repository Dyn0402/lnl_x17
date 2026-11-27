LNL PAC proposal (Jan 2027 call), MX17 two-arm X17 feasibility study.
Source of truth: GitHub Dyn0402/lnl_x17, proposal/latex/. Official LNL template (Indico event 50487):
  main.tex             - the Overleaf main document: abstract page + body in one PDF
  abstract_content.tex - text of the abstract page (1 page; title, accelerator, set-up, spokesperson, GLIMOS, authors, summary)
  body_content.tex     - text of the body, at most 5 pages per the LNL submission page (12 pt, figures and references included; the template text says 4)
  abstract.tex, body.tex - each part alone, for the two separate Indico uploads
  preamble.tex         - the template preamble; macros.tex - packages and macros
  figures/            - fig1a (photo, n_TOF), fig1b (n_TOF run 145 tracks), fig_event / fig_predictions / fig_reach
                        (drawn by proposal/figsrc/make_figures.py in the repo: do not edit them by hand)
Body sections follow the LNL template: Scientific Motivation / Proposed Experiment / Rate Estimates and Beam Time Request.
The body is 5 pages: after an edit, check that it has not grown to 6.
Edit the *_content.tex files. Red [..] markers are open items; set \draftfalse in macros.tex to hide them.
