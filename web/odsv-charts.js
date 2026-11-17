/* ODSV v1.1 – Diagramm-Helfer (optional, ohne Bibliothek). Zeichnet reines SVG in einen Container
   und gestaltet ausschließlich über odsv.css-Klassen (Token-Farben, Achsen-Typo).
   Formen (SPEC 7.3):
     line       Verlauf über Zeit, bis 4 Reihen; Anmerkungen, Zielwert, Endbeschriftung
     bars       Säulen, eine Reihe, bis 12 Zeitpunkte
     columns    Säulen mit mehreren Reihen: gruppiert, gestapelt oder 100 %
     hbars      waagrechte Balken, sortiert – Vergleich von Kategorien
     diverging  Balken ab Nulllinie in divergierenden Farben – Abweichung von Ziel/Null
     funnel     Trichter in abgestufter Einzelfarbe mit Quoten
     histogram  Verteilung in Klassen, optional Median/Mittelwert
     boxplot    Verteilung je Gruppe als Strich + Punkt
     scatter    Zusammenhang zweier Größen, optional Blasengröße und Trendlinie
     heatmap    Größe über zwei Dimensionen in der sequenziellen Palette
     slope      Rang/Wert an zwei Zeitpunkten
     multiples  kleine Vielfache mit gleicher Achse
     donut, spark
   Gemeinsam: label (Pflicht, Aussage für role="img"), Tooltip per Zeiger und Tastatur, Tabellenansicht
   ([data-odsv-chart-table] in der Figure), Legende als Schalter (button.odsv-legend__item[data-odsv-series]).
   Die Zeichnung passt sich der Containerbreite an (ResizeObserver); Schrift bleibt dadurch in px lesbar. */
