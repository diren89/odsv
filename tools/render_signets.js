// Rendert die Signetfamilie für andere Medien:
//   web/signets/<id>.svg                 eigenständige SVG mit festen Hex-Farben (Figma, Office, Druck)
//   pptx/signets/<name>-card.png         Signet-Karte der Titelfolie (4,883 × 6,167 in, 300 dpi, runde Ecken, Rand)
//   pptx/signets/<name>-mark.png         Signet-Marke des Kapiteltrenners (1,05 × 1,561 in, transparent)
// Aufruf: node tools/render_signets.js   (nach python3 tools/build_signets.py)
// Element- statt Seiten-Screenshot: headless Chrome auf macOS zeichnet hohe Viewports sonst mit Bruch im unteren Bereich.
const { chromium } = (() => { try { return require('playwright'); } catch (e) { return require('/opt/npm-tools/node_modules/playwright'); } })();
const CHROME = process.env.CHROME_PATH || (require('fs').existsSync('/usr/bin/google-chrome') ? '/usr/bin/google-chrome' : undefined);
const fs = require('fs'), path = require('path');
const root = path.join(__dirname, '..');
const sprite = fs.readFileSync(path.join(root, 'web', 'icons.svg'), 'utf8');
const tokCss = fs.readFileSync(path.join(root, 'web', 'tokens.css'), 'utf8');
const meta = JSON.parse(fs.readFileSync(path.join(root, 'catalog', 'signets.json'), 'utf8')).signets;
const hex = n => (tokCss.match(new RegExp(`--odsv-color-${n}:\\s*(#[0-9A-Fa-f]{3,8})`)) || [])[1];
const C = { 'signet-1': hex('signet-1'), 'signet-2': hex('signet-2'), 'signet-3': hex('signet-3'), 'signet-4': hex('signet-4'), 'signet-dot': hex('signet-dot'), 'bg-subtle': hex('bg-subtle'), 'border-subtle': hex('border-subtle') };
for (const [k, v] of Object.entries(C)) if (!v) { console.error('Farbe fehlt in tokens.css:', k); process.exit(1); }
const outSvg = path.join(root, 'web', 'signets'), outPng = path.join(root, 'pptx', 'signets');
fs.mkdirSync(outSvg, { recursive: true }); fs.mkdirSync(outPng, { recursive: true });
const symbolOf = id => { const m = sprite.match(new RegExp(`<symbol id="${id}"[^>]*>([\\s\\S]*?)</symbol>`)); return m[1]; };
const resolve = s => s.replace(/var\(--odsv-color-(signet-[1-4]|signet-dot)\)/g, (_, n) => C[n]);
const short = id => id === 'odsv-signet' ? 'basis' : id.replace('odsv-signet-', '');

(async () => {
  const b = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox'] });
  const page = await b.newPage({ deviceScaleFactor: 1 });
  for (const m of meta) {
    const inner = resolve(symbolOf(m.id));
    fs.writeFileSync(path.join(outSvg, m.id + '.svg'), `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" role="img" aria-label="ODSV-Signet ${m.name}"><title>ODSV-Signet ${m.name}</title>${inner}</svg>\n`);
    // Karte 1464 × 1850 px (= 4,883 × 6,167 in bei 300 dpi), Radius 0,28 in = 84 px, Rand 0,75 pt = 3 px
    const W = 1464, H = 1850;
    await page.setViewportSize({ width: W, height: H });
    await page.setContent(`<html><body style="margin:0;background:transparent">
      <div style="width:${W}px;height:${H}px;box-sizing:border-box;border-radius:84px;overflow:hidden;background:${C['bg-subtle']};border:3px solid ${C['border-subtle']}">
      <svg viewBox="0 0 400 400" preserveAspectRatio="xMaxYMid slice" style="width:100%;height:100%;display:block">${inner}</svg></div></body></html>`);
    await page.locator('body > div').screenshot({ path: path.join(outPng, short(m.id) + '-card.png'), omitBackground: true });
    // Marke 900 × 1338 px, transparent
    await page.setViewportSize({ width: 900, height: 1338 });
    await page.setContent(`<html><body style="margin:0;background:transparent"><svg viewBox="100 0 340 400" preserveAspectRatio="xMaxYMid meet" style="width:900px;height:1338px;display:block">${inner}</svg></body></html>`);
    await page.locator('body > svg').screenshot({ path: path.join(outPng, short(m.id) + '-mark.png'), omitBackground: true });
  }
  await b.close();
  console.log(meta.length + ' Signets gerendert → web/signets/*.svg, pptx/signets/*-card.png, *-mark.png');
})();
