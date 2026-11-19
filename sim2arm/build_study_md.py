#!/usr/bin/env python3
"""
build_study_md.py -- fills the result sections of TWO_ARM_STUDY.md (§0, §2, §3, §4.3, §6) from the CSVs, between the
<!-- RESULTS --> and the section markers, so the numbers in the text are the numbers in out/.

    python3 sim2arm/build_study_md.py [--tag _pass3]
"""
from __future__ import annotations

import argparse
import io
import math
import re
import subprocess
import sys
from contextlib import redirect_stdout
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / 'out'
sys.path.insert(0, str(HERE))
import report_tables as RT   # noqa: E402

REF, PNT, PNT1, TRG = RT.REF, RT.PNT, RT.PNT1, RT.TRG
Z90, MEG_A = 1.2816, 1.2e-5 / 5.8e-6


def z(d, T=5.0):
    return 3 * math.sqrt(T / d)


def P(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def cap(fn, *a, **k):
    b = io.StringIO()
    with redirect_stdout(b):
        fn(*a, **k)
    return b.getvalue()


def adj_text(tag):
    f = OUT / f'summary_rates{tag}.csv'
    if not f.exists():
        f = OUT / 'summary_rates_pass1.csv'
    rt = pd.read_csv(f)
    out = ['', '| E_p | component | adjacent, 25–90° | opposite (horizontal), all angles |', '|---|---|---|---|']
    for ep, lab in ((1100.0, '1.10 MeV'), (441.0, '0.441 MeV')):
        for comp, cl in (('E1', 'E1 IPC'), ('M1', 'M1 IPC'), ('epc', 'external conversions'), ('g1', '15.1 MeV IPC')):
            def v(p, col):
                m = rt[(rt['pair'] == p) & (rt['Ep_keV'] == ep) & (rt['level'] == REF) & (rt['resp'] == 'LNL calibrated')
                       & (rt['ewin'] == 'win') & (rt['comp'] == comp)]
                return float(m.iloc[0][col]) if not m.empty else float('nan')
            out.append(f'| {lab} | {cl} | {v("adj", "25-90"):.0f} | {v("horiz", "all"):.0f} |')
    out.append('')
    out.append('(pairs per day, pointing + 0.6 ns TOF, liquid working, E_sum window, 20 µm.) Half a day of adjacent running '
               'gives ~1,000 conversion pairs at 25–90°: the external-conversion model of the Cu wall, which carries ~20 % '
               'of the background in the X17 fit and rests on a few hundred MC events, gets a direct measurement. It also '
               'checks the opening-angle response away from the X17 window and the trigger with two arms at 90°, which '
               'is half the pair combinations of the four-arm experiment.')
    return '\n'.join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tag', default='_pass3')
    a = ap.parse_args()
    d20 = pd.read_csv(OUT / f'summary_reach{a.tag}.csv')
    f11 = OUT / f'summary_reach{a.tag}li11.csv'
    d11 = pd.read_csv(f11) if f11.exists() else None
    base, film = (d11, '11 µm') if d11 is not None else (d20, '20 µm')
    g = RT.g
    hw, hn, ho = (g(base, 'horiz', r, REF) for r in ('LNL calibrated', 'n_TOF as is', 'LNL calibrated, LS off'))
    vw = g(base, 'vert', 'LNL calibrated', REF)
    vwp, hwp = g(base, 'vert', 'LNL calibrated', PNT), g(base, 'horiz', 'LNL calibrated', PNT)
    h20 = g(d20, 'horiz', 'LNL calibrated', REF)
    a20 = g(d20, 'all', 'LNL calibrated', REF)
    dd = d20.pivot_table(index=['pair', 'resp'], columns='level', values='days3_direct')

    def dir_(p, r, lv):
        try:
            return dd.loc[(p, r), lv]
        except KeyError:
            return float('nan')
    cr = pd.read_csv(OUT / 'cosmic_rates.csv') if (OUT / 'cosmic_rates.csv').exists() else None

    s = []
    s.append(f'''## 0. Bottom line (2026-11-19, Geant4)

- **Do go for a measurement, as the second half of the run, and do not promise one.** Five days at 1.10 MeV with two
  opposite arms give an expected 90 % CL limit of **{Z90 / z(hw["days3"]):.2f} × R(ATOMKI)** with the liquid cells working,
  **{Z90 / z(hn["days3"]):.2f} ×** with the liquid as it ran at n_TOF and **{Z90 / z(ho["days3"]):.2f} ×** without it ({film} Li,
  horizontal pair, MM pointing + 0.6 ns TOF). MEG II's published limit is 2.07 × R(ATOMKI): every case beats it on
  statistics, the two with liquid cells reach the ATOMKI ratio or near it.
- **We would not see ATOMKI's signal at 3σ.** If it is there, the expected significance is {z(hn["days3"]):.1f}–{z(hw["days3"]):.1f}σ
  (liquid as at n_TOF … working): a 3σ excess with probability {100 * (1 - P(3 - z(hn["days3"]))):.0f}–{100 * (1 - P(3 - z(hw["days3"]))):.0f} %, a 2σ hint
  with {100 * (1 - P(2 - z(hn["days3"]))):.0f}–{100 * (1 - P(2 - z(hw["days3"]))):.0f} %. Days to 3σ: {hw["days3"]:.0f} ({hw["days3_lo"]:.0f}–{hw["days3_hi"]:.0f}) and {hn["days3"]:.0f} ({hn["days3_lo"]:.0f}–{hn["days3_hi"]:.0f}).
- **Two arms cost ×{h20["days3"] / a20["days3"]:.1f} in days against four** (20 µm, liquid working: {h20["days3"]:.0f} vs {a20["days3"]:.0f} d), a little worse than
  the ×2 the page assumed. The 10–12 µm film the target review asks for costs a further ×{hw["days3"] / h20["days3"]:.1f} (§3).
- **The liquid cells are the biggest lever: without them the days go up ×{ho["days3"] / hw["days3"]:.1f}.** Bring them (task S5).
- **Geometry: opposite arms, horizontal for the beam.**
  - With pointing + 0.6 ns TOF the vertical and horizontal pairs are equal within the MC ({vw["days3"]:.0f} vs {hw["days3"]:.0f} d).
  - Without sub-ns timing the horizontal pair keeps its reach ({hwp["days3"]:.0f} d with pointing only) and the vertical pair loses
    it ({vwp["days3"]:.0f} d): a horizontal muon has to cross both side arms, and after pointing the horizontal pair sees ~10× fewer
    cosmics in the window than the vertical one.
  - Turning the arms toward the 140° X17 angle costs ×1.1 (Δφ = 160°) to ×2–2.5 (140°) in days (§5). Adjacent ("perpendicular")
    arms see 25–120° and no X17; they are a background diagnostic (§6).
- **Test the veto where it is hardest, without beam:** a few nights of cosmics with the arms **vertical** during installation
  record the MEG II "140° peak" at full strength (~10⁴ cosmic pairs/day in the E_sum window, ~250 after pointing, ~1 after
  0.6 ns TOF) and measure σ_t, the muon segment angle and the arm gains (§7.2). Then roll to horizontal for the beam.
- **The 441 keV calibration is ~10× smaller than the proposal says:** ~600 selected pairs per day above 90° (two arms), not
  6–12 × 10³. One day is enough for a ~5 % check of the IPC rate and shape (§2).
- **The old cosmic sample (L4) missed the inclined muons**: it gave a horizontal pair 110 coincidences/day, the new one (L15,
  every zenith angle) ~6,000 (§4).
''')

    s.append('@@S23')
    s.append('''## 2. Rates per day

From `out/summary_rates*.csv` (the reference event tables: the Cu hemisphere's own X17, IPC and ⁸Be-γ Monte Carlo,
weighted with its film yields; cosmics L15). The signal window is 125–160°, |y| < 0.6 and the response's E_sum window.
''')
    s.append(cap(RT.rates_table, d20))
    sp = cap(RT.spectra_table, a.tag)
    if sp.strip():
        s.append(sp)
    s.append('''
- The 1.10 MeV background in the opposite pair is mostly the **E1 IPC** of direct capture, then M1 IPC, 15.1 MeV IPC and
  external conversions.
- At 441 keV the selected pairs are M1 IPC of the 17.64 MeV line plus conversions; X17 is not expected there.
- Adjacent arms see the small-angle IPC and the conversions at several thousand per day: a fast check of the material model.
''')

    s.append('''## 3. Reach: days to 3σ at R(ATOMKI), and what five days give

Reference fit (FEASIBILITY_SIM §19), Cu hemisphere as built, 1 µA, 1.10 MeV, m_X = 16.8 MeV, live 0.95. Central value =
geometric mean of the two MC-safe estimators, range in brackets.
''')
    s.append(cap(RT.days_table, d20, '20 µm Li (as simulated)'))
    if d11 is not None:
        s.append(cap(RT.days_table, d11, '11 µm Li (the review’s 10–12 µm)', pairs=[p for p in RT.PAIRS if p[0] != 'adj']))
    s.append('\n**The vetoes compared with one estimator** (direct + floor, 20 µm, days to 3σ):\n')
    s.append('| pair | stack | no veto | pointing | pointing + 1 ns TOF | pointing + 0.6 ns TOF |\n|---|---|---|---|---|---|')
    for p, pl in (('horiz', 'horizontal'), ('vert', 'vertical'), ('all', 'four arms')):
        for r, rl in RT.RESP:
            s.append(f'| {pl} | {rl} | ' + ' | '.join(f'{dir_(p, r, lv):.0f}' for lv in (TRG, PNT, PNT1, REF)) + ' |')
    s.append(cap(RT.limit_table, [('11 µm', d11), ('20 µm', d20)] if d11 is not None else [('20 µm', d20)]))
    s.append(f'''
- **Liquid cells:** working {dir_('horiz', 'LNL calibrated', REF):.0f} d, as at n_TOF {dir_('horiz', 'n_TOF as is', REF):.0f} d, none
  {dir_('horiz', 'LNL calibrated, LS off', REF):.0f} d (horizontal, direct). Without them E_sum is a SiPM bar plus 2 cm of plastic: the
  signal in the window drops ×6, and the γ₁ (15.1 MeV) pairs are no longer separated.
- **The time of flight matters only for the vertical pair.** Horizontal: {dir_('horiz', 'LNL calibrated', PNT):.0f} d with pointing,
  {dir_('horiz', 'LNL calibrated', REF):.0f} d with 0.6 ns TOF. Vertical: {dir_('vert', 'LNL calibrated', PNT):.0f} d and
  {dir_('vert', 'LNL calibrated', REF):.0f} d. A 1 ns TOF removes only a third of the remaining cosmics; it takes ≲ 0.4 ns.
- **No veto at all** costs the horizontal pair ×{dir_('horiz', 'LNL calibrated', TRG) / dir_('horiz', 'LNL calibrated', PNT):.1f} and
  the vertical pair ×{dir_('vert', 'LNL calibrated', TRG) / dir_('vert', 'LNL calibrated', PNT):.1f}.
- **The film:** 11 µm has ~55 % of the 20 µm yield, so the beam terms fall and the cosmics do not: ×{(hw["days3"] / h20["days3"]):.1f}
  in days for the horizontal pair, more for the vertical one where cosmics are a larger share.
''')

    s.append('@@S43')
    if cr is not None:
        s.append('### 4.3 Cosmics by veto (L15, liquid working, signal window, per day)\n')
        s.append('| pair | no veto | pointing | pointing + 1 ns TOF | pointing + 0.6 ns TOF |\n|---|---|---|---|---|')
        for p, pl in (('horiz', 'horizontal'), ('vert', 'vertical')):
            cells = []
            for lv in (TRG, PNT, PNT1, REF):
                x = g(d20, p, 'LNL calibrated', lv)
                cells.append(f'{x["Bcos_win"]:.1f} ({int(x["n_mc_cos_win"])} MC)' if x is not None else '–')
            s.append(f'| {pl} | ' + ' | '.join(cells) + ' |')
        lv = cr[cr['sample'] == 'L15 disk'].iloc[0]['live_days']
        s.append(f'\nThe fits used L15 chunks 0–3 (400 jobs, 2.45 live days: {g(d20, "vert", "LNL calibrated", TRG)["n_mc_cos_win"]:.0f} '
                 f'MC events in the vertical no-veto window, 76 in the horizontal pointing one); the coincidence tables of §4.1 '
                 f'(`out/cosmic_rates.csv`) use all of it, {lv:.1f} live days. At the levels where cosmics matter the fits have '
                 f'tens to thousands of MC events; with 0.6 ns TOF, 0–7 events: there they are negligible against ~600 beam pairs '
                 f'either way. The vertical and four-arm cosmic tables drop rows below 40° of opening angle (memory; the fit starts '
                 f'at 90° with 5° smoothing), so the spectra of those two pairs show no cosmics below 40°.\n')

    t = (HERE / 'TWO_ARM_STUDY.template.md').read_text()
    full = '\n'.join(s)
    s0, rest = full.split('@@S23', 1)
    s23, s43 = rest.split('@@S43', 1)
    parts = {'<!-- RESULTS -->': s0, '<!-- SECTIONS 2-3: reach and rates (filled from pass 2) -->': s23,
             '<!-- 4.3 numbers by veto, from pass 2 -->': s43,
             '<!-- 6 numbers from pass 2 spectra -->': adj_text(a.tag),
             '<!-- SECTION 7 -->': (HERE / 'section7_plan.md').read_text()}
    for k, v in parts.items():
        assert k in t, k
        t = t.replace(k, v)
    (HERE / 'TWO_ARM_STUDY.md').write_text(t)
    print('TWO_ARM_STUDY.md updated')


if __name__ == '__main__':
    main()
