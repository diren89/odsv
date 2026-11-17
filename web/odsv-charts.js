/* ODSV v1.0 – Diagramm-Helfer (optional, ohne Bibliothek). Zeichnet reines SVG in einen Container
   und gestaltet ausschließlich über odsv.css-Klassen (Token-Farben, Achsen-Typo).
   API:  ODSVCharts.line(el, {labels, series:[{name, values, cls:'odsv-dv-1', area:true}], height, yFormat, yTicks, label})
         ODSVCharts.bars(el, {labels, values, colors:['odsv-dv-1',…] | cls, height, yFormat, label})
         ODSVCharts.donut(el, {items:[{label, value, cls}], size, center:{value,label}, label})
         ODSVCharts.spark(el, values, cls)
   Die Zeichnung passt sich der Containerbreite an (ResizeObserver); Schrift bleibt dadurch in px lesbar. */
(function () {
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';
  function h(tag, attrs, parent) {
    var n = document.createElementNS(NS, tag);
    for (var k in attrs) if (Object.prototype.hasOwnProperty.call(attrs, k)) n.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(n);
    return n;
  }
  function niceMax(max) {
    if (max <= 0) return 1;
    var p = Math.pow(10, Math.floor(Math.log(max) / Math.LN10)), f = max / p, n;
    // feinere Stufen, die sich in 4 Teilstriche teilen lassen (277 → 300 statt 500)
    var steps = [1, 1.2, 1.6, 2, 2.4, 3, 4, 5, 6, 8, 10];
    for (var i = 0; i < steps.length; i++) if (f <= steps[i] + 1e-9) { n = steps[i]; break; }
    return n * p;
  }
  function fmtDe(v) { return Number(v).toLocaleString('de-DE', { maximumFractionDigits: 1 }); }
  function mount(el, draw) {
    el._odsvFn = draw; el._odsvLast = 0;
    function run() {
      var w = Math.floor(el.clientWidth);
      if (!w || w === el._odsvLast) return;
      el._odsvLast = w; el._odsvFn(w);
    }
    el._odsvDraw = function () { el._odsvLast = 0; run(); };
    run();
    if (!el._odsvRO) {
      if (window.ResizeObserver) { el._odsvRO = new ResizeObserver(run); el._odsvRO.observe(el); }
      else { el._odsvRO = true; window.addEventListener('resize', run); }
    }
  }
  function reset(el, w, hgt, label) {
    var old = el.querySelector('svg'); if (old) old.remove();
    var svg = h('svg', { width: w, height: hgt, viewBox: '0 0 ' + w + ' ' + hgt, role: 'img', 'aria-label': label || '' });
    el.insertBefore(svg, el.firstChild);
    return svg;
  }
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

  function line(el, o) {
    var H = o.height || 240, fmt = o.yFormat || fmtDe, tip = tipFor(el);
    mount(el, function (W) {
      var svg = reset(el, W, H, o.label);
      var m = { l: 40, r: 12, t: 12, b: 28 }, iw = W - m.l - m.r, ih = H - m.t - m.b;
      var max = 0; o.series.forEach(function (s) { s.values.forEach(function (v) { if (v > max) max = v; }); });
      var top = o.yMax || niceMax(max), ticks = o.yTicks || 4, n = o.labels.length;
      var x = function (i) { return m.l + (n < 2 ? iw / 2 : (i * iw) / (n - 1)); };
      var y = function (v) { return m.t + ih - (v / top) * ih; };
      var g = h('g', {}, svg);
      for (var t = 0; t <= ticks; t++) {
        var v = (top / ticks) * t, yy = y(v);
        h('line', { x1: m.l, x2: W - m.r, y1: yy, y2: yy, 'class': t === 0 ? 'odsv-axis-line' : 'odsv-grid-line' }, g);
        var tx = h('text', { x: m.l - 8, y: yy + 4, 'text-anchor': 'end', 'class': 'odsv-axis-text' }, g); tx.textContent = fmt(v);
      }
      var gap = Math.max(1, Math.ceil(64 / (n < 2 ? 64 : iw / (n - 1))));
      for (var li = n - 1; li >= 0; li -= gap) {
        var a = li === 0 ? 'start' : li === n - 1 ? 'end' : 'middle';
        var tx2 = h('text', { x: x(li), y: H - 8, 'text-anchor': a, 'class': 'odsv-axis-text' }, g); tx2.textContent = o.labels[li];
      }
      o.series.forEach(function (s) {
        var sg = h('g', { 'class': s.cls || 'odsv-dv-1' }, svg);
        var d = s.values.map(function (v, i) { return (i ? 'L' : 'M') + x(i).toFixed(1) + ' ' + y(v).toFixed(1); }).join('');
        if (s.area) h('path', { d: d + 'L' + x(n - 1).toFixed(1) + ' ' + y(0) + 'L' + x(0).toFixed(1) + ' ' + y(0) + 'Z', 'class': 'odsv-data-area' }, sg);
        h('path', { d: d, 'class': 'odsv-data-line' + (s.dash ? ' odsv-data-dash' : '') }, sg);
        var li = s.values.length - 1;
        h('circle', { cx: x(li), cy: y(s.values[li]), r: 4, 'class': 'odsv-data-point' }, sg);
      });
      var cur = h('line', { y1: m.t, y2: m.t + ih, 'class': 'odsv-cursor-line', style: 'display:none' }, svg);
      var pts = o.series.map(function (s) { var c = h('g', { 'class': s.cls || 'odsv-dv-1', style: 'display:none' }, svg); h('circle', { r: 5, 'class': 'odsv-data-point' }, c); return c; });
      var hit = h('rect', { x: m.l, y: m.t, width: iw, height: ih, fill: 'none', 'pointer-events': 'all' }, svg);
      function move(ev) {
        var r = svg.getBoundingClientRect(), px = ev.clientX - r.left;
        var i = Math.max(0, Math.min(n - 1, Math.round(((px - m.l) / iw) * (n - 1))));
        cur.setAttribute('x1', x(i)); cur.setAttribute('x2', x(i)); cur.style.display = '';
        var html = '<b>' + o.labels[i] + '</b>';
        o.series.forEach(function (s, k) {
          pts[k].style.display = ''; pts[k].firstChild.setAttribute('cx', x(i)); pts[k].firstChild.setAttribute('cy', y(s.values[i]));
          html += '<span class="' + (s.cls || 'odsv-dv-1') + '"><span class="odsv-swatch"></span></span> ' + (s.name ? s.name + ': ' : '') + fmt(s.values[i]) + '<br>';
        });
        placeTip(el, tip, x(i), m.t + 24, html);
      }
      function leave() { cur.style.display = 'none'; pts.forEach(function (p) { p.style.display = 'none'; }); tip.classList.remove('is-visible'); }
      hit.addEventListener('pointermove', move); hit.addEventListener('pointerleave', leave);
    });
  }

  function bars(el, o) {
    var H = o.height || 240, fmt = o.yFormat || fmtDe, n = o.labels.length;
    mount(el, function (W) {
      var svg = reset(el, W, H, o.label);
      var m = { l: 40, r: 8, t: 20, b: 28 }, iw = W - m.l - m.r, ih = H - m.t - m.b;
      var max = Math.max.apply(null, o.values), top = o.yMax || niceMax(max), ticks = o.yTicks || 4;
      var y = function (v) { return m.t + ih - (v / top) * ih; };
      for (var t = 0; t <= ticks; t++) {
        var v = (top / ticks) * t, yy = y(v);
        h('line', { x1: m.l, x2: W - m.r, y1: yy, y2: yy, 'class': t === 0 ? 'odsv-axis-line' : 'odsv-grid-line' }, svg);
        var tx = h('text', { x: m.l - 8, y: yy + 4, 'text-anchor': 'end', 'class': 'odsv-axis-text' }, svg); tx.textContent = fmt(v);
      }
      var slot = iw / n, bw = Math.min(40, slot * 0.62);
      var showVals = bw >= 22;
      o.values.forEach(function (val, i) {
        var cls = (o.colors && o.colors[i]) || o.cls || 'odsv-dv-1';
        var cx = m.l + slot * i + slot / 2, bh = Math.max(0, ih - (y(val) - m.t));
        var gg = h('g', { 'class': cls }, svg);
        h('path', { d: 'M' + (cx - bw / 2) + ' ' + (m.t + ih) + 'V' + (y(val) + 4) + 'Q' + (cx - bw / 2) + ' ' + y(val) + ' ' + (cx - bw / 2 + 4) + ' ' + y(val) + 'H' + (cx + bw / 2 - 4) + 'Q' + (cx + bw / 2) + ' ' + y(val) + ' ' + (cx + bw / 2) + ' ' + (y(val) + 4) + 'V' + (m.t + ih) + 'Z', 'class': 'odsv-data-bar' }, gg)
          .appendChild(document.createElementNS(NS, 'title')).textContent = o.labels[i] + ': ' + fmt(val);
        if (showVals && bh > 0) { var vt = h('text', { x: cx, y: y(val) - 6, 'text-anchor': 'middle', 'class': 'odsv-data-label' }, svg); vt.textContent = fmt(val); }
        var lx = h('text', { x: cx, y: H - 8, 'text-anchor': 'middle', 'class': 'odsv-axis-text' }, svg); lx.textContent = o.labels[i];
      });
    });
  }

  function donut(el, o) {
    var size = o.size || 200, total = o.items.reduce(function (a, b) { return a + b.value; }, 0);
    mount(el, function (W) {
      var S = Math.min(size, W), svg = reset(el, S, S, o.label);
      svg.style.margin = '0 auto'; svg.style.width = S + 'px';
      var c = S / 2, ro = c - 2, ri = ro * 0.64, a0 = -Math.PI / 2, gap = o.items.length > 1 ? 0.025 : 0;
      o.items.forEach(function (it) {
        var ang = (it.value / total) * Math.PI * 2, a1 = a0 + ang - gap, s = a0 + gap / 2;
        a1 = a0 + ang - gap / 2;
        var P = function (r, a) { return (c + r * Math.cos(a)).toFixed(2) + ' ' + (c + r * Math.sin(a)).toFixed(2); };
        var big = ang - gap > Math.PI ? 1 : 0;
        var gg = h('g', { 'class': it.cls }, svg);
        h('path', { d: 'M' + P(ro, s) + 'A' + ro + ' ' + ro + ' 0 ' + big + ' 1 ' + P(ro, a1) + 'L' + P(ri, a1) + 'A' + ri + ' ' + ri + ' 0 ' + big + ' 0 ' + P(ri, s) + 'Z', 'class': 'odsv-data-slice' }, gg)
          .appendChild(document.createElementNS(NS, 'title')).textContent = it.label + ': ' + fmtDe(it.value);
        a0 += ang;
      });
      if (o.center) {
        var t1 = h('text', { x: c, y: c + 4, 'text-anchor': 'middle', 'class': 'odsv-data-label', style: 'font-size:var(--odsv-font-size-28);fill:var(--odsv-color-text-primary);font-weight:var(--odsv-font-weight-semibold)' }, svg); t1.textContent = o.center.value;
        var t2 = h('text', { x: c, y: c + 24, 'text-anchor': 'middle', 'class': 'odsv-axis-title' }, svg); t2.textContent = o.center.label;
      }
    });
  }

  function spark(el, values, cls) {
    mount(el, function (W) {
      var H = el.clientHeight || 32, svg = reset(el, W, H, ''); svg.setAttribute('aria-hidden', 'true'); svg.removeAttribute('role');
      var min = Math.min.apply(null, values), max = Math.max.apply(null, values), rng = max - min || 1, n = values.length;
      var d = values.map(function (v, i) { return (i ? 'L' : 'M') + ((i * (W - 6)) / (n - 1) + 3).toFixed(1) + ' ' + (H - 4 - ((v - min) / rng) * (H - 8)).toFixed(1); }).join('');
      var g = h('g', { 'class': cls || 'odsv-dv-1' }, svg);
      h('path', { d: d, 'class': 'odsv-data-line' }, g);
    });
  }

  function redrawAll() { document.querySelectorAll('.odsv-chart__plot,[data-odsv-spark]').forEach(function (e) { if (e._odsvDraw) e._odsvDraw(); }); }
  window.ODSVCharts = { line: line, bars: bars, donut: donut, spark: spark, redraw: redrawAll, format: fmtDe };
})();
