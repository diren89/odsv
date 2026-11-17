// Gezielte Ausschnitte: node tools/shot.js seite.html m|d dark|light "#id1,#id2"
const { chromium } = (() => { try { return require('playwright'); } catch (e) { return require('/opt/npm-tools/node_modules/playwright'); } })();
const CHROME = process.env.CHROME_PATH || (require('fs').existsSync('/usr/bin/google-chrome') ? '/usr/bin/google-chrome' : undefined);
const path = require('path');
const [pg, v, theme, sels] = process.argv.slice(2);
const root = path.join(__dirname, '..', 'web');
(async () => {
  const b = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox'] });
  const vp = v === 'm' ? { width: 390, height: 844 } : { width: 1440, height: 900 };
  const ctx = await b.newContext({ viewport: vp });
  const p = await ctx.newPage();
  await p.addInitScript(t => { try { localStorage.setItem('odsv-theme', t); } catch (e) {} }, theme);
  await p.goto('file://' + path.join(root, pg)); await p.waitForTimeout(700);
  for (const s of sels.split(',')) {
    const el = await p.$(s); if (!el) { console.log('fehlt', s); continue; }
    await el.scrollIntoViewIfNeeded(); await p.waitForTimeout(200);
    const out = path.join(root, '_qa', 'cut-' + pg.replace(/[\/.]/g, '_') + '-' + v + '-' + theme + '-' + s.replace(/[^a-z0-9]/gi, '') + '.png');
    await el.screenshot({ path: out }); console.log(out);
  }
  await b.close();
})();
