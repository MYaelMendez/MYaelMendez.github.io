// PC:// resolver v0.1 — bidirectional: æQR -> email, email -> æQR. Read-only.
const norm = (s) => (s || "").normalize("NFC").trim().toLowerCase()
  .replace(/^web\+pc:(\/\/)?/, "pc://").replace(/^pc:(?!\/\/)/, "pc://");
const keyOf = (s) => { s = norm(s); if (!s.includes("://") && !s.includes("@")) s = "pc://" + s; return s; };
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
let REG = null;
async function load() { if (!REG) REG = await (await fetch("registry.json")).json(); return REG; }
function find(q) {
  const k = keyOf(q);
  return REG.aliases.find((a) => norm(a.aeqr) === k || norm(a.address) === norm(q)) || null;
}
function render(q) {
  const out = document.getElementById("out");
  if (!q) { out.innerHTML = ""; return; }
  const a = find(q);
  if (!a) { out.innerHTML = `<div class="card"><b>perdido</b> · sin manifiesto para <code>${esc(q)}</code>. No invento rutas.</div>`; return; }
  const dir = norm(a.address) === norm(q) ? "email → æQR" : "æQR → email";
  out.innerHTML = `<div class="card"><div class="m">${dir}</div>
  <div><span class="k">æQR</span>${esc(a.aeqr)}</div>
  <div><span class="k">email</span><a href="mailto:${esc(a.address)}">${esc(a.address)}</a></div>
  <div><span class="k">agente</span>${esc(a.agent)}</div>
  <div><span class="k">ruta</span>${esc(a.route)}</div>
  <div><span class="k">agentes</span>${a.agents_may.map((x) => `<span class="tag">${esc(x)}</span>`).join("")}</div>
  <div><span class="k">solo humano</span>${a.human_only.map((x) => `<span class="tag h">${esc(x)}</span>`).join("")}</div>
  <div class="m" style="margin-top:8px">${esc(REG.status)} · ${esc(REG.change_rule)}</div></div>`;
}
(async () => {
  await load();
  document.getElementById("list").innerHTML = "Registro:<ul>" + REG.aliases.map((a) =>
    `<li><a href="#" data-q="${esc(a.aeqr)}">${esc(a.aeqr)}</a> ↔ ${esc(a.address)}</li>`).join("") + "</ul>";
  document.getElementById("list").addEventListener("click", (e) => {
    const q = e.target.dataset && e.target.dataset.q; if (q) { e.preventDefault(); document.getElementById("q").value = q; render(q); } });
  document.getElementById("f").addEventListener("submit", (e) => { e.preventDefault(); render(document.getElementById("q").value); });
  const q = new URLSearchParams(location.search).get("q") || "";
  document.getElementById("q").value = q; render(q);
})();
