#!/usr/bin/env python3
"""compare_gases.py -- the non-flammable gases with some hydrocarbon quencher, compared directly (GAS_STUDY.md §11).

Dylan, 26 Nov: leave out the flammable and the low-quencher gases and compare the mixtures with some isobutane,
methane or ethane, with the water around 0.5-1 %. Two figures, both against the drift voltage (mesh at ground):
  figures/compare_band.png      v and D_T for every gas. The line is 0.75 % water and the band spans 0.5-1.0 % water,
                                at the middle gap. One panel per quencher family.
  figures/compare_by_water.png  v and D_T at 0.25, 0.5, 0.75 and 1.0 % water, every gas overlaid, with the gap band.
Reads gas/out/tables through analyze.py; the voltage window and the gaps come from voltage_plots.py.
"""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import voltage_plots as VP
import analyze as A
from mixtures import BASES, flammability

FAMS = [('Ar/CO₂/iC₄H₁₀', ['ArCO2Iso_96.5_2_1.5', 'ArCO2Iso_95.5_3_1.5', 'ArCO2Iso_94_4_2', 'ArCO2Iso_93_5_2',
                          'ArCO2Iso_90_8_2', 'ArCO2Iso_88_10_2']),
        ('Ar/CH₄/CO₂ and Ar/CO₂/C₂H₆', ['ArCH4CO2_94_4_2', 'ArCH4CO2_93_5_2', 'ArCH4CO2_91_5_4',
                                       'ArCO2Eth_93_5_2', 'ArCO2Eth_92_4_4'])]
# within a family: light to dark = less to more quencher. Iso in blues, methane in oranges, ethane in purples.
COL = {'ArCO2Iso_96.5_2_1.5': '#9cc3f2', 'ArCO2Iso_95.5_3_1.5': '#6aa6ec', 'ArCO2Iso_94_4_2': '#3a85e0',
       'ArCO2Iso_93_5_2': '#1c64c4', 'ArCO2Iso_90_8_2': '#134895', 'ArCO2Iso_88_10_2': '#0b2e5e',
       'ArCH4CO2_94_4_2': '#f5b971', 'ArCH4CO2_93_5_2': '#e8873a', 'ArCH4CO2_91_5_4': '#b35a14',
       'ArCO2Eth_93_5_2': '#a48be6', 'ArCO2Eth_92_4_4': '#5f3dc4'}
STYLE = {b: ('-' if 'Iso' in b else '--' if 'CH4' in b else '-.') for b in COL}
BAND_W = (0.5, 1.0)
MID_W = 0.75
QTY = [('v', 1.0, 'drift velocity v (µm/ns)'), ('dT', 1e4, 'transverse diffusion D_T (µm/√cm)')]


def table(C, b, w):
    """the curves at water w; linear interpolation in water between the two nearest simulated fractions."""
    k = f'{b}__w{w:g}'
    if k in C:
        return C[k], False
    ws = sorted(C[x]['_w'] for x in C if C[x]['_b'] == b)
    lo = max(x for x in ws if x < w); hi = min(x for x in ws if x > w)
    f = (w - lo) / (hi - lo)
    a, c = C[f'{b}__w{lo:g}'], C[f'{b}__w{hi:g}']
    return {q: (1 - f) * a[q] + f * c[q] if q in ('v', 'dT', 'dL') else a[q] for q in a}, True


def lbl(b):
    return VP.label(b)


