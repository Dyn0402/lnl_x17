# A lithium film known only to ±50 %: what it does to the slot-1 run

Written 2026-11-25. We are told that whatever target is made, its thickness and its homogeneity will carry an uncertainty
of about 50 %. This note works out what that uncertainty does to the rates, to the reach of the 8-day CN run, to the
441 keV calibration and to the choice of film. It also says how to measure the film during the run.

Code: `sim2arm/li_thickness.py` (yields: system or venv python; reach: the nTof_x17 venv, `-j 14`, ~15 min).
Outputs: `sim2arm/out/li_thickness/` (`yields_vs_thickness.csv`, `yields_441.csv`, `yields_chemistry.csv`,
`yields_nonuniform.csv`, `lioh_margin.csv`, `reach.csv`, `reach_summary.csv`, two figures).

## 0. Result in short

1. **The film thickness sets the γ rate, and the γ rate sets the reach.** At 1.10 MeV the γ₀ yield is close to
   proportional to the thickness: a film of 0.5 × the nominal 11 µm gives 0.45 × the γ rate, and a film of 1.5 × gives
   1.49 ×. The cosmic background does not change with the film. For this reason a thin film costs more than a thick
   film gains.
2. **For the 46 hours at 1.10 MeV, the expected limit with the liquid working moves from 3.8 × R(ATOMKI) to 6.2 ×
   (film 0.5 × nominal) or 3.1 × (film 1.5 × nominal).** The days of beam to 3σ change by × 2.7 and × 0.67.
   The proposal should quote 3.8 × with this range, or state the thickness it assumes. **Update 26 Nov:** with the
   external conversions of run L19 (sim2arm/EPC_L19.md) every limit is ~13 % higher: 6.9 × / 4.3 × / 3.55 × at
   0.5 / 1 / 1.5 × nominal. The relative effects of this note do not change (§8).
3. **An uneven film with the right mean thickness costs little.** The spot-averaged yield depends almost only on the
   mean thickness. A ±50 % spread across the beam spot changes the days to 3σ by 3 to 8 %. If half of the spot sits on
   bare copper (and the rest is twice as thick), the days increase by 18 %.
4. **The real danger is an uneven film combined with its chemistry.** Residual water turns lithium into LiOH. The
   oxygen and hydrogen add stopping power, so the beam leaves the film at a lower energy. The thick parts of an uneven
   film then reach the 441 keV resonance, which is about 50 times stronger than the 18.15 MeV one. With half of the
   lithium converted, a uniform 11 µm film takes 1.6 % of its γ₀ from the 17.64 MeV line. A film with a ±50 % Gaussian
   spread takes 36 %. The reach is then 2.4 to 3.7 times longer in days.
5. **The 441 keV point does not depend on the film.** On the narrow resonance the yield of any film thicker than
   about 4 µm is within 5 % of that of the 11 µm film. Therefore the ratio of the γ₀ yields at 1.10 MeV and at 441 keV
   measures the film thickness in the beam spot, directly, during the run. The 478 keV line of ⁷Li(p,p′γ), which the
   γ monitor sees anyway, is a second measurement of the lithium in the spot (PIGE).
6. **The measured R does not need the thickness, if it is normalised to the γ rate.** The proposal already normalises
   R to a γ monitor. With that, the thickness uncertainty only changes the statistical reach. Without a γ monitor, the
   normalisation would carry the full 50 %.
7. **Choice of the nominal film.** A thicker nominal film protects the reach against the thin side. However, it reaches
   the 441 keV resonance with less conversion. At 11 µm, the thickest part of a ±50 % film (16.5 µm) passes 10 % of γ₀
   from 17.64 MeV once 60 % of its lithium is LiOH. At 14 µm the thickest part (21 µm) does so at 40 %. We suggest
   keeping 10–12 µm, measuring the film on day 1, and replacing a film that is thin or uneven (§6).

## 1. The film and the question

The target is a metallic lithium film on the inside of the built Cu hemisphere (R 11 mm, 300 µm wall). The nominal
thickness is 11 µm, which is 587 µg/cm² (TARGET_REVIEW §4.2 chose 10–12 µm so that the film cannot reach the 441 keV
resonance even if it turns into hydroxide). The beam spot has σ = 2 mm.

We consider three kinds of uncertainty:
- the **mean thickness** in the beam spot, from 0.5 to 1.5 × nominal (5.5–16.5 µm);
- the **homogeneity**, which is a spread of the thickness across the beam spot at a fixed mean;
- the **chemistry**, which is the fraction of the lithium atoms that has turned into LiOH on the beam side.

## 2. Method

