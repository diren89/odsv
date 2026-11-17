#!/usr/bin/env python3
"""ODSV – Doku gegen Code und Katalog prüfen (läuft in tools/validate.sh, nur Standardbibliothek).

Prüft, dass die Einstiegsdokumente für Agents stimmen:
  1. Version in README, AGENTS, SPEC, llms.txt und odsv.js = tokens.json
  2. Zahlen in llms.txt, web/README.md, SPEC 10.4 = Katalog (Komponenten, Diagrammformen, Icons, Signets, Layouts, Lint-Regeln)
  3. jede Regel-ID aus tools/lint-html.js steht in AGENTS.md 3 und 3.1 – und umgekehrt
  4. jeder data-odsv-*-Hook aus odsv.js/odsv-charts.js und jede ODSVCharts-Funktion steht in catalog/js-api.md
  5. jede Komponenten-ID steht in AGENTS.md 7 (Absicht → Komponente)
  6. Dateipfade in Backticks existieren (Einstiegsdokumente)
Aufruf: python3 tools/check_docs.py   (Exit 1 bei Abweichung)
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def rd(p): return open(os.path.join(ROOT, p), encoding='utf-8').read()
def js(p): return json.load(open(os.path.join(ROOT, p), encoding='utf-8'))
errors = []
def err(msg): errors.append(msg)

version = js('tokens/tokens.json')['$extensions']['odsv']['version']
comps = js('catalog/components.json')['components']
charts = js('catalog/charts.json')['charts']
icons = js('catalog/icons.json')['icons']
signets = js('catalog/signets.json')['signets']
layouts = js('catalog/pptx-layouts.json')['layouts']
lint = rd('tools/lint-html.js')
rules = sorted(set(re.findall(r"add\('(?:error|warn)',\s*'([a-z-]+)'", lint)))
agents, spec, llms, api = rd('AGENTS.md'), rd('SPEC.md'), rd('llms.txt'), rd('catalog/js-api.md')

# 1) Version
for f, pat in [('README.md', r'^# .*v(\d+\.\d+\.\d+)'), ('AGENTS.md', r'ODSV (\d+\.\d+\.\d+) ist'), ('SPEC.md', r'^# .*v(\d+\.\d+\.\d+)'),
               ('llms.txt', r'^# .*?(\d+\.\d+\.\d+)'), ('web/odsv.js', r"version: '(\d+\.\d+\.\d+)'")]:
    m = re.search(pat, rd(f), re.M)
    if not m: err(f'{f}: Versionsangabe nicht gefunden')
    elif m.group(1) != version: err(f'{f}: Version {m.group(1)} ≠ tokens.json {version}')

# 2) Zahlen
facts = {'Komponenten': len(comps), 'Diagrammformen': len(charts), 'Icon-Namen': len(icons), 'Signets': len(signets), 'Folienlayouts': len(layouts), 'Regel-IDs': len(rules)}
for noun, n in facts.items():
    for m in re.finditer(r'(\d+) ' + noun, llms):
        if int(m.group(1)) != n: err(f'llms.txt: „{m.group(0)}“, Katalog hat {n}')
for m in re.finditer(r'(\d+) Diagrammformen', rd('web/README.md')):
    if int(m.group(1)) != len(charts): err(f'web/README.md: „{m.group(0)}“, Katalog hat {len(charts)}')
m = re.search(r'mit (\d+) Strich-Icons und (\d+) Signets', spec)
if not m: err('SPEC 10.4: Bestandsangabe „mit N Strich-Icons und M Signets“ fehlt')
elif (int(m.group(1)), int(m.group(2))) != (len(icons), len(signets)): err(f'SPEC 10.4: {m.group(0)} ≠ {len(icons)} Icons, {len(signets)} Signets')

# 3) Lint-Regeln
def section(text, n):
    m = re.search(rf'^## {n}\.[^\n]*\n(.*?)(?=^## \d+\.|\Z)', text, re.S | re.M)
    return m.group(1) if m else ''
sec3 = section(agents, 3)
table31 = sec3.split('### 3.1')[1] if '### 3.1' in sec3 else ''
in31 = set(re.findall(r'^\| `([a-z-]+)` \|', table31, re.M))
in3 = set(re.findall(r'\(([a-z]+)\)', sec3.split('### 3.1')[0]))
for r in rules:
    if r not in in31: err(f'AGENTS.md 3.1: Regel `{r}` fehlt in „Meldung → Behebung“')
    if r not in in3: err(f'AGENTS.md 3: Regel ({r}) bei keiner Muss-Regel genannt')
for r in sorted(in31 - set(rules)): err(f'AGENTS.md 3.1: Regel `{r}` gibt es in lint-html.js nicht')

# 4) JS-API
hooks = set()
for f in ('web/odsv.js', 'web/odsv-charts.js'):
    hooks |= set(re.findall(r"(data-odsv-[a-z]+(?:-[a-z]+)*)", rd(f)))
for hk in sorted(hooks):
    if hk not in api: err(f'catalog/js-api.md: Hook `{hk}` fehlt')
exp = re.search(r'window\.ODSVCharts = \{(.*?)\};', rd('web/odsv-charts.js'), re.S)
for fn in re.findall(r'(\w+):', exp.group(1) if exp else ''):
    if f'ODSVCharts.{fn}' not in api: err(f'catalog/js-api.md: ODSVCharts.{fn} fehlt')

# 5) Absicht → Komponente
sec7 = section(agents, 7)
named = set(re.findall(r'`([a-z0-9-]+)`', sec7))
for c in comps:
    if c['id'] not in named: err(f'AGENTS.md 7: Komponente `{c["id"]}` ohne Absicht')

# 6) Pfade
SKIP = {'validate_palette.js', 'out.pptx', 'seite.html', 'deine-seite.html', 'pfad/zu/seite.html', 'site/index.html'}
for f in ('README.md', 'AGENTS.md', 'CLAUDE.md', 'llms.txt', 'web/README.md', 'catalog/js-api.md', 'SPEC.md'):
    base = os.path.dirname(f)
    for p in set(re.findall(r'(?:`|\]\()((?:\.\./)?(?:[\w.-]+/)+[\w.-]+\.(?:md|py|js|json|css|html|svg|sh|potx|pptx|txt|yml))(?:`|\)|#)', rd(f))):
        if p in SKIP: continue
        if not (os.path.exists(os.path.join(ROOT, p)) or os.path.exists(os.path.join(ROOT, base, p))):
            err(f'{f}: Pfad `{p}` existiert nicht')

if errors:
    print('\n'.join('✗ ' + e for e in errors))
    print(f'{len(errors)} Abweichung(en) zwischen Doku und Code')
    sys.exit(1)
print(f'Doku: Version {version}, {len(comps)} Komponenten, {len(charts)} Diagrammformen, {len(rules)} Lint-Regeln, {len(hooks)} Hooks – alles beschrieben')
