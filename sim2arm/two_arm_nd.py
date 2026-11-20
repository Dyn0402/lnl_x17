#!/usr/bin/env python3
"""
two_arm_nd.py -- the FEASIBILITY_SIM §19 reference fit (x17_facility_search lnl/target/shapes/shapes_nd.py) run on
ONE PAIR OF ARMS of the four-arm Geant4 tables: the two-arm LNL feasibility set-up (lnl_x17 task R1, 2026-11-19).

Every merged table that lnl_geant / shapes_nd loads goes through lnl_geant._combine; this wrapper replaces it with a
version that keeps only events whose selected pair (a1, a2) is the requested pair.  Events with >= 3 ok arms are
< 0.2 % (cosmics) and 0 % (beam samples), so re-forming pairs from the per-arm data is not needed.  Normalisations
(cnt_n_generated) are untouched, so every rate is per day of the two-arm set-up.

Arms (MX17_Full_Geant, GEOMETRY_COORDINATE_CONVENTION.md; LNL runs: beam +y, up = +z):
    0 = +x (horizontal)  1 = -x (horizontal)  2 = +z (up)  3 = -z (down)
Pairs:  vert = (2, 3)  horiz = (0, 1)  adj = (0, 2) [one side + top]  adj_lo = (0, 3) [side + bottom]   all = 4 arms

Cosmics: the L15 disk sample (Cu hemisphere geometry, muons from every zenith angle, this study) when its merged chunks
exist ($L15_SEL/L15_cosmicdisk_ta4arm_c*_sel.npz), else L4 (Li2O baseline geometry, 1 live day, plane generator that
misses muons steeper than ~45 deg).  COSMICS=L4 forces the old sample.

    WORK_DATA=/media/dylan/data/work python3 sim2arm/two_arm_nd.py reach --pairs vert horiz adj all -j 3
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

os.environ.setdefault('WORK_DATA', '/media/dylan/data/work')
_W = Path(os.environ['WORK_DATA']) / 'x17_facility_search'
os.environ.setdefault('L13_SEL', str(_W / 'lnl_sel'))
os.environ.setdefault('L18_SEL', str(_W / 'sel_l18'))
FS = Path(os.environ.get('X17FS', Path.home() / 'PycharmProjects' / 'x17_facility_search'))
sys.path.insert(0, str(FS / 'lnl' / 'target' / 'shapes'))

import numpy as np            # noqa: E402
import pandas as pd           # noqa: E402

import shapes_nd as SN        # noqa: E402

G, S, C, N = SN.G, SN.S, SN.C, SN.N
HERE = Path(__file__).resolve().parent
OUT = HERE / 'out'
OUT.mkdir(exist_ok=True)
PAIRS = {'vert': (2, 3), 'horiz': (0, 1), 'adj': (0, 2), 'adj_lo': (0, 3), 'all': None}
L15_SEL = Path(os.environ.get('L15_SEL', _W / 'sel_l15'))
#: R11 (2026-11-20): the liquid cell right behind the SiPM wall, leg = SiPM AND (plastic OR liquid >= 1.7 MeV).
#: TA_LAYOUT=lsf16 swaps every dome300 table for the R11 run (beam samples and cosmics, same names with the R11 prefix).
LAYOUT = os.environ.get('TA_LAYOUT', '')
R11_SEL = Path(os.environ.get('R11_SEL', _W / 'sel_r11'))
SN.RUN_DIR['R11'] = R11_SEL
COS_SEL, COS_GLOB = ((R11_SEL, 'R11_cosmicdisk_dome300_lsf16_c*_sel.npz') if LAYOUT == 'lsf16'
                     else (L15_SEL, 'L15_cosmicdisk_ta4arm_c*_sel.npz'))
#: the target configuration of every two-arm number.  dome300 = the BUILT Cu hemisphere (R 11 mm, 300 µm wall, rim, grey
#: flange; SHAPES_GEANT.md).  Until 20 Nov the study used ogCu200, the Cu ogive of Pierfrancesco's 27 Oct sketch (not built)
#: under the name "Cu hemisphere": TA_CFG=ogCu200 reproduces those passes.
CFG = os.environ.get('TA_CFG', 'dome300')
PAIR = None
_COMBINE0 = G._combine
_LOAD0 = G._load


def pair_mask(z, pair):
    a1, a2 = np.asarray(z['a1']), np.asarray(z['a2'])
    p, q = pair
    return ((a1 == p) & (a2 == q)) | ((a1 == q) & (a2 == p))


def cut(z, pair):
    if pair is None or 'a1' not in z:
        return z
    m = pair_mask(z, pair)
    n = len(m)
    out = {}
    for k, v in z.items():
        out[k] = v[m] if isinstance(v, np.ndarray) and v.ndim >= 1 and len(v) == n and not k.startswith('cnt_') else v
    return out


def combine_pair(zs):
    return cut(_COMBINE0(zs), PAIR)


#: live seconds per generated muon: L4 plane (3 x 3 m, 1 /cm^2/min) and the L15 disk (R = 90 cm, A_eff = 4 pi R^2 / 3)
MU_LIVE_PLANE = 60.0 / (300.0 * 300.0)
MU_LIVE_DISK = 60.0 / (4 * np.pi / 3 * 90.0 ** 2)
COSMICS = os.environ.get('COSMICS', 'disk')      # 'disk' (L15, when merged) or 'L4'


def load_cos(run, sample, hw):
    """cosmics: the L15 disk sample (Cu hemisphere geometry, every zenith angle) replaces L4 when it is merged.
    L4's plane generator starts every muon 1.5 m above the target on a 3 x 3 m plane, so muons steeper than ~45 deg
    never reach the set-up's centre: it gives the horizontal pair 110 coincidences/day where the disk gives ~6,250.
    The disk table's n_generated is rescaled to L4 units (lnl_geant.MU_LIVE_S per muon)."""
    if run == 'L4' and sample == 'cosmic' and hw.startswith('as built') and COSMICS == 'disk':
        fl = sorted(COS_SEL.glob(COS_GLOB))      # merged in chunks of ~100 parts (L15; R11 with TA_LAYOUT=lsf16)
        if fl:
            zs = []
            for f in fl:      # memory: cut each chunk to the pair first; the big pairs also drop theta < 40 deg rows
                zc = cut(dict(np.load(f, allow_pickle=True)), PAIR)
                if PAIR in (None, (2, 3)):
                    m = np.asarray(zc['reco_c']) >= 40.0
                    n = len(m)
                    zc = {k: (v[m] if isinstance(v, np.ndarray) and v.ndim >= 1 and len(v) == n and not k.startswith('cnt_')
                              else v) for k, v in zc.items()}
                zs.append(zc)
            z = _COMBINE0(zs)
            f = fl[0]
            z['cnt_n_generated'] = np.array(int(round(int(z['cnt_n_generated']) * MU_LIVE_DISK / MU_LIVE_PLANE)))
            z['ngen'] = int(z['cnt_n_generated'])
            z['name'] = f.stem + ('|noLS' if hw in G.NO_LS else '')
            z['Esum'] = z['E_sipm2'] + z['E_plast2'] if hw in G.NO_LS else z['E1'] + z['E2']
            return z
    return _LOAD0(run, sample, hw)


