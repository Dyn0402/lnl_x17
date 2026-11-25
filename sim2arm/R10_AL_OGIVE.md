# R10: the Al ogive + Cu liner in two arms, from its Geant4 tables

Written 2026-11-25 (desktop), in two passes on the same day. The first pass (morning) used the holder's small run L12
alone and was marked interim. The second pass (afternoon) added the ×30 run L13, fetched from EOS, and settles the number.
**The numbers of record are those of the second pass (L12 + L13), in §0 and §3.** The first-pass numbers are kept in §5
as the history.

Task R10 of `planning/plan.py`: replace the scaled estimate for the lighter target holder by a number from the simulation.
Nothing in `planning/`, `proposal/`, `slot1_feasibility/` or the site was changed here.

Every number below is marked as **simulation** (the reference fit run on Geant4 tables) or **estimate** (a scaling).

## 0. Bottom line

- **The two-arm reach of the Al ogive + Cu liner is now a simulation on ×30 tables.** We ran the reference fit of
  `two_arm_nd.py` on the holder's own four-arm Geant4 tables (config `ogAl300cu12r8m4`, runs L12 + L13), cut to the
  horizontal pair, with the pass-4 settings. For the 11 µm Li film and the reference cosmic veto (Micromegas pointing +
  0.6 ns time of flight), the days to 3σ at R(ATOMKI) and the expected 90 % CL limit after five days are (simulation):

  | liquid cells | days to 3σ, two arms: central (lo–hi) | four arms, same fit | R₉₀(5 d) / R(ATOMKI), two arms | scaled estimate it replaces | simulation / estimate (days) | L12 alone (first pass) |
  |---|---|---|---|---|---|---|
  | working | **21.1** (20.4–21.8) | 11.6 d | **0.88** (0.86–0.89) | 10.4 d, 0.62 | ×2.03 | 19.1 d, 0.84 |
  | as at n_TOF | **38.8** (33.4–44.9) | 22.6 d | **1.19** (1.10–1.28) | 18.2 d, 0.81 | ×2.13 | 31.6 d, 1.07 |
  | none | **78.7** (61.5–101) | 44.2 d | **1.70** (1.50–1.92) | 58.8 d, 1.46 | ×1.34 | 81.1 d, 1.72 |

  For the 20 µm film the same three rows are 13.5, 24.4 and 53.3 d, which is 0.70, 0.94 and 1.40 × R(ATOMKI) (§3.2).
- **The scaled estimate was optimistic by ×1.3–2.1 in days (×1.2–1.5 in the limit).**
- **"A lighter aluminium holder would give an expected limit of 0.6–0.8 × R(ATOMKI) in five days" does not hold.** For
  the 11 µm film the simulation gives 0.88 × with the liquid cells working and 1.19 × with the liquid as it ran at n_TOF.
  We suggest "an expected limit of about R(ATOMKI) in five days (0.9–1.2 ×)". Without liquid cells the limit is 1.7 ×.
  Even a 20 µm film gives 0.70–0.94 ×.
- **The result is final as far as the Monte Carlo statistics go.** The horizontal pair now keeps 1,051 M1, 4,856 E1 and
  4,446 15.1 MeV-line Monte Carlo events in the fit region (43, 122 and 126 with L12 alone), and 1,913 beam-background
  events in the signal window (58 with L12 alone). This is the standard of passes 3 and 4. With the liquid working, the
  two estimators agree within 7 % and the raw fit agrees with the floored fit within 3 %. §4.4 lists what remains
  uncertain: the range of the two estimators for the other liquid states, and the design assumptions of a holder that is
  not built.
- **The first pass was close for two arms and too fast for four arms.** L12 alone gave ×0.81–1.03 of the ×30 days for
  the horizontal pair and ×0.63–0.72 for the four arms. This is what the thin-table test on the Cu ogive had indicated
  (§5.2).
- **A side finding on four arms.** The four-arm days of this holder in FEASIBILITY_SIM §19.3 and in
  `planning/two_arm_estimates.FOUR_ARM` (4.5 and 8.5 d) were made on the thin L12 tables with a 0.3 ns time of flight and
  the L4 cosmics. With the ×30 tables and the pass-4 settings the four arms give 6.9 and 13.1 d (20 µm). This is the
  main reason the scaled estimate was low (§6).

## 1. What was run

### 1.1 The holder and its tables

The lighter holder is the "Al ogive + Cu liner, Li mask r ≤ 4" row of FEASIBILITY_SIM §19.3 (x17_facility_search
`lnl/FEASIBILITY_SIM.md`). Its Geant4 configuration is `ogAl300cu12r8m4` (x17_facility_search
`lnl/target/shapes/shapes_geant.py`, `lnl/target/CU_LINER.md` §7). It is an Al ogive with a 300 µm wall, the same outline
as the Cu ogive (Ø50 × 63 mm), with a 12 µm Cu liner where the inner radius is at most 8 mm. The Li is evaporated through
a mask of radius 4 mm.

Two runs of this holder exist. Both have four arms as built, like the runs used in passes 3 and 4, so each arm pair can
be cut from the same tables.

- **Run L12** (4 Nov) is small: 5 × 100,000 pairs per IPC sample and for X17, and 10 × 2,000,000 γ for the external
  conversions. It was on this desktop already.
