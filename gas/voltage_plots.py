#!/usr/bin/env python3
"""voltage_plots.py -- drift velocity and transverse diffusion against the DRIFT VOLTAGE (GAS_STUDY.md §10).

The mesh is at ground, so E = V_drift / gap. Our chambers have different gaps, so one drift voltage gives a range of
fields. Each curve is drawn at the middle gap and the band spans the smallest to the largest gap of our chambers.
One colour per water fraction. Reads gas/out/tables/*.json through analyze.py; writes
gas/figures/v_vs_Vdrift.png, DT_vs_Vdrift.png, stability_vs_Vdrift.png and gas/out/vdrift_table.csv.
Only non-flammable gases without fluorine and with >= 3 % quencher are shown (MIN_QUENCH; Dylan 26 Nov).
System python3 (numpy, matplotlib).
"""
import os, sys, csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analyze as A                                    # noqa: E402  (load, curves, label, style)
from mixtures import BASES, flammability, PRESSURE_TORR  # noqa: E402

# Drift gaps (mm), nTof_x17 rerun/calib/physics_inputs.json and PAPER1_NUMBERS_2026-10-31.md (DET4GAP, det3 topography):
# det2 (B) 31.12 +- 0.42 (Y view 31.1-31.5), det3 (A) 28.08 +- 0.19, det4 (E) 28.6 +- 0.5 geometric (input 30.48),
# det6 (C/D) 28.0 adopted, det7 29.44 +- 1.12. Band: 28.0 mm (det3, det6) to 31.3 mm (det2).
GAP_MIN_CM, GAP_MAX_CM = 2.80, 3.13
GAP_MID_CM = 0.5 * (GAP_MIN_CM + GAP_MAX_CM)
V_SAFE, V_HARD = 700.0, 800.0
# the most a drift cathode has held in our logs (gas/hv_history/HV_HISTORY.md); the plots run to V_MAX
V_HELD = 1200.0   # A on the bench 26 Jun (4 h, Ar/iC4H10 95/5) and A, C, D at n_TOF run 3 (1.9 h, Ar/CO2 70/30)
V_LO, V_MAX = 400.0, 1200.0
V = np.linspace(V_LO, V_MAX, 161)
WINDOW_TEXT = 'Green: ≤ 700 V (design); orange: to 800 V; purple: to 1200 V (held in our logs).'

# the CERN store premixes (Dylan's scrape ~/PycharmProjects/Misc/cern_catalogue_scraper/cern_gases.csv, 2026-09-29):
# SCEM, m3 per bottle, CHF, lead time (working days). None = not a store item (custom order).
STORE = {
    'ArIso_98_2': ('61.02.05.020.3', 5.45, 288, 30), 'ArCH4_95_5': ('61.02.05.018.7', 7.5, 197, 30),
    'ArCO2_97_3': ('61.00.05.004.5 (97.5/2.5, 10 L)', 2.1, 225, 2), 'ArIso_95_5': ('61.02.05.027.6', 2.15, 263, 30),
    'ArCH4CO2_93_5_2': ('61.00.05.001.2', 10.0, 582, 25), 'ArCF4Iso_95_3_2': ('61.02.05.029.4', 2.5, 302, 16),
    'ArCO2Iso_93_5_2': ('61.03.05.309.8', 5.5, 547, 35), 'ArCO2_93_7': ('61.01.05.016.5', 7.5, 169, 30),
    'ArIso_90_10': ('61.01.05.013.8', 1.05, 169, 30), 'ArCH4_90_10': ('61.01.05.007.6', 7.5, 169, 30),
    'ArCO2_90_10': ('61.02.05.009.8', 7.5, 302, 16), 'ArCO2Iso_86_10_4': ('61.03.05.003.8', 2.35, 346, 30),
    'ArCF4Iso_88_10_2': ('61.01.05.035.2', 7.2, 263, 11),
}
# Dylan, 26 Nov: show only the non-flammable gases without fluorine, with at least 3 % quencher (all but argon).
MIN_QUENCH = 3.0


def quench(b):
    return 100.0 - dict(BASES[b][0])['ar']


GASES = sorted([b for b in BASES if 'CF4' not in b and flammability(BASES[b][0])[2] and quench(b) >= MIN_QUENCH - 1e-9],
               key=lambda b: (quench(b), b))
FAMILY_GROUPS = [('Ar/CO₂/iC₄H₁₀', 'ArCO2Iso'), ('Ar/CH₄ (+CO₂) and Ar/CO₂/C₂H₆', ('ArCH4', 'ArCO2Eth')),
                 ('Ar/CO₂ (no hydrocarbon)', 'ArCO2_')]
