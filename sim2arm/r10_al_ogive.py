#!/usr/bin/env python3
"""
r10_al_ogive.py -- the tables of R10_AL_OGIVE.md (task R10, 2026-11-25): the two-arm reach of the Al ogive + Cu liner
(Geant4 config ogAl300cu12r8m4) from two_arm_nd.py, against the scaled estimate of planning/two_arm_estimates.py.

    WORK_DATA=/media/ucla/work bash sim2arm/run_r10.sh 6                      # the fits (tags _pass5al*)
    WORK_DATA=/media/ucla/work $PY sim2arm/r10_al_ogive.py raw                # rows per sample in the merged tables
    WORK_DATA=/media/ucla/work $PY sim2arm/r10_al_ogive.py mcstat             # MC events per component, horizontal pair
    $PY sim2arm/r10_al_ogive.py tables                                        # summaries + the Markdown tables
    $PY sim2arm/r10_al_ogive.py thin                                          # thin tables against the x30 tables (step 6)

Reads sim2arm/out/two_arm_reach_pass5al*.csv and, read-only, the pass-4 files and planning/out/two_arm_reach.csv.
Writes only sim2arm/out/summary_reach_pass5al*.csv and sim2arm/out/r10_mcstat_pass5al[_l13].csv.
R10_SFX=_l13 selects the L12 + L13 tags (the tables of record); without it the L12-only first pass.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / 'out'
sys.path.insert(0, str(HERE))
import summarize as SU      # noqa: E402

AL, CU = 'ogAl300cu12r8m4', 'dome300'
RESPS = ['LNL calibrated', 'n_TOF as is', 'LNL calibrated, LS off']
LEVELS = ['MM 15° + TOF', 'MM 15° point, μ 3°']
#: '' = the first pass, the L12 tables alone (thin); '_l13' = L12 + L13 (x30), the tables of record since 25 Nov.
#: Tags: _pass5al<SFX> (20 µm) and _pass5al<SFX>li11 (11 µm), the names planning/two_arm_estimates.AL_TAGS reads.
SFX = os.environ.get('R10_SFX', '')
FILMS = [('11 µm', '_pass5al' + SFX + 'li11', '_pass4li11', '11 µm Li (recommended)'),
         ('20 µm', '_pass5al' + SFX, '_pass4', '20 µm Li (as simulated)')]
#: the scaled estimate that R10 replaces (planning/out/two_arm_reach.csv as it was on 25 Nov morning: the four-arm
#: §19.3 days x the Cu ogive's two-arm / four-arm ratio), horizontal pair: (film, liquid, veto) -> (days, R90 / R(ATOMKI)).
#: Frozen here because the planning now reads the simulation.
SCALED = {('11 µm', 'LNL calibrated', 'MM 15° + TOF'): (10.4, 0.62), ('11 µm', 'LNL calibrated', 'MM 15° point, μ 3°'): (9.4, 0.59),
          ('11 µm', 'n_TOF as is', 'MM 15° + TOF'): (18.2, 0.81), ('11 µm', 'n_TOF as is', 'MM 15° point, μ 3°'): (15.9, 0.76),
          ('11 µm', 'LNL calibrated, LS off', 'MM 15° + TOF'): (58.8, 1.46),
          ('11 µm', 'LNL calibrated, LS off', 'MM 15° point, μ 3°'): (57.8, 1.45),
          ('20 µm', 'LNL calibrated', 'MM 15° + TOF'): (7.5, 0.52), ('20 µm', 'LNL calibrated', 'MM 15° point, μ 3°'): (7.0, 0.50),
          ('20 µm', 'n_TOF as is', 'MM 15° + TOF'): (13.5, 0.70), ('20 µm', 'n_TOF as is', 'MM 15° point, μ 3°'): (11.6, 0.65),
          ('20 µm', 'LNL calibrated, LS off', 'MM 15° + TOF'): (43.1, 1.25),
          ('20 µm', 'LNL calibrated, LS off', 'MM 15° point, μ 3°'): (41.0, 1.22)}
STACK = {'LNL calibrated': '+ liquid working', 'n_TOF as is': '+ liquid as at n_TOF',
         'LNL calibrated, LS off': 'SiPM wall + small plastics (no liquid)'}
VETO = {'MM 15° + TOF': 'MM pointing + 0.6 ns TOF', 'MM 15° point, μ 3°': 'MM pointing only'}
T = 5.0


def r90(d):
    """expected 90 % CL limit after T days in units of R(ATOMKI) (planning/two_arm_estimates.r90)."""
    return 1.2816 / (3.0 * np.sqrt(T / d))


def summ(tag, write=True):
    f = OUT / f'two_arm_reach{tag}.csv'
    if not f.exists():
        return None
    rs = SU.reach(pd.read_csv(f), T)
    if write and 'pass5al' in tag:
        rs.to_csv(OUT / f'summary_reach{tag}.csv', index=False)
    return rs.set_index(['pair', 'resp', 'level'])


def f3(x):
    return f'{x:.3g}' if np.isfinite(x) else '–'


def tables():
    thin12 = {f: summ(t.replace(SFX, '', 1), write=False) for f, t, _, _ in FILMS} if SFX else {}
    for film, tag, tag4, flab in FILMS:
        s = summ(tag)
        if s is None:
            print(f'\n{film}: no table {tag}')
            continue
        p4 = pd.read_csv(OUT / f'summary_reach{tag4}.csv').set_index(['pair', 'resp', 'level'])
        print(f'\n**{film} Li, Al ogive + Cu liner** (`out/summary_reach{tag}.csv`)\n')
        print('| liquid | cosmic veto | two arms (horizontal pair): days to 3σ, central (lo–hi) | direct, transplant '
              '| R₉₀(5 d) / R(ATOMKI), two arms (range) | four arms, same fit: days (lo–hi) | R₉₀(5 d), four arms '
              '| scaled estimate: days, R₉₀ | simulation / estimate: days, R₉₀ | Cu hemisphere (pass 4): days, R₉₀ |'
              + (' L12 alone, two arms: days (direct, transplant), R₉₀ |' if SFX else ''))
        print('|---|---|---|---|---|---|---|---|---|---|' + ('---|' if SFX else ''))
        for r in RESPS:
            for lv in LEVELS:
                if ('horiz', r, lv) not in s.index:
                    continue
                h = s.loc[('horiz', r, lv)]
                a = s.loc[('all', r, lv)] if ('all', r, lv) in s.index else None
                ed, er = SCALED[(film, r, lv)]
                c = p4.loc[('horiz', r, lv)]
                four = (f"{f3(a.days3)} ({f3(a.days3_lo)}–{f3(a.days3_hi)}) | {r90(a.days3):.2f}" if a is not None else '– | –')
                print(f"| {SU.RESP_LABEL[r]} | {VETO[lv]} | **{f3(h.days3)}** ({f3(h.days3_lo)}–{f3(h.days3_hi)}) "
                      f"| {f3(h.days3_direct)}, {f3(h.days3_transplant)} "
                      f"| **{r90(h.days3):.2f}** ({r90(h.days3_lo):.2f}–{r90(h.days3_hi):.2f}) | {four} "
                      f"| {ed:g}, {er:.2f} | ×{h.days3 / ed:.2f}, ×{r90(h.days3) / er:.2f} "
                      f"| {f3(c.days3)}, {r90(c.days3):.2f} |"
                      + (f" {f3(t.days3)} ({f3(t.days3_direct)}, {f3(t.days3_transplant)}), {r90(t.days3):.2f} |"
                         if (t := (thin12.get(film).loc[('horiz', r, lv)] if thin12.get(film) is not None else None)) is not None
                         else ''))
    for tag, lab in (('_pass5al_closure', 'closure: dome300, horizontal, 11 µm'),
                     ('_pass5al_old', '§19.3 settings: 0.3 ns time of flight, L4 cosmics, 20 µm')):
        s = summ(tag)
        if s is not None:
            print(f'\n{lab} (`out/summary_reach{tag}.csv`)')
            print(s[['days3_direct', 'days3_transplant', 'days3', 'S_win', 'Bbeam_win', 'Bcos_win', 'n_mc_cos_win']].round(2).to_string())
    # MC counts in the fit region from the direct rows of the reach tables
    print('\nMC events in the fit region (direct rows, reference level, liquid working):')
    for lab, tag in (('Al ogive + Cu liner, L12 + L13', '_pass5al_l13li11'), ('Al ogive + Cu liner, L12', '_pass5alli11'),
                     ('Cu hemisphere, L10 + L18', '_pass4li11')):
        f = OUT / f'two_arm_reach{tag}.csv'
        if not f.exists():
            continue
        d = pd.read_csv(f)
        for pair in ('horiz', 'all'):
            m = (d.pair == pair) & (d.resp == RESPS[0]) & (d.level == LEVELS[0]) & (d.mc == 'direct')
            if m.any():
                x = d[m].iloc[0]
                print(f"  {lab:28s} {pair:5s}: " + ' '.join(f"{c} {int(x['n_' + c])} ({x['rate_' + c]:.3g}/d)"
                                                           for c in ('sig', 'M1', 'E1', 'g1', 'epc', 'cos')))


def thin():
    """the thin-table test (run_r10.sh step 6): the Cu ogive on L11 alone and the Cu hemisphere on L10 alone against
    the same fits on the x30 tables (passes 3 and 4).  11 µm, reference level."""
    lv = LEVELS[0]
    print('| holder | pair | liquid | thin tables: days (direct, transplant) | ×30 tables: days (direct, transplant) | thin / ×30 '
          '(direct, transplant) |')
    print('|---|---|---|---|---|---|')
    for lab, tthin, tdense in (('Cu ogive, L11 alone against L11 + L13', '_pass5al_thin_ogCu200li11', '_pass3li11'),
                               ('Cu hemisphere, L10 alone against L10 + L18', '_pass5al_thin_dome300li11', '_pass4li11')):
        a = summ(tthin)
        if a is None:
            continue
        b = pd.read_csv(OUT / f'summary_reach{tdense}.csv').set_index(['pair', 'resp', 'level'])
        for pair in ('horiz', 'all'):
            for r in RESPS:
                x, y = a.loc[(pair, r, lv)], b.loc[(pair, r, lv)]
                print(f"| {lab} | {SU.PAIR_LABEL[pair].split(' (')[0]} | {SU.RESP_LABEL[r]} "
                      f"| {f3(x.days3)} ({f3(x.days3_direct)}, {f3(x.days3_transplant)}) "
                      f"| {f3(y.days3)} ({f3(y.days3_direct)}, {f3(y.days3_transplant)}) "
                      f"| ×{x.days3 / y.days3:.2f} (×{x.days3_direct / y.days3_direct:.2f}, "
                      f"×{x.days3_transplant / y.days3_transplant:.2f}) |")
    for lab, tag in (('Cu ogive, L11 alone', '_pass5al_thin_ogCu200li11'), ('Cu ogive, L11 + L13', '_pass3li11'),
                     ('Cu hemisphere, L10 alone', '_pass5al_thin_dome300li11'), ('Cu hemisphere, L10 + L18', '_pass4li11'),
                     ('Al ogive + Cu liner, L12 alone', '_pass5alli11'), ('Al ogive + Cu liner, L12 + L13', '_pass5al_l13li11')):
        f = OUT / f'two_arm_reach{tag}.csv'
        if not f.exists():
            continue
        d = pd.read_csv(f)
        for pair in ('horiz', 'all'):
            m = (d.pair == pair) & (d.resp == RESPS[0]) & (d.level == lv) & (d.mc == 'direct')
            if m.any():
                x = d[m].iloc[0]
                print(f"  {lab:32s} {pair:5s}: " + ' '.join(f"{c} {int(x['n_' + c])} ({x['rate_' + c]:.3g}/d)"
                                                           for c in ('sig', 'M1', 'E1', 'g1', 'epc', 'cos')))


def raw():
    """rows per sample in the merged four-arm tables, all pairs and the horizontal pair (before any selection)."""
    W = Path(os.environ.get('WORK_DATA', '/media/ucla/work')) / 'x17_facility_search'
    runs = [('L12', 'lnl_sel', AL), ('L13', 'lnl_sel', AL), ('L10', 'lnl_sel', CU), ('L18', 'sel_l18', CU),
            ('L11', 'lnl_sel', 'ogCu200'), ('L13', 'lnl_sel', 'ogCu200')]
    print('| sample | run | config | generated | two-arm rows | horizontal pair | vertical pair |')
    print('|---|---|---|---|---|---|---|')
    for s in ('X17_m16.8', 'M1_18.15', 'E1_18.15', 'M1_15.1', 'E1_15.1', 'gam_8Be'):
        for run, d, cfg in runs:
            f = W / d / f'{run}_{s}_{cfg}_asb_sel.npz'
            if run == 'L13' and s.startswith('X17'):      # L13 has no X17 sample
                continue
            if not f.exists():
                print(f'| {s} | {run} | {cfg} | not on this disk | | | |')
                continue
            z = np.load(f, allow_pickle=True)
            a1, a2 = z['a1'], z['a2']
            h = ((a1 == 0) & (a2 == 1)) | ((a1 == 1) & (a2 == 0))
            v = ((a1 == 2) & (a2 == 3)) | ((a1 == 3) & (a2 == 2))
            print(f"| {s} | {run} | {cfg} | {int(z['cnt_n_generated']):,} | {len(a1):,} | {int(h.sum()):,} | {int(v.sum()):,} |")


def mcstat():
    """MC events per component for the horizontal pair and the four arms at the reference selection (liquid working,
    MM 15° + TOF, direct tables): in the fit region (θ ≥ 90°, the E_sum fit range) and in the signal window
    (125-160°, |y| < 0.6, the E_sum window).  Rates with the 11 µm yields."""
    os.environ.setdefault('WORK_DATA', '/media/ucla/work')
    os.environ['TA_CFG'] = AL
    if not SFX:                       # the first pass: the L12 tables alone (the L13 tables are on the disk since 25 Nov)
        os.environ['TA_RUNS'] = 'L12'
    import two_arm_nd as TA
    SN, N = TA.SN, TA.N
    rows = []
    for cfg in ((AL,) if SFX else (AL, CU)):     # TA_RUNS acts on TA_CFG only: the hemisphere keeps L10 + L18
        for pair in ('horiz', 'all'):
            for resp in (RESPS[0],):
                TA.set_pair(pair)
                SN.register_levels()
                ec = SN.window('asb', resp)
                an = N.analyses(ec)[SN.REF_AN]
                ev = SN.collect(cfg, 'asb', 1100.0, resp, level=LEVELS[0], I_uA=1.0, live=SN.LIVE_S2, li_ug=587.0)
                b = N.Binner(an, ev['v0'], False)
                v = ev['v0']
                win = b.m & (v['th'] >= SN.SIG_WIN['th'][0]) & (v['th'] < SN.SIG_WIN['th'][1]) & (v['y'] < SN.SIG_WIN['y']) \
                    & (v['E'] > ec[0]) & (v['E'] < ec[1])
                for c in ('sig', 'M1', 'E1', 'g1', 'epc', 'cos'):
                    r = dict(config=cfg, pair=pair, resp=resp, level=LEVELS[0], ecut=f'{ec[0]:g}-{ec[1]:g}', comp=c)
                    for lab, m in (('fit', b.m), ('win', win)):
                        mm = m & (ev['comp'] == c)
                        r[f'n_mc_{lab}'] = int(len(np.unique(ev['uid'][mm])))
                        r[f'rate_{lab}'] = float(ev['w'][mm].sum())
                    rows.append(r)
                    print(r, flush=True)
                SN._drop_tables()
    df = pd.DataFrame(rows)
    df.to_csv(OUT / f'r10_mcstat_pass5al{SFX}.csv', index=False)
    print(df.to_string())


if __name__ == '__main__':
    {'tables': tables, 'raw': raw, 'mcstat': mcstat, 'thin': thin}[sys.argv[1] if len(sys.argv) > 1 else 'tables']()
