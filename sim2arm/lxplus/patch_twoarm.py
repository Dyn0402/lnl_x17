import re, pathlib
R = pathlib.Path('/afs/cern.ch/work/d/dneff/git/x17_lnl/MX17_Full_Geant_twoarm')
h = R / 'include/SimConfig.hh'
s = h.read_text()
anchor = '    double mm_pinwheel_shift_cm[4] = {1.55, 1.575, 1.635, 1.73};\n'
assert anchor in s
s = s.replace(anchor, anchor + (
    '    // Two-arm studies (lnl_x17, 2026-11-19): extra rotation of each arm about the beam (+Y) axis [deg]\n'
    '    // (--arm-phi p0,p1,p2,p3; G4 rotateY sense: +Z turns toward +X) and which arms are built (--arms 2,3).\n'
    '    double arm_phi_deg[4] = {0, 0, 0, 0};\n'
    '    bool   arm_on[4]      = {true, true, true, true};\n'))
h.write_text(s)
m = R / 'mx17_full_sim.cc'
s = m.read_text()
anchor = '        else if (a == "--no-ls") config.noLS = true;\n'
assert anchor in s
s = s.replace(anchor, anchor + (
    '        else if (a == "--arm-phi" && i+1<argc) {   // p0,p1,p2,p3 [deg] about the beam axis\n'
    '            std::string v = argv[++i]; size_t p0 = 0;\n'
    '            for (int k = 0; k < 4; ++k) { size_t c = v.find(\',\', p0);\n'
    '                config.arm_phi_deg[k] = std::stod(v.substr(p0, c - p0));\n'
    '                if (c == std::string::npos) break; p0 = c + 1; }\n'
    '        }\n'
    '        else if (a == "--arms" && i+1<argc) {      // comma list of the arms to build, e.g. 2,3\n'
    '            std::string v = argv[++i];\n'
    '            for (int k = 0; k < 4; ++k) config.arm_on[k] = false;\n'
    '            for (char ch : v) if (ch >= \'0\' && ch <= \'3\') config.arm_on[ch - \'0\'] = true;\n'
    '        }\n'))
anchor2 = '              << "  --no-ls          omit the LS vessels\\n"\n'
assert anchor2 in s
s = s.replace(anchor2, anchor2 + '              << "  --arm-phi p0,p1,p2,p3  rotate each arm about the beam axis [deg]\\n"\n'
                                  '              << "  --arms 2,3       build only these arms\\n"\n')
m.write_text(s)
d = R / 'src/DetectorConstruction.cc'
s = d.read_text()
old = ('    for (int arm = 0; arm < 4; ++arm) {\n'
       '        const auto& ad = armDefs[arm];\n')
assert old in s
new = ('    for (int arm = 0; arm < 4; ++arm) {\n'
       '        // two-arm studies: rotate the arm about the beam axis, or leave it out\n'
       '        ArmDef adr = armDefs[arm];\n'
       '        if (fConfig.arm_phi_deg[arm] != 0.0) {\n'
       '            G4RotationMatrix Rphi; Rphi.rotateY(fConfig.arm_phi_deg[arm] * deg);\n'
       '            adr.rot = new G4RotationMatrix(Rphi * (armDefs[arm].rot ? *armDefs[arm].rot : G4RotationMatrix()));\n'
       '            adr.frontFace = Rphi * armDefs[arm].frontFace;\n'
       '            adr.uHat = Rphi * armDefs[arm].uHat;\n'
       '            adr.wHat = Rphi * armDefs[arm].wHat;\n'
       '        }\n'
       '        const auto& ad = adr;\n'
       '        if (!fConfig.arm_on[arm]) {\n'
       '            fArmAxes[arm].frontFace = ad.frontFace; fArmAxes[arm].uHat = ad.uHat;\n'
       '            fArmAxes[arm].vHat = G4ThreeVector(0, 1, 0); fArmAxes[arm].wHat = ad.wHat;\n'
       '            G4cout << "  Arm " << arm << " not built (--arms)" << G4endl;\n'
       '            continue;\n'
       '        }\n')
s = s.replace(old, new)
d.write_text(s)
print('patched')
