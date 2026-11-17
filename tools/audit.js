// Design-Audit: node tools/audit.js [seiten] → web/_audit/report.json + Sektions-Screenshots
// Prüft: Konsole, Überlauf, Kontrast (Text vs. effektiver Hintergrund), Trefferflächen,
// Werte außerhalb der Tokens (Farbe, Schriftgröße, Radius, Schrift), Überschriften-Hierarchie,
// Fokus-Sichtbarkeit, Bedienelemente ohne Namen, überlappende Texte.
const { chromium } = (() => { try { return require('playwright'); } catch (e) { return require('/opt/npm-tools/node_modules/playwright'); } })();
const CHROME = process.env.CHROME_PATH || (require('fs').existsSync('/usr/bin/google-chrome') ? '/usr/bin/google-chrome' : undefined);
const path = require('path'), fs = require('fs');
const root = path.join(__dirname, '..', 'web');
const out = path.join(root, '_audit'); fs.mkdirSync(out, { recursive: true });
const pages = process.argv[2] ? process.argv[2].split(',') : ['index.html', 'examples/website.html', 'examples/dashboard.html'];
const VARS = [...new Set((fs.readFileSync(path.join(root, 'tokens.css'), 'utf8').match(/--odsv-[a-z0-9-]+(?=\s*:)/g) || []))];
const VPS = [{ n: 'm', w: 390, h: 844 }, { n: 'd', w: 1440, h: 900 }];

