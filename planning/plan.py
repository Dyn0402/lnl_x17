"""Single source of the LNL plan: milestones, tasks, hardware, people, questions, risks, budget.

`python planning/plan.py` writes planning/out/plan.json (read by site/build_page.py) and prints a
short status. Edit the lists here, not the page. Dates are ISO; "est" marks an inferred date.

Statuses
  task:     done | active | todo | waiting | blocked
  hardware: ready | fix | borrow | find | buy | make | decide
"""
from __future__ import annotations

import csv
import json
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)

UPDATED = "2026-11-27"
DEADLINE = "2026-12-10T23:59:00+01:00"   # PAC proposal deadline, CET
PAC = ("2027-01-25", "2027-01-29")

# Where things live. The Overleaf link is the edit link: anyone with it can edit (Dylan, 19 Nov).
LINKS = dict(
    indico="https://agenda.infn.it/event/50487/",
    call_pdf="https://agenda.infn.it/event/50487/attachments/145501/242083/Text_Call_Jan2027.pdf",
    overleaf="https://www.overleaf.com/project/6afdf0e8d237ac71ebb14b1f/share#3b1dc1a8e5de4929271724fe938b4ae15b6237ddac75cf8f",  # edit link (Dylan, 19 Nov)
    beams="https://www.lnl.infn.it/wp-content/uploads/Beams_AN2000_CN.pdf",
)

# ----------------------------------------------------------------------------------------------
# Workstreams. Order is fixed: it is also the categorical colour order on the page.
WORKSTREAMS = [
    dict(id="prop", name="Proposal & PAC"),
    dict(id="sim", name="Simulation & reach"),
    dict(id="mm", name="Micromegas & DREAM"),
    dict(id="scint", name="Scintillators & trigger/DAQ"),
    dict(id="target", name="Target & beam line"),
    dict(id="site", name="LNL site, gas & safety"),
    dict(id="run", name="Integration & beam run"),
    dict(id="fund", name="Funding & full experiment"),
]

# ----------------------------------------------------------------------------------------------
# Timeline bars (Gantt). start/end ISO dates; est=True means the dates are a plan, not fixed.
PHASES = [
    # proposal
    dict(ws="prop", name="Write the proposal", start="2026-11-18", end="2026-12-09"),
    dict(ws="prop", name="Technical review → PAC talk", start="2027-01-11", end="2027-01-24"),
    dict(ws="prop", name="PAC meeting", start="2027-01-25", end="2027-01-29", fixed=True),
    dict(ws="prop", name="Schedule the beam days with LNL", start="2027-02-01", end="2027-02-28", est=True),
    # simulation
    dict(ws="sim", name="Two-arm re-reduction of L10–L13 (R1)", start="2026-11-19", end="2026-11-27"),
    dict(ws="sim", name="Two-arm Geant4 config + run plan sim", start="2027-02-01", end="2027-04-15", est=True),
    dict(ws="sim", name="Online analysis + calibration chain", start="2027-03-01", end="2027-06-30", est=True),
    # MM
    dict(ws="mm", name="Repair B's drift window (CEA); new windows optional", start="2027-02-01", end="2027-03-31", est=True),
    dict(ws="mm", name="DREAM loan: 4 FEUs + TCM, busy LEMO", start="2027-02-15", end="2027-04-15", est=True),
    dict(ws="mm", name="Cosmic bench: 2 MM + DREAM", start="2027-04-01", end="2027-05-14", est=True),
    # scint
    dict(ws="scint", name="Find PMTs, digitizers (~24 ch), N1081B", start="2026-12-01", end="2027-02-28", est=True),
    dict(ws="scint", name="Bench tests T1–T4 (trigger, prescale, busy lock)", start="2027-02-15", end="2027-04-15", est=True),
    dict(ws="scint", name="SiPM walls + plastics on cosmics", start="2027-03-15", end="2027-05-14", est=True),
    # target
    dict(ws="target", name="Choose target + holder (with PM)", start="2026-11-20", end="2027-01-31"),
    dict(ws="target", name="Build holder; Li films; LiOH test on the line", start="2027-02-01", end="2027-05-31", est=True),
    # site
    dict(ws="site", name="INFN-AAI account, LNL access, RP training", start="2026-11-19", end="2027-03-31"),
    dict(ws="site", name="Floor plan, line, gas safety file, GLIMOS", start="2027-02-01", end="2027-04-30", est=True),
    # integration
    dict(ws="run", name="Full chain, 2 arms, cosmics", start="2027-05-17", end="2027-06-11", est=True),
    dict(ws="run", name="Ship + install at LNL, cosmic commissioning", start="2027-06-14", end="2027-07-02", est=True),
    dict(ws="run", name="8 CN beam days (18 h of beam each) (June–July 2027; allocation ends 30 Jul)", start="2027-07-05", end="2027-07-14", est=True),
    dict(ws="run", name="First results note", start="2027-07-19", end="2027-09-30", est=True),
    # funding
    dict(ws="fund", name="INFN commission request (preventivi; dates: ask)", start="2027-06-01", end="2027-09-30", est=True),
    dict(ws="fund", name="Full experiment: proposal to the next PAC", start="2027-10-15", end="2027-12-15", est=True),
]

MILESTONES = [
    dict(date="2026-11-18", name="Go from Pierfrancesco: feasibility study, ~8 days", ws="prop", done=True),
    dict(date="2026-11-27", name="Draft v1 complete", ws="prop"),
    dict(date="2026-12-03", name="Draft to co-proponents", ws="prop"),
    dict(date="2026-12-09", name="Submit (one day of margin)", ws="prop"),
    dict(date="2026-12-10", name="Deadline 23:59 CET", ws="prop", hard=True),
    dict(date="2027-01-18", name="Technical-review feedback (~7 d before PAC)", ws="prop", est=True),
    dict(date="2027-01-25", name="PAC 25–29 Jan", ws="prop", hard=True),
    dict(date="2027-05-14", name="Go/no-go: both arms work on cosmics", ws="run", est=True),
    dict(date="2027-07-30", name="End of the call's allocation period (20 Feb – 30 Jul 2027)", ws="run", hard=True),
    dict(date="2027-07-05", name="Beam on target", ws="run", est=True),
]

