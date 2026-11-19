import pathlib
R = pathlib.Path('/afs/cern.ch/work/d/dneff/git/x17_lnl/MX17_Full_Geant_twoarm')
h = R / 'include/SimConfig.hh'; s = h.read_text()
a = '    double      cosmicHeight_mm = 1500.0;\n'
assert s.count(a) == 1
s = s.replace(a, a + (
    '    // --cosmic-disk R (lnl_x17, 2026-11-19): instead of the plane, each muon starts on a disk of radius R\n'
    '    // perpendicular to its own direction, centred on the target, 1.2 R upstream along the track: every zenith\n'
    '    // angle reaches the set-up (the plane misses theta > ~45 deg at the centre).  Zenith from the intensity\n'
    '    // through a surface normal to the track, cos^2 theta sin theta, theta < 89 deg.  Live time: N / (J A_eff),\n'
    '    // A_eff = (4 pi / 3) R^2 for J = 1 cm^-2 min^-1 through a horizontal surface (I0 = 2/pi cm^-2 min^-1 sr^-1).\n'
    '    double      cosmicDisk_mm   = 0.0;\n'))
h.write_text(s)
m = R / 'mx17_full_sim.cc'; s = m.read_text()
a = '        else if (a == "--cosmic") config.cosmic = true;\n'
assert s.count(a) == 1
s = s.replace(a, a + '        else if (a == "--cosmic-disk" && i+1<argc) { config.cosmic = true; config.cosmicDisk_mm = std::stod(argv[++i]); }\n')
m.write_text(s)
g = R / 'src/X17PrimaryGenerator.cc'; s = g.read_text()
a = '    // zenith: dN/dθ ∝ cos³θ sinθ → cosθ = u^(1/4), θ < 85°\n'
assert s.count(a) == 1
s = s.replace(a, (
    '    if (c.cosmicDisk_mm > 0) {                // --cosmic-disk: start on a disk normal to the track\n'
    '        double ctd;\n'
    '        do { ctd = std::cbrt(G4UniformRand()); } while (ctd < std::cos(89.0 * deg));\n'
    '        const double std_ = std::sqrt(1 - ctd * ctd), phd = CLHEP::twopi * G4UniformRand();\n'
    '        G4ThreeVector d;                       // local (a, b, w=up) -> world\n'
    '        if (c.illVerticalAxis == \'x\') d = G4ThreeVector(-ctd, std_ * std::cos(phd), std_ * std::sin(phd));\n'
    '        else                           d = G4ThreeVector(std_ * std::cos(phd), std_ * std::sin(phd), -ctd);\n'
    '        const G4ThreeVector e1 = d.orthogonal().unit(), e2 = d.cross(e1).unit();\n'
    '        const double r = c.cosmicDisk_mm * std::sqrt(G4UniformRand()), ps = CLHEP::twopi * G4UniformRand();\n'
    '        const G4ThreeVector pos0 = (r * std::cos(ps)) * e1 + (r * std::sin(ps)) * e2 - (1.2 * c.cosmicDisk_mm) * d;\n'
    '        const bool plusd = G4UniformRand() < 1.27 / 2.27;\n'
    '        G4ParticleDefinition* mud = plusd ? fMuPlus : fMuMinus;\n'
    '        const double md = mud->GetPDGMass(), ppd = p_GeV * GeV;\n'
    '        fGun->SetParticleDefinition(mud);\n'
    '        fGun->SetParticlePosition(pos0 * mm);\n'
    '        fGun->SetParticleMomentumDirection(d);\n'
    '        fGun->SetParticleEnergy(std::sqrt(ppd * ppd + md * md) - md);\n'
    '        fGun->GeneratePrimaryVertex(event);\n'
    '        return p_GeV;\n'
    '    }\n' + a))
g.write_text(s)
print('ok')
