/* 3D event display of the Predictions tab (site/predict3d.js, inlined by build_page.py as a module).
   Geant4 frame (mm): beam +y, up +z.  three.js frame (cm): X = x, Y = z (up), Z = -y. */
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { CSS2DRenderer, CSS2DObject } from "three/addons/renderers/CSS2DRenderer.js";
import { Line2 } from "three/addons/lines/Line2.js";
import { LineMaterial } from "three/addons/lines/LineMaterial.js";
import { LineGeometry } from "three/addons/lines/LineGeometry.js";

const EVD = window.EVD;
const G = EVD.geometry;
const cssv = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const col = v => new THREE.Color(cssv(v) || "#888888");
const V3 = (x, y, z) => new THREE.Vector3(x / 10, z / 10, -y / 10);
const AX = [{ n: [1, 0, 0], t: [0, 0, 1] }, { n: [-1, 0, 0], t: [0, 0, 1] }, { n: [0, 0, 1], t: [1, 0, 0] }, { n: [0, 0, -1], t: [1, 0, 0] }];
let inited = false, renderer, scene, camera, controls, labels, world, evg, box, curArms = null;
let cur = 0, view = "iso";
const fatMats = [];
function fat(pts, c, w, op, dashed) {
  const g = new LineGeometry(); g.setPositions(pts.flatMap(p => [p.x, p.y, p.z]));
  const m = new LineMaterial({ color: c, linewidth: w, transparent: op < 1, opacity: op, dashed: !!dashed, dashSize: 1.0, gapSize: 0.8 });
  if (box) m.resolution.set(box.clientWidth, box.clientHeight);
  fatMats.push(m);
  const l = new Line2(g, m); if (dashed) l.computeLineDistances(); return l;
}
const opt = { sec: true, gam: true, seg: true };

