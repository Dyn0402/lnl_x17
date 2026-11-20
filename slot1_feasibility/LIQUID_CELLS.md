# Liquid scintillator cells: baseline for slot 1, and wider or thicker ones

Written 2026-11-20 after Pierfrancesco's e-mail (`../correspondence/2026-11-20_mastinu_target_liquid.md`): the liquid is
there, the cans must be remade, and the PMTs are short. Everything below except §1 is a **scaling estimate** until a
Geant4 run replaces it (task S7).

## 1. Baseline for the proposal

- **Two cells, one per arm, 45 × 45 × 2 cm, in new cans**, behind the two small plastics, as the n_TOF cells
  (MX17_Full_Geant `include/SimConfig.hh`: slab 45.1 × 45.1 × 2.12 cm outer, 2.6 mm CFRP wall, funnel + neck to one
  PMT, 6.5 L each with the faces bulged; front 12.3–12.7 cm behind the SiPM-wall container, ≈ 47 cm from the beam).
- This is the simulated **"liquid working"** case of `../sim2arm/TWO_ARM_STUDY.md` §0 (response a = 0.5 √MeV, c = 15 %,
  "LNL calibrated"): **2.35 × R(ATOMKI) in 5 days** with the built Cu hemisphere (151 d to 3σ). As at n_TOF: 3.10 ×;
  without the liquid: 4.32 × (×3.4 in days).
- Needs: 2 new cans, 2 PMTs + bases (S1), 2 digitizer channels (already in the ~24), ~13 L of liquid.

## 2. Pierfrancesco's option: 4 cm in parallel or 2 cm in series

His words: "two detectors 4 cm thick in parallel, or two detectors 2 cm thick in series" (to clarify: per arm or in
total; question in `planning/plan.py`).

- Why thickness matters: 2 cm of scintillator stops neither lepton of an 18 MeV pair (the soft one carries 3–8 MeV and
  needs ~2–4 cm, the hard one more). The four-arm study found that **5 cm is a calorimeter and 2 cm is not**: E_sum
  separates γ₀ from γ₁ pairs at 1.2σ with 5 cm plates and 0.6σ as built (x17_facility_search `lnl/FEASIBILITY_SIM.md`
  §9 and the response table before it).
- Two 2 cm cells in series give the same 4 cm of liquid with a depth split (two PMTs per arm), which also tells a
  stopping soft lepton from a crossing one; one 4 cm cell needs one PMT.
- Not known without Geant4: how much of the 4.3 → 2.35 × gain comes from E_sum, and how much more 4 cm adds.

## 3. Wider cells instead of the big plastics

The full experiment was planned with four big plastics (4 × ~78 × 80 × 5 cm, worth ×13–15 in running time,
`FEASIBILITY_SIM.md` §9: mostly acceptance, a leg in both arms ×7, and calorimetry ×1.5). Since the cans are remade
anyway, they could be made wide enough to play that role, within the liquid we have (**~60 L, to confirm**).

**Acceptance saturates** (the §9 geometric toy, 5 cm plates, relative days; it is an estimate calibrated on Geant4):

| square side | 45 | 50 | 55 | 60 | 65 | 70 | 75 cm |
|---|---|---|---|---|---|---|---|
| days, plates at R = 41 cm (where the small plastics are) | 3.4 | 2.3 | 1.7 | 1.4 | 1.26 | 1.22 | 1.20 |
| days, plates at R = 35 cm (right behind the SiPM wall) | 1.95 | 1.42 | 1.22 | 1.19 | 1.19 | 1.19 | 1.19 |

The Micromegas (40 × 36 cm) set the cone, so past ~60 cm (at 35 cm) or ~70 cm (at 41 cm) nothing is gained. At the
present cell position (47 cm) the same cone needs ~80 cm.

**Liquid needed** (slab + ~2.5 L of funnel and neck per cell, as the n_TOF cans: 6.5 L for 45 × 45 × 2 cm):

| side × thickness | per cell | 2 arms | 4 arms |
|---|---|---|---|
| 45 × 45 × 2 (baseline) | 6.5 L | 13 L | 26 L |
| 60 × 60 × 2 | 9.7 L | 19 L | 39 L |
| 60 × 60 × 3 | 13.3 L | 27 L | **53 L** |
| 60 × 60 × 4 | 16.9 L | 34 L | 68 L |
| 70 × 70 × 4 | 22.1 L | 44 L | 88 L |
| 70 × 70 × 5 | 27.0 L | **54 L** | 108 L |
| 80 × 80 × 4 | 28.1 L | **56 L** | 112 L |

So with ~60 L:
- **Two arms (slot 1)**: a big-plastic-class leg is within reach, e.g. 70 × 70 × 5 cm or 80 × 80 × 4 cm per arm.
- **Four arms (slot 2)**: about 60 × 60 × 3 cm per arm, placed where the small plastics are now (35–41 cm). That keeps the
  acceptance (1.2–1.4 d vs 1.2 d for 75 cm in the toy) but gives 3 cm instead of 5 cm of calorimeter. More liquid, or
  plastic for two of the arms, would close the gap.

