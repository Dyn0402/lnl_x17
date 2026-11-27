#!/usr/bin/env python3
"""The figures of the LNL PAC proposal (2026-11-25), drawn at their final print size (text width 16.5 cm).

    python3 proposal/figsrc/make_figures.py          -> proposal/latex/figures/

    fig_event.pdf        Fig. 1c: two real Geant4 events in the two-arm set-up (an X17 pair, a cosmic muon), seen along the
                         beam, with a zoom on the Cu hemisphere.        Input: sim2arm/out/events3d.json (run L17d)
    fig_predictions.pdf  Fig. 2: what the run should see (Geant4): cosmic nights, the 441 keV day, the 1.10 MeV days.
                         Inputs: sim2arm/out/cosmic_theta.csv (L15), sim2arm/out/two_arm_spectra_pass4li11_l19.csv (pass 4 + L19)
    fig_reach.pdf        Fig. 3: expected limit against days, and the days to a 3 sigma test from this run to the full
                         experiment.                                    Input: planning/out/two_arm_reach.csv
    fig1a_ntof_photo.jpg, fig1b_ntof_fans.png   copied / cropped from figsrc/ (photo of MX17 at n_TOF EAR2, 2026-08-10;
                         run 145 tracks of arms A and C, make_ntof_fans.py)

Every number drawn is read from those tables; nothing is re-derived here except the two marked scalings in reach().
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Circle, Polygon, Rectangle

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
FIG = ROOT / "proposal" / "latex" / "figures"
SIM = ROOT / "sim2arm" / "out"
sys.path.insert(0, str(ROOT / "planning"))
import two_arm_estimates as E  # noqa: E402

W = 16.5 / 2.54                      # text width, inches
INK, MUTED, GRID = "#1a1a1a", "#5f5e5a", "#dddcd5"
# dataviz reference categorical slots (light), fixed order
BLUE, ORANGE, AQUA, YELLOW, MAGENTA, GREEN, VIOLET = ("#257de0", "#f47230", "#00b894", "#f2a600", "#ee7fac", "#008a17",
                                                      "#6a4ce2")
plt.rcParams.update({
    "font.family": "serif", "font.serif": ["Nimbus Roman", "Times New Roman", "STIXGeneral"], "mathtext.fontset": "stix",
    "font.size": 8, "axes.labelsize": 8, "axes.titlesize": 8, "xtick.labelsize": 7.5, "ytick.labelsize": 7.5,
    "legend.fontsize": 7, "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "xtick.major.size": 2.5, "ytick.major.size": 2.5, "xtick.minor.size": 1.5, "ytick.minor.size": 1.5,
    "axes.edgecolor": INK, "text.color": INK, "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK,
    "pdf.fonttype": 42, "savefig.dpi": 600,
})


def strip(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def tag(ax, s, x=0.0, y=1.03):
    ax.text(x, y, s, transform=ax.transAxes, ha="left", va="bottom", fontsize=8, fontweight="bold")


# The request (26 Nov, two_arm_estimates.py): 8 BEAM DAYS on the CN, each 24 h at 80 % operator efficiency (19.2 h of beam).
# Day 1 scan (~2 h) + 1.10 MeV, day 2 H2+ (441 keV), days 3-7 at 1.10 MeV, day 8 arms at 90 deg: 113 h = 5.9 beam days at
# 1.10 MeV with the opposite arms.  (Until 26 Nov: 8 working days of 8 h, 46 h.)
H441, H110 = E.H441, E.H110
REQ_DAYS = E.RUN_DAYS24              # days of 24 h of beam, the unit of E.r90
REQ_BD = E.RUN_BEAM_DAYS             # the same in beam days
BD = E.OPER_EFF                      # one beam day = BD days of 24 h of beam

# --------------------------------------------------------------------------------------------------------- Fig. 1c
def fig_event():
    ev = json.load(open(SIM / "events3d.json"))
    G = ev["geometry"]
    x17 = next(e for e in ev["events"] if e["kind"] == "x17" and e["eventID"] == 1238)
    mu = next(e for e in ev["events"] if e["kind"] == "mu_h" and e["eventID"] == 6819)
    RED = "#d63a2f"

    wcm, hcm = 7.1, 4.9
    fig = plt.figure(figsize=(wcm / 2.54, hcm / 2.54))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(-545, 545)
    ax.set_ylim(-545 * hcm / wcm - 25, 545 * hcm / wcm - 25)
    ax.set_aspect("equal")
    ax.axis("off")

    # the two arms, view along the beam: x horizontal, z (up) vertical; arm 0 at +x, arm 1 at -x
    style = {"drift": (BLUE, 0.22, "Micromegas TPC"), "pcb": ("#8a8983", 0.55, None), "support": ("#8a8983", 0.25, None),
             "sipm": (AQUA, 0.75, "SiPM wall"), "plastic": (VIOLET, 0.45, "plastic"), "ls": (YELLOW, 0.30, "liquid cell")}
    DR0, DR1 = next((L["r0"], L["r1"]) for L in G["layers"] if L["k"] == "drift")
    for arm, sgn in ((0, 1), (1, -1)):
        sh = G["arm_shift"][arm]
        for L in G["layers"]:
            if L["k"] not in style:
                continue
            c, a, _ = style[L["k"]]
            offs = [s * (L["u"] + L["gap"]) / 2 for s in (-1, 1)] if L["k"] == "plastic" else [0.0]
            for o in offs:
                x0 = sgn * L["r0"] if sgn > 0 else -L["r1"]
                ax.add_patch(Rectangle((x0, sh + o - L["u"] / 2), L["r1"] - L["r0"], L["u"], facecolor=c, alpha=a,
                                       edgecolor="none", zorder=2))
                ax.add_patch(Rectangle((x0, sh + o - L["u"] / 2), L["r1"] - L["r0"], L["u"], facecolor="none",
                                       edgecolor=INK, lw=0.35, zorder=3))
    # layer names, under arm B (left)
    for k, xt, yt, ha in (("drift", -150, -292, "center"), ("sipm", -300, -340, "center"), ("plastic", -424, -292, "center"),
                          ("ls", -470, -340, "center")):
        L = next(l for l in G["layers"] if l["k"] == k)
        xc = -(L["r0"] + L["r1"]) / 2
        ybot = G["arm_shift"][1] - (L["u"] if k != "plastic" else 2 * L["u"] + L["gap"]) / 2
        ax.plot([xc, xc if k != "drift" else xt + 40], [ybot - 5, yt + 8], color=MUTED, lw=0.4, zorder=1)
        ax.text(xt, yt, style[k][2], ha=ha, va="top", fontsize=6.5, color=INK)
    ax.text(365, 258, "arm 1", ha="center", va="bottom", fontsize=7.5, fontweight="bold")
    ax.text(-365, 258, "arm 2", ha="center", va="bottom", fontsize=7.5, fontweight="bold")

    # beam pipe (stainless tube, end-on) and target
    ax.add_patch(Circle((0, 0), 19.05, facecolor="white", edgecolor=MUTED, lw=0.6, zorder=4))
    ax.add_patch(Circle((0, 0), 5, facecolor=ORANGE, edgecolor="none", zorder=6))

    m = np.array(next(t for t in mu["tracks"] if t["id"] == 1)["pts"])
    ax.plot(m[:, 0], m[:, 2], color=INK, lw=0.9, ls=(0, (4, 2)), zorder=5)
    ang = np.degrees(np.arctan2(m[0, 2] - m[-1, 2], m[0, 0] - m[-1, 0]))
    ax.text(-118, -88, "cosmic muon", ha="center", va="center", fontsize=6.5, rotation=ang, rotation_mode="anchor")
    em = np.array(next(t for t in x17["tracks"] if t["id"] == 1)["pts"])
    ep = np.array(next(t for t in x17["tracks"] if t["id"] == 2)["pts"])
    for p, c, lab in ((em, BLUE, r"$e^-$"), (ep, RED, r"$e^+$")):
        ax.plot(p[:, 0], p[:, 2], color=c, lw=1.3, solid_capstyle="round", zorder=5)
        sx = np.sign(p[-1, 0])
        o = np.argsort(np.abs(p[:, 0]))
        o = o[: int(np.argmax(np.abs(p[o, 0]) > 260)) + 1] if (np.abs(p[:, 0]) > 260).any() else o
        xs = np.linspace(DR0, DR1, 12)                               # the segment that the TPC measures (drift gap)
        ax.plot(sx * xs, np.interp(xs, np.abs(p[o, 0]), p[o, 2]), color=INK, lw=2.6, solid_capstyle="butt", zorder=7)
        up = p[-1, 0] < 0                                            # label above the track on the left, below on the right
        ax.text(sx * (150 if up else 95), np.interp(150 if up else 95, np.abs(p[o, 0]), p[o, 2]) + (14 if up else -14), lab,
                ha="center", va="bottom" if up else "top", fontsize=8)
    ax.text(0, -150, r"X17 $\to e^+e^-$" "\n" rf"$\theta = {x17['truth']['theta']:.0f}^\circ$", ha="center", va="top",
            fontsize=7, linespacing=1.25)
    ax.plot([0, 0], [-144, -24], color=MUTED, lw=0.4)

    # scale bar
    ax.plot([200, 400], [-352, -352], color=INK, lw=1.2, solid_capstyle="butt")
    ax.text(300, -344, "200 mm", ha="center", va="bottom", fontsize=6.5)

    # ---- inset: the target, side view (beam from the left), drawn from the simulated geometry (dome300)
    ia = fig.add_axes([0.29, 0.625, 0.42, 0.365])
    ia.set_xlim(-40, 18)
    ia.set_ylim(-18.5, 18.5 + 5.6)
    ia.set_aspect("equal")
    ia.set_xticks([])
    ia.set_yticks([])
    for s in ia.spines.values():
        s.set_linewidth(0.5)
        s.set_edgecolor(MUTED)
    R, t, CU = 11.0, 0.3, "#c8763a"                     # Cu hemisphere: outer radius, wall (mm)
    th = np.linspace(-np.pi / 2, np.pi / 2, 80)
    yc = 0.5 - R                                        # the apex of the simulated dome profile is at y = +0.5 mm
    tw = 2.5 * t                                        # the wall is drawn 2.5 times thicker, to be visible
    outer = np.c_[yc + R * np.cos(th), R * np.sin(th)]
    inner = np.c_[yc + (R - tw) * np.cos(th[::-1]), (R - tw) * np.sin(th[::-1])]
    ia.add_patch(Polygon(np.r_[outer, inner], closed=True, facecolor=CU, edgecolor="none", zorder=3))
    for s in (1, -1):                                   # Cu rim (4 x 5 mm) and the beam tube
        ia.add_patch(Rectangle((yc - 5.0, 11.0 - tw if s > 0 else -15.0 + tw - 0.0), 5.0, 4.0, facecolor=CU,
                               edgecolor="none", zorder=3))
        ia.add_patch(Rectangle((-40, 13.6 if s > 0 else -15.2), 40 + yc - 5.0, 1.6, facecolor="#b9b8b2", edgecolor="none",
                               zorder=2))
    xf = yc + R - tw - 0.45
    ia.plot([xf, xf], [-2.8, 2.8], color=ORANGE, lw=1.8, solid_capstyle="butt", zorder=5)                  # the Li film
    ia.annotate("", xy=(xf - 0.6, 0), xytext=(-39, 0), arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.7,
                                                                        mutation_scale=5, shrinkA=0, shrinkB=0))
    ia.text(-38.5, 1.2, r"$p$ beam", ha="left", va="bottom", fontsize=6.5)
    ia.text(-38.5, -3.4, "Li film", ha="left", va="top", fontsize=6.5)
    ia.plot([-22.5, xf - 0.8], [-5.6, -1.6], color=MUTED, lw=0.4)
    ia.text(17.2, 13.0, "Cu wall,\n300 µm", ha="right", va="top", fontsize=6.5, linespacing=1.05)
    ia.plot([4.6, yc + R * np.cos(0.5) + 0.3], [8.6, R * np.sin(0.5) + 0.1], color=MUTED, lw=0.4)
    ia.text(-38.5, 23.2, "target holder, from above", ha="left", va="top", fontsize=6.5, fontweight="bold")
    for p, c in ((em, BLUE), (ep, RED)):               # the same pair, leaving through the wall (y-x plane)
        ia.plot(p[:3, 1], p[:3, 0], color=c, lw=1.0, zorder=6)
    fig.savefig(FIG / "fig_event.pdf")
    fig.savefig(FIG / "fig_event.png", dpi=300)
    plt.close(fig)


# ---------------------------------------------------------------------------------------------------------- Fig. 2
def spectra():
    """The horizontal-pair spectra with the L19 external conversions (x100 L18, 26 Nov, sim2arm/EPC_L19.md); the vertical
    cosmic rows of panel (a) are not in that table and come from pass 4 (cosmics do not depend on the γ-ray run)."""
    with open(SIM / "two_arm_spectra_pass4li11_l19.csv") as f:
        rows = list(csv.DictReader(f))
    with open(SIM / "two_arm_spectra_pass4li11.csv") as f:
        rows += [x for x in csv.DictReader(f) if x["pair"] == "vert"]
    return rows


def hist(rows, ep, pair, ewin, comp, rebin=2):
    r = sorted((x for x in rows if float(x["Ep_keV"]) == ep and x["pair"] == pair and x["ewin"] == ewin and x["comp"] == comp),
               key=lambda x: float(x["th_lo"]))
    y = np.array([float(x["rate_per_day"]) for x in r])
    n = np.array([float(x["n_mc"]) for x in r])
    return y.reshape(-1, rebin).sum(1), n.reshape(-1, rebin).sum(1)


def fig_predictions():
    S = spectra()
    with open(SIM / "cosmic_theta.csv") as f:
        C = [x for x in csv.DictReader(f) if x["sample"] == "L15 disk"]
    e5 = np.arange(0, 181, 5.0)
    e10 = np.arange(0, 181, 10.0)
    fig, axs = plt.subplots(1, 3, figsize=(W, 1.75))
    fig.subplots_adjust(left=0.062, right=0.985, bottom=0.205, top=0.875, wspace=0.27)

    # (a) cosmic nights: two-arm coincidences against the reconstructed opening angle
    ax = axs[0]
    allv = np.array([float(x["per_day"]) for x in C if x["pair"] == "vert"])
    allh = np.array([float(x["per_day"]) for x in C if x["pair"] == "horiz"])
    vv, _ = hist(S, 1100.0, "vert", "none", "cos", 1)
    vw, _ = hist(S, 1100.0, "vert", "win", "cos", 1)
    ax.axvspan(125, 160, color=GRID, alpha=0.6, lw=0, zorder=0)
    ax.stairs(allv, e5, color=INK, lw=1.3, label=f"all two-arm pairs ({round(allv.sum(), -3):.0f} per day)")
    ax.stairs(vv, e5, color=ORANGE, lw=1.3, label=f"+ pointing, time of flight ({round(vv.sum(), -1):.0f})")
    ax.stairs(vw, e5, color=BLUE, lw=1.3, label=rf"+ $E_\mathrm{{sum}}$ window ({round(vw.sum(), -1):.0f})")
    ax.set_yscale("log")
    ax.set_ylim(0.8, 6e6)
    ax.set_yticks([1, 1e2, 1e4, 1e6])
    ax.set_xlim(60, 180)
    ax.set_xticks([60, 90, 120, 150, 180])
    ax.set_xlabel(r"opening angle $\theta$ (deg)")
    ax.set_ylabel(r"cosmic-ray pairs per day per 5$^\circ$")
    ax.legend(frameon=False, loc="upper left", handlelength=1.3, borderaxespad=0.1, labelspacing=0.25, fontsize=6.5)
    tag(ax, "(a) cosmic rays, arms vertical")
    strip(ax)
    print(f"(a) vertical all {allv.sum():.0f}/d, pointing+TOF {vv.sum():.0f}, +Esum {vw.sum():.0f}; horizontal all {allh.sum():.0f}")

    # (b), (c) selected pairs, horizontal arms: 441 keV for one day, 1.10 MeV for five days
    def stack(ax, ep, days, title, sig_scale):
        h = {c: hist(S, ep, "horiz", "win", c)[0] * days for c in ("M1", "E1", "g1", "epc", "cos", "sig")}
        # external conversions: since L19 (352 simulated events in the window) drawn with their own shape after the cut
        ipc = h["M1"] + h["E1"] + h["g1"]
        parts = [("cosmic rays", h["cos"], "#b9b8b2"), ("external conversions", h["epc"], YELLOW),
                 ("IPC, E1 and 15 MeV lines", h["E1"] + h["g1"], AQUA), ("IPC, M1", h["M1"], BLUE)]
        base = np.zeros_like(ipc)
        for lab, y, c in parts:
            ax.stairs(base + y, e10, baseline=base, fill=True, color=c, alpha=0.85, lw=0, label=lab)
            ax.stairs(base + y, e10, baseline=base, color="white", lw=0.5)
            base = base + y
        ctr = 0.5 * (e10[:-1] + e10[1:])
        ok = base > 0
        ax.errorbar(ctr[ok], base[ok], yerr=np.sqrt(base[ok]), fmt="o", ms=2.2, color=INK, lw=0.7, capsize=0,
                    label="total, stat. error")
        if sig_scale:
            ax.stairs(h["sig"] * sig_scale, e10, color="#d63a2f", lw=1.3,
                      label=rf"X17 at {sig_scale:.2f}$\,R_\mathrm{{ATOMKI}}$")
        ax.set_xlim(90, 180)
        ax.set_xticks([90, 120, 150, 180])
        ax.set_ylim(0, (base + np.sqrt(base)).max() * (1.8 if sig_scale else 1.42))
        ax.set_xlabel(r"opening angle $\theta$ (deg)")
        ax.set_ylabel(r"selected pairs per 10$^\circ$")
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1], frameon=False, loc="upper left", handlelength=1.3, borderaxespad=0.1,
                  labelspacing=0.25)
        tag(ax, title)
        strip(ax)
        print(f"{title}: IPC {ipc.sum():.0f} (M1 {h['M1'].sum():.0f}, E1 {h['E1'].sum():.0f}, 15 MeV {h['g1'].sum():.0f}), EPC {h['epc'].sum():.0f}, cosmics {h['cos'].sum():.0f}, "
              f"X17 {h['sig'].sum():.1f} in {days} d")

    stack(axs[1], 441.0, H441 / 24, r"(b) $E_p$ = 441 keV (H$_2^+$), 1 beam day", 0)
    d_fix = float(next(r for r in reach_rows() if r["target"].startswith("Cu") and r["energy_stack"] == "+ liquid working")["d2_c"])
    r_lim = E.r90(d_fix, REQ_DAYS) / E.R_ATOMKI
    stack(axs[2], 1100.0, REQ_DAYS, rf"(c) $E_p$ = 1.10 MeV, {REQ_BD:.1f} beam days", r_lim)
    fig.savefig(FIG / "fig_predictions.pdf")
    fig.savefig(FIG / "fig_predictions.png", dpi=200)
    plt.close(fig)


# ---------------------------------------------------------------------------------------------------------- Fig. 2 (new)
def fig_acceptance():
    """Geometric pair acceptance against the opening angle (proposal/figsrc/acceptance.py, 26 Nov): (a) isotropic pairs
    flat in theta, one lepton per arm or both in one arm; (b) the M1 internal pairs of the 441 keV day reaching the TPCs."""
    with open(SIM / "acceptance_geom.csv") as f:
        A = list(csv.DictReader(f))
    with open(SIM / "acceptance_ipc441.csv") as f:
        B = list(csv.DictReader(f))
    ea = np.r_[[float(r["th_lo"]) for r in A], float(A[-1]["th_hi"])]
    eb = np.r_[[float(r["th_lo"]) for r in B], float(B[-1]["th_hi"])]
    fig, axs = plt.subplots(1, 2, figsize=(W, 1.6))
    fig.subplots_adjust(left=0.065, right=0.985, bottom=0.23, top=0.86, wspace=0.22)
    ax = axs[0]
    ax.axvspan(125, 160, color="#d63a2f", alpha=0.08, lw=0, zorder=0)
    for x_ in (125, 160):
        ax.axvline(x_, color="#d63a2f", lw=0.5, alpha=0.45, ls=(0, (3, 2)), zorder=0.6)
    ax.text(142.5, 26.8, "X17\nregion", ha="center", va="top", fontsize=6.5, color="#a8322a")
    ax.stairs([100 * float(r["acc_same"]) for r in A], ea, color=ORANGE, lw=1.4, label="both leptons in one arm")
    ax.stairs([100 * float(r["acc_opposite"]) for r in A], ea, color=BLUE, lw=1.4, label="one lepton in each arm")
    ax.set_xlim(0, 180)
    ax.set_ylim(0, 28)
    ax.set_xticks([0, 30, 60, 90, 120, 150, 180])
    ax.set_xlabel(r"opening angle $\theta$ (deg)")
    ax.set_ylabel("pair acceptance (%)")
    ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.43, 1.0), handlelength=1.3, borderaxespad=0.1, labelspacing=0.25)
    tag(ax, "(a) isotropic pairs, flat in opening angle")
    strip(ax)
    bx = axs[1]
    k = E.BEAM_DAY_H / 8.0                     # the table is per 8 h of beam; the figure shows one beam day (19.2 h)
    tot = np.array([float(r["emitted_per_8h"]) for r in B]) * k
    sm = np.array([float(r["same_per_8h"]) for r in B]) * k
    op = np.array([float(r["opposite_per_8h"]) for r in B]) * k
    bx.axvspan(125, 160, color="#d63a2f", alpha=0.08, lw=0, zorder=0)
    bx.axvline(125, color="#d63a2f", lw=0.5, alpha=0.45, ls=(0, (3, 2)), zorder=0.6)
    bx.axvline(160, color="#d63a2f", lw=0.5, alpha=0.45, ls=(0, (3, 2)), zorder=0.6)
    bx.text(142.5, 1.4e2, "X17\nregion", ha="center", va="bottom", fontsize=6.5, color="#a8322a")
    bx.stairs(tot, eb, color="#b9b8b2", fill=True, alpha=0.6, lw=0, label="emitted ({0}$\\times10^{{{1}}}$)".format(*f"{tot.sum():.1e}".split("e+0")))
    bx.stairs(sm, eb, color=ORANGE, lw=1.4, label=f"in one arm ({round(sm.sum(), -4):,.0f})")
    bx.stairs(op, eb, color=BLUE, lw=1.4, label=f"one in each arm ({round(op.sum(), -3):,.0f})")
    bx.set_yscale("log")
    bx.set_ylim(100, 8e6)
    bx.set_xlim(0, 180)
    bx.set_xticks([0, 30, 60, 90, 120, 150, 180])
    bx.set_xlabel(r"opening angle $\theta$ (deg)")
    bx.set_ylabel(r"pairs per 5$^\circ$")
    lg = bx.legend(frameon=True, fancybox=True, framealpha=0.8, facecolor="white", edgecolor="none", loc="upper right",
                   bbox_to_anchor=(1.0, 1.0), handlelength=1.3, borderaxespad=0.0, borderpad=0.15, labelspacing=0.2,
                   handletextpad=0.5)  # 27 Nov: tight white box over the X17 band, pushed into the top-right corner
    lg.get_frame().set_boxstyle("round", pad=0.0, rounding_size=0.3)
    tag(bx, r"(b) M1 internal pairs, $E_p$ = 441 keV, 1 beam day, 1 µA")
    strip(bx)
    print(f"Fig 2: IPC 441 emitted {tot.sum():.3g}, one arm {sm.sum():.0f}, each arm {op.sum():.0f} per beam day (geometry)")
    fig.savefig(FIG / "fig_acceptance.pdf")
    fig.savefig(FIG / "fig_acceptance.png", dpi=200)
    plt.close(fig)


# ---------------------------------------------------------------------------------------------------------- Fig. 3
def reach_rows():
    with open(ROOT / "planning" / "out" / "two_arm_reach.csv") as f:
        return [r for r in csv.DictReader(f) if r["geometry"] == "horizontal pair" and "TOF" in r["veto"]
                and r["film"].startswith("11")]


def fig_reach():
    rows = reach_rows()
    cu = {r["energy_stack"]: r for r in rows if r["target"].startswith("Cu")}
    al = {r["energy_stack"]: r for r in rows if r["target"].startswith("Al")}
    k_fix, k_ntof, k_off = "+ liquid working", "+ liquid as at n_TOF", "SiPM wall + small plastics (no liquid)"
    al_sim = al[k_fix]["source"].startswith("Geant4")       # since R10 (2026-11-25) the lighter holder's rows are simulated
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(W, 1.9), gridspec_kw=dict(width_ratios=[1.0, 1.0]))
    fig.subplots_adjust(left=0.062, right=0.985, bottom=0.19, top=0.885, wspace=0.62)

    # (a) expected 90 % CL limit against the days at 1.10 MeV, in units of R_ATOMKI
    days = np.linspace(0.5, 10, 96)
    U = E.R_ATOMKI
    for key, col, lab in ((k_off, MUTED, "no liquid cells"), (k_ntof, ORANGE, "liquid cells as at n_TOF"),
                          (k_fix, BLUE, "liquid cells, design response")):
        r = cu[key]
        lo, c, hi = float(r["d2_lo"]), float(r["d2_c"]), float(r["d2_hi"])
        ax.fill_between(days, [E.r90(hi, d) / U for d in days], [E.r90(lo, d) / U for d in days], color=col, alpha=0.15, lw=0)
        ax.plot(days, [E.r90(c, d) / U for d in days], color=col, lw=1.5, label=lab)
    r = al[k_fix]
    ax.plot(days, [E.r90(float(r["d2_c"]), d) / U for d in days], color=AQUA, lw=1.5, ls=(0, (4, 2)),
            label="lighter Al holder" + ("" if al_sim else " (estimate)"))
    ax.axhline(1.0, color=INK, lw=0.8)
    ax.text(9.9, 1.04, r"ATOMKI, $R = 5.8\times10^{-6}$", ha="right", va="bottom", fontsize=7)
    ax.axhline(E.R_MEG2_90 / U, color=INK, lw=0.8, ls=":")
    ax.text(9.9, E.R_MEG2_90 / U * 1.04, "MEG II, 90 % CL", ha="right", va="bottom", fontsize=7,
            bbox=dict(fc="white", ec="none", pad=0.4, alpha=0.8))
    ax.axvline(REQ_DAYS, color=GRID, lw=0.8, zorder=0)
    ax.text(REQ_DAYS + 0.12, 0.345, "requested", fontsize=7, color=MUTED, va="bottom")
    ax.set_yscale("log")
    ax.set_ylim(0.33, 30)       # 26 Nov: headroom for the legend above the L19 curves
    ax.set_yticks([0.5, 1, 2, 5, 10, 20])
    ax.get_yaxis().set_major_formatter(matplotlib.ticker.FormatStrFormatter("%g"))
    ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.set_xlim(0.5, 10)
    ax.set_xlabel(r"days of beam (24 h) at $E_p$ = 1.10 MeV, 1 µA")
    ax.set_ylabel(r"expected 90 % CL limit on $R$ / $R_\mathrm{ATOMKI}$")
    ax.legend(frameon=False, loc="upper right", handlelength=1.8, borderaxespad=0.0, labelspacing=0.25, ncol=1)
    tag(ax, "(a) this run: two arms, existing Cu holder")
    strip(ax)

    # (b) days to a 3 sigma test of R_ATOMKI, from this run to the full experiment (11 um Li, liquid cells working)
    d_cu = (float(cu[k_fix]["d2_c"]), float(cu[k_fix]["d2_lo"]), float(cu[k_fix]["d2_hi"]))
    d_al2 = (float(al[k_fix]["d2_c"]), float(al[k_fix]["d2_lo"]), float(al[k_fix]["d2_hi"]))
    d_al4 = (float(al[k_fix]["d4_c"]), float(al[k_fix]["d4_lo"]), float(al[k_fix]["d4_hi"]))
    # Large plastics: FEASIBILITY_SIM section 19.3, four arms, Al ogive + Cu liner, calibrated: 0.4 (0.35-0.5) d, made with
    # the 20 um film, a 0.3 ns time of flight and the L4 cosmics.  Scaled by this holder's four-arm days here (11 um,
    # 0.6 ns, L15 cosmics) over its section 19.3 four-arm days (4.5 d): a scaling estimate, drawn as an open circle.
    film = d_al4[0] / E.FOUR_ARM[("Al ogive + Cu liner (lighter)", "fix")][0]
    d_big = tuple(v * film for v in (0.4, 0.35, 0.5))
    bars = [("this run: two arms,\nexisting Cu holder", d_cu, BLUE, False),
            ("two arms,\nlighter Al holder", d_al2, AQUA, not al_sim),
            ("four arms,\nlighter Al holder", d_al4, AQUA, not al_sim),
            ("four arms, lighter holder,\nlarge plastic scintillators", d_big, AQUA, True)]
    for i, (lab, (c, lo, hi), col, est) in enumerate(bars):
        y = len(bars) - 1 - i
        bx.plot([lo, hi], [y, y], color=col, lw=2.2, solid_capstyle="butt", zorder=3)
        bx.plot([c], [y], "o", ms=6, mfc="white" if est else col, mec=col, mew=1.4, zorder=4)
        txt = f"{c:.0f} days" if c >= 2 else f"{c:.1f} days"
        bx.text(hi * 1.35, y, txt, ha="left", va="center", fontsize=7.5)
        print(f"(b) {lab!r}: {c:.2f} ({lo:.2f}-{hi:.2f}) d{' (estimate)' if est else ''}")
    bx.set_yticks(range(len(bars))[::-1])
    bx.set_yticklabels([b[0] for b in bars], fontsize=7.5, linespacing=1.1)
    bx.tick_params(axis="y", length=0)
    bx.set_xscale("log")
    bx.set_xlim(0.1, 1000)
    bx.set_ylim(-1.05, len(bars) - 0.45)
    bx.set_xticks([0.1, 1, 10, 100, 1000])
    bx.get_xaxis().set_major_formatter(matplotlib.ticker.FormatStrFormatter("%g"))
    bx.set_xlabel(r"days of beam to a 3$\sigma$ test of $R_\mathrm{ATOMKI}$, 1 µA")
    bx.plot([], [], "o", ms=6, mfc=INK, mec=INK, mew=1.4, label="Geant4")
    bx.plot([], [], "o", ms=6, mfc="white", mec=INK, mew=1.4, label="scaled from Geant4 (estimate)")
    bx.grid(axis="x", color=GRID, lw=0.5, zorder=0)
    bx.set_axisbelow(True)
    bx.legend(frameon=False, loc="lower right", handlelength=1.4, borderaxespad=0.0, labelspacing=0.25, fontsize=6.5)
    tag(bx, "(b) from this run to the full experiment", x=-0.62)
    strip(bx)
    fig.savefig(FIG / "fig_reach.pdf")
    fig.savefig(FIG / "fig_reach.png", dpi=200)
    plt.close(fig)


# ---------------------------------------------------------------------------------------------------------- Fig. 4 (new)
def road_steps():
    """The road from this run to the physics run (11 um Li, liquid cells at their design response, MM pointing + TOF):
    days of beam to a 3 sigma test of R_ATOMKI, each step adding one change. Same inputs as the old Fig. 3 (b)."""
    rows = reach_rows()
    k = "+ liquid working"
    cu = next(r for r in rows if r["target"].startswith("Cu") and r["energy_stack"] == k)
    al = next(r for r in rows if r["target"].startswith("Al") and r["energy_stack"] == k)
    t = lambda r, n: (float(r[f"{n}_c"]), float(r[f"{n}_lo"]), float(r[f"{n}_hi"]))
    d_al4 = t(al, "d4")
    film = d_al4[0] / E.FOUR_ARM[("Al ogive + Cu liner (lighter)", "fix")][0]   # see fig_reach: a scaling estimate
    al_sim = al["source"].startswith("Geant4")
    return [("this run", "this run: two arms, Cu holder", t(cu, "d2"), BLUE, False),
            ("+ lighter holder", "two arms, Al holder", t(al, "d2"), AQUA, not al_sim),
            ("+ four arms", "four arms, Al holder", d_al4, GREEN, not al_sim),
            ("+ large plastics", "four arms, Al holder, large plastics", tuple(v * film for v in (0.4, 0.35, 0.5)),
             VIOLET, True)]


def fig_road():
    """Days are BEAM DAYS (19.2 h of beam, E.OPER_EFF); the fits' days of 24 h are converted with E.beam_days."""
    steps = road_steps()
    U = E.R_ATOMKI
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(W, 1.8), gridspec_kw=dict(width_ratios=[1.0, 1.0]))
    fig.subplots_adjust(left=0.075, right=0.985, bottom=0.2, top=0.88, wspace=0.62)

    # (a) expected 90 % CL limit against the beam days at 1.10 MeV, one line per step (linear days, Dylan 26 Nov)
    XMAX = 30
    days = np.linspace(0.25, XMAX, 240)              # beam days
    for name, _, (c, lo, hi), col, est in steps:
        ax.fill_between(days, [E.r90(hi, d * BD) / U for d in days], [E.r90(lo, d * BD) / U for d in days], color=col,
                        alpha=0.15, lw=0)
        ax.plot(days, [E.r90(c, d * BD) / U for d in days], color=col, lw=1.5, ls=(0, (4, 2)) if est else "-",
                label=name + (" (estimate)" if est else ""))
    ax.axhline(1.0, color=INK, lw=0.8)
    ax.text(XMAX * 0.98, 0.93, "ATOMKI", ha="right", va="top", fontsize=7)
    ax.axhline(E.R_MEG2_90 / U, color=INK, lw=0.8, ls=":")
    ax.text(XMAX * 0.98, E.R_MEG2_90 / U * 1.06, "MEG II, 90 % CL", ha="right", va="bottom", fontsize=7)
    c0 = steps[0][2][0]
    y0 = E.r90(c0, REQ_DAYS) / U
    ax.plot([REQ_BD], [y0], "o", ms=4.5, mfc="white", mec=BLUE, mew=1.2, zorder=5)
    ax.annotate(f"this run, {REQ_BD:.1f} beam days", (REQ_BD, y0), xytext=(REQ_BD + 3.0, y0 * 2.2), fontsize=7,
                color=INK, va="center", arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.5, shrinkA=1, shrinkB=3))
    ax.set_yscale("log")
    ax.set_xlim(0, XMAX)
    ax.set_ylim(0.01, 20)
    ax.set_xticks([0, 5, 10, 15, 20, 25, 30])
    ax.set_yticks([0.01, 0.03, 0.1, 0.3, 1, 3, 10])
    ax.yaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter("%g"))
    ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.set_xlabel(r"beam days at $E_p$ = 1.10 MeV, 1 µA")
    ax.set_ylabel(r"90 % CL limit / $R_\mathrm{ATOMKI}$")
    ax.legend(frameon=False, loc="lower center", ncol=2, handlelength=1.8, borderaxespad=0.1, labelspacing=0.2,
              columnspacing=1.0, fontsize=6.5)
    tag(ax, "(a) expected limit, one change at a time")
    strip(ax)

    # (b) beam days to a 3 sigma test of R_ATOMKI for each step
    for i, (name, lab, d24, col, est) in enumerate(steps):
        c, lo, hi = (E.beam_days(v) for v in d24)
        y = len(steps) - 1 - i
        bx.plot([lo, hi], [y, y], color=col, lw=2.2, solid_capstyle="butt", zorder=3)
        bx.plot([c], [y], "o", ms=6, mfc="white" if est else col, mec=col, mew=1.4, zorder=4)
        bx.text(hi * 1.35, y, f"{c:.0f} days" if c >= 2 else f"{c:.1f} days", ha="left", va="center", fontsize=7.5)
        note = ("measures the inputs below", "tests: holder scattering, conversions", "tests: acceptance, cosmic rejection",
                "not tested in this run")[i]
        bx.text(-0.04, y - 0.3, note, transform=bx.get_yaxis_transform(), ha="right", va="center", fontsize=6.3,
                color=MUTED, style="italic")
        if i:   # arrow from the previous step's point down to this one, between the two rows
            cp = E.beam_days(steps[i - 1][2][0])
            bx.annotate("", xy=(c, y + 0.16), xytext=(cp, y + 0.84),
                        arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.6, mutation_scale=6, shrinkA=0, shrinkB=0))
        print(f"road {name}: {c:.2f} ({lo:.2f}-{hi:.2f}) beam days; beats MEG II after "
              f"{E.beam_days(E_days(d24[0], E.R_MEG2_90)):.1f} beam days, excludes ATOMKI after "
              f"{E.beam_days(E_days(d24[0], U)):.1f}{' (estimate)' if est else ''}")
    bx.set_yticks(range(len(steps))[::-1])
    bx.set_yticklabels([s_[1] for s_ in steps], fontsize=7.5, linespacing=1.1, va='bottom')
    bx.tick_params(axis="y", length=0, pad=4)
    bx.set_xscale("log")
    bx.set_xlim(0.3, 3000)
    bx.set_ylim(-0.65, len(steps) - 0.45)
    bx.set_xticks([1, 10, 100, 1000])
    bx.get_xaxis().set_major_formatter(matplotlib.ticker.FormatStrFormatter("%g"))
    bx.set_xlabel(r"beam days to a 3$\sigma$ test of $R_\mathrm{ATOMKI}$, 1 µA")
    bx.grid(axis="x", color=GRID, lw=0.5, zorder=0)
    bx.set_axisbelow(True)
    tag(bx, "(b) from this run to the physics run", x=-0.62)
    strip(bx)
    fig.savefig(FIG / "fig_road.pdf")
    fig.savefig(FIG / "fig_road.png", dpi=200)
    plt.close(fig)


