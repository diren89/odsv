// ODSV-Regelprüfung für erzeugtes HTML (für Menschen und AI-Agents).
// Aufruf: node tools/lint-html.js seite.html [weitere.html …] [--json]
// Lädt jede Seite in Chrome (Playwright) und prüft die ODSV-Regeln aus SPEC.md und catalog/components.json.
// Exit-Code 1, wenn mindestens ein Fehler (error) gefunden wurde; Warnungen (warn) brechen nicht ab.
const { chromium } = (() => { try { return require('playwright'); } catch (e) { return require('/opt/npm-tools/node_modules/playwright'); } })();
const CHROME = process.env.CHROME_PATH || (require('fs').existsSync('/usr/bin/google-chrome') ? '/usr/bin/google-chrome' : undefined);
const path = require('path'), fs = require('fs');
const root = path.join(__dirname, '..');
const catalog = JSON.parse(fs.readFileSync(path.join(root, 'catalog', 'classes.json'), 'utf8'));
const args = process.argv.slice(2), asJson = args.includes('--json');
const files = args.filter(a => !a.startsWith('--'));
if (!files.length) { console.error('Aufruf: node tools/lint-html.js datei.html [...] [--json]'); process.exit(2); }

function rules(valid) {
  const out = [], V = new Set(valid);
  const add = (level, rule, el, msg) => out.push({ level, rule, where: el ? where(el) : '', msg });
  function where(e) { const s = e.closest('section[id],[id]'); return (e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') + (e.className && typeof e.className === 'string' ? '.' + e.className.trim().split(/\s+/).slice(0, 2).join('.') : '') + (s && s !== e ? ' in #' + s.id : '') + (txt(e) ? ' „' + txt(e).slice(0, 28) + '“' : '')).slice(0, 120); }
  const vis = e => { const r = e.getBoundingClientRect(), cs = getComputedStyle(e); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; };
  const txt = e => (e.textContent || '').replace(/\s+/g, ' ').trim();
  const all = [...document.querySelectorAll('body *')].filter(e => !e.closest('template,svg,script,style,.docs-snippet'));

  // 1 Einbindung
  const css = [...document.querySelectorAll('link[rel=stylesheet]')].map(l => l.getAttribute('href') || '');
  if (!css.some(h => /tokens\.css$/.test(h))) add('error', 'einbindung', null, 'tokens.css ist nicht eingebunden.');
  if (!css.some(h => /odsv\.css$/.test(h))) add('error', 'einbindung', null, 'odsv.css ist nicht eingebunden.');
  if (!document.documentElement.lang) add('warn', 'einbindung', null, '<html lang="de"> fehlt.');
  // 2 Unbekannte Klassen
  const unknown = {};
  all.forEach(e => (typeof e.className === 'string' ? e.className.split(/\s+/) : []).forEach(c => { if (c.startsWith('odsv-') && !V.has(c)) (unknown[c] = unknown[c] || e); }));
  Object.entries(unknown).forEach(([c, e]) => add('error', 'klasse', e, `Unbekannte Klasse .${c} – nur Klassen aus catalog/classes.json verwenden.`));
  // 3 Farben außerhalb der Tokens
  all.forEach(e => { const st = e.getAttribute('style') || ''; if (/#[0-9a-f]{3,8}\b|rgba?\(|hsla?\(/i.test(st)) add('error', 'token', e, 'Farbwert im style-Attribut – var(--odsv-…) verwenden.'); });
  [...document.querySelectorAll('style')].forEach(s => { if (/(?<!-)(color|background|border)[^;{]*:\s*[^;]*(#[0-9a-f]{3,8}\b|rgba?\()/i.test(s.textContent)) add('warn', 'token', s, 'Hex/rgb-Farbe in <style> – var(--odsv-…) verwenden.'); });
  // 4 Primär-Buttons: höchstens einer je Ansicht (Sektion/Dialog/Seite ohne Sektion)
  const scopes = [...document.querySelectorAll('section, [role=dialog], main')];
  const counted = new Set();
  scopes.forEach(sc => { const p = [...sc.querySelectorAll('.odsv-btn--primary')].filter(b => vis(b) && b.closest('section,[role=dialog],main') === sc && !b.closest('[class*=docs-]'));
    p.forEach(b => counted.add(b)); if (p.length > 1) add('error', 'primaer', sc, `${p.length} Primär-Buttons in einer Ansicht – genau einer erlaubt.`); });
  // 5 Button-Texte
  const vague = /^(ok|okay|weiter|hier|hier klicken|klicken|mehr|absenden|submit|los)$/i;
  document.querySelectorAll('.odsv-btn, button').forEach(b => { if (!vis(b) || b.closest('[class*=docs-]')) return; const t = txt(b), l = b.getAttribute('aria-label');
    if (!t && !l) add('error', 'name', b, 'Button ohne Namen (Text oder aria-label).');
    else if (vague.test(t)) add('warn', 'buttontext', b, `Button „${t}“: Verb + Ziel verwenden (z. B. „Bericht öffnen“).`); });
  document.querySelectorAll('a[href]').forEach(a => { if (vis(a) && !txt(a) && !a.getAttribute('aria-label')) add('error', 'name', a, 'Link ohne Namen.'); });
  // 6 Versalien getippt und Headline-Länge
  document.querySelectorAll('.odsv-display,.odsv-h1,.odsv-h2,.odsv-eyebrow,.odsv-label').forEach(h => { const t = txt(h);
    if (t.length > 3 && /[a-zäöü]/i.test(t) && t === t.toUpperCase() && !/^[A-Z0-9-]{2,6}$/.test(t)) add('warn', 'versalien', h, `„${t.slice(0, 30)}“ ist getippt in Versalien – normal schreiben, CSS setzt Versalien.`);
    if ((h.matches('.odsv-display,.odsv-h1')) && t.length > 24) add('warn', 'headline', h, `Headline hat ${t.length} Zeichen (Ziel ≤ 24, höchstens 3 Wörter).`); });
  // 7 Dreiklang: Headline ohne Zweitsatz
  document.querySelectorAll('.odsv-display,.odsv-h1').forEach(h => { if (h.closest('[class*=docs-type]')) return; const n = h.nextElementSibling; if (!n || !n.matches('.odsv-sub')) add('warn', 'dreiklang', h, 'Headline ohne grauen Zweitsatz (.odsv-sub) direkt danach.'); });
  // 8 Überschriften-Hierarchie
  let last = 0, h1 = 0; document.querySelectorAll('h1,h2,h3,h4,h5,h6').forEach(h => { if (h.closest('template')) return; const l = +h.tagName[1]; if (l === 1) h1++; if (last && l > last + 1) add('warn', 'ueberschriften', h, `${h.tagName} folgt auf H${last} (Ebene übersprungen).`); last = l; });
  if (h1 !== 1) add('warn', 'ueberschriften', null, `${h1} <h1> auf der Seite (genau eine erwartet).`);
  // 9 Bilder, Icons, Diagramme
  document.querySelectorAll('img').forEach(i => { if (!i.hasAttribute('alt')) add('error', 'alt', i, '<img> ohne alt.'); });
  document.querySelectorAll('svg.odsv-icon').forEach(s => { if (!s.closest('[aria-hidden="true"]') && !s.getAttribute('aria-label') && !s.querySelector('title')) add('warn', 'icon', s, 'Icon ohne aria-hidden="true" (dekorativ) oder Namen.'); });
  document.querySelectorAll('.odsv-chart').forEach(c => { if (!c.querySelector('.odsv-chart__title')) add('error', 'diagramm', c, 'Diagramm ohne Titel (.odsv-chart__title, als Aussage).');
    if (!c.querySelector('.odsv-chart__footer') && !c.closest('[class*=docs-]')) add('warn', 'diagramm', c, 'Diagramm ohne Quelle (.odsv-chart__footer „Quelle: … · Stand …“).');
    c.querySelectorAll('.odsv-chart__plot svg').forEach(s => { if (!s.getAttribute('aria-label')) add('error', 'diagramm', s, 'Diagramm-SVG ohne aria-label (Aussage).'); }); });
  // 10 Tabellen, Formulare, Warnungen
  document.querySelectorAll('table.odsv-table').forEach(t => { if (!t.closest('.odsv-table-wrap')) add('error', 'tabelle', t, 'Tabelle nicht in .odsv-table-wrap (seitliches Scrollen).'); if (!t.querySelector('caption')) add('warn', 'tabelle', t, 'Tabelle ohne <caption>.'); });
  document.querySelectorAll('input:not([type=hidden]),select,textarea').forEach(f => { if (f.closest('template')) return; const ok = (f.labels && f.labels.length) || f.getAttribute('aria-label') || f.getAttribute('aria-labelledby'); if (!ok) add('error', 'formular', f, 'Feld ohne Label.'); });
  document.querySelectorAll('details .odsv-callout--warning, details .odsv-callout--danger').forEach(c => add('error', 'warnung', c, 'Warnung im Akkordeon – Warnungen nie einklappen.'));
  // 11 Akzent sparsam: gelbe Kacheln/Zahlen
  const tiles = [...document.querySelectorAll('.odsv-tile--accent')].filter(vis); if (tiles.length > 3) add('warn', 'akzent', null, `${tiles.length} gelbe Icon-Kacheln – Gelb nur für den Hauptmoment.`);
  // 12 Überlauf
  if (document.documentElement.scrollWidth > document.documentElement.clientWidth + 1) add('error', 'ueberlauf', null, 'Seite scrollt seitlich.');
  return out;
}

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox'] });
  const report = {}; let errors = 0;
  for (const f of files) {
    const res = [];
    for (const vp of [{ n: 'mobil', w: 390, h: 844, touch: true }, { n: 'desktop', w: 1440, h: 900 }]) {
      const ctx = await browser.newContext({ viewport: { width: vp.w, height: vp.h }, hasTouch: !!vp.touch, isMobile: !!vp.touch });
      const page = await ctx.newPage(); const cons = [];
      page.on('console', m => { if (m.type() === 'error') cons.push(m.text()); }); page.on('pageerror', e => cons.push(e.message));
      await page.goto('file://' + path.resolve(f)); await page.waitForTimeout(600);
      const r = await page.evaluate(rules, catalog.classes);
      cons.forEach(c => r.push({ level: 'error', rule: 'konsole', where: '', msg: c }));
      r.forEach(x => { x.viewport = vp.n; });
      res.push(...r); await ctx.close();
    }
    const seen = new Set(), uniq = res.filter(x => { const k = x.rule + x.where + x.msg; if (seen.has(k)) return false; seen.add(k); return true; });
    report[f] = uniq; errors += uniq.filter(x => x.level === 'error').length;
  }
  await browser.close();
  if (asJson) console.log(JSON.stringify(report, null, 1));
  else for (const [f, r] of Object.entries(report)) {
    const e = r.filter(x => x.level === 'error').length, w = r.length - e;
    console.log(`\n${f}: ${e} Fehler, ${w} Warnungen`);
    r.forEach(x => console.log(`  ${x.level === 'error' ? '✗' : '!'} [${x.rule}] ${x.msg}${x.where ? '  → ' + x.where : ''}${x.viewport === 'mobil' && x.rule === 'ueberlauf' ? ' (mobil)' : ''}`));
  }
  process.exit(errors ? 1 : 0);
})();
