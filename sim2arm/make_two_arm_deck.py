#!/usr/bin/env python3
"""
make_two_arm_deck.py -- the slide note of the two-arm LNL study (TWO_ARM_STUDY.md), from the sim2arm/out CSVs.

    python3 sim2arm/make_two_arm_deck.py [--tag _pass3] [--out sim2arm/out/lnl-two-arm-run.html]
    python3 ~/PycharmProjects/dylan-cern-site/scripts/add-note.py sim2arm/out/lnl-two-arm-run.html --slug lnl-two-arm-run --force --deploy
"""
from __future__ import annotations

import argparse
import math
import os
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, os.path.expanduser(os.environ.get('SLIDEDOC_DIR', '~/PycharmProjects/dylan-cern-site/scripts')))
import slidedoc as sd   # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / 'out'
R_A, MEG = 5.8e-6, 1.2e-5
Z90 = 1.2816
T_RES = 5.0
REF, PNT, PNT1, TRG = 'MM 15° + TOF', 'MM 15° point, μ 3°', 'MM 15° point, μ 3° + TOF 1 ns', 'trigger'
RESP = [('LNL calibrated', 'liquid working', sd.BLUE), ('n_TOF as is', 'liquid as at n_TOF', sd.ORANGE),
        ('LNL calibrated, LS off', 'no liquid', sd.GREY)]
GEOM = [('horiz', 'horizontal'), ('vert', 'vertical')]
LEVLAB = {TRG: 'no veto', PNT: 'pointing', PNT1: 'pointing + 1 ns TOF', REF: 'pointing + 0.6 ns TOF'}


def zf(d3, T=T_RES):
    return 3 * math.sqrt(T / d3)


def r90(d3, T=T_RES):
    return Z90 / zf(d3, T)