The yields come from the yield model of `x17_facility_search/lnl/target/target_model.py` (`layered_yield`). The proton
slows down through the film in steps of 0.25 keV, with PSTAR stopping powers. At each step the model adds the captures
of the 441 keV resonance (17.64 MeV, M1), of the 1.03 MeV resonance (18.15 MeV, M1) and of the direct E1 capture, with
the cross sections of Zahnow 1995.

For an uneven film we average the absolute yields over a thickness distribution with the given mean. The shapes are a
Gaussian with an rms of 25 % or 50 %, a flat distribution from 0.5 to 1.5 × the mean, a skewed gamma distribution
(rms 50 %), and a "holes" model where a fraction of the spot is bare copper and the rest is thicker.

The reach comes from the reference two-arm fit (`two_arm_nd.task`): horizontal pair, MM 15° pointing + 0.6 ns time of
flight, the built Cu hemisphere (L10 + L18 tables), 1 µA at 1.10 MeV. For each film we replace only the yields. The
Geant4 events stay those of the 20 µm run, since 10 µm of lithium is 10⁻⁵ X₀ and the leptons do not notice it. In the
fit the M1, E1 and γ₁ normalisations are free, so a changed capture mix costs only through the shapes. The central value
is the geometric mean of the two estimators (direct + floor, transplant), as in TWO_ARM_STUDY §1.3. The expected limit
after T days of beam is R₉₀ = 1.28 / (3 √(T/d₃)) × R(ATOMKI), with d₃ the days to 3σ. The 46 h are the CN request.

The nominal scenario reproduces the pass-4 result exactly: 151 / 263 / 511 days to 3σ (liquid working / as at n_TOF /
none), 3.8 / 5.0 / 7.0 × R(ATOMKI) in 46 h.

## 3. Rates and capture mix as a function of the thickness

Figure `out/li_thickness/yields_vs_thickness.png` shows, as a function of the film thickness, the γ₀ yield relative to
11 µm, the energy at which the beam leaves the film, and the share of γ₀ from direct (E1) capture.

**Uniform metallic film, E_p = 1.10 MeV**

| film (µm) | γ₀ yield / 11 µm | beam leaves at (keV) | 17.64 MeV share | 18.15 resonance share | direct E1 share |
|---|---|---|---|---|---|
| 5.5 (0.5 ×) | 0.45 | 1041 | 0.6 % | 47 % | 52 % |
| 8.25 | 0.73 | 1010 | 0.6 % | 48 % | 51 % |
| **11 (nominal)** | **1.00** | **979** | **0.6 %** | **47 %** | **52 %** |
| 13.75 | 1.25 | 947 | 0.7 % | 45 % | 55 % |
| 16.5 (1.5 ×) | 1.49 | 915 | 0.7 % | 42 % | 58 % |

- The yield is proportional to the thickness to within 10 %. The film is thin compared with the 168 keV width of the
  1.03 MeV resonance, so each micrometre adds about the same number of captures.
- The mix changes by a few per cent only. The thicker film reaches lower energies, below the resonance, where direct
  capture is a larger share. Since the E1 and M1 normalisations float in the fit, this matters little.
- A fresh metallic film never reaches the 441 keV resonance in this range. The beam leaves a 16.5 µm film at 915 keV.

## 4. Thickness and chemistry together

Table: share of γ₀ from the 17.64 MeV line at E_p = 1.10 MeV (in brackets, the energy at which the beam leaves the film,
keV), for a uniform film, as a function of the fraction of the lithium converted to LiOH.

| film (µm) | fresh | 25 % LiOH | 50 % LiOH | 75 % LiOH | 100 % LiOH |
|---|---|---|---|---|---|
| 5.5 | 0.6 % (1041) | 0.6 % (998) | 0.7 % (953) | 0.8 % (907) | 0.9 % (859) |
| 8.25 | 0.6 % (1010) | 0.7 % (944) | 1.0 % (873) | 1.4 % (799) | 1.6 % (720) |
| 11 | 0.6 % (979) | 0.9 % (887) | 1.6 % (789) | 2.7 % (681) | 4.4 % (560) |
| 13.75 | 0.7 % (947) | 1.3 % (829) | 2.7 % (697) | 8.9 % (547) | 76 % (364) |
| 16.5 | 0.7 % (915) | 1.7 % (767) | 5.8 % (598) | 91 % (389) | 77 % (54) |

The same with an uneven film of mean 11 µm (17.64 MeV share of the spot-averaged γ₀):

| film, mean 11 µm | fresh | 50 % LiOH | 100 % LiOH |
|---|---|---|---|
| uniform | 0.6 % | 1.6 % | 4.4 % |
| Gaussian, rms 25 % | 0.7 % | 2.8 % | 51 % |
| Gaussian, rms 50 % | 0.7 % | **36 %** | 62 % |
| flat, 0.5–1.5 × | 0.7 % | 2.4 % | 58 % |
| half the spot bare, the rest 22 µm | 0.9 % | 89 % | 77 % |

