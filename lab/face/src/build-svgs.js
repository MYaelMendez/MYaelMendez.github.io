// node src/build-svgs.js → lab/face/moods/<mood>.svg (static, holomesh style)
const fs = require("fs"), path = require("path");
const C = require("./core.js");
const OUT = path.join(__dirname, "..", "moods");
fs.mkdirSync(OUT, { recursive: true });
const G = "#D4AF37", CY = "#39e6ff", V = "#05060a", HOT = "#ff3b6b";
const esc = s => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;");
function overlay(m) {
  switch (m) {
    case "hold": return `<g opacity=".75"><path d="${C.facePath("hold")}" stroke="${CY}" transform="translate(-4 1)" opacity=".55"/><path d="${C.facePath("hold")}" stroke="${HOT}" transform="translate(4 -1)" opacity=".55"/></g>
  <g fill="${HOT}" opacity=".5"><rect x="40" y="150" width="120" height="3"/><rect x="250" y="262" width="110" height="2"/><rect x="70" y="330" width="60" height="2"/></g>
  <text x="200" y="18" text-anchor="middle" font-family="Orbitron,JetBrains Mono,monospace" font-size="13" fill="${HOT}" letter-spacing="3">⚠ HOLD · FAULT LATCHED</text>`;
    case "lost": return `<g fill="none" stroke="${CY}" opacity=".5"><circle cx="200" cy="210" r="168" stroke-dasharray="3 7"/><path d="M200 210L338 115" stroke-width="2" opacity=".8"/><path d="M200 210L338 115A168 168 0 0 1 366 190Z" fill="${CY}" fill-opacity=".08" stroke="none"/></g>
  <text x="352" y="72" text-anchor="end" font-family="JetBrains Mono,monospace" font-size="16" fill="${CY}">? ? ?</text>`;
    case "tired": return `<g transform="translate(318 50)" fill="none" stroke="${G}" stroke-width="2"><rect x="0" y="0" width="44" height="20" rx="3"/><rect x="44" y="6" width="4" height="8" fill="${G}"/><rect x="3" y="3" width="7" height="14" fill="${HOT}" stroke="none"/></g>`;
    case "sleep": return `<g font-family="Orbitron,JetBrains Mono,monospace" fill="${CY}"><text x="300" y="120" font-size="20" opacity=".9">z</text><text x="324" y="92" font-size="28" opacity=".7">z</text><text x="352" y="58" font-size="38" opacity=".5">Z</text></g>`;
    case "think": return `<g fill="${CY}"><circle cx="318" cy="96" r="5"/><circle cx="338" cy="74" r="7" opacity=".75"/><circle cx="362" cy="48" r="10" opacity=".5"/></g>`;
    case "ready": return `<g fill="none" stroke="${CY}"><circle cx="200" cy="215" r="176" opacity=".35"/><circle cx="200" cy="215" r="186" opacity=".15" stroke-dasharray="2 10"/></g>
  <text x="200" y="398" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="11" fill="${CY}" letter-spacing="2">ARMED · MOVE ALLOWED</text>`;
    case "work": return `<g><rect x="20" y="226" width="360" height="2" fill="${CY}" opacity=".7"/><rect x="20" y="214" width="360" height="26" fill="${CY}" opacity=".07"/></g>
  <g stroke="${CY}" stroke-width="2" opacity=".6"><path d="M30 380h20M60 380h20M90 380h20"/><path d="M290 380h20M320 380h20M350 380h20"/></g>`;
  }
  return "";
}
function svg(m) {
  const [r, l, pr] = C.pupils(m);
  const pup = pr ? `<g fill="${CY}"><circle cx="${r[0]}" cy="${r[1]}" r="${pr}"/><circle cx="${l[0]}" cy="${l[1]}" r="${pr}"/></g>` : "";
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 480" width="800" height="960" role="img" aria-label="æ æ æ face · ${m}">
  <title>æ æ æ · :${m} · ${esc(C.MEANS[m])}</title>
  <defs><pattern id="g" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="${CY}" stroke-opacity=".08"/></pattern>
  <radialGradient id="h" cx=".5" cy=".42" r=".6"><stop offset="0" stop-color="${G}" stop-opacity=".14"/><stop offset="1" stop-color="${V}" stop-opacity="0"/></radialGradient>
  <filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
  <rect width="400" height="480" fill="${V}"/><rect width="400" height="480" fill="url(#g)"/><rect width="400" height="480" fill="url(#h)"/>
  <g fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="3">${overlay(m)}</g>
  <text x="200" y="40" text-anchor="middle" font-family="Orbitron,JetBrains Mono,monospace" font-weight="900" font-size="22" fill="${G}" letter-spacing="8">æ æ æ</text>
  <path d="${C.facePath(m)}" fill="none" stroke="${G}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" filter="url(#glow)"/>
  ${pup}
  <text x="200" y="436" text-anchor="middle" font-family="Orbitron,JetBrains Mono,monospace" font-weight="900" font-size="30" fill="${m === "hold" ? HOT : G}" letter-spacing="4">:${m}</text>
  <text x="200" y="458" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="10.5" fill="${CY}">&gt;_ ${esc(C.SHORT[m])} · æ1 · read-only · Human stays root.</text>
  <text x="200" y="474" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="9" fill="${G}" opacity=".7">ae.face/0.1 · #osw #ioa #æææ · LAB</text>
</svg>
`;
}
C.ORDER.forEach(m => fs.writeFileSync(path.join(OUT, m + ".svg"), svg(m)));
console.log("wrote", C.ORDER.map(m => m + ".svg").join(" "));