# ----------------------------------------------------------------------------------------------
# Tasks. due ISO; who = owner (initials or role); dep = ids it waits on.
TASKS = [
    # --- proposal (now → 10 Dec)
    dict(id="P1", ws="prop", due="2026-11-20", who="Dylan", status="done",
         t="Send Pierfrancesco the outline, the two-arm numbers and the questions (spokesperson, GLIMOS, author list). Done 26 Nov (the short version); his answers in correspondence/2026-11-26_mastinu_cn_answers.md"),
    dict(id="P2", ws="prop", due="2026-11-20", who="Pierfrancesco", status="todo",
         t="Informal contact with Anna Selva / the Accelerator Division: the CN (AN2000 probably not available, 25 Nov), 1.10 MeV at 1 µA and H₂⁺ at 0.883 MV, beam hours (PF, 26 Nov: the CN can run 24/24 incl. weekends), line and floor space, June–July 2027 (the call's period ends 30 Jul)"),
    dict(id="P3", ws="prop", due="2026-11-23", who="Dylan", status="todo",
         t="Get the INFN-AAI account + 'Risorse IT' (needed to submit on Indico)"),
    dict(id="P3b", ws="prop", due="2026-11-18", who="Dylan", status="done",
         t="Download the LNL LaTeX template from Indico; move the draft into it; upload to Overleaf"),
    dict(id="P4", ws="prop", due="2026-11-24", who="Dylan", status="todo",
         t="Ask the co-proponents (Massimi, Mengoni, Gervino, Gustavino, Cosentino) to join; collect names + affiliations"),
    dict(id="P5", ws="prop", due="2026-11-27", who="Dylan", status="done", dep=["R1"],
         t="Done 27 Nov: draft v1 sent to Pierfrancesco (abstract page + 5-page body since 27 Nov; 18 h beam days, the BaF₂ γ monitor, checked references). History: draft v1 in Overleaf, abstract page + body of at most 4 pages (LNL template, 12 pt, figures and references included). 25 Nov: audited against the call and rebuilt around three figures (apparatus + n_TOF data + Geant4 event; the Geant4 predictions; reach and the path to the full experiment), template sections, one rates table; Dylan to proof-read. 26 Nov: reworked for run L19 (limits 4.3 / 5.5 / 7.2 ×, ~200 d to 3σ, the 441 keV day ~70 beam pairs of which a third external conversions, Fig. 2 from the L19 spectra) and the Li film known to ±50 % (rates for 11 µm, thickness from the 1.10 MeV / 441 keV yield ratio, 6.9 / 3.6 × for a film 0.5 / 1.5 × as thick)"),
    dict(id="P6", ws="prop", due="2026-11-30", who="Dylan", status="active", dep=["P5"],
         t="Draft to Pierfrancesco; agree the beam-day table and the machine. Sent 27 Nov (Dylan): waiting for his comments"),
    dict(id="P7", ws="prop", due="2026-12-03", who="Dylan", status="todo", dep=["P6"],
         t="Circulate to co-proponents; comments by 7 Dec"),
    dict(id="P8", ws="prop", due="2026-12-08", who="Dylan", status="todo", dep=["P7"],
         t="Freeze text; fill the online Beam Time Request and Targets Request Form (keep the confirmation password)"),
    dict(id="P9", ws="prop", due="2026-12-09", who="Dylan", status="todo", dep=["P8"],
         t="Submit on Indico (event 50487). Deadline is 10 Dec 23:59 CET"),
    dict(id="P10", ws="prop", due="2026-12-04", who="Dylan", status="todo",
         t="Talk to the LNL ⁸Be spectrometer group (T. Marchi et al.) before submitting: how this complements their AN2000 data"),
    dict(id="P11", ws="prop", due="2027-01-22", who="Dylan", status="todo",
         t="PAC talk: 12 min + 8 min discussion; answer the technical-review points"),
    # --- simulation
    dict(id="R1", ws="sim", due="2026-11-27", who="Dylan", status="done",
         t="Two-arm re-reduction of the L11–L13 tables, every pair geometry, new cosmics (L15) and rotated arms (L16): sim2arm/TWO_ARM_STUDY.md (19 Nov)"),
    dict(id="R2", ws="sim", due="2026-11-27", who="Dylan", status="done",
         t="Proposal figures: two-arm acceptance vs θ (Fig. 2), expected spectra at 441 keV and 1.10 MeV (Fig. 3), the road to the physics run (Fig. 4); the rates table folded into the text (26 Nov). Done 27 Nov, full text width"),
    dict(id="R15", ws="sim", due="2026-12-05", who="Dylan", status="done",
         t="Same-arm pairs at 441 keV (run L20, 27 Nov: M1 IPC 17.64 MeV and the 441 keV γ rays, every arm track kept; sim2arm/same_arm.py): selected IPC vs external-conversion background per beam day, θ resolution (Cu scattering ~12° per lepton). Done 27 Nov (sim2arm/SAME_ARM.md): ~2×10⁵ selected same-arm IPC per beam day on ~5×10⁶ pairs from γ conversions in the Cu hemisphere (×22, every angle); θ smeared ~19° by the Cu. The same-arm sample measures the holder's conversions and scattering, not the IPC shape. Proposed wording for the proposal in SAME_ARM.md §4"),
    dict(id="R3", ws="sim", due="2027-04-15", who="Dylan", status="todo",
         t="Geant4: two-arm geometry with the real target holder and stand (MX17_Full_Geant branch from lnl_target)"),
    dict(id="R4", ws="sim", due="2027-06-11", who="Dylan", status="todo",
         t="Timing on cosmics with the LNL readout (V1742/CFD): n_TOF beam-off muons give σ_t 0.52–0.64 ns per arm (walls), 0.95 (plastics) with the n_TOF readout (nTof_x17 ac_tof_beamoff, 19 Nov); decides the TOF cut"),
    dict(id="R5", ws="sim", due="2026-11-27", who="Dylan", status="done", dep=["R1"],
         t="Proposal text from sim2arm: the 441 keV rate (~140 pairs/day above 90° with the built Cu hemisphere), the reach rows (2.35 × R(ATOMKI) in 5 d, liquid working), the vertical-cosmics test. Done 24 Nov: abstract + body rewritten in Dylan's style, beam request table on the abstract page; pushed to Overleaf"),
    dict(id="R6", ws="sim", due="2026-11-20", who="Dylan", status="done",
         t="More as-built MC for the Cu hemisphere: done 20 Nov (run L18, ×30 the L10 tables; the 19 Nov study had used the Cu ogive)"),
    dict(id="R10", ws="sim", due="2026-12-05", who="Dylan", status="done",
         t="Two-arm Geant4 of the lighter Al end piece (Al ogive + Cu liner) from its own tables (L12 + the x30 L13): 21 d to 3 sigma and 0.88 x R(ATOMKI) in 5 d with the liquid working, 1.19 x as at n_TOF, 1.70 x without (11 µm). The old scaling (10 d, 0.62 x) was optimistic. Done 25 Nov (sim2arm/R10_AL_OGIVE.md); the 45° Al cap is not simulated in two arms"),
    dict(id="R11", ws="sim", due="2026-12-05", who="Dylan", status="done",
         t="Geant4 of the liquid cell right behind the SiPM wall (runs R11 + R11b, 21 Nov): no gain. Own MC (direct) 284 d to 3 sigma vs 189 d for the baseline; X17 acceptance x2.5 (toy x4.2), cosmics x3.5, gamma1 x7; the transplant (47 d) does not apply to this layout. Baseline kept (LIQUID_CELLS.md 4.1)"),
    dict(id="R7", ws="sim", due="2026-11-20", who="Dylan", status="done",
         t="Geant4 predictions of every observable of the run (trigger and track fractions, cosmic θ/Δt/pointing, beam singles, 441 keV and 1.10 MeV spectra) and a 3D view of real Geant4 events (run L17): Predictions tab, sim2arm/PREDICTIONS.md (20 Nov)"),
    dict(id="R8", ws="sim", due="2026-11-27", who="Dylan", status="done", dep=["R7"],
         t="Proposal: the Geant4 event as Fig. 1c (drawn from sim2arm/out/events3d.json by proposal/figsrc/make_figures.py, 25 Nov), the predictions as Fig. 2 and the rates in Table I"),
    dict(id="R9", ws="sim", due="2027-03-31", who="Dylan", status="todo",
         t="n_TOF beam-off A–C wall coincidences: 0.84 Hz measured vs 0.34 Hz in the cosmic toy MC; explain before quoting absolute cosmic rates (the chamber-level factor 2.5 is the reconstruction gate). Impact checked 26 Nov (TA_COS_SCALE=2.5, L19): 195 → 230 d to 3σ (days of 24 h), the run's limit 2.75 → 3.0 × R(ATOMKI) in beam days, since the beam background dominates the fit region (825 beam vs 72 cosmic pairs per day)"),
    # --- MM
    dict(id="M1", ws="mm", due="2027-01-15", who="Dylan", status="todo",
         t="Ask Stephan / CEA: repair B's drift window (needed); new aluminised-mylar windows for A and B (low-budget upgrade); dates"),
    dict(id="M2", ws="mm", due="2027-01-15", who="Dylan", status="todo",
         t="Ask CEA for the DREAM loan for Feb–Jul 2027 (bench from April, beam in July): 4 FEUs + 32 cables from CEA's common pool (the TCM, network card, NIM module and DAQ PC are kept for us at CEA); solder the TCM busy LEMO"),
    dict(id="M3", ws="mm", due="2027-03-31", who="Dylan", status="todo",
         t="Optional (high-budget upgrade): 4 CERN-design M1 cards for B. Slot 1 runs B with its existing Italian M1s"),
    dict(id="M4", ws="mm", due="2027-05-14", who="Dylan", status="todo",
         t="Cosmic bench, 2 MM + DREAM: efficiency, segment angle (μ ≲ 3°), noise with B's existing M1s"),
    dict(id="M5", ws="mm", due="2027-04-30", who="Dylan", status="todo",
         t="Gas choice (gas/GAS_STUDY.md §11–12, 27 Nov): bench test of chamber A on cosmics in the two CERN-store premixes, Ar/CO₂/iC₄H₁₀ 93/5/2 (in the proposal) and Ar/CH₄/CO₂ 93/5/2, with the drift at 1000–1200 V: drift HV hold and discharge rate, gain + spark scan, angle resolution and efficiency against the June 95/5 runs, with the water measured. Decide the gas from it; ~2 bottles, ~1 week (ask CEA)"),
    # --- scint / trigger
    dict(id="S1", ws="scint", due="2027-01-31", who="Pierfrancesco", status="todo",
         t="Find PMTs for the 4 small plastics + 2 for the liquid cells (PF, 20 Nov: PMTs are short)"),
    dict(id="S2", ws="scint", due="2027-01-31", who="Pierfrancesco", status="todo",
         t="Digitizers: ~24 channels (16 wall + 4–6 PMT + trigger word) from LNL pool; else ask CAEN for a test loan"),
    dict(id="S3", ws="scint", due="2027-02-15", who="Dylan", status="todo",
         t="Borrow list (25 Nov): LEMO cables + Ts from n_TOF (very likely, returned after the run); 2 N1081B, the N93B, 3–4 linear FIFOs, a NIM bin and the Delta SM3545-D LV rented from the CERN electronics pool and taken to LNL (hopefully); splitters + adapters bought"),
    dict(id="S4", ws="scint", due="2027-04-15", who="Dylan", status="todo",
         t="Bench tests T1, T2, T4 (prescaler, busy lock 1:1, trigger word)"),
    dict(id="S5", ws="scint", due="2026-11-20", who="Dylan", status="done",
         t="Liquid cells decided (PF + Dylan, 20 Nov): the proposal assumes 2 cells, 2 cm thick, one per arm, in new cans (the simulated 'liquid working': 2.35 × R(ATOMKI) in 5 d; 4.3 × without)"),
    dict(id="S6", ws="scint", due="2027-01-31", who="Dylan", status="todo",
         t="Thicker liquid cells: Geant4 scan 2 / 2+2 in series / 4 / 5 cm (PF: '4 cm in parallel or 2 cm in series'); expose the LS dimensions on the MX17_Full_Geant command line (slot1_feasibility/LIQUID_CELLS.md §2)"),
    dict(id="S7", ws="scint", due="2027-02-28", who="Dylan", status="todo",
         t="Wider liquid cells to replace the big plastics, within the 70 L (PF, 26 Nov): oversized-cell Geant4 run at 35/41/47 cm (60–80 cm sides need 27–56 L for 2 arms, ~53 L for 4 arms at 60 × 60 × 3 cm); trigger leg, light collection, PMTs (LIQUID_CELLS.md §3)"),
    dict(id="S8", ws="scint", due="2026-12-05", who="Dylan", status="todo",
         t="Ask PF: how much liquid (70 L, PF 26 Nov), which liquid, who remakes the cans and when, how many PMTs; '4 cm in parallel / 2 cm in series': per arm or in total?"),
    dict(id="S9", ws="scint", due="2027-04-01", who="Pierfrancesco", status="todo", dep=["S8"],
         t="Remake 2 liquid-cell cans (45 × 45 × 2 cm baseline, or the S6/S7 design) and fill them"),
    # --- target
    dict(id="T1", ws="target", due="2026-12-01", who="Pierfrancesco", status="todo",
         t="Target for the proposal: pressed Li on Cu (CN group), 10–12 µm; holder: the Cu hemisphere (already built: R 11 mm, 300 µm, rim; simulated as dome300 since 20 Nov, the 19 Nov numbers used the Cu ogive by mistake); a lighter Al end piece (Al ogive + Cu liner, or a flat Al end cap at 45°) would cut the days ×7 in simulation (R10: 21 d against 151 d to 3σ, liquid working): ask whether one can be made for slot 1. PF (20 Nov): the hemisphere exists and works, 'at least for the forward angles'; he has asked for an engineering thesis on the holder"),
    dict(id="T3", ws="target", due="2026-11-25", who="Dylan", status="done",
         t="What a ±50 % uncertainty on the Li film's thickness and homogeneity does (slot1_feasibility/LI_THICKNESS.md, sim2arm/li_thickness.py): yields, LiOH, reach for 17 film scenarios; in-situ measurement from the 1.10 MeV / 441 keV yield ratio"),
    dict(id="R12", ws="sim", due="2026-11-27", who="Dylan", status="done",
         t="External conversions at x100 statistics (sim2arm/EPC_L19.md, 26 Nov): run L19, 3e10 ⁸Be γ in the built Cu hemisphere, 6,000 clean jobs. Selected EPC pairs on 352 MC events (was 2): 21/day at 1.10 MeV (was 17), 74/day at 441 keV (was 1.4); signal-like θ shape, so 195 d to 3σ (was 151) and 4.3 × R(ATOMKI) in the 46 h (was 3.8 ×; 5.5 / 7.2 × as at n_TOF / no liquid). Proposal numbers updated 26 Nov (P5). Follow-ups 26 Nov: the full reach grid with L19 (sim2arm/run_l19_full.sh, run_l19_all.sh: tags _pass4{,li11}_l19, now read by two_arm_estimates and the page); the reference row reproduced (195 / 320 / 551 d); muon segments at 3° instead of 15° gain only 6 % (184 d); 4 µA gives 2.0 × in the 46 h (was 1.7 ×)"),
    dict(id="R13", ws="sim", due="2026-12-05", who="Dylan", status="todo",
         t="External conversions of the lighter Al holder (Al ogive + Cu liner) at L19 statistics (~5,000 core-h, test cluster first): R10's 21 days to 3σ (26 beam days) and Fig. 4's Al-holder steps rest on 2 simulated EPC events, and L19 showed the EPC shape is signal-like (Cu: 151 → 195 d). Needed before the text freeze (P8) if the Al holder stays in the proposal"),
    dict(id="R14", ws="sim", due="2027-03-31", who="Dylan", status="todo",
         t="How well does Geant4 predict the external conversions that reach two OPPOSITE arms? They need a large-angle scatter in the 300 µm Cu wall (87 % start in the dome, 15 % of the window pairs in the arms' own scintillators/PCBs) and are the largest beam component in the fit region (308 of 825 per 24 h of beam). Day 8 (arms at 90°) measures the dome conversion rate, not this tail; the 441 keV day measures it directly (25 of ~70 pairs) only if H₂⁺ exists. Check: a second EM physics option and the wall-thickness tolerance on an L19-size subsample; ask PF for the measured wall thickness"),
    dict(id="T4", ws="target", due="2027-05-31", who="Dylan", status="todo",
         t="Day-1 film check procedure (LI_THICKNESS.md §6): γ₀ yield per µC at 1.10 MeV vs 441 keV with the γ monitor (PF's BaF₂ 2 cm, 26 Nov; the ratio gives the thickness in the spot), 478 keV PIGE as the fallback without H₂⁺, the γ₀ yield per µC and γ₁/γ₀ as the LiOH alarm (a 2 cm BaF₂ cannot separate 17.64 from 18.15 MeV, GAMMA_MONITOR.md); replace a film below ~0.7 × nominal or whose yield per µC jumps. Write the thresholds into the run plan; needs the monitor's efficiency at 478 keV and 17–18 MeV"),
    dict(id="T5", ws="target", due="2027-03-31", who="Dylan", status="todo",
         t="Geant4 model of the γ monitor (PF's 2 cm BaF₂, or a NaI ≥ 3″×3″): efficiency above threshold for 17.64 / 18.15 / 14.6 MeV and at 478 keV, cosmic-muon rate, mounting (axis horizontal, ~20 cm). Replaces the hand estimates of slot1_feasibility/GAMMA_MONITOR.md; needs the crystal's diameter (ask PF)"),
    dict(id="T2", ws="target", due="2027-05-31", who="Pierfrancesco", status="todo",
         t="Build the holder; make films; a week of LiOH-conversion test on the line"),
    # --- site
    dict(id="L1", ws="site", due="2027-03-31", who="Dylan", status="todo",
         t="LNL access: registration ≥ 15 d ahead, RP training certificate, dosimeters, responsibility declaration"),
    dict(id="L2", ws="site", due="2027-04-30", who="Pierfrancesco", status="todo",
         t="Safety file: non-flammable argon premix bottles in the hall (ISO 10156; the 95/5 plan was flammable), gas panel, exhaust, O₂-deficiency check (gas/GAS_STUDY.md §2)"),
    dict(id="L3", ws="site", due="2027-02-28", who="Pierfrancesco", status="todo",
         t="Floor plan of the line: ~1.5 × 1.5 m around the target, beam height, cable path to the control room, network"),
    # --- run
    dict(id="I1", ws="run", due="2027-06-11", who="Dylan", status="todo",
         t="Full chain on cosmics: 2 arms, DREAM + digitizers on one event list, run control, slow control Tier 1"),
    dict(id="I2", ws="run", due="2027-07-02", who="all", status="todo",
         t="Ship, install, commission on cosmics at LNL: ≥ 3 nights with the arms VERTICAL (σ_t, μ segment angle, MIP gains, each cosmic veto), then roll to horizontal"),
    dict(id="I3", ws="run", due="2027-07-16", who="all", status="todo",
         t="8 CN beam days (18 h of beam each, 27 Nov; PF 26 Nov: 24/24 incl. weekends); shift list sent to RP ≥ 3 days ahead"),
    # --- funding
    dict(id="F1", ws="fund", due="2026-12-15", who="Pierfrancesco", status="todo",
         t="Which commission and when are the requests due? (Pierfrancesco wrote 'commission II'; INFN preventivi are usually prepared in summer: ask)"),
    dict(id="F2", ws="fund", due="2027-11-30", who="Dylan", status="todo",
         t="Full-experiment proposal (4 arms, big plastics) to the next LNL PAC, with the feasibility results"),
]

