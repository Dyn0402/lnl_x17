# The Micromegas gas for the LNL feasibility run

Started 2026-11-25, Magboltz study 2026-11-25/26 (dylan-MS-7C84). Status: **study done, choice not made yet** (§8 lists
what decides it). Scripts and outputs are in this folder (§9).

## 1. The question and the constraints

At n_TOF we chose the gas to survive the gamma flash. At LNL there is no flash. The beam is 1.10 MeV protons, below the
⁷Li(p,n) threshold of 1.88 MeV, so there are no neutrons either. The gamma background is about 2 Hz/cm² per Micromegas
(`slot1_feasibility/GAMMA_478_ESTIMATE.md` §3.1), which the gas composition hardly changes. For this reason we choose the
gas for tracking and for convenience. We set four constraints.

1. **The drift voltage.** The drift cathodes of some chambers do not hold more than 800 V. At n_TOF, chamber A (det3)
   sparked at 800 V on 17 July 2026 (run_51 `run_config.json`: "det A drift 550 V (sparking at 800 V)"). It ran at
   550–600 V for runs 51–59. From run 77 to run 162 (production) all four chambers ran at 700 V. Chamber A had held
   1000–1100 V on the CEA bench in June, so the limit appeared after transport. Chamber B (det2) ran 800 V at n_TOF and
   now needs a drift repair. **We therefore design for at most 700 V on both chambers, and we treat 800 V as a stretch
   that may not be available.** The mesh is at ground, so the drift field is the drift voltage divided by the gap. The
   gaps are 28.1 mm for A and 31.3 mm for B (nTof_x17 `rerun/PAPER1_NUMBERS_2026-10-31.md`, DET4GAP row). Chamber B sets
   the limit: 700 V gives at most **224 V/cm**, and 800 V gives at most **256 V/cm**. Chamber A reaches 249 V/cm at 700 V.
2. **Water.** There will be water in the gas. At the SPS the gas fit found 1.5–1.8 % water, and n_TOF had about as much.
   We hope to keep it below 1 %, and ideally to drive it towards 0.1 %. We therefore look at three bands of water:
   "dry" (0–0.1 %), "target" (0.1–0.5 %) and "as at n_TOF" (0.5–1.0 %).
3. **The figures of merit.** We want a drift velocity v that stays stable, and a small transverse diffusion D_T. The
   number of primary electrons was the first idea, but §4 shows that it is the same for every candidate.
4. **Convenience.** A non-flammable premix avoids the flammable-gas safety file at LNL and the ADR rules for shipping a
   flammable gas. CF₄ has a global warming potential of about 7,400, and CERN is phasing it out. For these reasons we
   keep the CF₄ mixtures as references only.

## 2. Which mixtures are non-flammable (ISO 10156)

ISO 10156:2017 classifies a mixture of flammable and inert gases. By its formula (3), the mixture is not flammable in air if

  Σ A_i (100/T_ci − 1) ≤ Σ B_k K_k.

Here A_i is the percentage of each flammable gas and B_k the percentage of each inert gas. T_ci is the most of that gas
which, mixed with nitrogen, is still not flammable. It is 3.4 % for isobutane and 8.7 % for methane (Table 2). K_k is the
nitrogen equivalency of each inert gas. It is 0.55 for argon, 1.5 for CO₂ and 2 for CF₄ (Table 1).

Argon is a weak inert gas (K = 0.55). For this reason the limits are tight:

- **Ar/iC₄H₁₀ holds at most 1.9 % isobutane.** Ar/iC₄H₁₀ 98/2 is therefore flammable, by a small margin. 95/5 and 90/10
  are clearly flammable.
- **The NSW gas Ar/CO₂/iC₄H₁₀ 93/5/2 is non-flammable, but only just** (56.8 ≤ 58.7). The 5 % of CO₂ is what makes it
  pass. At 2 % isobutane, about 3 % of CO₂ is the least that is needed.
- **Ar/CH₄ holds at most about 5 % methane.** P10 (Ar/CH₄ 90/10) is therefore flammable by this rule.

`magboltz/mixtures.py` computes the margin for every candidate (the `flam_margin` column of `out/ranking.csv`). LNL's
safety office makes the final classification **(ask)**. The water in the gas counts as an inert gas, so leaving it out is
conservative.

## 3. Method

- **Magboltz** through Garfield++ (pin 927e5c21, the nTof_x17 install) computes v, D_T, D_L and the attachment
  coefficient η. Each table covers 40–600 V/cm (16 field points, 5 × 10⁷ collisions per point) at **760 Torr and 20 °C**.
  Legnaro is about 10 m above sea level.