- This means that the homogeneity matters through the chemistry, not through the rate. A film whose thick parts reach
  the 441 keV resonance produces mostly 17.64 MeV γ rays. The trigger rate rises several-fold and the 18.15 MeV region
  sits under a background that the run was not designed for.
- How fast the film converts is not known (TARGET_REVIEW §4.2). The repo's upper-limit rate is 1.35 µm of lithium per
  day at 10⁻⁷ mbar of water. At that rate, 60 % of an 11 µm film is converted in about 5 days.

## 5. The reach

Table: days of beam to 3σ at R(ATOMKI) and the expected 90 % CL limit after the 46 h at 1.10 MeV, horizontal pair,
1 µA (`out/li_thickness/reach_summary.csv`). Figure `out/li_thickness/reach_vs_thickness.png` shows the uniform films.

| film | γ₀ per day | days to 3σ, liquid working | R₉₀ (46 h), liquid working | R₉₀ (46 h), as at n_TOF | R₉₀ (46 h), no liquid |
|---|---|---|---|---|---|
| uniform 0.5 × (5.5 µm) | 3.3 × 10⁸ | 409 (× 2.7) | 6.2 × | 8.2 × | 11.1 × |
| uniform 0.75 × | 5.4 × 10⁸ | 217 (× 1.44) | 4.5 × | 6.0 × | 8.3 × |
| **uniform 1.0 × (11 µm)** | **7.4 × 10⁸** | **151** | **3.8 ×** | **5.0 ×** | **7.0 ×** |
| uniform 1.25 × | 9.2 × 10⁸ | 119 (× 0.79) | 3.4 × | 4.4 × | 6.2 × |
| uniform 1.5 × (16.5 µm) | 1.1 × 10⁹ | 101 (× 0.67) | 3.1 × | 4.1 × | 5.7 × |
| mean 1 ×, Gaussian rms 50 % | 7.3 × 10⁸ | 160 (× 1.06) | 3.9 × | 5.2 × | 7.2 × |
| mean 1 ×, flat 0.5–1.5 × | 7.3 × 10⁸ | 156 (× 1.03) | 3.8 × | 5.1 × | 7.1 × |
| mean 1 ×, skewed (gamma, rms 50 %) | 7.2 × 10⁸ | 162 (× 1.08) | 3.9 × | 5.2 × | 7.3 × |
| mean 1 ×, half the spot bare | 7.1 × 10⁸ | 178 (× 1.18) | 4.1 × | 5.5 × | 7.7 × |
| uniform 1.0 ×, all LiOH | 6.4 × 10⁸ | 237 (× 1.57) | 4.7 × | 6.4 × | 8.9 × |
| uniform 1.5 ×, 50 % LiOH | 9.1 × 10⁸ | 170 (× 1.13) | 4.0 × | 5.4 × | 7.5 × |
| uniform 1.5 ×, 75 % LiOH | 9.5 × 10⁹ | 561 (× 3.7) | 7.3 × | 9.5 × | 12.6 × |
| mean 1 ×, Gaussian 50 %, 75 % LiOH | 1.5 × 10⁹ | 367 (× 2.4) | 5.9 × | 7.8 × | 10.4 × |
| mean 1 ×, flat, all LiOH | 1.4 × 10⁹ | 347 (× 2.3) | 5.7 × | 7.6 × | 10.1 × |

(The γ₀ per day includes the 17.64 MeV line. That is why it rises by up to × 13 once the beam reaches 441 keV.)

- The days to 3σ scale roughly as t^−1.2 between 0.5 and 1.5 × the nominal thickness. The beam background and the signal
  both scale with t, and the cosmic background does not. Therefore a thin film loses more than a thick film gains.
- At five days of beam (24-hour days), the same ranges are 3.9 × (0.5 ×), 2.35 × (nominal) and 1.9 × (1.5 ×).

## 6. What to do about it

1. **Measure the film in the beam on day 1.** The γ₀ yield per µC at 1.10 MeV is proportional to the lithium in the
   spot. The yield on the 441 keV resonance is the same for any film thicker than about 4 µm (`yields_441.csv`: within
   5 % from 4 to 20 µm at E_p 441–470 keV). Therefore the ratio of the two yields, read by the γ monitor, gives the film
   thickness in the spot without an absolute efficiency. This is one more reason to ask for the H₂⁺ day. Without H₂⁺,
   the 478 keV γ ray of ⁷Li(p,p′γ) gives the lithium content through its known thick-target yield (PIGE), with the
   efficiency of the monitor at 478 keV and the cross section as the uncertainties.
