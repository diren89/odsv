// QA: Screenshots (390x844, 1440x900; dunkel/hell), Konsolenfehler, horizontales Scrollen, abgeschnittene Texte.
const { chromium } = (() => { try { return require('playwright'); } catch (e) { return require('/opt/npm-tools/node_modules/playwright'); } })();
const CHROME = process.env.CHROME_PATH || (require('fs').existsSync('/usr/bin/google-chrome') ? '/usr/bin/google-chrome' : undefined);
const path = require('path'), fs = require('fs');
const root = path.join(__dirname, '..', 'web');
const pages = (process.argv[2] ? process.argv[2].split(',') : ['index.html', 'examples/website.html', 'examples/dashboard.html']);
const full = process.argv[3] !== 'viewport';
(async () => {
  const browser = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox'] });
  fs.mkdirSync(path.join(root, '_qa'), { recursive: true });
  let problems = 0;
  for (const pg of pages) {
    for (const vp of [{ n: 'm', w: 390, h: 844 }, { n: 'd', w: 1440, h: 900 }]) {
      for (const theme of ['dark', 'light']) {
        const ctx = await browser.newContext({ viewport: { width: vp.w, height: vp.h }, deviceScaleFactor: 1 });
        const page = await ctx.newPage();
        const errs = [];
        page.on('console', m => { if (['error', 'warning'].includes(m.type())) errs.push(m.type() + ': ' + m.text()); });
        page.on('pageerror', e => errs.push('pageerror: ' + e.message));
        page.on('requestfailed', r => errs.push('requestfailed: ' + r.url()));
        await page.addInitScript(t => { try { localStorage.setItem('odsv-theme', t); } catch (e) {} }, theme);
        await page.goto('file://' + path.join(root, pg));
        await page.waitForTimeout(700);
        const info = await page.evaluate(() => {
          const de = document.documentElement, over = de.scrollWidth - de.clientWidth;
          const wide = [];
          document.querySelectorAll('body *').forEach(e => {
            const r = e.getBoundingClientRect();
            if (e.tagName !== 'use' && r.width && r.right > de.clientWidth + 1 && !e.closest('.odsv-table-wrap,.docs-snippet,.odsv-scroll-x,.odsv-tabs,.odsv-sprite,.odsv-signet-card,[hidden],.odsv-sheet,.odsv-tooltip__content,.odsv-stage,.odsv-chart__tip,.odsv-topbar__nav')) {
              const cs = getComputedStyle(e); if (cs.position !== 'fixed' && cs.visibility !== 'hidden') wide.push(e.tagName + '.' + String(e.className && e.className.baseVal !== undefined ? e.className.baseVal : e.className).slice(0, 50));
            }
          });
          const clipped = [];
          document.querySelectorAll('h1,h2,h3,h4,p,span,a,button,li,dt,dd,th,td,label,summary').forEach(e => {
            if (e.closest('.odsv-sprite,svg,.odsv-table-wrap,.docs-snippet,.odsv-sr-only')) return;
            const cs = getComputedStyle(e); if (cs.visibility === 'hidden' || cs.display === 'none') return;
            if (e.scrollWidth > e.clientWidth + 2 && cs.overflow !== 'visible' && cs.display !== 'inline') clipped.push(e.tagName + ':' + (e.textContent || '').trim().slice(0, 30));
          });
          return { over, wide: wide.slice(0, 8), clipped: clipped.slice(0, 8), theme: de.getAttribute('data-theme'), h: de.scrollHeight };
        });
        const tag = pg.replace(/[\/.]/g, '_').replace('_html', '') + '-' + vp.n + '-' + theme;
        await page.screenshot({ path: path.join(root, '_qa', tag + '.png'), fullPage: full && info.h < 16000 });
        const bad = errs.length || info.over > 0 || info.wide.length || info.clipped.length;
        if (bad) problems++;
        console.log((bad ? 'X ' : 'ok ') + tag, '| theme', info.theme, '| scrollW+', info.over, '| h', info.h, errs.length ? '\n   console: ' + errs.slice(0, 5).join('\n   ') : '', info.wide.length ? '\n   wide: ' + info.wide.join(', ') : '', info.clipped.length ? '\n   clipped: ' + info.clipped.join(' | ') : '');
        await ctx.close();
      }
    }
  }
  await browser.close();
  console.log('Probleme:', problems);
})();