function pageAudit([isMobile, VARS]) {
  const res = { contrast: [], targets: [], offColors: {}, offSizes: {}, offRadii: {}, fonts: {}, headings: [], unnamed: [], overlap: [], focus: [] };
  const root = getComputedStyle(document.documentElement);
  // Token-Werte einsammeln
  const tokColors = new Set(), tokSizes = new Set(), tokRadii = new Set();
  const probe = document.createElement('div'); document.body.appendChild(probe);
  for (const p of VARS) {
    probe.removeAttribute('style');
    probe.style.setProperty('color', 'var(' + p + ')'); probe.style.setProperty('font-size', 'var(' + p + ')'); probe.style.setProperty('border-top-left-radius', 'var(' + p + ')');
    const cs = getComputedStyle(probe);
    if (/color|surface|bg|border|text|accent|status|dataviz|signet|lineart|focus|progress|action/.test(p)) tokColors.add(cs.color);
    if (/font-size|-size-|text-.*-size/.test(p)) tokSizes.add(cs.fontSize);
    if (p.includes('radius')) tokRadii.add(cs.borderTopLeftRadius);
  }
  probe.remove();
  const parse = c => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const a = m[1].split(/[ ,\/]+/).filter(Boolean).map(Number); return { r: a[0], g: a[1], b: a[2], a: a.length > 3 ? a[3] : 1 }; };
  const lum = c => { const f = v => { v /= 255; return v <= .03928 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4); }; return .2126 * f(c.r) + .7152 * f(c.g) + .0722 * f(c.b); };
  const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + .05) / (Math.min(x, y) + .05); };
  const blend = (top, bot) => ({ r: top.r * top.a + bot.r * (1 - top.a), g: top.g * top.a + bot.g * (1 - top.a), b: top.b * top.a + bot.b * (1 - top.a), a: 1 });
  function bgOf(el) {
    const layers = []; let e = el, img = false;
    while (e && e.nodeType === 1) {
      const cs = getComputedStyle(e);
      if (cs.backgroundImage && cs.backgroundImage !== 'none' && !cs.backgroundImage.startsWith('url')) img = true;
      const c = parse(cs.backgroundColor); if (c && c.a > 0) { layers.push(c); if (c.a >= 1) break; }
      if (parseFloat(cs.opacity) < 1) {}
      e = e.parentElement;
    }
    let base = { r: 0, g: 0, b: 0, a: 1 };
    if (!layers.length || layers[layers.length - 1].a < 1) { const bc = parse(getComputedStyle(document.body).backgroundColor); if (bc && bc.a) base = bc; }
    for (let i = layers.length - 1; i >= 0; i--) base = blend(layers[i], base);
    return { c: base, img };
  }
  const visible = e => { const r = e.getBoundingClientRect(); const cs = getComputedStyle(e); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none' && !e.closest('[hidden],.odsv-sr-only,.odsv-sprite,template') && !e.closest('details:not([open]) > :not(summary)'); };
  const label = e => (e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') + '.' + String(e.className && e.className.baseVal !== undefined ? e.className.baseVal : e.className).split(' ').slice(0, 2).join('.')).slice(0, 60) + ' „' + (e.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 28) + '“';
  const sect = e => { const s = e.closest('section[id],[id]'); return s ? s.id : ''; };
  // Text-Elemente
  const all = [...document.querySelectorAll('body *')].filter(e => !e.closest('svg,.odsv-sprite,script,style,template,.docs-snippet,[hidden]'));
  for (const e of all) {
    const hasText = [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 1);
    if (!hasText || !visible(e)) continue;
    const cs = getComputedStyle(e);
    let op = 1, x = e; while (x && x.nodeType === 1) { op *= parseFloat(getComputedStyle(x).opacity); x = x.parentElement; }
    const fg = parse(cs.color); if (!fg) continue;
    const { c: bg, img } = bgOf(e);
    const fgc = blend({ ...fg, a: fg.a * op }, bg);
    const r = ratio(fgc, bg), fs = parseFloat(cs.fontSize), bold = parseInt(cs.fontWeight) >= 700;
    const large = fs >= 24 || (fs >= 18.66 && bold);
    const disabled = e.closest(':disabled,[aria-disabled="true"],.is-disabled') || /disabled/.test(e.className);
    const need = large ? 3 : 4.5;
    if (r < need && !disabled && !img) res.contrast.push({ sel: label(e), sect: sect(e), ratio: +r.toFixed(2), need, fs });
    const docsOnly = e.closest('code,.docs-sw,.docs-type__meta,.docs-note,.docs-radius,.docs-box,.docs-elev,.docs-icons,.docs-pal,.docs-swatches');
    if (!docsOnly && !tokColors.has(cs.color) && fg.a === 1) res.offColors[cs.color] = (res.offColors[cs.color] || []).concat(label(e)).slice(0, 3);
    if (!docsOnly && !tokSizes.has(cs.fontSize)) res.offSizes[cs.fontSize] = (res.offSizes[cs.fontSize] || []).concat(label(e)).slice(0, 3);
    const fam = cs.fontFamily.split(',')[0].replace(/"/g, '').trim(); res.fonts[fam] = (res.fonts[fam] || 0) + 1;
  }
  for (const e of all) {
    if (!visible(e)) continue; const cs = getComputedStyle(e); const rad = cs.borderTopLeftRadius;
    if (!e.closest('code,[class*=docs-]') && rad !== '0px' && !rad.includes('%') && !tokRadii.has(rad) && parseFloat(rad) < 900) res.offRadii[rad] = (res.offRadii[rad] || []).concat(label(e)).slice(0, 3);
  }
  // Trefferflächen + Namen
  const inter = [...document.querySelectorAll('a[href],button,input:not([type=hidden]),select,textarea,summary,[role=button],[role=tab],[role=switch]')].filter(e => visible(e) && !e.closest('.docs-snippet'));
  for (const e of inter) {
    const r = e.getBoundingClientRect();
    const inline = e.tagName === 'A' && getComputedStyle(e).display === 'inline' && e.closest('p,li,td,dd');
    let rr = r; if (/INPUT/.test(e.tagName) && e.closest('label')) rr = e.closest('label').getBoundingClientRect();
    const min = isMobile ? 44 : 24;
    if (!inline && (rr.height < min - 0.5 || rr.width < min - 0.5) && !e.closest('.odsv-table--dense,[data-density="dense"]')) res.targets.push({ sel: label(e), sect: sect(e), w: Math.round(rr.width), h: Math.round(rr.height) });
    const name = (e.getAttribute('aria-label') || e.textContent || e.getAttribute('title') || (e.labels && e.labels[0] && e.labels[0].textContent) || e.getAttribute('placeholder') || '').trim();
    const lb = e.getAttribute('aria-labelledby');
    if (!name && !lb && !e.closest('label')) res.unnamed.push(label(e) + ' @' + sect(e));
  }
  // Überschriften
  let last = 0; document.querySelectorAll('h1,h2,h3,h4,h5,h6').forEach(h => { if (h.closest('template,[hidden]')) return; const l = +h.tagName[1]; if (last && l > last + 1) res.headings.push(h.tagName + ' nach H' + last + ': ' + h.textContent.trim().slice(0, 40)); last = l; });
  // Überlappende Texte (Geschwister-Blöcke)
  const blocks = all.filter(e => visible(e) && /^(H[1-6]|P|LI|DT|DD|LABEL|BUTTON|A|SUMMARY|FIGCAPTION|TH|TD|SPAN)$/.test(e.tagName) && [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) && getComputedStyle(e).position === 'static');
  const rects = blocks.map(e => ({ e, r: e.getBoundingClientRect() }));
  for (let i = 0; i < rects.length; i++) for (let j = i + 1; j < Math.min(rects.length, i + 40); j++) {
    const a = rects[i], b = rects[j]; if (a.e.contains(b.e) || b.e.contains(a.e)) continue;
    const ox = Math.min(a.r.right, b.r.right) - Math.max(a.r.left, b.r.left), oy = Math.min(a.r.bottom, b.r.bottom) - Math.max(a.r.top, b.r.top);
    if (ox > 4 && oy > 4) res.overlap.push(label(a.e) + ' ✕ ' + label(b.e));
  }
  res.overlap = res.overlap.slice(0, 15);
  return res;
}

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox'] });
  const report = {};
  for (const pg of pages) for (const vp of VPS) for (const theme of ['dark', 'light']) {
    const ctx = await browser.newContext({ viewport: { width: vp.w, height: vp.h }, deviceScaleFactor: 1, hasTouch: vp.n === 'm', isMobile: vp.n === 'm' });
    const page = await ctx.newPage(); const errs = [];
    page.on('console', m => { if (['error', 'warning'].includes(m.type())) errs.push(m.text()); });
    page.on('pageerror', e => errs.push('pageerror: ' + e.message));
    await page.addInitScript(t => { try { localStorage.setItem('odsv-theme', t); } catch (e) {} }, theme);
    await page.goto('file://' + (fs.existsSync(pg) ? path.resolve(pg) : path.join(root, pg))); await page.waitForTimeout(800);
    // alles ausklappen? nein – Standardzustand prüfen. Scrollen, damit Lazy-Inhalte laden.
    await page.evaluate(async () => { for (let y = 0; y < document.documentElement.scrollHeight; y += 700) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 30)); } window.scrollTo(0, 0); });
    await page.waitForTimeout(400);
    const r = await page.evaluate(pageAudit, [vp.n === 'm', VARS]);
    r.console = errs; r.overflowX = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    // Fokus: erste 60 Tab-Stopps
    const focus = [];
    for (let i = 0; i < 60; i++) {
      await page.keyboard.press('Tab');
      const f = await page.evaluate(() => { const e = document.activeElement; if (!e || e === document.body) return null; const cs = getComputedStyle(e); const vis = (cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) > 0) || (cs.boxShadow && cs.boxShadow !== 'none'); return vis ? null : e.tagName + '.' + String(e.className).slice(0, 40) + ' „' + (e.textContent || e.getAttribute('aria-label') || '').trim().slice(0, 24) + '“'; });
      if (f) focus.push(f);
    }
    r.focus = [...new Set(focus)];
    const key = pg + ' ' + vp.n + ' ' + theme; report[key] = r;
    // Sektions-Screenshots (nur Referenzseite) bzw. Ganzseite
    const tag = path.basename(pg).replace(/[\/.]/g, '_').replace('_html', '') + '-' + vp.n + '-' + theme;
    if (pg.endsWith('web/index.html') || pg === 'index.html') {
      await page.addStyleTag({ content: '.docs-topbar{position:relative!important}' });
      const ids = await page.$$eval('section.docs-section[id]', s => s.map(x => x.id));
      for (const id of ids) { const el = await page.$('#' + id); await el.scrollIntoViewIfNeeded(); await page.waitForTimeout(120); await el.screenshot({ path: path.join(out, tag + '-' + id + '.png') }).catch(() => {}); }
    } else {
      await page.screenshot({ path: path.join(out, tag + '.png'), fullPage: true });
    }
    const c = r;
    console.log(key.padEnd(34), 'console', c.console.length, '| overflowX', c.overflowX, '| kontrast', c.contrast.length, '| ziele', c.targets.length, '| farbe∉tok', Object.keys(c.offColors).length, '| größe∉tok', Object.keys(c.offSizes).length, '| radius∉tok', Object.keys(c.offRadii).length, '| H', c.headings.length, '| ohne Namen', c.unnamed.length, '| überlapp', c.overlap.length, '| fokus', c.focus.length, '| fonts', JSON.stringify(c.fonts));
    await ctx.close();
  }
  fs.writeFileSync(path.join(out, 'report.json'), JSON.stringify(report, null, 1));
  await browser.close();
})();
