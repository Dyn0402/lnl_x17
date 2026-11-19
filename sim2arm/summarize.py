#!/usr/bin/env python3
"""
summarize.py -- tables and figures from the two-arm reach and spectra (two_arm_nd.py) for TWO_ARM_STUDY.md.

    python3 sim2arm/summarize.py [--tag _pass3]

Inputs:  sim2arm/out/two_arm_reach<tag>.csv (or two_arm_nd<tag>.csv), two_arm_spectra<tag>.csv
Outputs: sim2arm/out/summary_reach<tag>.csv, summary_rates<tag>.csv, figures/*.png

Conversions (as planning/two_arm_estimates.py): Z after T days at R(ATOMKI) = 3 sqrt(T / d3); the expected 90 % CL
upper limit with no signal R90 = 1.2816 / Z(T) x R(ATOMKI) (background-dominated, Z linear in R).
Central value: geometric mean of the two MC-safe estimators (direct tables with the one-event floor, transplant);
range: the two of them.  Both are what FEASIBILITY_SIM §19.2 uses.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / 'out'
FIG = OUT / 'figures'
R_ATOMKI, R_MEG2_90, Z90 = 5.8e-6, 1.2e-5, 1.2816
PAIR_LABEL = {'vert': 'vertical pair (top + bottom)', 'horiz': 'horizontal pair (left + right)',
              'adj': 'adjacent pair (side + top)', 'adj_lo': 'adjacent pair (side + bottom)', 'all': 'four arms'}
RESP_LABEL = {'LNL calibrated': 'liquid working', 'n_TOF as is': 'liquid as at n_TOF',
              'LNL calibrated, LS off': 'no liquid'}
LEVEL_LABEL = {'trigger': 'no cosmic veto', 'MM 15°': 'MM pointing 15°', 'MM 15° point, μ 3°': 'MM pointing (μ 3°)',
               'MM 15° point, μ 3° + TOF 1 ns': 'pointing + 1 ns TOF', 'MM 15° + TOF': 'MM 15° + 0.6 ns TOF (ref.)',
               'MM 3°': 'MM 3° segments'}
COL = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4']      # dataviz reference categorical order


def z_at(d3, T):
    return 3.0 * np.sqrt(T / d3)


def reach(df, T=5.0):
    rows = []
    for (p, r, lv), g in df.groupby(['pair', 'resp', 'level'], sort=False):
        dd = g.set_index('mc')['days_floor1'].to_dict()
        vals = [v for v in dd.values() if np.isfinite(v) and v > 0]
        if not vals:
            continue
        c = float(np.exp(np.mean(np.log(vals))))
        gi = g.iloc[0]
        rows.append(dict(pair=p, resp=r, level=lv, days3_direct=dd.get('direct', np.nan),
                         days3_transplant=dd.get('transplant', np.nan), days3=c, days3_lo=min(vals), days3_hi=max(vals),
                         **{f'Z_{T:g}d': z_at(c, T)}, **{f'R90_{T:g}d_over_ATOMKI': Z90 / z_at(c, T)},
                         **{f'R90_{T:g}d_over_MEGII': Z90 / z_at(c, T) * R_ATOMKI / R_MEG2_90},
                         S_win=gi.get('S_win'), Bbeam_win=gi.get('Bbeam_win'), Bcos_win=gi.get('Bcos_win'),
                         n_mc_cos_win=gi.get('n_mc_cos_win'), S_fit=gi.get('S_fit'), Bbeam_fit=gi.get('Bbeam_fit'),
                         Bcos_fit=gi.get('Bcos_fit'), n_mc_cos_fit=gi.get('n_mc_cos_fit'), ecut=gi.get('ecut')))
    return pd.DataFrame(rows)


def rates(sp):
    """per pair / E_p / level / E window: rates per day in angle bands, per component."""
    bands = [(0, 25), (25, 90), (90, 125), (125, 160), (160, 180.1)]
    rows = []
    for key, g in sp.groupby(['pair', 'resp', 'level', 'Ep_keV', 'ewin'], sort=False):
        for c, gc in g.groupby('comp'):
            r = dict(zip(['pair', 'resp', 'level', 'Ep_keV', 'ewin'], key), comp=c)
            for lo, hi in bands:
                m = (gc['th_lo'] >= lo) & (gc['th_hi'] <= hi)
                r[f'{lo:g}-{min(hi, 180):g}'] = gc.loc[m, 'rate_per_day'].sum()
                r[f'nmc_{lo:g}-{min(hi, 180):g}'] = int(gc.loc[m, 'n_mc'].sum())
            r['all'] = gc['rate_per_day'].sum()
            rows.append(r)
    return pd.DataFrame(rows)


def fig_days(rs, tag):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    lv = 'MM 15° + TOF'
    pairs = [p for p in ('all', 'vert', 'horiz', 'adj') if p in set(rs['pair'])]
    resps = [r for r in RESP_LABEL if r in set(rs['resp'])]
    fig, ax = plt.subplots(figsize=(8, 4.2))
    w = 0.8 / len(resps)
    for i, r in enumerate(resps):
        for j, p in enumerate(pairs):
            m = (rs['pair'] == p) & (rs['resp'] == r) & (rs['level'] == lv)
            if not m.any():
                continue
            x = rs[m].iloc[0]
            ax.bar(j + (i - (len(resps) - 1) / 2) * w, x['days3'], w * 0.92, color=COL[i],
                   label=RESP_LABEL[r] if j == 0 else None)
            ax.plot([j + (i - (len(resps) - 1) / 2) * w] * 2, [x['days3_lo'], x['days3_hi']], color='#0b0b0b', lw=1)
    ax.axhline(5, color='#52514e', lw=1, ls='--')
    ax.text(len(pairs) - 0.5, 5.3, '5 beam days at 1.10 MeV', ha='right', va='bottom', fontsize=8, color='#52514e')
    ax.set_yscale('log')
    ax.set_xticks(range(len(pairs)), [PAIR_LABEL[p].replace(' (', '\n(') for p in pairs], fontsize=8)
    ax.set_ylabel('days to 3σ at R(ATOMKI), 1 µA')
    ax.set_title('Cu hemisphere, as built, reference fit, MM 15° + 0.6 ns TOF', fontsize=9)
    ax.legend(frameon=False, fontsize=8)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    FIG.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG / f'days_by_pair{tag}.png', dpi=150)
    plt.close(fig)


def fig_spectra(sp, tag, ep=1100.0, level='MM 15° + TOF', resp='LNL calibrated'):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    pairs = [p for p in ('vert', 'horiz', 'adj') if p in set(sp['pair'])]
    comps = [('sig', 'X17 at R(ATOMKI)'), ('M1', 'M1 IPC + EPC'), ('E1', 'E1 IPC'), ('g1', '15.1 MeV IPC'),
             ('cos', 'cosmics')]
    fig, axs = plt.subplots(1, len(pairs), figsize=(4 * len(pairs), 3.4), sharey=True)
    axs = np.atleast_1d(axs)
    for ax, p in zip(axs, pairs):
        g = sp[(sp['pair'] == p) & (sp['Ep_keV'] == ep) & (sp['level'] == level) & (sp['resp'] == resp)
               & (sp['ewin'] == 'win')]
        for i, (c, lab) in enumerate(comps):
            cc = ['M1', 'epc'] if c == 'M1' else [c]
            h = g[g['comp'].isin(cc)].groupby('th_lo')['rate_per_day'].sum()
            if h.sum() <= 0:
                continue
            ax.step(h.index + 2.5, h.values, where='mid', color=COL[i], lw=2, label=lab)
        ax.set_yscale('log')
        ax.set_ylim(0.1, None)
        ax.set_xlim(0, 180)
        ax.set_title(PAIR_LABEL[p], fontsize=9)
        ax.set_xlabel('opening angle θ (reco) [°]')
        for s in ('top', 'right'):
            ax.spines[s].set_visible(False)
    axs[0].set_ylabel('pairs per day per 5°')
    axs[-1].legend(frameon=False, fontsize=7)
    fig.suptitle(f'E_p = {ep / 1000:.3g} MeV, 1 µA, {RESP_LABEL.get(resp, resp)}, {LEVEL_LABEL.get(level, level)}',
                 fontsize=9)
    fig.tight_layout()
    fig.savefig(FIG / f'spectra_{ep:.0f}{tag}.png', dpi=150)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tag', default='_pass1')
    ap.add_argument('--T', type=float, default=5.0)
    a = ap.parse_args()
    f = OUT / f'two_arm_reach{a.tag}.csv'
    if not f.exists():
        f = OUT / f'two_arm_nd{a.tag}.csv'
    if f.exists():
        rs = reach(pd.read_csv(f), a.T)
        rs.to_csv(OUT / f'summary_reach{a.tag}.csv', index=False)
        with pd.option_context('display.width', 250, 'display.max_columns', 30, 'display.max_rows', 500):
            print(rs[['pair', 'resp', 'level', 'days3', 'days3_lo', 'days3_hi', f'Z_{a.T:g}d',
                      f'R90_{a.T:g}d_over_ATOMKI', 'S_win', 'Bbeam_win', 'Bcos_win', 'n_mc_cos_win']].round(2))
        fig_days(rs, a.tag)
    fs = OUT / f'two_arm_spectra{a.tag}.csv'
    if fs.exists():
        sp = pd.read_csv(fs)
        rt = rates(sp)
        rt.to_csv(OUT / f'summary_rates{a.tag}.csv', index=False)
        for ep in sorted(set(sp['Ep_keV'])):
            fig_spectra(sp, a.tag, ep=ep)


if __name__ == '__main__':
    main()
