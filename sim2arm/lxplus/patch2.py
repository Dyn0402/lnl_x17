import pathlib
d = pathlib.Path('/afs/cern.ch/work/d/dneff/git/x17_lnl/MX17_Full_Geant_twoarm/src/DetectorConstruction.cc')
s = d.read_text()
old = '        const auto& ad = adr;\n'
new = ('        const auto& ad = adr;\n'
       '        // G4PVPlacement takes the FRAME (inverse) rotation while the position math uses ad.rot actively; the\n'
       '        // original 90/180 deg arms are symmetric under that swap, an arbitrary phi is not: keep the solids\'\n'
       '        // original orientation P0^-1 and turn it by Rphi (active) -> frame rotation P0 * Rphi^-1.\n'
       '        G4RotationMatrix* placeRot = armDefs[arm].rot;\n'
       '        if (fConfig.arm_phi_deg[arm] != 0.0) {\n'
       '            G4RotationMatrix Rphi; Rphi.rotateY(fConfig.arm_phi_deg[arm] * deg);\n'
       '            placeRot = new G4RotationMatrix((armDefs[arm].rot ? *armDefs[arm].rot : G4RotationMatrix()) * Rphi.inverse());\n'
       '        }\n')
assert s.count(old) == 1
s = s.replace(old, new)
old2 = '            new G4PVPlacement(ad.rot, worldPos, lv,\n'
assert s.count(old2) == 1
s = s.replace(old2, '            new G4PVPlacement(placeRot, worldPos, lv,\n')
d.write_text(s)
print('ok')