2. **Watch the 17.64 / 18.15 MeV ratio continuously.** A LaBr₃ separates the two lines. The 17.64 MeV share is the
   alarm for a film that has started to reach 441 keV (TARGET_REVIEW §4.2 item 3). Replace the film when the share
   passes a few per cent.
3. **Map the film before it goes in, if LNL can.** An ion-beam analysis (RBS, NRA or PIGE) of each film at a few spots
   gives the mean and the spread. Dylan or Pierfrancesco to ask whether this is possible at LNL **(ask)**.
4. **Bring spare films.** A film that is thin (less than ~0.7 × nominal) or uneven can be replaced at the start, since
   films are cheap. The question is how long a film change takes on the CN line **(ask)**.
5. **Keep the nominal at 10–12 µm.** A thicker nominal film would protect the reach against the thin side. With 14 µm
   nominal, the limit for the 46 h would range from 5.1 × to 2.8 × instead of 6.2 × to 3.1 ×. However, the thickest
   part of the film would then reach 441 keV at 40 % conversion instead of 60 % (`lioh_margin.csv`). Since the
   conversion rate is unknown, we prefer the margin against the chemistry.

| nominal film | R₉₀ (46 h) at 0.5 × / 1 × / 1.5 × | LiOH fraction at which the 1.5 × part passes 10 % of γ₀ from 17.64 MeV |
|---|---|---|
| 8 µm | 7.9 / 4.7 / 3.6 × | 100 % |
| 9.5 µm | 7.0 / 4.1 / 3.3 × | 75 % |
| 11 µm | 6.2 / 3.8 / 3.1 × | 60 % |
| 12.5 µm | 5.6 / 3.5 / 2.9 × | 50 % |
| 14 µm | 5.1 / 3.3 / 2.8 × | 40 % |

## 7. Limits of this study

- The yield model is only as good as its cross sections (Zahnow 1995, ~10 %) and stopping powers (PSTAR, a few per
  cent). Lithium metal is assumed at bulk density. The film's real density and porosity change the thickness in µm, but
  not the areal density, which is what matters.
- The chemistry is modelled as a converted layer on the beam side. Real conversion may be patchy or follow the grain
  boundaries.
- The non-uniformity is modelled as a distribution of thickness over the spot. A gradient across the spot combined with
  a beam spot that moves would also make the rate drift during the run. The γ monitor follows that.
- The Geant4 events are those of the 20 µm run. The vertex depth in the film changes by less than 20 µm, and the energy
  loss of the leptons in the film is negligible, so we expect no effect on the shapes.

## 8. Update 2026-11-26: with the external conversions of run L19

The tables of §5 used the L18 external conversions, which rested on 2 simulated events in the window. Run L19
(sim2arm/EPC_L19.md) has 100 times more, and the fit then needs 195 days to 3σ instead of 151 for the nominal film. We
repeated the scan with L19 (`TA_EPC_RUN=L19 python sim2arm/li_thickness.py reach`; `out/li_thickness/reach_summary_l19.csv`,
`reach_vs_thickness_l19.png`).

| film | days to 3σ, liquid working (relative) | R₉₀ (46 h), liquid working | R₉₀ (46 h), as at n_TOF | R₉₀ (46 h), no liquid | R₉₀ (5 d), liquid working |
|---|---|---|---|---|---|
| uniform 0.5 × | 501 (× 2.57) | 6.9 × | 9.0 × | 11.6 × | 4.3 × |
| uniform 0.75 × | 275 (× 1.41) | 5.1 × | 6.6 × | 8.6 × | 3.2 × |
| **uniform 1.0 ×** | **195** | **4.3 ×** | **5.5 ×** | **7.2 ×** | **2.66 ×** |
| uniform 1.25 × | 156 (× 0.80) | 3.85 × | 4.9 × | 6.4 × | 2.4 × |
| uniform 1.5 × | 133 (× 0.68) | 3.55 × | 4.5 × | 5.9 × | 2.2 × |
| mean 1 ×, Gaussian rms 50 % | 206 (× 1.06) | 4.4 × | 5.7 × | 7.5 × | 2.7 × |
| mean 1 ×, half the spot bare | 229 (× 1.17) | 4.7 × | 6.0 × | 7.9 × | 2.9 × |
| mean 1 ×, Gaussian 50 %, 75 % LiOH | 461 (× 2.37) | 6.6 × | 8.2 × | 10.6 × | 4.1 × |
| uniform 1.5 ×, 75 % LiOH | 868 (× 4.45) | 9.1 × | 10.3 × | 13.9 × | 5.6 × |

The conclusions of §0 stand. The thickness moves the limit by the same factors as before, and the combination of an
uneven film with LiOH remains the case to avoid.