- **18 mixtures** (§2 and `mixtures.py`): 14 that are non-flammable by ISO 10156, Ar/iC₄H₁₀ 95/5 and 90/10 as flammable
  references, and the two CF₄ mixtures as references.
- **Water** displaces argon at 0, 0.25, 0.5, 1.0 and 1.5 %. For the 10 most interesting gases we added 0.1, 0.375 and
  0.75 %. We also ran **200 ppm O₂** at 0.5 % water, since the n_TOF and SPS fits found 130–400 ppm.
- **Temperature check.** Three gases were also run at 303 K. Their drift velocity agrees with the 293 K table read at
  E × 303/293 to 0.1 %. This means v depends only on E/N, as expected. Therefore the sensitivity to temperature and
  pressure follows from the slope S = d ln v / d ln E: a change of 1 K changes v by S × 0.34 %, and a change of 1 hPa
  changes v by −S × 0.10 %.
- **The operating field.** For each gas and each water band we choose the field, between 100 V/cm and the limit, where
  v changes least across the band. We also require that the slowest drift crosses B's gap within 1.9 µs (32 DREAM
  samples of 60 ns), so v ≥ 16.5 µm/ns. The "spread" is (v_max − v_min)/v_mean over the band.
- **HEED** gives the primary clusters for an 8 MeV electron (`magboltz/heed_primaries.py`).
- The desktop ran all 141 tables (about 60 core-hours, 14 at a time), so we did not need lxplus. No table failed.

## 4. Primary ionisation is not where the candidates differ

HEED gives **29–37 clusters/cm and 84–97 electrons/cm** for every candidate (`out/heed_primaries.json`). Over 3 cm this
is 90–110 clusters, and every argon mixture is within about ±10 % of the others. We therefore drop this criterion.

## 5. Water moves the velocity peak, and this decides the choice

Figure `figures/v_vs_E.png` shows v(E) for every candidate, from dry (dark) to 1.5 % water (light). The blue band is the
range we can reach with 700 V on B. Figure `figures/peak_vs_water.png` shows the field at which v peaks, against the water
fraction.

The main finding is simple. **Water hardly changes the height of the velocity peak, but it moves the peak to a higher
field.** Water is a strong inelastic scatterer at low electron energy. It cools the electrons, so the same velocity
needs a higher field. Near the peak, v does not depend on the field to first order, so v is also stable against
temperature, pressure and small changes in water. On the rising side of the curve, which is below the peak, v changes
almost in proportion to E/N and changes strongly with water.

| field of the v peak (V/cm) | dry | 0.25 % | 0.5 % | 1 % water |
|---|---|---|---|---|
| Ar/iC₄H₁₀ 98.2/1.8 | 99 | 170 | 243 | 415 |
| Ar/CH₄ 96/4 | 69 | 169 | 243 | 349 |
| Ar/iC₄H₁₀ 95/5 (flammable) | 204 | 291 | 415 | > 450 |
| Ar/CO₂ 97/3 | 245 | 349 | 415 | > 450 |
| Ar/CO₂/iC₄H₁₀ 96.5/2/1.5 | 243 | 294 | 415 | > 450 |
| Ar/CH₄/CO₂ 94/4/2 | 243 | 291 | 349 | > 450 |
| Ar/CO₂/iC₄H₁₀ 93/5/2 (NSW) | > 450 | > 450 | > 450 | > 450 |

What this shows:

- **Only gases with very little quencher keep the peak inside our window when wet.** These are Ar/iC₄H₁₀ 98.2/1.8 and
  Ar/CH₄ 96/4. Dry, they peak at 70–100 V/cm. With 0.25–0.5 % water they peak at 170–240 V/cm, which is within the
  700 V range of B.
- **The NSW gas never reaches its peak in our window.** In 93/5/2 the peak is above 450 V/cm even dry. At 222 V/cm it
  sits on the steep side: S ≈ 1.1, which means about 0.4 % of v per kelvin and about 10 % of v per 0.1 % of water.
  The NSW chambers run at 600 V/cm over a 5 mm gap. Our gap is 30 mm and our limit is 700–800 V, so this gas does not
  suit our chambers.
- **Gases with an intermediate quencher** (Ar/CO₂ 97/3, 96.5/2/1.5, Ar/CH₄/CO₂ 94/4/2, and the flammable 95/5) peak
  inside the window only when the gas is dry.

## 6. Results: stability against diffusion

Figure `figures/v_vs_water.png` shows v against water for six gases, each at its best field for the target band.
Figure `figures/tradeoff.png` shows every candidate's spread in the target band against its D_T. The full numbers are in
`out/ranking.csv` and `out/summary.json`. The table gives each band at the best field with 700 V on B.

