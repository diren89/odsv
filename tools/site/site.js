/* ODSV-Website – Verhalten der Oberfläche (Suche, Story-Steuerung, Frame-Höhe, Kopieren, Navigation mobil).
   Läuft nach odsv.js; nutzt dessen Segment-Umschalter (Event "odsv:change") und Theme (Event "odsv:theme"). */
(function () {
  'use strict';
  var root = document.documentElement;
  function qsa(s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); }
  function theme() { return root.getAttribute('data-theme') === 'light' ? 'light' : 'dark'; }

  /* ---- Hinweis (Toast) ---- */
  var toastTimer;
  function toast(msg) {
    var t = document.querySelector('.sb-toast');
    if (!t) {
      t = document.createElement('div');
      t.className = 'odsv-toast sb-toast'; t.setAttribute('role', 'status');
      document.body.appendChild(t);
    }
    t.textContent = msg; t.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { t.hidden = true; }, 1800);
  }
  function copy(text, label) {
    function done() { toast(label + ' kopiert'); }
    function fallback() {
      var ta = document.createElement('textarea'); ta.value = text; ta.setAttribute('readonly', '');
      ta.className = 'odsv-sr-only'; document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); done(); } catch (e) { toast('Kopieren nicht möglich'); }
      ta.remove();
    }
    if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(text).then(done, fallback);
    else fallback();
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('[data-sb-copy]');
    if (b) copy(b.getAttribute('data-sb-copy'), b.getAttribute('data-sb-copy-label') || 'Text');
    var c = e.target.closest && e.target.closest('[data-sb-copy-from]');
    if (c) { var src = document.querySelector(c.getAttribute('data-sb-copy-from')); if (src) copy(src.textContent, 'Code'); }
  });

  /* ---- Navigation mobil ---- */
  var shell = document.querySelector('.sb');
  var menu = document.querySelector('.sb-menu');
  var scrim = document.querySelector('.sb-scrim');
  function setNav(open) {
    if (!shell) return;
    shell.classList.toggle('is-nav-open', open);
    if (menu) menu.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (scrim) scrim.hidden = !open;
  }
  if (menu) menu.addEventListener('click', function () { setNav(!shell.classList.contains('is-nav-open')); });
  if (scrim) scrim.addEventListener('click', function () { setNav(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setNav(false); });

  /* ---- Suche in der Seitenleiste ---- */
  var search = document.getElementById('sb-search');
  var current = document.querySelector('.sb-nav a[aria-current="page"]');
  if (current && current.scrollIntoView) current.scrollIntoView({ block: 'center' });
  if (search) {
    var empty = document.querySelector('.sb-nav__empty');
    search.addEventListener('input', function () {
      var q = search.value.trim().toLowerCase(), any = false;
      qsa('.sb-nav li').forEach(function (li) {
        var hit = !q || li.textContent.toLowerCase().indexOf(q) > -1 || (li.getAttribute('data-sb-keys') || '').indexOf(q) > -1;
        li.hidden = !hit; if (hit) any = true;
      });
      qsa('.sb-nav__group').forEach(function (g) { g.hidden = !qsa('li', g).some(function (li) { return !li.hidden; }); });
      qsa('.sb-nav__sub').forEach(function (s) {
        var ul = s.nextElementSibling; s.hidden = ul ? !qsa('li', ul).some(function (li) { return !li.hidden; }) : false;
      });
      if (empty) empty.hidden = any;
    });
    search.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') { var first = qsa('.sb-nav li').filter(function (li) { return !li.hidden; })[0]; if (first) first.querySelector('a').click(); }
      if (e.key === 'Escape') { search.value = ''; search.dispatchEvent(new Event('input')); }
    });
    document.addEventListener('keydown', function (e) {
      var t = e.target.tagName;
      if (e.key === '/' && t !== 'INPUT' && t !== 'TEXTAREA' && !e.target.isContentEditable) { e.preventDefault(); setNav(true); search.focus(); }
    });
  }

  /* ---- Storys ---- */
  function selectSeg(group, value) {
    qsa('[role="radio"]', group).forEach(function (it) {
      var on = it.getAttribute('data-value') === value;
      it.setAttribute('aria-checked', on ? 'true' : 'false'); it.tabIndex = on ? 0 : -1;
    });
  }
  function frameSrc(story) {
    return story.getAttribute('data-src') + '?theme=' + story.getAttribute('data-theme-sel');
  }
  qsa('.sb-story').forEach(function (story) {
    var frame = story.querySelector('.sb-canvas__frame');
    var canvas = story.querySelector('.sb-canvas');
    var open = story.querySelector('[data-sb-open]');
    story.setAttribute('data-theme-sel', theme());
    selectSeg(story.querySelector('[data-sb-ctl="theme"]'), theme());
    frame.src = frameSrc(story);
    if (open) open.href = frameSrc(story);
    story.addEventListener('odsv:change', function (e) {
      var ctl = e.target.closest('[data-sb-ctl]'); if (!ctl) return;
      var v = e.detail && e.detail.value;
      if (ctl.getAttribute('data-sb-ctl') === 'theme') {
        story.setAttribute('data-theme-sel', v); story.setAttribute('data-theme-pinned', '1');
        frame.src = frameSrc(story); if (open) open.href = frameSrc(story);
      } else if (ctl.getAttribute('data-sb-ctl') === 'vp') {
        canvas.setAttribute('data-vp', v);
      }
    });
    var codeBtn = story.querySelector('[data-sb-code]');
    var code = story.querySelector('.sb-code');
    if (codeBtn && code) codeBtn.addEventListener('click', function () {
      var on = codeBtn.getAttribute('aria-expanded') !== 'true';
      codeBtn.setAttribute('aria-expanded', on ? 'true' : 'false');
      codeBtn.textContent = on ? 'Code ausblenden' : 'Code anzeigen';
      code.hidden = !on;
    });
  });
  document.addEventListener('odsv:theme', function () {
    qsa('.sb-story:not([data-theme-pinned])').forEach(function (story) {
      story.setAttribute('data-theme-sel', theme());
      selectSeg(story.querySelector('[data-sb-ctl="theme"]'), theme());
      story.querySelector('.sb-canvas__frame').src = frameSrc(story);
      var open = story.querySelector('[data-sb-open]'); if (open) open.href = frameSrc(story);
    });
  });
  /* Frames melden ihre Höhe per postMessage (funktioniert auch über file://). */
  window.addEventListener('message', function (e) {
    var d = e.data; if (!d || typeof d.sbHeight !== 'number') return;
    qsa('.sb-canvas__frame').forEach(function (f) {
      if (f.contentWindow === e.source) f.style.height = Math.max(80, Math.ceil(d.sbHeight)) + 'px';
    });
  });
})();
