/* ---------- predictions (site/predict.js, inlined by build_page.py) ---------- */
const P = __PRED__;
const EVD = __EVENTS__;
window.EVD = EVD;
const SUP = { "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹", "-": "⁻" };
const nf = (v, s = 3) => {
  if (v === null || v === undefined) return "–";
  if (Math.abs(v) >= 1e6) { const [m, e] = v.toExponential(1).split("e"); return (m.endsWith(".0") ? m.slice(0, -2) : m) + "×10" + String(+e).replace(/./g, c => SUP[c]); }
  return Number(v.toPrecision(s)).toLocaleString("en-GB");
};
const pct = (v, d = 0) => v === null || v === undefined ? "–" : (100 * v).toFixed(d) + " %";
const CC = { M1: "var(--s1)", E1: "var(--s2)", g1: "var(--s3)", epc: "var(--s4)", cos: "var(--s5)", sig: "var(--s7)" };

function prLegend(id, items) {
  const b = $("#" + id); if (!b) return; b.innerHTML = "";
  for (const [name, col, ln] of items) b.append(h("span", {}, h("i", { class: ln ? "ln" : "", style: `background:${col}` }), name));
}
function niceStep(span, n = 4) {
  const raw = span / n, p = Math.pow(10, Math.floor(Math.log10(raw))), f = raw / p;
  return (f < 1.5 ? 1 : f < 3 ? 2 : f < 7 ? 5 : 10) * p;
}
/* histogram chart: o = {edges, series:[{name,col,y,dash,err}], stacked, xr, xstep, xlab, ylab, band, log, H, unit, days} */
function prHist(id, o) {
  const box = $("#" + id); if (!box) return; box.innerHTML = "";
  const W = Math.max(box.clientWidth || 520, 280), H = o.H || 230, L = 54, R = 10, T = 10, B = 36;
  const e = o.edges, n = e.length - 1;
  const x0 = o.xr ? o.xr[0] : e[0], x1 = o.xr ? o.xr[1] : e[n];
  const bins = [...Array(n).keys()].filter(i => e[i] >= x0 - 1e-9 && e[i + 1] <= x1 + 1e-9);
  const X = v => L + (W - L - R) * (v - x0) / (x1 - x0);
  const tot = i => o.series.reduce((s, q) => s + (q.y[i] || 0), 0);
  const days = o.days || 1;
  const errOf = i => Math.sqrt(Math.max(tot(i), 0) * days) / days;
  let ymax = 0, ymin = Infinity;
  for (const i of bins) {
    if (o.stacked) ymax = Math.max(ymax, tot(i) + (o.errbars ? errOf(i) : 0));
    for (const q of o.series) { const v = q.y[i] || 0; if (!o.stacked) ymax = Math.max(ymax, v); if (v > 0) ymin = Math.min(ymin, v); }
  }
  if (!(ymax > 0)) ymax = 1;
  let Y, ticks = [];
  if (o.log) {
    const lo = Math.pow(10, Math.floor(Math.log10(Math.max(ymin, ymax * 1e-5)))), hi = Math.pow(10, Math.ceil(Math.log10(ymax * 1.2)));
    Y = v => T + (H - T - B) * (Math.log10(hi) - Math.log10(Math.max(v, lo))) / (Math.log10(hi) - Math.log10(lo));
    for (let v = lo; v <= hi * 1.001; v *= 10) ticks.push(v);
  } else {
    const st = niceStep(ymax), hi = Math.ceil(ymax * 1.05 / st) * st;
    Y = v => T + (H - T - B) * (1 - v / hi);
    for (let v = 0; v <= hi + 1e-9; v += st) ticks.push(v);
  }
  const svg = h("svg:svg", { width: W, height: H, viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": o.aria || o.ylab || "histogram" });
  if (o.band) svg.append(h("svg:rect", { x: X(o.band[0]), y: T, width: X(o.band[1]) - X(o.band[0]), height: H - T - B, fill: "var(--accent-wash)" }));
  for (const v of ticks) {
    svg.append(h("svg:line", { class: "gridl", x1: L, x2: W - R, y1: Y(v), y2: Y(v) }));
    svg.append(h("svg:text", { x: L - 6, y: Y(v) + 4, "text-anchor": "end", "font-size": 11 }, o.log ? (v >= 1 ? nf(v, 1) : String(v)) : nf(v, 3)));
  }
  const xs = o.xstep || niceStep(x1 - x0, 6);
  for (let v = Math.ceil(x0 / xs) * xs; v <= x1 + 1e-9; v += xs) svg.append(h("svg:text", { x: X(v), y: H - B + 15, "text-anchor": "middle", "font-size": 11 }, nf(v)));
  svg.append(h("svg:line", { x1: L, x2: W - R, y1: H - B, y2: H - B, stroke: "var(--axis)" }));
  svg.append(h("svg:text", { x: (L + W - R) / 2, y: H - 5, "text-anchor": "middle", "font-size": 11.5 }, o.xlab || ""));
  svg.append(h("svg:text", { x: 11, y: T + (H - T - B) / 2, "font-size": 11.5, transform: `rotate(-90 11 ${T + (H - T - B) / 2})`, "text-anchor": "middle" }, o.ylab || ""));
  if (o.stacked) {
    for (const i of bins) {
      let acc = 0; const xa = X(e[i]) + 1, wb = Math.max(X(e[i + 1]) - X(e[i]) - 2, 1);
      for (const q of o.series) {
        const v = q.y[i] || 0; if (v <= 0) continue;
        const ya = Y(acc + v), yb = Y(acc);
        svg.append(h("svg:rect", { x: xa, y: ya, width: wb, height: Math.max(yb - ya - (acc > 0 ? 1 : 0), 0.5), fill: q.col, rx: 1 }));
        acc += v;
      }
      if (o.errbars && acc > 0) {
        const er = errOf(i), xc = X((e[i] + e[i + 1]) / 2);
        svg.append(h("svg:line", { x1: xc, x2: xc, y1: Y(acc + er), y2: Y(Math.max(acc - er, 0)), stroke: "var(--ink)", "stroke-width": 1.3 }));
      }
    }
  } else {
    for (const q of o.series) {
      let d = "";
      for (const i of bins) { const v = q.y[i] || 0; const yv = Y(o.log && v <= 0 ? 0 : v); d += (d ? `L${X(e[i])},${yv}` : `M${X(e[i])},${yv}`) + `L${X(e[i + 1])},${yv}`; }
      svg.append(h("svg:path", { d, fill: "none", stroke: q.col, "stroke-width": 2, "stroke-dasharray": q.dash || null, "stroke-linejoin": "round" }));
    }
  }
  for (const [v, lab] of (o.vlines || [])) {
    svg.append(h("svg:line", { x1: X(v), x2: X(v), y1: T, y2: H - B, stroke: "var(--ink-2)", "stroke-dasharray": "4 3" }));
    svg.append(h("svg:text", { x: X(v) + 4, y: T + 12, "font-size": 11 }, lab));
  }
  const hl = h("svg:rect", { y: T, height: H - T - B, fill: "var(--hover)", opacity: 0 });
  svg.append(hl);
  for (const i of bins) {
    const r = h("svg:rect", { x: X(e[i]), y: T, width: X(e[i + 1]) - X(e[i]), height: H - T - B, fill: "transparent" });
    tipOn(r, () => {
      hl.setAttribute("x", X(e[i])); hl.setAttribute("width", X(e[i + 1]) - X(e[i])); hl.setAttribute("opacity", 1);
      const rows = o.series.map(q => `<span style="color:${q.col}">■</span> ${q.name}: <b>${nf(q.y[i] || 0)}</b>${q.n ? ` <span style="color:var(--muted)">(MC ${q.n[i]})</span>` : ""}`);
      if (o.stacked) rows.push(`total <b>${nf(tot(i))}</b>` + (o.errbars ? ` ± ${nf(errOf(i), 2)} in ${days} d` : ""));
      return `<b>${nf(e[i])}–${nf(e[i + 1])} ${o.xunit || ""}</b> · ${o.unit || ""}<br>` + rows.join("<br>");
    });
    r.addEventListener("mouseleave", () => hl.setAttribute("opacity", 0));
    svg.append(r);
  }
  box.append(svg);
}
/* line chart over x points: o = {x:[...], series:[{name,col,y}], xlab, ylab, ymin, ymax, fmt} */
function prLine(id, o) {
  const box = $("#" + id); if (!box) return; box.innerHTML = "";
  const W = Math.max(box.clientWidth || 520, 280), H = o.H || 210, L = 54, R = 12, T = 10, B = 36;
  const x0 = o.x[0], x1 = o.x[o.x.length - 1];
  let ymax = o.ymax || Math.max(...o.series.flatMap(q => q.y)) * 1.1, y0 = o.ymin || 0;
  const st = niceStep(ymax - y0); ymax = Math.ceil(ymax / st) * st;
  const X = v => L + (W - L - R) * (v - x0) / (x1 - x0), Y = v => T + (H - T - B) * (1 - (v - y0) / (ymax - y0));
  const svg = h("svg:svg", { width: W, height: H, viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": o.ylab });
  for (let v = y0; v <= ymax + 1e-9; v += st) {
    svg.append(h("svg:line", { class: "gridl", x1: L, x2: W - R, y1: Y(v), y2: Y(v) }));
    svg.append(h("svg:text", { x: L - 6, y: Y(v) + 4, "text-anchor": "end", "font-size": 11 }, o.fmt ? o.fmt(v) : nf(v)));
  }
  let lastX = -1e9;
  for (const v of o.x) { if (X(v) - lastX < 34) continue; lastX = X(v); svg.append(h("svg:text", { x: X(v), y: H - B + 15, "text-anchor": "middle", "font-size": 11 }, String(v))); }
  svg.append(h("svg:line", { x1: L, x2: W - R, y1: H - B, y2: H - B, stroke: "var(--axis)" }));
  svg.append(h("svg:text", { x: (L + W - R) / 2, y: H - 5, "text-anchor": "middle", "font-size": 11.5 }, o.xlab));
  svg.append(h("svg:text", { x: 11, y: T + (H - T - B) / 2, "font-size": 11.5, transform: `rotate(-90 11 ${T + (H - T - B) / 2})`, "text-anchor": "middle" }, o.ylab));
  for (const q of o.series) {
    svg.append(h("svg:polyline", { points: o.x.map((x, i) => `${X(x)},${Y(q.y[i])}`).join(" "), fill: "none", stroke: q.col, "stroke-width": 2 }));
    o.x.forEach((x, i) => {
      const c = h("svg:circle", { cx: X(x), cy: Y(q.y[i]), r: 4, fill: q.col, stroke: "var(--surface)", "stroke-width": 2 });
      tipOn(c, `<b>${q.name}</b><br>${x} µA: <b>${o.fmt ? o.fmt(q.y[i]) : nf(q.y[i])}</b>`);
      svg.append(c);
    });
  }
  box.append(svg);
}

function prTiles() {
  const c = P.cosmics.pairs, s = P.singles.ep, b4 = P.pairs["441"].ref, b11 = P.pairs["1100"].ref;
  const sel441 = ["M1", "E1", "g1", "epc"].reduce((a, k) => a + b4[k].per_day_win_gt90, 0);
  const T = $("#pr-tiles"); T.innerHTML = "";
  [["Cosmic pair triggers, arms vertical", nf(c.vert.trig_per_night), `per 10 h night (${nf(c.vert.trig_hz)} Hz); ${pct(c.vert.frac2_eps)} with both tracks × ε`],
   ["Same, arms horizontal", nf(c.horiz.trig_per_night), `per night: ${nf(c.vert.trig_hz / c.horiz.trig_hz, 2)}× fewer`],
   ["Beam legs per arm, 1 µA", nf(s["1100"].beam_leg_hz_per_uA) + " Hz", `at 1.10 MeV (${nf(s["441"].beam_leg_hz_per_uA)} Hz at 441 keV) + ${nf(P.singles.cos_side_leg_hz)} Hz cosmics`],
   ["441 keV calibration pairs", nf(sel441) + " / day", "selected, θ > 90°, E_sum window"],
   ["X17 at R(ATOMKI), 1.10 MeV", nf(b11.sig.per_day_win_gt90) + " / day", `on ${nf(["M1", "E1", "g1", "epc", "cos"].reduce((a, k) => a + b11[k].per_day_win_gt90, 0))} background pairs/day`]]
    .forEach(([k, v, sub]) => T.append(h("div", { class: "tile" }, h("div", { class: "k" }, k), h("div", { class: "v" }, v), h("div", { class: "s" }, sub))));
}

function prTable() {
  const c = P.cosmics.pairs, a = P.cosmics.arms, s = P.singles, b4 = P.pairs["441"], b11 = P.pairs["1100"];
  const sum = (o, ks, f) => ks.reduce((t, k) => t + (o[k][f] || 0), 0);
  const BEAM = ["M1", "E1", "g1", "epc", "sig"];
  const rows = [
    ["Cosmic nights, arms vertical (top + bottom)"],
    ["A1", "Trigger legs per arm", "beam off", `${nf((a[2].leg_hz + a[3].leg_hz) / 2)} Hz`, "scintillator thresholds, cosmic flux, geometry", `MC ${nf(a[2].n_mc)}`],
    ["A2", "Two-arm (PAIR) triggers", "beam off", `${nf(c.vert.trig_hz)} Hz`, `${nf(c.vert.trig_per_night)} per night`, `MC ${nf(c.vert.n_mc)}`],
    ["A3", "PAIR triggers with a Micromegas track in 2 / 1 / 0 arms", "beam off", `${pct(c.vert.frac2_eps)} / ${pct(c.vert.frac1_eps)} / ${pct(c.vert.frac0_eps, 1)}`,
      `in-situ chamber efficiency (simulation: ${pct(c.vert.frac2, 1)} / ${pct(c.vert.frac1, 1)} at ε = 1)`, ""],
    ["A4", "Two-track pairs at 125–160°", "beam off", `${pct(c.vert.frac_125_160)}`, `${nf(c.vert.per_day_125_160 * P.night_h / 24)} per night: the MEG II structure, measured`, ""],
    ["A5", "Δt lower − upper wall", `σ_t ${P.sigma_t_ns} ns`, `+${nf(c.vert.dt_true_mean, 2)} ns`, `${pct(c.vert.frac_downward)} downward: the TOF veto and σ_t`, ""],
    ["A6", "Pairs left in 125–160° after E_sum + pointing + TOF", "beam off", `${nf(c.vert.ref_win_125_160)} / day`, "the veto's rejection, end to end", `MC ${nf(c.vert.ref_win_125_160_nmc)}`],
    ["Cosmics, arms horizontal (the beam geometry)"],
    ["B1", "Trigger legs per side arm", "beam off", `${nf(P.singles.cos_side_leg_hz)} Hz`, "", `MC ${nf(a[0].n_mc)}`],
    ["B2", "PAIR triggers", "beam off", `${nf(c.horiz.trig_hz)} Hz`, `${nf(c.horiz.trig_per_night)} per night; ${nf(c.vert.trig_hz / c.horiz.trig_hz, 2)}× below vertical`, `MC ${nf(c.horiz.n_mc)}`],
    ["B3", "… with tracks in 2 / 1 / 0 arms", "beam off", `${pct(c.horiz.frac2_eps)} / ${pct(c.horiz.frac1_eps)} / ${pct(c.horiz.frac0_eps, 1)}`, "", ""],
    ["B4", "Pairs left in 125–160° after all cuts", "beam off", `${nf(c.horiz.ref_win_125_160)} / day`, "the cosmic background of the beam days", `MC ${nf(c.horiz.ref_win_125_160_nmc)}`],
    ["Beam singles (day 1, current scan)"],
    ["C1", "Beam trigger legs per side arm", "1.10 MeV / 441 keV", `${nf(s.ep["1100"].beam_leg_hz_per_uA)} / ${nf(s.ep["441"].beam_leg_hz_per_uA)} Hz per µA`,
      "γ yield × leg probability: the film's Li content; linear in current", `${nf(s.lines_gamma_per_line)} γ per line`],
    ["C2", "Beam legs with a Micromegas track", "1 µA", `${pct(s.ep["1100"].frac_track_eps)}`, `vs ${pct(P.cosmics.arms[0].frac_track_eps)} for cosmics: the γ conversions in the Cu hemisphere`, ""],
    ["C3", "Accidental two-arm coincidences (20 ns)", "1 µA, before cuts", `${nf(s.ep["1100"].accidental_pairs_per_day_1uA)} / ${nf(s.ep["441"].accidental_pairs_per_day_1uA)} per day`, "1.10 MeV / 441 keV; negligible after the cuts", ""],
    ["Pairs at 441 keV (day 2)"],
    ["D1", "Two-arm events with both tracks (any θ, any E)", "1 µA", `${nf(sum(b4.trigger, BEAM, "per_day"))} / day`, `+ ${nf(b4.trigger.cos.per_day)} cosmics/day`, ""],
    ["D2", "Selected pairs, θ > 90°, E_sum window", "pointing + TOF", `${nf(sum(b4.ref, ["M1", "E1", "g1", "epc"], "per_day_win_gt90"))} / day`,
      `M1 IPC ${nf(b4.ref.M1.per_day_win_gt90)}, conversions ${nf(b4.ref.epc.per_day_win_gt90)}, 14.6/15.1 IPC ${nf(b4.ref.g1.per_day_win_gt90)}; cosmics ${nf(b4.ref.cos.per_day_win_gt90)}`, `MC ${nf(b4.ref.M1.n_mc_win_gt90)} (M1)`],
    ["D3", "Selected pairs per beam leg", "441 keV", `${nf(P.ratio_pairs_per_leg_441 * 1e5, 3)}×10⁻⁵`, "independent of the film's Li content", ""],
    ["D4", "Opening-angle shape, E_sum peak, |y|", "441 keV", "§5 plots", "angular response and energy scale on a transition with no anomaly", ""],
    ["Pairs at 1.10 MeV (days 3–7)"],
    ["E1", "Selected background pairs", "pointing + TOF", `${nf(sum(b11.ref, ["M1", "E1", "g1", "epc", "cos"], "per_day_win_gt90"))} / day`,
      `E1 IPC ${nf(b11.ref.E1.per_day_win_gt90)}, 15.1 IPC ${nf(b11.ref.g1.per_day_win_gt90)}, M1 ${nf(b11.ref.M1.per_day_win_gt90)}, cosmics ${nf(b11.ref.cos.per_day_win_gt90)}`, `MC ${nf(b11.ref.E1.n_mc_win_gt90)} (E1)`],
    ["E2", "X17 at R(ATOMKI)", "θ > 90°, window", `${nf(b11.ref.sig.per_day_win_gt90)} / day`, "the reach (Beam & reach tab)", ""],
  ];
  const t = $("#pr-table"); t.innerHTML = "";
  t.append(h("thead", {}, h("tr", {}, ["#", "Observable", "Condition", "Geant4", "What it checks", "MC"].map((x, i) => h("th", { class: i === 3 ? "num" : "" }, x)))));
  const tb = h("tbody");
  for (const r of rows) {
    if (r.length === 1) { tb.append(h("tr", {}, h("td", { class: "stage", colspan: 6 }, r[0]))); continue; }
    tb.append(h("tr", {}, h("td", { class: "small muted" }, r[0]), h("td", {}, r[1]), h("td", { class: "small" }, r[2]), h("td", { class: "v num" }, r[3]),
      h("td", { class: "small" }, r[4]), h("td", { class: "small muted" }, r[5])));
  }
  t.append(tb);
}

function prCharts() {
  const c = P.cosmics.pairs, nightK = P.night_h / 24;
  const sc = (hst, k = 1) => hst.y.map(v => (v || 0) * k);
  prLegend("pc-th-l", [["arms vertical", "var(--s1)", 1], ["arms horizontal", "var(--s2)", 1]]);
  prHist("pc-th", { edges: c.vert.theta.edges, series: [{ name: "vertical", col: "var(--s1)", y: sc(c.vert.theta, nightK), n: c.vert.theta.n }, { name: "horizontal", col: "var(--s2)", y: sc(c.horiz.theta, nightK), n: c.horiz.theta.n }],
    log: true, band: [125, 160], xlab: "opening angle θ (°)", ylab: "pairs per 5° per night", xstep: 30, unit: "per night", xunit: "°" });
  prLegend("pc-dt-l", [["vertical (lower − upper)", "var(--s1)", 1], ["horizontal (−x − +x)", "var(--s2)", 1]]);
  prHist("pc-dt", { edges: c.vert.dt.edges, series: [{ name: "vertical", col: "var(--s1)", y: sc(c.vert.dt, nightK), n: c.vert.dt.n }, { name: "horizontal", col: "var(--s2)", y: sc(c.horiz.dt, nightK), n: c.horiz.dt.n }],
    log: true, xlab: "Δt (ns)", ylab: "pairs per 0.25 ns per night", xstep: 2, unit: "per night", xunit: "ns", vlines: [[0, "beam pairs"]] });
  prLegend("pc-dca-l", [["true segment", "var(--ink-2)", 1], ["15° resolution", "var(--s1)", 1], ["3° resolution", "var(--s3)", 1]]);
  prHist("pc-dca", { edges: c.vert.dca_true.edges, series: [{ name: "true", col: "var(--ink-2)", y: sc(c.vert.dca_true, nightK), dash: "4 3" }, { name: "15°", col: "var(--s1)", y: sc(c.vert.dca_15, nightK) }, { name: "3°", col: "var(--s3)", y: sc(c.vert.dca_3, nightK) }],
    xlab: "distance of closest approach to the spot (mm)", ylab: "pairs per 10 mm per night", xstep: 50, unit: "vertical pair, per night", xunit: "mm",
    vlines: [[P.seg_D_15, "cut 15°"], [P.seg_D_3, "3°"]] });
  prLegend("pc-zen-l", [["vertical pair", "var(--s1)", 1], ["horizontal pair", "var(--s2)", 1]]);
  prHist("pc-zen", { edges: c.vert.zenith.edges, series: [{ name: "vertical", col: "var(--s1)", y: sc(c.vert.zenith, nightK) }, { name: "horizontal", col: "var(--s2)", y: sc(c.horiz.zenith, nightK) }],
    log: true, xlab: "muon zenith angle (°)", ylab: "pairs per 5° per night", xstep: 15, unit: "per night", xunit: "°" });

  const s = P.singles.ep, I = s["1100"].scan.map(r => r.I_uA);
  prLegend("ps-I-l", [["441 keV", "var(--s2)", 1], ["1.10 MeV", "var(--s1)", 1]]);
  prLine("ps-I", { x: I, series: [{ name: "441 keV", col: "var(--s2)", y: s["441"].scan.map(r => r.leg_hz) }, { name: "1.10 MeV", col: "var(--s1)", y: s["1100"].scan.map(r => r.leg_hz) }],
    xlab: "beam current (µA)", ylab: "legs per second, one arm" });
  prLegend("ps-F-l", [["441 keV", "var(--s2)", 1], ["1.10 MeV", "var(--s1)", 1]]);
  prLine("ps-F", { x: I, series: [{ name: "441 keV", col: "var(--s2)", y: s["441"].scan.map(r => r.track_frac * P.eps_mm) }, { name: "1.10 MeV", col: "var(--s1)", y: s["1100"].scan.map(r => r.track_frac * P.eps_mm) }],
    xlab: "beam current (µA)", ylab: "legs with a track (× ε)", ymin: 0.3, ymax: 0.6, fmt: v => pct(v) });
  const ce = P.singles.cos_E_hist_leg_track;
  prLegend("ps-E-l", [["beam, 441 keV", "var(--s2)", 1], ["beam, 1.10 MeV", "var(--s1)", 1], ["cosmics", "var(--s5)", 1]]);
  prHist("ps-E", { edges: s["1100"].E_hist.leg_track.edges, series: [{ name: "441 keV", col: "var(--s2)", y: s["441"].E_hist.leg_track.y }, { name: "1.10 MeV", col: "var(--s1)", y: s["1100"].E_hist.leg_track.y }, { name: "cosmics", col: "var(--s5)", y: ce ? ce.y : [] }],
    log: true, xlab: "energy in one arm (MeV, raw deposit)", ylab: "per s per MeV, one arm", xstep: 5, unit: "1 µA", xunit: "MeV" });
  const tb = $("#ps-tab"); tb.innerHTML = "";
  const tt = h("table", {}, h("thead", {}, h("tr", {}, h("th", {}, ""), h("th", { class: "num" }, "441 keV"), h("th", { class: "num" }, "1.10 MeV"))));
  const body = h("tbody");
  [["γ₀ at the target (17.64 + 18.15)", "g0_per_s", " /s"], ["beam legs per arm", "beam_leg_hz_per_uA", " Hz"], ["… with a Micromegas track (× ε)", "frac_track_eps", "", pct],
   ["legs per arm incl. cosmics", "total_leg_hz_1uA_side", " Hz"], ["beam / cosmic legs", "beam_over_cosmic_side", "×"], ["accidental pairs, 20 ns", "accidental_pairs_per_day_1uA", " /day"]]
    .forEach(([k, f, u, fm]) => body.append(h("tr", {}, h("td", {}, k), ...["441", "1100"].map(ep => h("td", { class: "num" }, fm ? fm(s[ep][f]) : nf(s[ep][f]) + u)))));
  tt.append(body); tb.append(tt);
  tb.append(h("p", { class: "prcap" }, "Per-γ leg probability ", nf(P.singles.p_leg_per_gamma["18.15"] * 1e3, 2), "×10⁻³ per arm (18.15 MeV), the same for the four lines within 5 %. The 478 keV ⁷Li line never makes a leg."));

  // 441 keV and 1.10 MeV pairs
  const win = $("#p4-win").checked, dd = +$("#p4-days").value; $("#p4-days-v").textContent = dd;
  const stack = (ref, keys, f) => keys.map(k => ({ name: P.comp_names[k], col: CC[k], y: ref[k][f].y, n: ref[k][f].n }));
  const ORD4 = ["M1", "epc", "g1", "E1", "cos"];
  prLegend("p4-th-l", ORD4.map(k => [P.comp_names[k], CC[k]]));
  const r4 = P.pairs["441"].ref;
  prHist("p4-th", { edges: r4.M1.theta_win.edges, series: stack(r4, ORD4, win ? "theta_win" : "theta_all"), stacked: true, errbars: true, days: dd, xr: [90, 180],
    band: [125, 160], xlab: "opening angle θ (°)", ylab: "pairs per 5° per day", xstep: 15, unit: "per day, 441 keV", xunit: "°", H: 250 });
  prLegend("p4-E-l", ORD4.map(k => [P.comp_names[k], CC[k]]));
  prHist("p4-E", { edges: r4.M1.Esum_gt90.edges, series: stack(r4, ORD4, "Esum_gt90"), stacked: true, xr: [5, 25], xlab: "E_sum (MeV)", ylab: "per 0.5 MeV per day", xstep: 5,
    unit: "θ > 90°, per day", xunit: "MeV", band: P.pairs.ewin, H: 200 });
  prHist("p4-y", { edges: r4.M1.y_win_gt90.edges, series: stack(r4, ORD4, "y_win_gt90"), stacked: true, xlab: "|y| energy sharing", ylab: "per 0.05 per day", xstep: 0.2,
    unit: "θ > 90°, window, per day", H: 170 });
  const r11 = P.pairs["1100"].ref, ORD11 = ["E1", "g1", "M1", "epc", "cos", "sig"];
  prLegend("p11-th-l", ORD11.map(k => [P.comp_names[k], CC[k]]));
  prHist("p11-th", { edges: r11.E1.theta_win.edges, series: stack(r11, ORD11, win ? "theta_win" : "theta_all"), stacked: true, errbars: true, days: dd, xr: [90, 180],
    band: [125, 160], xlab: "opening angle θ (°)", ylab: "pairs per 5° per day", xstep: 15, unit: "per day, 1.10 MeV", xunit: "°", H: 250 });
  const t11 = $("#p11-txt"); t11.innerHTML = "";
  [["Rates", "Every absolute rate (A1–A2, B1–B2, C1, D1–D2) tests the flux, the γ yields and the trigger thresholds together. Ratios (D3, A2/B2) cancel the yield or the flux."],
   ["Chamber efficiency", "A3/B3: a cosmic PAIR trigger with one track instead of two is a chamber that missed it. The simulation is 100 % efficient, so the measured 1-track fraction gives ε for each chamber in situ, per night."],
   ["Shapes", "The 441 keV θ, E_sum and |y| distributions have no free parameter once the rate is fixed: they test the angular response, the energy scale and the IPC model on a transition where ATOMKI saw nothing."],
   ["The cosmic veto", "A4–A6: the vertical nights show the full 140° structure and how much of it pointing and TOF remove. If A6 comes out well above the prediction, the beam-day cosmics (B4) are underestimated too."],
   ["The film", "C1 and D1 scale with the Li content of the film (LiOH conversion, thickness); C2 and D3 do not."]]
    .forEach(([k, v]) => t11.append(h("p", { style: "margin:0 0 8px" }, h("b", {}, k + ". "), v)));
}

function prCaveats() {
  const b = $("#pr-cav"); b.innerHTML = "";
  const go = P.gam_origin || (EVD.gam_origin || null);
  const items = [
    ["The n_TOF check of the cosmic simulation (2026, beam off, arms A + C).", " The zenith-angle shape of A–C muon pairs matched the expectation (median 73.6° measured, 74.4° predicted); the rate did not at first (0.063 Hz against 0.161 Hz). The factor 2.5 is the reconstruction's track gate, tuned on capsule tracks: 57 % of clean A–C muons fail it in at least one arm. Without the gate the rate is 0.11–0.17 Hz, consistent. Still open: the A–C wall coincidences without chambers, 0.84 Hz measured against 0.34 Hz predicted (nTof_x17 ntof_cosmics/ac_cosmic_rate.py; to understand before quoting absolute cosmic rates)."],
    ["Cosmic flux.", " The L15 generator is 1 μ/cm²/min at sea level, open sky, cos²θ; the LNL hall roof lowers it a little (not modelled)."],
    ["Chamber efficiency.", ` ε = ${P.eps_mm} from the bench (91–93 % within 5 mm) applied per chamber where marked; the track definition is the simulation's (dominant segment, ≥ 3 steps, centroid in the active area), so a reconstruction gate like n_TOF's would cut further.`],
    ["Beam backgrounds not simulated.", " Room background, beam-line activation, target contaminants (¹⁹F, ¹¹B, ¹³C), neutrons (none expected below the ⁷Li(p,n) threshold at 1.88 MeV). The singles prediction is the 8Be γ part: measure beam-on minus beam-off, and anything above the prediction is these."],
    ["Thin Monte Carlo.", ` The external conversions at 441 keV rest on ${P.pairs["441"].ref.epc.n_mc_win_gt90} simulated events after the selection (the hover shows the count per bin): good to a factor ~2, and ~25 % of the selected 441 keV sample, so D2 is uncertain by about ±20 % (task R6). The spike in |y| is one of those events.`],
    ["Energies.", " The single-arm spectra are raw Geant4 deposits (no light yield, quenching or resolution); the pair E_sum and |y| plots include the LNL-calibrated response."],
    ["Yields.", " 11 µm Li in the Cu hemisphere, the x17_facility_search film yields; a 20 µm film or LiOH conversion changes C1 and D1–E2 by the same factor."],
  ];
  for (const [k, v] of items) b.append(h("p", { style: "margin:0 0 8px" }, h("b", {}, k), v));
}

let prDone = false;
function predict() {
  $("#pr-made").textContent = fmtY(P.made);
  $("#pr-eps").textContent = P.eps_mm; $("#pr-sigt").textContent = P.sigma_t_ns;
  $("#pr-D15").textContent = Math.round(P.seg_D_15); $("#pr-D3").textContent = Math.round(P.seg_D_3);
  $("#pr-cosfrac").textContent = pct(P.cosmics.arms[0].frac_track_eps) + " (× ε)";
  $("#pr-gamfrac").textContent = pct(P.singles.ep["1100"].frac_track_eps) + " (× ε)";
  const go = EVD.gam_origin;
  $("#pr-gorig").textContent = go ? `${go.track["Cu hemisphere"] || 0} of ${Object.values(go.track).reduce((a, b) => a + b, 0)} drawn-sample singles with a track` : "";
  if (!prDone) {
    $("#p4-win").addEventListener("change", prCharts);
    $("#p4-days").addEventListener("input", prCharts);
    prDone = true;
  }
  prTiles(); prTable(); prCharts(); prCaveats();
  if (window.EV3D_init) window.EV3D_init(); else window.EV3D_want = true;
}