# ----------------------------------------------------------------------------------------------
# Hardware for slot 1 (two arms): everything the run needs, owned, borrowed, bought or made (Hardware tab).
#   status  what we must do: ready (in hand) | fix | borrow | find | buy | make | decide
#   org     lender or source, for grouping: MX17 collaboration | CEA Saclay | INFN / LNL | CERN (n_TOF / pool) | purchase | our own work
#   src     where it comes from, in words; who = our contact for it
#   state   progress: in hand | agreed | to ask | asked | to find | to order | to make | to decide
#   need    date it must be in hand (the bench tests start Feb–Apr 2027, the cosmic bench April, installation mid-June 2027)
#   b       the BUDGET line that prices it (cash, tier and the cost if a loan falls through come from there)
#   place   where it sits on the Hardware tab's diagram (keys of PLACES in site/template.html)
#   inv     ids in the central inventory (x17_facility_search/inventory/inventory.py): owner, location, condition
#   conf    for a loan or rental: how sure we are to get it (LOAN_CONF); the fallback price is in its BUDGET line
#   tasks   task ids; ids mmA, mmB, mmCD, walls, plast, ls are also the layers of the Set-up view.
LOAN_CONF = ["agreed", "very likely", "likely", "hopefully", "unknown"]

HARDWARE = [
    # --- Micromegas & DREAM
    dict(id="mmA", part="Micromegas A (det3)", qty="1", grp="Micromegas & DREAM", status="ready", org="MX17 collaboration", src="MX17 collaboration",
         who="Dylan", state="in hand", need="2027-04-01", inv=["mmA"], place=["mmA"], tasks=["M4"],
         note="Best chamber: 92.9 % within 5 mm on the bench. Runs as is; a new aluminised-mylar window is a low-budget upgrade. Clean CERN M1 cards.",
         detail="40 × 36 cm active, 30 mm drift, Ar/iC₄H₁₀ 95/5, bulked at CEA in June 2026. Ran at n_TOF in 2026."),
    dict(id="mmB", part="Micromegas B (det2)", qty="1", grp="Micromegas & DREAM", status="fix", org="CEA Saclay", src="CEA Saclay",
         who="Stephan (CEA)", state="to ask", need="2027-03-31", b="Repair B's drift window", inv=["mmB"], place=["mmB"], tasks=["M1", "M4"],
         note="91.3 % on the bench; drift window needs a repair (likely just an electrical connection; needed for the test); a new window is a low-budget upgrade. Its M1 cards were the noisy Italian ones.",
         detail="Amplification is good. The repair is critical for the test; the risk that it is not done in time is low."),
    dict(id="win", part="New aluminised-mylar drift windows", qty="2 (A, B)", grp="Micromegas & DREAM", status="buy", org="CEA Saclay", src="CEA Saclay",
         who="Stephan (CEA)", state="to ask", need="2027-03-31", b="New aluminised-mylar drift windows, A and B", inv=["mmA", "mmB"], place=["mmA", "mmB"], tasks=["M1"],
         note="Low-budget upgrade: aluminised mylar only (the aluminium is the cathode), dropping the 9 µm Cu that triples the material per crossing.",
         detail="x17_facility_search budget item 'windows': ~€2.5k for four (frames, glue, labour), so ~€1.25k for two. Not needed for the test."),
    dict(id="mmCD", part="Micromegas C, D, E (spares)", qty="3", grp="Micromegas & DREAM", status="decide", org="CEA Saclay", src="CEA Saclay",
         who="CEA", state="to decide", need="", inv=["mmC", "mmD", "mmE"], place=[], tasks=[],
         note="C and D are spark-limited (57.8 %, 43.1 %) and need a re-bulk; E (det4) amplifies on only 38 % of its area. Not required for slot 1. C re-bulked would be the spare. All five chambers are at CEA Saclay (25 Nov).",
         detail="Needed for slot 2 (four arms)."),
    dict(id="m1", part="M1 multiplex cards", qty="8 (4 per chamber)", grp="Micromegas & DREAM", status="ready", org="MX17 collaboration", src="MX17 collaboration (CERN + Italian cards)",
         who="Dylan", state="in hand", need="2027-04-01", inv=["m1cern", "m1ital"], place=["m1"], tasks=["M4"],
         note="Clean CERN cards on A; B keeps its noisier Italian cards for slot 1. At CEA: 4 good and 20 bad M1 cards, plus 4 M4 and 16 M2 cards (25 Nov).",
         detail="The noise on B's cards was seen at n_TOF; the cosmic bench (M4) measures it with the LNL set-up."),
    dict(id="m1new", part="CERN-design M1 cards for B", qty="4", grp="Micromegas & DREAM", status="buy", org="purchase", src="CERN design, produced to order",
         who="Dylan", state="to decide", need="2027-03-31", b="4 CERN M1 cards for B (B runs its Italian M1s for the test)", inv=["m1ital"], place=["m1"], tasks=["M3"],
         note="High-budget upgrade toward slot 2 (~€2k each). Slot 1 runs B with its existing Italian cards.",
         detail="x17_facility_search budget item 'm1': 12 cards €24k."),
    dict(id="dream", part="DREAM: FEUs + TCM + cables", qty="4 FEUs, 32 cables; 1 TCM, network card, NIM module", grp="Micromegas & DREAM", status="borrow", org="CEA Saclay",
         src="CEA Saclay: the TCM, network card and NIM module are kept for us; FEUs and cables from CEA's common pool",
         who="Stephan (CEA)", state="to ask", need="2027-04-01", inv=["dream", "dream_feu", "dreamcab"], place=["feu", "tcm"], tasks=["M2"],
         note="Half the n_TOF system. The TCM, the network card and the large NIM module are at CEA for us; the FEUs and cables went back into CEA's common pool, so they must be asked for (25 Nov). Solder a LEMO on the TCM busy output before the run (daq_trigger/PLAN.md §4.2).",
         detail="A loan with a liability (the full 8-FEU system was valued at €72k in the budget). DREAM is busy 298 µs per event: with every single-arm trigger at 1 µA it is 96 % live at 1.10 MeV and 88 % on the 441 keV day (a SINGLE prescale is kept ready, daq_trigger/PLAN.md)."),
    dict(id="busy", part="LEMO on the TCM busy output", qty="1", grp="Micromegas & DREAM", status="make", org="our own work", src="our own work",
         who="Dylan", state="to make", need="2027-04-30", inv=["dream"], place=["tcm"], tasks=["M2", "S4"],
         note="The TCM has a busy output but its LEMO is not fitted. It vetoes the trigger so both systems keep one event list.",
         detail="Check level, polarity and assertion delay on the bench (test T2, daq_trigger/PLAN.md §4.2)."),
    # --- Scintillators
    dict(id="walls", part="SiPM walls + summing boards", qty="2", grp="Scintillators", status="ready", org="INFN / LNL", src="INFN (n_TOF set-up)",
         who="Pierfrancesco", conf="agreed", state="agreed", need="2027-04-01", inv=["walls"], place=["walls"], tasks=["R4"],
         note="16 of 20 bars read, ganged as at n_TOF on the summing boards: 8 channels per wall. Bias ~54 V, ~0.2 mA per wall.",
         detail="EJ-212 bars, 3 × 26 × 500 mm. Pierfrancesco confirmed they can be used (18 Nov 2026)."),
    dict(id="plast", part="Small plastic scintillators 20 × 30 × 2 cm", qty="4 (2 per arm)", grp="Scintillators", status="ready", org="INFN / LNL", src="INFN",
         who="Pierfrancesco", conf="agreed", state="agreed", need="2027-04-01", inv=["plast_small"], place=["plast"], tasks=["S1"],
         note="The scintillators are available; their PMTs went back to the lender (next line).",
         detail="Behind the SiPM wall; trigger and energy."),
    dict(id="pmt", part="PMTs + bases for the plastics", qty="4 (+2 for liquid cells)", grp="Scintillators", status="find", org="INFN / LNL", src="lender to find (INFN / LNL pool)",
         who="Pierfrancesco", state="to find", need="2027-04-01", b="If the PMTs must be bought: 4–6 fast 2″ PMTs + bases", inv=["pmt_small"], place=["plast"], tasks=["S1"],
         note="The n_TOF PMTs went back to their lender. Borrow again or find others that fit; buying is the expensive fallback.",
         detail="Fast 2″ tubes. Ask whether the original lender can lend them again (question for Pierfrancesco)."),
    dict(id="ls", part="Liquid cells 45 × 45 × 2 cm, new cans", qty="2", grp="Scintillators", status="make", org="MX17 collaboration", src="liquid from the n_TOF set-up (70 L, PF 26 Nov); cans remade",
         who="Pierfrancesco / Dylan", state="to make", need="2027-04-01", b="New cans for the 2 liquid cells", inv=["ls"], place=["ls"], tasks=["S5", "S6", "S7", "S8", "S9"],
         note="In the proposal (PF, 20 Nov: 'the liquid we have, the cans have to be remade'). Without them the days to 3σ go up ×2.8 (260 → 735 beam days). 67–76 % pile-up at n_TOF (γ-flash); LNL rates are far lower.",
         detail="2 PMTs and 2 digitizer channels. Thicker (4 cm, or 2 + 2 in series) and wider cells (in place of the big plastics) to study: slot1_feasibility/LIQUID_CELLS.md."),
    # --- Trigger & DAQ
    dict(id="dig", part="Digitizers, ~24 channels", qty="1 V1742 or 2 × V1730", grp="Trigger & DAQ", status="find", org="INFN / LNL", src="LNL pool; else the CERN electronics pool (desktop CAEN DT5730SB); else a CAEN loan",
         who="Pierfrancesco / CAEN", state="to find", need="2027-04-01", b="If no LNL digitizer loan: 4 × DT5730SB (32 ch) rented from the CERN pool", place=["vme"], tasks=["S2"],
         note="16 wall + 4 plastic PMTs (+2 LS) + 2–3 trigger-word + spares. A V1742 (32 ch) covers it. '10–20 channels we could find' (Pierfrancesco).",
         detail="CERN pool options (epool, 25 Nov 2026; x17_facility_search/inventory/CERN_EPOOL.md §4): CAEN DT5730SB desktop, 8 ch, 14 bit, 500 MS/s, 124.38 CHF/month, 5 in stock (4 units = 32 ch, no VME crate needed); CAEN V1720 VME, 8 ch, 12 bit, 250 MS/s, 59.49, only 2 in stock. The pool has no V1742 or V1730. 500 MS/s sampling is 10 times coarser than the V1742; whether it keeps σ_t ≲ 0.5 ns per arm is to check on cosmics (task R4). Price if bought: V1742 €9,500, CAEN offer 26OFC.01101."),
    dict(id="vme", part="VME crate + optical bridge", qty="VME8004B + A4818", grp="Trigger & DAQ", status="borrow", org="INFN / LNL", src="LNL pool",
         who="Pierfrancesco", state="to ask", need="2027-04-01", b="If no VME crate: VME64x tower + bridge from the CERN pool", place=["vme"], tasks=["S2"],
         note="Holds the digitizers; the A4818 links them to the DAQ PC over optical fibre.", detail="Price if bought: CAEN offer."),
    dict(id="n1081", part="N1081B programmable logic units", qty="2", grp="Trigger & DAQ", status="borrow", org="CERN (n_TOF / pool)",
         src="CERN electronics pool: rent and take to LNL; else the LNL pool or a CAEN loan", conf="hopefully",
         who="Dylan / Pierfrancesco / CAEN", state="to ask", need="2027-04-01", b="If no N1081B loan: 2 × N1081B", inv=["n1081b_cern"], place=["nim"], tasks=["S3", "S4"],
         note="The n_TOF trigger for two arms: legs per arm in 20 ns coincidence, PAIR never prescaled, SINGLE ÷P, 1 Hz clock, trigger word, scalers.",
         detail="Pierfrancesco suggested a CAEN test loan. Our n_TOF tooling (trigger_mode.py, poll_modules) runs on N1081Bs, the reason to stay with them. CERN pool: CEP-0594, 70.30 CHF/month each, SPECIAL category, 5 in stock (epool, 25 Nov 2026)."),
    dict(id="timer", part="Dual timer", qty="1 (N93B)", grp="Trigger & DAQ", status="borrow", org="CERN (n_TOF / pool)",
         src="CERN electronics pool: rent and take to LNL; else the LNL pool", conf="hopefully",
         who="Dylan / Pierfrancesco", state="to ask", need="2027-04-01", b="If no dual timer: N93B", inv=["n93b_cern"], place=["nim"], tasks=["S3"],
         note="Hold gate after each trigger, ORed with DREAM's busy.", detail="CERN pool: CEP-4869, 14.96 CHF/month, 19 in stock (epool, 25 Nov 2026). Price if bought: CAEN offer."),
    dict(id="fifo", part="Linear fan-in/fan-outs (428F)", qty="3–4", grp="Trigger & DAQ", status="borrow", org="CERN (n_TOF / pool)",
         src="CERN electronics pool: rent and take to LNL; else the LNL pool", conf="hopefully",
         who="Dylan / Pierfrancesco", state="to ask", need="2027-04-01", b="If no FIFO rental: 3 × CAEN N625", inv=["fifo_cern"], place=["nim"], tasks=["S3"],
         note="As at n_TOF: one per wall sums the top and bottom ends of each segment for the trigger; one fans the 4 plastic PMTs (+2 liquid cells) out to the digitizer and the trigger.",
         detail="x17_facility_search budget item 'fifo': 6 at n_TOF for 4 arms, so 3 for two (4 with the liquid cells). The N625 is €2,290 (CAEN offer 26OFC.01101). CERN pool: LeCroy 428F CEP-4546, 14.76 CHF/month, 16 in stock (epool, 25 Nov 2026)."),
    dict(id="nimbin", part="NIM bin", qty="1–2", grp="Trigger & DAQ", status="borrow", org="CERN (n_TOF / pool)",
         src="CERN electronics pool with the modules (or the large NIM module kept at CEA, ask); else the LNL pool", conf="hopefully",
         who="Dylan / Pierfrancesco", state="to ask", need="2027-04-01", b="If no NIM bin rental: 1 × CAEN NIM8303", place=["nim"], tasks=["S3"],
         note="For the N1081Bs, the timer and the linear FIFOs: 2 × 2 + 1 + 3–4 = 8–9 slots, one 12-slot bin.",
         detail="Is the 'large NIM module' kept with DREAM at CEA the NIM bin the budget counts on (ask Stephan)? CERN pool (epool, 25 Nov 2026): bin UEN01 CEP-9432 12.18 CHF/month (66 in stock) + 300 W supply UEP22M CEP-9331 27.40 + fan tray UEL02M CEP-9643 6.09; or a compact 5-slot CAEN N8302P + N8315 supply, 7.57 + 15.14."),
    dict(id="lemo", part="LEMO cables, Ts, adapters (n_TOF's set)", qty="~110 cables, ~20 Ts, ~20 adapters needed", grp="Trigger & DAQ", status="borrow", org="CERN (n_TOF / pool)",
         src="n_TOF: the cables and connectors of the 2026 set-up, returned after the run", conf="very likely",
         who="n_TOF (Dylan)", state="to ask", need="2027-04-01", b="If no n_TOF LEMO loan: ~110 LEMO cables, 20 Ts, 20 adapters", inv=["lemo_ntof", "lemo_t_ntof"], place=["cables"], tasks=["S3"],
         note="n_TOF has about 60 × 16 ns, 60 × 5 ns, 20 × 2 ns and 20 × 1 ns LEMO cables and ~30 LEMO Ts, plus the small connectors and adapters (Dylan's estimate, 25 Nov). We can very likely borrow them if we return them. The Ts also do the split of the wall channels, as at n_TOF.",
         detail="The count agrees with the n_TOF set-up: ~120 N1081B inputs and outputs in use (n1081b_module_map.py) plus the wall, plastic and FIFO links, ~150 cables for 4 arms. Two arms need about 110: 16 wall channels to the splitters, digitizer and FIFOs (~50), the FIFO sums and plastics to the trigger and digitizer (~20), ~30 between the 2 N1081Bs, the timer and DREAM, the trigger word and the clock (~10). 16 ns ≈ 3.2 m, 5 ns ≈ 1 m at ~5 ns/m."),
    dict(id="split", part="50 Ω resistive splitters for the wall channels", qty="~20", grp="Trigger & DAQ", status="buy", org="purchase", src="to order",
         who="Dylan", state="to decide", need="2027-04-01", b="50 Ω resistive splitters for the 16 wall channels (instead of Ts)", place=["cables"], tasks=["S3"],
         note="Low-budget upgrade. Every scintillator signal goes to the digitizer and to the trigger. The PMTs go through the FIFOs (a T split halved the plastic amplitude at n_TOF). The wall channels can be split with n_TOF's Ts, as at n_TOF; matched splitters avoid the reflections of a T.",
         detail="x17_facility_search budget item 'splitters': resistive splitters €10–84 each (BNC-T to Mini-Circuits ZFRSC-42-S+)."),
    dict(id="pc", part="DAQ PC (DREAM + run control)", qty="1", grp="Trigger & DAQ", status="borrow", org="CEA Saclay", src="CEA Saclay (kept for us)", conf="agreed",
         who="Stephan (CEA)", state="agreed", need="2027-04-01", inv=["daqpc"], place=["pc"], tasks=["M2", "I1"],
         note="Not Dylan's, but kept for MX17 at CEA with the DREAM core (Dylan, 25 Nov 2026). Run control from n_TOF: DREAM + digitizers on one event list.",
         detail="Network at LNL: ask (task L3)."),
    dict(id="switch", part="Network switch", qty="1", grp="Trigger & DAQ", status="ready", org="MX17 collaboration", src="Dylan's own",
         who="Dylan", state="in hand", need="2027-04-01", inv=["switch"], place=["pc"], tasks=[],
         note="Dylan's (19 Nov 2026).", detail=""),
    dict(id="pdu", part="Switched PDU (remote power cycles)", qty="1", grp="Trigger & DAQ", status="buy", org="purchase", src="to order",
         who="Dylan", state="to order", need="2027-04-30", b="Switched PDU (remote power switch)", place=["pdu"], tasks=[],
         note="Low-budget upgrade. N1081B daemons wedge after dirty disconnects; at n_TOF there was no remote reboot.",
         detail="NETIO PowerPDU class (daq_trigger/PLAN.md §7)."),
    # --- Power
    dict(id="lv", part="LV supply 5 V / ~25 A (DREAM)", qty="1", grp="Power", status="borrow", org="CERN (n_TOF / pool)",
         src="CERN electronics pool: the Delta Elektronika SM3545-D that powered DREAM at n_TOF (Dylan, 25 Nov 2026), rented again and taken to LNL; else LNL", conf="hopefully",
         who="Dylan", state="to ask", need="2027-04-01", b="If no LV rental: TDK-Lambda GEN6-100/LN", inv=["lv_dream"], place=["lv"], tasks=["M2"],
         note="4 FEUs at ~5 A + TCM ~5 A. The same supply as at n_TOF keeps the noise conditions we know.",
         detail="Delta Elektronika SM3545-D (0–35 V, 45 A), CERN pool CEP-0127, 24.88 CHF/month, 3 in stock (epool, 25 Nov 2026). Dylan rented one (CEP-01270008) from 25 Mar to 13 Aug 2026 for DREAM at n_TOF. Fallback price: x17_facility_search budget item 'lvfeu' (Datatec, 30 Oct 2026)."),
    dict(id="cernrent", part="CERN electronics-pool rental (NIM modules + LV)", qty="~2 months", grp="Power", status="buy", org="purchase",
         src="CERN electronics pool", who="Dylan", state="to ask", need="2027-04-01", b="CERN pool rental fee: 2 N1081B, N93B, FIFOs, NIM bin, LV", place=[], tasks=["S3"],
         note="The rental itself: about 285 CHF/month for the set in the CERN epool catalogue (25 Nov 2026), so ~€0.6k for the ~2 months of the LNL run (Dylan, 25 Nov 2026; moved to the June–July run on 25 Nov: shipping in mid-June to the return after the beam in July). Whether rented modules may leave CERN for LNL is still to ask the pool. This covers the feasibility study only. The physics measurement (hoped for winter 2027) will need its own plan for the hardware. The N1081B is a SPECIAL support-category item (5 in stock).",
         detail="About mid-June to mid-August 2027. If the pool modules are also used in the full-chain cosmic test (17 May–11 Jun), the rental grows to ~3 months; with the bench tests from February, ~6 months (the high end of the budget line)."),
    dict(id="hv", part="HV: Micromegas drift + mesh, PMTs", qty="1 CAEN unit", grp="Power", status="borrow", org="INFN / LNL", src="LNL pool",
         who="Pierfrancesco", state="to ask", need="2027-04-01", place=["hv"], tasks=[],
         note="Micromegas ≤ 600 V; PMTs negative. Driven by caen_hv_py.", detail="SiPM bias from the walls' own supplies. CERN pool fallback (epool, 25 Nov 2026): CAEN N1470, 4 channels up to 8 kV, CEP-0422, 43.26 CHF/month, 15 in stock; N470 37.16 (21 in stock)."),
    # --- Gas & slow control
    dict(id="gas", part="Gas: non-flammable argon premix bottles (Ar/CO₂/iC₄H₁₀ 93/5/2 or Ar/CH₄/CO₂ 93/5/2, CERN store), regulators, panel", qty="1 panel", grp="Gas & slow control", status="buy", org="purchase", src="to order (via LNL)",
         who="Dylan / LNL", state="to order", need="2027-04-01", b="Gas: premix bottles, regulators, panel", place=["gas"], tasks=["L2"],
         note="No mixer comes from n_TOF. Gas (gas/GAS_STUDY.md §10–12, 26–27 Nov): the chambers have held 1200 V on the drift (A on the bench, A and C at n_TOF), so the two non-flammable premixes in the CERN store bracket the choice at 1000–1200 V: Ar/CO₂/iC₄H₁₀ 93/5/2 (more quencher, less diffusion; named in the proposal) and Ar/CH₄/CO₂ 93/5/2 (steady v). Both need the water below 0.5 %. Until 26 Nov the plan was a low-quencher premix at ≤ 700 V; 95/5 is flammable. Final choice after the bench test (M5).",
         detail="Non-flammable (ISO 10156): no flammable-gas file, ADR class 2.2 shipping. Bottles in the hall still need the safety file (L2). Flow high enough to flush water; the water level matters more than the mixture (GAS_STUDY.md §6)."),
    dict(id="gaslines", part="Low-permeation gas lines", qty="2 arms", grp="Gas & slow control", status="buy", org="purchase", src="to order",
         who="Dylan", state="to order", need="2027-04-01", b="Low-permeation gas lines", place=["gaslines"], tasks=[],
         note="Critical since 26 Nov (Synflex type or metal): at 0.5–1 % water no candidate gas is stable within the 700–800 V drift limit (gas/GAS_STUDY.md §6). n_TOF and the SPS ran with ~1.5 % water.", detail=""),
    dict(id="slow", part="Gas and environment sensors (slow control Tier 1)", qty="1 set", grp="Gas & slow control", status="buy", org="purchase", src="to order",
         who="Dylan", state="to decide", need="2027-04-30", b="Gas and environment sensors (slow control Tier 1)", place=["sensors"], tasks=["I1"],
         note="Low-budget upgrade: T/p/RH, SHT85 cells on the gas line, logger.", detail="x17_facility_search slow_control/SENSOR_OPTIONS.md §6."),
    # --- Target & beam line
    dict(id="tgt", part="Li target films (pressed on Cu)", qty="several", grp="Target & beam line", status="make", org="INFN / LNL", src="LNL CN target laboratory",
         who="Pierfrancesco", state="to make", need="2027-06-01", place=["target"], tasks=["T1", "T2"],
         note="LNL rolls Li to 10–20 µm in an Ar glovebox and presses it onto Cu. 10–12 µm recommended (LiOH). Boron-free.",
         detail="A week of LiOH-conversion test on the line before the run (T2)."),
    dict(id="holder", part="Cu hemisphere target holder", qty="1", grp="Target & beam line", status="ready", org="INFN / LNL", src="LNL (already built)",
         who="Pierfrancesco", conf="agreed", state="in hand", need="2027-06-01", inv=["cu_hemi"], place=["target"], tasks=["T1"],
         note="Already built, so the baseline (Dylan, 19 Nov): R 11 mm, 300 µm, Cu rim, on the grey flange (Geant4 dome300, runs L10 + L18). Not the Cu ogive of the 27 Oct sketch, which the 19 Nov two-arm numbers used by mistake. A flat Al end cap at 45° would be lighter.",
         detail="Confirm it fits the CN line end (question for Pierfrancesco)."),
    dict(id="line", part="CN beam line end + floor space", qty="~1.5 × 1.5 m", grp="Target & beam line", status="borrow", org="INFN / LNL", src="LNL Accelerator Division",
         who="Pierfrancesco", state="to ask", need="2027-06-14", place=["beamline"], tasks=["P2", "L3"],
         note="A line ending in ~1.5 × 1.5 m of open floor, beam height, cable path to the control room.", detail="CN (25 Nov: AN2000 probably not available). Full current only on the small-angle lines (−15°, 0°, +15°); larger angles can drop to 30 %. Working days, mainly daytime."),
    dict(id="stand", part="Two-arm stand", qty="1", grp="Target & beam line", status="decide", org="INFN / LNL", src="LNL mechanics (ask)",
         who="Pierfrancesco", state="to decide", need="2027-06-01", place=["stand"], tasks=["L3", "R3"],
         note="Two opposite arms, faces at ±204 mm from the beam axis. It should roll 90° about the beam: vertical for the cosmic nights, horizontal for the beam days (sim2arm, 19 Nov).",
         detail="Opposite arms are best (turning them toward 140° costs ×1.1–2.5 in days, run L16). Its material goes into the Geant4 geometry (R3)."),
    dict(id="gmon", part="γ-yield monitor: PF's BaF₂, 2 cm thick (baseline, in the proposal 27 Nov); a NaI(Tl) ≥ 3″×3″ if he finds one", qty="1", grp="Target & beam line", status="borrow", org="INFN / LNL", src="Pierfrancesco: a 2 cm BaF₂, or a NaI(Tl) if not too thick (26 Nov). Either works as a γ₀ counter; a NaI ≥ 3″×3″ is better (slot1_feasibility/GAMMA_MONITOR.md, 27 Nov)",
         who="Pierfrancesco", state="to ask", need="2027-06-01", place=["target"], tasks=["I3"],
         note="Normalises every pair rate (γ₀ above a few MeV), gives the film thickness from the γ₀ yield per µC at 1.10 MeV / 441 keV, and the 478 keV PIGE line. BaF₂ 2 cm at ~20 cm, axis horizontal (cosmic muons out of the window), away from the arms: ~7 γ₀/s at 1.10 MeV, ~40/s at 441 keV, ~2.4×10⁴/s of 478 keV (dead-time correction). It cannot separate 17.64 from 18.15 MeV. Hand estimates, slot1_feasibility/GAMMA_MONITOR.md (27 Nov); Geant4 model of the crystal to do.",
         detail="One spare digitizer channel."),
    # --- Logistics
    dict(id="ship", part="Shipping CEA / CERN → LNL and back", qty="", grp="Logistics", status="buy", org="purchase", src="to order",
         who="Dylan", state="to order", need="2027-06-01", b="Shipping CEA/CERN → LNL and back", place=[], tasks=["I2"],
         note="Chambers, DREAM, walls, electronics.", detail="Guess."),
]