| gas (non-flammable unless marked) | dry: field, spread, D_T | target 0.1–0.5 %: field (V on B), spread, v range, D_T | 0.5–1 %: spread | with 800 V on B: target spread |
|---|---|---|---|---|
| **Ar/iC₄H₁₀ 98.2/1.8** | 102 V/cm, 0 %, 654 | **181 V/cm (566 V), 7 %, 31–33 µm/ns, 518 µm/√cm** | 33 % | 7 % |
| **Ar/CH₄ 96/4** | 101 V/cm, 1 %, 732 | **174 V/cm (544 V), 8 %, 34–37 µm/ns, 569 µm/√cm** | 32 % | 8 % |
| Ar/CO₂/iC₄H₁₀ 96.5/2/1.5 | 222 V/cm, 2 %, 440 | 222 V/cm, 28 %, 29–38, 370 | 49 % | 17 % |
| Ar/CH₄/CO₂ 94/4/2 | 222 V/cm, 3 %, 455 | 222 V/cm, 30 %, 31–42, 383 | 53 % | 18 % |
| Ar/CO₂ 97/3 | 222 V/cm, 4 %, 436 | 222 V/cm, 32 %, 27–37, 359 | 50 % | 20 % |
| Ar/CO₂/iC₄H₁₀ 93/5/2 (NSW) | 222 V/cm, 9 %, 284 | 222 V/cm, 39 %, 18–26, 244 | 39 % | 35 % |
| Ar/iC₄H₁₀ 95/5 (flammable, current plan) | 222 V/cm, 1 %, 456 | 222 V/cm, 21 %, 33–41, 385 | 48 % | 12 % |
| Ar/iC₄H₁₀ 90/10 (flammable, n_TOF) | 222 V/cm, 6 %, 352 | 222 V/cm, 35 %, 27–39, 302 | 48 % | 28 % |
| Ar/CF₄/iC₄H₁₀ 95/3/2 (T2K, CF₄) | 222 V/cm, 13 %, 307 | 222 V/cm, 58 %, 37–66, 270 | 62 % | 48 % |

D_T is given in µm/√cm. Over the full 3 cm gap the transverse spread is D_T × 1.73, for example 0.9 mm for 518 µm/√cm
and 0.42 mm for 244 µm/√cm. The strip pitch is 0.78 mm.

What the table shows:

1. **With 0.1–0.5 % water, the two low-quencher gases are about 5× steadier than the NSW gas.** Both sit at about
   175–180 V/cm, which is about 550–570 V on B and well below the 700 V limit. In the middle of the band their drift
   velocity moves by only about 0.6 % per 0.1 % of water, and by less than 0.04 % per kelvin.
2. **Their cost is diffusion.** Their D_T is about 520–570 µm/√cm, against 244 for 93/5/2 and 385 for 95/5. Their D_L
   is about 300–310 µm/√cm, against 286 for 93/5/2, so the longitudinal diffusion is about the same.
3. **If the gas stays dry (≤ 0.1 %), the intermediate gases become the better choice.** 96.5/2/1.5, Ar/CH₄/CO₂ 94/4/2
   and Ar/CO₂ 97/3 then keep v within 2–4 % at 222 V/cm, with D_T of 440–455. They have more quencher than the
   low-quencher gases and less diffusion. However, a little water ruins them: at 0.1–0.5 % water their spread is 28–32 %.
4. **No candidate is stable at 0.5–1 % water within 256 V/cm.** Every spread is 32 % or more. Water at the n_TOF level
   would therefore make any of these gases a calibration problem, whichever we choose. **Keeping the water below 0.5 %
   matters more than the choice of gas.**
5. **The 800 V stretch helps only the intermediate gases** (28 → 17 % for 96.5/2/1.5). It does nothing for the
   low-quencher gases, which do not need it, and little for 93/5/2.
6. **Oxygen.** With 200 ppm O₂ and 0.5 % water, 54 % (93/5/2) to 78 % (Ar/CH₄ 96/4) of the electrons from the cathode
   survive the 3 cm drift. Water alone attaches nothing. The low-quencher gases lose the fewest electrons, but every gas
   loses a significant fraction. Therefore oxygen also has to be kept low: tight joints, metal lines and enough flow.
7. **The drift time** at the target field is about 0.9–1.0 µs for the low-quencher gases. This is less than n_TOF's
   20 samples × 60 ns (1.2 µs) window. For 93/5/2 the drift time is 1.8 µs, which needs 32 samples.

## 7. What Magboltz does not tell us

