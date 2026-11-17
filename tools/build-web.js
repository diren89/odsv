// ODSV Web-Build: kopiert tokens.css nach web/ und bettet icons.svg als Inline-Sprite in die HTML-Seiten ein
// (file:// erlaubt kein <use href="icons.svg#…"> über Dateigrenzen; per HTTP funktioniert beides).
// Aufruf: node tools/build-web.js
const fs = require('fs'), path = require('path');
const root = path.join(__dirname, '..');
fs.copyFileSync(path.join(root, 'tokens/tokens.css'), path.join(root, 'web/tokens.css'));
let sprite = fs.readFileSync(path.join(root, 'web/icons.svg'), 'utf8')
  .replace(/<\?xml[^>]*\?>/, '').replace(/<!--[\s\S]*?-->/g, '').trim()
  .replace(/^<svg[^>]*>/, '<svg xmlns="http://www.w3.org/2000/svg" class="odsv-sprite" aria-hidden="true" focusable="false" style="position:absolute;width:0;height:0;overflow:hidden">');
for (const f of ['web/index.html', 'web/examples/website.html', 'web/examples/dashboard.html', 'templates/website.html', 'templates/dashboard.html']) {
  const p = path.join(root, f);
  if (!fs.existsSync(p)) continue;
  let h = fs.readFileSync(p, 'utf8');
  const re = /<!--ODSV-SPRITE-->[\s\S]*?<!--\/ODSV-SPRITE-->/;
  if (!re.test(h)) { console.log('Marker fehlt:', f); continue; }
  h = h.replace(re, () => '<!--ODSV-SPRITE-->' + sprite + '<!--/ODSV-SPRITE-->');
  fs.writeFileSync(p, h);
  console.log('Sprite eingebettet:', f);
}