# ----------------------------------------------------------------------------------------------
# Slot-1 cash budget, for our planning (not needed in the proposal). Tiers (Dylan, 18 Nov):
#   need = critical for the test; low = low-budget upgrade; high = high-budget upgrade, toward the final
#   measurement; loan = only if that loan falls through. 19 Nov (Dylan): new drift windows are a low-budget
#   upgrade, the repair of B's drift window stays critical.
# (central EUR, low, high, basis). Scaled from x17_facility_search/budget/items.py (2026-11-17).
TIERS = [
    dict(id="need", name="Critical for the test"),
    dict(id="low", name="Low-budget upgrade"),
    dict(id="high", name="High-budget upgrade (toward the final measurement)"),
    dict(id="loan", name="Only if a loan falls through"),
]
BUDGET = [
    dict(item="Repair B's drift window", c=300, lo=0, hi=1000, basis="items.py driftfix (guess)", tier="need"),
    dict(item="Gas: premix bottles, regulators, panel", c=3000, lo=2000, hi=4500, basis="items.py gas", tier="need"),
    dict(item="CERN pool rental fee: 2 N1081B, N93B, FIFOs, NIM bin, LV", c=600, lo=550, hi=1400, basis="CERN epool catalogue monthly fees (read 25 Nov 2026): 2 × N1081B 70.30 + N93B 14.96 + 4 × 428F 14.76 + NIM bin UEN01 12.18 + 300 W PS UEP22M 27.40 + fan tray 6.09 + Delta SM3545-D LV 24.88 = 285 CHF/month; × 2 months (the LNL run, Dylan 25 Nov) × 1.07 €/CHF. Low: 3 FIFOs; high: 2 bins and 4 months (also the June–July cosmic test). Whether the modules may go to LNL is still to ask", tier="need"),
    dict(item="New cans for the 2 liquid cells", c=1500, lo=600, hi=3000, basis="guess (ask PF: CFRP or Al, LNL workshop)", tier="need"),
    dict(item="Shipping CEA/CERN → LNL and back", c=2000, lo=1000, hi=4000, basis="guess", tier="need"),
    dict(item="New aluminised-mylar drift windows, A and B", c=1250, lo=500, hi=2500, basis="items.py windows €2.5k for 4, × 2/4", tier="low"),
    dict(item="Low-permeation gas lines", c=400, lo=250, hi=700, basis="items.py gaslines; critical since 26 Nov (gas/GAS_STUDY.md §8)", tier="need"),
    dict(item="Gas and environment sensors (slow control Tier 1)", c=2500, lo=2000, hi=3200, basis="items.py slowctl", tier="low"),
    dict(item="50 Ω resistive splitters for the 16 wall channels (instead of Ts)", c=800, lo=200, hi=1700, basis="items.py splitters: 20 × €10–84; n_TOF's Ts do the job for the test", tier="low"),
    dict(item="Switched PDU (remote power switch)", c=290, lo=290, hi=400, basis="items.py pdu", tier="low"),
    dict(item="4 CERN M1 cards for B (B runs its Italian M1s for the test)", c=8000, lo=6000, hi=10000, basis="items.py m1: 12 cards €24k → €2k/card", tier="high"),
    dict(item="If no LNL digitizer loan: 4 × DT5730SB (32 ch) rented from the CERN pool", c=1100, lo=800, hi=2200, basis="epool CEP-0579, 124.38 CHF/month each, 5 in stock (25 Nov 2026); 2 months × 1.07 €/CHF; low 3 units (24 ch), high 4 months. If the pool cannot lend off site: V1742 €9,500 (CAEN offer 26OFC.01101)", tier="loan"),
    dict(item="If no N1081B loan: 2 × N1081B", c=13960, lo=13960, hi=13960, basis="CAEN offer, €6,980 each", tier="loan"),
    dict(item="If no FIFO rental: 3 × CAEN N625", c=6870, lo=6870, hi=6870, basis="CAEN offer, €2,290 each", tier="loan"),
    dict(item="If no NIM bin rental: 1 × CAEN NIM8303", c=5110, lo=4390, hi=5110, basis="CAEN offer €5,110 (12 slots); GANIL tender €4,390", tier="loan"),
    dict(item="If no LV rental: TDK-Lambda GEN6-100/LN", c=1850, lo=1700, hi=2400, basis="items.py lvfeu: Datatec, 30 Oct 2026", tier="loan"),
    dict(item="If no n_TOF LEMO loan: ~110 LEMO cables, 20 Ts, 20 adapters", c=5000, lo=3300, hi=6800, basis="items.py splitters: LEMO 00 cable €25–49 made up; T €12–30; LEMO↔BNC adapter €15–40", tier="loan"),
    dict(item="If no VME crate: VME64x tower + bridge from the CERN pool", c=250, lo=0, hi=450, basis="epool (25 Nov 2026): Schroff 7-slot VME64x tower CEP-0542 32.45 + V3718 bridge CEP-0606 73.55 CHF/month, × 2–4 months; none needed with desktop digitizers. To buy: VME8004B + A4818 €4,760 (CAEN offer)", tier="loan"),
    dict(item="If no dual timer: N93B", c=2720, lo=2720, hi=2720, basis="CAEN offer", tier="loan"),
    dict(item="If the PMTs must be bought: 4–6 fast 2″ PMTs + bases", c=12000, lo=6000, hi=24000, basis="guess; Hamamatsu Italia scale", tier="loan"),
]