WATER = [0.0, 0.1, 0.25, 0.375, 0.5, 0.75, 1.0, 1.5]
WCOL = dict(zip(WATER, ['#0b2e5e', '#123f86', '#1b5bb3', '#2a78d6', '#4f95e3', '#7fb3ee', '#f08a3c', '#d1495b']))
BANDS_W = [(0.1, 0.5), (0.5, 1.0)]   # the water we hope for, and the water as at n_TOF (GAS_STUDY.md §1)


def label(b):
    return A.label(b).replace('C4H10', 'C₄H₁₀').replace('CH4', 'CH₄').replace('CO2', 'CO₂').replace('CF4', 'CF₄').replace('C2H6', 'C₂H₆')


def tag(b):
    ok = flammability(BASES[b][0])[2]
    s = STORE.get(b)
    return ('non-flammable' if ok else 'FLAMMABLE') + (f' · CERN store, {s[3]} wd' if s else ' · custom order')


def at_V(c, key, gap):
    """quantity at drift voltage V for one gap, from the smoothed table (log-log interpolation in E)."""
    E = V / gap
    y = np.exp(np.interp(np.log(E), np.log(c['E']), np.log(c[key])))
    y[(E < c['E'][0]) | (E > c['E'][-1])] = np.nan
    return y


def window(ax):
    ax.axvspan(V[0], V_SAFE, color='#eaf5ea', zorder=0)
    ax.axvspan(V_SAFE, V_HARD, color='#fdf3e1', zorder=0)
    ax.axvline(V_SAFE, color='#7cb77c', lw=1); ax.axvline(V_HARD, color='#e0a64b', lw=1, ls='--')
    if V_HELD:
        ax.axvspan(V_HARD, V_HELD, color='#f1ecfa', zorder=0)
        ax.axvline(V_HELD, color='#9a7fd6', lw=1, ls=':')


def load_curves():
    """every table without O2 and at 20 C, resampled to 600 V/cm (the Magboltz grid's top)."""
    C = {}
    for k, d in A.load().items():
        if d.get('o2_ppm', 0) or 'T' in k.split('__')[1]:
            continue
        c = A.curves(d, e_max=600.0); c['_b'], c['_w'] = d['base'], d['water_pct']; C[k] = c
    return C


