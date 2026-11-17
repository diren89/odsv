#!/usr/bin/env python3
"""Erzeugt den Agenten-Katalog aus den Quellen (nie von Hand ändern):
  catalog/components.json   Komponenten: Zweck, Abgrenzung, Klassen, Varianten, Zustände, Regeln, A11y, JS, Beispiele
  catalog/COMPONENTS.md     dasselbe lesbar
  catalog/classes.json      alle gültigen .odsv-Klassen (für tools/lint-html.js)
  catalog/icons.json        Icon-Namen aus web/icons.svg
  catalog/tokens.flat.json  alle Tokens flach: CSS-Variable, Wert dunkel/hell, Typ, Beschreibung
  catalog/pptx-layouts.json Folienlayouts: Platzhalter-Rollen → idx, Name, Stil, Zeichengrenzen, Regeln
Quellen: catalog/src/components.meta.py, web/odsv.css, web/index.html, web/icons.svg,
         tokens/tokens.json, tokens/pptx.json, pptx/_build/roles.json
Aufruf: python3 tools/build_catalog.py
"""
import json, re, textwrap, runpy, pathlib, collections, sys
from bs4 import BeautifulSoup

ROOT = pathlib.Path(__file__).resolve().parent.parent
CAT = ROOT / 'catalog'
META = runpy.run_path(str(CAT / 'src' / 'components.meta.py'))['META']
css = (ROOT / 'web' / 'odsv.css').read_text()
html = (ROOT / 'web' / 'index.html').read_text()
version = json.loads((ROOT / 'tokens' / 'tokens.json').read_text())['$extensions']['odsv']['version']

# --- Klassen aus CSS ---------------------------------------------------------------------------
all_classes = sorted(set(re.findall(r'\.(odsv-[a-z0-9_-]+)', css)))
states = sorted(set(re.findall(r'\.(is-[a-z-]+)', css)))
def root_of(c):
    return re.split(r'__|--', c[5:])[0]
by_root = collections.defaultdict(lambda: {'elements': set(), 'modifiers': set(), 'classes': set()})
for c in all_classes:
    r = root_of(c); b = by_root[r]; b['classes'].add(c)
    if '__' in c: b['elements'].add(c.split('__', 1)[1].split('--')[0])
    if '--' in c: b['modifiers'].add(c.split('--')[-1])
def roots_match(r, want):
    return r == want or (want in ('col', 'mt', 'dv') and r.startswith(want + '-')) or (want == 'col' and r == 'col-')

# --- Beispiele aus der Referenzseite -------------------------------------------------------------
soup = BeautifulSoup(html, 'html.parser')
def clean(s):
    s = textwrap.dedent(s.strip('\n')).strip()
    return re.sub(r'\n\s*\n+', '\n', s)
examples = {}
for sec in soup.select('section.docs-section[id]'):
    out = []
    blocks = sec.select('div.docs-block')
    if blocks:
        for b in blocks:
            t = b.find('template', class_='docs-src')
            if not t: continue
            h = b.find(['h3'])
            out.append({'title': h.get_text(strip=True) if h else '', 'captions': (t.get('data-captions') or '').split('|') if t.get('data-captions') else [], 'html': clean(t.decode_contents())})
    for t in sec.find_all('template', class_='docs-src', recursive=False):
        out.append({'title': '', 'captions': (t.get('data-captions') or '').split('|') if t.get('data-captions') else [], 'html': clean(t.decode_contents())})
    examples[sec['id']] = out

# --- Komponenten zusammenführen ----------------------------------------------------------------
components, covered = [], set()
for cid, m in META.items():
    roots = [r for r in by_root if any(roots_match(r, w) for w in m['roots'])]
    covered.update(roots)
    cls = sorted(set().union(*[by_root[r]['classes'] for r in roots])) if roots else []
    comp = {
        'id': cid, 'name': m['name'], 'use': m['use'], 'avoid': m.get('avoid', ''),
        'root_classes': ['odsv-' + r for r in m['roots']],
        'classes': cls,
        'elements': sorted(set().union(*[by_root[r]['elements'] for r in roots])) if roots else [],
        'modifiers': sorted(set().union(*[by_root[r]['modifiers'] for r in roots])) if roots else [],
        'variants': m.get('variants', {}), 'states': m.get('states', {}),
        'rules': m.get('rules', []), 'a11y': m.get('a11y', []), 'js': m.get('js', ''),
        'content_limits': m.get('content', {}),
        'reference': 'web/index.html#' + m['section'],
        'examples': examples.get(m['section'], []) if cid not in ('hgroup', 'toast', 'footer', 'list-facts', 'utilities') else
                    [e for e in examples.get(m['section'], []) if (cid == 'hgroup' and 'Headline' in e['title']) or (cid == 'toast' and e['title'] == 'Toast') or (cid == 'footer' and 'Fuß' in e['title']) or (cid == 'list-facts' and 'Liste' in e['title'])],
    }
    components.append(comp)
