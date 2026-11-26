#!/usr/bin/env python3
"""scan_drift_hv.py -- per sub-run drift-cathode HV of every MX17 chamber, from the CAEN hv_monitor.csv logs.

Runs on lxplus (interactive, reads /eos directly): `ssh lxplus python3 - < scan_drift_hv.py > drift_hv_subruns.csv`.
For each run directory with run_config.json, maps each mx17 detector's drift channel (hv_channels.drift = [card, ch])
and summarises each sub-run's hv_monitor.csv: set value, vmon median / max, time held within 2 % of the set value,
max imon, and whether the channel tripped (vmon fell below 50 % of set, or power went off, while set > 0).
"""
import os, sys, csv, json, glob, statistics, datetime
ROOT = '/eos/experiment/ntof/data/x17'
AREAS = ['july_beam/runs', 'cosmic_bench/june_tests', 'cosmic_bench/det_1', 'cosmic_bench/det_0_old',
         'cosmic_bench/det_1_old', 'cosmic_bench/det_3_old', 'cosmic_bench/det_4_old', 'may_beam/runs', 'feb_beam/runs']
W = csv.writer(sys.stdout)
W.writerow(['area', 'run', 'subrun', 'det', 'description', 'gas', 't_start', 'set_V', 'vmon_med', 'vmon_max',
            'held_s', 'dur_s', 'imon_max_uA', 'tripped', 'n'])


def ts(s):
    try:
        return datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
    except Exception:
        return None


for area in AREAS:
    for cfgf in sorted(glob.glob(f'{ROOT}/{area}/*/run_config.json')):
        rdir = os.path.dirname(cfgf)
        try:
            cfg = json.load(open(cfgf))
        except Exception:
            continue
        dets = [(d['name'], d.get('description', ''), d['hv_channels']['drift']) for d in cfg.get('detectors', [])
                if d.get('det_type') == 'mx17' and 'drift' in d.get('hv_channels', {})]
        if not dets:
            continue
        gas = cfg.get('gas', '')
        for hv in sorted(glob.glob(f'{rdir}/*/hv_monitor.csv')):
            sub = os.path.basename(os.path.dirname(hv))
            try:
                rows = list(csv.DictReader(open(hv)))
            except Exception:
                continue
            if not rows:
                continue
            t0, t1 = ts(rows[0]['timestamp']), ts(rows[-1]['timestamp'])
            dur = (t1 - t0).total_seconds() if t0 and t1 else ''
            for name, desc, (c, k) in dets:
                key = f'{c}:{k}'
                if f'{key} vmon' not in rows[0]:
                    continue
                try:
                    vs = [float(r[f'{key} vmon']) for r in rows]
                    sets = [float(r[f'{key} v0']) for r in rows]
                    pw = [r[f'{key} power'] in ('1', 'True', 'true') for r in rows]
                    im = [float(r[f'{key} imon']) for r in rows]
                    tt = [ts(r['timestamp']) for r in rows]
                except Exception:
                    continue
                s = statistics.median(sets)
                held = 0.0
                for i in range(1, len(rows)):
                    if pw[i] and s > 0 and abs(vs[i] - sets[i]) <= 0.02 * max(sets[i], 1) and tt[i] and tt[i - 1]:
                        held += (tt[i] - tt[i - 1]).total_seconds()
                trip = any(sets[i] > 50 and (not pw[i] or vs[i] < 0.5 * sets[i]) for i in range(len(rows))
                           if i > 2)
                W.writerow([area, os.path.basename(rdir), sub, name, desc[:80], gas, rows[0]['timestamp'], s,
                            round(statistics.median(vs), 1), round(max(vs), 1), round(held), dur,
                            round(max(im), 4), int(trip), len(rows)])
        sys.stdout.flush()
