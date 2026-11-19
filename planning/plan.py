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

UPDATED = "2026-11-19"
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
    dict(ws="prop", name="Schedule the beam days with LNL", start="2027-02-01", end="2027-03-31", est=True),
    # simulation
    dict(ws="sim", name="Two-arm re-reduction of L10–L13 (R1)", start="2026-11-19", end="2026-11-27"),
    dict(ws="sim", name="Two-arm Geant4 config + run plan sim", start="2027-02-01", end="2027-04-30", est=True),
    dict(ws="sim", name="Online analysis + calibration chain", start="2027-04-01", end="2027-08-31", est=True),
    # MM
    dict(ws="mm", name="Repair B's drift window (CEA); new windows optional", start="2027-02-01", end="2027-04-30", est=True),
    dict(ws="mm", name="DREAM loan: 4 FEUs + TCM, busy LEMO", start="2027-03-01", end="2027-05-31", est=True),
    dict(ws="mm", name="Cosmic bench: 2 MM + DREAM", start="2027-05-01", end="2027-06-15", est=True),
    # scint
    dict(ws="scint", name="Find PMTs, digitizers (~24 ch), N1081B", start="2026-12-01", end="2027-03-31", est=True),
    dict(ws="scint", name="Bench tests T1–T4 (trigger, prescale, busy lock)", start="2027-03-01", end="2027-05-31", est=True),
    dict(ws="scint", name="SiPM walls + plastics on cosmics", start="2027-04-15", end="2027-06-15", est=True),
    # target
    dict(ws="target", name="Choose target + holder (with PM)", start="2026-11-20", end="2027-01-31"),
    dict(ws="target", name="Build holder; Li films; LiOH test on the line", start="2027-02-01", end="2027-06-30", est=True),
    # site
    dict(ws="site", name="INFN-AAI account, LNL access, RP training", start="2026-11-19", end="2027-03-31"),
    dict(ws="site", name="Floor plan, line, gas safety file, GLIMOS", start="2027-02-01", end="2027-05-31", est=True),
    # integration
    dict(ws="run", name="Full chain, 2 arms, cosmics", start="2027-06-15", end="2027-07-31", est=True),
    dict(ws="run", name="Ship + install at LNL, cosmic commissioning", start="2027-08-23", end="2027-09-17", est=True),
    dict(ws="run", name="8 beam days (H2 2027)", start="2027-09-20", end="2027-10-01", est=True),
    dict(ws="run", name="First results note", start="2027-10-01", end="2027-11-30", est=True),
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
    dict(date="2027-06-15", name="Go/no-go: both arms work on cosmics", ws="run", est=True),
    dict(date="2027-09-20", name="Beam on target", ws="run", est=True),
]

