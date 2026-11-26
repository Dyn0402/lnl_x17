#!/usr/bin/env python3
"""analyze.py -- the LNL gas study: metrics, ranking and figures from the Magboltz tables (GAS_STUDY.md §3-6).

Reads gas/out/tables/*.json (gas/magboltz/drift_one.py) and gas/out/heed_primaries.json.
Writes gas/out/metrics.csv, gas/out/ranking.csv, gas/out/summary.json and gas/figures/*.png.
System python3 (numpy, matplotlib).
"""
import os, sys, json, glob, csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'magboltz'))
from mixtures import BASES, WATER_PCT, flammability, PRESSURE_TORR, TEMP_K, T_CHECK as T_CHECK_BASES  # noqa: E402

OUT = os.path.join(HERE, 'out')
FIG = os.path.join(HERE, 'figures')
os.makedirs(FIG, exist_ok=True)

# ---- the operating window (GAS_STUDY.md §1) ---------------------------------------------------------------
# Drift gaps from nTof_x17 rerun/PAPER1_NUMBERS_2026-10-31.md (DET4GAP row): det3 (A) 28.0-28.2 mm, det2 (B)
# 31.1-31.5 mm. Mesh at ground, so the drift field is V_drift / gap. n_TOF: A sparked at 800 V (run_51, 17 Jul
# 2026) and ran 550-600 V, then all four ran 700 V in production (runs 77-162).
GAP_CM = {'A': 2.81, 'B': 3.13}
V_SAFE, V_HARD = 700.0, 800.0
E_LO = 100.0                                            # below this every gas is slow and steep; not considered
E_SAFE = min(V_SAFE / g for g in GAP_CM.values())      # 224 V/cm, set by B
E_HARD = min(V_HARD / g for g in GAP_CM.values())      # 256 V/cm
W_DESIGN = 0.5                                         # % water we design for (n_TOF/SPS had ~1.5 %)
DT_K, DP_HPA, DW_PCT = 1.0, 10.0, 0.1                  # assumed run-to-run swings: hall T, weather p, water drift
L_CM = 3.0
# slowest acceptable drift: B's 31.3 mm in 32 samples x 60 ns = 1.92 us (n_TOF production read 20 samples)
V_MIN = 16.5
FAMILY = {'ArIso': 'Ar/iC4H10', 'ArCO2Iso': 'Ar/CO2/iC4H10', 'ArCO2': 'Ar/CO2', 'ArCH4': 'Ar/CH4 (+CO2)',
          'ArCH4CO2': 'Ar/CH4 (+CO2)', 'ArCF4Iso': 'Ar/CF4/iC4H10 (reference)'}
FAM_COLOR = {'Ar/iC4H10': '#257de0', 'Ar/CO2/iC4H10': '#f47230', 'Ar/CO2': '#00b894',
             'Ar/CH4 (+CO2)': '#f2a600', 'Ar/CF4/iC4H10 (reference)': '#ee7fac'}
WATER_COLOR = {0.0: '#0e3d7e', 0.25: '#1b64be', 0.5: '#338ced', 1.0: '#84b9f3', 1.5: '#b6d5f8'}


def family(b):
    return FAMILY[b.split('_')[0]]


def label(b):
    head, *nums = b.split('_')
    return FAMILY[head].replace(' (reference)', '').replace(' (+CO2)', '+CO2' if head == 'ArCH4CO2' else '') \
        + ' ' + '/'.join(nums)


def load():
    T = {}
    for f in glob.glob(os.path.join(OUT, 'tables', '*.json')):
        d = json.load(open(f))
        T[d['key']] = d
    return T