- **Run L13** (10 Nov) is the ×30 background run: 150 × 100,000 pairs for the M1 and E1 IPC at 18.15 and 15.1 MeV, and
  150 × 2,000,000 γ. It has no X17 sample. Its merged tables were on EOS only. We fetched the five as-built tables on
  25 Nov (§2.3) into `/media/ucla/work/x17_facility_search/lnl_sel/L13_*_ogAl300cu12r8m4_asb_sel.npz`, next to the L12
  tables.

### 1.2 The change to the code

`sim2arm/two_arm_nd.py` got two additive changes. The defaults and every existing output are unchanged.

1. A new entry beside `ogCu200` and `dome300`: `SN.RUNS['ogAl300cu12r8m4'] = ['L12', 'L13']`. The configuration is selected
   with `TA_CFG=ogAl300cu12r8m4`. A run whose tables are not on the disk is skipped by the reference fit.
2. An environment variable `TA_RUNS`. `TA_RUNS=L12` makes the fit use the tables of run L12 alone for the configuration
   given by `TA_CFG`. It is used for the first-pass tags and for the thin-table test of §5.2.

Two new scripts hold the commands and the tables: `sim2arm/run_r10.sh` (the fits) and `sim2arm/r10_al_ogive.py` (the
summaries and the tables of this note).

### 1.3 Settings

The settings are those of pass 4 (`run_pass.sh _pass4`), with only the configuration changed:

- the reference fit of FEASIBILITY_SIM §19 at E_p = 1.10 MeV, 1 µA, live fraction 0.95, m_X = 16.8 MeV;
- the L15 cosmics (every zenith angle);
- the level `MM 15° + TOF` with the measured σ_t = 0.6 ns (the reference), and `MM 15° point, μ 3°` (pointing only);
- the three liquid states: `LNL calibrated` (liquid working), `n_TOF as is` (liquid as at n_TOF), `LNL calibrated, LS off`
  (no liquid);
- the yields of an 11 µm film (`LI_UG=587`) and of the simulated 20 µm film. The Geant4 events are those of the 20 µm run
  in both cases;