# ----------------------------------------------------------------------------------------------
# Tasks. due ISO; who = owner (initials or role); dep = ids it waits on.
TASKS = [
    # --- proposal (now → 10 Dec)
    dict(id="P1", ws="prop", due="2026-11-20", who="Dylan", status="active",
         t="Send Pierfrancesco the outline, the two-arm numbers and the questions (spokesperson, GLIMOS, author list)"),
    dict(id="P2", ws="prop", due="2026-11-20", who="Pierfrancesco", status="todo",
         t="Informal contact with Anna Selva / the Accelerator Division: AN2000 vs CN, 0.441 + 1.10 MeV at 1 µA, line and floor space, H2 2027"),
    dict(id="P3", ws="prop", due="2026-11-23", who="Dylan", status="todo",
         t="Get the INFN-AAI account + 'Risorse IT' (needed to submit on Indico)"),
    dict(id="P3b", ws="prop", due="2026-11-18", who="Dylan", status="done",
         t="Download the LNL LaTeX template from Indico; move the draft into it; upload to Overleaf"),
    dict(id="P4", ws="prop", due="2026-11-24", who="Dylan", status="todo",
         t="Ask the co-proponents (Massimi, Mengoni, Gervino, Gustavino, Cosentino) to join; collect names + affiliations"),
    dict(id="P5", ws="prop", due="2026-11-27", who="Dylan", status="todo", dep=["R1"],
         t="Draft v1 in Overleaf: abstract page + body of at most 4 pages (LNL template, 12 pt, figures and references included)"),
    dict(id="P6", ws="prop", due="2026-11-30", who="Dylan", status="todo", dep=["P5"],
         t="Draft to Pierfrancesco; agree the beam-day table and the machine"),
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
    dict(id="R2", ws="sim", due="2026-11-27", who="Dylan", status="todo",
         t="Proposal figures: two-arm acceptance vs θ, expected spectra (441 keV and 1.10 MeV), rates table"),
    dict(id="R3", ws="sim", due="2027-04-30", who="Dylan", status="todo",
         t="Geant4: two-arm geometry with the real target holder and stand (MX17_Full_Geant branch from lnl_target)"),
    dict(id="R4", ws="sim", due="2027-06-30", who="Dylan", status="todo",
         t="Timing on cosmics with the LNL readout (V1742/CFD): n_TOF beam-off muons give σ_t 0.52–0.64 ns per arm (walls), 0.95 (plastics) with the n_TOF readout (nTof_x17 ac_tof_beamoff, 19 Nov); decides the TOF cut"),
    dict(id="R5", ws="sim", due="2026-11-27", who="Dylan", status="todo", dep=["R1"],
         t="Proposal text from sim2arm: the 441 keV rate (~600 pairs/day above 90°, not 6–12k), the reach rows, the vertical-cosmics test"),
    dict(id="R6", ws="sim", due="2027-03-31", who="Dylan", status="todo",
         t="More as-built MC for the Cu hemisphere (EPC and IPC rest on a few hundred events per pair) before the PAC talk"),
    # --- MM
    dict(id="M1", ws="mm", due="2027-01-15", who="Dylan", status="todo",
         t="Ask Stephan / CEA: repair B's drift window (needed); new aluminised-mylar windows for A and B (low-budget upgrade); dates"),
    dict(id="M2", ws="mm", due="2027-01-15", who="Dylan", status="todo",
         t="Ask CEA for the DREAM loan for H2 2027: 4 FEUs + TCM + 32 cables + LV; solder the TCM busy LEMO"),
    dict(id="M3", ws="mm", due="2027-04-30", who="Dylan", status="todo",
         t="Optional (high-budget upgrade): 4 CERN-design M1 cards for B. Slot 1 runs B with its existing Italian M1s"),
    dict(id="M4", ws="mm", due="2027-06-15", who="Dylan", status="todo",
         t="Cosmic bench, 2 MM + DREAM: efficiency, segment angle (μ ≲ 3°), noise with B's existing M1s"),
    # --- scint / trigger
    dict(id="S1", ws="scint", due="2027-01-31", who="Pierfrancesco", status="todo",
         t="Find PMTs for the 4 small plastics (+2 for liquid cells if taken)"),
    dict(id="S2", ws="scint", due="2027-01-31", who="Pierfrancesco", status="todo",
         t="Digitizers: ~24 channels (16 wall + 4–6 PMT + trigger word) from LNL pool; else ask CAEN for a test loan"),
    dict(id="S3", ws="scint", due="2027-02-28", who="Dylan", status="todo",
         t="Trigger logic: 2–3 N1081B, a dual timer, FIFOs/splitters, NIM bin — borrow list"),
    dict(id="S4", ws="scint", due="2027-05-31", who="Dylan", status="todo",
         t="Bench tests T1, T2, T4 (prescaler, busy lock 1:1, trigger word)"),
    dict(id="S5", ws="scint", due="2027-02-28", who="Dylan", status="todo",
         t="Decide: bring 2 liquid cells? Without them the days to 3σ go up ×2–4 (sim2arm); even as at n_TOF they beat none"),
    # --- target
    dict(id="T1", ws="target", due="2026-12-01", who="Pierfrancesco", status="todo",
         t="Target for the proposal: pressed Li on Cu (CN group), 10–12 µm; holder: the Cu hemisphere (already built, most likely; the 'Cu ogive' of the simulation); flat Al end cap at 45° only if it pays"),
    dict(id="T2", ws="target", due="2027-06-30", who="Pierfrancesco", status="todo",
         t="Build the holder; make films; a week of LiOH-conversion test on the line"),
    # --- site
    dict(id="L1", ws="site", due="2027-03-31", who="Dylan", status="todo",
         t="LNL access: registration ≥ 15 d ahead, RP training certificate, dosimeters, responsibility declaration"),
    dict(id="L2", ws="site", due="2027-05-31", who="Pierfrancesco", status="todo",
         t="Safety file: Ar/iC₄H₁₀ 95/5 bottles in the hall, gas panel and exhaust (flammable)"),
    dict(id="L3", ws="site", due="2027-03-31", who="Pierfrancesco", status="todo",
         t="Floor plan of the line: ~1.5 × 1.5 m around the target, beam height, cable path to the control room, network"),
    # --- run
    dict(id="I1", ws="run", due="2027-07-31", who="Dylan", status="todo",
         t="Full chain on cosmics: 2 arms, DREAM + digitizers on one event list, run control, slow control Tier 1"),
    dict(id="I2", ws="run", due="2027-09-17", who="all", status="todo",
         t="Ship, install, commission on cosmics at LNL: ≥ 3 nights with the arms VERTICAL (σ_t, μ segment angle, MIP gains, each cosmic veto), then roll to horizontal"),
    dict(id="I3", ws="run", due="2027-10-01", who="all", status="todo",
         t="8 beam days + beam-off cosmic nights; shift list sent to RP ≥ 3 days ahead"),
    # --- funding
    dict(id="F1", ws="fund", due="2026-12-15", who="Pierfrancesco", status="todo",
         t="Which commission and when are the requests due? (Pierfrancesco wrote 'commission II'; INFN preventivi are usually prepared in summer: ask)"),
    dict(id="F2", ws="fund", due="2027-11-30", who="Dylan", status="todo",
         t="Full-experiment proposal (4 arms, big plastics) to the next LNL PAC, with the feasibility results"),
]

