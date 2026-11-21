"""r11_diag.py -- R11 diagnostic (21 Nov): days of the horizontal pair, MM 15° + TOF, one response, with and without the
structure terms and the gain nuisance.  Env: TA_LAYOUT=lsf16 (R11) or unset (L18), RESP, COS (cosmic scale), LI_UG.
Raw fits (no floor): with thin MC they are unstable (see LIQUID_CELLS.md §4.1)."""
import sys, os
sys.path.insert(0, '/home/dylan/PycharmProjects/lnl_x17/sim2arm')
import two_arm_nd as T
SN, N, S = T.SN, T.N, T.S
pair, resp, level = 'horiz', os.environ.get('RESP','LNL calibrated'), 'MM 15° + TOF'
for mc in ['direct']:
    T.set_pair(pair); SN.register_levels()
    ec = SN.window('asb', resp); an = N.analyses(ec)[SN.REF_AN]
    ev = SN.collect(T.CFG, 'asb', 1100.0, resp, level=level, I_uA=1.0, live=SN.LIVE_S2, transplant=mc == 'transplant', li_ug=T.LI_UG, cos_scale=float(os.environ.get('COS','1')))
    out = {}
    for st in ['none', SN.REF_STRUCT]:
        _, _, names, o = SN.templates(ev, an, st)
        out[st] = SN.days_from(o, names)
    pg = S.PRIOR_G; S.PRIOR_G = None
    _, _, names, o = SN.templates(ev, an, 'none'); out['none,no gain'] = SN.days_from(o, names); S.PRIOR_G = pg
    print(os.environ.get('TA_LAYOUT') or 'L18', mc, {k: round(v, 1) for k, v in out.items()}, flush=True)
    SN._drop_tables()
