#!/usr/bin/env python3
"""
epc_l19.py -- the external conversions (EPC) of the ⁸Be γ lines in the built Cu hemisphere, L18 (3e8 γ) against L19
(x100, analog, same geometry), at the level of the merged pair tables (lnl_x17, 2026-11-25; write-up EPC_L19.md).

    python3 sim2arm/epc_l19.py            # -> out/epc_l19/steps.csv, volumes.csv, esum.csv, *.png

* steps: two-arm 'ok' pairs per 10⁹ γ (all four lines, equal weights) for each arm pair, step by step: θ > 90°,
  125-160°, raw E_sum > 10 MeV, raw E_sum 13-19 MeV; L18 and L19 side by side (a consistency test of the two runs).
* volumes: where the primary γ first interacted (L19's g_fvol), for the horizontal pair at 125-160°.
* esum: the raw E_sum spectrum of the horizontal / vertical pairs at 125-160°.
The fit-level numbers (detector response, pointing, TOF, the yields) come from two_arm_nd.py with TA_EPC_RUN=L19.
"""
from __future__ import annotations

import os
from pathlib import Path

import numpy as np

W = Path(os.environ.get('WORK_DATA', '/media/ucla/work')) / 'x17_facility_search'
HERE = Path(__file__).resolve().parent
OUT = HERE / 'out' / 'epc_l19'
OUT.mkdir(parents=True, exist_ok=True)
F18 = W / 'sel_l18' / 'L18_gam_8Be_dome300_asb_sel.npz'
F19 = W / 'sel_l19' / 'L19_gam_8Be_dome300_asb_sel.npz'
PAIRS = {'horiz': (0, 1), 'vert': (2, 3), 'adj': (0, 2)}


def load(f):
    z = np.load(f, allow_pickle=False)
    return {k: z[k] for k in z.files if not k.startswith('sg_')}


def masks(z, pair):
    a1, a2 = z['a1'], z['a2']
    p, q = pair
    m = ((a1 == p) & (a2 == q)) | ((a1 == q) & (a2 == p))
    th, E = z['reco_c'], z['E1'] + z['E2']
    return dict(pair=m, th90=m & (th > 90), win=m & (th > 125) & (th < 160),
                win_E10=m & (th > 125) & (th < 160) & (E > 10),
                win_E13_19=m & (th > 125) & (th < 160) & (E > 13) & (E < 19),
                adj25_90=m & (th > 25) & (th < 90))


def main():
    import pandas as pd
    runs = {'L18': load(F18)}
    if F19.exists():
        runs['L19'] = load(F19)
    rows = []
    for run, z in runs.items():
        ng = int(z['cnt_n_generated'])
        for pn, pr in PAIRS.items():
            for step, m in masks(z, pr).items():
                n = int(m.sum())
                rows.append(dict(run=run, n_gamma=ng, pair=pn, step=step, n_mc=n, per_1e9=n / ng * 1e9,
                                 err_per_1e9=np.sqrt(max(n, 1)) / ng * 1e9))
    st = pd.DataFrame(rows)
    st.to_csv(OUT / 'steps.csv', index=False)
    pd.set_option('display.width', 200)
    piv = st.pivot_table(index=['pair', 'step'], columns='run', values=['n_mc', 'per_1e9'])
    print(piv.round(2).to_string())
    if 'L19' in runs:
        a = st[st.run == 'L18'].set_index(['pair', 'step'])
        b = st[st.run == 'L19'].set_index(['pair', 'step'])
        pull = (b.per_1e9 - a.per_1e9) / np.hypot(a.err_per_1e9, b.err_per_1e9)
        print('\nL19 - L18 in σ (per 10⁹ γ):')
        print(pull.round(2).to_string())

    z = runs.get('L19')
    if z is not None and 'g_fvol' in z:
        vr = []
        for pn in ('horiz', 'vert', 'adj'):
            mm = masks(z, PAIRS[pn])
            for step in ('win', 'win_E10', 'win_E13_19', 'adj25_90'):
                m = mm[step]
                v, c = np.unique(z['g_fvol'][m], return_counts=True)
                p_, pc = np.unique(z['g_fproc'][m], return_counts=True)
                for vi, ci in zip(v, c):
                    vr.append(dict(pair=pn, step=step, what='volume', name=vi, n=int(ci), frac=ci / max(m.sum(), 1)))
                for vi, ci in zip(p_, pc):
                    vr.append(dict(pair=pn, step=step, what='process', name=vi, n=int(ci), frac=ci / max(m.sum(), 1)))
        vd = pd.DataFrame(vr)
        vd.to_csv(OUT / 'volumes.csv', index=False)
        for pn in ('horiz', 'adj'):
            for step in (('win', 'win_E13_19') if pn == 'horiz' else ('adj25_90',)):
                d = vd[(vd.pair == pn) & (vd.step == step)].sort_values('n', ascending=False)
                print(f'\n{pn} {step}: first interaction of the primary γ')
                print(d[['what', 'name', 'n', 'frac']].round(3).head(14).to_string(index=False))
        if 'gcnt_vol' in z:
            print('\nall generated γ by first-interaction volume (top 12, per cent):')
            o = np.argsort(-z['gcnt_n'])
            for i in o[:12]:
                print(f'  {z["gcnt_vol"][i] or "(none)":24s} {100 * z["gcnt_n"][i] / z["cnt_n_generated"]:.3f}')

    # raw E_sum at 125-160°, horizontal and vertical
    edges = np.arange(0, 26, 1.0)
    er = []
    for run, z in runs.items():
        ng = int(z['cnt_n_generated'])
        for pn in ('horiz', 'vert'):
            m = masks(z, PAIRS[pn])['win']
            h = np.histogram((z['E1'] + z['E2'])[m], edges)[0]
            for i, n in enumerate(h):
                er.append(dict(run=run, pair=pn, E_lo=edges[i], n_mc=int(n), per_1e9=n / ng * 1e9))
    ed = pd.DataFrame(er)
    ed.to_csv(OUT / 'esum.csv', index=False)
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 2, figsize=(10, 3.8))
        for k, pn in enumerate(('horiz', 'vert')):
            for run, c in (('L18', '#c80'), ('L19', 'k')):
                d = ed[(ed.run == run) & (ed.pair == pn)]
                if len(d):
                    y = d.per_1e9.values
                    ax[k].step(d.E_lo + 0.5, np.where(y > 0, y, np.nan), where='mid', c=c, label=f'{run} ({d.n_mc.sum()} MC)')
            ax[k].axvspan(13, 19, color='#fc3', alpha=0.3, lw=0)
            ax[k].set_yscale('log')
            ax[k].set_xlabel('raw E_sum of the two arms [MeV]')
            ax[k].set_title(f'{pn} pair, θ 125-160°', fontsize=10)
            ax[k].legend(frameon=False, fontsize=8)
        ax[0].set_ylabel('pairs per 10⁹ γ per MeV')
        fig.tight_layout()
        fig.savefig(OUT / 'esum.png', dpi=130)
        print('->', OUT / 'esum.png')
    except ImportError:
        pass


if __name__ == '__main__':
    main()
