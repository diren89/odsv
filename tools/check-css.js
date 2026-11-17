// Prüft web/odsv.css: keine Hex-Farben (außer in Kommentaren), alle var(--odsv-…) in tokens.css definiert.
const fs = require('fs'), path = require('path');
const root = path.join(__dirname, '..');
const css = fs.readFileSync(path.join(root, 'web/odsv.css'), 'utf8');
const tok = fs.readFileSync(path.join(root, 'tokens/tokens.css'), 'utf8');
const strip = s => s.replace(/\/\*[\s\S]*?\*\//g, '');
let fail = 0;
function scan(file) {
  const c = strip(fs.readFileSync(path.join(root, file), 'utf8'));
  const hex = c.match(/#[0-9a-fA-F]{3,8}\b/g) || [];
  const fn = c.match(/\b(?:rgb|rgba|hsl|hsla)\(/g) || [];
  const named = c.match(/:\s*(?:white|black|red|green|blue|yellow|gray|grey|orange)\b/g) || [];
  const defined = new Set([...tok.matchAll(/(--odsv-[a-z0-9-]+)\s*:/g)].map(m => m[1]));
  const used = new Set([...c.matchAll(/var\((--odsv-[a-z0-9-]+)/g)].map(m => m[1]));
  const undef = [...used].filter(v => !defined.has(v));
  console.log(file, '| Hex:', hex.length, '| rgb/hsl:', fn.length, '| Farbnamen:', named.length, '| var verwendet:', used.size, '| undefiniert:', undef.length);
  if (hex.length) console.log('  Hex:', [...new Set(hex)].join(' '));
  if (undef.length) console.log('  undefiniert:', undef.join(' '));
  if (hex.length || fn.length || named.length || undef.length) fail = 1;
}
['web/odsv.css', 'web/docs.css'].forEach(f => fs.existsSync(path.join(root, f)) && scan(f));
// Inline-<style>/style=-Attribute der HTML-Seiten
for (const f of ['web/index.html', 'web/examples/website.html', 'web/examples/dashboard.html']) {
  if (!fs.existsSync(path.join(root, f))) continue;
  const h = fs.readFileSync(path.join(root, f), 'utf8');
  const styles = [...h.matchAll(/<style[^>]*>([\s\S]*?)<\/style>/g)].map(m => m[1]).join('\n') + [...h.matchAll(/style="([^"]*)"/g)].map(m => m[1]).join('\n');
  const hex = strip(styles).match(/#[0-9a-fA-F]{3,8}\b/g) || [];
  const defined = new Set([...tok.matchAll(/(--odsv-[a-z0-9-]+)\s*:/g)].map(m => m[1]));
  const undef = [...new Set([...styles.matchAll(/var\((--odsv-[a-z0-9-]+)/g)].map(m => m[1]))].filter(v => !defined.has(v));
  console.log(f, '| Inline-Hex:', hex.length, '| undefiniert:', undef.length, undef.join(' '));
  if (hex.length || undef.length) fail = 1;
}
const same = fs.readFileSync(path.join(root, 'web/tokens.css'), 'utf8') === tok;
console.log('web/tokens.css identisch mit tokens/tokens.css:', same); if (!same) fail = 1;
process.exit(fail);
