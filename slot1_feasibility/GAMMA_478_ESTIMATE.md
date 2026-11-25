# The 478 keV line of 7Li(p,p'γ)7Li: yield, detector rates and dose (estimate)

2026-11-25. Literature and arithmetic only. No Geant4 was run. Every number marked **(estimate)** is a scaling or
rests on an assumption that is written next to it. Numbers without that mark are taken from the cited source.

A referee asked about the 478 keV gamma line of 7Li(p,p'γ)7Li. Our Geant4 simulation does not include this line. This
note estimates how many 478 keV photons the target emits, what they do in the detectors, and what dose rate they give.

**Result in short.** At 1.10 MeV and 1 µA the lithium film emits about 1.0 × 10^7 photons/s of 478 keV (±30 %). This
is about 1200 times the simulated 17-18 MeV gamma yield (8.5 × 10^3 /s). At 0.441-0.45 MeV the beam is below the
reaction threshold of 0.546 MeV, so the line is absent on that day. A 478 keV photon cannot make a trigger leg.

## 1. Yield of 478 keV photons

### 1.1 Threshold, and what it means for the 0.45 MeV day

The first excited state of 7Li is at 477.6 keV [S7]. The reaction 7Li(p,p'γ)7Li therefore has Q = −0.4776 MeV. The
threshold in the laboratory is E_th = |Q| (m_p + m_Li)/m_Li = 0.4776 × 8.0238/7.0160 = **0.546 MeV**. This confirms the
value in the question.

The 0.441-0.45 MeV beam is 0.1 MeV below this threshold, and the beam only loses energy in the film. Therefore the
lithium emits **no 478 keV photons from 7Li(p,p'γ) on the 0.45 MeV day**. The state has spin 1/2, so at 1.10 MeV the
478 keV photons are emitted isotropically. Taskaev et al. checked this at 15° and 110° [S1].

### 1.2 Energy loss of the beam in the 11 µm film

Lithium is not one of the PSTAR elements. We use the Andersen-Ziegler stopping formula for lithium as it is written in
Taskaev et al. [S1], with a density of 0.534 g/cm3. This formula reproduces the proton ranges quoted in that paper (we
find 30 µm at 0.70 MeV and 142 µm at 1.85 MeV, and the paper quotes 31 µm and 144 µm).

| Beam energy | dE/dx in Li at entry | Energy after 11 µm (587 µg/cm2) | Energy lost |
|---|---|---|---|
| 1.10 MeV | 11.4 keV/µm (213 MeV cm2/g) | 0.97 MeV | 0.13 MeV |
| 0.441 MeV | 20.8 keV/µm (390 MeV cm2/g) | 0.15 MeV | 0.29 MeV |
| 0.450 MeV | 20.5 keV/µm | 0.17 MeV | 0.28 MeV |

The range of a 0.441 MeV proton in lithium is 15.5 µm, so the beam still leaves the film and stops in the copper.
(Estimate: numerical integration of the formula. SRIM was not run.)

### 1.3 Published data used

| Source | What is measured | Values used |
|---|---|---|
| Taskaev et al. 2021 [S1], Table 1 | 478 keV yield of a thick natural-lithium metal target on copper, HPGe, absolute accuracy 15 % | 0.340 × 10^7 /µC at 0.974 MeV, 0.496 × 10^7 at 1.001 MeV, 1.01 × 10^7 at 1.075 MeV, **1.20 × 10^7 /µC at 1.100 MeV**, 1.38 × 10^7 at 1.125 MeV |
| Taskaev et al. 2021 [S1], Table 2 | cross section per 7Li nucleus | 27.2 mb at 0.967 MeV, 35.1 mb at 0.994, 40.0 mb at 1.019, **40.8 mb at 1.043**, 39.0 mb at 1.068, 36.3 mb at 1.093 MeV |
| Mateus et al. 2002 [S2] (EXFOR D0328) | total cross section from a thin LiF target, HPGe at 135°, 10 % | 20.6 mb at 0.971 MeV, 28.9 mb at 0.995, 36.1 mb at 1.019, **37.9 mb at 1.043**, 37.1 mb at 1.067, 35.3 mb at 1.092 MeV. The lowest point is 0.078 mb at 0.652 MeV |
| Aslam et al. 2002 [S3] (EXFOR C0901) | cross section, NaI, 99.9 % 7Li | 20.7 mb at 1.00 MeV, 38.2 mb at 1.05 MeV, 42.5 mb at 1.12 MeV |

The cross section has a broad maximum of about 40 mb at 1.03-1.05 MeV. Our beam crosses exactly this region
(1.10 MeV to 0.97 MeV), so the film sits on the maximum. Caciolli et al. 2006 [S4] covers 3.0-5.7 MeV and is not usable
here. We did not retrieve Boni et al. 1988 or the IBANDL files (the IBANDL and EXFOR search pages block scripted access).

### 1.4 Arithmetic at 1.10 MeV, 1 µA

Method A uses the thick-target yields directly. The film yield is the thick-target yield at the entry energy minus the
thick-target yield at the exit energy. The target of Taskaev et al. is natural lithium metal on copper, as ours is.

- Y(1.100 MeV) − Y(0.969 MeV) = (1.20 − 0.31) × 10^7 = 0.89 × 10^7 photons/µC. At 1 µA this is **0.89 × 10^7 /s**.

Method B integrates the cross section through the film. The film holds 5.10 × 10^19 Li atoms/cm2, of which
4.71 × 10^19 /cm2 are 7Li. The beam is 6.24 × 10^12 protons/s.

- With the cross sections of Taskaev et al. we find 1.10 × 10^7 /s. With those of Mateus et al. we find 0.98 × 10^7 /s.
- Check by hand: 6.24 × 10^12 × 4.71 × 10^19 × 35 mb (average over the film) = 1.0 × 10^7 /s.

**We adopt 1.0 × 10^7 photons/s into 4π at 1.10 MeV and 1 µA (estimate, ±30 %).**

The uncertainty has three parts. The absolute accuracy of the yield measurement is 15 %. The two methods differ by
24 %, and Aslam et al. is about 30 % above Mateus et al. at 1.12 MeV. A film that is 20 % thinner or thicker changes
the yield by −17 % or +14 %, and a beam energy 25 keV lower or higher changes the yield by −9 % or +3 %. The
uncertainty is therefore well inside a factor of 2. It is not a factor of 10.

| Beam energy | 478 keV photons/s at 1 µA | 17-18 MeV photons/s (simulation, given) | Ratio |
|---|---|---|---|
| 0.441-0.45 MeV | 0 (below the 0.546 MeV threshold) | 5.4 × 10^4 | 0 |
| 1.10 MeV | 1.0 × 10^7 (±30 %) | 8.5 × 10^3 | about 1200 |

## 2. Other prompt sources, one line each

1. **63Cu, 65Cu(p,γ) in the beam stop.** The protons enter the copper with at most 0.97 MeV. The lowest measured
   points of Sevior et al. 1983 [S5] are 1.2 ± 0.3 µb at 1.031 MeV for 65Cu(p,γ)66Zn and 3.3 ± 0.7 µb at 1.112 MeV for
   63Cu(p,γ)64Zn. With a cross section of about 0.7 µb at 0.97 MeV that falls by a factor e every 70-100 keV, and a
   stopping power of 120 MeV cm2/g [S9], we estimate 20-60 captures/s (estimate). This is below 1 % of the 17-18 MeV
   gamma yield, and the capture cascades carry at most 8.7 MeV (64Zn) or 9.9 MeV (66Zn). On the 0.45 MeV day the
   protons reach the copper with 0.15 MeV and this source is zero.
2. **63Cu, 65Cu(p,p'γ) in the beam stop.** The first levels are at 670 keV (63Cu) and 771 keV (65Cu). Qiang 1990 [S6]
   measured only 11-52 µb at 2.0 MeV. At 0.97 MeV the protons are 0.2-0.3 MeV above these thresholds and far below
   the Coulomb barrier. We found no measurement below 1 MeV. A semiclassical Coulomb-excitation estimate gives well
   below 1 nb, which means less than 1 photon/s (estimate, order of magnitude only).
3. **7Li(p,n)7Be.** The threshold is 1.880 MeV [S8]. This confirms the value in the question. Both beam energies are
   below the threshold, so the lithium produces no neutrons.
4. **7Li(p,α)α.** Q = 17.35 MeV, so at 1.10 MeV the alpha particles have 7.6-10.8 MeV in the laboratory. The range of
   a 10 MeV alpha particle in copper is 24 mg/cm2 = 27 µm [S9]. The 300 µm copper therefore stops every forward alpha
   particle. The backward alpha particles stop in the beam-pipe wall.
5. **19F(p,αγ)16O, 6.1-7.1 MeV gammas, if the lithium carries fluorine.** Between 0.97 and 1.10 MeV there is only the
   narrow 1090 keV resonance and the tails of the 935 keV and 1189 keV resonances [S10]. We take an average of about
   5 mb (estimate, factor 3). For a fluorine fraction f (F atoms per Li atom) the rate is 1.6 × 10^6 × f per second.
   A fraction of 10^-3 would give 1.6 × 10^3 /s, which is 20 % of the 17-18 MeV yield. A fraction of 10^-4 gives 2 %.
   At 0.441 MeV the beam crosses the 340 keV resonance and the rate is (0.5-1) × 10^6 × f per second, which is 1-2 %
   of the 17.6 MeV yield for f = 10^-3 (estimate). We have no measurement of the fluorine content of our lithium (ask).
6. **11B(p,γ)12C.** Per atom the cross section near 1 MeV is of the same order as that of 7Li(p,γ)8Be (about 30 µb
   from the simulated yield). A boron fraction f therefore adds a relative gamma yield of order f (estimate, the boron
   cross section was not looked up). This is negligible for metallic lithium.
7. **7Be build-up.** 7Li(p,n)7Be gives none below 1.880 MeV. 6Li(p,γ)7Be (7.6 % 6Li, S ≈ 0.1 keV b [S11]) has a
   cross section of 3-5 µb at our energies, which gives about 100 atoms of 7Be per second, or about 1 Bq per day of
   beam (estimate). This reaction also gives a few tens of 429 keV photons per second, which is negligible.
8. **Not in the question: aluminium in the beam.** At 1.10 MeV any beam that stops in aluminium crosses the strong
   992 keV resonance of 27Al(p,γ)28Si (gammas of 1.78 and up to 10.8 MeV). With a resonance strength of 1.9 eV (quoted
   from memory, to be checked) the thick-target yield is about 10^-9 per proton, or 7 × 10^3 /s if the full 1 µA hit
   aluminium (estimate). Collimators and holders seen by the beam should be copper or tantalum.

## 3. Singles rates from the 478 keV line at 1.10 MeV, 1 µA

All rates in this section are estimates. They use 1.0 × 10^7 photons/s, isotropic emission, each detector centred on
the arm axis, and NIST attenuation coefficients at 478 keV [S12] (Ar 0.081, plastic scintillator 0.096, air 0.089,
glass 0.089 cm2/g). They ignore the vacuum chamber wall. The 300 µm copper absorbs only 2 % of the photons.

### 3.1 Micromegas TPC

The 40 × 36 cm2 active area at 204 mm covers 1.93 sr, which is 15.3 % of 4π. Therefore **1.5 × 10^6 photons/s cross
one Micromegas active area** (about 1100 photons/cm2/s).

Electrons in the 3 cm gas gap come from three places.

- Compton scattering in the gas. Ar/isobutane 95/5 has 1.70 mg/cm3, so 3 cm is 5.1 mg/cm2. The interaction
  probability is 4.1 × 10^-4 at normal incidence and about 4.8 × 10^-4 averaged over the angles. This gives about
  0.7 kHz.
- Compton electrons from the air in front (20 cm, 25 mg/cm2) and from the window. The mean Compton electron has
  160 keV and a range of about 35 mg/cm2 [S9]. We assume that the electrons made in the last third of one range reach
  the gas. This gives about 1 × 10^-3 electrons per photon, or about 1.5 kHz.
- Backscatter from the mesh and the 7 mm PCB. We assume a few hundred Hz. The PCB absorbs 11 % of the photons, and
  nearly all of the electrons made in the PCB stop in the PCB.

The total is **2-3 kHz of electrons per Micromegas (factor 3), which is about 2 Hz/cm2**. With 1 µs long events the
probability that such an electron overlaps a triggered event is 0.2-0.3 %. If one electron fires about 20 of the 500
strips of a plane, the rate per strip is about 100 Hz. Micromegas detectors are normally operated at particle fluxes
of kHz/cm2 and above (general statement, not sourced here), so this rate is small for the detector. The Micromegas
readout is triggered by the scintillators, so these electrons do not add triggers.

### 3.2 Scintillators above 100 keV

A Compton electron from a 478 keV photon has more than 100 keV in 66 % of the scatters (Klein-Nishina). It has more
than 250 keV in 26 % and more than 300 keV in 6 % of the scatters.

| Detector | Fraction of 4π | Photons/s arriving | Interaction probability | Rate above 100 keV |
|---|---|---|---|---|
| SiPM wall, 3 mm plastic, 40 × 47 cm2 at 330 mm | 9.7 % | 8.7 × 10^5 (after the PCB) | 3.5 % | **2 × 10^4 Hz per wall**, 1 kHz per bar (20 bars) |
| One 2 cm plastic, 20 × 30 cm2 at 414 mm | 2.4 % | 2.0 × 10^5 | 18 % | **2.4 × 10^4 Hz per plastic** |
| Liquid cell, 45 × 45 × 4 cm at 460 mm | 6.2 % | 5.3 × 10^5 | 29 % | about 1 × 10^5 Hz |

We assumed that the two plastics sit side by side and cover 40 × 30 cm2 on the axis. The uncertainty of these rates is
about a factor of 2 (yield, material in front, threshold).

### 3.3 Can a 478 keV photon make a leg?

No. The Compton edge of a 478 keV photon is 311 keV, and the photon carries 478 keV in total. A leg needs about 2 MeV
(0.5 MIP) in the 2 cm plastic. One photon cannot deposit this energy.

Pile-up cannot do it either. At least 7 photons would have to scatter in the same plastic within its resolving time.
The plastic sees 3.7 × 10^4 interactions/s. For a 50 ns resolving time the rate of such 7-fold pile-up is about
10^-15 Hz. The probability that one extra 478 keV scatter (at most 0.31 MeV) falls on a real signal is 0.2 %.

The 3 mm bars are different, because 0.5 MIP in a bar is only 0.3 MeV. If the bar threshold is at 0.25-0.3 MeV, the
478 keV line fires the bars at 2-8 kHz per wall. A leg then needs a random coincidence with a real plastic signal
above 2 MeV. For a ±20 ns coincidence the accidental leg rate is 8 kHz × 40 ns = 3 × 10^-4 of the plastic singles rate
above 2 MeV. Even for an assumed 1 kHz of plastic singles this is 0.3 Hz, which is small relative to the simulated
67 Hz of real legs.

## 4. Radioprotection: ambient dose-equivalent rate at 1 m, unshielded, 1 µA

A point source of Y photons/s gives a fluence rate of Y/(4π × 10^4 cm2) at 1 m.

| Source | Photons/s | Fluence rate at 1 m | Coefficient | Dose rate at 1 m |
|---|---|---|---|---|
| 478 keV line, 1.10 MeV beam | 1.0 × 10^7 | 80 /cm2/s | H*(10)/Φ = 2.81 pSv cm2 | **0.8 µSv/h** (±30 %) |
| 17-18 MeV gammas, 0.441 MeV beam | 5.4 × 10^4 | 0.43 /cm2/s | 35 pSv cm2 | **0.05 µSv/h** |
| 17-18 MeV gammas, 1.10 MeV beam | 8.5 × 10^3 | 0.068 /cm2/s | 35 pSv cm2 | 0.01 µSv/h |

The 478 keV coefficient is interpolated between the ICRP 74 values of 2.38 pSv cm2 at 0.4 MeV and 2.93 pSv cm2 at
0.5 MeV [S13]. We quote these two values from memory of ICRP 74 Table A.21. We checked them in two ways. They reproduce
the known dose-rate constant of 137Cs (0.09 µSv/h per MBq at 1 m). The ICRP 116 effective dose for front irradiation
[S14] gives 2.37 pSv cm2 and 0.7 µSv/h, which is consistent.

The ICRP 74 table of H*(10) ends at 10 MeV. For the 17-18 MeV gammas we therefore use the ICRP 116 effective-dose
coefficient, which is 26-30 pSv cm2 at 15 MeV and 31-38 pSv cm2 at 20 MeV depending on the geometry [S14]. We take
35 pSv cm2 (estimate).

The dose rate at 1 m is therefore dominated by the 478 keV line on the 1.10 MeV day. It is below 1 µSv/h without any
shielding. Natural background is about 0.1 µSv/h. Bremsstrahlung from the accelerator itself is not part of this
estimate.

## 5. Statement for the proposal

> At 1.10 MeV the lithium target also emits the 478 keV line of 7Li(p,p'γ)7Li, which our simulation does not include.
> From the measured thick-target yields of Taskaev et al. (2021) we estimate about 10^7 photons per second at 1 µA
> (±30 %), roughly a thousand times the 17-18 MeV gamma yield. At 0.441 MeV the beam is below the 0.546 MeV threshold
> of this reaction and the line is absent. A 478 keV photon deposits at most 0.31 MeV in a Compton scatter, so it
> cannot satisfy the trigger, which requires about 2 MeV in the plastic scintillator. We estimate that it adds a few
> kHz of low-energy electrons in each Micromegas (about 2 Hz/cm2), about 20 kHz above 100 keV in each scintillator
> layer, and an unshielded ambient dose rate of about 1 µSv/h at 1 m from the target.

## 6. What this note does not have

- No simulation. The detector rates in section 3 are single-scatter estimates and should be replaced by a Geant4 run
  with a 478 keV isotropic source of 10^7 /s.
- No measurement of the Cu(p,p'γ) yield below 1 MeV, of the 19F(p,αγ) cross section between 0.97 and 1.10 MeV (we used
  the 1959 resonance table), or of the fluorine and boron content of the lithium.
- The material between the target and the Micromegas (chamber wall, window thickness) was not known to us. It changes
  the electron rate of section 3.1 within the quoted factor 3.

## Sources

- [S1] S. Taskaev et al., "Measurement of the 7Li(p,p'γ)7Li reaction cross-section and 478 keV photon yield from a
  thick lithium target at proton energies from 0.65 MeV to 2.225 MeV", NIM B 502 (2021) 85.
  https://doi.org/10.1016/j.nimb.2021.06.010 , full text https://bnct.inp.nsk.su/publics/2021/NIM_B_2021.pdf
- [S2] R. Mateus et al., "Proton-induced γ-ray analysis of lithium in thick samples", NIM B 190 (2002) 117.
  https://doi.org/10.1016/S0168-583X(01)01222-8 , data https://www-nds.iaea.org/nrdc/exfor-master/entry/d/d0328.txt
- [S3] Aslam, W.V. Prestwich, F.E. McNeill, "Thin target 7Li(p,p'γ)7Li inelastic gamma-ray yield measurements",
  J. Radioanal. Nucl. Chem. 254 (2002) 533. https://doi.org/10.1023/A:1021646222974 ,
  data https://www-nds.iaea.org/nrdc/exfor-master/entry/c/c0901.txt
- [S4] A. Caciolli et al., "Measurements of γ-ray emission induced by protons on fluorine and lithium", NIM B 249
  (2006) 98 (3.0-5.7 MeV only).
  https://flore.unifi.it/bitstream/2158/253303/1/Measurements%20of%20%ce%b3-ray%20emission%20induced%20by%20protons%20on%20fluorine%20and%20lithium.pdf
- [S5] M.E. Sevior et al., "Absolute cross sections of proton induced reactions on 65Cu, 64Ni and 63Cu", Aust. J. Phys.
  36 (1983) 463. https://www.publish.csiro.au/ph/PH830463 ,
  data https://www-nds.iaea.org/nrdc/exfor-master/entry/a/a0198.txt
- [S6] S. Qiang, "Sub-Coulomb proton induced reactions on copper", thesis (1990), EXFOR C0739.
  https://www-nds.iaea.org/nrdc/exfor-master/entry/c/c0739.txt
- [S7] TUNL Nuclear Data, energy levels of 7Li (first excited state 0.478 MeV, 1/2−).
  https://nucldata.tunl.duke.edu/nucldata/HTML/A=7/07Li_2002.shtml
- [S8] 7Li(p,n)7Be threshold 1880.4-1880.8 keV: "Calibration of proton accelerator beam energy",
  https://arxiv.org/abs/1703.00644 . Taskaev et al. [S1] use 1.882 MeV.
- [S9] NIST PSTAR, ASTAR and ESTAR stopping-power and range tables (copper, air, plastic scintillator).
  https://physics.nist.gov/PhysRefData/Star/Text/intro.html
- [S10] TUNL Nuclear Data, Table 20.13 of Ajzenberg-Selove and Lauritsen 1959, resonances for 6-7 MeV gammas in
  19F(p,α)16O. https://nucldata.tunl.duke.edu/nucldata/HTML/A=20/20_13_1959.pdf
- [S11] 6Li(p,γ)7Be S-factor, S(0) ≈ 90-100 eV b: "The 6Li(p,γ)7Be reaction rate in the light of the new LUNA data",
  https://arxiv.org/abs/2201.07987
- [S12] NIST X-ray mass attenuation coefficients (Hubbell and Seltzer).
  https://physics.nist.gov/PhysRefData/XrayMassCoef/tab3.html and
  https://physics.nist.gov/PhysRefData/XrayMassCoef/tab4.html
- [S13] ICRP Publication 74 (1996), "Conversion coefficients for use in radiological protection against external
  radiation", Table A.21. https://www.icrp.org/publication.asp?id=ICRP%20Publication%2074
- [S14] ICRP Publication 116 (2010), photon effective dose per fluence, as tabulated in
  https://github.com/openmc-dev/openmc/blob/develop/openmc/data/dose/icrp116/photons.txt ;
  https://www.icrp.org/publication.asp?id=ICRP%20Publication%20116