function mat(c, op) { return new THREE.MeshBasicMaterial({ color: c, transparent: true, opacity: op, depthWrite: false, side: THREE.DoubleSide }); }
function edges(mesh, c, o) {
  const e = new THREE.LineSegments(new THREE.EdgesGeometry(mesh.geometry), new THREE.LineBasicMaterial({ color: c, transparent: true, opacity: o }));
  e.position.copy(mesh.position); e.rotation.copy(mesh.rotation); return e;
}
function label(text, pos) {
  const d = document.createElement("div"); d.className = "lbl3"; d.textContent = text;
  const o = new CSS2DObject(d); o.position.copy(pos); return o;
}
/* an axis-aligned slab of arm a: from r0 to r1 along the arm normal, u along its transverse axis, v along the beam */
function slab(a, r0, r1, u, v, tOff, c, op, eo) {
  const A = AX[a], sh = G.arm_shift[a] + (tOff || 0), rc = (r0 + r1) / 2;
  const cg = [0, 1, 2].map(k => A.n[k] * rc + A.t[k] * sh);
  const sg = [0, 1, 2].map(k => Math.abs(A.n[k]) * (r1 - r0) + Math.abs(A.t[k]) * u + (k === 1 ? v : 0));
  const m = new THREE.Mesh(new THREE.BoxGeometry(sg[0] / 10, sg[2] / 10, sg[1] / 10), mat(c, op));
  m.position.copy(V3(cg[0], cg[1], cg[2]));
  const g = new THREE.Group(); g.add(m); if (eo) g.add(edges(m, c, eo));
  return g;
}
function buildWorld(arms, hitArms) {
  if (world) { dropLabels(world); scene.remove(world); }
  world = new THREE.Group(); scene.add(world);
  const cMM = col("--ink-2"), cAct = col("--s3"), cS = col("--muted"), cHit = col("--s3");
  for (const a of arms) {
    const hit = hitArms.includes(a);
    for (const L of G.layers) {
      if (L.k === "mylar") world.add(slab(a, L.r0, L.r1 + 0.5, L.u, L.v, 0, cMM, 0.10));
      else if (L.k === "drift") world.add(slab(a, L.r0, L.r1, L.u, L.v, 0, cMM, 0.06, 0.45));
      else if (L.k === "active") world.add(slab(a, L.r0, L.r1, L.u, L.v, 0, cAct, 0.0, 0.7));
      else if (L.k === "pcb") world.add(slab(a, L.r0, L.r1, L.u, L.v, 0, cMM, 0.16));
      else if (L.k === "support") world.add(slab(a, L.r0, L.r1, L.u, L.v, 0, cS, 0.10, 0.25));
      else if (L.k === "sipm") {
        const w = L.u / L.bars;
        world.add(slab(a, L.r0, L.r1, L.u, L.v, 0, hit ? cHit : cS, hit ? 0.22 : 0.10, 0.45));
      } else if (L.k === "plastic") {
        for (const s of [-1, 1]) world.add(slab(a, L.r0, L.r1, L.u, L.v, s * (L.u + L.gap) / 2, hit ? cHit : cS, hit ? 0.22 : 0.08, 0.5));
      } else if (L.k === "ls") world.add(slab(a, L.r0, L.r1, L.u, L.v, 0, cS, 0.06, 0.35));
    }
    const A = AX[a], sh = G.arm_shift[a];
    const lp = (r, off) => V3(A.n[0] * r + A.t[0] * (sh + off), -150, A.n[2] * r + A.t[2] * (sh + off));
    world.add(label("Micromegas " + ["0 (+x)", "1 (−x)", "2 (top)", "3 (bottom)"][a], lp(224, 210)));
    if (a === arms[0]) world.add(label("SiPM wall", lp(331, -250)), label("plastics", lp(424, 215)), label("liquid cell", lp(482, -260)));
  }
  // Cu hemisphere (wall profile from the step points) and the beam line
  const prof = G.dome.map(([y, r]) => new THREE.Vector2(r / 10, y / 10));
  const dome = new THREE.Mesh(new THREE.LatheGeometry(prof, 48), mat(new THREE.Color("#b87333"), 0.45));
  dome.rotation.x = -Math.PI / 2; world.add(dome);
  for (const t of G.beamline) {
    const cyl = new THREE.Mesh(new THREE.CylinderGeometry(t.r1 / 10, t.r1 / 10, (t.y1 - t.y0) / 10, 40, 1, true), mat(cS, 0.16));
    cyl.rotation.x = -Math.PI / 2; cyl.position.z = -(t.y0 + t.y1) / 20; world.add(cyl);
  }
  const bl = new THREE.Line(new THREE.BufferGeometry().setFromPoints([V3(0, -620, 0), V3(0, 0, 0)]), new THREE.LineBasicMaterial({ color: col("--s8") }));
  world.add(bl, label("p beam →", V3(0, -560, 40)), label(EVD.target === "dome300" ? "Cu hemisphere (R 11 mm, 300 µm) + Li film" : "Cu ogive + Li film", V3(0, -40, -60)));
}
function dropLabels(g) { g.traverse(o => { if (o.isCSS2DObject && o.element.parentNode) o.element.parentNode.removeChild(o.element); }); }

