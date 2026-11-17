/* Dokumentationsseite: erzeugt Navigation, Farbfelder (Hex + Kontrast live aus den Tokens), Abstände, Radien,
   Bewegung, Icon-Raster, Paletten und rendert alle Komponenten-Demos samt kopierbarem HTML aus <template class="docs-src">. */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var P = '--odsv-';
  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  var de = function (n, d) { return Number(n).toLocaleString('de-DE', { minimumFractionDigits: d, maximumFractionDigits: d }); };

  /* ---------- Farbe: lesen, mischen, Kontrast ---------- */
  var probe = el('span'); probe.style.cssText = 'position:absolute;visibility:hidden;pointer-events:none'; document.body.appendChild(probe);
  function readColor(v) {
    probe.style.color = 'var(' + P + v + ')';
    var m = getComputedStyle(probe).color.match(/[\d.]+/g) || [0, 0, 0];
    return { r: +m[0], g: +m[1], b: +m[2], a: m[3] === undefined ? 1 : +m[3] };
  }
  function over(c, bg) { return { r: c.r * c.a + bg.r * (1 - c.a), g: c.g * c.a + bg.g * (1 - c.a), b: c.b * c.a + bg.b * (1 - c.a), a: 1 }; }
  function lum(c) { var f = function (x) { x /= 255; return x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4); }; return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b); }
  function ratio(a, b) { var x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); }
  function hex(c) {
    var h = function (n) { return ('0' + Math.round(n).toString(16)).slice(-2); };
    return ('#' + h(c.r) + h(c.g) + h(c.b) + (c.a < 0.999 ? h(c.a * 255) : '')).toUpperCase();
  }
  function grade(r) { return r >= 7 ? 'AAA' : r >= 4.5 ? 'AA' : r >= 3 ? 'AA (Großtext/UI)' : 'unter 3:1'; }

  /* name, Rolle, Kontrast gegen [var,…] (für Flächen: Text darauf; "text:" = Vordergrund gegen Fläche) */
  var COLORS = [
    ['Flächen', 'Bühne und Karten – Tiefe entsteht durch Stufen, nicht durch Schatten.', [
      ['color-bg-base', 'Seite, Folie', ['color-text-primary']],
      ['color-bg-subtle', 'Signet-Karte, abgesetzte Sektion', ['color-text-primary']],
      ['color-bg-stage', '3D, Explosionszeichnung, Vollbild-Diagramm', ['color-text-primary']],
      ['color-surface-1', 'Karte', ['color-text-primary']],
      ['color-surface-2', 'Karte in Karte, Hover', ['color-text-primary']],
      ['color-surface-3', 'gedrückt, ausgewählte Zeile', ['color-text-primary']],
      ['color-surface-inverse', 'umgekehrte Fläche (Gegenwahl)', ['color-text-inverse']]]],
    ['Text', 'Fünf deckende Stufen; alle ≥ 4,5:1 auf Grund und Karte 1.', [
      ['color-text-primary', 'Headline, betonter Wert', ['color-bg-base', 'color-surface-1']],
      ['color-text-body', 'Fließtext', ['color-bg-base', 'color-surface-1']],
      ['color-text-secondary', 'Eyebrow, Label', ['color-bg-base', 'color-surface-1']],
      ['color-text-muted', 'Zweitsatz, Erklärtext', ['color-bg-base', 'color-surface-1']],
      ['color-text-faint', 'Fußnote, Achsen (nicht auf Karte 3)', ['color-bg-base', 'color-surface-1']],
      ['color-text-disabled', 'deaktiviert – nie für Information', ['color-bg-base', 'color-surface-1']]]],
    ['Akzent', 'Akzentgelb: eine Handlung, eine Zahl, ein Marker.', [
      ['color-accent-fill', 'Primär-Button (Verlauf bis fill-end), Marker', ['color-bg-base']],
      ['color-accent-fill-end', 'Ende des Button-Verlaufs', ['color-bg-base']],
      ['color-accent-hover', 'Hover Primär', ['color-bg-base']],
      ['color-accent-pressed', 'Gedrückt Primär', ['color-bg-base']],
      ['color-accent-text', 'betonte Kennzahl, Icon', ['color-bg-base', 'color-surface-1']],
      ['color-accent-line', 'aktiver Strich, Rand', ['color-bg-base']],
      ['color-accent-on', 'Schrift auf Gelb', ['color-accent-fill']],
      ['color-accent-subtle', 'getönter Grund', ['color-text-primary']],
      ['color-focus-ring', 'Fokusring', ['color-bg-base']]]],
    ['Status', 'Immer Icon + Wort; nie Farbe allein.', [
      ['color-status-success-base', 'Erfolg: Fläche, Icon', ['color-surface-1']],
      ['color-status-success-text', 'Erfolg: Text', ['color-surface-1']],
      ['color-status-warning-base', 'Warnung: Fläche, Icon', ['color-surface-1']],
      ['color-status-warning-text', 'Warnung: Text', ['color-surface-1']],
      ['color-status-danger-base', 'Fehler: Fläche, Icon', ['color-surface-1']],
      ['color-status-danger-text', 'Fehler: Text', ['color-surface-1']],
      ['color-status-info-base', 'Info: Fläche, Icon', ['color-surface-1']],
      ['color-status-info-text', 'Info: Text', ['color-surface-1']]]],
    ['Linien', 'Kartenränder sind Dekor; Bedienelemente nutzen border-control (≥ 3:1).', [
      ['color-border-subtle', 'Kartenrand, Trennlinie (Dekor)', ['color-bg-base']],
      ['color-border-strong', 'Label-Pille, Tabellenkopf', ['color-bg-base']],
      ['color-border-control', 'Formularfeld, Checkbox', ['color-bg-base', 'color-surface-1']],
      ['color-border-active', 'aktive Karte', ['color-bg-base']]]],
    ['Signet', 'Nur Signet/Titelmoment – nie als Button, Text oder Diagrammfarbe.', [
      ['color-signet-1', 'Bogen 1 (Pink)', null], ['color-signet-2', 'Bogen 2 (Orange)', null],
      ['color-signet-3', 'Bogen 3', null], ['color-signet-4', 'Bogen 4', null], ['color-signet-dot', 'Kern', null]]]
  ];

  function renderColors() {
    var host = $('#docs-colors'); if (!host) return;
    host.innerHTML = '';
    COLORS.forEach(function (g) {
      var blk = el('div', 'docs-block');
      blk.appendChild(el('h3', 'odsv-h3', g[0]));
      blk.appendChild(el('p', 'docs-note', g[1]));
      var grid = el('div', 'docs-swatches');
      g[2].forEach(function (c) {
        var col = readColor(c[0]);
        var base = readColor('color-bg-base');
        var rows = '';
        (c[2] || []).forEach(function (ag) {
          var other = over(readColor(ag), base), mine = over(col, other);
          var r = ratio(mine, other);
          rows += '<span class="docs-sw__ratio">' + de(r, 2) + ':1 · ' + grade(r) + ' <span class="odsv-caption">vs ' + ag.replace('color-', '') + '</span></span>';
        });
        var card = el('div', 'docs-sw',
          '<div class="docs-sw__chip" style="background:var(' + P + c[0] + ')"></div><div class="docs-sw__meta">' +
          '<span class="docs-sw__name">' + P + c[0] + '</span><span class="docs-sw__hex">' + hex(col) + '</span><span>' + c[1] + '</span>' + rows + '</div>');
        grid.appendChild(card);
      });
      blk.appendChild(grid);
      host.appendChild(blk);
    });
  }

  /* ---------- Abstände, Radien, Bewegung ---------- */
  function renderSpace() {
    var h = $('#docs-space'); if (!h) return;
    [1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32].forEach(function (n) {
      var row = el('div', 'docs-space__row', '<code>space-' + n + '</code><span>' + n * 4 + ' px</span><div class="docs-space__bar" style="width:min(100%,var(' + P + 'space-' + n + '))"></div>');
      h.appendChild(row);
    });
  }
  function renderRadii() {
    var h = $('#docs-radii'); if (!h) return;
    [['segment', 'Segment'], ['checkbox', 'Checkbox'], ['sm', 'klein'], ['control-inner', 'Bedienelement innen'], ['control', 'Bedienelement'], ['inset', 'Einsatz'], ['card-sm', 'Karte klein'], ['tile', 'Kachel'], ['card', 'Karte'], ['pill', 'Pille']].forEach(function (r) {
      probe.style.borderRadius = 'var(' + P + 'radius-' + r[0] + ')';
      var px = getComputedStyle(probe).borderTopLeftRadius; probe.style.borderRadius = '';
      h.appendChild(el('div', 'docs-radius', '<div class="docs-radius__box" style="border-radius:var(' + P + 'radius-' + r[0] + ')"></div><span><code>radius-' + r[0] + '</code><br>' + r[1] + ' · ' + (r[0] === 'pill' ? '∞' : parseFloat(px) + ' px') + '</span>'));
    });
  }
  function renderMotion() {
    var h = $('#docs-motion'); if (!h) return;
    var rows = [['instant', 'standard', '100 ms · Hover'], ['fast', 'standard', '200 ms · Button'], ['base', 'standard', '300 ms · Einblenden'], ['slow', 'in-out', '400 ms · Linien'], ['stage', 'standard', '500 ms · Bühne'], ['camera', 'in-out', '1000 ms · Kamera']];
    rows.forEach(function (r) {
      h.appendChild(el('div', 'docs-motion__row', '<span><code>' + r[0] + '</code><br>' + r[2] + '</span><div class="docs-motion__track"><div class="docs-motion__dot" style="transition:transform var(' + P + 'motion-duration-' + r[0] + ') var(' + P + 'motion-easing-' + r[1] + ')"></div></div>'));
    });
    var btn = $('#docs-motion-play');
    function size() { var t = $('.docs-motion__track', h); if (t) h.style.setProperty('--_run', Math.max(0, t.clientWidth - 29) + 'px'); }
    size(); window.addEventListener('resize', size);
    btn.addEventListener('click', function () { size(); h.classList.toggle('is-playing'); });
  }

  /* ---------- Paletten ---------- */
  function pal(host, vars, labels) {
    var h = $(host); if (!h) return;
    vars.forEach(function (v, i) { h.appendChild(el('div', '', '<span>' + (labels ? labels[i] : i + 1) + '</span>')).style.background = 'var(' + P + v + ')'; });
  }

  /* ---------- Demos aus <template> ---------- */
  function dedent(t) {
    var lines = t.replace(/\t/g, '  ').split('\n');
    while (lines.length && !lines[0].trim()) lines.shift();
    while (lines.length && !lines[lines.length - 1].trim()) lines.pop();
    var min = Infinity;
    lines.forEach(function (l) { if (l.trim()) min = Math.min(min, l.match(/^ */)[0].length); });
    return lines.map(function (l) { return l.slice(min === Infinity ? 0 : min); }).join('\n');
  }
  function esc(s) { return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  var demoN = 0;
  function renderDemos() {
    $$('template.docs-src').forEach(function (tpl) {
      var n = ++demoN, raw = dedent(tpl.innerHTML);
      var demo = el('div', 'docs-demo');
      var stage = el('div', 'docs-demo__stage' + (tpl.dataset.surface ? ' docs-demo__stage--surface' : ''));
      var caps = tpl.dataset.captions ? tpl.dataset.captions.split('|') : null;
      if (caps) {
        stage.classList.add('docs-demo__stage--states'); if (tpl.dataset.wide) stage.classList.add('docs-demo__stage--wide-states');
        var frag = tpl.content.cloneNode(true), kids = Array.prototype.filter.call(frag.childNodes, function (c) { return c.nodeType === 1; });
        kids.forEach(function (k, i) { var f = el('figure'); f.appendChild(k); f.appendChild(el('figcaption', '', caps[i] || '')); stage.appendChild(f); });
      } else if (!tpl.dataset.nolive) stage.appendChild(tpl.content.cloneNode(true));
      if (!tpl.dataset.nolive) demo.appendChild(stage);
      var det = el('details', 'docs-snippet');
      det.innerHTML = '<summary><svg class="odsv-icon" aria-hidden="true"><use href="#odsv-icon-chevron"/></svg>HTML ansehen</summary>' +
        '<div class="docs-snippet__actions"><button type="button" class="odsv-btn odsv-btn--ghost odsv-btn--sm" data-odsv-copy="#snip-' + n + '">Kopieren</button></div>' +
        '<pre tabindex="0"><code id="snip-' + n + '">' + esc(raw) + '</code></pre>';
      demo.appendChild(det);
      tpl.replaceWith(demo);
      if (window.ODSV && window.ODSV.init) window.ODSV.init(demo);
    });
  }

  /* ---------- Icons ---------- */
  function copy(text) {
    try {
      if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(text);
    } catch (e) { /* weiter mit Fallback */ }
    return new Promise(function (res, rej) {
      try { var t = el('textarea'); t.value = text; t.style.cssText = 'position:fixed;opacity:0'; document.body.appendChild(t); t.select(); var ok = document.execCommand('copy'); t.remove(); ok ? res() : rej(); } catch (e) { rej(e); }
    });
  }
  function renderIcons() {
    var h = $('#docs-icons'); if (!h) return;
    $$('symbol[id^="odsv-icon-"]').forEach(function (s) {
      var name = s.id.replace('odsv-icon-', '');
      var b = el('button', 'docs-icon', '<svg class="odsv-icon" aria-hidden="true"><use href="#' + s.id + '"/></svg><span>' + name + '</span>');
      b.type = 'button'; b.title = 'Snippet kopieren: ' + name;
      b.addEventListener('click', function () {
        var span = $('span', b), old = span.textContent;
        var snip = '<svg class="odsv-icon" aria-hidden="true"><use href="#' + s.id + '"/></svg>';
        var done = function (m) { span.textContent = m; setTimeout(function () { span.textContent = old; }, 1400); };
        try { copy(snip).then(function () { done('Kopiert'); }, function () { done('Nicht möglich'); }); } catch (e) { done('Nicht möglich'); }
      });
      h.appendChild(b);
    });
  }

  /* ---------- Navigation ---------- */
  function renderNav() {
    var secs = $$('.docs-section[data-nav]'), groups = [], map = {};
    secs.forEach(function (s) { var g = s.dataset.group || ''; if (!map[g]) { map[g] = []; groups.push(g); } map[g].push(s); });
    function build(ul, cls) {
      groups.forEach(function (g) {
        if (g) ul.appendChild(el('li', 'odsv-nav__group', '<span class="odsv-eyebrow">' + g + '</span>'));
        map[g].forEach(function (s) { ul.appendChild(el('li', '', '<a class="odsv-nav__link" href="#' + s.id + '">' + s.dataset.nav + '</a>')); });
      });
    }
    $$('[data-docs-nav]').forEach(function (ul) { build(ul); });
    var links = $$('[data-docs-nav] a');
    if (!('IntersectionObserver' in window)) return;
    var cur = null;
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) cur = e.target.id; });
      links.forEach(function (a) { if (a.getAttribute('href') === '#' + cur) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current'); });
    }, { rootMargin: '-20% 0px -70% 0px' });
    secs.forEach(function (s) { io.observe(s); });
  }

  /* ---------- Diagramm-Demos ---------- */
  function renderCharts() {
    if (!window.ODSVCharts) return;
    var C = window.ODSVCharts;
    var months = ['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez'];
    $$('[data-demo-chart="line"]').forEach(function (e) {
      C.line(e, { labels: months, series: [{ name: 'Registrierungen', values: [42, 48, 55, 51, 63, 70, 74, 69, 81, 88, 92, 97], cls: 'odsv-dv-1', area: true }, { name: 'Supportanfragen', values: [18, 17, 21, 19, 22, 20, 24, 21, 23, 22, 25, 24], cls: 'odsv-dv-2' }], height: 220, label: 'Registrierungen steigen von 42 im Januar auf 97 im Dezember; Supportanfragen bleiben zwischen 17 und 25.' });
    });
    $$('[data-demo-chart="bars"]').forEach(function (e) {
      C.bars(e, { labels: ['Q1', 'Q2', 'Q3', 'Q4'], values: [145, 184, 224, 277], colors: ['odsv-dv-context', 'odsv-dv-context', 'odsv-dv-context', 'odsv-dv-highlight'], height: 200, label: 'Registrierungen je Quartal; Q4 ist mit 277 am höchsten.' });
    });
    $$('[data-demo-chart="donut"]').forEach(function (e) {
      C.donut(e, { items: [{ label: 'Abgeschlossen', value: 62, cls: 'odsv-dv-1' }, { label: 'In Arbeit', value: 24, cls: 'odsv-dv-2' }, { label: 'Offen', value: 14, cls: 'odsv-dv-neutral' }], size: 180, center: { value: '62 %', label: 'fertig' }, label: '62 Prozent abgeschlossen, 24 in Arbeit, 14 offen.' });
    });
    /* Analyse-Diagramme – alle Werte sind Beispieldaten; Zufallswerte aus festem Startwert, damit jede Ansicht gleich aussieht. */
    var seed = 7; function rnd() { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }
    function normal(m, s) { var u = 0, v = 0; while (!u) u = rnd(); while (!v) v = rnd(); return m + s * Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); }
    $$('[data-demo-chart="line-annot"]').forEach(function (e) {
      C.line(e, { labels: months, unit: 'Tsd. €', endLabels: true, height: 240,
        series: [{ name: 'Web', values: [62, 64, 61, 66, 68, 71, 84, 90, 94, 99, 103, 108], cls: 'odsv-dv-1' }, { name: 'App', values: [38, 40, 43, 42, 45, 47, 49, 50, 54, 55, 57, 60], cls: 'odsv-dv-2' }, { name: 'Händler', values: [51, 50, 52, 49, 50, 48, 47, 49, 46, 45, 47, 44], cls: 'odsv-dv-3' }],
        annotations: [{ at: 6, label: 'Relaunch' }], target: { value: 95, label: 'Ziel Web 95' },
        label: 'Web steigt nach dem Relaunch im Juli von 71 auf 108 Tausend Euro und liegt ab Oktober über dem Ziel von 95; App wächst stetig, Händler sinkt leicht.' });
    });
    $$('[data-demo-chart="columns-stacked"]').forEach(function (e) {
      C.columns(e, { labels: ['Q1', 'Q2', 'Q3', 'Q4'], mode: 'stacked', unit: 'Tsd. €', height: 240,
        series: [{ name: 'Bestand', values: [120, 124, 126, 129], cls: 'odsv-dv-2' }, { name: 'Neukunden', values: [24, 38, 55, 71], cls: 'odsv-dv-1' }],
        label: 'Der Umsatz steigt von 144 auf 200 Tausend Euro; der Anteil der Neukunden wächst von 24 auf 71.' });
    });
    $$('[data-demo-chart="columns-grouped"]').forEach(function (e) {
      C.columns(e, { labels: ['Q1', 'Q2', 'Q3', 'Q4'], mode: 'grouped', height: 240,
        series: [{ name: 'Nord', values: [31, 34, 38, 52], cls: 'odsv-dv-2' }, { name: 'Süd', values: [48, 50, 51, 53], cls: 'odsv-dv-4' }, { name: 'West', values: [40, 42, 39, 41], cls: 'odsv-dv-5' }],
        label: 'Süd liegt in jedem Quartal vorn; Nord wächst von 31 auf 52 Abschlüsse und erreicht im Q4 fast Süd.' });
    });
    $$('[data-demo-chart="hbars"]').forEach(function (e) {
      var cities = ['Berlin', 'Hamburg', 'München', 'Köln', 'Frankfurt', 'Stuttgart', 'Leipzig'];
      C.hbars(e, { labels: cities, values: [1840, 1120, 1065, 860, 790, 610, 455], colors: ['odsv-dv-highlight', 'odsv-dv-context', 'odsv-dv-context', 'odsv-dv-context', 'odsv-dv-context', 'odsv-dv-context', 'odsv-dv-context'],
        label: 'Berlin hat mit 1.840 Bestellungen die meisten, vor Hamburg mit 1.120 und München mit 1.065.' });
    });
    $$('[data-demo-chart="diverging"]').forEach(function (e) {
      C.diverging(e, { labels: ['Vertrieb', 'Service', 'Marketing', 'Logistik', 'Einkauf', 'Technik'], values: [8.5, 3.2, 1.1, -2.4, -4.8, -6.1], negLabel: 'unter Plan', posLabel: 'über Plan',
        format: function (v) { return (v > 0 ? '+' : '') + C.format(v) + ' Pp.'; }, label: 'Vertrieb liegt 8,5 Prozentpunkte über Plan; Logistik, Einkauf und Technik liegen darunter, Technik am weitesten mit minus 6,1.' });
    });
    $$('[data-demo-chart="funnel"]').forEach(function (e) {
      C.funnel(e, { steps: [{ label: 'Besuch', value: 48200 }, { label: 'Produktseite', value: 21300 }, { label: 'Warenkorb', value: 6400 }, { label: 'Kasse', value: 3900 }, { label: 'Kauf', value: 3100 }],
        label: 'Von 48.200 Besuchen erreichen 21.300 eine Produktseite; nur 30 Prozent davon legen etwas in den Warenkorb, am Ende kaufen 3.100.' });
    });
    $$('[data-demo-chart="histogram"]').forEach(function (e) {
      seed = 7; var v = []; for (var i = 0; i < 240; i++) v.push(Math.max(0.1, Math.abs(normal(1.6, 0.9)) + (i % 9 === 0 ? 2.5 : 0)));
      C.histogram(e, { values: v, binWidth: 0.5, mark: 'median', unit: 'Tickets', xFormat: function (x) { return C.format(x) + ' h'; },
        label: '240 Tickets nach Lösungszeit; die meisten sind nach 1 bis 2 Stunden gelöst, der Median liegt bei etwa 1,7 Stunden.' });
    });
    $$('[data-demo-chart="boxplot"]').forEach(function (e) {
      seed = 11; var mk = function (m, s, n) { var a = []; for (var i = 0; i < n; i++) a.push(Math.max(0.2, normal(m, s))); return a; };
      var b = mk(2.6, 1.3, 60); b.push(8.2, 9.1);
      C.boxplot(e, { groups: [{ label: 'Team A', values: mk(1.8, 0.5, 60) }, { label: 'Team B', values: b, cls: 'odsv-dv-highlight' }, { label: 'Team C', values: mk(2.1, 0.7, 60) }],
        format: function (x) { return C.format(Math.round(x * 10) / 10) + ' h'; }, label: 'Team B hat den höchsten Median und die größte Streuung, mit zwei Ausreißern über 8 Stunden; Team A ist am schnellsten.' });
    });
    $$('[data-demo-chart="scatter"]').forEach(function (e) {
      seed = 5; var on = [], pr = [];
      for (var i = 0; i < 14; i++) { var x = 5 + rnd() * 45; on.push({ x: Math.round(x), y: Math.round(40 * Math.log(x) - 40 + normal(0, 8)), r: Math.round(20 + rnd() * 80), label: 'Kampagne O' + (i + 1) }); }
      for (var j = 0; j < 6; j++) { var xp = 10 + rnd() * 35; pr.push({ x: Math.round(xp), y: Math.round(28 * Math.log(xp) - 30 + normal(0, 6)), r: Math.round(20 + rnd() * 60), label: 'Kampagne P' + (j + 1) }); }
      on[3].highlight = true;
      C.scatter(e, { series: [{ name: 'Online', points: on, cls: 'odsv-dv-2' }, { name: 'Print', points: pr, cls: 'odsv-dv-5' }], xLabel: 'Budget, Tsd. €', yLabel: 'Leads', sizeName: 'Umsatz, Tsd. €', trend: true, xZero: true, yZero: true,
        label: 'Leads steigen mit dem Budget, aber flacher je höher das Budget; Online-Kampagnen erzielen bei gleichem Budget mehr Leads als Print.' });
    });
    $$('[data-demo-chart="heatmap"]').forEach(function (e) {
      var days = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So'], hours = []; for (var hh = 7; hh <= 20; hh++) hours.push(hh + '');
      var vals = days.map(function (d, di) { return hours.map(function (hs, hi) {
        var hr = +hs, base = di < 5 ? 40 + 60 * Math.exp(-Math.pow(hr - 10, 2) / 3) + 50 * Math.exp(-Math.pow(hr - 14, 2) / 4) : 15 + 12 * Math.exp(-Math.pow(hr - 12, 2) / 8);
        if (di === 6 && hr < 9) return null; return Math.round(base * (di === 4 ? 0.85 : 1)); }); });
      C.heatmap(e, { rows: days, cols: hours, values: vals, scaleTitle: 'Anfragen je Stunde', label: 'Werktags gibt es zwei Spitzen um 10 und 14 Uhr mit bis zu rund 100 Anfragen; am Wochenende bleibt die Last unter 30.' });
    });
    $$('[data-demo-chart="slope"]').forEach(function (e) {
      C.slope(e, { from: '2025', to: '2026', items: [{ label: 'Hamburg', a: 68, b: 81, cls: 'odsv-dv-highlight' }, { label: 'Berlin', a: 74, b: 76 }, { label: 'München', a: 79, b: 78 }, { label: 'Köln', a: 71, b: 73 }, { label: 'Leipzig', a: 65, b: 69 }],
        label: 'Hamburg steigt von 68 auf 81 Punkte und überholt alle anderen Städte; München sinkt leicht von 79 auf 78.' });
    });
    $$('[data-demo-chart="multiples"]').forEach(function (e) {
      C.multiples(e, { labels: months, yFormat: function (v) { return C.format(v); }, columns: 2, height: 110,
        series: [{ name: 'Nord', values: [3.1, 3.0, 3.2, 3.4, 3.3, 3.1, 3.0, 3.2, 3.3, 3.4, 3.5, 3.6] }, { name: 'Ost', values: [1.2, 1.4, 1.5, 1.7, 1.9, 2.1, 2.3, 2.4, 2.6, 2.8, 3.0, 3.2] },
                 { name: 'Süd', values: [4.0, 4.1, 3.9, 3.8, 4.0, 4.2, 4.1, 3.9, 3.8, 3.9, 4.0, 4.1] }, { name: 'West', values: [2.6, 2.5, 2.7, 2.6, 2.4, 2.3, 2.5, 2.4, 2.2, 2.3, 2.2, 2.1] }],
        label: 'Umsatz je Region über zwölf Monate: Ost wächst von 1,2 auf 3,2 Millionen Euro, Süd bleibt bei rund 4, West sinkt leicht.' });
    });
  }

  function init() {
    renderDemos(); renderColors(); renderSpace(); renderRadii(); renderMotion(); renderIcons(); renderNav(); renderCharts();
    pal('#docs-pal-cat', ['dataviz-categorical-1', 'dataviz-categorical-2', 'dataviz-categorical-3', 'dataviz-categorical-4', 'dataviz-categorical-5', 'dataviz-categorical-6', 'dataviz-categorical-7']);
    pal('#docs-pal-seq', ['dataviz-sequential-1', 'dataviz-sequential-2', 'dataviz-sequential-3', 'dataviz-sequential-4', 'dataviz-sequential-5', 'dataviz-sequential-6']);
    pal('#docs-pal-div', ['dataviz-diverging-neg-3', 'dataviz-diverging-neg-2', 'dataviz-diverging-neg-1', 'dataviz-diverging-mid', 'dataviz-diverging-pos-1', 'dataviz-diverging-pos-2', 'dataviz-diverging-pos-3'], ['−3', '−2', '−1', '0', '+1', '+2', '+3']);
    pal('#docs-pal-sem', ['dataviz-highlight', 'dataviz-context', 'dataviz-neutral', 'dataviz-positive', 'dataviz-negative'], ['betont', 'Kontext', 'Sonstige', 'positiv', 'negativ']);
    document.addEventListener('odsv:theme', function () { renderColors(); if (window.ODSVCharts) window.ODSVCharts.redraw(); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
