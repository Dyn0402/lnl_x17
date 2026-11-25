#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_ntof_fans.py -- the "two opposing fans" picture of real 2026 n_TOF data,
re-drawn at its final print size for the LNL proposal.

This is the LEFT panel only of nTof_x17's `run145_overhead_AC.png`
(`mpgd26/make_run145_pointing.py`, `figure_overhead()`).  The overhead view
shows the tracks of the two opposing Micromegas arms A and C.  Each track is
drawn from where it crossed the strip plane back to its closest approach to
the beam axis.  The two fans cross at the 3He capsule.

Nothing is re-implemented here.  The tracks, the selection, the in-situ angle
scale and the drawing of the fans come from the nTof_x17 code, imported
(`arm_tracks`, `k_insitu`, `_fan`, `_stage`, `_x_at_target`, `P.DET_COLOR`).
Only the stale input paths of that module are repointed, by setting module
attributes, and the panel is laid out at 2.1 in x 2.1 in with 7 pt labels.

Data: run_145 (started 2026-08-05, 3He target, production configuration),
sub-runs stat090_0000 and stat090_0001, n_TOF partner run 224670.
Selection: a track fitted in both the x and the y strip plane, |tan| < 1 in
both, whose extrapolation lands on a SiPM wall segment AND a plastic bar that
both have an in-time hit (`run145_target_imaging.pointing_coincidence`).

Usage (nTof_x17 venv):
    ~/PycharmProjects/nTof_x17/.venv/bin/python make_ntof_fans.py