sig_path = CAT / 'signets.json'
if sig_path.exists():
    for c in components:
        if c['id'] == 'signet': c['signets'] = json.loads(sig_path.read_text())['signets']
uncovered = sorted(r for r in by_root if r not in covered)
if uncovered:
    print('WARNUNG – CSS-Wurzeln ohne Katalogeintrag:', ', '.join(uncovered));

# --- Icons, Tokens, Folien ---------------------------------------------------------------------
icons = sorted(re.findall(r'id="odsv-icon-([a-z0-9-]+)"', (ROOT / 'web' / 'icons.svg').read_text()))
tok = json.loads((ROOT / 'tokens' / 'tokens.json').read_text())
flat = {}
def walk(o, path, theme):
    if isinstance(o, dict):
        if '$value' in o:
            name = '--odsv-' + '-'.join(path)
            e = flat.setdefault(name, {'path': '.'.join(path), 'type': o.get('$type', ''), 'description': o.get('$description', '')})
            e['dark' if theme == 'dark' else theme] = o['$value']
            if o.get('$description') and not e['description']: e['description'] = o['$description']
            return
        for k, v in o.items():
            if k.startswith('$'): continue
            if not path and k == 'theme':
                for th, sub in v.items(): walk(sub, [], th)
                continue
            walk(v, path + [k], theme)
walk(tok, [], 'dark')
pj = json.loads((ROOT / 'tokens' / 'pptx.json').read_text())
roles = json.loads((ROOT / 'pptx' / '_build' / 'roles.json').read_text())
spec_by_id = {l['name']: l for l in pj['layouts']}
SPEC_ID = {'Titel': 'title', 'Kapiteltrenner': 'chapter', 'Agenda': 'agenda', 'Inhalt einspaltig': 'content-1', 'Zwei Spalten': 'content-2',
           'KPI drei Zahlen': 'kpi', 'Diagramm': 'chart', 'Bild vollflächig': 'image', 'Bild in Karte': 'image-card', 'Zitat': 'quote',
           'Prozess vier Schritte': 'process', 'Vergleich': 'compare', 'Tabelle': 'table', 'Abschluss': 'closing', 'Nur Titel': 'title-only', 'Leer': 'blank'}
def spec_key(role):
    base = re.sub(r'\d+$', '', role); n = role[len(base):]
    m = {'title': 'headline', 'body': 'list', 'ilabel': 'insight', 'itext': 'insight', 'inote': 'insight', 'tl': 'tiles', 'tv': 'tiles',
         'n': 'cards', 't': 'cards', 'x': 'cards'}
    if base in ('label', 'title', 'text', 'head') and n:
        return [{'0': 'left', '1': 'right'}[n], {'0': 'a', '1': 'b'}[n], base]
    return [role, base, m.get(base, base), 'list' if base == 'body' else base]
try:
    from pptx import Presentation
    prs = Presentation(str(ROOT / 'pptx' / 'ODSV-Vorlage.pptx'))
    ph_names = {l.name: {p.placeholder_format.idx: p.name for p in l.placeholders} for l in prs.slide_layouts}
except Exception:
    ph_names = {}
layouts = []
for r in roles:
    s = spec_by_id.get(SPEC_ID.get(r['name'], ''), {})
    sp_all = s.get('placeholders') or {}
    phs = []
    for role, idx in r['map'].items():
        sp = {}
        for k in spec_key(role):
            if k in sp_all and isinstance(sp_all[k], dict): sp = sp_all[k]; break
        dflt = {'eyebrow': ('eyebrow', None), 'title': ('headline', 34), 'sub': ('sub', 90), 'body': ('body', None), 'image': ('image', None)}.get(role, ('', None))
        phs.append({'role': role, 'idx': idx, 'name': ph_names.get(r['name'], {}).get(idx, ''), 'style': sp.get('style') or dflt[0],
                    'maxChars': sp.get('maxChars') or dflt[1], 'lines': sp.get('lines')})
    layouts.append({'name': r['name'], 'spec_id': s.get('name', ''), 'use': s.get('use', ''), 'progress': s.get('progress', True),
                    'footer': s.get('footer', True), 'placeholders': phs, 'rules': s.get('rules', [])})
