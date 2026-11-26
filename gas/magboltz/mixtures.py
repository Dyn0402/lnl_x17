"""mixtures.py -- the single source of the LNL gas study's candidates (gas/GAS_STUDY.md §2-3).

Every composition is % by volume. Water and O2 displace argon. Flammability is ISO 10156:2017 formula (3):
the mixture is not flammable in air if  sum_i A_i (100/Tci_i - 1) <= sum_k B_k K_k.
Tci (Table 2): isobutane 3.4, methane 8.7. K_k (Table 1): Ar 0.55, CO2 1.5, CF4 2, N2 1 (H2O and O2 left out:
water would count as a 3-atom inert, K 1.5, so leaving it out is conservative).
"""
PRESSURE_TORR = 760.0      # Legnaro is ~10 m above sea level; mean sea-level pressure
TEMP_K = 293.15
E_MIN, E_MAX, N_GRID = 40.0, 600.0, 16
NCOLL = 5

TCI = {'ic4h10': 3.4, 'ch4': 8.7}
KK = {'ar': 0.55, 'co2': 1.5, 'cf4': 2.0, 'n2': 1.0}

# label -> (dry composition, role)
BASES = {
    'ArIso_95_5':        ([('ar', 95.0), ('ic4h10', 5.0)], 'reference: current LNL plan, flammable'),
    'ArIso_90_10':       ([('ar', 90.0), ('ic4h10', 10.0)], 'reference: n_TOF production gas, flammable'),
    'ArIso_98.2_1.8':    ([('ar', 98.2), ('ic4h10', 1.8)], 'the most isobutane Ar/iC4H10 can hold and stay non-flammable'),
    'ArCO2_97_3':        ([('ar', 97.0), ('co2', 3.0)], 'binary, no hydrocarbon'),
    'ArCO2_95_5':        ([('ar', 95.0), ('co2', 5.0)], 'binary, no hydrocarbon'),
    'ArCO2_93_7':        ([('ar', 93.0), ('co2', 7.0)], 'NSW backup gas'),
    'ArCO2_90_10':       ([('ar', 90.0), ('co2', 10.0)], 'binary, no hydrocarbon'),
    'ArCO2Iso_95.5_3_1.5': ([('ar', 95.5), ('co2', 3.0), ('ic4h10', 1.5)], 'ternary, low CO2'),
    'ArCO2Iso_94_4_2':   ([('ar', 94.0), ('co2', 4.0), ('ic4h10', 2.0)], 'ternary, least CO2 at 2 % isobutane'),
    'ArCO2Iso_93_5_2':   ([('ar', 93.0), ('co2', 5.0), ('ic4h10', 2.0)], 'ATLAS NSW gas (SPS CO2 epoch)'),
    'ArCO2Iso_90_8_2':   ([('ar', 90.0), ('co2', 8.0), ('ic4h10', 2.0)], 'ternary, more CO2'),
    'ArCO2Iso_88_10_2':  ([('ar', 88.0), ('co2', 10.0), ('ic4h10', 2.0)], 'ternary, most CO2'),
    'ArCH4_96_4':        ([('ar', 96.0), ('ch4', 4.0)], 'P10-like, below the methane limit (~5 %)'),
    'ArCH4CO2_91_5_4':   ([('ar', 91.0), ('ch4', 5.0), ('co2', 4.0)], 'methane + CO2, non-flammable'),
    'ArCO2Iso_96.5_2_1.5': ([('ar', 96.5), ('co2', 2.0), ('ic4h10', 1.5)], 'ternary, low quencher (added 26 Nov)'),
    'ArCH4CO2_94_4_2':   ([('ar', 94.0), ('ch4', 4.0), ('co2', 2.0)], 'methane + a little CO2 (added 26 Nov)'),
    'ArCF4Iso_95_3_2':   ([('ar', 95.0), ('cf4', 3.0), ('ic4h10', 2.0)], 'reference: T2K TPC gas (CF4, high GWP)'),
    'ArCF4Iso_88_10_2':  ([('ar', 88.0), ('cf4', 10.0), ('ic4h10', 2.0)], 'reference: SPS CF4 epoch (CF4, high GWP)'),
}
WATER_PCT = [0.0, 0.25, 0.5, 1.0, 1.5]
# second pass (26 Nov): finer water steps where the velocity peak crosses the window
FINE_WATER = [0.1, 0.375, 0.75]
FINE_BASES = ['ArCH4_96_4', 'ArIso_98.2_1.8', 'ArCO2_97_3', 'ArCO2Iso_93_5_2', 'ArIso_95_5', 'ArIso_90_10',
              'ArCF4Iso_95_3_2', 'ArCO2Iso_95.5_3_1.5', 'ArCO2Iso_96.5_2_1.5', 'ArCH4CO2_94_4_2']
O2_PPM_AT = (0.5, 200.0)      # one attachment point: 0.5 % water + 200 ppm O2 (n_TOF/SPS fits: 130-400 ppm)
T_CHECK = ['ArIso_95_5', 'ArCO2Iso_93_5_2', 'ArCO2_93_7']   # dry at 303.15 K: tests the E/N scaling


def flammability(comps):
    """ISO 10156 formula (3). Returns (lhs, rhs, non_flammable)."""
    lhs = sum(a * (100.0 / TCI[g] - 1.0) for g, a in comps if g in TCI)
    rhs = sum(b * KK[g] for g, b in comps if g in KK)
    return lhs, rhs, lhs <= rhs


def _wet(dry, water_pct, o2_ppm=0.0):
    out = []
    for g, f in dry:
        if g == 'ar':
            f = f - water_pct - o2_ppm * 1e-4
        out.append((g, round(f, 4)))
    if water_pct > 0:
        out.append(('h2o', water_pct))
    if o2_ppm > 0:
        out.append(('o2', o2_ppm * 1e-4))
    return out


def compositions():
    out = {}
    for b, (dry, role) in BASES.items():
        for w in WATER_PCT:
            out[f'{b}__w{w:g}'] = dict(base=b, role=role, water_pct=w, o2_ppm=0.0, comps=_wet(dry, w))
        w, o2 = O2_PPM_AT
        out[f'{b}__w{w:g}_o{o2:g}'] = dict(base=b, role=role, water_pct=w, o2_ppm=o2, comps=_wet(dry, w, o2))
    for b in FINE_BASES:
        for w in FINE_WATER:
            out[f'{b}__w{w:g}'] = dict(base=b, role=BASES[b][1], water_pct=w, o2_ppm=0.0, comps=_wet(BASES[b][0], w))
    for b in T_CHECK:
        out[f'{b}__w0_T303'] = dict(base=b, role=BASES[b][1], water_pct=0.0, o2_ppm=0.0, T=303.15,
                                    comps=_wet(BASES[b][0], 0.0))
    return out


if __name__ == '__main__':
    for b, (dry, role) in BASES.items():
        l, r, ok = flammability(dry)
        print(f'{b:22s} {"non-flammable" if ok else "FLAMMABLE":14s} {l:6.1f} <= {r:6.1f}?  {role}')
    print(len(compositions()), 'tables')
