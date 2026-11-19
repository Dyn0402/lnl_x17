#!/usr/bin/env python3
"""
report_tables.py -- the Markdown tables of TWO_ARM_STUDY.md §2, §3, §6 from the summary CSVs (no number typed by hand).

    python3 sim2arm/report_tables.py [--tag _pass3] > sim2arm/out/tables_pass2.md
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / 'out'
Z90, MEG_A = 1.2816, 1.2e-5 / 5.8e-6
REF, PNT, PNT1, TRG = 'MM 15° + TOF', 'MM 15° point, μ 3°', 'MM 15° point, μ 3° + TOF 1 ns', 'trigger'
LEV = [(TRG, 'no veto'), (PNT, 'pointing'), (PNT1, 'pointing + 1 ns TOF'), (REF, 'pointing + 0.6 ns TOF')]
RESP = [('LNL calibrated', 'liquid working'), ('n_TOF as is', 'liquid as at n_TOF'), ('LNL calibrated, LS off', 'no liquid')]
PAIRS = [('horiz', 'horizontal'), ('vert', 'vertical'), ('adj', 'adjacent'), ('all', 'four arms')]


def z(d3, T=5.0):
    return 3 * math.sqrt(T / d3)


def g(df, p, r, lv):
    m = df[(df['pair'] == p) & (df['resp'] == r) & (df['level'] == lv)]
    return None if m.empty else m.iloc[0]


def days_table(df, title, pairs=PAIRS):
    print(f'\n**{title}** — days to 3σ at R(ATOMKI), 1 µA, 1.10 MeV (central; range of the two estimators)\n')
    print('| pair | stack | ' + ' | '.join(lab for _, lab in LEV) + ' |')
    print('|---|---|' + '---|' * len(LEV))
    for p, pl in pairs:
        for r, rl in RESP:
            cells = []
            for lv, _ in LEV:
                x = g(df, p, r, lv)
                if x is None:
                    cells.append('–')
                elif math.isnan(x['days3_transplant']):
                    cells.append(f'{x["days3"]:.0f}†')
                else:
                    cells.append(f'{x["days3"]:.0f} ({x["days3_lo"]:.0f}–{x["days3_hi"]:.0f})')
            if all(c == '–' for c in cells):
                continue
            print(f'| {pl} | {rl} | ' + ' | '.join(cells) + ' |')
    print('\n† direct estimator only (no transplant run); compare with the direct values of the other columns '
          '(out/summary_reach*.csv, days3_direct), not with their central values.')


def limit_table(dfs):
    print('\n**Five days at 1.10 MeV** — expected Z if R = R(ATOMKI), expected 90 % CL limit / R(ATOMKI) '
          '(MEG II: 2.07), chance of ≥ 3σ and ≥ 2σ if ATOMKI is right; horizontal pair\n')
    print('| film | stack | veto | days to 3σ | Z(5 d) | R₉₀ / R(ATOMKI) | R₉₀ / MEG II | P(≥ 3σ) | P(≥ 2σ) |')
    print('|---|---|---|---|---|---|---|---|---|')
    P = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))   # noqa: E731
    for film, df in dfs:
        for r, rl in RESP:
            for lv, ll in ((REF, 'pointing + 0.6 ns TOF'), (PNT, 'pointing')):
                x = g(df, 'horiz', r, lv)
                if x is None:
                    continue
                zz = z(x['days3'])
                print(f'| {film} | {rl} | {ll} | {x["days3"]:.0f} | {zz:.2f} | {Z90 / zz:.2f} | {Z90 / zz / MEG_A:.2f} | '
                      f'{100 * (1 - P(3 - zz)):.0f} % | {100 * (1 - P(2 - zz)):.0f} % |')


def rates_table(df):
    print('\n**Pairs per day in the signal window** (125–160°, |y| < 0.6, E_sum window), liquid working, 20 µm\n')
    print('| pair | veto | X17 at R(ATOMKI) | beam background | cosmics (MC events) | S/B |')
    print('|---|---|---|---|---|---|')
    for p, pl in PAIRS[:2]:
        for lv, ll in LEV:
            x = g(df, p, 'LNL calibrated', lv)
            if x is None:
                continue
            b = x['Bbeam_win'] + x['Bcos_win']
            print(f'| {pl} | {ll} | {x["S_win"]:.1f} | {x["Bbeam_win"]:.0f} | {x["Bcos_win"]:.1f} ({int(x["n_mc_cos_win"])}) | '
                  f'{100 * x["S_win"] / b:.1f} % |')


def spectra_table(tag):
    f = OUT / f'summary_rates{tag}.csv'
    if not f.exists():
        return
    rt = pd.read_csv(f)
    cols = ['25-90', '90-125', '125-160', '160-180']
    for ep, lab in ((1100.0, '1.10 MeV'), (441.0, '0.441 MeV')):
        print(f'\n**{lab}, pairs per day by opening angle** (pointing + 0.6 ns TOF, liquid working, E_sum window; '
              f'in brackets: no E_sum cut)\n')
        print('| pair | component | ' + ' | '.join(c + '°' for c in cols) + ' | all |')
        print('|---|---|' + '---|' * (len(cols) + 1))
        for p, pl in (('horiz', 'horizontal'), ('adj', 'adjacent')):
            for comp, cl in (('sig', 'X17 at R(ATOMKI)'), ('E1', 'E1 IPC'), ('M1', 'M1 IPC'), ('epc', 'external conv.'),
                             ('g1', '15.1 MeV IPC')):
                def val(ew):
                    m = rt[(rt['pair'] == p) & (rt['Ep_keV'] == ep) & (rt['level'] == REF) & (rt['resp'] == 'LNL calibrated')
                           & (rt['ewin'] == ew) & (rt['comp'] == comp)]
                    return None if m.empty else m.iloc[0]
                a, b = val('win'), val('none')
                if a is None:
                    continue
                cells = [f'{a[c]:.0f} ({b[c]:.0f})' if b is not None else f'{a[c]:.0f}' for c in cols + ['all']]
                print(f'| {pl} | {cl} | ' + ' | '.join(cells) + ' |')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tag', default='_pass3')
    a = ap.parse_args()
    d20 = pd.read_csv(OUT / f'summary_reach{a.tag}.csv')
    f11 = OUT / f'summary_reach{a.tag}li11.csv'
    d11 = pd.read_csv(f11) if f11.exists() else None
    days_table(d20, '20 µm Li (as simulated)')
    if d11 is not None:
        days_table(d11, '11 µm Li (the review’s 10–12 µm)', pairs=[p for p in PAIRS if p[0] != 'adj'])
    limit_table([('11 µm', d11), ('20 µm', d20)] if d11 is not None else [('20 µm', d20)])
    rates_table(d20)
    spectra_table(a.tag)


if __name__ == '__main__':
    main()
