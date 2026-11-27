# The γ-yield monitor: Pierfrancesco's 2 cm BaF₂ or a NaI(Tl)? (2026-11-27)

Pierfrancesco (26 Nov) has a BaF₂ crystal 2 cm thick, or can probably get a NaI(Tl) "if it need not be too thick". He asks
which γ energies we want to see. This note says what the monitor must do, and whether each detector can do it.
**All numbers are hand estimates** (attenuation coefficients from XCOM, rough efficiencies above a threshold); a Geant4
model of the chosen crystal replaces them.

## 1. What the monitor is for

1. **Normalise every pair rate to the γ yield** (LI_THICKNESS.md item 6). We count the 17–18 MeV γ rays above a
   threshold of a few MeV. This removes the ±50 % uncertainty of the film thickness from the measured rates.
2. **Measure the film thickness in the beam spot on day 1**: the ratio of the γ₀ yields per µC at 1.10 MeV and at
   441 keV (LI_THICKNESS.md §6.1). This is a relative measurement, so the absolute efficiency cancels.
3. **The lithium content from the 478 keV line of ⁷Li(p,p′γ)** (PIGE), at 1.10 MeV only.
4. **An alarm when the film starts to reach the 441 keV resonance** (LiOH, uneven film). LI_THICKNESS.md §6.2 planned
   to watch the 17.64 / 18.15 MeV ratio "with a LaBr₃". See §3: neither detector offered can do that.

## 2. Rates for the two candidates (1 µA, isotropic emission, crystal on axis at distance d)

The BaF₂ diameter is not known; we assume 5 cm **(ask)**. The NaI is taken as a standard 3″ × 3″.

| detector, distance | γ₀ counted at 1.10 MeV | γ₀ counted at 441 keV | 478 keV hits (1.10 MeV) | cosmic muons |
|---|---|---|---|---|
| BaF₂ 2 cm × ⌀5 cm, 20 cm | ~7 /s | ~40 /s | ~2.4 × 10⁴ /s | ~0.3 /s |
| NaI 3″ × 3″, 20 cm | ~40 /s | ~270 /s | ~8 × 10⁴ /s | ~0.8 /s |
| NaI 3″ × 3″, 40 cm | ~11 /s | ~70 /s | ~2 × 10⁴ /s | ~0.8 /s |

Inputs: γ₀ emitted 8.5 × 10³ /s at 1.10 MeV and 5.4 × 10⁴ /s at 441 keV (PREDICTIONS.md §3); 478 keV ≈ 1.0 × 10⁷ /s at
1.10 MeV, none at 441 keV (GAMMA_478_ESTIMATE.md). A 17.6 MeV γ interacts in 2 cm of BaF₂ with a probability of ~31 %
and in 7.6 cm of NaI with ~64 %; we assume that ~2/3 (BaF₂) and ~85 % (NaI) of the interactions deposit more than the
threshold.

## 3. Does each detector do the job?

1. **Normalisation and the thickness ratio: both work.** Even the BaF₂ counts ~6 × 10⁵ γ₀ per beam day at 1.10 MeV,
   so the statistical error is about 0.1 % per day. The limits are systematic:
   - **Cosmic muons.** A muon crossing 2 cm of BaF₂ deposits ~13 MeV, right in the γ₀ window. They are ~5 % of the
     counts at 1.10 MeV. They are measured with the beam off and subtracted, or removed by mounting the crystal with its
     axis horizontal (a vertical muon then crosses 5 cm, ~33 MeV). In a 3″ NaI most muons deposit ~35 MeV, above the window.
   - **The γ₁ lines (14.6–15 MeV).** A 2 cm crystal contains only part of a 17 MeV shower (one radiation length), so it
     sees a continuum and cannot separate γ₀ from γ₁. The γ₁ share differs between 441 keV (γ₁/γ₀ = 0.45) and 1.10 MeV.
     Therefore the thickness ratio needs a Geant4 response of the crystal and the γ₁ share at each energy. A 3″ NaI holds
     about three radiation lengths, so it separates 17.6 from 14.6 MeV partly (escape peaks, ~10 % resolution). That
     makes the ratio less model-dependent.
2. **478 keV (PIGE): both see it; the rate is the issue.** At 20 cm the BaF₂ takes ~2.4 × 10⁴ /s of 478 keV photons.
   With its 0.63 µs slow component, a few per cent of the pulses pile up. Two piled-up 478 keV pulses sum to ~1 MeV, far
   below the γ₀ threshold, so the γ₀ count is safe. The 478 keV peak area needs a dead-time and pile-up correction (a
   pulser, or the digitizer's live-time counter). A NaI at 20 cm would take ~8 × 10⁴ /s, too much for its 0.23 µs decay
   and µs shaping; at ~40 cm, or behind 1 cm of lead (16 % transmission at 478 keV, ~50 % at 17 MeV), it is fine. NaI
   resolves the line better (~7 % FWHM against ~11 % for BaF₂). The line is alone in that region (511 keV from
   annihilation is ~10³ times weaker), so either resolution is enough.
3. **The 17.64 / 18.15 MeV ratio: neither works.** The two lines are 0.5 MeV apart (2.8 %). Separating them needs a
   crystal that contains the whole shower (≥ 15 cm) with ~2 % resolution at 18 MeV. A 2 cm BaF₂ or a "not too thick" NaI
   cannot do this. The alarm can come instead from the **γ₀ yield per µC**: any part of the film that reaches 441 keV
   raises it, since that resonance is ~50 times stronger (a 10 % share of 17.64 MeV raises the yield per µC by ~10 %).
   The current must be integrated on the target for this **(ask: how LNL measures the current on a closed target)**. The
   γ₁/γ₀ ratio also changes when 441 keV contributes, and a 3″ NaI sees that partly.

## 4. Recommendation

- **Either detector does the essential job** (items 1 and 2). The BaF₂ is enough as a counter, with the crystal mounted
  axis-horizontal at ~20 cm, above or below the target (the arms are horizontal on the beam days), and a Geant4 model of
  its response.
- **A NaI(Tl) of 3″ × 3″ or larger is better**: about 6 times the γ₀ rate, partial separation of γ₀ and γ₁, cosmic
  muons out of the window, and a better 478 keV peak. Place it at ~40 cm or behind 1 cm of lead.
- **Drop the 17.64 / 18.15 line-ratio alarm** from the plan. Use the γ₀ yield per µC and the γ₁/γ₀ ratio instead.
- **Questions for Pierfrancesco:** the BaF₂ diameter and its PMT; the size of the NaI he can get; a free digitizer
  channel (the monitor goes into the scintillator DAQ, with its own self-trigger and a live-time counter).
- **Reply to his question "which energy":** 17.64 and 18.15 MeV (the γ₀ yield, counted above ~5 MeV), and 478 keV at
  1.10 MeV (the lithium content). Rates as in §2.