def set_pair(name):
    global PAIR
    PAIR = PAIRS[name]
    G._combine = combine_pair
    G._load = load_cos
    G._CACHE.clear()
    G._SEG.clear()
    SN._TAB.clear()
    SN.RUNS['ogCu200'] = ['L11', 'L13']      # the dense as-built background MC of the Cu ogive (not built)
    SN.RUNS['dome300'] = ['L10', 'L18']      # the BUILT Cu hemisphere, R 11 mm, 300 µm (L18: lnl_x17, 20 Nov)
    if LAYOUT == 'lsf16':
        SN.RUNS['dome300'] = ['R11']         # the same hemisphere, liquid right behind the SiPM wall (R11)


RESPS = ['LNL calibrated', 'n_TOF as is', 'LNL calibrated, LS off']
#: Li film areal density for the yields [µg/cm²]; None = the simulated 20 µm (1068).  The target review recommends
#: 10-12 µm (LiOH conversion): LI_UG=587 is 11 µm (53.4 µg/cm² per µm); the Geant4 events stay those of the 20 µm run.
LI_UG = float(os.environ['LI_UG']) if os.environ.get('LI_UG') else None
LEVELS = ['trigger', 'MM 15°', 'MM 15° point, μ 3°', 'MM 15° point, μ 3° + TOF 1 ns', 'MM 15° + TOF', 'MM 3°']


def task(args):
    pair, cfg, resp, level, mc = args
    set_pair(pair)
    SN.register_levels()
    ec = SN.window('asb', resp)
    an = N.analyses(ec)[SN.REF_AN]
    t0 = time.time()
    try:
        ev = SN.collect(cfg, 'asb', 1100.0, resp, level=level, I_uA=1.0, live=SN.LIVE_S2,
                        transplant=mc == 'transplant', li_ug=LI_UG)
        _, _, names, out = SN.templates(ev, an, SN.REF_STRUCT)
        d_raw = SN.days_from(out, names)
        d_fl = SN.days_from(out, names, mu_floor=SN.mu_floor_of(ev, an, SN.FLOOR))
        mn = SN.mode_numbers(ev, ec)
        rc = SN.raw_counts(ev, an)
        try:
            cnt = SN.counting(ev, ec)
        except Exception:
            cnt = {}
        r = dict(pair=pair, config=cfg, resp=resp, level=level, mc=mc, ecut=f'{ec[0]:g}-{ec[1]:g}', li_ug=LI_UG or 1068.0,
                 days_floor1=d_fl, days_raw=d_raw, S_fitout=out['S'], B_fitout=out['B'], **mn, **rc,
                 **{f'cnt_{k}': v for k, v in cnt.items()}, g0_per_day=ev['meta']['g0_per_day'])
    except Exception as e:     # noqa: BLE001
        import traceback
        traceback.print_exc()
        r = dict(pair=pair, config=cfg, resp=resp, level=level, mc=mc, error=repr(e))
    print(f"{pair:6s} {resp:24s} {level:32s} {mc:10s}: floor {r.get('days_floor1', np.nan):.3g} d raw "
          f"{r.get('days_raw', np.nan):.3g}  S/d {r.get('S_win', np.nan):.3g} Bbeam {r.get('Bbeam_win', np.nan):.3g} "
          f"Bcos {r.get('Bcos_win', np.nan):.3g} ({r.get('n_mc_cos_win', -1)} MC)  {time.time() - t0:.0f}s", flush=True)
    SN._drop_tables()
    return r


