"""Proposal figure: expected 90 % CL limit on R vs days at 1.10 MeV, two arms (scaling estimate).

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

# Cu ogive rows (the last three of FOUR_ARM): the Cu hemisphere is already built, the likely target (Dylan, 19 Nov); slot colours = dataviz reference, fixed order.
ROWS = [(E.FOUR_ARM[i], lab, col) for i, lab, col in [
    (3, "SiPM wall + small plastics", "#2a78d6"),
    (4, "+ liquid cells as at n_TOF", "#eb6834"),
    (5, "+ liquid cells repaired", "#1baf7a"),
]]


def main() -> None:
    days = np.linspace(0.5, 10, 96)
    fig, ax = plt.subplots(figsize=(6.4, 3.6), dpi=150)
    out = []
    for (tgt, stack, c, lo, hi, _), lab, col in ROWS:
        mid = [E.r90(c * E.F_C, d) / 1e-6 for d in days]
        band_lo = [E.r90(lo * E.F_LO, d) / 1e-6 for d in days]
        band_hi = [E.r90(hi * E.F_HI, d) / 1e-6 for d in days]
        ax.fill_between(days, band_lo, band_hi, color=col, alpha=0.15, lw=0)
        ax.plot(days, mid, color=col, lw=2, label=lab)
        for d, m, a, b in zip(days, mid, band_lo, band_hi):
            out.append([lab, round(d, 3), round(m, 3), round(a, 3), round(b, 3)])
    ax.axhline(E.R_ATOMKI / 1e-6, color="#52514e", lw=1.2, ls="--")
    ax.text(9.9, E.R_ATOMKI / 1e-6 * 0.95, "ATOMKI 5.8×10⁻⁶", ha="right", va="top", fontsize=8, color="#52514e")
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
    ax.set_title("Two opposite MX17 arms, Cu hemisphere target (×2 scaling of 4-arm Geant4)", fontsize=9)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="y", which="both", color="#e1e0d9", lw=0.6)
    ax.legend(fontsize=8, frameon=False, loc="lower left")
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(FIG / f"limit_vs_days.{ext}")
    with open(FIG / "limit_vs_days.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["stack", "days", "r90_1e-6", "r90_lo_1e-6", "r90_hi_1e-6"])
        w.writerows(out)
    print("wrote", FIG / "limit_vs_days.pdf")


if __name__ == "__main__":
    main()