def main():
    C = VP.load_curves()
    gases = {b for _, gs in FAMS for b in gs if f'{b}__w0' in C}
    for b in gases:
        assert flammability(BASES[b][0])[2], b
    V = VP.V
    # ---- figure 1: band = 0.5-1.0 % water, line = 0.75 %
    fig, axs = plt.subplots(2, 2, figsize=(14, 9), sharex=True)
    for col, (fam, gs) in enumerate(FAMS):
        for row, (q, fac, ylab) in enumerate(QTY):
            ax = axs[row, col]; A.style(ax); VP.window(ax)
            for b in gs:
                if b not in gases:
                    continue
                lo = VP.at_V(table(C, b, BAND_W[0])[0], q, VP.GAP_MID_CM) * fac
                hi = VP.at_V(table(C, b, BAND_W[1])[0], q, VP.GAP_MID_CM) * fac
                mid_t, interp = table(C, b, MID_W)
                mid = VP.at_V(mid_t, q, VP.GAP_MID_CM) * fac
                ax.fill_between(V, np.fmin(lo, hi), np.fmax(lo, hi), color=COL[b], alpha=0.18, lw=0)
                ax.plot(V, mid, color=COL[b], lw=1.8, ls=STYLE[b], label=lbl(b) + (' (0.75 % interp.)' if interp else ''))
            ax.set_xlim(V[0], V[-1])
            if row == 0:
                ax.set_title(fam, fontsize=11, loc='left')
                ax.legend(fontsize=7.5, frameon=False, loc='upper left', ncol=2)
            else:
                ax.set_xlabel('drift voltage (V), mesh at ground', fontsize=9)
            if col == 0:
                ax.set_ylabel(ylab, fontsize=9)
    for row in range(2):
        lo_ = min(axs[row, 0].get_ylim()[0], axs[row, 1].get_ylim()[0]); hi_ = max(axs[row, 0].get_ylim()[1], axs[row, 1].get_ylim()[1])
        for col in range(2):
            axs[row, col].set_ylim(lo_, hi_)
    fig.suptitle(f'Non-flammable gases with isobutane, methane or ethane. Line: 0.75 % water; band: 0.5–1.0 % water. '
                 f'{VP.GAP_MID_CM*10:.1f} mm gap. {VP.WINDOW_TEXT}', fontsize=10, x=0.01, ha='left')
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(os.path.join(A.FIG, 'compare_band.png'), dpi=120); plt.close(fig)

    # ---- figure 2: one column per water fraction, every gas overlaid, band = gap range
    WS = [0.25, 0.5, 0.75, 1.0]
    fig, axs = plt.subplots(2, 4, figsize=(17, 8.5), sharex=True, sharey='row')
    for j, w in enumerate(WS):
        for row, (q, fac, ylab) in enumerate(QTY):
            ax = axs[row, j]; A.style(ax); VP.window(ax)
            for _, gs in FAMS:
                for b in gs:
                    if b not in gases:
                        continue
                    t, interp = table(C, b, w)
                    lo, mid, hi = (VP.at_V(t, q, g) * fac for g in (VP.GAP_MIN_CM, VP.GAP_MID_CM, VP.GAP_MAX_CM))
                    ax.fill_between(V, np.fmin(lo, hi), np.fmax(lo, hi), color=COL[b], alpha=0.15, lw=0)
                    ax.plot(V, mid, color=COL[b], lw=1.5, ls=STYLE[b], label=lbl(b))
            ax.set_xlim(V[0], V[-1])
            if row == 0:
                ax.set_title(f'{w:g} % water', fontsize=11, loc='left')
            else:
                ax.set_xlabel('drift voltage (V)', fontsize=9)
            if j == 0:
                ax.set_ylabel(ylab, fontsize=9)
    h, l = axs[0, 0].get_legend_handles_labels()
    fig.legend(h, l, fontsize=8, frameon=False, ncol=6, loc='upper left', bbox_to_anchor=(0.01, 0.955))
    fig.suptitle(f'The same gases at four water fractions. Line: {VP.GAP_MID_CM*10:.1f} mm gap; band: '
                 f'{VP.GAP_MIN_CM*10:.1f}–{VP.GAP_MAX_CM*10:.1f} mm. {VP.WINDOW_TEXT}', fontsize=10, x=0.01, ha='left')
    fig.tight_layout(rect=(0, 0, 1, 0.9))
    fig.savefig(os.path.join(A.FIG, 'compare_by_water.png'), dpi=120); plt.close(fig)
    print('wrote figures/compare_band.png, compare_by_water.png;', len(gases), 'gases')


if __name__ == '__main__':
    main()