def main():
    C = load_curves()
    gases = [g for g in GASES if f'{g}__w0' in C]
    missing = [g for g in GASES if f'{g}__w0' not in C]
    if missing:
        print('no tables yet for', missing)
    rows = []
    for qty, fac, ylab, fname in (('v', 1.0, 'drift velocity v (µm/ns)', 'v_vs_Vdrift'),
                                  ('dT', 1e4, 'transverse diffusion D_T (µm/√cm)', 'DT_vs_Vdrift')):
        ncol = 4; nrow = (len(gases) + ncol - 1) // ncol
        fig, axs = plt.subplots(nrow, ncol, figsize=(14, 2.75 * nrow), sharex=True, sharey=True)
        for ax, b in zip(axs.flat, gases):
            A.style(ax); window(ax)
            for w in WATER:
                c = C.get(f'{b}__w{w:g}')
                if c is None:
                    continue
                lo, mid, hi = (at_V(c, qty, g) * fac for g in (GAP_MIN_CM, GAP_MID_CM, GAP_MAX_CM))
                ax.fill_between(V, np.fmin(lo, hi), np.fmax(lo, hi), color=WCOL[w], alpha=0.16, lw=0)
                ax.plot(V, mid, color=WCOL[w], lw=1.3, label=f'{w:g} %')
                if qty == 'v':
                    for vv in (500, 600, 700, 800, 900, 1000, 1100, 1200):
                        j = int(np.argmin(abs(V - vv)))
                        rows.append(dict(gas=b, water_pct=w, V_drift=vv, v_lo=round(float(min(lo[j], hi[j])), 2),
                                         v_mid=round(float(mid[j]), 2), v_hi=round(float(max(lo[j], hi[j])), 2),
                                         dT_mid_um=round(float(at_V(c, 'dT', GAP_MID_CM)[j] * 1e4))))
            ax.set_title(f'{label(b)}\n{tag(b)}', fontsize=8.5, color='#222', loc='left')
            ax.set_xlim(V[0], V[-1])
        for ax in list(axs.flat)[len(gases):]:
            ax.axis('off')
        h, l = axs.flat[0].get_legend_handles_labels()
        fig.legend(h, l, title='water', fontsize=8, title_fontsize=8, frameon=False, ncol=len(l),
                   loc='upper right', bbox_to_anchor=(0.995, 0.968))
        for ax in axs[-1]:
            ax.set_xlabel('drift voltage (V), mesh at ground', fontsize=8)
        for ax in axs[:, 0]:
            ax.set_ylabel(ylab, fontsize=8)
        fig.suptitle(f'{ylab} against drift voltage, {PRESSURE_TORR:.0f} Torr, 20 °C (Magboltz). Line: {GAP_MID_CM*10:.1f} mm '
                     f'gap; band: {GAP_MIN_CM*10:.1f} mm (A, det6) to {GAP_MAX_CM*10:.1f} mm (B). '
                     + WINDOW_TEXT,
                     fontsize=10, x=0.01, ha='left')
        fig.tight_layout(rect=(0, 0, 1, 0.955))
        fig.savefig(os.path.join(A.FIG, fname + '.png'), dpi=120); plt.close(fig)

    # stability: the spread of v over a water band, at each drift voltage. Each chamber has its own fixed gap, which
    # we calibrate, so the gap is not an instability: the line is the middle gap, the band the gap range.
    fig, axs = plt.subplots(2, 3, figsize=(15, 8.6), sharex=True, sharey=True)
    groups = [(t, [g for g in gases if g.startswith(p)]) for t, p in FAMILY_GROUPS]
    PAL = {'ArCO2Iso': ['#9cc3f2', '#5b9ee8', '#2a78d6', '#1b5bb3', '#123f86', '#0b2e5e'],
           'ArCH4': ['#f5c98f', '#eda15a', '#d9782d', '#a85314'], 'ArCO2Eth': ['#a48be6', '#5f3dc4'],
           'ArCO2_': ['#8fd1b9', '#3fae8a', '#1a7f5e', '#0b4f3a']}
    fam_cols = {}
    for fam, pal in PAL.items():
        for i, g in enumerate([g for g in gases if g.startswith(fam)]):
            fam_cols[g] = pal[min(i, len(pal) - 1)]

    def spread(b, gap, band):
        ws_all = [w for w in WATER if f'{b}__w{w:g}' in C]
        arr = np.array([at_V(C[f'{b}__w{w:g}'], 'v', gap) for w in ws_all])
        vs = np.array([[np.interp(w, ws_all, arr[:, j]) for j in range(len(V))] for w in np.linspace(*band, 9)])
        return (vs.max(0) - vs.min(0)) / vs.mean(0) * 100

    for r, band in enumerate(BANDS_W):
        for c_, (title, gs) in enumerate(groups):
            ax = axs[r, c_]; A.style(ax); window(ax)
            for b in gs:
                n_in = sum(1 for w in WATER if f'{b}__w{w:g}' in C and band[0] <= w <= band[1])
                s_lo, s_mid, s_hi = (spread(b, g, band) for g in (GAP_MIN_CM, GAP_MID_CM, GAP_MAX_CM))
                ax.fill_between(V, np.fmin(s_lo, s_hi), np.fmax(s_lo, s_hi), color=fam_cols[b], alpha=0.15, lw=0)
                ax.plot(V, s_mid, color=fam_cols[b], lw=1.6, label=label(b) + ('' if n_in >= 3 else ' *'))
            ax.set_xlim(V[0], V[-1]); ax.set_ylim(0, 60)
            if r == 0:
                ax.set_title(title, fontsize=10, loc='left'); ax.legend(fontsize=7, frameon=False, loc='lower left')
            else:
                ax.set_xlabel('drift voltage (V)', fontsize=9)
            if c_ == 0:
                ax.set_ylabel(f'spread of v over {band[0]:g}–{band[1]:g} % H₂O (%)', fontsize=9)
    fig.suptitle(f'How much the drift velocity changes when the water moves within a band (top: 0.1–0.5 %, bottom: '
                 f'0.5–1.0 %), at each drift voltage. (v_max − v_min)/v_mean; lower is steadier.\nLine: '
                 f'{GAP_MID_CM*10:.1f} mm gap; band: {GAP_MIN_CM*10:.1f}–{GAP_MAX_CM*10:.1f} mm. {WINDOW_TEXT} '
                 '(* fewer than 3 water points simulated inside the band)', fontsize=10, x=0.01, ha='left')
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(os.path.join(A.FIG, 'stability_vs_Vdrift.png'), dpi=120); plt.close(fig)

    with open(os.path.join(A.OUT, 'vdrift_table.csv'), 'w', newline='') as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0])); wr.writeheader(); wr.writerows(rows)
    print('wrote figures/v_vs_Vdrift.png, DT_vs_Vdrift.png, stability_vs_Vdrift.png, out/vdrift_table.csv')


if __name__ == '__main__':
    main()