def E_days(d3, r_target):
    """Days of beam for the expected 90 % CL limit to reach r_target (E.r90 scales as 1/sqrt(days))."""
    ref = 1.0
    return ref * (E.r90(d3, ref) / r_target) ** 2


def photos():
    """Fig. 1a, 1b: the n_TOF photo (cropped to 3:4, 1100 px wide) and the run-145 fans (make_ntof_fans.py)."""
    try:
        from PIL import Image, ImageOps
    except ImportError:
        print("no PIL: fig1a not rebuilt")
        return
    src = HERE / "ntof_ear2_topdown.jpg"
    if src.exists():
        im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
        w, h = im.size
        box = (int(0.06 * w), int(0.10 * h), int(0.98 * w), int(0.10 * h) + int(0.92 * w * 4 / 3 * 0.86))
        im = im.crop(box)
        im.thumbnail((1100, 1600))
        im.save(FIG / "fig1a_ntof_photo.jpg", quality=88)
        print("fig1a", im.size)
    fans = HERE / "ntof_fans.png"
    if fans.exists():
        Image.open(fans).save(FIG / "fig1b_ntof_fans.png")


if __name__ == "__main__":
    import matplotlib.ticker  # noqa: F401
    FIG.mkdir(parents=True, exist_ok=True)
    what = sys.argv[1:] or ["event", "acc", "pred", "road", "photos"]
    if "event" in what:
        fig_event()
    if "acc" in what:
        fig_acceptance()
    if "pred" in what:
        fig_predictions()
    if "reach" in what:
        fig_reach()
    if "road" in what:
        fig_road()
    if "photos" in what:
        photos()
    print("figures in", FIG)
