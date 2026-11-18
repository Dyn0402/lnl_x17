"""Two-arm feasibility run at LNL: what 8 beam days can show.

A SCALING ESTIMATE, not a simulation. It takes the four-arm Geant4 reach of
x17_facility_search/lnl/FEASIBILITY_SIM.md §19.3 (reference fit, days to 3 sigma at
R(ATOMKI) = 5.8e-6, 1 uA, 1.10 MeV, m_X = 16.8, MM 15 deg + TOF) and scales it to two
opposite arms.

Why x2 in days: the ~140 deg X17 pairs and the large-angle IPC in the fit window are
seen through opposite arms (lnl/README.md, ESTIMATES.md §2). Keeping one of the two
opposite pairs halves both S and B in the window, so Z per day drops by sqrt(2) and the
days to a given Z double. Adjacent-arm pairs sit at 25-92 deg and carry no X17. The
range F_LO..F_HI covers the per-arm leg efficiency and the angular edges.
To be replaced by a two-arm re-reduction of the existing L10-L13 tables (planning task R1).

Outputs planning/out/two_arm_reach.csv and planning/out/beam_days.csv.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

OUT = Path(__file__).resolve().parent / "out"
OUT.mkdir(exist_ok=True)

R_ATOMKI = 5.8e-6          # Gamma_X / Gamma_gamma at 18.15 MeV (ATOMKI 2016)
R_MEG2_90 = 1.2e-5         # MEG II 90 % CL upper limit at 18.1 MeV (2025)
Z90 = 1.2816               # one-sided 90 % CL in Gaussian units

F_LO, F_C, F_HI = 1.7, 2.0, 2.5   # two-arm / four-arm days

# Four-arm days to 3 sigma at R(ATOMKI), FEASIBILITY_SIM.md §19.3 (central, low, high).
FOUR_ARM = [
    # (target, energy stack, central, low, high, note)
    ("Al ogive + Cu liner", "SiPM wall + small plastics (no liquid)", 30.5, 28, 33, "§19.3 'liquid off'"),
    ("Al ogive + Cu liner", "  + liquid as at n_TOF", 8.5, 7, 10, "§19.3"),
    ("Al ogive + Cu liner", "  + liquid repaired", 4.5, 3.6, 5.5, "§19.3"),
    ("Cu ogive", "SiPM wall + small plastics (no liquid)", 45, 40, 50, "§19.3 'liquid off'"),
    ("Cu ogive", "  + liquid as at n_TOF", 11, 9, 14, "§19.3"),
    ("Cu ogive", "  + liquid repaired", 6, 5, 8, "§19.3"),
]

# The 8-day request (Pierfrancesco, 18 Nov 2026: "8 days are due and feasible").
BEAM_PLAN = [
    # (day, E_p, what, beam)
    ("1", "1.10 MeV", "Beam on target at low current; target conditioning; current scan 0.05 → 1 µA: "
                      "trigger rates, DREAM live time, Micromegas occupancy, SiPM/plastic singles", "on"),
    ("2", "0.441 MeV", "Locate the 441 keV resonance on the γ yield (17.64 MeV, M1); IPC calibration run", "on"),
    ("3", "0.441 MeV", "IPC calibration run: opening-angle resolution, acceptance, energy scale against Geant4", "on"),
    ("4", "1.10 MeV", "18.15 MeV region: IPC spectrum, X17 window", "on"),
    ("5", "1.10 MeV", "18.15 MeV region (cont.)", "on"),
    ("6", "1.10 MeV", "18.15 MeV region (cont.)", "on"),
    ("7", "1.10 MeV", "18.15 MeV region (cont.); end-of-run target check (γ yield vs day 4)", "on"),
    ("8", "1.10 MeV", "18.15 MeV region (cont.), or 0.80 MeV off-resonance if the target allows; contingency", "on"),
    ("nights/weekend", "—", "Beam-off cosmic runs with the full trigger: the cosmic background model, measured", "off"),
]
DAYS_ON_RES = 5.0          # days 4-8 at 1.10 MeV
LIVE = 0.95                # already inside the §19.3 numbers; kept here only for the text

# 441 keV calibration: 12-24 k selected pairs / day at 1 uA with four arms (§19.5).
CAL_4ARM = (12e3, 24e3)


def z_at_atomki(days_to_3sigma: float, days: float) -> float:
    return 3.0 * math.sqrt(days / days_to_3sigma)


def r90(days_to_3sigma: float, days: float) -> float:
    """Expected 90 % CL upper limit on R if no signal: Z is linear in R (background-dominated)."""
    return Z90 / z_at_atomki(days_to_3sigma, days) * R_ATOMKI


def main() -> None:
    rows = []
    for tgt, stack, c, lo, hi, src in FOUR_ARM:
        d2 = (lo * F_LO, c * F_C, hi * F_HI)
        z = z_at_atomki(d2[1], DAYS_ON_RES)
        rows.append(dict(
            target=tgt, energy_stack=stack.strip(), four_arm_days=c, four_arm_range=f"{lo}-{hi}",
            two_arm_days=round(d2[1], 1), two_arm_range=f"{d2[0]:.0f}-{d2[2]:.0f}",
            z_in_5d=round(z, 2),
            z_in_5d_range=f"{z_at_atomki(d2[2], DAYS_ON_RES):.2f}-{z_at_atomki(d2[0], DAYS_ON_RES):.2f}",
            r90_5d=f"{r90(d2[1], DAYS_ON_RES):.2e}",
            r90_over_atomki=round(r90(d2[1], DAYS_ON_RES) / R_ATOMKI, 2),
            r90_over_megii=round(r90(d2[1], DAYS_ON_RES) / R_MEG2_90, 2),
            source=src))
    with open(OUT / "two_arm_reach.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    with open(OUT / "beam_days.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["day", "E_p", "what", "beam"])
        w.writerows(BEAM_PLAN)

    cal = [x / F_C for x in CAL_4ARM]
    print(f"441 keV calibration, two arms: {cal[0]:.0f}-{cal[1]:.0f} selected pairs/day at 1 uA "
          f"-> {2*cal[0]/1e3:.0f}-{2*cal[1]/1e3:.0f} k in 2 days")
    print(f"{'target':22s} {'stack':42s} 4arm  2arm (range)   Z(5d)  R90/ATOMKI R90/MEGII")
    for r in rows:
        print(f"{r['target']:22s} {r['energy_stack']:42s} {r['four_arm_days']:5}  {r['two_arm_days']:5} "
              f"({r['two_arm_range']:>7s})  {r['z_in_5d']:4}   {r['r90_over_atomki']:5}     {r['r90_over_megii']}")


if __name__ == "__main__":
    main()