- **Gain and spark stability.** Both leaders have less than 2 % quencher. Gases with that little quencher can have
  photon feedback, a steep gain curve and sparks. We have run 95/5 and 90/10 (n_TOF), and 93/5/2 and 88/10/2 CF₄ (SPS),
  but never < 2 % quencher in these chambers. Garfield (nTof_x17 `garfield_sim/results/HV_EQUIVALENCE.md`) puts
  Ar/iC₄H₁₀ 98/2 about 65 V below 95/5 for the same gain, with a similar slope. That is only a simulation of the gain,
  not of the stability. **A bench test on cosmics decides this (§8).**
- **What the extra diffusion does to the angle resolution.** A larger D_T spreads each cluster over more strips. That
  gives more strips per track, but the strips are also more correlated and the per-strip timing is noisier. We have not
  simulated this. The MX17 response simulation (MX17_Geant `design/RESPONSE_SIM_PLAN.md`) with D_T and D_L as inputs could answer it. The
  SPS runs give one data point with these chambers: run 53 (93/5/2) and run 63 (CF₄ 88/10/2). However, they differ in
  water and field as well, so they do not isolate D_T.
- **The water we will actually have.** The study gives v for a given water fraction. The water fraction itself depends
  on the gas lines, the chambers' outgassing and the flow (x17_facility_search `slow_control/`).
- Magboltz cross-sections for water and isobutane carry their own uncertainty, typically a few percent on v. The trends
  across mixtures are more reliable than the absolute values.

## 8. Recommendation and the decisions left

The recommendation depends on how dry we can keep the gas, which we do not know yet.

1. **Fix the gas system first, whichever gas we choose.** Metal or low-permeation lines, parallel feeds, a dryer and a
   water sensor at the inlet and outlet (x17_facility_search `slow_control/SENSOR_OPTIONS.md` §6). The low-permeation
   lines (€0.4k) move from the "low-budget upgrade" tier to the critical tier.
2. **The baseline: Ar/iC₄H₁₀ 98.2/1.8 or Ar/CH₄ 96/4 at about 175–180 V/cm (550–570 V on B).** They are non-flammable,
   they are within the 700 V limit with margin, and they are the most stable from 0.1 to 0.5 % water. Of the two,
   isobutane is the better-known quencher in our chambers and has slightly less diffusion. Methane is cheaper, gives a
   slightly faster drift, and has a larger margin below its flammability limit (42 against 53, compared with 51 against
   54 for isobutane). A premix with 1.8 % isobutane needs a supplier who certifies it below the 1.9 % limit **(ask SIAD / Sapio /
   Air Liquide)**.
3. **If we can show that the gas stays below 0.1 % water,** move to Ar/CO₂/iC₄H₁₀ 96.5/2/1.5 or Ar/CH₄/CO₂ 94/4/2 at
   about 220 V/cm. They have less diffusion (about 440–455 µm/√cm dry) and more quencher.
4. **Not the NSW gas 93/5/2** with these drift cathodes. It needs about 500 V/cm to reach its peak.
5. **The bench test that decides between items 2 and 3.** At CEA, with chamber A on cosmics, we take a gain and spark
   scan in 98.2/1.8 (or Ar/CH₄ 96/4) and in 96.5/2/1.5. We take a drift scan at 100–250 V/cm in each, with the water
   measured. We compare the angle resolution and the efficiency with the June 95/5 runs.
   This needs about 2 bottles and ~1 week. **(ask CEA: can the bench run a premix of ours?)**
6. **Simulation follow-up:** the effect of D_T 250 against 550 µm/√cm on the angle resolution, in the MX17 response
   simulation.
7. **Questions for LNL:** the flammability classification of the chosen mixture, and whether LNL stocks argon premixes.

## 9. Files

| path | what |
|---|---|
| `magboltz/mixtures.py` | the candidates, the water and O₂ grid, the ISO 10156 calculation (`python3 mixtures.py` prints the flammability table) |
| `magboltz/drift_one.py` | one Magboltz table → `out/tables/<key>.json` |
| `magboltz/run_local.sh` | runs every missing table on the desktop (`./run_local.sh 14`; needs nTof_x17 `garfield_sim/setup_garfield.sh`) |
| `magboltz/heed_primaries.py` | HEED clusters per cm → `out/heed_primaries.json` |
| `analyze.py` | metrics, operating fields, ranking and figures (system python3) |
| `out/ranking.csv`, `out/summary.json` | every candidate's numbers per band and voltage limit |
| `out/metrics.csv` | v and D_T at 150 / 200 / 224 / 256 V/cm for every gas and water level |
| `figures/` | `v_vs_E`, `DT_vs_E`, `peak_vs_water`, `v_vs_water`, `tradeoff` |