- the pairs `horiz` (arms 0 + 1) and `all` (four arms);
- both estimators, `direct` (the holder's own tables with the one-event floor) and `transplant`. As in passes 1–4, the
  central value is the geometric mean of the two estimators and the range is the two estimators.

The output tags are new, and no file of passes 1–4 was written:

| tag | tables | film |
|---|---|---|
| `_pass5al_l13li11` | L12 + L13 | 11 µm |
| `_pass5al_l13` | L12 + L13 | 20 µm |
| `_pass5alli11` | L12 alone (first pass) | 11 µm |
| `_pass5al` | L12 alone (first pass) | 20 µm |

These are the names that `planning/two_arm_estimates.AL_TAGS` looks for (`_pass5al_l13` first, then `_pass5al`, with the
film suffix `li11`). We did not run or edit the planning script.

### 1.4 Not run

The vertical pair, the `trigger` level and the 1 ns time-of-flight level were not run. They are step 5 of `run_r10.sh`
(about 30 minutes). The spectra task was not run either.

## 2. Checks of the set-up

### 2.1 Closure: the Cu hemisphere through the same code path

We ran the hemisphere (`dome300`, horizontal pair, liquid working, 11 µm, reference level) again with the edited
`two_arm_nd.py` and a fresh cache (tag `_pass5al_closure`). The result is identical to pass 4 (simulation):

| estimator | pass 4 | this run |
|---|---|---|
| direct, floor | 189.465 d | 189.465 d |
| transplant | 120.311 d | 120.311 d |
| central | 151.0 d | 151.0 d |

The Monte Carlo counts and the rates per day are identical too. The new configuration is therefore the only difference
between pass 4 and the tables of §3.

### 2.2 The four arms with the settings of FEASIBILITY_SIM §19.3

FEASIBILITY_SIM §19.3 gives 4.5 (3.6–5.5) d and 8.5 (7–10) d for the four arms of this holder. Those numbers used run L12
alone, a 0.3 ns time of flight, the L4 cosmics and the 20 µm film. We ran the new configuration with those settings
(`LNL_TOF_SIGMA_NS=0.3 COSMICS=L4`, L12 alone, tag `_pass5al_old`). The result is (simulation):

| four arms, 20 µm, 0.3 ns, L4 cosmics, L12 alone | direct | transplant | central | FEASIBILITY_SIM §19.3 |
|---|---|---|---|---|
| liquid working | 4.41 d | 4.89 d | 4.64 d | 4.5 d (`nd_reach.csv`: 4.19, 4.65) |
| liquid as at n_TOF | 7.87 d | 10.6 d | 9.15 d | 8.5 d |

The 5 % difference to `nd_reach.csv` is the live fraction (0.95 here, 0.999 there). The new entry in `two_arm_nd.py`
therefore reads the same tables and yields as the fit behind §19.3.

### 2.3 The L13 tables: complete on EOS, and consistent with L12

Before fetching, we checked run L13 on EOS (read-only, through `ssh lxplus`).

- The five merged as-built tables of this holder are in `/eos/experiment/ntof/data/x17/lnl/target/sel_l13/`, merged on
  11 Nov between 15:24 and 15:37. The set of samples is the same as for the Cu ogive: M1 and E1 IPC at 18.15 and 15.1 MeV,
  and the ⁸Be γ lines. (The big-plastics tables and the γ singles table of this holder are there too. They are not needed
  here and were not fetched.)
- Each sample has 150 simulation files, 150 reduced parts and 150 timing parts, as its `RUN_INFO.txt` says
  (150 × 100,000 pairs, 150 × 2,000,000 γ). The Cu ogive's L13 has the same counts. No part is newer than the merged
  table, and there is no `bad/` directory.
- No simulation file is truncated: the smallest ROOT file of each sample is within 1.5 % of the median size. (One L13 job
  of the Cu ogive had a truncated file on 12 Nov, which is why we looked.)
- After the copy, the md5 sums of the five local files equal those on EOS. The tables hold 15,000,000 generated pairs
  per IPC sample and 300,000,000 generated γ.

The table below compares the two-arm rows per generated event in L13 and in L12. The two runs agree within the
statistics of L12 (the largest difference is 2.3σ, for the M1 15.1 MeV sample in the horizontal pair).

| sample | L12: two-arm rows per 1,000 generated | L13: two-arm rows per 1,000 generated | L12: horizontal rows per 10⁶ generated | L13: horizontal rows per 10⁶ generated |
|---|---|---|---|---|
| M1 IPC 18.15 | 3.67 ± 0.09 | 3.61 ± 0.02 | 140 ± 17 | 135 ± 3 |
| E1 IPC 18.15 | 5.93 ± 0.11 | 5.95 ± 0.02 | 570 ± 34 | 629 ± 6 |
| M1 IPC 15.1 | 3.16 ± 0.08 | 3.19 ± 0.01 | 80 ± 13 | 109 ± 3 |
| E1 IPC 15.1 | 5.19 ± 0.10 | 5.21 ± 0.02 | 516 ± 32 | 548 ± 6 |
| ⁸Be γ lines | 0.0023 ± 0.0003 | 0.0023 ± 0.0001 | 0.10 ± 0.07 | 0.08 ± 0.02 |

## 3. Results (L12 + L13)

All numbers in this section are **simulation** on the ×30 tables. The scaled estimate is the row that
`planning/out/two_arm_reach.csv` held on the morning of 25 Nov for the same film, liquid state and veto (the four-arm
§19.3 days times the Cu ogive's two-arm / four-arm ratio). The last two columns give the Cu hemisphere of pass 4 and the
first pass (L12 alone) for comparison.

R₉₀ is the expected 90 % CL upper limit after five days with no signal, R₉₀ = 1.2816 / (3 √(5 / d₃)) × R(ATOMKI), where d₃
is the days to 3σ (`planning/two_arm_estimates.r90`).

### 3.1 The 11 µm film (`out/summary_reach_pass5al_l13li11.csv`)

| liquid | cosmic veto | two arms (horizontal pair): days to 3σ, central (lo–hi) | direct, transplant | R₉₀(5 d) / R(ATOMKI), two arms (range) | four arms, same fit: days (lo–hi) | R₉₀(5 d), four arms | scaled estimate: days, R₉₀ | simulation / estimate: days, R₉₀ | Cu hemisphere (pass 4): days, R₉₀ | L12 alone, two arms: days (direct, transplant), R₉₀ |
|---|---|---|---|---|---|---|---|---|---|---|
| liquid working | MM pointing + 0.6 ns TOF | **21.1** (20.4–21.8) | 21.8, 20.4 | **0.88** (0.86–0.89) | 11.6 (11.2–12) | 0.65 | 10.4, 0.62 | ×2.03, ×1.42 | 151, 2.35 | 19.1 (21.1, 17.3), 0.84 |
| liquid working | MM pointing only | **18.7** (18.7–18.8) | 18.7, 18.8 | **0.83** (0.83–0.83) | 10.1 (9.57–10.8) | 0.61 | 9.4, 0.59 | ×1.99, ×1.40 | 132, 2.20 | 17.4 (17.7, 17.2), 0.80 |
| liquid as at n_TOF | MM pointing + 0.6 ns TOF | **38.8** (33.4–44.9) | 33.4, 44.9 | **1.19** (1.10–1.28) | 22.6 (21.9–23.4) | 0.91 | 18.2, 0.81 | ×2.13, ×1.47 | 263, 3.10 | 31.6 (26, 38.5), 1.07 |
| liquid as at n_TOF | MM pointing only | **36.9** (30.4–44.8) | 30.4, 44.8 | **1.16** (1.05–1.28) | 21.3 (20.5–22.1) | 0.88 | 15.9, 0.76 | ×2.32, ×1.53 | 226, 2.87 | 32.3 (28, 37.3), 1.09 |
| no liquid | MM pointing + 0.6 ns TOF | **78.7** (61.5–101) | 61.5, 101 | **1.70** (1.50–1.92) | 44.2 (42.7–45.8) | 1.27 | 58.8, 1.46 | ×1.34, ×1.16 | 511, 4.32 | 81.1 (79.3, 82.9), 1.72 |
| no liquid | MM pointing only | **75.9** (56.3–102) | 56.3, 102 | **1.66** (1.43–1.93) | 49.1 (43.3–55.6) | 1.34 | 57.8, 1.45 | ×1.31, ×1.15 | 472, 4.15 | 79.7 (75.1, 84.6), 1.71 |

### 3.2 The 20 µm film (`out/summary_reach_pass5al_l13.csv`)

| liquid | cosmic veto | two arms (horizontal pair): days to 3σ, central (lo–hi) | direct, transplant | R₉₀(5 d) / R(ATOMKI), two arms (range) | four arms, same fit: days (lo–hi) | R₉₀(5 d), four arms | scaled estimate: days, R₉₀ | simulation / estimate: days, R₉₀ | Cu hemisphere (pass 4): days, R₉₀ | L12 alone, two arms: days (direct, transplant), R₉₀ |
|---|---|---|---|---|---|---|---|---|---|---|
| liquid working | MM pointing + 0.6 ns TOF | **13.5** (13.0–14.0) | 14.0, 13.0 | **0.70** (0.69–0.71) | 6.89 (6.62–7.17) | 0.50 | 7.5, 0.52 | ×1.80, ×1.35 | 86.5, 1.78 | 12.0 (13.4, 10.7), 0.66 |
| liquid working | MM pointing only | **12.0** (12.0–12.0) | 12.0, 12.0 | **0.66** (0.66–0.66) | 6.24 (5.88–6.63) | 0.48 | 7.0, 0.50 | ×1.71, ×1.32 | 77.6, 1.68 | 11.0 (10.9, 11.1), 0.63 |
| liquid as at n_TOF | MM pointing + 0.6 ns TOF | **24.4** (21.2–28.0) | 21.2, 28.0 | **0.94** (0.88–1.01) | 13.1 (12.8–13.5) | 0.69 | 13.5, 0.70 | ×1.81, ×1.35 | 151, 2.35 | 19.5 (16.6, 22.9), 0.84 |
| liquid as at n_TOF | MM pointing only | **23.7** (19.8–28.4) | 19.8, 28.4 | **0.93** (0.85–1.02) | 13.1 (12.2–14.0) | 0.69 | 11.6, 0.65 | ×2.04, ×1.43 | 130, 2.18 | 20.1 (17.7, 22.9), 0.86 |
| no liquid | MM pointing + 0.6 ns TOF | **53.3** (40.5–70.2) | 40.5, 70.2 | **1.40** (1.22–1.60) | 31.2 (29.2–33.4) | 1.07 | 43.1, 1.25 | ×1.24, ×1.12 | 293, 3.27 | 55.5 (53.6, 57.5), 1.42 |
| no liquid | MM pointing only | **51.2** (37.4–70.1) | 37.4, 70.1 | **1.37** (1.17–1.60) | 34.2 (29.2–40.1) | 1.12 | 41.0, 1.22 | ×1.25, ×1.12 | 260, 3.08 | 53.6 (50.9, 56.5), 1.40 |

### 3.3 What the tables show

1. With the Al ogive + Cu liner the horizontal pair is ×7 faster than with the built Cu hemisphere (21.1 d against 151 d,
   11 µm, liquid working). The holder is still the largest lever of the run. The lever is half as large as the scaled
   estimate said (×14.5).
2. The Al ogive + Cu liner is ×0.84 of the Cu ogive of pass 3 in days (21.1 d against 25.2 d; 38.8 d against 43.6 d with
   the liquid as at n_TOF, ×0.89). In two arms the lighter wall therefore gains 10–15 % over the Cu ogive.
3. Two arms take ×1.8 the days of four arms with the liquid working (21.1 d against 11.6 d), ×1.7 with the liquid as at
   n_TOF and ×1.8 without liquid. The four-arm fit sums all pairs, as in pass 4.
4. The 0.6 ns time of flight does not help the horizontal pair. Pointing alone gives 18.7 d against 21.1 d with the
   reference level. Pass 4 shows the same for the hemisphere (132 d against 151 d). The reference level smears the muon
   segments by 15° and keeps more cosmics than the pointing-only level (118 against 76 Monte Carlo events in the signal
   window).
5. The 11 µm film costs ×1.56 in days against the 20 µm film (21.1 d against 13.5 d).

## 4. Monte Carlo statistics (L12 + L13)

### 4.1 Rows in the merged tables (before any selection)

The table below shows the generated events of each sample and the rows whose selected pair is the horizontal pair
(`r10_al_ogive.py raw`).

| sample | Al ogive + Cu liner, L12 + L13: generated / horizontal rows | L12 alone | Cu hemisphere, L10 + L18: generated / horizontal rows | Cu ogive, L11 + L13: generated / horizontal rows |
|---|---|---|---|---|
| X17 16.8 MeV | 500,000 / 8,383 (L12 only) | 500,000 / 8,383 | 3,500,000 / 28,406 | 500,000 / 7,111 |
| M1 IPC 18.15 | 15,500,000 / 2,088 | 500,000 / 70 | 15,500,000 / 2,276 | 15,500,000 / 3,050 |
| E1 IPC 18.15 | 15,500,000 / 9,715 | 500,000 / 285 | 15,500,000 / 6,175 | 15,500,000 / 9,938 |
| M1 IPC 15.1 | 15,500,000 / 1,677 | 500,000 / 40 | 15,500,000 / 1,562 | 15,500,000 / 2,606 |
| E1 IPC 15.1 | 15,500,000 / 8,480 | 500,000 / 258 | 15,500,000 / 4,354 | 15,500,000 / 8,566 |
| ⁸Be γ lines (external conversions) | 320,000,000 / 25 | 20,000,000 / 2 | 320,000,000 / 258 | 320,000,000 / 155 |

The Al ogive has 741 two-arm rows from the ⁸Be γ lines in all pairs together, against 20,363 for the hemisphere and 6,244
for the Cu ogive in tables of the same size. The external conversions are therefore much rarer in the lighter holder.

### 4.2 Monte Carlo events at the reference selection

The table below shows the Monte Carlo events per component for the horizontal pair, liquid working, reference level,
direct tables, 11 µm yields (`out/r10_mcstat_pass5al_l13.csv`; the first pass and the hemisphere are in
`out/r10_mcstat_pass5al.csv`). The fit region is θ ≥ 90° in the E_sum fit range. The signal window is 125–160°, |y| < 0.6
and the E_sum window 13–19 MeV. Each cell gives the Monte Carlo events and, in brackets, the pairs per day.

| component | Al ogive, L12 + L13: fit region | signal window | Al ogive, L12 alone: fit region | signal window | Cu hemisphere, L10 + L18: fit region | signal window |
|---|---|---|---|---|---|---|
| X17 at R(ATOMKI) | 4,531 (33.1) | 1,650 (12.0) | 4,531 (33.1) | 1,650 (12.0) | 12,369 (14.3) | 1,537 (1.77) |
| M1 IPC (18.15, 17.64) | **1,051** (64) | 282 (18) | 43 (75) | 13 (21) | 840 (50) | 91 (5.1) |
| E1 IPC 18.15 | **4,856** (432) | 1,405 (128) | 122 (328) | 39 (92) | 2,459 (213) | 291 (27) |
| 15.1 MeV lines (M1 + E1 IPC) | **4,446** (674) | 226 (34) | 126 (595) | 6 (28) | 1,544 (254) | 10 (1.6) |
| external conversions | 2 (0.15) | 0 (0) | 0 (0) | 0 (0) | 49 (252) | 0 (0) |
| cosmics (L15) | 186 (72) | 118 (46) | 186 (72) | 118 (46) | 186 (72) | 118 (46) |

For the four arms with L12 + L13 the fit region holds 10,684 M1, 27,765 E1, 28,571 15.1 MeV-line and 30
external-conversion events (616, 2,313, 4,282 and 157 pairs per day), and 2,426 cosmic events (938 per day).

- The beam background of the horizontal pair is 1,169 pairs per day in the fit region, carried by 10,355 Monte Carlo
  events. In the signal window it is 180 pairs per day, carried by 1,913 events. The statistical uncertainty of the
  signal-window background is therefore about ±2.5 % (±14 % with L12 alone, which gave 141 per day).
- Every IPC component now has more Monte Carlo events than in the hemisphere tables of pass 4.
- The external conversions are the one component that stays thinly sampled, and they are small. The horizontal pair has
  2 events (0.15 pairs per day). The four arms have 30 events, 157 pairs per day, which is 2.1 % of the four-arm beam
  background. If the horizontal pair had the same share, its external conversions would be about 25 pairs per day
  (estimate), again 2 % of its beam background. CU_LINER §7 found 3 % for this holder with big plastics. The effect on
  the days is at the 2 % level either way.
- The cosmics are the L15 sample of pass 4: 118 Monte Carlo events in the signal window (46 pairs per day). This is the
  same in every two-arm number of this study.
- The X17 sample is that of L12 (L13 has none): 4,531 events in the fit region, which is enough.

### 4.3 The two estimators

| horizontal pair, 11 µm, reference level | direct, floor | direct, raw (no floor) | transplant | direct / transplant |
|---|---|---|---|---|
| liquid working | 21.8 d | 21.2 d | 20.4 d | ×1.07 |
| liquid as at n_TOF | 33.4 d | 32.8 d | 44.9 d | ×0.74 |
| no liquid | 61.5 d | 33.0 d | 101 d | ×0.61 |

- With the liquid working the two estimators agree within 7 %, and the raw fit agrees with the floored fit within 3 %.
  With L12 alone the raw fit gave 0.7 d, the artefact of thin tables (FEASIBILITY_SIM §19.1). That artefact is gone.
- With the liquid as at n_TOF the two estimators differ by ×1.34, and without liquid by ×1.64 (up to ×1.87 for 20 µm,
  pointing only). All twelve rows of §3 are within the ×2 that we ask for. The Cu ogive on its ×30 tables shows the
  same pattern (×1.07, ×1.99 and ×2.45 in pass 3). The spread is therefore a property of the two estimators when the
  energy resolution is poor, and more Monte Carlo would not reduce it.
- Without liquid the raw fit is still ×0.54 of the floored fit. The no-liquid rows are the least certain of the table.

### 4.4 Verdict: final for the Monte Carlo statistics, and what remains

**The two-arm number of the Al ogive + Cu liner is now on the same footing as the hemisphere's (pass 4) and the Cu
ogive's (pass 3).** No further Geant4 run is needed for it. What remains uncertain is not the Monte Carlo statistics:

1. The range of the two estimators: ±3 % in days with the liquid working, ±15 % with the liquid as at n_TOF, and
   −22 % / +28 % without liquid (11 µm, reference level). These ranges are in the tables.
2. The holder is a design, not a part. The mask radius, the liner and the mount are those of CU_LINER and of the 27 Oct
   sketch (§7) **(ask)**.
3. The external conversions of the horizontal pair rest on 2 events. Their effect is at the 2 % level (§4.2).
4. Everything that pass 4 does not cover either: the SiPM-wall leg efficiency, the cosmic veto on real data, the 17.64
   and 14.6 MeV substitutions (FEASIBILITY_SIM §19.3).

## 5. History: the first pass on L12 alone (25 Nov, morning)

### 5.1 The first-pass numbers

The first pass used run L12 alone, because the L13 tables of this holder were not on the desktop and the task did not
connect to lxplus. Its numbers are in the last column of the tables of §3 and in `out/summary_reach_pass5alli11.csv`
and `out/summary_reach_pass5al.csv`. For 11 µm and the reference level it gave 19.1 (17.3–21.1), 31.6 (26.0–38.5) and
81.1 (79.3–82.9) d, which is 0.84, 1.07 and 1.72 × R(ATOMKI). The four arms gave 8.1, 16.3 and 27.9 d.

Its Monte Carlo statistics were thin (§4.2, the L12 columns): 43 M1 events in the fit region, 39 events in the leading
background of the signal window, and no external-conversion event. The two estimators agreed within ×1.5, so the usual
check passed. The numbers were marked interim.

### 5.2 The thin-table test, and how well it predicted

To see whether the agreement of the two estimators is enough on thin tables, we ran the same fit on the Cu ogive with run
L11 alone and on the Cu hemisphere with run L10 alone (`run_r10.sh` step 6). L11 and L10 have the size of L12. We compare
with passes 3 and 4, which use the ×30 tables. All rows are for 11 µm and the reference level (simulation).

| holder | pair | liquid | thin tables: days (direct, transplant) | ×30 tables: days (direct, transplant) | thin / ×30 (direct, transplant) |
|---|---|---|---|---|---|
| Cu ogive, L11 alone against L11 + L13 | horizontal pair | liquid working | 28.7 (28.5, 28.8) | 25.2 (26, 24.4) | ×1.14 (×1.10, ×1.18) |
| Cu ogive, L11 alone against L11 + L13 | horizontal pair | liquid as at n_TOF | 42.2 (28.4, 62.8) | 43.6 (30.9, 61.5) | ×0.97 (×0.92, ×1.02) |
| Cu ogive, L11 alone against L11 + L13 | horizontal pair | no liquid | 82 (40.7, 165) | 93.8 (60, 147) | ×0.87 (×0.68, ×1.12) |
| Cu ogive, L11 alone against L11 + L13 | four arms | liquid working | 10.4 (8.07, 13.3) | 15.3 (17.9, 13.1) | ×0.68 (×0.45, ×1.02) |
| Cu ogive, L11 alone against L11 + L13 | four arms | liquid as at n_TOF | 18.3 (12.4, 26.9) | 29.7 (27.8, 31.8) | ×0.61 (×0.45, ×0.84) |
| Cu ogive, L11 alone against L11 + L13 | four arms | no liquid | 49.8 (33.2, 74.7) | 67.5 (59.2, 77) | ×0.74 (×0.56, ×0.97) |
| Cu hemisphere, L10 alone against L10 + L18 | horizontal pair | liquid working | 95.7 (82.3, 111) | 151 (189, 120) | ×0.63 (×0.43, ×0.92) |
| Cu hemisphere, L10 alone against L10 + L18 | horizontal pair | liquid as at n_TOF | 126 (89.9, 177) | 263 (321, 215) | ×0.48 (×0.28, ×0.82) |
| Cu hemisphere, L10 alone against L10 + L18 | horizontal pair | no liquid | 209 (107, 410) | 511 (494, 529) | ×0.41 (×0.22, ×0.77) |
| Cu hemisphere, L10 alone against L10 + L18 | four arms | liquid working | 55.3 (41.3, 74.1) | 148 (256, 85.2) | ×0.37 (×0.16, ×0.87) |
| Cu hemisphere, L10 alone against L10 + L18 | four arms | liquid as at n_TOF | 67.6 (50.3, 90.7) | 194 (301, 126) | ×0.35 (×0.17, ×0.72) |
| Cu hemisphere, L10 alone against L10 + L18 | four arms | no liquid | 133 (77.9, 227) | 372 (450, 308) | ×0.36 (×0.17, ×0.74) |

The test showed that the transplant estimator is stable on thin tables (×0.72–1.18 of its ×30 value in all twelve
rows), and that the direct estimator with the floor is not (×0.16–1.10). Where the direct estimator is biased, it is
biased toward fewer days. The Cu ogive's horizontal pair was right within 15 % on thin tables, and its four arms were too
fast by ×1.35–1.65. The hemisphere was too fast everywhere. We expected the Al ogive to behave like the Cu ogive, because
it has the same outline, the same beam line and similar rates.

The Al ogive itself can now be added to the test (simulation, 11 µm, reference level):

| Al ogive + Cu liner, L12 alone against L12 + L13 | liquid working | liquid as at n_TOF | no liquid |
|---|---|---|---|
| horizontal pair: thin / ×30, central (direct, transplant) | ×0.90 (×0.97, ×0.85) | ×0.81 (×0.78, ×0.86) | ×1.03 (×1.29, ×0.82) |
| four arms: thin / ×30, central (direct, transplant) | ×0.70 (×0.56, ×0.87) | ×0.72 (×0.50, ×1.04) | ×0.63 (×0.51, ×0.77) |

The Al ogive behaves like the Cu ogive, as expected. The first-pass numbers for the horizontal pair were low by 10–19 %
with liquid cells, and the four-arm numbers were low by ×1.4–1.6.

**A lesson for other holders:** on tables of the size of L10, L11 or L12, the agreement of the two estimators does not
show that a fit is converged. The four-arm fits are too fast by ×1.4–2.9 on such tables in all three holders tested.

## 6. Why the scaled estimate was low

The scaled estimate of `planning/two_arm_estimates.py` was the four-arm 4.5 d of FEASIBILITY_SIM §19.3 times 2.30. The
factor 2.30 is the Cu ogive's ratio of the horizontal pair at 11 µm to the four arms at 20 µm, on its ×30 tables with the
pass-3 settings. This gave 10.4 d. The simulation follows the same chain on the Al ogive's own tables:

| step (liquid working, reference level) | Al ogive + Cu liner (simulation) | factor | the scaling assumed |
|---|---|---|---|
| four arms, 20 µm, 0.3 ns, L4 cosmics, L12 alone | 4.64 d | | 4.5 d |
| four arms, 20 µm, 0.6 ns, L15 cosmics, L12 alone | 5.19 d | ×1.12 | ×1 |
| four arms, 20 µm, L12 + L13 | 6.89 d | ×1.33 | ×1 |
| horizontal pair, 20 µm, L12 + L13 | 13.5 d | ×1.96 | ×1.67 (Cu ogive) |
| horizontal pair, 11 µm, L12 + L13 | 21.1 d | ×1.56 | ×1.38 (Cu ogive) |

- The largest single term is the base of the scaling. The four-arm 4.5 d was made on the thin L12 tables, where the
  four-arm fit is too fast by ×1.33. The 0.6 ns time of flight and the L15 cosmics add ×1.12.
- The two ratios taken from the Cu ogive are each about 15 % smaller than the Al ogive's own ratios. The lighter holder
  has less beam background, so the cosmics and the smaller yield of the thin film weigh more.
- The product of the five differences is ×2.03, which is the ratio of 21.1 d to 10.4 d.
- A consequence outside this task: the four-arm days of the Al ogive + Cu liner in FEASIBILITY_SIM §19.3 and in
  `planning/two_arm_estimates.FOUR_ARM` (4.5 and 8.5 d) should be replaced by 6.9 and 13.1 d (20 µm, `all` rows of
  `out/summary_reach_pass5al_l13.csv`), or 11.6 and 22.6 d for 11 µm.

## 7. What else differs from the Cu-hemisphere pass

A reader comparing §3 with pass 4 should know the following differences, beyond the holder itself.

1. **The Li spot.** The Al-ogive runs place the vertices only where the beam lands at r ≤ 4 mm (`--li-mask-r 4`), and
   the yields are those of a line-of-sight film behind that mask (`LiLos4`): 86 % of a σ = 2 mm beam is on the Li, and
   the γ₀ yield per proton is 0.90 of a flat film (CU_LINER §3). The hemisphere uses a flat film with the whole beam on
   Li. For 11 µm this gives 6.66 × 10⁸ γ₀ per day for the Al ogive against 7.37 × 10⁸ for the hemisphere. CU_LINER §7
   notes that the r ≤ 4 mask also helps the opening-angle resolution by about 25 % in days, because flank vertices are
   excluded. A real mask of r ≤ 6 mm, which CU_LINER recommends for the yield, would lose part of this gain. This was not
   simulated here.
2. **The beam line.** The ogive sits on an Al ring and a DN40 steel tube
   (`Al:19.05:30:-68:-63,SS:17.4:19.05:-620:-68,SS:31:57:-620:-585`), as in Pierfrancesco's 27 Oct sketch. The hemisphere
   run has the photographed grey flange with its PVC pieces and Al flange (`LINE_CUP`). The ogive's mount is a sketch, not
   a built part **(ask)**.
3. **The Monte Carlo statistics** are now the same for the backgrounds (L12 + L13 against L10 + L18). The X17 sample of
   the Al ogive is ×1/7 of the hemisphere's (500,000 against 3,500,000 generated).
4. **The binaries.** L12 and L13 used `mx17_full_sim_culiner_812488b`; L18 used `mx17_full_sim_twoarm_10229eb`. Both
   build the four arms as built. TWO_ARM_STUDY §1.1 records that the two-arm branch builds the same geometry when no new
   option is given.
5. **The cosmics** are the same L15 sample in both cases. L15 was simulated with the Cu ogive in place, which does not
   matter for muons that cross the arms.
6. **The E_sum windows** are the reference windows per liquid state (13–19, 13–22 and 13–20 MeV), as in pass 4. The
   window scan of pass 4 (`esum_scan.py`) was made for the hemisphere only. The leptons lose less energy in the Al
   ogive, so the reference windows should suit it at least as well, but this was not scanned.
7. **The 11 µm film** changes the yields only, as in pass 4. The Geant4 events are those of the 20 µm film.
8. **The 17.64 MeV share** is 0.9 % for the line-of-sight film at 1.10 MeV (CU_LINER §3), so the substitution of the
   18.15 MeV tables for the 17.64 MeV term matters little here.

## 8. What to quote

- For the 11 µm film, horizontal pair, five days at 1.10 MeV (simulation, L12 + L13): **0.88 × R(ATOMKI)** with the
  liquid cells working, **1.19 ×** with the liquid as at n_TOF, **1.70 ×** without liquid cells. Days to 3σ: 21 (20–22),
  39 (33–45) and 79 (62–101).
- For the 20 µm film: 0.70, 0.94 and 1.40 × R(ATOMKI); 13.5, 24.4 and 53.3 d.
- The sentence "a lighter aluminium holder would give an expected limit of 0.6–0.8 × R(ATOMKI) in five days" should become
  "about R(ATOMKI) (0.9–1.2 ×)". With the hemisphere at 2.35 × and MEG II at 2.07 ×, the statement that the lighter holder
  turns the run from a feasibility test into a first limit still holds.
- Four arms of this holder, pass-4 settings: 11.6 and 22.6 d (11 µm), 6.9 and 13.1 d (20 µm), in place of 4.5 and 8.5 d.
- `planning/`, the page and the proposal were not edited here. `planning/two_arm_estimates.py` (another session's edit)
  reads `out/summary_reach_pass5al_l13*.csv` first, so its next run takes the numbers of §3.

## 9. Files and commands

First pass (desktop, 6 workers, about 1.5 h):

```
cd ~/PycharmProjects/lnl_x17
WORK_DATA=/media/ucla/work bash sim2arm/run_r10.sh 6                    # steps 1-4: closure, 11 µm, 20 µm, §19.3 settings (L12 alone)
WORK_DATA=/media/ucla/work R10_STEPS="6" bash sim2arm/run_r10.sh 6      # the thin-table test of §5.2
PY=~/PycharmProjects/nTof_x17/.venv/bin/python
WORK_DATA=/media/ucla/work $PY sim2arm/r10_al_ogive.py mcstat           # -> out/r10_mcstat_pass5al.csv (L12 alone, hemisphere)
$PY sim2arm/r10_al_ogive.py tables                                      # -> out/summary_reach_pass5al*.csv (L12 alone)
$PY sim2arm/r10_al_ogive.py thin                                        # §5.2
```

Second pass (about 1 h):

```
ssh lxplus 'ls -la /eos/experiment/ntof/data/x17/lnl/target/sel_l13/'   # and the part counts, sizes, md5 sums of §2.3 (read-only)
rsync -t --ignore-existing --no-perms --no-owner --no-group --include='L13_*_ogAl300cu12r8m4_asb_sel.npz' --exclude='*' \
    'lxplus:/eos/experiment/ntof/data/x17/lnl/target/sel_l13/*' /media/ucla/work/x17_facility_search/lnl_sel/
WORK_DATA=/media/ucla/work R10_STEPS="2 3" R10_SFX=_l13 bash sim2arm/run_r10.sh 6      # tags _pass5al_l13li11, _pass5al_l13
WORK_DATA=/media/ucla/work R10_SFX=_l13 $PY sim2arm/r10_al_ogive.py mcstat           # -> out/r10_mcstat_pass5al_l13.csv
R10_SFX=_l13 $PY sim2arm/r10_al_ogive.py tables                                      # §3 -> out/summary_reach_pass5al_l13*.csv
WORK_DATA=/media/ucla/work $PY sim2arm/r10_al_ogive.py raw                            # §4.1
```

The 11 µm fits of the second pass were first written under the tag `_pass5alli11_l13`. The file and its cache were renamed
to `_pass5al_l13li11`, the name the planning reads, and `run_r10.sh` now writes that name directly. Since the L13 tables
are on the disk, `run_r10.sh` sets `TA_RUNS=L12` for the tags without a suffix, so that the first pass stays reproducible.

The single fits behind `run_r10.sh` are calls of this form (step 2 with `R10_SFX=_l13`, the 11 µm film):

```
LI_UG=587 TA_CFG=ogAl300cu12r8m4 $PY sim2arm/two_arm_nd.py reach --pairs horiz all \
    --resps 'LNL calibrated' 'n_TOF as is' 'LNL calibrated, LS off' --levels 'MM 15° + TOF' 'MM 15° point, μ 3°' \
    --mcs direct transplant -j 6 --tag _pass5al_l13li11
```

| file | what |
|---|---|
| `sim2arm/two_arm_nd.py` | new entry `ogAl300cu12r8m4` (L12 + L13); `TA_RUNS` to restrict the runs |
| `sim2arm/run_r10.sh` | the fits, steps 1–6 |
| `sim2arm/r10_al_ogive.py` | summaries and the tables of this note (`R10_SFX=_l13` for the second pass) |
| `sim2arm/out/two_arm_reach_pass5al_l13li11.csv`, `summary_reach_pass5al_l13li11.csv` | **L12 + L13, 11 µm (of record)** |
| `sim2arm/out/two_arm_reach_pass5al_l13.csv`, `summary_reach_pass5al_l13.csv` | **L12 + L13, 20 µm (of record)** |
| `sim2arm/out/r10_mcstat_pass5al_l13.csv` | Monte Carlo events per component, L12 + L13 (§4.2) |
| `sim2arm/out/two_arm_reach_pass5alli11.csv`, `summary_reach_pass5alli11.csv` | L12 alone, 11 µm (first pass) |
| `sim2arm/out/two_arm_reach_pass5al.csv`, `summary_reach_pass5al.csv` | L12 alone, 20 µm (first pass) |
| `sim2arm/out/r10_mcstat_pass5al.csv` | Monte Carlo events per component, L12 alone and the hemisphere |
| `sim2arm/out/*_pass5al_closure.csv` | the hemisphere through the same code path (§2.1) |
| `sim2arm/out/*_pass5al_old.csv` | the settings of FEASIBILITY_SIM §19.3 (§2.2) |
| `sim2arm/out/*_pass5al_thin_ogCu200li11.csv`, `*_pass5al_thin_dome300li11.csv` | the thin-table test (§5.2) |
| `sim2arm/out/parts/reach_pass5al*/` | the fit caches of the new tags |
| `/media/ucla/work/x17_facility_search/lnl_sel/L13_*_ogAl300cu12r8m4_asb_sel.npz` | the five L13 tables, a copy of EOS (73 MB) |

Nothing was committed. `summarize.py` was not run on the new tags, because its figure carries the title "Cu hemisphere";
`r10_al_ogive.py` writes the summary tables with the same function (`summarize.reach`).