# ----------------------------------------------------------------------------------------------
# Open questions, by who answers.
QUESTIONS = [
    dict(who="Pierfrancesco", q="Answered 27 Nov (Dylan, Overleaf): spokesperson and GLIMOS both P. Mastinu. History: spokesperson(s) and GLIMOS for the abstract page? 26 Nov: PF has no idea who the GLIMOS is and asks where we saw it: the abstract must give 'the names of the Group Leader In Matter of Safety (GLIMOS)', on LNL's 'Details for submission' page (lnl.infn.it/en/details-for-submissions), not in the .tex template. Who it should be is not stated: ask LNL (pacbeams@lnl.infn.it)."),
    dict(who="Pierfrancesco", q="Answered 26 Nov: the CN can run 24/24, weekends included. We count beam days of 18 h of CN beam (27 Nov; 26 Nov: 24 h at 80 % = 19.2 h): 8 beam days = 144 h, 106 h (5.9 beam days) at 1.10 MeV with the arms opposite: 2.8 × R(ATOMKI) (was 4.3 × for 8 working days of 8 h). Still open: which CN line (−15°, 0°, +15°)? PF did not answer that one."),
    dict(who="Pierfrancesco", q="Can the CN give more than 1 µA at 1.10 MeV? The beam sheet says 1 µA at 0.8–2 MeV; the CN paper's ~4 µA limit is set by neutrons, and ⁷Li(p,n) makes none below 1.88 MeV. In the 5.9 beam days at 1.10 MeV, 4 µA would bring the limit from 2.8 to ~1.35 × R(ATOMKI), below MEG II (2.07 ×; scaled from the L19 4 µA fit, CN_BEAM.md §3). 26 Nov: PF says the spot is smaller than 5 mm FWHM ('5 mm diameter is even more than the FWHM'), so our σ = 2 mm Gaussian is conservative; the current itself not yet answered."),
    dict(who="Pierfrancesco", q="Target for the proposal: pressed Li on Cu in the existing Cu hemisphere: confirm it fits the CN line end?"),
    dict(who="Pierfrancesco", q="Can the stand roll 90° about the beam? Plan (sim2arm): vertical pair for the cosmic nights before the beam, horizontal for the beam days."),
    dict(who="Pierfrancesco", q="Liquid scintillator: 70 L (PF, 26 Nov). Still open: which liquid, who remakes the cans and by when, how many PMTs? '4 cm in parallel or 2 cm in series': per arm or in total? Wider cells could replace the big plastics (LIQUID_CELLS.md)."),
    dict(who="Pierfrancesco", q="The holder thesis: when would a student start, and could a lighter end piece exist before the June–July 2027 run?"),
    dict(who="Pierfrancesco", q="γ-yield monitor: PF (26 Nov) has a BaF₂, 2 cm thick, or can get a NaI(Tl) if it need not be too thick; he asks the γ energies. Answer him: 17.64 and 18.15 MeV counted above ~5 MeV (the γ₀ yield) and 478 keV at 1.10 MeV (Li content, PIGE). The proposal uses his BaF₂ (27 Nov); a NaI ≥ 3″×3″ would be better (6× the rate, partial γ₀/γ₁ separation), GAMMA_MONITOR.md. Still ask: the BaF₂ diameter and PMT, the NaI size, a free digitizer channel, and how the current is measured on the closed target (the yield per µC is the LiOH alarm)."),
    dict(who="Pierfrancesco", q="Li films (LI_THICKNESS.md, 25 Nov): can LNL measure each film's thickness and uniformity before the run (RBS / NRA / PIGE at a few spots, or weighing)? How long does a film change take on the CN line, and how many spare films can we have?"),
    dict(who="Pierfrancesco", q="'Commission II': which INFN commission, and when must the request be in? Results before that date?"),
    dict(who="Pierfrancesco", q="Author list: affiliations for Massimi, Mengoni, Gervino, Gustavino, Cosentino; anyone else (n_TOF, CEA, Torino)?"),
    dict(who="LNL Accelerator Division", q="A CN line (−15°, 0° or +15°, for the full current) ending in ~1.5 × 1.5 m of free floor; beam height; 1 µA at 1.10 MeV? (Spot: PF 26 Nov, FWHM below 5 mm.)"),
    dict(who="LNL Accelerator Division", q="Answered 26 Nov (PF): the CN runs 24/24 including weekends. The plan counts beam days of 18 h of beam (safety factor, Dylan). Confirm the shift / access rules for night running."),
    dict(who="LNL Accelerator Division", q="H₂⁺ from the CN source at 0.883 MV (two 0.441 MeV protons), up to 0.5 µA? 26 Nov: PF says a small D⁺ contamination is possible and he will ask the machine people for a number. The 441 keV calibration depends on H₂⁺; the proposal does not."),
    dict(who="Pierfrancesco", q="Answered 25 Nov: the call allocates 20 Feb – 30 Jul 2027 (the call page prints 2026, a typo), so we aim for June or July 2027 (proposal changed). Still to ask: does LNL prefer June or July for the CN, and what happens if we are not ready by July (the next period, autumn 2027)?"),
    dict(who="Pierfrancesco", q="Body length: the template says 4 pages, the LNL submission page says 5. Since 27 Nov the draft uses 5 (Dylan): fine with him?"),
    dict(who="LNL Accelerator Division", q="Gas: we plan a non-flammable argon premix from the CERN store (Ar/CO₂/iC₄H₁₀ 93/5/2, or Ar/CH₄/CO₂ 93/5/2; ISO 10156 non-flammable). Does LNL agree with the classification, what does it need for bottles in the hall (storage, exhaust, O₂ monitor), and does LNL stock argon premixes?"),
    dict(who="CEA (Stephan, DREAM)", q="Repair B's drift window in February 2027, as the proposal says (and 2 new windows, if cheap)? Lend 4 FEUs + TCM for Mar–Jul 2027?"),
    dict(who="CERN electronics pool", q="Can rented modules go to LNL for ~2 months (mid-June to mid-August 2027): 2 × N1081B, the N93B, 3–4 linear FIFOs, a NIM bin and the Delta SM3545-D LV (and digitizers, if LNL has none)? Catalogue fees ~285 CHF/month for the set (epool, 25 Nov 2026)."),
    dict(who="n_TOF", q="Lend the LEMO cables (~60 × 16 ns, 60 × 5 ns, 20 × 2 ns, 20 × 1 ns) and ~30 LEMO Ts for Mar–Jul 2027, returned after the run?"),
    dict(who="CEA (Stephan, DREAM)", q="Is the large NIM module kept with DREAM a NIM bin with room for our trigger modules? Can 4 FEUs + 32 cables come out of the common pool for Mar–Jul 2027?"),
    dict(who="CAEN", q="A test loan of a V1742 or 2 × V1730 + 2 N1081B for the run (Pierfrancesco's suggestion)?"),
    dict(who="LNL ⁸Be group (Marchi)", q="Status of their 2023–24 AN2000 data; is a joint or complementary run welcome; is the AN2000 room free?"),
    dict(who="Plastics lender", q="Can we borrow the 4 small plastics' PMTs again (or which PMTs fit them)?"),
]

