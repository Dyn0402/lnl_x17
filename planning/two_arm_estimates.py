"""Two-arm feasibility run at LNL: what 8 beam days can show.

Updated 2026-11-20: the two-arm numbers for the BUILT Cu hemisphere (R 11 mm, 300 µm, rim, grey flange; Geant4 dome300)
come from the SIMULATION (sim2arm/TWO_ARM_STUDY.md): the FEASIBILITY_SIM §19 reference fit run on one pair of arms of the
L10 + L18 Geant4 tables, with the L15 cosmics (every zenith angle). sim2arm/out/summary_reach<SIM_TAG>.csv holds them.
Until 20 Nov these rows came from the Cu OGIVE of the 27 Oct sketch (ogCu200, L11 + L13, pass 3), which is not built.
The Al ogive + Cu liner has no two-arm simulation: its two-arm days are the four-arm §19.3 days times the two-arm /
four-arm ratio simulated for the Cu ogive (pass 3, the same shape; an estimate, marked so).

Rows: target x energy stack (liquid working / as at n_TOF / none) x geometry (horizontal / vertical pair) x cosmic
veto (MM pointing + 0.6 ns TOF, the reference; pointing only).

Outputs planning/out/two_arm_reach.csv and planning/out/beam_days.csv.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
SIM = HERE.parent / "sim2arm" / "out"
SIM_TAG = "_pass4"          # dome300, the built hemisphere
OG_TAG = "_pass3"           # ogCu200, the Cu ogive: the two-arm / four-arm ratio for the Al ogive rows
#: the Al ogive + Cu liner's own two-arm tables (task R10, 2026-11-25, sim2arm/R10_AL_OGIVE.md), newest first.  When one
#: exists its rows replace the scaling below; rows it does not hold (the vertical pair) are dropped, not scaled.
AL_TAGS = ("_pass5al_l13", "_pass5al")
#: (label, suffix of the summary table): the simulated 20 µm film and the review's 10–12 µm (yields of 11 µm)
FILMS = [("11 µm Li (recommended)", "li11"), ("20 µm Li (as simulated)", "")]

R_ATOMKI = 5.8e-6          # Gamma_X / Gamma_gamma at 18.15 MeV (ATOMKI 2016)
R_MEG2_90 = 1.2e-5         # MEG II 90 % CL upper limit at 18.1 MeV (2025)
Z90 = 1.2816               # one-sided 90 % CL in Gaussian units

# the old scaling (kept for the Al ogive and as the fallback when the simulation table is missing)
F_LO, F_C, F_HI = 1.7, 2.0, 2.5

STACKS = [  # (label, sim response, four-arm §19.3 key)
    ("SiPM wall + small plastics (no liquid)", "LNL calibrated, LS off", "off"),
    ("+ liquid as at n_TOF", "n_TOF as is", "ntof"),
    ("+ liquid working", "LNL calibrated", "fix"),
]
GEOMS = [("horizontal pair", "horiz"), ("vertical pair", "vert")]
VETOES = [("MM pointing + 0.6 ns TOF", "MM 15° + TOF"), ("MM pointing only", "MM 15° point, μ 3°")]

# Four-arm days to 3 sigma at R(ATOMKI), FEASIBILITY_SIM.md §19.3 (central, low, high), MM 15° + TOF.
FOUR_ARM = {
    ("Cu hemisphere (built)", "off"): (45, 40, 50),
    ("Cu hemisphere (built)", "ntof"): (11, 9, 14),
    ("Cu hemisphere (built)", "fix"): (6, 5, 8),
    ("Al ogive + Cu liner (lighter)", "off"): (30.5, 28, 33),
    ("Al ogive + Cu liner (lighter)", "ntof"): (8.5, 7, 10),
    ("Al ogive + Cu liner (lighter)", "fix"): (4.5, 3.6, 5.5),
}

# The 8-day request (2026-11-19, sim2arm/TWO_ARM_STUDY.md §7). The cosmic veto test runs before the beam.
BEAM_PLAN = [
    # (day, E_p, what, beam)
    ("before", "—", "Installation week, VERTICAL pair: ≥ 3 nights of cosmics with the full trigger. Measures the arm-to-arm "
                    "time of flight (σ_t), each arm's MIP gain and the rejection of every cosmic veto, in the worst geometry", "off"),
    ("1", "1.10 MeV", "Roll to the HORIZONTAL pair. Beam on target at low current; target conditioning; current scan 0.05 → 1 µA: "
                      "trigger rates, DREAM live time, Micromegas occupancy, SiPM/plastic singles; γ-yield reference", "on"),
    ("2", "0.441 MeV", "Locate the 441 keV resonance (singles rate); 17.64 MeV M1 IPC: absolute rate, opening-angle "
                       "shape and energy scale against Geant4 (~140 pairs/day above 90° in the E_sum window, built Cu hemisphere)", "on"),
    ("3", "1.10 MeV", "18.15 MeV region: IPC spectrum, X17 window", "on"),
    ("4", "1.10 MeV", "18.15 MeV region (cont.)", "on"),
    ("5", "1.10 MeV", "18.15 MeV region (cont.)", "on"),
    ("6", "1.10 MeV", "18.15 MeV region (cont.)", "on"),
    ("7", "1.10 MeV", "18.15 MeV region (cont.); end-of-run target check (γ yield vs day 1)", "on"),
    ("8", "1.10 MeV", "Half a day with the arms ADJACENT (90°): small-angle IPC and external conversions at 6× the "
                      "opposite-pair rate; then back to opposite, or contingency", "on"),
    ("nights", "—", "Any beam-off time: cosmics with the full trigger in the physics geometry", "off"),
]
DAYS_ON_RES = 5.0          # days 3-7 at 1.10 MeV
LIVE = 0.95                # inside the fit numbers

# 441 keV: two arms, selected M1 pairs per day above 90° (sim2arm spectra, MM 15° + TOF, liquid working)
CAL_2ARM_PER_DAY = (120, 160)   # built Cu hemisphere (predictions.py, 20 Nov: 141/day); the Cu ogive gave 550-700


def z_at_atomki(days_to_3sigma: float, days: float) -> float:
    return 3.0 * math.sqrt(days / days_to_3sigma)


def r90(days_to_3sigma: float, days: float) -> float:
    """Expected 90 % CL upper limit on R if no signal: Z is linear in R (background-dominated)."""
    return Z90 / z_at_atomki(days_to_3sigma, days) * R_ATOMKI


def sim_rows(suffix="", tag=None):
    f = SIM / f"summary_reach{tag or SIM_TAG}{suffix}.csv"
    if not f.exists():
        return None
    with open(f) as fh:
        return {(r["pair"], r["resp"], r["level"]): r for r in csv.DictReader(fh)}


def main() -> None:
    rows = []
    sim20 = sim_rows("")
    og20 = sim_rows("", OG_TAG)
    for film, suffix in FILMS:
        al, al_tag = next(((t, tag) for tag in AL_TAGS if (t := sim_rows(suffix, tag))), (None, None))
        rows += film_rows(film, sim_rows(suffix), sim20, sim_rows(suffix, OG_TAG), og20, al, al_tag)
    write(rows)


def film_rows(film, sim, sim20, og, og20, al=None, al_tag=None):
    """sim: this film's simulated table (the Cu hemisphere); sim20: its 20 µm one.  og, og20: the same for the Cu ogive
    (pass 3), whose ratios scale the Al ogive's four-arm §19.3 days: Al(4 arms, 20 µm) × Cu ogive(this row) /
    Cu ogive(4 arms, 20 µm)."""
    rows = []
    for tgt in ("Cu hemisphere (built)", "Al ogive + Cu liner (lighter)"):
        for stack, resp, key in STACKS:
            c4, lo4, hi4 = FOUR_ARM[(tgt, key)]
            for glab, pair in GEOMS:
                for vlab, level in VETOES:
                    T, T20 = (sim, sim20) if tgt.startswith("Cu") else (og, og20)
                    if tgt.startswith("Al") and al:              # R10: the holder's own tables, cut to the pair
                        a2, a4 = al.get((pair, resp, level)), al.get(("all", resp, level))
                        if a2 is None:
                            continue
                        d2 = (float(a2["days3_lo"]), float(a2["days3"]), float(a2["days3_hi"]))
                        d4 = (float(a4["days3_lo"]), float(a4["days3"]), float(a4["days3_hi"])) if a4 else d2
                        thin = "" if "l13" in al_tag else ", L12 tables only (thin Monte Carlo: interim)"
                        src = src4 = f"Geant4, the Al ogive + Cu liner's own tables (sim2arm/R10_AL_OGIVE.md{thin})"
                        rows.append(row(tgt, film, stack, glab, vlab, d2, d4, src, src4))
                        continue
                    s = T.get((pair, resp, level)) if T else None
                    s4 = T.get(("all", resp, "MM 15° + TOF")) if T else None
                    s420 = T20.get(("all", resp, "MM 15° + TOF")) if T20 else None
                    if s is None:
                        if level != "MM 15° + TOF" or pair != "horiz":
                            continue
                        d2 = (lo4 * F_LO, c4 * F_C, hi4 * F_HI)
                        src = "×2 scaling of §19.3 (no simulation table)"
                    elif tgt.startswith("Cu"):
                        d2 = (float(s["days3_lo"]), float(s["days3"]), float(s["days3_hi"]))
                        src = "Geant4, two-arm re-reduction (sim2arm)"
                    else:
                        k = float(s["days3"]) / float(s420["days3"]) if s420 else F_C
                        d2 = (lo4 * k * float(s["days3_lo"]) / float(s["days3"]), c4 * k,
                              hi4 * k * float(s["days3_hi"]) / float(s["days3"]))
                        src = (f"§19.3 four-arm (20 µm) × {k:.2f} = the Cu ogive's simulated ratio of this row to its "
                               f"four arms at 20 µm: estimate")
                    if tgt.startswith("Cu") and s4 is not None:     # four arms: the same simulation, all pairs
                        d4 = (float(s4["days3_lo"]), float(s4["days3"]), float(s4["days3_hi"]))
                        s4l = T.get(("all", resp, level))
                        if s4l is not None:
                            d4 = (float(s4l["days3_lo"]), float(s4l["days3"]), float(s4l["days3_hi"]))
                        src4 = "Geant4, four arms, same fit (sim2arm)"
                    else:
                        f4 = float(s4["days3"]) / float(s420["days3"]) if (s4 is not None and s420 is not None) else 1.0
                        d4 = (lo4 * f4, c4 * f4, hi4 * f4)
                        src4 = "FEASIBILITY_SIM §19.3" + (f" × {f4:.2f} (film)" if f4 != 1.0 else "")
                    rows.append(row(tgt, film, stack, glab, vlab, d2, d4, src, src4))
    return rows


def row(tgt, film, stack, glab, vlab, d2, d4, src, src4):
    z = z_at_atomki(d2[1], DAYS_ON_RES)
    return dict(
        target=tgt, film=film, energy_stack=stack, geometry=glab, veto=vlab, four_arm_days=round(d4[1], 1),
        four_arm_range=f"{d4[0]:.0f}-{d4[2]:.0f}", d4_lo=round(d4[0], 2), d4_c=round(d4[1], 2),
        d4_hi=round(d4[2], 2), d2_lo=round(d2[0], 2), d2_c=round(d2[1], 2), d2_hi=round(d2[2], 2),
        four_arm_source=src4, two_arm_days=round(d2[1], 1),
        two_arm_range=f"{d2[0]:.0f}-{d2[2]:.0f}", z_in_5d=round(z, 2),
        z_in_5d_range=f"{z_at_atomki(d2[2], DAYS_ON_RES):.2f}-{z_at_atomki(d2[0], DAYS_ON_RES):.2f}",
        r90_5d=f"{r90(d2[1], DAYS_ON_RES):.2e}",
        r90_over_atomki=round(r90(d2[1], DAYS_ON_RES) / R_ATOMKI, 2),
        r90_over_megii=round(r90(d2[1], DAYS_ON_RES) / R_MEG2_90, 2),
        source=src)


def write(rows):
    with open(OUT / "two_arm_reach.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    with open(OUT / "beam_days.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["day", "E_p", "what", "beam"])
        w.writerows(BEAM_PLAN)
    print(f"441 keV calibration, two arms: {CAL_2ARM_PER_DAY[0]}-{CAL_2ARM_PER_DAY[1]} M1 pairs/day above 90 deg")
    print(f"{'film':24s} {'target':30s} {'stack':40s} {'geometry':16s} {'veto':25s} 2arm (range)  Z(5d) R90/ATOMKI R90/MEGII")
    for r in rows:
        print(f"{r['film']:24s} {r['target']:30s} {r['energy_stack']:40s} {r['geometry']:16s} {r['veto']:25s} {r['two_arm_days']:6} "
              f"({r['two_arm_range']:>7s})  {r['z_in_5d']:4}  {r['r90_over_atomki']:5}  {r['r90_over_megii']}")


if __name__ == "__main__":
    main()
