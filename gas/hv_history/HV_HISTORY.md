# The highest drift voltage our chambers have held

2026-11-26 (dylan-MS-7C84). Question (Dylan): what is the highest drift voltage any chamber held, in the early n_TOF
runs and on the cosmic bench, leaving out B at n_TOF (its drift was disconnected there)?

## 1. Method

We read every CAEN `hv_monitor.csv` on EOS (`/eos/experiment/ntof/data/x17/{july_beam,may_beam,feb_beam}/runs`,
`cosmic_bench/{june_tests,det_1,det_*_old}`), 14,923 chamber-sub-runs in all. For each run, `run_config.json` gives each
MX17 chamber's drift channel. For each sub-run, `scan_drift_hv.py` records the set value, the measured voltage (vmon),
the time the vmon stayed within 2 % of the set value, and the largest current (imon). The output is
`drift_hv_subruns.csv.gz` (one row per chamber and sub-run) and `drift_hv_summary.csv` (one row per chamber and set
value). A short second pass counted the small discharges at 900–1200 V: a dip of vmon by more than 4 V, or a current
spike above 1 µA.

The "tripped" flag in the CSV also fires on the ramp at the start of a sub-run. We therefore checked every high-voltage
case by hand. None of the cases below is a real trip.

## 2. Result: 1200 V, held by A on the bench and by A, C and D at n_TOF

| chamber | where, when, gas | highest drift held | how long | current | small discharges |
|---|---|---|---|---|---|
| **A** (det3, Stephan 15 Jun) | bench, 26 Jun, Ar/iC₄H₁₀ 95/5 | **1200 V** | 4.2 h | 0.41 µA | 56 per hour (mesh at 530 V, above working gain) |
| A | bench, 27 Jun, 95/5 | 1100 V | 15 min | 0.37 µA | 6 in 15 min |
| A | bench, 22–27 Jun, 95/5 | 1000 V | about 20 h at working gain | 0.34 µA | 0–1.5 per hour |
| **A** | n_TOF run 3, 3 Jul, Ar/CO₂ 70/30 | **1200 V** | 1.9 h (beam on and off) | 0.36 µA | none seen |
| **C** | n_TOF run 3, 3 Jul, Ar/CO₂ 70/30 | **1200 V** | 1.9 h | 0.36 µA | none seen |
| D | n_TOF run 3, 3 Jul, Ar/CO₂ 70/30 | 1200 V | 1.8 h | **8–25 µA** (leaking) | |
| A, C, D | n_TOF runs 1–4, Ar/CO₂ 70/30 | 1000 V | 6.8 h | 0.28–0.38 µA | |
| B (det2, Arnaud 12 Jun) | bench, 17–22 Jun, 95/5 | 1000 V | 29 h | 0.003 µA | none in 13 h |

The older prototype boards held more, but they are not the chambers we will use: 2000 V (February beam, Ar/CO₂
70/30, 1.25 h) and 1400 V (May beam, 6.4 h).

What this shows:

- **The present chambers have held 1200 V.** A did it twice, on the bench in Ar/iC₄H₁₀ and at n_TOF in Ar/CO₂. C did it
  at n_TOF. Nobody tried higher on these four chambers.
- **1000 V is clean.** A ran about 20 h at 1000 V with almost no discharges, and B ran 13 h with none.
- **The discharge rate at high drift appears to follow the mesh, not the drift.** At 1000 V on 27 June, A's dip rate
  rose from 0–4 per hour at a mesh of 455–490 V to 35–51 per hour at 515–525 V. The 1200 V bench run had the mesh at
  530 V. Its 56 dips per hour are therefore most likely amplification sparks seen through the drift supply. We did not
  run 1200 V at working gain, so this is not demonstrated.
- **D leaked at 1200 V** (8–25 µA against 0.36 µA for A and C, whose currents are ohmic like at 1000 V). D is not a
  slot-1 chamber.
- **The 800 V sparking of A on 17 July (run 51) came after this.** A held 1200 V on 3 July and sparked at 800 V on
  17 July in Ar/iC₄H₁₀ 95/5. Something changed in between. A's drift current at 800 V reached 39 µA during the July
  runs. Finding out what changed (the window, a contaminant, the cathode edge) is the work that would bring back
  1000–1200 V.

## 3. At n_TOF the drift discharges followed the quencher

At n_TOF all chambers ran 800 V on the drift through five gas periods. We counted the sub-runs in which the drift
current spiked above 2 µA, which is about 6 times the ohmic current. The table gives the rate per hour of running at
800 V.

| gas (dates) | A | C | D |
|---|---|---|---|
| Ar/CF₄/iC₄H₁₀ 88/10/2 (4–7 Jul, 34 h) | 0 | 0 | 0 |
| **Ar/iC₄H₁₀ 95/5** (8–11 Jul and 16–17 Jul, 53–56 h) | **0.39 /h** | 0 | **2.2 /h** |
| Ar/iC₄H₁₀ 80/20 (11–12 Jul, 6 h) | 0 | 0 | |
| Ar/iC₄H₁₀ 90/10 (12–19 Jul, 56–88 h) | 0 | 0 | 0.11 /h |

What this shows:

- **The drift discharges appear with the least quenched gas we ran, 95/5.** They stop in 90/10, and they come back
  when we return to 95/5 on 16–17 July. The gas is therefore the cause, not the passing time or a slow damage.
- C, the chamber that never discharged, ran through the same gases.
- This was under the n_TOF beam, with its gamma flash and neutron-induced recoils. LNL has neither, and on the bench
  (cosmics only) A held 1200 V in 95/5. The effect will therefore be weaker at LNL. However, it is the one direct
  measurement we have of the quencher on these chambers, and it points the same way as Dylan's worry: **less quencher
  than 95/5 is a risk on the drift side as well as on the mesh**. The bench test M5 should include a drift scan to
  1000–1200 V in each candidate gas, with a source or cosmics.

## 4. What we use

The gas plots (`gas/voltage_plots.py`, `gas/compare_gases.py`) now run from 400 to 1200 V. Green marks the design limit
(≤ 700 V), orange 700–800 V, and purple 800–1200 V ("held in our logs"). This assumes A's July problem can be fixed and
B's drift repair restores its 1000 V.

## 5. Files

| path | what |
|---|---|
| `scan_drift_hv.py` | the scan (`ssh lxplus python3 - < scan_drift_hv.py > drift_hv_subruns.csv`, about 10 min) |
| `drift_hv_subruns.csv.gz` | every chamber and sub-run |
| `drift_hv_summary.csv` | per chamber and set value: hours held, largest current, runs, gases |
