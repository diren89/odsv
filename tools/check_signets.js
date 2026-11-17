// Prüft jede Signet-Variante gegen die Grammatik (tools/build_signets.py, SPEC 10.4).
// Aufruf: node tools/check_signets.js   → Exit-Code 1 bei Verstoß. Das Basis-Signet ist von der Sichtzone ausgenommen.
const { chromium } = (() => { try { return require('playwright'); } catch (e) { return require('/opt/npm-tools/node_modules/playwright'); } })();
const CHROME = process.env.CHROME_PATH || (require('fs').existsSync('/usr/bin/google-chrome') ? '/usr/bin/google-chrome' : undefined);
const fs = require('fs'), path = require('path');
const root = path.join(__dirname, '..');
const sprite = fs.readFileSync(path.join(root, 'web', 'icons.svg'), 'utf8');
const css = fs.readFileSync(path.join(root, 'web', 'tokens.css'), 'utf8');
(async () => {
  const b = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox'] });
  const p = await b.newPage();
  await p.setContent(`<style>${css}</style>${sprite}`);
  const res = await p.evaluate(() => {
    const out = [];
    const want = ['--odsv-color-signet-1', '--odsv-color-signet-2', '--odsv-color-signet-3', '--odsv-color-signet-4'];
    document.querySelectorAll('symbol[id^="odsv-signet"]').forEach(sym => {
      const id = sym.id, errs = [];
      const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svg.setAttribute('viewBox', '0 0 400 400'); svg.setAttribute('width', 400); svg.setAttribute('height', 400);
      svg.innerHTML = sym.innerHTML; document.body.appendChild(svg);
      const paths = [...svg.querySelectorAll('path')], dots = [...svg.querySelectorAll('circle')];
      if (paths.length !== 4) errs.push(`${paths.length} Striche statt 4`);
      if (dots.length !== 1) errs.push(`${dots.length} Punkte statt 1`);
      paths.forEach((pa, i) => {
        const st = pa.getAttribute('style') || '';
        if (!st.includes(`var(${want[i]})`)) errs.push(`Strich ${i + 1} nicht in ${want[i]}`);
        if (!/stroke-width:26/.test(st) || !/stroke-linecap:round/.test(st)) errs.push(`Strich ${i + 1}: Breite 26 und runde Enden nötig`);
      });
      dots.forEach(d => { const r = +d.getAttribute('r'); if (r < 24 || r > 34) errs.push(`Punkt r=${r} (erlaubt 24–34)`); if (!/signet-dot/.test(d.getAttribute('style') || '')) errs.push('Punkt nicht in signet-dot'); });
      if (id !== 'odsv-signet') {
        // Geometrie mit Strichbreite abtasten
        let minY = 1e9, maxY = -1e9, minX = 1e9, zone = 0;
        paths.forEach(pa => { const L = pa.getTotalLength(); for (let t = 0; t <= L; t += 2) { const q = pa.getPointAtLength(t);
          minY = Math.min(minY, q.y - 13); maxY = Math.max(maxY, q.y + 13); minX = Math.min(minX, q.x - 13);
          if (q.x - 13 < 240 && q.y + 13 > 302) zone++; } });
        dots.forEach(d => { const cx = +d.getAttribute('cx'), cy = +d.getAttribute('cy'), r = +d.getAttribute('r');
          minY = Math.min(minY, cy - r); maxY = Math.max(maxY, cy + r); minX = Math.min(minX, cx - r); if (cx - r < 240 && cy + r > 302) zone++; });
        if (minY < 50) errs.push(`ragt oben aus der Sichtzone (y ${minY.toFixed(0)} < 50)`);
        if (maxY > 350) errs.push(`ragt unten aus der Sichtzone (y ${maxY.toFixed(0)} > 350)`);
        if (minX < 107) errs.push(`zu weit links (x ${minX.toFixed(0)} < 107)`);
        if (zone) errs.push('berührt die Wortmarken-Zone (x < 240, y > 300)');
      }
      svg.remove(); out.push({ id, errs });
    });
    return out;
  });
  await b.close();
  let bad = 0; res.forEach(r => { console.log((r.errs.length ? '✗ ' : '✓ ') + r.id + (r.errs.length ? ': ' + r.errs.join('; ') : '')); bad += r.errs.length; });
  process.exit(bad ? 1 : 0);
})();