"""
from __future__ import annotations

import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------ locations
NTOF_REPO = os.environ.get(
    'NTOF_X17_REPO', os.path.expanduser('~/PycharmProjects/nTof_x17'))
X17_DATA = os.environ.get('X17_DATA', '/media/dylan/data/x17')

# Where the inputs are now (2026-11-25).  The paths hard-coded in
# make_run145_pointing.py are stale.
RUNS = os.path.join(X17_DATA, 'beam_july', 'runs')
SLIM = os.path.join(RUNS, 'run_145', '{sub}', 'ntof_hits',
                    'ntof_hits_run_145_{sub}_224670.root')
RUN_CFG = os.path.join(RUNS, 'run_145', 'run_config.json')
# Track tables (events_prelim.parquet) of the 2026-09-07 full pass, and the
# imaging summaries (k_phys per arm) made from the same tables.
ANALYSIS_BASE = os.path.join(X17_DATA, 'sept26_prelim', 'fullpass')
IMAGING = os.path.join(X17_DATA, 'sept26_prelim', 'kcal',
                       'run_145_{sub}', 'imaging_summary.json')

for p in (NTOF_REPO, os.path.join(NTOF_REPO, 'mpgd26')):
    if p not in sys.path:
        sys.path.insert(0, p)

import matplotlib                                                  # noqa: E402
matplotlib.use('Agg')
import matplotlib.pyplot as plt                                    # noqa: E402

import plotstyle as P                                              # noqa: E402
import make_run145_pointing as M                                   # noqa: E402
from ntof_tracking import run145_target_imaging as TI              # noqa: E402

M.SLIM = SLIM
M.RUN_CFG = RUN_CFG
M.IMAGING = IMAGING
TI.ANALYSIS_BASE = ANALYSIS_BASE

# --------------------------------------------------------------------- layout
FIG_IN = 2.1                 # final print size [in], square
DPI = 600
HALF = 255.0                 # the view is +-HALF mm in both directions
FS = 7.0                     # every label, in points at the final size
INK = P.INK


def check_inputs():
    """Stop with the list of missing inputs before any drawing is done."""
    need = [RUN_CFG]
    for sub in M.SUBRUNS:
        need += [SLIM.format(sub=sub), IMAGING.format(sub=sub)]
        for arm in ('A', 'C'):
            base = os.path.join(ANALYSIS_BASE, M.RUN, sub, f'mx17_{arm}',
                                'events_prelim')
            need += [base + '.parquet', base + '.meta.json']
    missing = [p for p in need if not os.path.exists(p)]
    if missing:
        sys.exit('missing inputs:\n  ' + '\n  '.join(missing))


def main():
    check_inputs()
    P.use()

    K = M.k_insitu()
    arms = {a: M.arm_tracks(a, coincidence=True, k=K.get(a, 1.0))
            for a in ('A', 'C')}
    col = {a: P.DET_COLOR[a] for a in arms}

    fig = plt.figure(figsize=(FIG_IN, FIG_IN), facecolor='white')
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
    ax.set_xlim(-HALF, HALF)
    ax.set_ylim(-HALF, HALF)
    ax.set_aspect('equal')
    ax.set_facecolor('white')
    ax.axis('off')

    # The capsule and the two strip planes, then the two fans.  The original
    # panel is ~6.2 in wide and this one is 2.1 in wide, so the line widths
    # are scaled by ~1/3 to keep the same picture.
    M._stage(ax, arms)
    for patch in ax.patches:
        patch.set_linewidth(0.4)
    ax.patches[-1].set_linewidth(0.9)          # the capsule circle, drawn last
    for a, d in arms.items():
        M._fan(ax, d, col[a], 0.12, 0.030)
    for c in ax.collections:
        c.set_rasterized(True)

    # arm names, next to their strip planes
    for a in arms:
        cz = arms[a]['center'][2]
        ax.text(np.sign(cz) * 220.0, 247.0, f'arm {a}',
                ha='right' if cz > 0 else 'left', va='top',
                fontsize=FS, fontweight='bold', color=col[a], zorder=10)

    # the target, with a leader to the circle
    ax.annotate(r'target ($^{3}$He capsule)', xy=(0.0, M.CAPSULE_R),
                xytext=(0.0, 118.0), fontsize=FS, color=INK,
                ha='center', va='bottom', zorder=10,
                arrowprops=dict(arrowstyle='-', color=INK, lw=0.5,
                                shrinkA=1.5, shrinkB=1.5))

    # scale bar
    x0, y0 = -222.0, -241.0
    ax.plot([x0, x0 + 100.0], [y0, y0], color=INK, lw=1.0, zorder=10,
            solid_capstyle='butt')
    ax.text(x0 + 50.0, y0 + 6.0, '100 mm', ha='center', va='bottom',
            fontsize=FS, color=INK, zorder=10)

    out = os.path.join(HERE, 'ntof_fans.png')
    # plotstyle sets savefig.bbox = 'tight', which pads the figure.  The full
    # figure box with no padding keeps the image at exactly FIG_IN x FIG_IN.
    fig.savefig(out, dpi=DPI, facecolor='white', bbox_inches=fig.bbox_inches,
                pad_inches=0.0)
    plt.close(fig)

    # ---------------------------------------------------------------- report
    print(f'-> {out}   {FIG_IN} in x {FIG_IN} in at {DPI} dpi')
    print(f'run {M.RUN}, sub-runs {", ".join(M.SUBRUNS)}')
    print(f'in-situ angle scale k = {K}')
    n_tot = 0
    for a, d in arms.items():
        i = d['info']
        n_tot += i['n_coincident']
        x = M._x_at_target(d)
        core = x[np.abs(x) < 90]
        print(f"arm {a}: events {i['n_events']:,}  x&y fitted {i['n_2plane']:,}"
              f"  |tan|<1 {i['n_sel']:,}  with wall hit {i['n_wall']:,}"
              f"  predictable {i['n_predictable']:,}"
              f"  coincident (drawn) {i['n_coincident']:,}")
        print(f"       back-projected X at the target plane: median "
              f"{np.median(core):+.1f} mm (|X| < 90 mm), "
              f"{100 * np.mean(np.abs(x) < M.CAPSULE_R):.1f} % inside the "
              f"{M.CAPSULE_R:.0f} mm bore;  d_perp {d['d_perp']:.1f} mm, "
              f"foot_x {d['foot_x']:+.1f} mm")
    print(f'total drawn: {n_tot:,}')


if __name__ == '__main__':
    main()