missing = [l['name'] for l in layouts if not l['spec_id']]
if missing: print('WARNUNG – Folienlayouts ohne Spezifikation:', missing)

# --- Schreiben -----------------------------------------------------------------------------------
CAT.mkdir(exist_ok=True)
def dump(name, data):
    (CAT / name).write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n')
dump('components.json', {'version': version, 'generated_by': 'tools/build_catalog.py', 'states': states, 'components': components})
dump('classes.json', {'version': version, 'classes': all_classes, 'states': states})
dump('icons.json', {'version': version, 'usage': '<svg class="odsv-icon" aria-hidden="true"><use href="#odsv-icon-NAME"/></svg>', 'icons': icons})
dump('tokens.flat.json', {'version': version, 'tokens': flat})
dump('pptx-layouts.json', {'version': version, 'template': 'pptx/ODSV-Vorlage.potx', 'helper': 'pptx/odsv_pptx.py', 'footer_placeholders': {'source': 11, 'slide_number': 12}, 'layouts': layouts})

md = [f'# ODSV {version} – Komponentenkatalog', '',
      '> Erzeugt von `tools/build_catalog.py` aus `catalog/src/components.meta.py`, `web/odsv.css` und `web/index.html`. Nicht von Hand ändern.',
      '> Maschinenlesbar: `catalog/components.json`. Gültige Klassen: `catalog/classes.json`.', '',
      '| Komponente | Wurzelklassen | Wofür |', '|---|---|---|']
for c in components:
    md.append(f"| [{c['name']}](#{c['id']}) | {' '.join('`.'+r+'`' for r in c['root_classes'][:4])}{' …' if len(c['root_classes'])>4 else ''} | {c['use'].split('.')[0]}. |")
md.append('')
for c in components:
    md += [f'<a id="{c["id"]}"></a>', f"## {c['name']}", '', f"**Wofür:** {c['use']}", '']
    if c['avoid']: md += [f"**Nicht für:** {c['avoid']}", '']
    if c['variants']:
        md += ['| Klasse/Variante | Bedeutung |', '|---|---|'] + [f'| `{k}` | {v} |' for k, v in c['variants'].items()] + ['']
    if c['states']:
        md += ['**Zustände:** ' + ' · '.join(f'`{k}` – {v}' for k, v in c['states'].items()), '']
    if c['elements']:
        md += ['**Elemente:** ' + ', '.join('`__' + e + '`' for e in c['elements']), '']
    if c['rules']: md += ['**Regeln**', ''] + ['- ' + r for r in c['rules']] + ['']
    if c['a11y']: md += ['**Barrierefreiheit**', ''] + ['- ' + r for r in c['a11y']] + ['']
    if c['js']: md += [f"**Verhalten (odsv.js):** {c['js']}", '']
    if c.get('signets'): md += ['**Signet-Familie** (`catalog/signets.json`, SPEC 10.6)', '', '| ID | Gruppe | Thema | Bedeutung |', '|---|---|---|---|'] + [f"| `{x['id']}` | {x['group']} | {x['name']} | {x['meaning']} |" for x in c['signets']] + ['']
    if c['content_limits']: md += ['**Inhaltsgrenzen:** ' + ' · '.join(f'{k}: {v}' for k, v in c['content_limits'].items()), '']
    if c['examples']:
        ex = c['examples'][0]
        md += [f"**Beispiel{(' – ' + ex['title']) if ex['title'] else ''}** (weitere in `components.json`, live: `{c['reference']}`)", '', '```html', ex['html'][:2400] + ('\n<!-- … gekürzt -->' if len(ex['html']) > 2400 else ''), '```', '']
(CAT / 'COMPONENTS.md').write_text('\n'.join(md))
print(f'Katalog: {len(components)} Komponenten, {len(all_classes)} Klassen, {len(icons)} Icons, {len(flat)} Tokens, {len(layouts)} Folienlayouts')
if uncovered: sys.exit(1)