def curves(d, smooth=True):
    """E, v, dT, dL, eta from the table nodes, resampled on a fine log grid with a smoothing fit in ln E."""
    n = d['nodes']
    E = np.array([p['E_Vcm'] for p in n])
    lnE = np.log(E)
    Ef = np.logspace(np.log10(60), np.log10(450), 200)
    out = dict(E=Ef)
    for k, key in (('v', 'v_um_per_ns'), ('dT', 'dT_sqrtcm'), ('dL', 'dL_sqrtcm')):
        y = np.log(np.array([p[key] for p in n]))
        # local quadratic (5-node window) in ln E: smooths ~0.3 % Magboltz noise before differentiating
        fit = np.array([np.polyval(np.polyfit(lnE[max(0, i - 2):i + 3], y[max(0, i - 2):i + 3], 2), lnE[i])
                        for i in range(len(E))]) if smooth else y
        out[k] = np.exp(np.interp(np.log(Ef), lnE, fit))
    out['eta'] = np.interp(np.log(Ef), lnE, np.array([p['eta_per_cm'] for p in n]))
    out['S'] = np.gradient(np.log(out['v']), np.log(Ef))        # dln v / dln E
    return out


def at(c, k, e):
    return float(np.interp(e, c['E'], c[k]))


BANDS = {'dry': (0.0, 0.1), 'target': (0.1, 0.5), 'ntof': (0.5, 1.0)}   # % water: aim, realistic, as at n_TOF/SPS
KEY6 = ['ArCO2Iso_93_5_2', 'ArIso_95_5', 'ArIso_98.2_1.8', 'ArCH4_96_4', 'ArCH4CO2_94_4_2', 'ArCO2_97_3']
CAT6 = ['#257de0', '#f47230', '#00b894', '#f2a600', '#ee7fac', '#008a17']


def waters(C, b):
    return sorted(C[k]['_w'] for k in C if C[k]['_b'] == b)


def vgrid(C, b):
    """W (n_w), E (n_E), lnv (n_w, n_E), dT, eta at each water."""
    ws = waters(C, b)
    cs = [C[f'{b}__w{w:g}'] for w in ws]
    return np.array(ws), cs[0]['E'], np.log(np.array([c['v'] for c in cs])), np.array([c['dT'] for c in cs]), cs


def v_at_w(W, lnv, w):
    """ln v at water w, linear interpolation in w at each field."""
    return np.array([np.interp(w, W, lnv[:, j]) for j in range(lnv.shape[1])])


def band_spread(W, E, lnv, lo, hi):
    """(max - min) / mean of v over the water band, at each field; 11 water steps."""
    vs = np.exp(np.array([v_at_w(W, lnv, w) for w in np.linspace(lo, hi, 11)]))
    return (vs.max(0) - vs.min(0)) / vs.mean(0), vs.min(0), vs.max(0)