const PCOL = { "e-": "--s1", "e+": "--s8", gamma: "--s4", "mu-": "--s7", "mu+": "--s7" };
function drawEvent(E) {
  if (evg) { dropLabels(evg); scene.remove(evg); }
  evg = new THREE.Group(); scene.add(evg);
  fatMats.length = 0;
  for (const t of E.tracks) {
    const prim = t.parent === 0;
    if (!prim && !opt.sec) continue;
    if (t.p === "gamma" && !opt.gam) continue;
    const pts = t.pts.map(p => V3(p[0], p[1], p[2]));
    const c = col(PCOL[t.p] || "--muted");
    const w = t.p === "gamma" ? 1.6 : prim ? 3.2 : 1.6;
    evg.add(fat(pts, c, w, prim ? 1 : 0.75, t.p === "gamma"));
  }
  if (opt.seg) for (const a of E.arms) {
    if (!a.seg) continue;
    const c = new THREE.Vector3(...a.seg.c), d = new THREE.Vector3(...a.seg.d).normalize();
    const p0 = c.clone().addScaledVector(d, -45), p1 = c.clone().addScaledVector(d, 45);
    evg.add(fat([V3(p0.x, p0.y, p0.z), V3(p1.x, p1.y, p1.z)], col("--ink"), 2.4, 1));
    const tt = -c.dot(d), pc = c.clone().addScaledVector(d, tt);
    const pl = new THREE.Line(new THREE.BufferGeometry().setFromPoints([V3(c.x, c.y, c.z), V3(pc.x, pc.y, pc.z)]),
      new THREE.LineDashedMaterial({ color: col("--ink-2"), dashSize: 0.5, gapSize: 0.7, transparent: true, opacity: 0.7 }));
    pl.computeLineDistances(); evg.add(pl);
  }
  const v = new THREE.Mesh(new THREE.SphereGeometry(0.12, 16, 12), new THREE.MeshBasicMaterial({ color: col("--ink") }));
  v.position.copy(V3(...E.vertex)); evg.add(v);
}
function info(E) {
  const b = document.getElementById("ev-info"); b.innerHTML = "";
  const tr = E.truth, kind = EVD.kinds[E.kind] || E.kind;
  const h3 = document.createElement("h3"); h3.style.marginTop = "0"; h3.textContent = kind; b.append(h3);
  const dl = document.createElement("dl");
  const add = (k, v) => { const dt = document.createElement("dt"); dt.textContent = k; const dd = document.createElement("dd"); dd.innerHTML = v; dl.append(dt, dd); };
  const isMu = E.kind.startsWith("mu"), isG = E.kind.startsWith("gam");
  if (isMu) add("muon", `${tr.em_ke >= 1000 ? (tr.em_ke / 1000).toFixed(1) + " GeV" : tr.em_ke.toFixed(0) + " MeV"}`);
  else if (isG) add("γ", `${tr.E} MeV`);
  else add("pair (truth)", `m<sub>ee</sub> ${tr.E} MeV, θ ${tr.theta}°, e⁻ ${tr.em_ke} + e⁺ ${tr.ep_ke} MeV`);
  add("reconstructed θ", E.theta_reco === null ? "– (one arm)" : `<b>${E.theta_reco}°</b> (charge centroids from the spot)`);
  for (const a of E.arms) add(`arm ${a.arm}`, `${a.leg ? "<b>leg</b>" : "no leg"} · ${a.mm ? "MM track" : "no MM track"}<br>SiPM ${a.E_sipm} · plastics ${a.E_plast} · liquid ${a.E_ls} MeV`);
  const t = E.arms.map(a => a.t);
  if (t[0] !== null && t[1] !== null) add("Δt (true)", `${(t[1] - t[0]).toFixed(2)} ns (arm ${E.arms[1].arm} − arm ${E.arms[0].arm})`);
  add("E in both arms", `${E.Esum} MeV (raw deposit)`);
  add("vertex", `(${E.vertex.map(v => v.toFixed(0)).join(", ")}) mm`);
  add("Geant4", `job ${E.job}, event ${E.eventID}, ${E.tracks.length} tracks drawn`);
  b.append(dl);
  const p = document.createElement("p"); p.className = "prcap";
  p.textContent = isMu ? "A cosmic muon crossing both arms looks like a back-to-back pair seen from the spot; its segments do not point to the target and its arm-to-arm time is ±2–3 ns, not 0."
    : isG ? (E.kind === "gam_trk" ? "The photon interacted in the Cu hemisphere wall; the electron it made crosses the drift gap: a single-arm trigger with a Micromegas track pointing back to the target."
      : "The photon crossed the chamber and converted behind the drift gap (readout PCB, support plate or SiPM wall): a leg with no track.")
      : E.kind === "x17" ? "Drawn as Geant4 tracks it. If ATOMKI is right, one ⁸Be decay in about 170,000 γ₀ goes this way; 18 such pairs a day would be selected." : "Both leptons cross the drift gap and fire the leg of their arm: a selected pair.";
  b.append(p);
}
function setView(k) {
  view = k;
  const P = k === "beam" ? [0, 0, 150] : k === "top" ? [0, 160, 0.01] : k === "target" ? [6, 2.2, -1.5] : [88, 58, 92];
  camera.position.set(...P); camera.up.set(0, 1, 0); controls.target.set(0, 0, k === "target" ? 0.6 : 0); controls.update();
  document.querySelectorAll("#ev-view button").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.v === k)));
  render();
}
function show(i) {
  cur = i; const E = EVD.events[i];
  const arms = E.kind === "mu_v" ? [2, 3] : [0, 1];
  buildWorld(arms, E.arms.filter(a => a.leg).map(a => a.arm)); curArms = arms.join();
  drawEvent(E); info(E);
  document.querySelectorAll("#ev-pick button").forEach(b => b.setAttribute("aria-pressed", String(+b.dataset.i === i)));
  render();
}
function picker() {
  const box = document.getElementById("ev-pick"); box.innerHTML = "";
  const seen = {};
  EVD.events.forEach((E, i) => {
    seen[E.kind] = (seen[E.kind] || 0) + 1;
    const b = document.createElement("button"); b.type = "button"; b.className = "chip btn"; b.dataset.i = i;
    const short = { ipc441: "441 keV pair", ipc1100: "1.10 MeV pair", x17: "X17 pair", gam_trk: "γ single, track", gam_notrk: "γ single, no track", mu_h: "muon, side arms", mu_v: "muon, vertical arms" }[E.kind] || E.kind;
    b.textContent = `${short} ${seen[E.kind]}` + (E.theta_reco ? ` · ${Math.round(E.theta_reco)}°` : "");
    b.addEventListener("click", () => show(i));
    box.append(b);
  });
}
function render() { if (renderer) { renderer.render(scene, camera); labels.render(scene, camera); } }
function resize() {
  if (!renderer) return;
  const w = box.clientWidth, hh = box.clientHeight;
  renderer.setSize(w, hh); labels.setSize(w, hh); fatMats.forEach(m => m.resolution.set(w, hh)); camera.aspect = w / hh; camera.updateProjectionMatrix(); render();
}
function init() {
  box = document.getElementById("ev3d");
  if (!box || !EVD || !EVD.events.length) return;
  if (inited) { resize(); return; }
  inited = true;
  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  box.innerHTML = ""; box.append(renderer.domElement);
  labels = new CSS2DRenderer(); labels.domElement.style.position = "absolute"; labels.domElement.style.top = "0"; labels.domElement.style.pointerEvents = "none";
  box.append(labels.domElement);
  scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(38, 1.6, 0.1, 3000);
  controls = new OrbitControls(camera, renderer.domElement); controls.addEventListener("change", render);
  new ResizeObserver(resize).observe(box);
  document.querySelectorAll("#ev-view button").forEach(b => b.addEventListener("click", () => setView(b.dataset.v)));
  for (const k of ["sec", "gam", "seg"]) document.getElementById("ev-" + k).addEventListener("change", e => { opt[k] = e.target.checked; drawEvent(EVD.events[cur]); render(); });
  document.getElementById("ev-png").addEventListener("click", () => {
    render(); const a = document.createElement("a"); a.href = renderer.domElement.toDataURL("image/png");
    a.download = `lnl_two_arm_${EVD.events[cur].kind}_${EVD.events[cur].eventID}.png`; a.click();
  });
  const rebuild = () => show(cur);
  new MutationObserver(rebuild).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", rebuild);
  picker();
  const first = EVD.events.findIndex(E => E.kind === "ipc1100");
  resize(); show(first >= 0 ? first : 0); setView("iso");
}
window.EV3D_init = init;
if (window.EV3D_want) init();