RISKS = [
    dict(r="Drift cathodes do not hold the field the gas needs (A sparked at 800 V at n_TOF), or water in the gas above 0.5 %", l="med", i="med",
         m="The chambers held 1200 V on the drift in June–July 2026 (GAS_STUDY.md §11); at n_TOF the drift discharged only in the least quenched gas (95/5), so we keep ≥ 5 % quencher and test the drift to 1200 V on the bench in each candidate (M5). At 700 V (the old design limit) the store premixes are too slow. Low-permeation lines, a dryer and a water sensor are critical: above 0.5 % water no gas keeps v steady, so v is then calibrated in situ from the cathode edge of the drift-time distribution."),
    dict(r="Micromegas B not repaired in time", l="low", i="high",
         m="Likely just an electrical connection on the drift (Dylan, 19 Nov). A is ready now; C re-bulk as the spare; one-arm-plus-scintillator fallback still gives the 441 keV and background programme."),
    dict(r="DREAM not available in Mar–Jul 2027 (CEA's own use)", l="med", i="high",
         m="Ask now (M2); 4 FEUs is half the system; fix dates with CEA before the PAC talk."),
    dict(r="Too few digitizer channels", l="low", i="med",
         m="Two arms need ~24, PM can find 10–20; CAEN loan; ganged walls keep it at 8 per wall."),
    dict(r="No H₂⁺ beam on the CN, so no 441 keV calibration", l="med", i="med",
         m="Without it the H₂⁺ day is also at 1.10 MeV (the request stays 8 beam days). The energy scale then comes from the 18.15 MeV pairs; the run loses its transition without an expected anomaly, the in-beam film thickness from the 1.10 MeV / 441 keV yield ratio (fallback: 478 keV PIGE, T4) and the direct test of the holder's opposite-arm conversions at 17.64 MeV (a third of the 441 keV pairs, R14)."),
    dict(r="CN gives fewer beam hours than assumed (18 h per beam day) or a shorter block", l="low", i="med",
         m="PF (26 Nov): the CN can run 24/24 incl. weekends; the plan already counts 18 h of beam per day (75 %) as a safety factor. 8 beam days give 106 h at 1.10 MeV: 2.8 × R(ATOMKI) (L19). The reach scales as the square root of the hours: at 8 h per working day (the old assumption) it would be 4.3 ×."),
    dict(r="The built Cu hemisphere limits the physics reach", l="high", i="high",
         m="Simulated (sim2arm; external conversions from run L19, 26 Nov): with the hemisphere's 300 µm wall five days give 2.7 × R(ATOMKI) (liquid working), above MEG II's limit, and the run's 5.9 beam days give 2.8 ×; the holder's conversions are signal-like. A lighter Al end piece (Al ogive + Cu liner) gives 0.9–1.2 × in five days (Geant4, R10, 25 Nov; its conversions rest on 2 MC events: R13). Ask PF whether one can be made (T1); otherwise sell the run as the feasibility test it is."),
    dict(r="Cosmic veto weaker than simulated (σ_t > 0.4 ns, segments worse than 3°)", l="med", i="med",
         m="n_TOF beam-off muons: σ_t 0.52–0.64 ns per arm (19 Nov). Horizontal pair for the beam days: its days barely depend on σ_t (17.4 d with no TOF, 17.7 at any σ_t; sim2arm tof_scan); the vertical pair goes 17.1 → 18.7 d from 0.3 to 0.7 ns. R4 with the LNL readout."),
    dict(r="Liquid-cell cans not remade in time, or PMTs not found", l="med", i="med",
         m="The proposal assumes them (2.8 × R(ATOMKI) in the 5.9 beam days at 1.10 MeV); without them 4.8 ×, the run stays a feasibility test. Ask now (S8); the n_TOF cans as a fallback if they can be reused."),
    dict(r="Li film degrades (LiOH) under beam", l="med", i="med",
         m="10–12 µm films; γ-yield monitor each day; a spare film; a week's conversion test before the run."),
    dict(r="Li film thickness and homogeneity known only to ~50 % (whatever film is made)", l="high", i="med",
         m="slot1_feasibility/LI_THICKNESS.md (25 Nov): the γ rate follows the mean thickness, so the run's limit (5.9 beam days at 1.10 MeV) spans 4.5 × (0.5 × 11 µm) to 2.4 × (1.5 ×) around 2.8 × R(ATOMKI) (scaled to 18 h beam days) (with the L19 external conversions); an uneven film with the right mean costs 3–18 % in days. The danger is unevenness plus LiOH: thick spots reach 441 keV (36 % of γ₀ from 17.64 MeV at ±50 % spread and half the Li converted; days × 2.3–3.7). Measure the film on day 1 (γ₀ yield ratio 1.10 MeV / 441 keV, which does not depend on the film; 478 keV PIGE), watch 17.64/18.15 with the γ monitor, bring spare films, map films by IBA before the run if LNL can. R stays normalised to the γ monitor, so the thickness changes only the statistics."),
    dict(r="Machine-future decision (one machine to replace AN2000 + CN)", l="low", i="high",
         m="Run in 2027 is unaffected; follow the decision (x17_facility_search/lnl/NOTE_CN_AN2000_REPLACEMENT.md)."),
    dict(r="Not ready by July: only ~5 months from the PAC (late Jan) to the end of the allocation period (30 Jul 2027)", l="med", i="high",
         m="Moved from H2 2027 to June–July on 25 Nov (the call covers 20 Feb – 30 Jul). Go/no-go on cosmics by 14 May; B's window and the DREAM loan asked before the PAC (M1, M2); the hardware asks go out in December. If the go/no-go fails, ask LNL to move the 8 days to the next period (autumn 2027, after the August closure)."),
    dict(r="Proposal deadline missed (next call ~a year later)", l="low", i="high",
         m="Draft by 27 Nov; submit 9 Dec; get the INFN-AAI account this week."),
]