TH_EDGES = np.arange(0, 181, 5.0)


def task_spectra(args):
    """(pair, cfg, resp, level, ep): selected pairs per day in 5° bins of the reconstructed opening angle, per
    component, inside the response's E_sum window and with no E_sum cut (beam, cosmics; X17 at R(ATOMKI))."""
    pair, cfg, resp, level, ep = args
    set_pair(pair)
    SN.register_levels()
    rows = []
    t0 = time.time()
    for elab, ec in (('win', SN.window('asb', resp)), ('none', (0.0, 60.0))):
        ev = SN.collect(cfg, 'asb', ep, resp, level=level, I_uA=1.0, live=SN.LIVE_S2, erange=ec, li_ug=LI_UG)
        th, E, w, comp = ev['v0']['th'], ev['v0']['E'], ev['w'], ev['comp']
        m0 = (E > ec[0]) & (E < ec[1])
        for c in np.unique(comp):
            m = m0 & (comp == c)
            h = np.histogram(th[m], TH_EDGES, weights=w[m])[0]
            n = np.histogram(th[m], TH_EDGES)[0]
            for i in range(len(h)):
                rows.append(dict(pair=pair, config=cfg, resp=resp, level=level, Ep_keV=ep, ewin=elab,
                                 ecut=f'{ec[0]:g}-{ec[1]:g}', comp=c, th_lo=TH_EDGES[i], th_hi=TH_EDGES[i + 1],
                                 rate_per_day=h[i], n_mc=int(n[i])))
        SN._drop_tables()
    tot = {}
    for r in rows:
        if r['ewin'] == 'win':
            tot[r['comp']] = tot.get(r['comp'], 0) + r['rate_per_day']
    print(f"spectra {pair:6s} {resp:24s} {level:28s} {ep:.0f}: " + ' '.join(f'{k} {v:.3g}' for k, v in tot.items())
          + f'  {time.time() - t0:.0f}s', flush=True)
    return rows


class Resumable:
    """one pickle per finished task in out/parts/<what><tag>/ (a crash or a restart keeps what is done)."""
    def __init__(self, fn, pdir):
        self.fn, self.pdir = fn, pdir

    def __call__(self, t):
        import hashlib
        import pickle
        f = self.pdir / (hashlib.md5(repr(t).encode()).hexdigest()[:16] + '.pkl')
        if f.exists():
            return pickle.loads(f.read_bytes())
        try:
            r = self.fn(t)
        except Exception as e:      # noqa: BLE001
            import traceback
            traceback.print_exc()
            print('FAILED', t, repr(e), flush=True)
            return [] if isinstance(t[-1], float) else dict(zip(('pair', 'config', 'resp', 'level', 'mc'), t), error=repr(e))
        f.write_bytes(pickle.dumps(r))
        return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('what', choices=['reach', 'quick', 'spectra'])
    ap.add_argument('--eps', nargs='+', type=float, default=[1100.0, 441.0])
    ap.add_argument('--pairs', nargs='+', default=['vert', 'horiz', 'adj', 'all'])
    ap.add_argument('--resps', nargs='+', default=RESPS)
    ap.add_argument('--levels', nargs='+', default=LEVELS)
    ap.add_argument('--mcs', nargs='+', default=['direct', 'transplant'])
    ap.add_argument('--cfg', default=CFG)
    ap.add_argument('--tag', default='')
    ap.add_argument('-j', type=int, default=3)
    a = ap.parse_args()
    if a.what == 'spectra':
        fn = task_spectra
        tasks = [(p, a.cfg, r, lv, ep) for p in a.pairs for r in a.resps for lv in a.levels for ep in a.eps]
    else:
        fn = task
        tasks = [(p, a.cfg, r, lv, mc) for p in a.pairs for r in a.resps for lv in a.levels for mc in a.mcs]
    print(f'{len(tasks)} tasks', flush=True)
    pdir = OUT / 'parts' / f'{a.what}{a.tag}'
    pdir.mkdir(parents=True, exist_ok=True)
    fn = Resumable(fn, pdir)
    if a.j > 1:
        import multiprocessing as mp
        with mp.get_context('fork').Pool(a.j, maxtasksperchild=1) as pool:
            rows = pool.map(fn, tasks, chunksize=1)
    else:
        rows = [fn(t) for t in tasks]
    if a.what == 'spectra':
        rows = [r for rr in rows for r in rr]
    df = pd.DataFrame(rows)
    f = OUT / f'two_arm_{a.what}{a.tag}.csv'
    df.to_csv(f, index=False)
    print('->', f)


if __name__ == '__main__':
    main()