Open points before this can replace the big plastics:
1. The trigger leg is now SiPM bar × plastic. A wide cell behind (or instead of) the small plastics would have to form the
   leg itself: timing (the liquid is fast, but one PMT on a 70 cm cell has a position-dependent delay), threshold, rates.
2. Light collection on a 70–80 cm cell with one PMT: the n_TOF cells were threshold-limited (FEASIBILITY_SIM C4). Probably
   two or more PMTs per cell; PMTs are already short.
3. Weight and mechanics: 54 L of liquid per arm is ~47 kg plus the can, on the arm stand.
4. Safety: flammable liquid (if EJ-301/BC-501A-like) in the hall: LNL rules, with the gas premix (L2).

## 4. Liquid in front: right behind the SiPM wall, the plastics behind it (Dylan, 20 Nov)

Code: `../sim2arm/leg_layout.py` → `../sim2arm/out/leg_layout.csv` (15 s). **A scaling estimate:** the geometric leg
toy of `FEASIBILITY_SIM.md` §9 (fitted to the Geant4 X17 pair-tags), horizontal pair only, counting in 125–155°; days
∝ B/S², applied to the Geant4 hemisphere reach (151 d to 3σ, 2.35 × R(ATOMKI) in 5 d, liquid working).

| layout | X17 pairs | days to 3σ | 90 % limit in 5 d |
|---|---|---|---|
| A. as now: leg = SiPM × plastics (2 × 20×30); liquid behind, energy only | ×1 | 151 | 2.35 × |
| B. as now, but the liquid also makes a leg | ×1.7 | ~83 | ~1.7 × |
| **C. liquid 45×45 right behind the SiPM wall, the 2 plastics behind; leg = SiPM × (liquid OR plastic)** | **×4.2** | **~34** | **~1.1 ×** |
| D. as C with 3 plastics (60 × 30) behind | ×4.8 | ~30 | ~1.0 × |
| E. 3 plastics 60 × 30, no liquid in the leg | ×1.9 | ~79 | ~1.7 × |
| F. a 60 × 60 cell right behind the SiPM wall | ×7.2 | ~20 | ~0.85 × |

- **The gain is the trigger leg, not the order as such.** Today a lepton needs a SiPM bar and a 40 × 30 cm plastic; the
  liquid only adds energy. A 45 × 45 cell 10 cm closer covers ~4× more pairs, and the IPC grows with it (S/B unchanged),
  so the days fall as 1/S. B shows half of it with the cell where it is now.
- **The plastics behind add almost no acceptance** (C with or without them is the same): they sit in the cell's shadow.
  Their use is calorimetry: 2 cm liquid + 2 cm plastic stops more of the soft lepton. The third block (D) gains ×1.15 in
  the toy, and less in reality, since a lepton loses ~4 MeV in the liquid before reaching it. Possible (8 plastics exist,
  inventory `plast_small`), but it costs 2 more PMTs, which are short.
- **Not in the toy, for the Geant4 run:** cosmics (half of the selected background with the hemisphere; their legs grow
  with the area too, so they should scale roughly like the IPC); the E_sum window for leptons that hit only 2 cm of
  liquid (worse calorimetry outside the plastics); the extra energy threshold to reach the plastics.
- Mechanics: the gap SiPM wall → plastics is 6.1–6.5 cm; the n_TOF can (2.1 cm, faces bulged ~1.3 cm each) would fit, and
  the new cans can be designed for it (ask). Trigger: the leg uses the liquid PMT in the 20 ns coincidence; the
  arm-to-arm TOF stays on the SiPM walls. Beam singles roughly double (~150 Hz per arm at 1.10 MeV): fine for DREAM.

## 5. To do (plan.py)

- **S6** Geant4 thickness scan of the liquid (2, 2 + 2 in series, 4, 5 cm; two arms, the hemisphere, L18 tables):
  expose `ls_slab_thick_cm`, `ls_slab_u/v_cm`, `ls_fill_liters` and the cell position on the MX17_Full_Geant command line.
- **S7** Geant4 run with an oversized liquid cell (like `--big-plastic`; cut smaller squares offline) at 35, 41 and 47 cm:
  replaces the toy above; decides whether wide cells replace the big plastics for slot 2.
- **R11** Geant4 of layout C (and F): the liquid right behind the SiPM wall, leg = SiPM × (liquid OR plastic), as L18;
  needs the LS position and size on the command line (S6) and the leg definition in the reduction.
- **S8** Ask Pierfrancesco: how much liquid (~60 L?), which liquid, who remakes the cans, how many PMTs exist, and what he
  means by "in parallel / in series".
