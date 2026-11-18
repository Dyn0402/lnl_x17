# Slot 2: the ⁸Be X17 measurement with the full MX17 apparatus

Started 2026-11-18 as an outline. It is the experiment slot 1 prepares; nothing is requested yet.

## 0. Outline

- **When:** a proposal to the LNL PAC after slot 1, probably the call of late 2027, for beam in 2028 (estimate; the
  call rhythm was ~12–15 months).
- **Set-up:** four arms (A, B and re-bulked C and D), new windows on all four, the big plastics (4 in-house plates
  ~78 × 80 × 5 cm) behind the SiPM walls, own trigger/DAQ (architecture B or D of `x17_facility_search/daq_trigger/PLAN.md`),
  DREAM from CEA again.
- **Programme:** 441 keV calibration; 3σ at R(ATOMKI) at 1.10 MeV; off-resonance points at 0.80 and 1.225 MeV (clean
  points need 5–10 µm films). With big plastics the programme is **4.4 d** (Al ogive + Cu liner) to **12 d** (Cu ogive);
  as built 23–80 d (`x17_facility_search/lnl/FEASIBILITY_SIM.md` §19.5).
- **Budget:** Lean €103k, Self-sufficient €223k, Upgrade €279k (`x17_facility_search/budget/`, 17 Nov 2026).
- **Funding:** the INFN commission request that slot 1 is meant to support; the ERC CoG 2027 application
  (`x17_facility_search/funding/`).

## 1. What slot 1 must hand over

| slot-1 measurement | decides in slot 2 |
|---|---|
| 441 keV IPC: angular resolution, acceptance, energy scale | the reach numbers of the proposal, from data instead of Geant4 |
| cosmic rate in the X17 window, with and without the track veto | whether the TOF cut is needed; the shielding |
| arm-to-arm timing | 13 against 20 days as built |
| liquid cells at LNL rates | whether the liquid stays, or big plastics only |
| target lifetime, LiOH conversion, γ-yield stability | the film thickness, the holder |
| trigger and singles rates vs current | prescale, DREAM live time at > 1 µA, whether to ask for more current |

## 2. To do (after the PAC answer)

1. Re-bulk C and D at CEA; four windows.
2. Big plastics: bench-test a 5 cm plate (response), then buy raw slabs (`x17_facility_search/trigger_scint/`).
3. Choose the DAQ architecture after bench test T5.
4. The INFN commission request, with the slot-1 calibration in it.
5. The full proposal: the slot-1 results as the "status of activities from previous periods" that continuation
   proposals must summarise.