(function () {
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';
  var MINUS = '−';

  /* ---------- Grundbausteine ---------- */
  function h(tag, attrs, parent) {
    var n = document.createElementNS(NS, tag);
    for (var k in attrs) if (Object.prototype.hasOwnProperty.call(attrs, k)) n.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(n);
    return n;
  }
  function txt(parent, attrs, s) { var t = h('text', attrs, parent); t.textContent = s; return t; }
  function title(node, s) { node.appendChild(document.createElementNS(NS, 'title')).textContent = s; return node; }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function fmtDe(v) {
    if (v == null || isNaN(v)) return '–';
    var s = Number(v).toLocaleString('de-DE', { maximumFractionDigits: 1 });
    return s.charAt(0) === '-' ? MINUS + s.slice(1) : s;
  }
  function signed(fmt) { return function (v) { return (v > 0 ? '+' : '') + fmt(v); }; }
  function niceMax(max) {
    if (max <= 0) return 1;
    var p = Math.pow(10, Math.floor(Math.log(max) / Math.LN10)), f = max / p, n;
    // feinere Stufen, die sich in 4 Teilstriche teilen lassen (277 → 300 statt 500)
    var steps = [1, 1.2, 1.6, 2, 2.4, 3, 4, 5, 6, 8, 10];
    for (var i = 0; i < steps.length; i++) if (f <= steps[i] + 1e-9) { n = steps[i]; break; }
    return n * p;
  }
  function niceStep(x) {
    var p = Math.pow(10, Math.floor(Math.log(x) / Math.LN10)), f = x / p;
    return (f <= 1 ? 1 : f <= 2 ? 2 : f <= 2.5 ? 2.5 : f <= 5 ? 5 : 10) * p;
  }
  /* Achsenbereich mit runden Teilstrichen; schließt 0 ein, wenn zero=true (Balken beginnen immer bei 0). */
  function scale(lo, hi, count, zero) {
    if (zero) { lo = Math.min(0, lo); hi = Math.max(0, hi); }
    if (hi === lo) { hi = lo + 1; }
    var step = niceStep((hi - lo) / (count || 4));
    lo = Math.floor(lo / step + 1e-9) * step; hi = Math.ceil(hi / step - 1e-9) * step;
    var ticks = []; for (var v = lo; v <= hi + step / 2; v += step) ticks.push(Math.abs(v) < step / 1e6 ? 0 : v);
    return { lo: lo, hi: hi, ticks: ticks };
  }
  function quantile(sorted, q) {
    var pos = (sorted.length - 1) * q, b = Math.floor(pos), r = pos - b;
    return sorted[b + 1] !== undefined ? sorted[b] + r * (sorted[b + 1] - sorted[b]) : sorted[b];
  }
  function charW(s) { return String(s).length * 6.6; } // Schätzung für 12–13 px Systemschrift
  function rgbOf(s) {
    s = String(s || '').trim();
    if (s.charAt(0) === '#') { var x = s.slice(1); if (x.length < 6) x = x.split('').map(function (c) { return c + c; }).join(''); return [0, 2, 4].map(function (i) { return parseInt(x.substr(i, 2), 16); }); }
    var m = s.match(/[\d.]+/g); return m ? m.slice(0, 3).map(Number) : [0, 0, 0];
  }
  function lum(c) { return c.map(function (v) { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }).reduce(function (a, v, i) { return a + v * [0.2126, 0.7152, 0.0722][i]; }, 0); }
  function contrast(a, b) { var x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); }

  function mount(el, draw) {
    el._odsvFn = draw; el._odsvLast = 0;
    function run() {
      var w = Math.floor(el.clientWidth);
      if (!w || w === el._odsvLast) return;
      el._odsvLast = w; el._odsvFn(w);
      if (el._odsvTableOpen) renderTable(el);
    }
    el._odsvDraw = function () { el._odsvLast = 0; run(); };
    run();
    if (!el._odsvRO) {
      if (window.ResizeObserver) { el._odsvRO = new ResizeObserver(run); el._odsvRO.observe(el); }
      else { el._odsvRO = true; window.addEventListener('resize', run); }
    }
  }
  function reset(el, w, hgt, label) {
    var old = el.querySelector(':scope > svg, :scope > .odsv-chart__multiples'); if (old) old.remove();
    var svg = h('svg', { width: w, height: hgt, viewBox: '0 0 ' + w + ' ' + hgt, role: 'img', 'aria-label': label || '' });
    el.insertBefore(svg, el.firstChild);
    return svg;
  }
  function hidden(el) { return el._odsvHidden || (el._odsvHidden = {}); }
  function visible(el, s) { return !hidden(el)[s.name]; }

  /* ---------- Tooltip und Ansage ---------- */
  function tipFor(el) {
    var t = el.querySelector('.odsv-chart__tip');
    if (!t) { t = document.createElement('div'); t.className = 'odsv-chart__tip'; t.setAttribute('aria-hidden', 'true'); el.appendChild(t); }
    return t;
  }
  function placeTip(el, tip, x, y, html) {
    tip.innerHTML = html; tip.classList.add('is-visible');
    var tw = tip.offsetWidth, w = el.clientWidth;
    var left = Math.min(Math.max(x + 12, 0), w - tw);
    if (x + tw + 24 > w) left = Math.max(0, x - tw - 12);
    tip.style.left = left + 'px'; tip.style.top = Math.max(0, y - 8) + 'px';
  }
  function hideTip(el) { var t = el.querySelector('.odsv-chart__tip'); if (t) t.classList.remove('is-visible'); }
  function announce(el, s) {
    var r = el.querySelector('.odsv-chart__live');
    if (!r) { r = document.createElement('div'); r.className = 'odsv-chart__live odsv-sr-only'; r.setAttribute('aria-live', 'polite'); el.appendChild(r); }
    r.textContent = s;
  }
  function row(cls, name, value) { return '<span class="' + esc(cls) + '"><span class="odsv-swatch"></span></span> ' + (name ? esc(name) + ': ' : '') + esc(value) + '<br>'; }
  /* Fokus und Pfeiltasten: wandert durch n Positionen, show(i) zeichnet Marke und Tooltip. */
  function keys(el, svg, n, show, clear) {
    svg.setAttribute('tabindex', '0'); svg.setAttribute('focusable', 'true');
    var i = -1;
    svg.addEventListener('focus', function () { if (i < 0) i = 0; show(i, true); });
    svg.addEventListener('blur', function () { clear(); });
    svg.addEventListener('keydown', function (e) {
      var j = i;
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') j = Math.min(n - 1, i + 1);
      else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') j = Math.max(0, i - 1);
      else if (e.key === 'Home') j = 0; else if (e.key === 'End') j = n - 1;
      else if (e.key === 'Escape') { clear(); return; } else return;
      e.preventDefault(); i = j; show(i, true);
    });
  }

  /* ---------- Tabellenansicht ---------- */
  function setTable(el, caption, head, rows) { el._odsvTable = { caption: caption, head: head, rows: rows }; }
  function renderTable(el) {
    var d = el._odsvTable; if (!d) return;
    var wrap = el.nextElementSibling && el.nextElementSibling.classList.contains('odsv-chart__table') ? el.nextElementSibling : null;
    if (!wrap) {
      wrap = document.createElement('div'); wrap.className = 'odsv-table-wrap odsv-chart__table';
      wrap.setAttribute('role', 'region'); wrap.setAttribute('tabindex', '0');
      el.parentNode.insertBefore(wrap, el.nextSibling);
    }
    wrap.setAttribute('aria-label', d.caption); wrap.hidden = !el._odsvTableOpen; wrap.textContent = '';
    var t = document.createElement('table'); t.className = 'odsv-table odsv-table--compact';
    var cap = t.createCaption(); cap.className = 'odsv-sr-only'; cap.textContent = d.caption;
    var tr = t.createTHead().insertRow();
    d.head.forEach(function (c, i) { var th = document.createElement('th'); th.scope = 'col'; th.textContent = c; if (i) th.className = 'odsv-table__num'; tr.appendChild(th); });
    var tb = t.createTBody();
    d.rows.forEach(function (r) {
      var x = tb.insertRow();
      r.forEach(function (c, i) {
        var cell = document.createElement(i ? 'td' : 'th'); if (!i) cell.scope = 'row'; else cell.className = 'odsv-table__num';
        cell.textContent = c; x.appendChild(cell);
      });
    });
    wrap.appendChild(t);
  }
  function plotsOf(btn) { var f = btn.closest('.odsv-chart'); return f ? Array.prototype.slice.call(f.querySelectorAll('.odsv-chart__plot')) : []; }
  document.addEventListener('click', function (e) {
    var t = e.target.closest ? e.target : e.target.parentElement;
    var tb = t && t.closest('[data-odsv-chart-table]');
    if (tb) {
      var open = tb.getAttribute('aria-expanded') !== 'true';
      tb.setAttribute('aria-expanded', open ? 'true' : 'false');
      var lab = tb.querySelector('[data-odsv-label]') || tb;
      lab.textContent = open ? 'Tabelle ausblenden' : 'Daten als Tabelle';
      plotsOf(tb).forEach(function (p) { p._odsvTableOpen = open; renderTable(p); });
      return;
    }
    var lg = t && t.closest('.odsv-chart [data-odsv-series]');
    if (lg) {
      var on = lg.getAttribute('aria-pressed') === 'false';
      var buttons = Array.prototype.slice.call(lg.closest('.odsv-chart').querySelectorAll('[data-odsv-series]'));
      if (!on && buttons.filter(function (b) { return b.getAttribute('aria-pressed') !== 'false'; }).length === 1) return; // eine Reihe bleibt sichtbar
      lg.setAttribute('aria-pressed', on ? 'true' : 'false');
      plotsOf(lg).forEach(function (p) { hidden(p)[lg.getAttribute('data-odsv-series')] = !on; if (p._odsvDraw) p._odsvDraw(); });
    }
  });

  /* ---------- Achsen ---------- */
  function yAxis(g, sc, m, W, y, fmt) {
    sc.ticks.forEach(function (v) {
      var yy = y(v);
      h('line', { x1: m.l, x2: W - m.r, y1: yy, y2: yy, 'class': v === 0 || (v === sc.lo && sc.lo >= 0) ? 'odsv-axis-line' : 'odsv-grid-line' }, g);
      txt(g, { x: m.l - 8, y: yy + 4, 'text-anchor': 'end', 'class': 'odsv-axis-text' }, fmt(v));
    });
  }
  function xAxisV(g, sc, m, H, x, fmt) { // senkrechte Gitterlinien, Werte unten (waagrechte Balken, Streudiagramm)
    sc.ticks.forEach(function (v) {
      var xx = x(v);
      h('line', { x1: xx, x2: xx, y1: m.t, y2: H - m.b, 'class': v === 0 ? 'odsv-axis-line' : 'odsv-grid-line' }, g);
      txt(g, { x: xx, y: H - m.b + 18, 'text-anchor': 'middle', 'class': 'odsv-axis-text' }, fmt(v));
    });
  }
  function unit(g, x, y, s, anchor) { if (s) txt(g, { x: x, y: y, 'text-anchor': anchor || 'start', 'class': 'odsv-axis-title' }, s); }
  function barPath(x0, x1, y0, y1, r) { // senkrechte Säule, Datenende bei y1 gerundet
    var up = y1 < y0; r = Math.min(r, Math.abs(x1 - x0) / 2, Math.abs(y1 - y0));
    var s = up ? 1 : -1;
    return 'M' + x0 + ' ' + y0 + 'V' + (y1 + s * r) + 'Q' + x0 + ' ' + y1 + ' ' + (x0 + r) + ' ' + y1 + 'H' + (x1 - r) + 'Q' + x1 + ' ' + y1 + ' ' + x1 + ' ' + (y1 + s * r) + 'V' + y0 + 'Z';
  }
  function hbarPath(x0, x1, y0, y1, r) { // waagrechter Balken, Datenende bei x1 gerundet
    var right = x1 > x0; r = Math.min(r, Math.abs(y1 - y0) / 2, Math.abs(x1 - x0));
    var s = right ? -1 : 1;
    return 'M' + x0 + ' ' + y0 + 'H' + (x1 + s * r) + 'Q' + x1 + ' ' + y0 + ' ' + x1 + ' ' + (y0 + r) + 'V' + (y1 - r) + 'Q' + x1 + ' ' + y1 + ' ' + (x1 + s * r) + ' ' + y1 + 'H' + x0 + 'Z';
  }
  /* Beschriftungen senkrecht entzerren (Endbeschriftung, Steigungsdiagramm). */
  function spread(items, minGap, lo, hi) {
    items.sort(function (a, b) { return a.y - b.y; });
    for (var i = 1; i < items.length; i++) if (items[i].y - items[i - 1].y < minGap) items[i].y = items[i - 1].y + minGap;
    var over = items.length ? items[items.length - 1].y - hi : 0;
    if (over > 0) for (var j = items.length - 1; j >= 0; j--) { items[j].y -= over; if (j && items[j].y - items[j - 1].y >= minGap) break; }
    if (items.length && items[0].y < lo) { var d = lo - items[0].y; items.forEach(function (it) { it.y += d; }); }
    return items;
  }

  /* ---------- Linie ---------- */
  function line(el, o) {
    var H = o.height || 240, fmt = o.yFormat || fmtDe, tip = tipFor(el), n = o.labels.length;
    setTable(el, o.label || 'Daten', [o.xTitle || ''].concat(o.series.map(function (s) { return s.name || 'Wert'; })),
      o.labels.map(function (l, i) { return [l].concat(o.series.map(function (s) { return fmt(s.values[i]); })); }));
    mount(el, function (W) {
      var svg = reset(el, W, H, o.label), vis = o.series.filter(function (s) { return visible(el, s); });
      var endW = 0;
      if (o.endLabels) vis.forEach(function (s) { endW = Math.max(endW, charW((s.name || '') + ' ' + fmt(s.values[n - 1]))); });
      var m = { l: 44, r: o.endLabels ? Math.min(160, endW + 20) : 12, t: o.unit || o.annotations ? 24 : 12, b: 28 }, iw = W - m.l - m.r, ih = H - m.t - m.b;
      var lo = Infinity, hi = -Infinity;
      o.series.forEach(function (s) { s.values.forEach(function (v) { if (v == null) return; lo = Math.min(lo, v); hi = Math.max(hi, v); }); });
      if (o.target) { lo = Math.min(lo, o.target.value); hi = Math.max(hi, o.target.value); }
      var sc = o.yMin != null || lo < 0 ? scale(o.yMin != null ? o.yMin : lo, o.yMax || hi, o.yTicks || 4, false) : { lo: 0, hi: o.yMax || niceMax(hi), ticks: [] };
      if (!sc.ticks.length) { var tk = o.yTicks || 4; for (var t = 0; t <= tk; t++) sc.ticks.push((sc.hi / tk) * t); }
      var x = function (i) { return m.l + (n < 2 ? iw / 2 : (i * iw) / (n - 1)); };
      var y = function (v) { return m.t + ih - ((v - sc.lo) / (sc.hi - sc.lo)) * ih; };
      var g = h('g', {}, svg);
      yAxis(g, sc, m, W, y, fmt);
      unit(g, m.l - 8, 12, o.unit, 'start');
      var gap = Math.max(1, Math.ceil(64 / (n < 2 ? 64 : iw / (n - 1))));
      for (var li = n - 1; li >= 0; li -= gap) {
        var a = li === 0 ? 'start' : li === n - 1 ? 'end' : 'middle';
        txt(g, { x: x(li), y: H - 8, 'text-anchor': a, 'class': 'odsv-axis-text' }, o.labels[li]);
      }
      (o.annotations || []).forEach(function (an) {
        var ax = x(an.at);
        h('line', { x1: ax, x2: ax, y1: m.t - 4, y2: m.t + ih, 'class': 'odsv-data-event' }, g);
        var tw = charW(an.label) + 14, lx = Math.min(Math.max(ax - tw / 2, m.l), W - m.r - tw);
        h('rect', { x: lx, y: 2, width: tw, height: 18, rx: 9, 'class': 'odsv-data-pill' }, g);
        txt(g, { x: lx + tw / 2, y: 15, 'text-anchor': 'middle', 'class': 'odsv-data-pill-text' }, an.label);
      });
      if (o.target) {
        var ty = y(o.target.value);
        h('line', { x1: m.l, x2: W - m.r, y1: ty, y2: ty, 'class': 'odsv-data-ref' }, g);
        if (o.target.label) {
          // Label dort, wo die Linien am weitesten weg sind: links (Anfang) oder rechts (Ende), oberhalb oder unterhalb
          var dist = function (i) { return Math.min.apply(null, o.series.map(function (s) { return s.values[i] == null ? 1e9 : Math.abs(y(s.values[i]) - ty); })); };
          var atEnd = dist(n - 1) > dist(0), above = true, ix = atEnd ? n - 1 : 0;
          o.series.forEach(function (s) { var v = s.values[ix]; if (v != null && y(v) < ty && ty - y(v) < 20) above = false; });
          txt(g, { x: atEnd ? W - m.r : m.l + 4, y: above ? ty - 6 : ty + 15, 'text-anchor': atEnd ? 'end' : 'start', 'class': 'odsv-data-label' }, o.target.label);
        }
      }
      var ends = [];
      vis.forEach(function (s) {
        var sg = h('g', { 'class': s.cls || 'odsv-dv-1' }, svg), d = '', pen = false;
        s.values.forEach(function (v, i) { if (v == null) { pen = false; return; } d += (pen ? 'L' : 'M') + x(i).toFixed(1) + ' ' + y(v).toFixed(1); pen = true; });
        if (s.area) h('path', { d: d + 'L' + x(n - 1).toFixed(1) + ' ' + y(Math.max(sc.lo, 0)) + 'L' + x(0).toFixed(1) + ' ' + y(Math.max(sc.lo, 0)) + 'Z', 'class': 'odsv-data-area' }, sg);
        h('path', { d: d, 'class': 'odsv-data-line' + (s.dash ? ' odsv-data-dash' : '') }, sg);
        var last = s.values.length - 1;
        if (s.values[last] != null) {
          h('circle', { cx: x(last), cy: y(s.values[last]), r: 4, 'class': 'odsv-data-point' }, sg);
          ends.push({ y: y(s.values[last]) + 4, s: s, v: s.values[last] });
        }
      });
      if (o.endLabels) spread(ends, 15, m.t + 4, m.t + ih).forEach(function (e) {
        txt(svg, { x: W - m.r + 10, y: e.y, 'class': 'odsv-data-label' }, (e.s.name ? e.s.name + ' ' : '') + fmt(e.v));
      });
      var cur = h('line', { y1: m.t, y2: m.t + ih, 'class': 'odsv-cursor-line', style: 'display:none' }, svg);
      var pts = vis.map(function (s) { var c = h('g', { 'class': s.cls || 'odsv-dv-1', style: 'display:none' }, svg); h('circle', { r: 5, 'class': 'odsv-data-point' }, c); return c; });
      var hit = h('rect', { x: m.l, y: m.t, width: iw, height: ih, fill: 'none', 'pointer-events': 'all' }, svg);
      function show(i, say) {
        cur.setAttribute('x1', x(i)); cur.setAttribute('x2', x(i)); cur.style.display = '';
        var html = '<b>' + esc(o.labels[i]) + '</b>', spoken = o.labels[i] + ': ';
        vis.forEach(function (s, k) {
          var v = s.values[i];
          if (v == null) { pts[k].style.display = 'none'; } else { pts[k].style.display = ''; pts[k].firstChild.setAttribute('cx', x(i)); pts[k].firstChild.setAttribute('cy', y(v)); }
          html += row(s.cls || 'odsv-dv-1', s.name, fmt(v)); spoken += (s.name ? s.name + ' ' : '') + fmt(v) + '; ';
        });
        placeTip(el, tip, x(i), m.t + 24, html);
        if (say) announce(el, spoken);
      }
      function clear() { cur.style.display = 'none'; pts.forEach(function (p) { p.style.display = 'none'; }); hideTip(el); }
      hit.addEventListener('pointermove', function (ev) {
        var r = svg.getBoundingClientRect(), px = ev.clientX - r.left;
        show(Math.max(0, Math.min(n - 1, Math.round(((px - m.l) / iw) * (n - 1)))), false);
      });
      hit.addEventListener('pointerleave', clear);
      keys(el, svg, n, show, clear);
    });
  }

  /* ---------- Säulen (eine Reihe) ---------- */
  function bars(el, o) {
    var H = o.height || 240, fmt = o.yFormat || fmtDe, n = o.labels.length;
    setTable(el, o.label || 'Daten', [o.xTitle || '', o.name || 'Wert'], o.labels.map(function (l, i) { return [l, fmt(o.values[i])]; }));
    mount(el, function (W) {
      var svg = reset(el, W, H, o.label);
      var m = { l: 44, r: 8, t: o.unit ? 28 : 20, b: 28 }, iw = W - m.l - m.r, ih = H - m.t - m.b;
      var max = Math.max.apply(null, o.values), top = o.yMax || niceMax(max), ticks = o.yTicks || 4, sc = { lo: 0, hi: top, ticks: [] };
      for (var t = 0; t <= ticks; t++) sc.ticks.push((top / ticks) * t);
      var y = function (v) { return m.t + ih - (v / top) * ih; };
      yAxis(svg, sc, m, W, y, fmt); unit(svg, m.l - 8, 12, o.unit);
      var slot = iw / n, bw = Math.min(40, slot * 0.62), showVals = bw >= 22;
      o.values.forEach(function (val, i) {
        var cls = (o.colors && o.colors[i]) || o.cls || 'odsv-dv-1', cx = m.l + slot * i + slot / 2;
        var gg = h('g', { 'class': cls }, svg);
        title(h('path', { d: barPath(cx - bw / 2, cx + bw / 2, m.t + ih, y(val), 4), 'class': 'odsv-data-bar' }, gg), o.labels[i] + ': ' + fmt(val));
        if (showVals && val > 0) txt(svg, { x: cx, y: y(val) - 6, 'text-anchor': 'middle', 'class': 'odsv-data-label' }, fmt(val));
        txt(svg, { x: cx, y: H - 8, 'text-anchor': 'middle', 'class': 'odsv-axis-text' }, o.labels[i]);
      });
    });
  }

  /* ---------- Säulen mit mehreren Reihen ---------- */
  function columns(el, o) {
    var H = o.height || 260, mode = o.mode || 'grouped', pct = mode === 'percent', stacked = mode !== 'grouped';
    var fmt = o.yFormat || (pct ? function (v) { return fmtDe(v) + ' %'; } : fmtDe), n = o.labels.length, tip = tipFor(el);
    var vfmt = o.valueFormat || fmtDe;
    setTable(el, o.label || 'Daten', [o.xTitle || ''].concat(o.series.map(function (s) { return s.name; })),
      o.labels.map(function (l, i) { return [l].concat(o.series.map(function (s) { return vfmt(s.values[i]); })); }));
    mount(el, function (W) {
      var svg = reset(el, W, H, o.label), vis = o.series.filter(function (s) { return visible(el, s); });
      var m = { l: 44, r: 8, t: o.unit ? 28 : 16, b: 28 }, iw = W - m.l - m.r, ih = H - m.t - m.b;
      var totals = o.labels.map(function (_, i) { return vis.reduce(function (a, s) { return a + (s.values[i] || 0); }, 0); });
      var hi = pct ? 100 : stacked ? Math.max.apply(null, totals) : Math.max.apply(null, vis.map(function (s) { return Math.max.apply(null, s.values); }));
      var top = pct ? 100 : (o.yMax || niceMax(hi)), sc = { lo: 0, hi: top, ticks: [] }, tk = o.yTicks || 4;
      for (var t = 0; t <= tk; t++) sc.ticks.push((top / tk) * t);
      var y = function (v) { return m.t + ih - (v / top) * ih; };
      yAxis(svg, sc, m, W, y, fmt); unit(svg, m.l - 8, 12, o.unit);
      var slot = iw / n, groupW = Math.min(stacked ? 48 : 18 * vis.length + 4 * (vis.length - 1), slot * 0.72);
      var bw = stacked ? groupW : Math.max(4, (groupW - 3 * (vis.length - 1)) / Math.max(1, vis.length));
      var labelEvery = Math.max(1, Math.ceil(56 / slot));
      o.labels.forEach(function (l, i) {
        var cx = m.l + slot * i + slot / 2, acc = 0;
        vis.forEach(function (s, k) {
          var raw = s.values[i] || 0, v = pct ? (totals[i] ? raw / totals[i] * 100 : 0) : raw, gg = h('g', { 'class': s.cls }, svg), p;
          if (stacked) {
            var y0 = y(acc), y1 = y(acc + v), topSeg = k === vis.length - 1;
            p = topSeg ? h('path', { d: barPath(cx - bw / 2, cx + bw / 2, y0, y1, 4), 'class': 'odsv-data-bar odsv-data-bar--seg' }, gg)
                       : h('rect', { x: cx - bw / 2, y: y1, width: bw, height: Math.max(0, y0 - y1), 'class': 'odsv-data-bar odsv-data-bar--seg' }, gg);
            acc += v;
          } else {
            var x0 = cx - groupW / 2 + k * (bw + 3);
            p = h('path', { d: barPath(x0, x0 + bw, y(0), y(v), 3), 'class': 'odsv-data-bar' }, gg);
          }
          title(p, l + ' · ' + s.name + ': ' + vfmt(raw) + (pct ? ' (' + fmtDe(v) + ' %)' : ''));
        });
        if (i % labelEvery === 0) txt(svg, { x: cx, y: H - 8, 'text-anchor': 'middle', 'class': 'odsv-axis-text' }, l);
      });
      var band = h('rect', { y: m.t, height: ih, width: slot, 'class': 'odsv-data-band', style: 'display:none' }, svg);
      svg.insertBefore(band, svg.firstChild);
      function show(i, say) {
        band.setAttribute('x', m.l + slot * i); band.style.display = '';
        var html = '<b>' + esc(o.labels[i]) + '</b>', spoken = o.labels[i] + ': ';
        vis.slice().reverse().forEach(function (s) { var raw = s.values[i]; html += row(s.cls, s.name, vfmt(raw) + (pct && totals[i] ? ' · ' + fmtDe(raw / totals[i] * 100) + ' %' : '')); spoken += s.name + ' ' + vfmt(raw) + '; '; });
        if (stacked && !pct) html += '<b>Summe ' + esc(vfmt(totals[i])) + '</b>';
        placeTip(el, tip, m.l + slot * i + slot / 2, m.t + 16, html);
        if (say) announce(el, spoken);
      }
      function clear() { band.style.display = 'none'; hideTip(el); }
      var hit = h('rect', { x: m.l, y: m.t, width: iw, height: ih, fill: 'none', 'pointer-events': 'all' }, svg);
      hit.addEventListener('pointermove', function (ev) { var r = svg.getBoundingClientRect(); show(Math.max(0, Math.min(n - 1, Math.floor((ev.clientX - r.left - m.l) / slot))), false); });
      hit.addEventListener('pointerleave', clear);
      keys(el, svg, n, show, clear);
    });
  }

  /* ---------- Waagrechte Balken (Vergleich, Trichter, Abweichung) ---------- */
  function hbarsCore(el, o, kind) {
    var fmt = o.format || (kind === 'diverging' ? signed(fmtDe) : fmtDe), tip = tipFor(el);
    var items = o.labels.map(function (l, i) { return { label: l, value: o.values[i], cls: (o.colors && o.colors[i]) || o.cls, i: i }; });
    if (kind === 'bars' && o.sort !== false) items.sort(function (a, b) { return b.value - a.value; });
    if (kind === 'diverging' && o.sort) items.sort(function (a, b) { return b.value - a.value; });
    var first = items.length ? items[0].value : 0;
    var head = [o.categoryTitle || '', o.name || 'Wert'];
    if (kind === 'funnel') head = head.concat(['Anteil am Start', 'Quote zum Vorschritt']);
    setTable(el, o.label || 'Daten', head, items.map(function (it, k) {
      var r = [it.label, fmt(it.value)];
      if (kind === 'funnel') r.push(fmtDe(first ? it.value / first * 100 : 0) + ' %', k ? fmtDe(items[k - 1].value ? it.value / items[k - 1].value * 100 : 0) + ' %' : '–');
      return r;
    }));
    var rowH = o.rowHeight || 32, bar = Math.min(20, rowH - 10);
    mount(el, function (W) {
      var labW = o.labelWidth || Math.min(W * 0.38, Math.max.apply(null, items.map(function (it) { return charW(it.label); })) + 12);
      var maxVal = Math.max.apply(null, items.map(function (it) { return charW(fmt(it.value)); }));
      var valW = kind === 'funnel' ? maxVal + charW(' · 100 %') + 12 : maxVal + 12;
      var m = { l: labW, r: valW, t: o.unit || (kind === 'diverging' && (o.negLabel || o.posLabel)) ? 24 : 4, b: kind === 'funnel' ? 6 : 26 };
      if (kind === 'diverging') m.l = valW; // Werte stehen außen an beiden Enden, Kategorien innen an der Nulllinie
      var H = m.t + m.b + items.length * rowH, svg = reset(el, W, H, o.label), iw = W - m.l - m.r;
      var lo = Math.min.apply(null, items.map(function (it) { return it.value; })), hi = Math.max.apply(null, items.map(function (it) { return it.value; }));
      var sc;
      if (kind === 'diverging') { var mx = Math.max(Math.abs(lo), Math.abs(hi)); sc = scale(-mx, mx, 4, true); var e = Math.max(-sc.lo, sc.hi); sc = scale(-e, e, 4, true); }
      else sc = scale(0, o.max || hi, 4, true);
      var x = function (v) { return m.l + ((v - sc.lo) / (sc.hi - sc.lo)) * iw; };
      var g = h('g', {}, svg);
      if (kind !== 'funnel') xAxisV(g, sc, m, H, x, kind === 'diverging' ? signed(o.axisFormat || fmtDe) : (o.axisFormat || fmtDe));
      unit(g, m.l, 14, o.unit);
      items.forEach(function (it, k) {
        var cy = m.t + k * rowH + rowH / 2, y0 = cy - bar / 2, y1 = cy + bar / 2, cls = it.cls, p;
        if (kind === 'funnel') cls = cls || 'odsv-dv-seq-' + Math.max(1, 6 - Math.round(k * 5 / Math.max(1, items.length - 1)));
        if (kind === 'diverging') cls = cls || (it.value < 0 ? 'odsv-dv-div-neg' : 'odsv-dv-div-pos');
        cls = cls || 'odsv-dv-1';
        var gg = h('g', { 'class': cls }, svg);
        if (it.value !== 0) p = h('path', { d: hbarPath(x(0), x(it.value), y0, y1, 4), 'class': 'odsv-data-bar' }, gg);
        else p = h('rect', { x: x(0) - 1, y: y0, width: 2, height: bar, 'class': 'odsv-data-bar' }, gg);
        title(p, it.label + ': ' + fmt(it.value));
        var lx = kind === 'diverging' ? (it.value < 0 ? x(0) + 8 : x(0) - 8) : m.l - 10;
        txt(svg, { x: lx, y: cy + 4, 'text-anchor': kind === 'diverging' && it.value < 0 ? 'start' : 'end', 'class': 'odsv-axis-text odsv-axis-text--cat' }, it.label);
        var vx = it.value < 0 ? x(it.value) - 6 : x(it.value) + 6;
        var vtxt = fmt(it.value);
        if (kind === 'funnel' && k) vtxt += ' · ' + fmtDe(items[k - 1].value ? it.value / items[k - 1].value * 100 : 0) + ' %';
        txt(svg, { x: vx, y: cy + 4, 'text-anchor': it.value < 0 ? 'end' : 'start', 'class': 'odsv-data-label' }, vtxt);
      });
      if (kind === 'diverging') {
        // Kategorie steht auf der Gegenseite der Null: Platz dafür schaffen, indem Balken die halbe Fläche nutzen
        var nl = o.negLabel, pl = o.posLabel;
        if (nl) txt(g, { x: m.l, y: 14, 'class': 'odsv-axis-title' }, '← ' + nl);
        if (pl) txt(g, { x: W - m.r, y: 14, 'text-anchor': 'end', 'class': 'odsv-axis-title' }, pl + ' →');
      }
      var focus = h('rect', { x: 0, width: W, height: rowH, 'class': 'odsv-data-band', style: 'display:none' }, svg);
      svg.insertBefore(focus, svg.firstChild);
      function show(k, say) {
        var it = items[k]; focus.setAttribute('y', m.t + k * rowH); focus.style.display = '';
        if (say) announce(el, it.label + ': ' + fmt(it.value));
      }
      function clear() { focus.style.display = 'none'; hideTip(el); }
      keys(el, svg, items.length, show, clear);
    });
  }
  function hbars(el, o) { hbarsCore(el, o, 'bars'); }
  function diverging(el, o) { hbarsCore(el, o, 'diverging'); }
  function funnel(el, o) { hbarsCore(el, { labels: o.steps.map(function (s) { return s.label; }), values: o.steps.map(function (s) { return s.value; }), format: o.format, label: o.label, cls: o.cls, unit: o.unit, name: o.name, rowHeight: o.rowHeight }, 'funnel'); }

  /* ---------- Histogramm ---------- */
  function histogram(el, o) {
    var H = o.height || 220, xf = o.xFormat || fmtDe, tip = tipFor(el);
    var vals = o.values.filter(function (v) { return v != null && !isNaN(v); }).sort(function (a, b) { return a - b; });
    var lo = vals[0], hi = vals[vals.length - 1];
    var w = o.binWidth || niceStep((hi - lo) / (o.bins || 10) || 1), start = Math.floor(lo / w) * w, nb = Math.max(1, Math.ceil((hi - start) / w + 1e-9));
    if (start + nb * w <= hi) nb++;
    var counts = []; for (var b = 0; b < nb; b++) counts.push(0);
    vals.forEach(function (v) { counts[Math.min(nb - 1, Math.floor((v - start) / w))]++; });
    var med = quantile(vals, 0.5), mean = vals.reduce(function (a, v) { return a + v; }, 0) / vals.length;
    setTable(el, o.label || 'Verteilung', ['Klasse', 'Anzahl'], counts.map(function (c, i) { return [xf(start + i * w) + ' bis unter ' + xf(start + (i + 1) * w), fmtDe(c)]; }));
    mount(el, function (W) {
      var svg = reset(el, W, H, o.label), m = { l: 44, r: 12, t: o.mark || o.unit ? 28 : 12, b: 28 }, iw = W - m.l - m.r, ih = H - m.t - m.b;
      var top = niceMax(Math.max.apply(null, counts)), sc = { lo: 0, hi: top, ticks: [] };
      for (var t = 0; t <= 4; t++) sc.ticks.push(top / 4 * t);
      var y = function (v) { return m.t + ih - (v / top) * ih; }, x = function (v) { return m.l + ((v - start) / (nb * w)) * iw; };
      yAxis(svg, sc, m, W, y, fmtDe); unit(svg, m.l - 8, 12, o.unit || 'Anzahl');
      var g = h('g', { 'class': o.cls || 'odsv-dv-2' }, svg);
      counts.forEach(function (c, i) {
        var x0 = x(start + i * w) + 1, x1 = x(start + (i + 1) * w) - 1;
        if (c) title(h('path', { d: barPath(x0, x1, y(0), y(c), 3), 'class': 'odsv-data-bar' }, g), xf(start + i * w) + ' bis unter ' + xf(start + (i + 1) * w) + ': ' + fmtDe(c));
      });
      var every = Math.max(1, Math.ceil(56 / (iw / nb)));
      for (var e = 0; e <= nb; e += every) txt(svg, { x: x(start + e * w), y: H - 8, 'text-anchor': e === 0 ? 'start' : e >= nb ? 'end' : 'middle', 'class': 'odsv-axis-text' }, xf(start + e * w));
      if (o.mark) {
        var mv = o.mark === 'mean' ? mean : med, mx = x(mv), ml = (o.mark === 'mean' ? 'Mittelwert ' : 'Median ') + xf(mv);
        h('line', { x1: mx, x2: mx, y1: 20, y2: m.t + ih, 'class': 'odsv-data-ref' }, svg);
        var pw = charW(ml) + 14, minX = m.l + charW(o.unit || 'Anzahl') + 12, px = Math.min(Math.max(mx - pw / 2, minX), W - m.r - pw);
        h('rect', { x: px, y: 2, width: pw, height: 18, rx: 9, 'class': 'odsv-data-pill' }, svg);
        txt(svg, { x: px + pw / 2, y: 15, 'text-anchor': 'middle', 'class': 'odsv-data-pill-text odsv-data-pill-text--plain' }, ml); // Einheiten nie versalisieren
      }
      function show(i, say) { if (say) announce(el, xf(start + i * w) + ' bis unter ' + xf(start + (i + 1) * w) + ': ' + fmtDe(counts[i])); placeTip(el, tip, x(start + (i + 0.5) * w), y(counts[i]), '<b>' + esc(xf(start + i * w) + ' – ' + xf(start + (i + 1) * w)) + '</b>' + esc(fmtDe(counts[i])) + ' Werte'); }
      keys(el, svg, nb, show, function () { hideTip(el); });
    });
  }

  /* ---------- Boxplot (Strich + Punkt) ---------- */
  function stats(values) {
    var s = values.filter(function (v) { return v != null && !isNaN(v); }).sort(function (a, b) { return a - b; });
    var q1 = quantile(s, 0.25), q3 = quantile(s, 0.75), iqr = q3 - q1, lo = q1 - 1.5 * iqr, hi = q3 + 1.5 * iqr;
    var inner = s.filter(function (v) { return v >= lo && v <= hi; });
    return { n: s.length, min: inner[0], max: inner[inner.length - 1], q1: q1, med: quantile(s, 0.5), q3: q3, out: s.filter(function (v) { return v < lo || v > hi; }) };
  }
  function boxplot(el, o) {
    var xf = o.format || fmtDe, tip = tipFor(el), rowH = 40;
    var gs = o.groups.map(function (g) { var st = stats(g.values); st.label = g.label; st.cls = g.cls || o.cls || 'odsv-dv-2'; return st; });
    setTable(el, o.label || 'Verteilung', ['Gruppe', 'Minimum', '1. Quartil', 'Median', '3. Quartil', 'Maximum', 'Ausreißer', 'n'],
      gs.map(function (s) { return [s.label, xf(s.min), xf(s.q1), xf(s.med), xf(s.q3), xf(s.max), s.out.length ? s.out.map(xf).join(', ') : '–', fmtDe(s.n)]; }));
    mount(el, function (W) {
      var labW = Math.min(W * 0.32, Math.max.apply(null, gs.map(function (s) { return charW(s.label); })) + 14);
      var m = { l: labW, r: 16, t: o.unit ? 22 : 6, b: 26 }, H = m.t + m.b + gs.length * rowH, svg = reset(el, W, H, o.label), iw = W - m.l - m.r;
      var all = []; o.groups.forEach(function (g) { all = all.concat(g.values); });
      var sc = scale(o.min != null ? o.min : Math.min.apply(null, all), o.max != null ? o.max : Math.max.apply(null, all), 4, false);
      var x = function (v) { return m.l + ((v - sc.lo) / (sc.hi - sc.lo)) * iw; };
      var g = h('g', {}, svg); xAxisV(g, sc, m, H, x, xf); unit(g, m.l, 14, o.unit);
      gs.forEach(function (s, k) {
        var cy = m.t + k * rowH + rowH / 2, gg = h('g', { 'class': s.cls }, svg);
        txt(svg, { x: m.l - 10, y: cy + 4, 'text-anchor': 'end', 'class': 'odsv-axis-text odsv-axis-text--cat' }, s.label);
        h('line', { x1: x(s.min), x2: x(s.max), y1: cy, y2: cy, 'class': 'odsv-data-whisker' }, gg);
        h('line', { x1: x(s.q1), x2: x(s.q3), y1: cy, y2: cy, 'class': 'odsv-data-box' }, gg);
        title(h('circle', { cx: x(s.med), cy: cy, r: 6, 'class': 'odsv-data-point' }, gg), s.label + ': Median ' + xf(s.med) + ', Quartile ' + xf(s.q1) + '–' + xf(s.q3) + ', Spanne ' + xf(s.min) + '–' + xf(s.max));
        s.out.forEach(function (v) { h('circle', { cx: x(v), cy: cy, r: 3.5, 'class': 'odsv-data-outlier' }, gg); });
      });
      function show(k, say) {
        var s = gs[k], cy = m.t + k * rowH + rowH / 2;
        placeTip(el, tip, x(s.med), cy - 4, '<b>' + esc(s.label) + '</b>Median ' + esc(xf(s.med)) + '<br>Quartile ' + esc(xf(s.q1)) + ' – ' + esc(xf(s.q3)) + '<br>Spanne ' + esc(xf(s.min)) + ' – ' + esc(xf(s.max)) + (s.out.length ? '<br>' + s.out.length + ' Ausreißer' : ''));
        if (say) announce(el, s.label + ': Median ' + xf(s.med) + ', Quartile ' + xf(s.q1) + ' bis ' + xf(s.q3));
      }
      keys(el, svg, gs.length, show, function () { hideTip(el); });
      Array.prototype.forEach.call(svg.querySelectorAll('.odsv-data-point'), function (p, k) { p.addEventListener('pointerenter', function () { show(k, false); }); p.addEventListener('pointerleave', function () { hideTip(el); }); });
    });
  }

  /* ---------- Streudiagramm ---------- */
  function scatter(el, o) {
    var H = o.height || 300, xf = o.xFormat || fmtDe, yf = o.yFormat || fmtDe, tip = tipFor(el);
    var rows = []; o.series.forEach(function (s) { s.points.forEach(function (p) { rows.push([p.label || s.name, xf(p.x), yf(p.y)].concat(o.sizeName ? [fmtDe(p.r)] : []).concat(o.series.length > 1 ? [s.name] : [])); }); });
    setTable(el, o.label || 'Daten', ['Punkt', o.xLabel || 'x', o.yLabel || 'y'].concat(o.sizeName ? [o.sizeName] : []).concat(o.series.length > 1 ? ['Reihe'] : []), rows);
    mount(el, function (W) {
      var svg = reset(el, W, H, o.label), m = { l: 48, r: 16, t: 24, b: 40 }, iw = W - m.l - m.r, ih = H - m.t - m.b;
      var xs = [], ys = [], rs = [];
      o.series.forEach(function (s) { s.points.forEach(function (p) { xs.push(p.x); ys.push(p.y); if (p.r != null) rs.push(p.r); }); });
      var sx = scale(o.xMin != null ? o.xMin : Math.min.apply(null, xs), o.xMax != null ? o.xMax : Math.max.apply(null, xs), 5, !!o.xZero);
      var sy = scale(o.yMin != null ? o.yMin : Math.min.apply(null, ys), o.yMax != null ? o.yMax : Math.max.apply(null, ys), 4, !!o.yZero);
      var x = function (v) { return m.l + ((v - sx.lo) / (sx.hi - sx.lo)) * iw; }, y = function (v) { return m.t + ih - ((v - sy.lo) / (sy.hi - sy.lo)) * ih; };
      var rMax = rs.length ? Math.max.apply(null, rs) : 1, rad = function (p) { return p.r != null ? 4 + Math.sqrt(p.r / rMax) * 14 : 5; };
      var g = h('g', {}, svg);
      yAxis(g, sy, m, W, y, yf);
      sx.ticks.forEach(function (v) { txt(g, { x: x(v), y: H - m.b + 18, 'text-anchor': 'middle', 'class': 'odsv-axis-text' }, xf(v)); });
      unit(g, m.l - 8, 12, o.yLabel); unit(g, W - m.r, H - 4, o.xLabel, 'end');
      var vis = o.series.filter(function (s) { return visible(el, s); }), pts = [];
      if (o.trend) {
        var all = []; vis.forEach(function (s) { all = all.concat(s.points); });
        if (all.length > 2) {
          var n = all.length, mx = 0, my = 0; all.forEach(function (p) { mx += p.x / n; my += p.y / n; });
          var sxy = 0, sxx = 0, syy = 0; all.forEach(function (p) { sxy += (p.x - mx) * (p.y - my); sxx += (p.x - mx) * (p.x - mx); syy += (p.y - my) * (p.y - my); });
          var k = sxx ? sxy / sxx : 0, d = my - k * mx, r2 = sxx && syy ? (sxy * sxy) / (sxx * syy) : 0;
          var tl = title(h('line', { x1: x(sx.lo), y1: y(k * sx.lo + d), x2: x(sx.hi), y2: y(k * sx.hi + d), 'class': 'odsv-data-trend' }, g), 'Trend (lineare Regression), R² = ' + fmtDe(Math.round(r2 * 100) / 100));
          var clip = h('clipPath', { id: 'odsv-clip-' + (el._odsvId || (el._odsvId = Math.random().toString(36).slice(2))) }, svg);
          h('rect', { x: m.l, y: m.t, width: iw, height: ih }, clip); tl.setAttribute('clip-path', 'url(#' + clip.id + ')');
          txt(g, { x: W - m.r, y: m.t + 12, 'text-anchor': 'end', 'class': 'odsv-axis-text' }, 'Trend · R² ' + fmtDe(Math.round(r2 * 100) / 100));
        }
      }
      vis.forEach(function (s) {
        var sg = h('g', { 'class': s.cls || 'odsv-dv-2' }, svg);
        s.points.slice().sort(function (a, b) { return (b.r || 0) - (a.r || 0); }).forEach(function (p) {
          var c = h('circle', { cx: x(p.x), cy: y(p.y), r: rad(p), 'class': p.r != null ? 'odsv-data-bubble' : 'odsv-data-point' }, sg);
          pts.push({ p: p, s: s, cx: x(p.x), cy: y(p.y), node: c });
          if (p.label && p.annotate !== false && p.highlight) txt(svg, { x: x(p.x) + rad(p) + 4, y: y(p.y) + 4, 'class': 'odsv-data-label' }, p.label);
        });
      });
      pts.sort(function (a, b) { return a.cx - b.cx; });
      var ring = h('circle', { r: 9, 'class': 'odsv-data-focus', style: 'display:none' }, svg);
      function show(i, say) {
        var q = pts[i]; if (!q) return;
        ring.setAttribute('cx', q.cx); ring.setAttribute('cy', q.cy); ring.setAttribute('r', (+q.node.getAttribute('r')) + 4); ring.style.display = '';
        var html = '<b>' + esc(q.p.label || q.s.name || '') + '</b>' + (o.xLabel ? esc(o.xLabel) + ': ' : 'x: ') + esc(xf(q.p.x)) + '<br>' + (o.yLabel ? esc(o.yLabel) + ': ' : 'y: ') + esc(yf(q.p.y)) + (q.p.r != null ? '<br>' + esc((o.sizeName || 'Größe') + ': ' + fmtDe(q.p.r)) : '');
        placeTip(el, tip, q.cx, q.cy, html);
        if (say) announce(el, (q.p.label || q.s.name || '') + ': ' + xf(q.p.x) + ', ' + yf(q.p.y));
      }
      function clear() { ring.style.display = 'none'; hideTip(el); }
      var hit = h('rect', { x: m.l, y: m.t, width: iw, height: ih, fill: 'none', 'pointer-events': 'all' }, svg);
      hit.addEventListener('pointermove', function (ev) {
        var r = svg.getBoundingClientRect(), px = ev.clientX - r.left, py = ev.clientY - r.top, best = -1, bd = 24 * 24;
        pts.forEach(function (q, i) { var dd = (q.cx - px) * (q.cx - px) + (q.cy - py) * (q.cy - py); if (dd < bd) { bd = dd; best = i; } });
        if (best < 0) clear(); else show(best, false);
      });
      hit.addEventListener('pointerleave', clear);
      keys(el, svg, pts.length, show, clear);
    });
  }

  /* ---------- Heatmap ---------- */
  function heatmap(el, o) {
    var vf = o.format || fmtDe, tip = tipFor(el), steps = 6;
    var flat = []; o.values.forEach(function (r) { r.forEach(function (v) { if (v != null) flat.push(v); }); });
    var lo = o.min != null ? o.min : Math.min.apply(null, flat), hi = o.max != null ? o.max : Math.max.apply(null, flat);
    var step = function (v) { return Math.max(1, Math.min(steps, 1 + Math.floor(((v - lo) / ((hi - lo) || 1)) * steps - 1e-9))); };
    setTable(el, o.label || 'Daten', [o.cornerTitle || ''].concat(o.cols), o.rows.map(function (r, i) { return [r].concat(o.values[i].map(function (v) { return v == null ? '–' : vf(v); })); }));
    mount(el, function (W) {
      var labW = Math.min(W * 0.3, Math.max.apply(null, o.rows.map(charW)) + 14);
      var cellH = o.cellHeight || 30, m = { l: labW, r: 4, t: 22, b: 52 }, iw = W - m.l - m.r, cw = iw / o.cols.length;
      var H = m.t + m.b + o.rows.length * cellH, svg = reset(el, W, H, o.label), showVals = o.showValues !== false && cw >= 40;
      // Zahl in der Zelle: Textstufe mit dem höheren Kontrast zur Zellfarbe (Themes kehren die Palette um)
      var cs = getComputedStyle(el), inkA = rgbOf(cs.getPropertyValue('--odsv-color-text-primary')), inkB = rgbOf(cs.getPropertyValue('--odsv-color-text-inverse'));
      var every = Math.max(1, Math.ceil(44 / cw));
      o.cols.forEach(function (c, j) { if (j % every === 0) txt(svg, { x: m.l + cw * j + cw / 2, y: 14, 'text-anchor': 'middle', 'class': 'odsv-axis-text' }, c); });
      var cells = [];
      o.rows.forEach(function (r, i) {
        txt(svg, { x: m.l - 10, y: m.t + i * cellH + cellH / 2 + 4, 'text-anchor': 'end', 'class': 'odsv-axis-text odsv-axis-text--cat' }, r);
        o.cols.forEach(function (c, j) {
          var v = o.values[i][j], cx = m.l + cw * j, cy = m.t + i * cellH;
          if (v == null) { h('rect', { x: cx + 1, y: cy + 1, width: cw - 2, height: cellH - 2, rx: 3, 'class': 'odsv-data-cell odsv-data-cell--empty' }, svg); }
          else {
            var gg = h('g', { 'class': 'odsv-dv-seq-' + step(v) }, svg);
            title(h('rect', { x: cx + 1, y: cy + 1, width: cw - 2, height: cellH - 2, rx: 3, 'class': 'odsv-data-cell' }, gg), r + ' · ' + c + ': ' + vf(v));
            if (showVals) {
              var cc = rgbOf(getComputedStyle(gg).color), inv = contrast(inkB, cc) > contrast(inkA, cc);
              txt(svg, { x: cx + cw / 2, y: cy + cellH / 2 + 4, 'text-anchor': 'middle', 'class': 'odsv-data-cell-text' + (inv ? ' odsv-data-cell-text--inverse' : '') }, vf(v));
            }
          }
          cells.push({ i: i, j: j, v: v, x: cx + cw / 2, y: cy });
        });
      });
      // Skala: 6 Stufen mit Grenzen
      var sw = Math.min(48, (iw - 8) / steps), sy = H - 34;
      txt(svg, { x: m.l, y: sy - 6, 'class': 'odsv-axis-title' }, o.scaleTitle || 'Wenig → viel');
      for (var k = 1; k <= steps; k++) h('rect', { x: m.l + (k - 1) * sw, y: sy, width: sw - 2, height: 10, rx: 2, 'class': 'odsv-data-cell', fill: 'currentColor' }, h('g', { 'class': 'odsv-dv-seq-' + k }, svg));
      txt(svg, { x: m.l, y: sy + 24, 'class': 'odsv-axis-text' }, vf(lo));
      txt(svg, { x: m.l + steps * sw - 2, y: sy + 24, 'text-anchor': 'end', 'class': 'odsv-axis-text' }, vf(hi));
      var ring = h('rect', { width: cw - 2, height: cellH - 2, rx: 4, 'class': 'odsv-data-focus', style: 'display:none' }, svg);
      function show(n, say) {
        var c = cells[n]; ring.setAttribute('x', c.x - cw / 2 + 1); ring.setAttribute('y', c.y + 1); ring.style.display = '';
        placeTip(el, tip, c.x, c.y, '<b>' + esc(o.rows[c.i] + ' · ' + o.cols[c.j]) + '</b>' + esc(c.v == null ? 'kein Wert' : vf(c.v)));
        if (say) announce(el, o.rows[c.i] + ', ' + o.cols[c.j] + ': ' + (c.v == null ? 'kein Wert' : vf(c.v)));
      }
      function clear() { ring.style.display = 'none'; hideTip(el); }
      var hit = h('rect', { x: m.l, y: m.t, width: iw, height: o.rows.length * cellH, fill: 'none', 'pointer-events': 'all' }, svg);
      hit.addEventListener('pointermove', function (ev) {
        var r = svg.getBoundingClientRect(), j = Math.floor((ev.clientX - r.left - m.l) / cw), i = Math.floor((ev.clientY - r.top - m.t) / cellH);
        if (i < 0 || j < 0 || i >= o.rows.length || j >= o.cols.length) clear(); else show(i * o.cols.length + j, false);
      });
      hit.addEventListener('pointerleave', clear);
      keys(el, svg, cells.length, show, clear);
    });
  }

  /* ---------- Steigungsdiagramm ---------- */
  function slope(el, o) {
    var H = o.height || Math.max(200, o.items.length * 22 + 60), vf = o.format || fmtDe, tip = tipFor(el);
    setTable(el, o.label || 'Daten', ['', o.from, o.to, 'Veränderung'], o.items.map(function (it) { return [it.label, vf(it.a), vf(it.b), signed(vf)(it.b - it.a)]; }));
    mount(el, function (W) {
      var svg = reset(el, W, H, o.label), vis = o.items.filter(function (it) { return visible(el, { name: it.label }); });
      var labW = Math.min(W * 0.3, Math.max.apply(null, o.items.map(function (it) { return charW(it.label + ' ' + vf(it.a)); })) + 12);
      var m = { l: labW, r: Math.min(W * 0.3, Math.max.apply(null, o.items.map(function (it) { return charW(vf(it.b) + ' ' + it.label); })) + 12), t: 30, b: 12 };
      var all = []; o.items.forEach(function (it) { all.push(it.a, it.b); });
      var sc = scale(o.min != null ? o.min : Math.min.apply(null, all), o.max != null ? o.max : Math.max.apply(null, all), 4, !!o.zero);
      var y = function (v) { return m.t + (H - m.t - m.b) - ((v - sc.lo) / (sc.hi - sc.lo)) * (H - m.t - m.b); };
      var x0 = m.l, x1 = W - m.r;
      txt(svg, { x: x0, y: 14, 'text-anchor': 'middle', 'class': 'odsv-axis-title' }, o.from);
      txt(svg, { x: x1, y: 14, 'text-anchor': 'middle', 'class': 'odsv-axis-title' }, o.to);
      h('line', { x1: x0, x2: x0, y1: m.t - 6, y2: H - m.b, 'class': 'odsv-grid-line' }, svg);
      h('line', { x1: x1, x2: x1, y1: m.t - 6, y2: H - m.b, 'class': 'odsv-grid-line' }, svg);
      var order = vis.slice().sort(function (a, b) { return (a.cls && a.cls !== 'odsv-dv-context' ? 1 : 0) - (b.cls && b.cls !== 'odsv-dv-context' ? 1 : 0); });
      order.forEach(function (it) {
        var gg = h('g', { 'class': it.cls || 'odsv-dv-context' }, svg);
        title(h('line', { x1: x0, y1: y(it.a), x2: x1, y2: y(it.b), 'class': 'odsv-data-line' }, gg), it.label + ': ' + vf(it.a) + ' → ' + vf(it.b));
        h('circle', { cx: x0, cy: y(it.a), r: 4, 'class': 'odsv-data-point' }, gg);
        h('circle', { cx: x1, cy: y(it.b), r: 4, 'class': 'odsv-data-point' }, gg);
      });
      spread(vis.map(function (it) { return { y: y(it.a) + 4, it: it }; }), 15, m.t, H - m.b + 4).forEach(function (l) { txt(svg, { x: x0 - 10, y: l.y, 'text-anchor': 'end', 'class': 'odsv-data-label' + (l.it.cls && l.it.cls !== 'odsv-dv-context' ? '' : ' odsv-data-label--muted') }, l.it.label + ' ' + vf(l.it.a)); });
      spread(vis.map(function (it) { return { y: y(it.b) + 4, it: it }; }), 15, m.t, H - m.b + 4).forEach(function (l) { txt(svg, { x: x1 + 10, y: l.y, 'class': 'odsv-data-label' + (l.it.cls && l.it.cls !== 'odsv-dv-context' ? '' : ' odsv-data-label--muted') }, vf(l.it.b) + ' ' + l.it.label); });
      function show(k, say) { var it = vis[k]; placeTip(el, tip, (x0 + x1) / 2, (y(it.a) + y(it.b)) / 2, '<b>' + esc(it.label) + '</b>' + esc(o.from + ': ' + vf(it.a)) + '<br>' + esc(o.to + ': ' + vf(it.b)) + '<br>' + esc(signed(vf)(it.b - it.a))); if (say) announce(el, it.label + ': ' + vf(it.a) + ' auf ' + vf(it.b)); }
      keys(el, svg, vis.length, show, function () { hideTip(el); });
    });
  }

  /* ---------- Kleine Vielfache ---------- */
  function multiples(el, o) {
    var fmt = o.yFormat || fmtDe, n = o.labels.length, ph = o.height || 120;
    setTable(el, o.label || 'Daten', [''].concat(o.series.map(function (s) { return s.name; })), o.labels.map(function (l, i) { return [l].concat(o.series.map(function (s) { return fmt(s.values[i]); })); }));
    mount(el, function (W) {
      var old = el.querySelector(':scope > svg, :scope > .odsv-chart__multiples'); if (old) old.remove();
      var hi = 0; o.series.forEach(function (s) { s.values.forEach(function (v) { if (v > hi) hi = v; }); });
      var top = o.yMax || niceMax(hi);
      var cols = o.columns || Math.max(1, Math.min(o.series.length, Math.floor(W / 200)));
      var grid = document.createElement('div'); grid.className = 'odsv-chart__multiples'; grid.setAttribute('role', 'group'); grid.setAttribute('aria-label', o.label || '');
      grid.style.setProperty('--_cols', cols);
      el.insertBefore(grid, el.firstChild);
      var pw = Math.floor((W - (cols - 1) * 16) / cols);
      o.series.forEach(function (s, k) {
        var cell = document.createElement('div'); cell.className = 'odsv-chart__multiple';
        var cap = document.createElement('p'); cap.className = 'odsv-chart__multiple-title';
        var last = s.values[n - 1];
        cap.textContent = s.name + ' · ' + fmt(last); cell.appendChild(cap); grid.appendChild(cell);
        var leftAxis = k % cols === 0, m = { l: leftAxis ? 36 : 6, r: 6, t: 6, b: 20 }, iw = pw - m.l - m.r, ih = ph - m.t - m.b;
        var svg = h('svg', { width: pw, height: ph, viewBox: '0 0 ' + pw + ' ' + ph, role: 'img', 'aria-label': s.name + ': von ' + fmt(s.values[0]) + ' (' + o.labels[0] + ') auf ' + fmt(last) + ' (' + o.labels[n - 1] + ')' }, cell);
        var x = function (i) { return m.l + (i * iw) / Math.max(1, n - 1); }, y = function (v) { return m.t + ih - (v / top) * ih; };
        [0, top / 2, top].forEach(function (v) { h('line', { x1: m.l, x2: pw - m.r, y1: y(v), y2: y(v), 'class': v === 0 ? 'odsv-axis-line' : 'odsv-grid-line' }, svg); if (leftAxis) txt(svg, { x: m.l - 6, y: y(v) + 4, 'text-anchor': 'end', 'class': 'odsv-axis-text' }, fmt(v)); });
        txt(svg, { x: m.l, y: ph - 4, 'class': 'odsv-axis-text' }, o.labels[0]);
        txt(svg, { x: pw - m.r, y: ph - 4, 'text-anchor': 'end', 'class': 'odsv-axis-text' }, o.labels[n - 1]);
        if (o.context !== false) o.series.forEach(function (c) {
          if (c === s) return;
          h('path', { d: c.values.map(function (v, i) { return (i ? 'L' : 'M') + x(i).toFixed(1) + ' ' + y(v).toFixed(1); }).join(''), 'class': 'odsv-data-line odsv-data-line--context' }, h('g', { 'class': 'odsv-dv-context' }, svg));
        });
        var sg = h('g', { 'class': s.cls || o.cls || 'odsv-dv-highlight' }, svg);
        h('path', { d: s.values.map(function (v, i) { return (i ? 'L' : 'M') + x(i).toFixed(1) + ' ' + y(v).toFixed(1); }).join(''), 'class': 'odsv-data-line' }, sg);
        h('circle', { cx: x(n - 1), cy: y(last), r: 3.5, 'class': 'odsv-data-point' }, sg);
      });
    });
  }

  /* ---------- Donut und Sparkline ---------- */
  function donut(el, o) {
    var size = o.size || 200, total = o.items.reduce(function (a, b) { return a + b.value; }, 0);
    setTable(el, o.label || 'Anteile', ['', 'Wert', 'Anteil'], o.items.map(function (it) { return [it.label, fmtDe(it.value), fmtDe(total ? it.value / total * 100 : 0) + ' %']; }));
    mount(el, function (W) {
      var S = Math.min(size, W), svg = reset(el, S, S, o.label);
      svg.style.margin = '0 auto'; svg.style.width = S + 'px';
      var c = S / 2, ro = c - 2, ri = ro * 0.64, a0 = -Math.PI / 2, gap = o.items.length > 1 ? 0.025 : 0;
      o.items.forEach(function (it) {
        var ang = (it.value / total) * Math.PI * 2, s = a0 + gap / 2, a1 = a0 + ang - gap / 2;
        var P = function (r, a) { return (c + r * Math.cos(a)).toFixed(2) + ' ' + (c + r * Math.sin(a)).toFixed(2); };
        var big = ang - gap > Math.PI ? 1 : 0;
        var gg = h('g', { 'class': it.cls }, svg);
        title(h('path', { d: 'M' + P(ro, s) + 'A' + ro + ' ' + ro + ' 0 ' + big + ' 1 ' + P(ro, a1) + 'L' + P(ri, a1) + 'A' + ri + ' ' + ri + ' 0 ' + big + ' 0 ' + P(ri, s) + 'Z', 'class': 'odsv-data-slice' }, gg), it.label + ': ' + fmtDe(it.value));
        a0 += ang;
      });
      if (o.center) {
        txt(svg, { x: c, y: c + 4, 'text-anchor': 'middle', 'class': 'odsv-data-center' }, o.center.value);
        txt(svg, { x: c, y: c + 24, 'text-anchor': 'middle', 'class': 'odsv-axis-title' }, o.center.label);
      }
    });
  }

  function spark(el, values, cls) {
    mount(el, function (W) {
      var H = el.clientHeight || 32, svg = reset(el, W, H, ''); svg.setAttribute('aria-hidden', 'true'); svg.removeAttribute('role');
      var min = Math.min.apply(null, values), max = Math.max.apply(null, values), rng = max - min || 1, n = values.length;
      var px = function (i) { return (i * (W - 6)) / (n - 1) + 3; }, py = function (v) { return H - 4 - ((v - min) / rng) * (H - 8); };
      var d = values.map(function (v, i) { return (i ? 'L' : 'M') + px(i).toFixed(1) + ' ' + py(v).toFixed(1); }).join('');
      var g = h('g', { 'class': cls || 'odsv-dv-1' }, svg);
      h('path', { d: d, 'class': 'odsv-data-line' }, g);
      h('circle', { cx: px(n - 1), cy: py(values[n - 1]), r: 3, 'class': 'odsv-data-point' }, g);
    });
  }

  function redrawAll() { document.querySelectorAll('.odsv-chart__plot,[data-odsv-spark]').forEach(function (e) { if (e._odsvDraw) e._odsvDraw(); }); }
  document.addEventListener('odsv:theme', redrawAll); // Heatmap wählt die Textfarbe je Theme neu
  window.ODSVCharts = {
    line: line, bars: bars, columns: columns, hbars: hbars, diverging: diverging, funnel: funnel,
    histogram: histogram, boxplot: boxplot, scatter: scatter, heatmap: heatmap, slope: slope, multiples: multiples,
    donut: donut, spark: spark, redraw: redrawAll, format: fmtDe, stats: stats
  };
})();