def main():
    T = load()
    heed = json.load(open(os.path.join(OUT, 'heed_primaries.json')))
    C = {}
    for k, d in T.items():
        if d.get('o2_ppm', 0) or 'T' in d:
            continue
        c = curves(d); c['_b'] = d['base']; c['_w'] = d['water_pct']; C[k] = c
    rank, rows = [], []
    for b in BASES:
        if f'{b}__w0' not in C:
            print('missing', b); continue
        W, E, lnv, dT, cs = vgrid(C, b)
        l, r, nonflam = flammability(BASES[b][0])
        peaks = {f'{w:g}': round(float(E[np.argmax(lnv[i])]), 0) for i, w in enumerate(W)}
        rec = dict(base=b, label=label(b), family=family(b), role=BASES[b][1], non_flammable=nonflam,
                   flam_margin=round(r - l, 1), n_water=len(W), E_peak=peaks,
                   v_peak_dry=round(float(np.exp(lnv[0].max())), 1),
                   clusters_per_cm=round(heed[b]['clusters_per_cm'], 1))
        for name, (lo, hi) in BANDS.items():
            for lim, emax in (('700', E_SAFE), ('800', E_HARD)):
                sp, vmin, vmax = band_spread(W, E, lnv, lo, hi)
                m = (E >= E_LO) & (E <= emax) & (vmin >= V_MIN)
                if m.any():
                    j = np.flatnonzero(m)[np.argmin(sp[m])]
                else:                                   # never fast enough: take the top of the window
                    j = int(np.flatnonzero(E <= emax)[-1])
                wm = 0.5 * (lo + hi)
                lnv_m = v_at_w(W, lnv, wm)
                S = float(np.gradient(lnv_m, np.log(E))[j])
                dw = 0.02
                dlnv_dw = float((v_at_w(W, lnv, min(wm + dw, W[-1]))[j] - v_at_w(W, lnv, max(wm - dw, 0))[j])
                                / (min(wm + dw, W[-1]) - max(wm - dw, 0)))
                dTm = float(np.exp(np.interp(wm, W, np.log(dT[:, j]))))
                dLm = float(np.interp(wm, W, [c['dL'][j] for c in cs]))
                rec[f'{name}_{lim}'] = dict(
                    E=round(float(E[j]), 0), V_B=round(float(E[j]) * GAP_CM['B']),
                    spread_pct=round(100 * float(sp[j]), 1), v_min=round(float(vmin[j]), 1), v_max=round(float(vmax[j]), 1),
                    S=round(S, 3), pct_per_K=round(100 * S / TEMP_K, 3), pct_per_0p1w=round(10 * dlnv_dw, 2),
                    DT_um=round(dTm * 1e4), DL_um=round(dLm * 1e4), t_max_ns=round(GAP_CM['B'] * 1e4 / float(vmin[j])))
        o2 = T.get(f'{b}__w0.5_o200')
        if o2:
            co = curves(o2); e = rec['target_700']['E']
            rec['surv_3cm_w0.5_o200'] = round(float(np.exp(-max(at(co, 'eta', e), 0) * L_CM)), 3)
            rec['surv_3cm_w0.5'] = round(float(np.exp(-max(at(C[f'{b}__w0.5'], 'eta', e), 0) * L_CM)), 3)
        rank.append(rec)
        for i, w in enumerate(W):
            for e in (150, 200, 224, 256):
                rows.append(dict(base=b, water_pct=w, E_Vcm=e, v=round(float(np.exp(np.interp(e, E, lnv[i]))), 2),
                                 DT_um=round(float(np.interp(e, E, dT[i])) * 1e4)))
    rank.sort(key=lambda r: (not r['non_flammable'], r['target_700']['spread_pct']))
    with open(os.path.join(OUT, 'metrics.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    flat = []
    for r in rank:
        d = {k: v for k, v in r.items() if not isinstance(v, dict)}
        for band in BANDS:
            for lim in ('700', '800'):
                for k, v in r[f'{band}_{lim}'].items():
                    d[f'{band}_{lim}_{k}'] = v
        flat.append(d)
    with open(os.path.join(OUT, 'ranking.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(flat[0])); w.writeheader(); w.writerows(flat)
    tcheck = {}
    for b in T_CHECK_BASES:
        k3, k2 = f'{b}__w0_T303', f'{b}__w0'
        if k3 in T and k2 in T:
            c3, c2 = curves(T[k3]), curves(T[k2])
            tcheck[b] = {str(e): dict(v303=round(at(c3, 'v', e), 2), v293_at_E_x_303_293=round(at(c2, 'v', e * 303.15 / TEMP_K), 2))
                         for e in (150, 200, 250)}
    json.dump(dict(E_SAFE=E_SAFE, E_HARD=E_HARD, E_A_700=V_SAFE / GAP_CM['A'], bands=BANDS, ranking=rank, tcheck=tcheck),
              open(os.path.join(OUT, 'summary.json'), 'w'), indent=1)
    figures(C, rank)
    for r in rank:
        t, d, n = r['target_700'], r['dry_700'], r['ntof_700']
        print(f"{r['label']:24s} {'ok ' if r['non_flammable'] else 'FLM'} pk(w0/.25/.5/1)={[r['E_peak'].get(k) for k in ('0','0.25','0.5','1')]} "
              f"| dry E{d['E']:.0f} sp{d['spread_pct']:5.1f}% | target E{t['E']:.0f} sp{t['spread_pct']:5.1f}% v{t['v_min']}-{t['v_max']} "
              f"DT{t['DT_um']} {t['pct_per_0p1w']}%/0.1w | ntof E{n['E']:.0f} sp{n['spread_pct']:5.1f}% | 800V target sp{r['target_800']['spread_pct']}% "
              f"| surv {r.get('surv_3cm_w0.5_o200')}")
    print('T check', json.dumps(tcheck))


def style(ax):
    ax.grid(True, color='#e6e6e6', lw=0.6); ax.set_axisbelow(True)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    for s in ('left', 'bottom'):
        ax.spines[s].set_color('#9c9c9c')
    ax.tick_params(colors='#555', labelsize=8)


def window(ax):
    ax.axvspan(E_LO, E_SAFE, color='#e9f2fd', zorder=0)
    ax.axvspan(E_SAFE, E_HARD, color='#f6f6f6', zorder=0)
    ax.axvline(E_SAFE, color='#9dc8f7', lw=1); ax.axvline(E_HARD, color='#c8c8c8', lw=1, ls='--')


RAMP = ['#0e3d7e', '#1757ac', '#2370cd', '#338ced', '#6aabf1', '#9dc8f7', '#b6d5f8', '#cce3fd']


def figures(C, rank):
    bases = [r['base'] for r in rank]
    for qty, ylab, fname, fac in (('v', 'drift velocity (µm/ns)', 'v_vs_E', 1.0),
                                  ('dT', 'transverse diffusion D_T (µm/√cm)', 'DT_vs_E', 1e4)):
        n = len(bases); ncol = 4; nrow = (n + ncol - 1) // ncol
        fig, axs = plt.subplots(nrow, ncol, figsize=(13, 2.5 * nrow), sharex=True, sharey=True)
        for ax, b in zip(axs.flat, bases):
            style(ax); window(ax)
            ws = waters(C, b)
            for i, w in enumerate(ws):
                c = C[f'{b}__w{w:g}']
                ax.plot(c['E'], c[qty] * fac, color=RAMP[min(i, 7)], lw=1.4, label=f'{w:g} % H₂O')
            r = next(x for x in rank if x['base'] == b)
            ax.set_title(r['label'] + ('' if r['non_flammable'] else '  (flammable)'), fontsize=9, color='#222')
            ax.set_xscale('log'); ax.set_xlim(60, 450)
            ax.set_xticks([60, 100, 150, 224, 300, 450]); ax.set_xticklabels(['60', '100', '150', '224', '300', '450'])
            ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
            if len(ws) == 8 and b == bases[0]:
                ax.legend(fontsize=6.5, frameon=False, loc='lower right' if qty == 'v' else 'upper right', ncol=2)
        for ax in list(axs.flat)[n:]:
            ax.axis('off')
        for ax in axs[-1]:
            ax.set_xlabel('drift field (V/cm)', fontsize=8)
        for ax in axs[:, 0]:
            ax.set_ylabel(ylab, fontsize=8)
        fig.suptitle(f'{ylab} at {PRESSURE_TORR:.0f} Torr, 20 °C, dark = dry to light = 1.5 % water. Blue band: drift ≤ 700 V on B '
                     f'(≤ {E_SAFE:.0f} V/cm); grey: ≤ 800 V (≤ {E_HARD:.0f} V/cm)', fontsize=10, x=0.01, ha='left')
        fig.tight_layout(rect=(0, 0, 1, 0.97))
        fig.savefig(os.path.join(FIG, fname + '.png'), dpi=120); plt.close(fig)
    # the velocity peak against water, six key gases
    fig, ax = plt.subplots(figsize=(7.5, 4.6)); style(ax)
    ax.axhspan(E_LO, E_SAFE, color='#e9f2fd', zorder=0); ax.axhspan(E_SAFE, E_HARD, color='#f6f6f6', zorder=0)
    for b, col in zip(KEY6, CAT6):
        r = next((x for x in rank if x['base'] == b), None)
        if r is None: continue
        ws = sorted(float(k) for k in r['E_peak']); ep = [r['E_peak'][f'{w:g}'] for w in ws]
        ax.plot(ws, ep, color=col, lw=2, marker='o', ms=5, mec='white', mew=1.5, label=r['label'])
    ax.set_yscale('log'); ax.set_ylim(60, 470)
    ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.axhline(450, color='#9c9c9c', lw=0.8, ls=':')
    ax.text(0.0, 452, 'at the top: the peak is above 450 V/cm', fontsize=7, color='#666', va='bottom')
    ax.set_yticks([60, 100, 150, 224, 256, 300, 450]); ax.set_yticklabels(['60', '100', '150', '224', '256', '300', '450'])
    ax.set_xlabel('water in the gas (%)', fontsize=9); ax.set_ylabel('field of the drift-velocity peak (V/cm)', fontsize=9)
    ax.set_title('Water moves the velocity peak up. Blue: reachable with 700 V on B; grey: with 800 V', fontsize=10, loc='left')
    ax.legend(fontsize=8, frameon=False, loc='lower right')
    fig.tight_layout(); fig.savefig(os.path.join(FIG, 'peak_vs_water.png'), dpi=140); plt.close(fig)
    # v against water at each gas's best field for the target band
    fig, ax = plt.subplots(figsize=(7.5, 4.6)); style(ax)
    ax.axvspan(*BANDS['target'], color='#e9f2fd', zorder=0)
    for b, col in zip(KEY6, CAT6):
        r = next((x for x in rank if x['base'] == b), None)
        if r is None: continue
        W, E, lnv, dT, cs = vgrid(C, b)
        e = r['target_700']['E']; j = int(np.argmin(abs(E - e)))
        wf = np.linspace(0, 1.5, 61)
        ax.plot(wf, np.exp([np.interp(w, W, lnv[:, j]) for w in wf]), color=col, lw=2,
                label=f"{r['label']} at {e:.0f} V/cm")
        ax.plot(W, np.exp(lnv[:, j]), 'o', color=col, ms=4, mec='white', mew=1)
    ax.set_xlabel('water in the gas (%)', fontsize=9); ax.set_ylabel('drift velocity (µm/ns)', fontsize=9)
    ax.set_title('Drift velocity against water, each gas at its best field ≤ 224 V/cm for 0.1–0.5 % water (band)',
                 fontsize=10, loc='left')
    ax.legend(fontsize=7.5, frameon=False, loc='upper right')
    fig.tight_layout(); fig.savefig(os.path.join(FIG, 'v_vs_water.png'), dpi=140); plt.close(fig)
    # trade-off
    fig, ax = plt.subplots(figsize=(8.5, 5.5)); style(ax)
    fams = []
    for r in rank:
        f = r['family']; t = r['target_700']
        ax.scatter(t['spread_pct'], t['DT_um'], s=60, color=FAM_COLOR[f], edgecolor='white', lw=2, zorder=3,
                   marker='o' if r['non_flammable'] else 'X', label=f if f not in fams else None)
        fams.append(f)
        ax.annotate(r['label'].split(' ')[-1], (t['spread_pct'], t['DT_um']), xytext=(5, 3),
                    textcoords='offset points', fontsize=7, color='#333')
    ax.set_xscale('log')
    ax.set_xlabel('spread of the drift velocity over 0.1–0.5 % water, at the best field ≤ 224 V/cm (%)', fontsize=9)
    ax.set_ylabel('transverse diffusion D_T there, at 0.3 % water (µm/√cm)', fontsize=9)
    ax.set_title('Each candidate at its best field (× = flammable). Lower left is better.', fontsize=10, loc='left')
    ax.legend(fontsize=8, frameon=False, loc='upper right')
    fig.tight_layout(); fig.savefig(os.path.join(FIG, 'tradeoff.png'), dpi=140); plt.close(fig)


if __name__ == '__main__':
    main()
