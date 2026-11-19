"""Proposal figure: expected 90 % CL limit on R vs days at 1.10 MeV, two opposite arms (Geant4, sim2arm).

Reads planning/out/two_arm_reach.csv (two_arm_estimates.py, run it first): Cu hemisphere, horizontal pair, MM pointing +
0.3 ns TOF, the three energy stacks; solid = 11 µm Li (recommended), thin dashed = 20 µm (as simulated).
Writes proposal/latex/figures/limit_vs_days.{pdf,png} and the .csv beside them.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker  # noqa: F401
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import two_arm_estimates as E  # noqa: E402

FIG = HERE.parent / "proposal" / "latex" / "figures"
FIG.mkdir(parents=True, exist_ok=True)
#: dataviz reference categorical slots, fixed order
COLS = {"SiPM wall + small plastics (no liquid)": ("#2a78d6", "walls + plastics, no liquid"),
        "+ liquid as at n_TOF": ("#eb6834", "+ liquid cells as at n_TOF"),
        "+ liquid working": ("#1baf7a", "+ liquid cells working")}


def rows():
    with open(HERE / "out" / "two_arm_reach.csv") as f:
        return [r for r in csv.DictReader(f) if r["target"].startswith("Cu") and r["geometry"] == "horizontal pair"
                and "TOF" in r["veto"]]


def main() -> None:
    days = np.linspace(0.5, 10, 96)
    fig, ax = plt.subplots(figsize=(6.4, 3.6), dpi=150)
    out = []
    for r in rows():
        col, lab = COLS[r["energy_stack"]]
        thin = r["film"].startswith("20")
        lo, c, hi = float(r["d2_lo"]), float(r["d2_c"]), float(r["d2_hi"])
        mid = [E.r90(c, d) / 1e-6 for d in days]
        if thin:
            ax.plot(days, mid, color=col, lw=1, ls="--")
        else:
            ax.fill_between(days, [E.r90(hi, d) / 1e-6 for d in days], [E.r90(lo, d) / 1e-6 for d in days],
                            color=col, alpha=0.15, lw=0)
            ax.plot(days, mid, color=col, lw=2, label=lab)
        for d, m in zip(days, mid):
            out.append([r["film"], lab, round(d, 3), round(m, 3)])
    ax.plot([], [], color="#52514e", lw=1, ls="--", label="dashed: 20 µm film")
    ax.axhline(E.R_ATOMKI / 1e-6, color="#52514e", lw=1.2, ls="--")
    ax.text(9.9, E.R_ATOMKI / 1e-6 * 1.05, "ATOMKI 5.8×10⁻⁶", ha="right", va="bottom", fontsize=8, color="#52514e",
            bbox=dict(fc="white", ec="none", pad=0.5))
    ax.axhline(E.R_MEG2_90 / 1e-6, color="#52514e", lw=1.2, ls=":")
    ax.text(9.9, E.R_MEG2_90 / 1e-6 * 1.05, "MEG II 90 % CL", ha="right", va="bottom", fontsize=8, color="#52514e")
    ax.axvline(E.DAYS_ON_RES, color="#c3c2b7", lw=1)
    ax.text(E.DAYS_ON_RES + 0.1, 45, "5 d requested", fontsize=8, color="#52514e")
    ax.set_yscale("log")
    ax.set_ylim(1.5, 60)
    ax.set_yticks([2, 3, 5, 10, 20, 50])
    ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.set_xlim(0.5, 10)
    ax.set_xlabel("days at E$_p$ = 1.10 MeV, 1 µA")
    ax.set_ylabel("expected 90 % CL limit on R  (×10⁻⁶)")
    ax.set_title("Two opposite MX17 arms, Cu hemisphere, 11 µm Li (Geant4)", fontsize=9)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="y", which="both", color="#e1e0d9", lw=0.6)
    ax.legend(fontsize=7.5, frameon=False, loc="lower left")
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(FIG / f"limit_vs_days.{ext}")
    with open(FIG / "limit_vs_days.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["film", "stack", "days", "r90_1e-6"])
        w.writerows(out)
    print("wrote", FIG / "limit_vs_days.pdf")


if __name__ == "__main__":
    main()