# ----------------------------------------------------------------------------------------------
# Hardware for slot 1 (two arms): everything the run needs, owned, borrowed, bought or made (Hardware tab).
#   status  what we must do: ready (in hand) | fix | borrow | find | buy | make | decide
#   org     lender or source, for grouping: MX17 collaboration | CEA Saclay | INFN / LNL | purchase | our own work
#   src     where it comes from, in words; who = our contact for it
#   state   progress: in hand | agreed | to ask | asked | to find | to order | to make | to decide
#   need    date it must be in hand (the cosmic bench starts May 2027, installation Aug 2027)
#   b       the BUDGET line that prices it (cash, tier and the cost if a loan falls through come from there)
#   place   where it sits on the Hardware tab's diagram (keys of PLACES in site/template.html)
#   inv     ids in the central inventory (x17_facility_search/inventory/inventory.py): owner, location, condition
#   tasks   task ids; ids mmA, mmB, mmCD, walls, plast, ls are also the layers of the Set-up view.
HARDWARE = [
    # --- Micromegas & DREAM
    dict(id="mmA", part="Micromegas A (det3)", qty="1", grp="Micromegas & DREAM", status="ready", org="MX17 collaboration", src="MX17 collaboration",
         who="Dylan", state="in hand", need="2027-05-01", inv=["mmA"], place=["mmA"], tasks=["M4"],
         note="Best chamber: 92.9 % within 5 mm on the bench. Runs as is; a new aluminised-mylar window is a low-budget upgrade. Clean CERN M1 cards.",
         detail="40 × 36 cm active, 30 mm drift, Ar/iC₄H₁₀ 95/5, bulked at CEA in June 2026. Ran at n_TOF in 2026."),
    dict(id="mmB", part="Micromegas B (det2)", qty="1", grp="Micromegas & DREAM", status="fix", org="CEA Saclay", src="CEA Saclay",
         who="Stephan (CEA)", state="to ask", need="2027-04-30", b="Repair B's drift window", inv=["mmB"], place=["mmB"], tasks=["M1", "M4"],
         note="91.3 % on the bench; drift window needs a repair (likely just an electrical connection; needed for the test); a new window is a low-budget upgrade. Its M1 cards were the noisy Italian ones.",
         detail="Amplification is good. The repair is critical for the test; the risk that it is not done in time is low."),
    dict(id="win", part="New aluminised-mylar drift windows", qty="2 (A, B)", grp="Micromegas & DREAM", status="buy", org="CEA Saclay", src="CEA Saclay",
         who="Stephan (CEA)", state="to ask", need="2027-04-30", b="New aluminised-mylar drift windows, A and B", inv=["mmA", "mmB"], place=["mmA", "mmB"], tasks=["M1"],
         note="Low-budget upgrade: aluminised mylar only (the aluminium is the cathode), dropping the 9 µm Cu that triples the material per crossing.",
         detail="x17_facility_search budget item 'windows': ~€2.5k for four (frames, glue, labour), so ~€1.25k for two. Not needed for the test."),
    dict(id="mmCD", part="Micromegas C, D (spares)", qty="2", grp="Micromegas & DREAM", status="decide", org="CEA Saclay", src="CEA Saclay",
         who="CEA", state="to decide", need="", inv=["mmC", "mmD"], place=[], tasks=[],
         note="Spark-limited (57.8 %, 43.1 %); re-bulk needed. Not required for slot 1. C re-bulked would be the spare.",
         detail="Needed for slot 2 (four arms)."),
    dict(id="m1", part="M1 multiplex cards", qty="8 (4 per chamber)", grp="Micromegas & DREAM", status="ready", org="MX17 collaboration", src="MX17 collaboration (CERN + Italian cards)",
         who="Dylan", state="in hand", need="2027-05-01", inv=["m1cern", "m1ital"], place=["m1"], tasks=["M4"],
         note="Clean CERN cards on A; B keeps its noisier Italian cards for slot 1.",
         detail="The noise on B's cards was seen at n_TOF; the cosmic bench (M4) measures it with the LNL set-up."),
    dict(id="m1new", part="CERN-design M1 cards for B", qty="4", grp="Micromegas & DREAM", status="buy", org="purchase", src="CERN design, produced to order",
         who="Dylan", state="to decide", need="2027-04-30", b="4 CERN M1 cards for B (B runs its Italian M1s for the test)", inv=["m1ital"], place=["m1"], tasks=["M3"],
         note="High-budget upgrade toward slot 2 (~€2k each). Slot 1 runs B with its existing Italian cards.",
         detail="x17_facility_search budget item 'm1': 12 cards €24k."),
    dict(id="dream", part="DREAM: FEUs + TCM + cables", qty="4 FEUs, 1 TCM, 32 cables", grp="Micromegas & DREAM", status="borrow", org="CEA Saclay", src="CEA Saclay",
         who="Stephan (CEA)", state="to ask", need="2027-05-01", inv=["dream", "dreamcab"], place=["feu", "tcm"], tasks=["M2"],
         note="Half the n_TOF system. Solder a LEMO on the TCM busy output before the run (daq_trigger/PLAN.md §4.2).",
         detail="A loan with a liability (the full 8-FEU system was valued at €72k in the budget). At LNL rates DREAM is > 95 % live."),
    dict(id="busy", part="LEMO on the TCM busy output", qty="1", grp="Micromegas & DREAM", status="make", org="our own work", src="our own work",
         who="Dylan", state="to make", need="2027-05-31", inv=["dream"], place=["tcm"], tasks=["M2", "S4"],
         note="The TCM has a busy output but its LEMO is not fitted. It vetoes the trigger so both systems keep one event list.",
         detail="Check level, polarity and assertion delay on the bench (test T2, daq_trigger/PLAN.md §4.2)."),
    # --- Scintillators
    dict(id="walls", part="SiPM walls + summing boards", qty="2", grp="Scintillators", status="ready", org="INFN / LNL", src="INFN (n_TOF set-up)",
         who="Pierfrancesco", state="agreed", need="2027-05-01", inv=["walls"], place=["walls"], tasks=["R4"],
         note="16 of 20 bars read, ganged as at n_TOF on the summing boards: 8 channels per wall. Bias ~54 V, ~0.2 mA per wall.",
         detail="EJ-212 bars, 3 × 26 × 500 mm. Pierfrancesco confirmed they can be used (18 Nov 2026)."),
    dict(id="plast", part="Small plastic scintillators 20 × 30 × 2 cm", qty="4 (2 per arm)", grp="Scintillators", status="ready", org="INFN / LNL", src="INFN",
         who="Pierfrancesco", state="agreed", need="2027-05-01", inv=["plast_small"], place=["plast"], tasks=["S1"],
         note="The scintillators are available; their PMTs went back to the lender (next line).",
         detail="Behind the SiPM wall; trigger and energy."),
    dict(id="pmt", part="PMTs + bases for the plastics", qty="4 (+2 for liquid cells)", grp="Scintillators", status="find", org="INFN / LNL", src="lender to find (INFN / LNL pool)",
         who="Pierfrancesco", state="to find", need="2027-05-01", b="If the PMTs must be bought: 4–6 fast 2″ PMTs + bases", inv=["pmt_small"], place=["plast"], tasks=["S1"],
         note="The n_TOF PMTs went back to their lender. Borrow again or find others that fit; buying is the expensive fallback.",
         detail="Fast 2″ tubes. Ask whether the original lender can lend them again (question for Pierfrancesco)."),
    dict(id="ls", part="Liquid cells 45 × 45 cm (optional)", qty="2", grp="Scintillators", status="decide", org="MX17 collaboration", src="MX17 collaboration (n_TOF set-up)",
         who="Dylan / Pierfrancesco", state="to decide", need="2027-05-01", inv=["ls"], place=["ls"], tasks=["S5"],
         note="67–76 % pile-up at n_TOF (γ-flash), so left out of the budget. LNL rates are far lower. With them the reach is ×3.6 better.",
         detail="Need 2 more PMTs and 2 digitizer channels if taken."),
    # --- Trigger & DAQ
    dict(id="dig", part="Digitizers, ~24 channels", qty="1 V1742 or 2 × V1730", grp="Trigger & DAQ", status="find", org="INFN / LNL", src="LNL pool, else a CAEN loan",
         who="Pierfrancesco / CAEN", state="to find", need="2027-05-01", b="If no digitizer loan: V1742 (32 ch)", place=["vme"], tasks=["S2"],
         note="16 wall + 4 plastic PMTs (+2 LS) + 2–3 trigger-word + spares. A V1742 (32 ch) covers it. '10–20 channels we could find' (Pierfrancesco).",
         detail="Price if bought: CAEN offer 26OFC.01101."),
    dict(id="vme", part="VME crate + optical bridge", qty="VME8004B + A4818", grp="Trigger & DAQ", status="borrow", org="INFN / LNL", src="LNL pool",
         who="Pierfrancesco", state="to ask", need="2027-05-01", b="If no VME crate: VME8004B + A4818", place=["vme"], tasks=["S2"],
         note="Holds the digitizers; the A4818 links them to the DAQ PC over optical fibre.", detail="Price if bought: CAEN offer."),
    dict(id="n1081", part="N1081B programmable logic units", qty="2", grp="Trigger & DAQ", status="borrow", org="INFN / LNL", src="LNL pool, else a CAEN loan",
         who="Pierfrancesco / CAEN", state="to ask", need="2027-05-01", b="If no N1081B loan: 2 × N1081B", inv=["n1081b_cern"], place=["nim"], tasks=["S3", "S4"],
         note="The n_TOF trigger for two arms: legs per arm in 20 ns coincidence, PAIR never prescaled, SINGLE ÷P, 1 Hz clock, trigger word, scalers.",
         detail="Pierfrancesco suggested a CAEN test loan. Our n_TOF tooling (trigger_mode.py, poll_modules) runs on N1081Bs, the reason to stay with them."),
    dict(id="timer", part="Dual timer", qty="1 (N93B)", grp="Trigger & DAQ", status="borrow", org="INFN / LNL", src="LNL pool",
         who="Pierfrancesco", state="to ask", need="2027-05-01", b="If no dual timer: N93B", inv=["n93b_cern"], place=["nim"], tasks=["S3"],
         note="Hold gate after each trigger, ORed with DREAM's busy.", detail="Price if bought: CAEN offer."),
    dict(id="nimbin", part="NIM bin", qty="1–2", grp="Trigger & DAQ", status="borrow", org="INFN / LNL", src="LNL pool",
         who="Pierfrancesco", state="to ask", need="2027-05-01", place=["nim"], tasks=["S3"],
         note="For the N1081Bs, the timer and the linear FIFOs.", detail="Standard pool item (ask)."),
    dict(id="split", part="Active splitters, LEMO cables, adapters", qty="for 2 arms", grp="Trigger & DAQ", status="buy", org="purchase", src="to order",
         who="Dylan", state="to order", need="2027-05-01", b="Splitters, LEMO cables, adapters (2 arms)", place=["cables"], tasks=["S3"],
         note="Every scintillator signal is split actively: one copy to the digitizer, one to the trigger. A passive split halved the plastic amplitude at n_TOF.",
         detail="x17_facility_search budget item 'splitters' (€7.6k for 4 arms), halved."),
    dict(id="pc", part="DAQ PC (DREAM + run control)", qty="1", grp="Trigger & DAQ", status="borrow", org="CEA Saclay", src="CEA Saclay",
         who="Stephan (CEA)", state="to ask", need="2027-05-01", inv=["daqpc"], place=["pc"], tasks=["M2", "I1"],
         note="Not Dylan's: borrow it from CEA with the DREAM loan (Dylan, 19 Nov 2026). Run control from n_TOF: DREAM + digitizers on one event list.",
         detail="Network at LNL: ask (task L3)."),
    dict(id="switch", part="Network switch", qty="1", grp="Trigger & DAQ", status="ready", org="MX17 collaboration", src="Dylan's own",
         who="Dylan", state="in hand", need="2027-05-01", inv=["switch"], place=["pc"], tasks=[],
         note="Dylan's (19 Nov 2026).", detail=""),
    dict(id="pdu", part="Switched PDU (remote power cycles)", qty="1", grp="Trigger & DAQ", status="buy", org="purchase", src="to order",
         who="Dylan", state="to order", need="2027-05-31", b="Switched PDU (remote power switch)", place=["pdu"], tasks=[],
         note="Low-budget upgrade. N1081B daemons wedge after dirty disconnects; at n_TOF there was no remote reboot.",
         detail="NETIO PowerPDU class (daq_trigger/PLAN.md §7)."),
    # --- Power
    dict(id="lv", part="LV supply 5 V / ~25 A", qty="1", grp="Power", status="borrow", org="INFN / LNL", src="LNL / CERN pool",
         who="Pierfrancesco", state="to ask", need="2027-05-01", place=["lv"], tasks=["M2"],
         note="4 FEUs at ~5 A + TCM ~5 A.", detail="Ask CEA whether the LV comes with the DREAM loan."),
    dict(id="hv", part="HV: Micromegas drift + mesh, PMTs", qty="1 CAEN unit", grp="Power", status="borrow", org="INFN / LNL", src="LNL pool",
         who="Pierfrancesco", state="to ask", need="2027-05-01", place=["hv"], tasks=[],
         note="Micromegas ≤ 600 V; PMTs negative. Driven by caen_hv_py.", detail="SiPM bias from the walls' own supplies."),
    # --- Gas & slow control
    dict(id="gas", part="Gas: Ar/iC₄H₁₀ 95/5 premix bottles, regulators, panel", qty="1 panel", grp="Gas & slow control", status="buy", org="purchase", src="to order (via LNL)",
         who="Dylan / LNL", state="to order", need="2027-05-01", b="Gas: premix bottles, regulators, panel", place=["gas"], tasks=["L2"],
         note="No mixer comes from n_TOF. Flammable-gas rules at LNL: ask.", detail="~1 L/h with exhaust. Bottles in the hall need the safety file (L2)."),
    dict(id="gaslines", part="Low-permeation gas lines", qty="2 arms", grp="Gas & slow control", status="buy", org="purchase", src="to order",
         who="Dylan", state="to order", need="2027-05-01", b="Low-permeation gas lines", place=["gaslines"], tasks=[],
         note="Low-budget upgrade (Synflex type); slot 1 can run on standard lines.", detail=""),
    dict(id="slow", part="Gas and environment sensors (slow control Tier 1)", qty="1 set", grp="Gas & slow control", status="buy", org="purchase", src="to order",
         who="Dylan", state="to decide", need="2027-05-31", b="Gas and environment sensors (slow control Tier 1)", place=["sensors"], tasks=["I1"],
         note="Low-budget upgrade: T/p/RH, SHT85 cells on the gas line, logger.", detail="x17_facility_search slow_control/SENSOR_OPTIONS.md §6."),
    # --- Target & beam line
    dict(id="tgt", part="Li target films (pressed on Cu)", qty="several", grp="Target & beam line", status="make", org="INFN / LNL", src="LNL CN target laboratory",
         who="Pierfrancesco", state="to make", need="2027-08-31", place=["target"], tasks=["T1", "T2"],
         note="LNL rolls Li to 10–20 µm in an Ar glovebox and presses it onto Cu. 10–12 µm recommended (LiOH). Boron-free.",
         detail="A week of LiOH-conversion test on the line before the run (T2)."),
    dict(id="holder", part="Cu hemisphere target holder", qty="1", grp="Target & beam line", status="ready", org="INFN / LNL", src="LNL (already built)",
         who="Pierfrancesco", state="in hand", need="2027-08-31", inv=["cu_hemi"], place=["target"], tasks=["T1"],
         note="Already built, so the baseline (Dylan, 19 Nov). The 'Cu ogive' of the simulation. A flat Al end cap at 45° would be lighter (~30 % less beam time).",
         detail="Confirm it fits the AN2000 line end (question for Pierfrancesco)."),
    dict(id="line", part="AN2000 beam line end + floor space", qty="~1.5 × 1.5 m", grp="Target & beam line", status="borrow", org="INFN / LNL", src="LNL Accelerator Division",
         who="Pierfrancesco", state="to ask", need="2027-09-01", place=["beamline"], tasks=["P2", "L3"],
         note="A line ending in ~1.5 × 1.5 m of open floor, beam height, cable path to the control room.", detail="AN2000 is self-service; one energy change per day."),
    dict(id="stand", part="Two-arm stand", qty="1", grp="Target & beam line", status="decide", org="INFN / LNL", src="LNL mechanics (ask)",
         who="Pierfrancesco", state="to decide", need="2027-08-01", place=["stand"], tasks=["L3", "R3"],
         note="Two opposite arms, faces at ±204 mm from the beam axis. It should roll 90° about the beam: vertical for the cosmic nights, horizontal for the beam days (sim2arm, 19 Nov).",
         detail="Opposite arms are best (turning them toward 140° costs ×1.1–2.5 in days, run L16). Its material goes into the Geant4 geometry (R3)."),
    dict(id="gmon", part="γ-yield monitor (LaBr₃ or NaI)", qty="1", grp="Target & beam line", status="borrow", org="INFN / LNL", src="LNL detector pool (ask)",
         who="Pierfrancesco", state="to ask", need="2027-08-01", place=["target"], tasks=["I3"],
         note="The target's daily health (LiOH conversion) and a γ₀ cross-check, independent of the arms. Not in the set-up so far (sim2arm §7.5).",
         detail="One spare digitizer channel."),
    # --- Logistics
    dict(id="ship", part="Shipping CEA / CERN → LNL and back", qty="", grp="Logistics", status="buy", org="purchase", src="to order",
         who="Dylan", state="to order", need="2027-08-15", b="Shipping CEA/CERN → LNL and back", place=[], tasks=["I2"],
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
    dict(item="Splitters, LEMO cables, adapters (2 arms)", c=3800, lo=2500, hi=5000, basis="items.py splitters €7.6k for 4 arms, halved", tier="need"),
    dict(item="Shipping CEA/CERN → LNL and back", c=2000, lo=1000, hi=4000, basis="guess", tier="need"),
    dict(item="New aluminised-mylar drift windows, A and B", c=1250, lo=500, hi=2500, basis="items.py windows €2.5k for 4, × 2/4", tier="low"),
    dict(item="Low-permeation gas lines", c=400, lo=250, hi=700, basis="items.py gaslines", tier="low"),
    dict(item="Gas and environment sensors (slow control Tier 1)", c=2500, lo=2000, hi=3200, basis="items.py slowctl", tier="low"),
    dict(item="Switched PDU (remote power switch)", c=290, lo=290, hi=400, basis="items.py pdu", tier="low"),
    dict(item="4 CERN M1 cards for B (B runs its Italian M1s for the test)", c=8000, lo=6000, hi=10000, basis="items.py m1: 12 cards €24k → €2k/card", tier="high"),
    dict(item="If no digitizer loan: V1742 (32 ch)", c=9500, lo=9500, hi=9500, basis="CAEN offer 26OFC.01101", tier="loan"),
    dict(item="If no N1081B loan: 2 × N1081B", c=13960, lo=13960, hi=13960, basis="CAEN offer, €6,980 each", tier="loan"),
    dict(item="If no VME crate: VME8004B + A4818", c=4760, lo=4760, hi=4760, basis="CAEN offer", tier="loan"),
    dict(item="If no dual timer: N93B", c=2720, lo=2720, hi=2720, basis="CAEN offer", tier="loan"),
    dict(item="If the PMTs must be bought: 4–6 fast 2″ PMTs + bases", c=12000, lo=6000, hi=24000, basis="guess; Hamamatsu Italia scale", tier="loan"),
]

# ----------------------------------------------------------------------------------------------
# Open questions, by who answers.
QUESTIONS = [
    dict(who="Pierfrancesco", q="Spokesperson(s) and GLIMOS for the abstract page? (GLIMOS is normally local.)"),
    dict(who="Pierfrancesco", q="AN2000 or CN? The CN starts at 0.8 MV, so no 441 keV calibration there; AN2000 runs 0.2–2.0 MV self-service."),
    dict(who="Pierfrancesco", q="Target for the proposal: pressed Li on Cu in the existing Cu hemisphere: confirm it fits the AN2000 line end?"),
    dict(who="Pierfrancesco", q="Can the stand roll 90° about the beam? Plan (sim2arm): vertical pair for the cosmic nights before the beam, horizontal for the beam days."),
    dict(who="Pierfrancesco", q="A γ-yield monitor (LaBr₃ or NaI) from the LNL pool for the target's daily check?"),
    dict(who="Pierfrancesco", q="'Commission II': which INFN commission, and when must the request be in? Results before that date?"),
    dict(who="Pierfrancesco", q="Is the H2-2027 window flexible to June–July, so that results exist before the funding requests?"),
    dict(who="Pierfrancesco", q="Author list: affiliations for Massimi, Mengoni, Gervino, Gustavino, Cosentino; anyone else (n_TOF, CEA, Torino)?"),
    dict(who="LNL Accelerator Division", q="A line on AN2000 (or CN) ending in ~1.5 × 1.5 m of free floor; beam height; 1 µA at 0.441 and 1.10 MeV on that line?"),
    dict(who="LNL Accelerator Division", q="Is a PAC 'day' 24 h? Night and weekend running with self-service AN2000?"),
    dict(who="LNL Accelerator Division", q="Flammable premix (Ar/iC₄H₁₀ 95/5) in the hall: rules, storage, exhaust."),
    dict(who="CEA (Stephan, DREAM)", q="Repair B's drift window by April 2027 (and 2 new windows, if cheap)? Lend 4 FEUs + TCM for Jun–Oct 2027?"),
    dict(who="CAEN", q="A test loan of a V1742 or 2 × V1730 + 2 N1081B for the run (Pierfrancesco's suggestion)?"),
    dict(who="LNL ⁸Be group (Marchi)", q="Status of their 2023–24 AN2000 data; is a joint or complementary run welcome; is the AN2000 room free?"),
    dict(who="Plastics lender", q="Can we borrow the 4 small plastics' PMTs again (or which PMTs fit them)?"),
]

RISKS = [
    dict(r="Micromegas B not repaired in time", l="low", i="high",
         m="Likely just an electrical connection on the drift (Dylan, 19 Nov). A is ready now; C re-bulk as the spare; one-arm-plus-scintillator fallback still gives the 441 keV and background programme."),
    dict(r="DREAM not available in H2 2027 (CEA's own use)", l="med", i="high",
         m="Ask now (M2); 4 FEUs is half the system; fix dates with CEA before the PAC talk."),
    dict(r="Too few digitizer channels", l="low", i="med",
         m="Two arms need ~24, PM can find 10–20; CAEN loan; ganged walls keep it at 8 per wall."),
    dict(r="AN2000 room occupied (LNL ⁸Be spectrometer) or no free line", l="med", i="high",
         m="Talk to the Marchi group first; CN fallback (no 441 keV; 1.03–1.10 only)."),
    dict(r="Reach in 8 days oversold", l="low", i="high",
         m="Simulated (sim2arm): an ATOMKI-size signal shows at 1–2σ in 5 days, not 3σ. Quote the expected limit (0.8–1.1 × R(ATOMKI) with liquid cells); the feasibility results come first."),
    dict(r="Cosmic veto weaker than simulated (σ_t > 0.4 ns, segments worse than 3°)", l="med", i="med",
         m="n_TOF beam-off muons: σ_t 0.52–0.64 ns per arm (19 Nov). Horizontal pair for the beam days: its days barely depend on σ_t (17.4 d with no TOF, 17.7 at any σ_t; sim2arm tof_scan); the vertical pair goes 17.1 → 18.7 d from 0.3 to 0.7 ns. R4 with the LNL readout."),
    dict(r="Li film degrades (LiOH) under beam", l="med", i="med",
         m="10–12 µm films; γ-yield monitor each day; a spare film; a week's conversion test before the run."),
    dict(r="Machine-future decision (one machine to replace AN2000 + CN)", l="low", i="high",
         m="Run in 2027 is unaffected; follow the decision (x17_facility_search/lnl/NOTE_CN_AN2000_REPLACEMENT.md)."),
    dict(r="Proposal deadline missed (next call ~a year later)", l="low", i="high",
         m="Draft by 27 Nov; submit 9 Dec; get the INFN-AAI account this week."),
]

# The proposal itself: structure, from https://www.lnl.infn.it/en/details-for-submissions/ (read 2026-11-18).
PROPOSAL = dict(
    rules=[
        "Use the LNL templates (abstract + body, LaTeX or Word); submit PDF only. Abstract: one page (not counted in the body)",
        "Abstract fields: title, accelerator, set-up, spokesperson(s), GLIMOS, all authors + affiliations, short summary",
        "Body: max 4 pages per the official template (the LNL web page says 5), 12 pt, tables + figures + references included",
        "Body must contain: scientific motivation; technical details (instrumentation, quantities measured, precision); beam days from count-rate estimates",
        "Online: Beam Time Request, then the Targets Request Form; keep the confirmation e-mail (password)",
        "Needs an active INFN-AAI account with 'Risorse IT'",
        "Internal LNL technical review before the PAC (beam, target, set-up readiness, radioprotection, safety); issues sent ~7 days before",
        "Possible oral presentation: 12 min + 8 min discussion, hybrid",
    ],
    sections=[
        dict(id="abs", name="Abstract page", status="draft", pages=1, owner="Dylan"),
        dict(id="mot", name="1. Scientific motivation", status="draft", pages=0.9, owner="Dylan"),
        dict(id="app", name="2. MX17 and the two-arm set-up", status="draft", pages=0.9, owner="Dylan"),
        dict(id="meas", name="3. Measurements and precision", status="draft", pages=0.9, owner="Dylan"),
        dict(id="beam", name="4. Beam request and count rates", status="draft", pages=0.6, owner="Dylan"),
        dict(id="next", name="5. From feasibility to the full experiment", status="draft", pages=0.4, owner="Dylan"),
        dict(id="ref", name="References", status="draft", pages=0.3, owner="Dylan"),
    ],
)

SLOT2 = dict(
    name="Slot 2: the ⁸Be X17 measurement",
    when="2028 (next PAC call, est. late 2027)",
    setup=[
        "Four arms: A, B + re-bulked C and D, new windows on all",
        "Big plastics (4 × ~78 × 80 × 5 cm in-house plates) behind the SiPM walls: ×13–15 in running time",
        "SiPM walls per bar end (FERS, 160 ch) in the Upgrade preset; ganged in Self",
        "Own trigger/DAQ (architecture B or D), DREAM still from CEA",
        "Target from the slot-1 experience (flat Al end cap / Cu ogive, 10–12 µm Li)",
    ],
    programme=[
        "441 keV calibration (17.64 MeV, no anomaly expected)",
        "3σ at R(ATOMKI) at 1.10 MeV, then 0.80 and 1.225 MeV off-resonance (clean points need 5–10 µm films)",
        "Big plastics: 4.4 d (Al + Cu liner) to 12 d (Cu ogive) for the programme; as built 23–80 d",
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
            r["fallback" if bl["tier"] == "loan" else "cash"] = bl["c"]
        rows.append(r)
    return rows


def main() -> None:
    import two_arm_estimates as E  # noqa: E402  (same directory)
    E.main()
    data = dict(
        updated=UPDATED, deadline=DEADLINE, pac=PAC, links=LINKS, tiers=TIERS, workstreams=WORKSTREAMS, phases=PHASES,
        milestones=MILESTONES, tasks=TASKS, hardware=hardware_rows(), budget=BUDGET, questions=QUESTIONS,
        risks=RISKS, proposal=PROPOSAL, slot2=SLOT2, reach=reach_rows(), beam=beam_rows(),
        reach_model=dict(r_atomki=E.R_ATOMKI, r_megii=E.R_MEG2_90, days_on_res=E.DAYS_ON_RES,
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