def pnorm(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def get(df, pair, resp, level):
    m = df[(df['pair'] == pair) & (df['resp'] == resp) & (df['level'] == level)]
    return None if m.empty else m.iloc[0]


def geom_svg(kind, w=360, h=330):
    """beam's-eye view: the target, the two arms (thick bars), cosmic arrows."""
    cx, cy, R, L = w / 2, h / 2 + 10, 92, 120
    s = []
    for k in range(4):   # all four arm places, faint
        a = math.radians(90 * k)
        x, y = cx + R * math.cos(a), cy - R * math.sin(a)
        dx, dy = -math.sin(a) * L / 2, -math.cos(a) * L / 2
        s.append(sd.line(x - dx, y - dy, x + dx, y + dy, sd.RULE, 10))
    on = {'vert': (90, 270), 'horiz': (0, 180), 'adj': (0, 90), 'rot': (70, 110)}[kind]
    for deg in on:
        a = math.radians(deg)
        x, y = cx + R * math.cos(a), cy - R * math.sin(a)
        dx, dy = -math.sin(a) * L / 2, -math.cos(a) * L / 2
        s.append(sd.line(x - dx, y - dy, x + dx, y + dy, sd.BLUE, 14))
    s.append(f'<circle cx="{cx}" cy="{cy}" r="9" fill="{sd.RED}"/>')
    for x0 in (cx - 120, cx + 120):
        s.append(sd.arrow(x0, 18, x0 - 14, 80, sd.GREY, 2.5))
    s.append(sd.arrow(cx, 18, cx, 52, sd.GREY, 2.5))
    s.append(sd.T(cx + 60, 30, 'cosmic μ', 18, sd.MUT))
    return sd.svg(w, h, ''.join(s), kind)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tag', default='_pass3')
    ap.add_argument('--out', default=str(OUT / 'lnl-two-arm-run.html'))
    a = ap.parse_args()
    rs = pd.read_csv(OUT / f'summary_reach{a.tag}.csv')
    f11 = OUT / f'summary_reach{a.tag}li11.csv'
    r11 = pd.read_csv(f11) if f11.exists() else None
    rt = pd.read_csv(OUT / f'summary_rates{a.tag}.csv') if (OUT / f'summary_rates{a.tag}.csv').exists() else None
    ta = pd.read_csv(OUT / 'ta_compare.csv') if (OUT / 'ta_compare.csv').exists() else None
    cr = pd.read_csv(OUT / 'cosmic_rates.csv') if (OUT / 'cosmic_rates.csv').exists() else None
    cth = pd.read_csv(OUT / 'cosmic_theta.csv') if (OUT / 'cosmic_theta.csv').exists() else None

    base = r11 if r11 is not None else rs
    film = '11 µm Li' if r11 is not None else '20 µm Li'
    h_fix, h_nt, h_off = (get(base, 'horiz', r, REF) for r, _, _ in RESP)
    best, mid = r90(h_fix['days3']), r90(h_nt['days3'])
    z_fix, z_nt = zf(h_fix['days3']), zf(h_nt['days3'])
    D = sd.Deck('Two arms, 8 days at LNL: what to expect and how to spend them',
                'Geant4 two-arm study for the slot-1 LNL feasibility run: reach, geometry, cosmics, run plan')

    # ---- 1 cover
    p3 = 1 - pnorm(3 - z_nt)
    cover = (sd.kicker('LNL slot 1 · two Micromegas arms · the built Cu hemisphere · Geant4, 20 Nov 2026')
             + sd.p(f'Two arms in 8 days with the built Cu hemisphere: about MEG II’s limit, a feasibility test first', 60, sd.DINK, 600)
             + sd.p('Its 300 µm wall costs ×6 in days against the Cu ogive simulated on 19 Nov by mistake; a lighter Al end piece would recover it (estimate). Opposite arms, horizontal; liquid cells in; the veto tested vertical before the beam.', 28, sd.DMUT)
             + sd.row(sd.bignum(f'{min(mid, best):.1f}–{max(mid, best):.1f}×', 'expected 90 % limit / R(ATOMKI)', sd.DBLUE,
                                f'5 days at 1.10 MeV, {film}, liquid as at n_TOF … working. MEG II: 2.07×',
                                tip='R90 = 1.28 / Z × R(ATOMKI); Z = 3 √(5 d / d₃σ) from the reference fit'),
                      sd.bignum(f'{z_nt:.1f}–{z_fix:.1f}σ', 'expected Z if ATOMKI is right', sd.DGREEN,
                                f'chance of ≥ 3σ: {100 * p3:.0f}–{100 * (1 - pnorm(3 - z_fix)):.0f} %'),
                      sd.bignum(f'×{h_off["days3"] / h_fix["days3"]:.0f}', 'days without the liquid cells', sd.DRED,
                                'the single biggest lever on the reach'), gap=56))
    D.slide('cover', cover, '', dark=True, short='Answer')

    # ---- 2 geometries
    cells = []
    for kind, name, sub in (('vert', 'vertical pair', 'X17 window; every vertical muon crosses both arms'),
                            ('horiz', 'horizontal pair', 'X17 window; muons must be near-horizontal'),
                            ('adj', 'adjacent (90°)', 'opening angles 25–120°: no X17'),
                            ('rot', 'turned in (Δφ < 180°)', 'centred on 140°: more IPC, tested and dropped')):
        cells.append(sd.col(geom_svg(kind), sd.p(name, 28, weight=600), sd.p(sub, 22, sd.MUT), w=380, gap=8))
    body = (sd.title('Four ways to place two arms, seen along the beam',
                     'Simulated: all four on the Cu hemisphere, as built, the reference fit cut to each pair')
            + sd.row(*cells, gap=36)
            + sd.p('Hover the dotted terms and the points for numbers and sources.', 22, sd.MUT))
    D.slide('geom', body, '''The four arm places are those of the n_TOF pinwheel (faces at ±20.4 cm). Arms 2/3 are top/bottom
(+z/−z), 0/1 the sides. Every beam sample (X17 m16.8, Born M1/E1 IPC at 18.15 and 15.1 MeV, ⁸Be γ for external
conversions) is the four-arm Geant4 of runs L11 + L13; each fit keeps only events whose selected pair is the requested one.
The turned-in geometry is a new Geant4 run (L16, MX17_Full_Geant branch lnl_twoarm, --arms 0,1 --arm-phi).''', short='Geometries')

    # ---- 3 spectra
    if rt is not None:
        sp = pd.read_csv(OUT / f'two_arm_spectra{a.tag}.csv')
        panels = []
        comps = [('sig', 'X17 at R(ATOMKI)', sd.RED), ('E1', 'E1 IPC (direct capture)', sd.BLUE),
                 ('M1', 'M1 IPC + conversions', sd.PURPLE), ('g1', '15.1 MeV IPC', sd.GOLD), ('cos', 'cosmics', sd.GREY)]
        for pair, nm in (('horiz', 'horizontal pair'), ('adj', 'adjacent pair')):
            g = sp[(sp['pair'] == pair) & (sp['Ep_keV'] == 1100) & (sp['level'] == REF) & (sp['resp'] == 'LNL calibrated')
                   & (sp['ewin'] == 'win')]
            P = sd.Plot(800, 520, x=(0, 180, 'lin'), y=(0.1, 300, 'log'), xlabel='opening angle θ [°]',
                        ylabel='pairs / day / 5°', title=nm)
            P.xticks([(v, str(v)) for v in [0, 30, 60, 90, 120, 150, 180]])
            P.yticks([(0.1, '0.1'), (1, '1'), (10, '10'), (100, '100')])
            for c, lab, col in comps:
                cc = ['M1', 'epc'] if c == 'M1' else [c]
                hh = g[g['comp'].isin(cc)].groupby('th_lo')['rate_per_day'].sum()
                if hh.sum() <= 0:
                    continue
                keep = [(x + 2.5, v) for x, v in zip(hh.index, hh.values) if v > 0.1]
                xs = [k[0] for k in keep]
                ys = [k[1] for k in keep]
                tips = [f'{lab}\nθ {x - 2.5:.0f}–{x + 2.5:.0f}°: {v:.1f} / day' for x, v in keep]
                P.line(xs, ys, col, w=3, r=4, tips=tips)
            panels.append(P.svg(nm))
        body = (sd.title('Opposite arms hold the X17 window; adjacent arms see the small angles at 6× the rate',
                         '1.10 MeV, 1 µA, 20 µm Li, liquid working, E_sum window, pointing + 0.6 ns TOF')
                + sd.row(*panels, gap=44) + sd.legend([(lab, col) for _, lab, col in comps]))
        D.slide('spectra', body, '''Rates per day of the two-arm set-up, from the reference event tables (the Cu hemisphere's own
X17 and IPC Monte Carlo, weighted with its film yields at E_p = 1.10 MeV). "M1 IPC + conversions" includes the external
pair conversion (EPC) of ⁸Be γ in the Cu wall, which rests on a few hundred MC events: its bins jump.
The vertical pair looks the same as the horizontal one for beam pairs (not shown).''', short='Spectra')

    # ---- 4 reach bars
    rows = []
    for df, flab in ((rs, '20 µm'), (r11, '11 µm')):
        if df is None:
            continue
        for pair, gl in GEOM:
            for resp, rl, col in RESP:
                for lv in (REF, PNT):
                    x = get(df, pair, resp, lv)
                    if x is None:
                        continue
                    tip = (f'{gl} pair, {rl}, {LEVLAB[lv]}, {flab} Li\ndays to 3σ {x["days3"]:.1f} '
                           f'({x["days3_lo"]:.1f}–{x["days3_hi"]:.1f})\nZ in 5 d {zf(x["days3"]):.2f}σ, '
                           f'R90 {r90(x["days3"]):.2f}×R(ATOMKI)\nS {x["S_win"]:.1f}/d, beam B {x["Bbeam_win"]:.0f}/d, '
                           f'cosmic B {x["Bcos_win"]:.1f}/d in 125–160°')
                    rows.append((flab, pair, gl, resp, rl, col, lv, x, tip))
    if rows:
        P = sd.Plot(1664, 640, x=(-0.5, len(rows) - 0.5, 'lin'), y=(3, 300, 'log'), ylabel='days to 3σ at R(ATOMKI)',
                    margin=(24, 30, 150, 110))
        P.yticks([(5, '5'), (10, '10'), (20, '20'), (50, '50'), (100, '100'), (200, '200')])
        for i, (flab, pair, gl, resp, rl, col, lv, x, tip) in enumerate(rows):
            P.vbar(i, x['days3'], 30, col, tip=tip, base=3, opacity=1.0 if lv == REF else 0.45)
            P.raw(sd.line(P.X(i), P.Y(x['days3_lo']), P.X(i), P.Y(x['days3_hi']), sd.INK, 2))
        groups = {}
        for i, r in enumerate(rows):
            groups.setdefault((r[0], r[2]), []).append(i)
        for (flab, gl), ii in groups.items():
            P.text((ii[0] + ii[-1]) / 2, 2.2, f'{gl} · {flab}', 22, sd.INK, 'middle', 600)
        P.hline(T_RES, sd.RED, label='5 beam days', where='above')
        body = (sd.title('No configuration reaches 3σ in 5 days; the liquid cells decide the rest',
                         'Reference fit, Cu hemisphere as built, 1 µA, 1.10 MeV; bar = central, line = the two MC-safe estimators')
                + P.svg('days to 3 sigma')
                + sd.legend([(rl, col, 'box') for _, rl, col in RESP]
                            + [('solid: pointing + 0.6 ns TOF', sd.INK, 'line'), ('pale: pointing only', sd.GREY, 'line')]))
        D.slide('reach', body, '''Days to 3σ at R(ATOMKI) = 5.8×10⁻⁶, from the FEASIBILITY_SIM §19 reference fit (θ × |y| × E_sum,
background shape floating) on one pair of arms. Central value: geometric mean of the "direct + one-event floor" and
"transplant" estimators; the black line spans them. 11 µm: the yields of an 11 µm film (target review), the Geant4
events of the 20 µm run. Table: sim2arm/out/summary_reach*.csv.''', short='Reach')

    # ---- 5 limit vs days
    P = sd.Plot(1100, 640, x=(1, 15, 'lin'), y=(0.3, 4, 'log'), xlabel='days at 1.10 MeV, 1 µA',
                ylabel='expected 90 % CL limit / R(ATOMKI)')
    P.xticks([(v, str(v)) for v in [1, 3, 5, 7, 9, 11, 13, 15]])
    P.yticks([(0.3, '0.3'), (0.5, '0.5'), (1, '1'), (2, '2'), (4, '4')])
    P.hline(1.0, sd.RED, label='ATOMKI', where='above')
    P.hline(MEG / R_A, sd.PURPLE, label='MEG II 90 % limit', where='above')
    for resp, rl, col in RESP:
        x = get(base, 'horiz', resp, REF)
        if x is None:
            continue
        ds = [1 + 0.5 * k for k in range(29)]
        P.band(ds, [r90(x['days3_hi'], d) for d in ds], [r90(x['days3_lo'], d) for d in ds], col, 0.15)
        P.line(ds, [r90(x['days3'], d) for d in ds], col, markers=False,
               tip=f'{rl}: days to 3σ {x["days3"]:.1f}')
    P.vline(T_RES, label='the plan')
    body = (sd.title('Five days with the built Cu hemisphere: about MEG II’s limit with the liquid cells, above it without',
                     f'Horizontal pair, {film}, pointing + 0.6 ns TOF; band = the two estimators')
            + sd.row(P.svg('limit vs days'),
                     sd.col(sd.legend([(rl, col) for _, rl, col in RESP]),
                            sd.callout(f'An ATOMKI-size signal would show at {z_nt:.1f}–{z_fix:.1f}σ: no physics result. A lighter Al end piece: ~0.6–0.8 × R(ATOMKI) (estimate).', sd.RED),
                            sd.callout('Every result below the purple line is a better limit than MEG II’s.', sd.PURPLE),
                            w=520), gap=44))
    D.slide('limit', body, '''Expected 90 % CL upper limit with no signal: R90 = 1.2816 / Z(T) × R(ATOMKI), with Z linear in R
(background-dominated) and Z(T) = 3 √(T / d₃σ). MEG II (EPJC 85, 763 (2025)): R(18.1 MeV) < 1.2×10⁻⁵ at 90 % CL.
Systematics beyond the fit's floating background shape are not included.''', short='Limit')

    # ---- 6 cosmics: generator + MEG II peak
    if cr is not None:
        bars = []
        for pair, nm in (('vert', 'vertical'), ('horiz', 'horizontal'), ('adj', 'adjacent')):
            for smp, col in (('L4 plane', sd.GREY), ('L15 disk', sd.BLUE)):
                m = cr[(cr['sample'] == smp) & (cr['pair'] == pair)]
                if m.empty:
                    continue
                v = float(m['per_day'].iloc[0])
                bars.append((f'{nm} · {smp.split()[0]}', max(v, 1), col,
                             f'{smp}: {v:,.0f} two-arm coincidences / day ({int(m["n_mc"].iloc[0])} MC, '
                             f'{float(m["live_days"].iloc[0]):.1f} live days)'))
        left = sd.col(sd.p('Two-arm cosmic coincidences per day', 26, weight=600),
                      sd.hbars(bars, 3e5, width=520, log=True, vmin=10, label_w=280, fmt=lambda v: f'{v:,.0f}', size=24),
                      sd.legend([('L4: plane 1.5 m above (old)', sd.GREY, 'box'), ('L15: every zenith angle (new)', sd.BLUE, 'box')], 22),
                      w=900)
        right = ''
        if cth is not None:
            g = cth[(cth['sample'] == 'L15 disk') & (cth['pair'] == 'vert')]
            P = sd.Plot(700, 520, x=(0, 180, 'lin'), y=(0, max(g['per_day'].max() * 1.15, 1), 'lin'),
                        xlabel='opening angle θ [°]', ylabel='per day / 5°', title='vertical pair, no veto')
            P.xticks([(v, str(v)) for v in [0, 45, 90, 135, 180]])
            mx = g['per_day'].max()
            P.yticks([(v, f'{v / 1000:.0f}k') for v in range(0, int(mx * 1.15), 5000 if mx > 10000 else 1000)])
            for _, r in g.iterrows():
                P.vbar(r['th_lo'] + 2.5, r['per_day'], 12, sd.GREY, tip=f'θ {r["th_lo"]:.0f}–{r["th_hi"]:.0f}°: {r["per_day"]:,.0f} / day')
            P.vline(140, sd.RED, label='X17')
            right = P.svg('vertical pair cosmic angles')
        body = (sd.title('The old cosmic sample missed the inclined muons: ×57 too few for side arms',
                         'Left: coincidences at the table level. Right: what a vertical pair records, the MEG II "140° peak"')
                + sd.row(left, right, gap=44))
        D.slide('cosmics', body, '''L4 started every muon on a 3 × 3 m plane 1.5 m above the target: a muon more than ~45° off the
zenith never reaches the set-up's centre. L15 (new option --cosmic-disk 900) starts each muon on a 90 cm disk normal to its
own direction: every zenith angle up to 89°, cos²θ intensity, 1 cm⁻² min⁻¹ through a horizontal surface. Same Cu-hemisphere
geometry, all four arms, cut to pairs. The vertical pair's coincidences pile up at 125–160°, the peak the MEG II members'
2026 study found in ATOMKI-type spectrometers (arXiv:2609.18383).''', short='Cosmics')

    # ---- 7 cosmics by veto
    rowsv = []
    for pair, gl in GEOM:
        for lv in (TRG, PNT, PNT1, REF):
            x = get(rs, pair, 'LNL calibrated', lv)
            if x is None:
                continue
            v = float(x['Bcos_win'])
            n = int(x['n_mc_cos_win']) if not math.isnan(x['n_mc_cos_win']) else 0
            rowsv.append((f'{gl} · {LEVLAB[lv]}', max(v, 0.3), sd.BLUE if pair == 'horiz' else sd.ORANGE,
                          f'{v:.1f} cosmics / day in the signal window ({n} MC events)' + (' (0: drawn at 0.3)' if v <= 0 else '')))
    beam = get(rs, 'horiz', 'LNL calibrated', REF)
    body = (sd.title('Pointing removes 97–99 % of the cosmics, the time of flight the rest',
                     'Cosmics per day in the signal window (125–160°, |y| < 0.6, E_sum window), liquid working')
            + sd.row(sd.hbars(rowsv, 3e4, width=560, log=True, vmin=0.3, label_w=420, fmt=lambda v: f'{v:,.1f}', size=24),
                     sd.col(sd.callout(f'Beam background in the same window: ~{beam["Bbeam_win"]:.0f} / day.' if beam is not None else '', sd.INK),
                            sd.callout('The vertical pair is where a veto failure would show: test it there, on cosmics, before the beam.', sd.ORANGE),
                            w=440), gap=40))
    D.slide('veto', body, '''Levels: no veto = the E_sum window only; pointing = both Micromegas segments point back to the spot
within D (90 % of X17 segments) with the muons' segments at the bench's 3°, plus a 20° collinearity veto; + TOF = arm-to-arm
time of flight at σ_t 1 ns or 0.6 ns (measured on n_TOF beam-off cosmics: 0.52–0.64 ns per arm). Counts with 0–2 MC events are single events in ~5 live days
of L15.''', short='Vetoes')

    # ---- 8 rotated arms
    if ta is not None:
        g = ta[(ta['resp'] == 'LNL calibrated') & (ta['level'] == REF)]
        P = sd.Plot(900, 560, x=(130, 190, 'lin'), y=(0.8, 2.6, 'lin'), xlabel='angle between the arm normals Δφ [°]',
                    ylabel='days, relative to opposite arms')
        P.xticks([(v, str(v)) for v in [140, 160, 180]])
        P.yticks([(1, '1.0'), (1.5, '1.5'), (2, '2.0'), (2.5, '2.5')])
        xs, ys, tips = [], [], []
        for _, r in g.iterrows():
            d = 180 if r['dphi'].startswith('180') else float(r['dphi'])
            if r['dphi'] == '180':
                continue
            xs.append(d)
            ys.append(r['days_factor'])
            tips.append(f'Δφ {d:.0f}°: X17 ×{r["S_ratio"]:.2f}, IPC ×{r["B_ratio"]:.2f} → days ×{r["days_factor"]:.2f}')
        P.line(xs, ys, sd.BLUE, tips=tips)
        P.text(150, 2.35, 'turning the arms in adds IPC faster than X17', 24, sd.INK, 'start', 600)
        acc = [('180° (4-arm tables)', 1.42, sd.GREY, 'opposite pair of the L11 four-arm X17 sample'),
               ('180° (2 arms built)', 1.45, sd.BLUE, 'L16, 5×10⁵ X17 m16.8'),
               ('160°', 1.39, sd.BLUE, 'L16, 5×10⁵ X17 m16.8'), ('140°', 1.06, sd.BLUE, 'L16, 5×10⁵ X17 m16.8')]
        right = sd.col(sd.p('Two-arm X17 acceptance', 26, weight=600),
                       sd.hbars(acc, 1.6, width=360, label_w=260, fmt=lambda v: f'{v:.2f} %', size=24),
                       sd.p('Opposite arms already see 140° pairs: each arm spans ±40° along the beam.', 24, sd.MUT), w=700)
        body = (sd.title('Turning the arms toward 140° costs time: keep them opposite',
                         'Run L16: two arms built, tilted by (180° − Δφ)/2 each; X17 and 18.15 MeV IPC, liquid working, ref. veto')
                + sd.row(P.svg('rotated arms'), right, gap=48))
        D.slide('rot', body, '''Opposite arms already accept 140° pairs: each arm spans ±40° along the beam, and the opening can lie
along the beam. Two-arm X17 acceptance: 1.45 % (Δφ 180°, two arms built; 1.42 % from the four-arm tables), 1.39 % (160°),
1.06 % (140°). Days scaled as counting: IPC ratio / X17 ratio², the IPC mixed as the opposite pair's E1/M1 in the fit
region. The 15.1 MeV IPC and conversions were not simulated rotated.''', short='Rotation')

    # ---- 9 run plan
    steps = [dict(label='Before the beam', sub='vertical pair · ≥ 3 nights of cosmics: σ_t, MIP gains, every veto', color=sd.ORANGE),
             dict(label='Day 1 · 1.10 MeV', sub='roll to horizontal · current scan · rates, live time, occupancy', color=sd.BLUE),
             dict(label='Day 2 · 0.441 MeV', sub='resonance · 17.64 MeV M1 IPC: rate, θ shape, energy scale', color=sd.GOLD),
             dict(label='Days 3–7 · 1.10 MeV', sub='X17 data · daily yield check · E1/M1 mix', color=sd.BLUE),
             dict(label='Day 8', sub='½ day adjacent (EPC, small-angle IPC) · contingency', color=sd.GREEN)]
    body = (sd.title('The plan: test the veto without beam, calibrate in a day, then five days of X17 data',
                     'Two opposite arms; the roll between vertical and horizontal is the only reconfiguration')
            + sd.flow(steps, size=26)
            + sd.row(sd.card(sd.p('Bring the liquid cells', 28, weight=600) + sd.p('×3 in days; even as at n_TOF they beat none.', 24, sd.MUT)),
                     sd.card(sd.p('σ_t with the LNL readout', 28, weight=600) + sd.p('0.6 ns per arm measured with the n_TOF readout; check it with the LNL digitisers.', 24, sd.MUT)),
                     sd.card(sd.p('Thin film, daily yield', 28, weight=600) + sd.p('10–12 µm Li against LiOH; a γ monitor (ask LNL).', 24, sd.MUT)), gap=32))
    D.slide('plan', body, '''Why horizontal for the beam days: with the built Cu hemisphere the horizontal pair needs ×1.6 fewer days than
the vertical one even with working vetoes (cosmics are a large share of its background), and if the vetoes disappoint it sees
~10× fewer cosmics. Why vertical before the beam: cosmics need no beam, and the
vertical pair records them at full strength, including the 140° peak MEG II pointed at; a few nights measure the arm-to-arm
time of flight with ~10⁵ crossing muons per day. Why 441 keV for one day: ~140 selected pairs above 90° per day in the opposite
pair with the hemisphere, an ~8 % check of the absolute IPC rate and the angular shape against Geant4, no anomaly expected. Why adjacent at the
end: the external conversions in the Cu wall are the least-known background; adjacent arms see them at 25–90° at several
thousand per day.''', short='Plan')

    # ---- 10 closing
    end = (sd.kicker('What this does not rule out')
           + sd.p('The numbers are as good as the as-built Monte Carlo of the Cu hemisphere', 52, sd.DINK, 600)
           + sd.row(sd.col(sd.p('Not covered', 30, sd.DINK, 600),
                           sd.p('· the IPC shape beyond the fit’s floating 2 % + 1 %<br>· a two-arm simulation of the lighter Al end piece<br>'
                                '· σ_t with the LNL digitisers (0.6 ns with n_TOF’s)<br>· air showers (several particles at once)', 26, sd.DMUT)),
                    sd.col(sd.p('Open decisions', 30, sd.DINK, 600),
                           sd.p('· a lighter Al end piece for slot 1 (T1, R10)<br>· bring the two liquid cells (S5)<br>· a stand that rolls 90° about the beam<br>'
                                '· AN2000 for the 441 keV day<br>· a γ-yield monitor from LNL', 26, sd.DMUT)), gap=80))
    D.slide('end', end, '', dark=True, short='Limits')
    D.write(a.out, note_meta=dict(title='LNL two-arm run: what 8 days can show',
                                  summary='Geant4 two-arm study for the slot-1 LNL feasibility run: reach by geometry and stack, '
                                          'cosmics from every zenith angle, rotated arms, and the 8-day plan.',
                                  tags='lnl, x17, simulation', date='2026-11-19'))
    print('wrote', a.out)


if __name__ == '__main__':
    main()
