# lnl_x17: working notes for Claude

The LNL X17 experiment: slot 1 (two-arm feasibility study, PAC deadline 10 Dec 2026) and slot 2 (the full experiment).
Read `README.md` and the newest `HANDOFF.md` entry first.

- **Numbers come from elsewhere.** Physics, Geant4 reach, targets, budget, DAQ: `~/PycharmProjects/x17_facility_search`
  (`lnl/FEASIBILITY_SIM.md`, `lnl/target/`, `budget/items.py`, `daq_trigger/PLAN.md`, `slow_control/`). Detector geometry:
  MX17_Full_Geant `include/SimConfig.hh`, MX17_Geant `shared/MX17ModuleGeometry.hh`. Cite the section; never re-derive silently.
- **Hardware facts** (owner, location, condition) live in the central inventory `x17_facility_search/inventory/inventory.py`;
  `plan.py` HARDWARE refers to it with `inv=[ids]` and keeps only what this run needs (lender to ask, date, budget line).
- **Scaling estimates are marked as such** until a simulation replaces them (`two_arm_estimates.py` is one).
- **`planning/plan.py` is the single source** for tasks, timeline, hardware, budget, questions and risks. Edit it, then
  `python3 site/build_page.py` and redeploy the site page (redeploy without asking; if the site repo has another session's
  uncommitted work, rsync only `facilities/lnl-feasibility.html` and `facilities/lnl/lnl_x17_pac_proposal.*`).
- Geant4 and heavy reductions run only on lxplus (condor), as in x17_facility_search's CLAUDE.md.
- E-mail: only the threads asked about; summarise decisions in `correspondence/`, no long quotes.
- Mark facts not public as **(ask)**. Date every update; number sections in write-ups.
- When something here changes the LNL picture (machine, dates, verdict), also update
  `x17_facility_search/lnl/FACILITY.md`, its README read-first block and `survey/dashboard.py` (`lnl_cn` EXTRA + LOG).
- Python: system `python3` (numpy, matplotlib) is fine here.
