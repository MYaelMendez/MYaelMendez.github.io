/* æ protocol — theme system.
   ONE module, every surface. Include with:
       <script src="assets/brand/ae-theme.js"></script>
   Spec: https://myaelmendez.github.io/MECH-OS-BUILD-SPEC.md (S2)

   - palettes are complete surfaces (bg/ink/accent/dim/line), not one hex value
   - follows prefers-color-scheme until the visitor chooses; choice persists
     to localStorage['ae-theme-v1']
   - writes --ae-* always, and --gold/--secondary-color/--primary-color only when
     the surface already declares them
   - mounts its own control via aeTheme.panel(mount)                              */
(function () {
  'use strict';
  var KEY = 'ae-theme-v1';

  var PALETTES = {
    void:    { name: 'æ void', bg: '#050505', ink: '#EDEDED', accent: '#D4AF37', dim: '#8A8A8A', line: '#2A2A2A' },
    ember:   { name: 'ember',   bg: '#120B08', ink: '#FFE8D6', accent: '#FF6B35', dim: '#B0897A', line: '#3A241A' },
    glacier: { name: 'glacier', bg: '#04080C', ink: '#D9F4FB', accent: '#6EE7F9', dim: '#7FA6B2', line: '#1B3540' },
    verdant: { name: 'verdant', bg: '#041007', ink: '#E2F8E6', accent: '#7CE38B', dim: '#8BB894', line: '#1B3A24' },
    orchid:  { name: 'orchid',  bg: '#0C0514', ink: '#F0E4FF', accent: '#C084FC', dim: '#A58BC4', line: '#2E1B45' },
    paper:   { name: 'paper',   bg: '#F5F1E6', ink: '#1A1A1A', accent: '#8A6A00', dim: '#7A7263', line: '#DDD3BE' }
  };
  /* dark first for night, light for day */
  var AUTO = { dark: 'void', light: 'paper' };

  function get() {
    try { return JSON.parse(localStorage.getItem(KEY) || 'null') } catch (e) { return null }
  }
  function store(v) { try { localStorage.setItem(KEY, JSON.stringify(v)) } catch (e) {} }

  function resolve() {
    var saved = get();
    if (saved && PALETTES[saved.id]) return saved.id;
    var dark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    return dark ? AUTO.dark : AUTO.light;
  }

  function apply(id) {
    var t = PALETTES[id] || PALETTES.void;
    var root = document.documentElement;
    root.style.setProperty('--ae-bg', t.bg);
    root.style.setProperty('--ae-ink', t.ink);
    root.style.setProperty('--ae-accent', t.accent);
    root.style.setProperty('--ae-dim', t.dim);
    root.style.setProperty('--ae-line', t.line);
    /* follow a surface's existing accents, but never invent them */
    if (getComputedStyle(root).getPropertyValue('--secondary-color').trim()) {
      root.style.setProperty('--secondary-color', t.accent);
    }
    if (getComputedStyle(root).getPropertyValue('--primary-color').trim()) {
      root.style.setProperty('--primary-color', t.accent);
    }
    if (getComputedStyle(root).getPropertyValue('--gold').trim()) {
      root.style.setProperty('--gold', t.accent);
      root.style.setProperty('--gold-hi', t.accent);
    }
    document.body.style.backgroundColor = t.bg;
    document.body.style.color = t.ink;
    document.body.setAttribute('data-theme', id);
    if (!get() || get().id !== id) store({ id: id });
    return t;
  }

  function cycle() {
    var ids = Object.keys(PALETTES), i = ids.indexOf(resolve());
    var next = ids[(i + 1) % ids.length];
    apply(next); store({ id: next });
    document.dispatchEvent(new CustomEvent('ae-theme', { detail: { id: next } }));
    return next;
  }

  function panel(mount) {
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'ae-theme-btn';
    b.setAttribute('title', 'theme · several palettes, day or night (æ protocol S2)');
    b.addEventListener('click', function () { cycle(); paint(); });
    if (mount) mount.appendChild(b);
    function paint() { b.textContent = '◐ ' + (PALETTES[resolve()] || PALETTES.void).name; }
    paint();
    document.addEventListener('ae-theme', paint);
    return b;
  }

  window.aeTheme = { apply: apply, cycle: cycle, resolve: resolve, panel: panel, palettes: PALETTES, key: KEY };
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { apply(resolve()) });
  } else { apply(resolve()) }
})();