# The proposal itself: structure, from https://www.lnl.infn.it/en/details-for-submissions/ (read 2026-11-18).
PROPOSAL = dict(
    rules=[
        "Use the LNL templates (abstract + body, LaTeX or Word); submit PDF only. Abstract: one page (not counted in the body)",
        "Abstract fields: title, accelerator, set-up, spokesperson(s), GLIMOS, all authors + affiliations, short summary",
        "Body: max 5 pages per the LNL submission page ('strictly'; the template text says 4; re-read 25 Nov), 12 pt, tables + figures + references included. We use 5 since 27 Nov",
        "Template sections: Scientific Motivation / Proposed Experiment / Rate Estimates and Beam Time Request; the request lists beam (ion, intensity, energy, pulsed or continuous), target (isotope, thickness, backing), set-up, days; figure captions below, table captions above",
        "Allocation period of this call: 20 Feb – 30 Jul 2027 (call page, read 25 Nov; it prints 2026)",
        "Body must contain: scientific motivation; technical details (instrumentation, quantities measured, precision); beam days from count-rate estimates",
        "Online: Beam Time Request, then the Targets Request Form; keep the confirmation e-mail (password)",
        "Needs an active INFN-AAI account with 'Risorse IT'",
        "Internal LNL technical review before the PAC (beam, target, set-up readiness, radioprotection, safety); issues sent ~7 days before",
        "Possible oral presentation: 12 min + 8 min discussion, hybrid",
    ],
    sections=[
        dict(id="abs", name="Abstract page (with the beam request table)", status="draft", pages=1, owner="Dylan"),
        dict(id="mot", name="1. Scientific Motivation", status="draft", pages=0.6, owner="Dylan"),
        dict(id="exp", name="2. Proposed Experiment (apparatus, target, the three measurements; Figs. 1–2)", status="draft", pages=2.0, owner="Dylan"),
        dict(id="beam", name="3. Rate Estimates and Beam Time Request (Table I, Fig. 3, the request, readiness and safety)", status="draft", pages=1.2, owner="Dylan"),
        dict(id="ref", name="References", status="draft", pages=0.2, owner="Dylan"),
    ],
)

