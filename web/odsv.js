/* ODSV v1.1 – Verhalten (optional, ohne Abhängigkeiten). Gestaltung liegt vollständig in odsv.css.
   Einbindung im <head> ohne defer, damit das gespeicherte Theme ohne Flackern gesetzt wird.
   Hooks (data-Attribute):
     [data-odsv-theme-toggle]                       Theme dunkel/hell, gespeichert in localStorage "odsv-theme"
     [data-odsv-segmented] > [role=radio]           Segment-Umschalter (Pfeile, Pos1/Ende), Event "odsv:change"
     [data-odsv-tabs]                               Tabs (ARIA, Pfeile, Pos1/Ende)
     [data-odsv-checklist="schlüssel"]              Checkliste mit localStorage, Zähler, Zurücksetzen, Fortschritt
     [data-odsv-scrollprogress]                     Segmentierte Leiste folgt dem Scroll durch Kapitel
     [data-odsv-nav-toggle]                         Menü der Top-Bar (mobil)
     [data-odsv-sheet-open="#id"] / [data-odsv-sheet-close]   Bottom-Sheet
     [data-odsv-copy="#id"]                         Text eines Elements kopieren                      */
(function () {
  'use strict';
  var root = document.documentElement;
  var THEME_KEY = 'odsv-theme';

  function store(op, key, val) {
    try {
      if (op === 'get') return window.localStorage.getItem(key);
      if (op === 'set') window.localStorage.setItem(key, val);
      if (op === 'del') window.localStorage.removeItem(key);
    } catch (e) { /* Speicher gesperrt: ohne Persistenz weiterarbeiten */ }
    return null;
  }
  function qsa(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }

  /* ---- Theme (sofort ausführen) ---- */
  function setTheme(t, persist) {
    if (t !== 'light' && t !== 'dark') return;
    root.setAttribute('data-theme', t);
    if (persist) store('set', THEME_KEY, t);
    qsa('[data-odsv-theme-toggle]').forEach(function (b) {
      b.setAttribute('aria-pressed', t === 'light' ? 'true' : 'false');
      b.setAttribute('aria-label', t === 'light' ? 'Dunkles Theme aktivieren' : 'Helles Theme aktivieren');
    });
    document.dispatchEvent(new CustomEvent('odsv:theme', { detail: { theme: t } }));
  }
  var saved = store('get', THEME_KEY);
  if (saved === 'light' || saved === 'dark') root.setAttribute('data-theme', saved);
  window.ODSV = { version: '1.1.0', setTheme: function (t) { setTheme(t, true); } };

  /* ---- Segment-Umschalter ---- */
  function initSegmented(group) {
    var items = qsa('[role="radio"]', group);
    function select(item, focus) {
      items.forEach(function (it) {
        var on = it === item;
        it.setAttribute('aria-checked', on ? 'true' : 'false');
        it.tabIndex = on ? 0 : -1;
        var pid = it.getAttribute('aria-controls');
        var panel = pid && document.getElementById(pid);
        if (panel) panel.hidden = !on;
      });
      if (focus) item.focus();
      group.dispatchEvent(new CustomEvent('odsv:change', { bubbles: true, detail: { value: item.getAttribute('data-value'), item: item } }));
    }
    items.forEach(function (it) {
      if (!it.hasAttribute('aria-checked')) it.setAttribute('aria-checked', 'false');
      it.tabIndex = it.getAttribute('aria-checked') === 'true' ? 0 : -1;
      it.addEventListener('click', function () { select(it, false); });
    });
    if (!items.some(function (i) { return i.tabIndex === 0; }) && items[0]) items[0].tabIndex = 0;
    group.addEventListener('keydown', function (e) {
      var i = items.indexOf(document.activeElement);
      if (i < 0) return;
      var n = null;
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') n = items[(i + 1) % items.length];
      else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') n = items[(i - 1 + items.length) % items.length];
      else if (e.key === 'Home') n = items[0];
      else if (e.key === 'End') n = items[items.length - 1];
      if (n) { e.preventDefault(); select(n, true); }
    });
  }

  /* ---- Tabs ---- */
  function initTabs(list) {
    var tabs = qsa('[role="tab"]', list);
    function activate(tab, focus) {
      var show = tab.getAttribute('aria-controls');
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute('aria-selected', on ? 'true' : 'false');
        t.tabIndex = on ? 0 : -1;
        var pid = t.getAttribute('aria-controls'), p = pid && document.getElementById(pid);
        if (p && pid !== show) p.hidden = true;
      });
      var sp = show && document.getElementById(show); if (sp) sp.hidden = false;
      if (focus) tab.focus();
      list.dispatchEvent(new CustomEvent('odsv:change', { bubbles: true, detail: { value: tab.getAttribute('data-value') || tab.id, tab: tab } }));
    }
    tabs.forEach(function (t) {
      t.addEventListener('click', function () { activate(t, false); });
    });
    var cur = tabs.filter(function (t) { return t.getAttribute('aria-selected') === 'true'; })[0] || tabs[0];
    if (cur) activate(cur, false);
    list.addEventListener('keydown', function (e) {
      var i = tabs.indexOf(document.activeElement);
      if (i < 0) return;
      var n = null;
      if (e.key === 'ArrowRight') n = tabs[(i + 1) % tabs.length];
      else if (e.key === 'ArrowLeft') n = tabs[(i - 1 + tabs.length) % tabs.length];
      else if (e.key === 'Home') n = tabs[0];
      else if (e.key === 'End') n = tabs[tabs.length - 1];
      if (n) { e.preventDefault(); activate(n, true); }
    });
  }

  /* ---- Checkliste ---- */
  function initChecklist(el) {
    var key = 'odsv-checklist:' + el.getAttribute('data-odsv-checklist');
    var boxes = qsa('input[type="checkbox"]', el);
    var count = el.querySelector('[data-odsv-checklist-count]');
    var bar = el.querySelector('[data-odsv-checklist-progress]');
    var reset = el.querySelector('[data-odsv-checklist-reset]');
    var segs = [];
    function idOf(b, i) { return b.getAttribute('data-id') || b.id || String(i); }
    if (bar) {
      bar.innerHTML = '';
      boxes.forEach(function () {
        var li = document.createElement('li');
        li.className = 'odsv-progress__seg';
        li.innerHTML = '<span class="odsv-progress__bar"></span>';
        bar.appendChild(li); segs.push(li);
      });
    }
    function render() {
      var n = 0;
      boxes.forEach(function (b, i) {
        if (b.checked) n++;
        if (segs[i]) segs[i].style.setProperty('--p', b.checked ? '1' : '0');
      });
      if (count) count.textContent = n + ' von ' + boxes.length;
      if (bar) {
        bar.classList.toggle('odsv-progress--success', n === boxes.length && n > 0);
        bar.setAttribute('role', 'progressbar');
        bar.setAttribute('aria-valuemin', '0');
        bar.setAttribute('aria-valuemax', String(boxes.length));
        bar.setAttribute('aria-valuenow', String(n));
        bar.setAttribute('aria-valuetext', n + ' von ' + boxes.length + ' erledigt');
      }
    }
    function save() {
      var ids = [];
      boxes.forEach(function (b, i) { if (b.checked) ids.push(idOf(b, i)); });
      store('set', key, JSON.stringify(ids));
    }
    try {
      var raw = store('get', key);
      var ids = raw ? JSON.parse(raw) : [];
      if (Array.isArray(ids)) boxes.forEach(function (b, i) { b.checked = ids.indexOf(idOf(b, i)) > -1; });
    } catch (e) { /* defekte Daten ignorieren */ }
    boxes.forEach(function (b) { b.addEventListener('change', function () { render(); save(); }); });
    if (reset) reset.addEventListener('click', function () {
      boxes.forEach(function (b) { b.checked = false; });
      store('del', key); render();
    });
    render();
  }

  /* ---- Scroll-Fortschritt (segmentiert) ---- */
  function initScrollProgress(bar) {
    var links = qsa('a[href^="#"]', bar);
    var items = links.map(function (a) {
      return { a: a, li: a.closest('.odsv-progress__seg') || a, sec: document.getElementById(a.getAttribute('href').slice(1)) };
    }).filter(function (x) { return x.sec; });
    var label = document.querySelector('[data-odsv-scrollprogress-label]');
    var ticking = false;
    function update() {
      ticking = false;
      var vh = window.innerHeight, y = window.scrollY, probe = y + vh * 0.35, active = -1;
      items.forEach(function (it, i) {
        var top = it.sec.getBoundingClientRect().top + y;
        var h = it.sec.offsetHeight || 1;
        var p = Math.max(0, Math.min(1, (y + vh * 0.5 - top) / (h + vh * 0.5)));
        if (i === items.length - 1 && y + vh >= document.documentElement.scrollHeight - 2) p = 1;
        it.li.style.setProperty('--p', p.toFixed(3));
        if (probe >= top) active = i;
      });
      items.forEach(function (it, i) {
        if (i === active) it.a.setAttribute('aria-current', 'step'); else it.a.removeAttribute('aria-current');
      });
      if (label && items[active]) label.textContent = items[active].a.getAttribute('data-title') || items[active].a.getAttribute('aria-label') || '';
    }
    function req() { if (!ticking) { ticking = true; window.requestAnimationFrame(update); } }
    window.addEventListener('scroll', req, { passive: true });
    window.addEventListener('resize', req);
    update();
  }

  /* ---- Top-Bar-Menü ---- */
  function initNavToggle(btn) {
    var bar = btn.closest('.odsv-topbar');
    if (!bar) return;
    function set(open) {
      bar.classList.toggle('is-open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    }
    btn.addEventListener('click', function () { set(!bar.classList.contains('is-open')); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && bar.classList.contains('is-open')) { set(false); btn.focus(); } });
    qsa('.odsv-topbar__nav a', bar).forEach(function (a) { a.addEventListener('click', function () { set(false); }); });
  }

  /* ---- Bottom-Sheet ---- */
  var lastFocus = null, openSheet = null;
  function showSheet(sheet) {
    lastFocus = document.activeElement; openSheet = sheet;
    sheet.hidden = false;
    window.requestAnimationFrame(function () { sheet.classList.add('is-open'); });
    var panel = sheet.querySelector('.odsv-sheet__panel');
    if (panel) { panel.setAttribute('tabindex', '-1'); panel.focus({ preventScroll: true }); }
  }
  function hideSheet(sheet) {
    sheet.classList.remove('is-open');
    var done = function () { sheet.hidden = true; };
    var dur = parseFloat(window.getComputedStyle(sheet.querySelector('.odsv-sheet__panel')).transitionDuration) || 0;
    if (dur < 0.001) done(); else window.setTimeout(done, 420);
    openSheet = null;
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  document.addEventListener('keydown', function (e) {
    if (!openSheet) return;
    if (e.key === 'Escape') { hideSheet(openSheet); return; }
    if (e.key === 'Tab') {
      var f = qsa('a[href],button:not([disabled]),input,select,textarea,[tabindex="0"]', openSheet).filter(function (n) { return n.offsetParent !== null; });
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && (document.activeElement === first || document.activeElement === openSheet.querySelector('.odsv-sheet__panel'))) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });

  /* ---- Kopieren ---- */
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(text);
    return new Promise(function (res, rej) {
      try {
        var ta = document.createElement('textarea');
        ta.value = text; ta.setAttribute('readonly', ''); ta.style.position = 'fixed'; ta.style.opacity = '0';
        document.body.appendChild(ta); ta.select();
        var ok = document.execCommand('copy'); document.body.removeChild(ta);
        ok ? res() : rej(new Error('copy'));
      } catch (e) { rej(e); }
    });
  }
  function onCopy(btn) {
    var sel = btn.getAttribute('data-odsv-copy'), src = sel ? document.querySelector(sel) : null;
    if (!src) return;
    var label = btn.getAttribute('data-label') || btn.textContent;
    btn.setAttribute('data-label', label);
    var done = function (msg) { btn.textContent = msg; window.setTimeout(function () { btn.textContent = label; }, 1600); };
    try { copyText(src.textContent).then(function () { done('Kopiert'); }, function () { done('Nicht möglich'); }); }
    catch (e) { done('Nicht möglich'); }
  }

  /* ---- Init ---- */
  function once(node, fn) { if (node._odsvReady) return; node._odsvReady = true; fn(node); }
  function scan(ctx) {
    qsa('[data-odsv-segmented]', ctx).forEach(function (n) { once(n, initSegmented); });
    qsa('[data-odsv-tabs]', ctx).forEach(function (n) { once(n, initTabs); });
    qsa('[data-odsv-checklist]', ctx).forEach(function (n) { once(n, initChecklist); });
    qsa('[data-odsv-scrollprogress]', ctx).forEach(function (n) { once(n, initScrollProgress); });
    qsa('[data-odsv-nav-toggle]', ctx).forEach(function (n) { once(n, initNavToggle); });
    qsa('.odsv-tooltip', ctx).forEach(function (t) {
      once(t, function () {
        t.addEventListener('mouseleave', function () { t.classList.remove('is-dismissed'); });
        t.addEventListener('focusout', function () { t.classList.remove('is-dismissed'); });
      });
    });
  }
  // Versalien-Headlines: lange Wörter nie mitten im Wort brechen (SPEC 2.6, 4.3).
  // Passt das längste Wort nicht, erst Laufweite display-tight, dann Schrift bis 72 % verkleinern.
  var fitTargets = '.odsv-display, .odsv-h1, .odsv-h2, [data-odsv-fit]';
  var meas;
  function wordWidth(el, word) {
    if (!meas) { meas = document.createElement('span'); meas.setAttribute('aria-hidden', 'true'); meas.style.cssText = 'position:absolute;visibility:hidden;white-space:nowrap;left:-9999px;top:0;'; document.body.appendChild(meas); }
    var cs = getComputedStyle(el);
    meas.style.font = cs.font; meas.style.letterSpacing = cs.letterSpacing; meas.style.textTransform = cs.textTransform; meas.style.fontSize = cs.fontSize;
    meas.textContent = word; return meas.getBoundingClientRect().width;
  }
  function fitHeadline(el) {
    el.style.removeProperty('font-size'); el.classList.remove('odsv-fit-tight');
    var avail = el.clientWidth; if (!avail) return;
    var words = (el.textContent || '').replace(/\u00AD/g, '').split(/\s+/).filter(Boolean);
    if (!words.length) return;
    var longest = words.reduce(function (a, b) { return b.length > a.length ? b : a; });
    if (/\u00AD/.test(el.innerHTML) || el.innerHTML.indexOf('&shy;') > -1) return; // Trennstelle vorgegeben
    if (wordWidth(el, longest) <= avail) return;
    el.classList.add('odsv-fit-tight');
    var w = wordWidth(el, longest); if (w <= avail) return;
    var fs = parseFloat(getComputedStyle(el).fontSize), f = Math.max(0.72, (avail - 2) / w);
    el.style.fontSize = (fs * f).toFixed(2) + 'px';
  }
  function fitAll(ctx) { qsa(fitTargets, ctx || document).forEach(fitHeadline); }
  var fitT; window.addEventListener('resize', function () { clearTimeout(fitT); fitT = setTimeout(function () { fitAll(); }, 120); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { fitAll(); });
  window.ODSV.fit = fitAll;
  window.ODSV.init = function (ctx) { scan(ctx || document); fitAll(ctx); };
  function init() {
    setTheme(root.getAttribute('data-theme') === 'light' ? 'light' : 'dark', false);
    scan(document);
    fitAll();
    document.addEventListener('click', function (e) {
      var tgt = e.target.closest ? e.target : e.target.parentElement;
      var th = tgt.closest('[data-odsv-theme-toggle]');
      if (th) { setTheme(root.getAttribute('data-theme') === 'light' ? 'dark' : 'light', true); return; }
      var op = tgt.closest('[data-odsv-sheet-open]');
      if (op) { var s = document.querySelector(op.getAttribute('data-odsv-sheet-open')); if (s) showSheet(s); return; }
      var cl = tgt.closest('[data-odsv-sheet-close]');
      if (cl) { var sh = cl.closest('.odsv-sheet'); if (sh) hideSheet(sh); return; }
      var cp = tgt.closest('[data-odsv-copy]');
      if (cp) onCopy(cp);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape') return;
      qsa('.odsv-tooltip:hover, .odsv-tooltip:focus-within').forEach(function (t) { t.classList.add('is-dismissed'); });
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