SLOT2 = dict(
    name="Slot 2: the ⁸Be X17 measurement",
    when="2028 (next PAC call, est. late 2027)",
    setup=[
        "Four arms: A, B + re-bulked C and D, new windows on all",
        "Big plastics (4 × ~78 × 80 × 5 cm in-house plates) behind the SiPM walls: ×13–15 in running time; or wide liquid cells from the 70 L we have (~60 × 60 × 3 cm for 4 arms; S7, LIQUID_CELLS.md)",
        "SiPM walls per bar end (FERS, 160 ch) in the Upgrade preset; ganged in Self",
        "Own trigger/DAQ (architecture B or D), DREAM still from CEA",
        "Target from the slot-1 experience (flat Al end cap / Cu ogive, 10–12 µm Li)",
    ],
    programme=[
        "441 keV calibration (17.64 MeV, no anomaly expected)",
        "3σ at R(ATOMKI) at 1.10 MeV, then 0.80 and 1.225 MeV off-resonance (clean points need 5–10 µm films)",
        "The road (proposal Fig. 4, beam days to 3σ at R(ATOMKI), 27 Nov): two arms as built 260; + lighter Al holder 28; + four arms 15; + large plastics ~1.4 (scaling estimate)",
    ],
    budget="Self-sufficient €223k, Upgrade €279k (x17_facility_search budget, 17 Nov 2026); Lean €103k",
)


def reach_rows():
    p = OUT / "two_arm_reach.csv"
    if not p.exists():
        return []
    with open(p) as f:
        return list(csv.DictReader(f))


def beam_rows():
    p = OUT / "beam_days.csv"
    if not p.exists():
        return []
    with open(p) as f:
        return list(csv.DictReader(f))


def inventory() -> dict[str, dict]:
    """The central MX17 inventory (x17_facility_search/inventory/inventory.py), by id; {} if that repo is missing."""
    d = Path.home() / "PycharmProjects" / "x17_facility_search" / "inventory"
    if not (d / "inventory.py").exists():
        print("warning: x17_facility_search/inventory not found; the page shows no owner/location")
        return {}
    import importlib.util
    spec = importlib.util.spec_from_file_location("mx17_inventory", d / "inventory.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return {k: dict(v, avail_l=m.AVAIL[v["avail"]]) for k, v in m.by_id().items()}


def hardware_rows() -> list[dict]:
    """HARDWARE with its BUDGET line merged in: cash (central EUR), lo/hi, tier; for tier 'loan' the cash is 0 and
    'fallback' is the cost if the loan falls through. Every BUDGET line must belong to exactly one item."""
    byname = {b["item"]: b for b in BUDGET}
    used = [x["b"] for x in HARDWARE if x.get("b")]
    assert sorted(used) == sorted(byname), (set(byname) ^ set(used))
    inv = inventory()
    rows = []
    for x in HARDWARE:
        assert x.get("conf", "unknown") in LOAN_CONF, (x["id"], x.get("conf"))
        r = dict(x, cash=0, fallback=0, tier="")
        if inv:
            missing = [i for i in x.get("inv", []) if i not in inv]
            assert not missing, (x["id"], missing)
            r["inv"] = [{k: inv[i][k] for k in ("id", "name", "qty", "owner", "where", "cond", "avail_l", "note")} for i in x.get("inv", [])]
        else:
            r["inv"] = []
        if x.get("b"):
            bl = byname[x["b"]]
            r.update(tier=bl["tier"], lo=bl["lo"], hi=bl["hi"], basis=bl["basis"])
            if x.get("conf"):
                bl["conf"] = x["conf"]
            r["fallback" if bl["tier"] == "loan" else "cash"] = bl["c"]
        rows.append(r)
    return rows


def main() -> None:
    import two_arm_estimates as E  # noqa: E402  (same directory)
    E.main()
    data = dict(
        updated=UPDATED, deadline=DEADLINE, pac=PAC, links=LINKS, tiers=TIERS, workstreams=WORKSTREAMS, phases=PHASES,
        milestones=MILESTONES, tasks=TASKS, hardware=hardware_rows(), budget=BUDGET, loan_conf=LOAN_CONF, questions=QUESTIONS,
        risks=RISKS, proposal=PROPOSAL, slot2=SLOT2, reach=reach_rows(), beam=beam_rows(),
        reach_model=dict(r_atomki=E.R_ATOMKI, r_megii=E.R_MEG2_90, days_on_res=E.DAYS_ON_RES, oper_eff=E.OPER_EFF,
                         beam_day_h=E.BEAM_DAY_H, run_beam_days=E.RUN_BEAM_DAYS,
                         sim_tag=E.SIM_TAG, cal_2arm_per_day=list(E.CAL_2ARM_PER_DAY)),
    )
    (OUT / "plan.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    today = date.today().isoformat()
    due = [t for t in TASKS if t["status"] != "done" and t["due"] <= "2026-12-10"]
    print(f"\nplan.json written ({len(TASKS)} tasks, {len(PHASES)} phases). Before the deadline: {len(due)} open tasks.")
    tot = {t["id"]: sum(b["c"] for b in BUDGET if b["tier"] == t["id"]) for t in TIERS}
    print("Slot-1 cash: critical €{need:.1f}k, + low upgrade €{low:.1f}k, + high upgrade €{high:.1f}k; "
          "if loans fail +€{loan:.1f}k".format(**{k: v / 1e3 for k, v in tot.items()}))
    late = [t["id"] for t in TASKS if t["status"] not in ("done",) and t["due"] < today]
    if late:
        print("Overdue:", ", ".join(late))


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(HERE))
    main()
