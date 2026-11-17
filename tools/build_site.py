#!/usr/bin/env python3
"""ODSV – statische Website im Stil eines Komponenten-Explorers (wie Storybook) erzeugen.

Aufruf:  python3 tools/build_site.py [--out site]
Quellen: catalog/*.json, catalog/tokens.flat.json, SPEC.md, AGENTS.md, web/* , pptx/ODSV-Vorlage.potx
Ergebnis: site/ – reines HTML/CSS/JS ohne Build-Kette, läuft über file:// und auf jedem statischen Host
(z. B. GitHub Pages, siehe .github/workflows/pages.yml). Nur Python-Standardbibliothek.

Aufbau:
  index.html                 Einführung, Einbindung, Überblick
  grundlagen/*.html          Farben, Typografie, Raster und Maße, Effekte, Icons, Signets
  komponenten/<id>.html      je Komponente: Storys (Canvas im iframe, Theme, Viewport, Code) und Doku
  frames/<id>-<n>.html       isolierte Story (wie Storybooks iframe.html), ?theme=dark|light
  richtlinien/*.html         SPEC.md je Kapitel, AGENTS.md
  praesentationen.html, downloads.html
  assets/                    tokens.css, odsv.css, odsv.js, odsv-charts.js, icons.svg, Signets, Vorlage
"""
import argparse, html, json, os, re, shutil, sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def src(*p): return os.path.join(ROOT, *p)
def read(*p): return open(src(*p), encoding='utf-8').read()
esc = lambda s: html.escape(str(s), quote=True)

TOKENS = json.load(open(src('catalog/tokens.flat.json')))
VERSION = TOKENS['version']
FLAT = TOKENS['tokens']
COMPS = json.load(open(src('catalog/components.json')))['components']
SIGNETS = json.load(open(src('catalog/signets.json')))['signets']
ICONS = json.load(open(src('catalog/icons.json')))
LAYOUTS = json.load(open(src('catalog/pptx-layouts.json')))
SPRITE = re.sub(r'<!--.*?-->', '', read('web/icons.svg'), flags=re.S).strip()
SPRITE = SPRITE.replace('<svg ', '<svg aria-hidden="true" focusable="false" class="sbf-sprite" width="0" height="0" ', 1)
ICON_NAMES = re.findall(r'<symbol id="odsv-icon-([^"]+)"', SPRITE)

def icon(name, label=None):
    a = f' role="img" aria-label="{esc(label)}"' if label else ' aria-hidden="true"'
    return f'<svg class="odsv-icon"{a}><use href="#odsv-icon-{name}"/></svg>'

# ---------------------------------------------------------------- Gruppen
GROUPS = [
    ('Grundlagen', ['typography', 'layout', 'icon', 'hgroup', 'utilities']),
    ('Aktionen', ['button', 'link']),
    ('Inhalte', ['card', 'kpi', 'step', 'list-facts', 'tile']),
    ('Fortschritt und Auswahl', ['progress', 'segmented', 'checklist', 'accordion', 'tabs']),
    ('Daten', ['table', 'chart', 'label3d']),
    ('Rückmeldung', ['callout', 'badge', 'toast', 'empty-loading', 'tooltip']),
    ('Formulare', ['form']),
    ('Navigation', ['navigation', 'sheet', 'footer']),
    ('Marke', ['signet']),
]
BY_ID = {c['id']: c for c in COMPS}
missing = [c['id'] for c in COMPS if not any(c['id'] in ids for _, ids in GROUPS)]
GROUPS[-1][1].extend(missing)  # neue Komponenten landen sichtbar am Ende, statt zu fehlen
GROUP_OF = {cid: g for g, ids in GROUPS for cid in ids}

FOUNDATIONS = [
    ('farben', 'Farben', 'Rollen, Themes und Kontraste'),
    ('typografie', 'Typografie', 'Schriften, Stile und Versalien'),
    ('raster', 'Raster und Maße', 'Abstände, Radien, Größen, Layout'),
    ('effekte', 'Effekte und Bewegung', 'Schatten, Bewegung, Ebenen, Breakpoints'),
    ('icons', 'Icons', f'{len(ICON_NAMES)} Strich-Icons im 24-px-Raster'),
    ('signets', 'Signets', f'{len(SIGNETS)} Signets einer Familie'),
]

# ---------------------------------------------------------------- Markdown (klein, für SPEC/AGENTS)
def slug(s):
    s = s.lower().translate(str.maketrans({'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss'}))
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-') or 'abschnitt'

def inline(t):
    codes = []
    def keep(m):
        codes.append('<code>' + esc(m.group(1)) + '</code>'); return f'\x00{len(codes) - 1}\x00'
    t = re.sub(r'`([^`]+)`', keep, t)
    t = esc(t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<em>\1</em>', t)
    def link(m):
        label, url = m.group(1), html.unescape(m.group(2))
        if re.match(r'https?://', url):
            return f'<a class="odsv-link" href="{esc(url)}">{label}</a>'
        mapped = LINKMAP.get(url.split('#')[0])
        return f'<a class="odsv-link" href="{{P}}{mapped}">{label}</a>' if mapped else label
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link, t)
    return re.sub(r'\x00(\d+)\x00', lambda m: codes[int(m.group(1))], t)

def split_row(line):
    line = line.strip().strip('|')
    cells, cur, in_code = [], '', False
    i = 0
    while i < len(line):
        ch = line[i]
        if ch == '\\' and i + 1 < len(line) and line[i + 1] == '|': cur += '|'; i += 2; continue
        if ch == '`': in_code = not in_code
        if ch == '|' and not in_code: cells.append(cur.strip()); cur = ''
        else: cur += ch
        i += 1
    cells.append(cur.strip())
    return cells

def markdown(md, toc=None):
    lines = md.split('\n'); out = []; i = 0
    def list_block(i):
        items = []; ordered = bool(re.match(r'\s*\d+\.\s', lines[i])); base = len(lines[i]) - len(lines[i].lstrip())
        while i < len(lines):
            l = lines[i]; ind = len(l) - len(l.lstrip())
            m = re.match(r'\s*(?:[-*]|\d+\.)\s+(.*)', l)
            if m and ind == base:
                items.append([inline(m.group(1)), []]); i += 1
            elif m and ind > base and items:
                sub, i = list_block(i); items[-1][1].append(sub)
            elif l.strip() and ind > base and items and not m:
                items[-1][0] += ' ' + inline(l.strip()); i += 1
            else: break
        tag = 'ol' if ordered else 'ul'
        return f'<{tag}>' + ''.join(f'<li>{t}{"".join(s)}</li>' for t, s in items) + f'</{tag}>', i
    while i < len(lines):
        l = lines[i]
        if not l.strip(): i += 1; continue
        if l.startswith('```'):
            lang = l[3:].strip(); i += 1; buf = []
            while i < len(lines) and not lines[i].startswith('```'): buf.append(lines[i]); i += 1
            i += 1
            out.append(f'<pre tabindex="0"><code>{esc(chr(10).join(buf))}</code></pre>'); continue
        m = re.match(r'(#{1,4})\s+(.*)', l)
        if m:
            lvl = max(2, len(m.group(1))); text = m.group(2).strip(); hid = slug(re.sub(r'`', '', text))
            if toc is not None and lvl == 3: toc.append((hid, re.sub(r'`', '', text)))
            out.append(f'<h{lvl} id="{hid}">{inline(text)}</h{lvl}>'); i += 1; continue
        if re.match(r'\s*(---|\*\*\*)\s*$', l): out.append('<hr>'); i += 1; continue
        if l.lstrip().startswith('|') and i + 1 < len(lines) and re.match(r'\s*\|?\s*:?-{2,}', lines[i + 1]):
            head = split_row(l); i += 2; rows = []
            while i < len(lines) and lines[i].lstrip().startswith('|'): rows.append(split_row(lines[i])); i += 1
            th = ''.join(f'<th scope="col">{inline(c)}</th>' for c in head)
            tb = ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>' for r in rows)
            out.append(f'<div class="odsv-table-wrap" role="region" tabindex="0" aria-label="Tabelle"><table class="odsv-table odsv-table--compact">'
                       f'<thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table></div>'); continue
        if l.startswith('>'):
            buf = []
            while i < len(lines) and lines[i].startswith('>'): buf.append(lines[i].lstrip('> ')); i += 1
            out.append(f'<blockquote>{inline(" ".join(buf))}</blockquote>'); continue
        if re.match(r'\s*(?:[-*]|\d+\.)\s+', l):
            block, i = list_block(i); out.append(block); continue
        buf = [l.strip()]; i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r'(#{1,4}\s|```|\s*(?:[-*]|\d+\.)\s+|\||>)', lines[i]):
            buf.append(lines[i].strip()); i += 1
        out.append(f'<p>{inline(" ".join(buf))}</p>')
    return '\n'.join(out)

# ---------------------------------------------------------------- Richtlinien aus SPEC.md
spec = read('SPEC.md')
parts = re.split(r'(?m)^## ', spec)
SPEC_INTRO = parts[0]
CHAPTERS = []
for p in parts[1:]:
    title, _, body = p.partition('\n')
    m = re.match(r'(\d+)\.\s+(.*)', title.strip())
    if not m: continue
    CHAPTERS.append({'num': int(m.group(1)), 'title': m.group(2).strip(), 'slug': f'{int(m.group(1)):02d}-{slug(m.group(2))}',
                     'body': body.strip().rstrip('-').strip()})
LINKMAP = {'AGENTS.md': 'richtlinien/agents.html', 'SPEC.md': 'richtlinien/index.html'}

# ---------------------------------------------------------------- Seitenrahmen
def nav(active, P):
    def li(href, label, key, keys=''):
        cur = ' aria-current="page"' if key == active else ''
        k = f' data-sb-keys="{esc(keys.lower())}"' if keys else ''
        return f'<li{k}><a href="{P}{href}"{cur}>{esc(label)}</a></li>'
    g = []
    g.append('<div class="sb-nav__group"><p class="odsv-eyebrow">Start</p><ul>'
             + li('index.html', 'Einführung', 'index') + li('downloads.html', 'Downloads', 'downloads', 'css js potx tokens') + '</ul></div>')
    g.append('<div class="sb-nav__group"><p class="odsv-eyebrow">Grundlagen</p><ul>'
             + ''.join(li(f'grundlagen/{s}.html', t, f'f-{s}', d) for s, t, d in FOUNDATIONS) + '</ul></div>')
    comp = ['<div class="sb-nav__group"><p class="odsv-eyebrow">Komponenten</p>']
    for gname, ids in GROUPS:
        comp.append(f'<p class="sb-nav__sub">{esc(gname)}</p><ul>')
        for cid in ids:
            c = BY_ID[cid]
            comp.append(li(f'komponenten/{cid}.html', c['name'], f'c-{cid}', ' '.join(c.get('root_classes', [])) + ' ' + cid))
        comp.append('</ul>')
    comp.append('</div>'); g.append(''.join(comp))
    g.append('<div class="sb-nav__group"><p class="odsv-eyebrow">Richtlinien</p><ul>'
             + li('richtlinien/index.html', 'Überblick', 'r-index')
             + ''.join(li(f'richtlinien/{ch["slug"]}.html', f'{ch["num"]}. {ch["title"]}', f'r-{ch["slug"]}') for ch in CHAPTERS)
             + li('richtlinien/agents.html', 'Für AI-Agents', 'r-agents', 'agents llm ki') + '</ul></div>')
    g.append('<div class="sb-nav__group"><p class="odsv-eyebrow">Medien</p><ul>'
             + li('praesentationen.html', 'Präsentationen', 'pptx', 'pptx powerpoint folien') + '</ul></div>')
    return '<nav class="sb-nav" aria-label="Inhalte">' + ''.join(g) + '<p class="sb-nav__empty" hidden>Kein Treffer. Suchbegriff ändern.</p></nav>'

def page(path, title, body, active, crumbs=(), desc=''):
    depth = path.count('/'); P = '../' * depth
    crumb = ''.join(f'<span>{esc(c)}</span><span aria-hidden="true">/</span>' for c in crumbs) + f'<strong>{esc(title)}</strong>'
    doc = f'''<!doctype html>
<html lang="de" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · ODSV</title>
<meta name="description" content="{esc(desc or 'ODSV – dunkles Design-System für Websites, Dashboards und Präsentationen.')}">
<link rel="icon" href="{P}assets/signets/odsv-signet.svg" type="image/svg+xml">
<link rel="stylesheet" href="{P}assets/tokens.css">
<link rel="stylesheet" href="{P}assets/odsv.css">
<link rel="stylesheet" href="{P}assets/site.css">
<script src="{P}assets/odsv.js"></script>
</head>
<body>
{SPRITE}
<a class="odsv-skip" href="#inhalt">Zum Inhalt springen</a>
<div class="sb">
<aside class="sb-side" aria-label="Seitenleiste">
<a class="sb-brand" href="{P}index.html"><span class="sb-brand__name">ODSV</span><span class="sb-brand__ver">v{esc(VERSION)}</span></a>
<div class="sb-search" role="search">
<label class="odsv-sr-only" for="sb-search">Komponenten und Seiten durchsuchen</label>
<input class="odsv-input" id="sb-search" type="search" placeholder="Suchen …" autocomplete="off">
<p class="sb-search__hint">Taste <kbd class="odsv-kbd">/</kbd> zum Suchen</p>
</div>
{nav(active, P)}
</aside>
<div class="sb-scrim" hidden></div>
<div class="sb-main">
<header class="sb-top">
<button class="odsv-icon-btn sb-menu" type="button" aria-label="Navigation öffnen" aria-expanded="false">{icon('menu')}</button>
<p class="sb-crumbs">{crumb}</p>
<button class="odsv-icon-btn sb-theme" type="button" data-odsv-theme-toggle aria-label="Helles Theme aktivieren"><svg class="odsv-icon sb-theme__moon" aria-hidden="true"><use href="#odsv-icon-moon"/></svg><svg class="odsv-icon sb-theme__sun" aria-hidden="true"><use href="#odsv-icon-sun"/></svg></button>
</header>
<main class="sb-content" id="inhalt" tabindex="-1">
{body.replace('{P}', P)}
</main>
<footer class="sb-foot">ODSV {esc(VERSION)} · erzeugt aus dem Repository mit <code>tools/build_site.py</code>. Werte: <code>tokens/tokens.json</code>, Regeln: <code>SPEC.md</code>.</footer>
</div>
</div>
<script src="{P}assets/odsv-charts.js" defer></script>
<script src="{P}assets/site.js" defer></script>
</body>
</html>
'''
    write(path, doc)

OUT = None
def write(path, text):
    full = os.path.join(OUT, path); os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8').write(text)

def head(eyebrow, title, sub, level=1):
    return (f'<header class="sb-head odsv-hgroup"><p class="odsv-eyebrow">{esc(eyebrow)}</p>'
            f'<h{level} class="odsv-h1">{esc(title)}</h{level}><p class="odsv-sub">{sub}</p></header>')

def section(title, inner, sid=None):
    i = f' id="{sid}"' if sid else ''
    return f'<section class="sb-section"{i}><h2 class="odsv-h3">{esc(title)}</h2>{inner}</section>'

def ul(items):
    return '<ul class="odsv-list">' + ''.join(f'<li>{inline(x)}</li>' for x in items) + '</ul>'

def table(caption, headers, rows, num=()):
    NUM = ' class="odsv-table__num"'
    th = ''.join(f'<th scope="col"{NUM if i in num else ""}>{h}</th>' for i, h in enumerate(headers))
    tb = ''.join('<tr>' + ''.join(f'<td{NUM if i in num else ""}>{c}</td>' for i, c in enumerate(r)) + '</tr>' for r in rows)
    return (f'<div class="odsv-table-wrap" role="region" tabindex="0" aria-label="{esc(caption)}"><table class="odsv-table odsv-table--compact">'
            f'<caption class="odsv-sr-only">{esc(caption)}</caption><thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table></div>')

# ---------------------------------------------------------------- Story-Frames
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}
class TopSplit(HTMLParser):
    """Zerlegt ein Fragment in Elemente der obersten Ebene (für die Beschriftung von Zuständen)."""
    def __init__(self, text):
        super().__init__(convert_charrefs=False); self.text = text; self.depth = 0; self.starts = []; self.parts = []
        self.lines = [0]
        for ln in text.split('\n'): self.lines.append(self.lines[-1] + len(ln) + 1)
        self.feed(text); self.close()
    def pos(self):
        l, c = self.getpos(); return self.lines[l - 1] + c
    def handle_starttag(self, tag, attrs):
        if self.depth == 0: self.starts.append(self.pos())
        if tag not in VOID: self.depth += 1
        elif self.depth == 0: self.parts.append(self.text[self.starts.pop():self.pos() + len(self.get_starttag_text())])
    def handle_startendtag(self, tag, attrs):
        if self.depth == 0: self.parts.append(self.text[self.pos():self.pos() + len(self.get_starttag_text())])
    def handle_endtag(self, tag):
        if tag in VOID: return
        self.depth -= 1
        if self.depth == 0:
            end = self.text.index('>', self.pos()) + 1
            self.parts.append(self.text[self.starts.pop():end])

CHART_DEMO = read('web/docs.js')
m = re.search(r'function renderCharts\(\) \{(.*?)\n  \}\n', CHART_DEMO, re.S)
CHART_DEMO = ('document.addEventListener("DOMContentLoaded",function(){var $$=function(s){return Array.prototype.slice.call(document.querySelectorAll(s));};'
              + m.group(1) + '\n});document.addEventListener("odsv:theme",function(){if(window.ODSVCharts)window.ODSVCharts.redraw();});') if m else ''

BLOCKY = re.compile(r'odsv-(table|chart|grid|accordion|topbar|sheet|stack|footer|app|sidebar|progress|tabs|checklist|section|container|field|fieldset|callout|stage|kpi|card|step|facts|list|hgroup|signet-card)\b')

def frame(cid, n, ex, comp):
    h = ex['html']; caps = [c for c in ex.get('captions', []) if c]
    cls = 'sbf-stage'
    if caps:
        parts = TopSplit(h).parts
        if len(parts) == len(caps):
            h = ''.join(f'<figure class="sbf-state">{p}<figcaption>{esc(c)}</figcaption></figure>' for p, c in zip(parts, caps))
            cls += ' sbf-stage--states' + (' sbf-stage--wide' if any(len(BLOCKY.findall(p)) for p in parts) else '')
        else:
            caps = []
    if not caps and BLOCKY.search(h): cls += ' sbf-stage--block'
    demo = f'<script>{CHART_DEMO}</script>' if 'data-demo-chart' in h else ''
    title = f'{comp["name"]} – {ex["title"] or "Beispiel"}'
    write(f'frames/{cid}-{n}.html', f'''<!doctype html>
<html lang="de" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · ODSV</title>
<link rel="stylesheet" href="../assets/tokens.css">
<link rel="stylesheet" href="../assets/odsv.css">
<link rel="stylesheet" href="../assets/site.css">
<script src="../assets/odsv.js"></script>
<script>(function(){{var t=new URLSearchParams(location.search).get('theme');if(t==='light'||t==='dark')document.documentElement.setAttribute('data-theme',t);}})();</script>
<script src="../assets/odsv-charts.js" defer></script>
</head>
<body class="sbf">
{SPRITE}
<main class="{cls}">
{h}
</main>
{demo}
<script>(function(){{if(window.parent===window)return;function send(){{window.parent.postMessage({{sbHeight:document.documentElement.scrollHeight}},'*');}}
window.addEventListener('load',send);if(window.ResizeObserver)new ResizeObserver(send).observe(document.body);document.addEventListener('odsv:change',function(){{setTimeout(send,350);}});}})();</script>
</body>
</html>
''')

def story(cid, n, ex):
    sid = f'{cid}-{n}'
    title = ex['title'] or BY_ID[cid]['name']
    seg_theme = ('<div class="odsv-segmented odsv-segmented--sm odsv-segmented--inverse" role="radiogroup" aria-label="Theme der Vorschau" data-odsv-segmented data-sb-ctl="theme">'
                 '<button class="odsv-segmented__item" type="button" role="radio" aria-checked="true" data-value="dark">Dunkel</button>'
                 '<button class="odsv-segmented__item" type="button" role="radio" aria-checked="false" data-value="light">Hell</button></div>')
    seg_vp = ('<div class="odsv-segmented odsv-segmented--sm odsv-segmented--inverse" role="radiogroup" aria-label="Breite der Vorschau" data-odsv-segmented data-sb-ctl="vp">'
              '<button class="odsv-segmented__item" type="button" role="radio" aria-checked="false" data-value="390">390</button>'
              '<button class="odsv-segmented__item" type="button" role="radio" aria-checked="false" data-value="768">768</button>'
              '<button class="odsv-segmented__item" type="button" role="radio" aria-checked="true" data-value="full">Voll</button></div>')
    return f'''<article class="sb-story" id="story-{sid}" data-src="{{P}}frames/{sid}.html">
<div class="sb-story__bar"><h3 class="sb-story__title">{esc(title)}</h3>
<div class="sb-story__ctl">{seg_theme}{seg_vp}
<a class="odsv-icon-btn" data-sb-open href="{{P}}frames/{sid}.html" target="_blank" rel="noopener" aria-label="Story „{esc(title)}“ isoliert öffnen">{icon('external')}</a></div></div>
<div class="sb-canvas" data-vp="full"><iframe class="sb-canvas__frame" title="Vorschau: {esc(title)}" loading="lazy"></iframe></div>
<div class="sb-code__bar"><button class="odsv-textbtn" type="button" data-sb-code aria-expanded="false" aria-controls="code-{sid}">Code anzeigen</button>
<button class="odsv-btn odsv-btn--ghost odsv-btn--sm" type="button" data-sb-copy-from="#src-{sid}">{icon('copy')}HTML kopieren</button></div>
<div class="sb-code" id="code-{sid}" hidden><pre class="sb-pre" tabindex="0"><code id="src-{sid}">{esc(ex['html'])}</code></pre></div>
</article>'''

# ---------------------------------------------------------------- Komponentenseiten
def kv_table(caption, d, h1, h2):
    return table(caption, [h1, h2], [[f'<code class="odsv-code-inline">{esc(k)}</code>', inline(v)] for k, v in d.items()])

def comp_page(c):
    cid = c['id']
    for n, ex in enumerate(c['examples'], 1): frame(cid, n, ex, c)
    body = [head(GROUP_OF.get(cid, 'Komponente'), c['name'], inline(c['use']))]
    if c['examples']:
        body.append('<section class="sb-section" aria-labelledby="h-storys"><h2 class="odsv-h3" id="h-storys">Storys</h2><div class="sb-stories">'
                    + ''.join(story(cid, n, ex) for n, ex in enumerate(c['examples'], 1)) + '</div></section>')
    body.append(section('Einsatz', f'<div class="sb-do"><div class="sb-do__item sb-do__item--yes"><p class="odsv-label">{icon("check")}Verwenden für</p><p class="odsv-body-small">{inline(c["use"])}</p></div>'
                                   f'<div class="sb-do__item sb-do__item--no"><p class="odsv-label">{icon("close")}Nicht verwenden für</p><p class="odsv-body-small">{inline(c["avoid"])}</p></div></div>'))
    two = []
    if c.get('variants'): two.append(section('Varianten', kv_table(f'Varianten von {c["name"]}', c['variants'], 'Variante', 'Bedeutung')))
    if c.get('states'): two.append(section('Zustände', kv_table(f'Zustände von {c["name"]}', c['states'], 'Zustand', 'Bedeutung')))
    if two: body.append('<div class="sb-two">' + ''.join(two) + '</div>')
    two = []
    if c.get('rules'): two.append(section('Regeln', ul(c['rules'])))
    if c.get('a11y'): two.append(section('Barrierefreiheit', ul(c['a11y'])))
    if two: body.append('<div class="sb-two">' + ''.join(two) + '</div>')
    if c.get('content_limits'): body.append(section('Inhaltsgrenzen', kv_table(f'Inhaltsgrenzen von {c["name"]}', c['content_limits'], 'Element', 'Grenze')))
    if c.get('js'): body.append(section('Verhalten', f'<p class="odsv-body">{inline(c["js"])}</p>'))
    if c.get('classes'):
        body.append(section('Klassen', '<div class="sb-classes">' + ''.join(
            f'<button class="sb-chip" type="button" data-sb-copy="{esc(k)}" data-sb-copy-label="Klasse" aria-label="Klasse {esc(k)} kopieren">.{esc(k)}</button>' for k in c['classes']) + '</div>'))
    page(f'komponenten/{cid}.html', c['name'], '\n'.join(body), f'c-{cid}', ('Komponenten', GROUP_OF.get(cid, '')), c['use'])

# ---------------------------------------------------------------- Farben
def hex_of(v, theme, depth=0):
    if isinstance(v, str) and v.startswith('{') and depth < 20:
        key = '--odsv-' + v[1:-1].replace('.', '-')
        t = FLAT.get(key, {})
        return hex_of(t.get(theme, t.get('dark')), theme, depth + 1)
    return v

def rgba(hx):
    hx = hx.lstrip('#')
    if len(hx) in (3, 4): hx = ''.join(ch * 2 for ch in hx)
    r, g, b = (int(hx[i:i + 2], 16) for i in (0, 2, 4)); a = int(hx[6:8], 16) / 255 if len(hx) == 8 else 1
    return r, g, b, a

def over(fg, bg):
    r, g, b, a = rgba(fg); R, G, B, _ = rgba(bg)
    return '#%02x%02x%02x' % tuple(round(x * a + y * (1 - a)) for x, y in ((r, R), (g, G), (b, B)))

def lum(hx):
    def ch(c):
        c /= 255; return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b, _ = rgba(hx); return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)

def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True); return (la + 0.05) / (lb + 0.05)

COLOR_GROUPS = [('color.bg', 'Grund'), ('color.surface', 'Flächen'), ('color.border', 'Ränder'), ('color.text', 'Text'),
                ('color.accent', 'Akzent'), ('color.action', 'Aktionen'), ('color.status', 'Status'), ('color.focus', 'Fokus'),
                ('color.progress', 'Fortschritt'), ('color.signet', 'Signet'), ('color.lineart', 'Line-Art'), ('dataviz', 'Diagramme')]

def colors_page():
    out = [head('Grundlagen', 'Farben', 'Jede Rolle mit Wert im dunklen und hellen Theme. Klick auf eine Farbe kopiert die CSS-Variable.')]
    out.append('<p class="odsv-body sb-lead">Linke Hälfte dunkles Theme, rechte Hälfte helles Theme. Transparente Werte stehen auf dem jeweiligen Seitengrund. Bei Textfarben steht das Kontrastverhältnis zum Seitengrund (<code class="odsv-code-inline">--odsv-color-bg-base</code>) dabei; AA verlangt 4,5:1.</p>')
    bg = {t: hex_of(FLAT['--odsv-color-bg-base'][t], t) for t in ('dark', 'light')}
    for prefix, label in COLOR_GROUPS:
        items = [(k, v) for k, v in FLAT.items() if v['type'] == 'color' and (v['path'] == prefix or v['path'].startswith(prefix + '.'))]
        if not items: continue
        cards = []
        for k, v in items:
            dv, lv = hex_of(v['dark'], 'dark'), hex_of(v.get('light', v['dark']), 'light')
            chips = ''
            for th, val in (('dark', dv), ('light', lv)):
                solid = over(val, bg[th]); ink = '#000000' if lum(solid) > 0.4 else '#FFFFFF'
                chips += f'<span class="sb-swatch__chip" style="background:linear-gradient({val},{val}),{bg[th]};color:{ink}">{"Dunkel" if th == "dark" else "Hell"}</span>'
            alias = v['dark'] if str(v['dark']).startswith('{') else ''
            vals = f'{esc(dv)} · {esc(lv)}' + (f'<br>→ {esc(alias[1:-1])}' if alias else '')
            badges = ''
            if prefix == 'color.text' and 'link' not in k:
                for th, val in (('dark', dv), ('light', lv)):
                    r = ratio(over(val, bg[th]), bg[th]); ok = r >= 4.5
                    badges += (f'<span class="odsv-badge odsv-badge--{"success" if ok else "warning"}">{icon("check" if ok else "warning")}'
                               f'{"Dunkel" if th == "dark" else "Hell"} {r:.1f}:1'.replace('.', ',') + '</span>')
            cards.append(f'<button class="sb-swatch" type="button" data-sb-copy="var({k})" data-sb-copy-label="Variable">'
                         f'<span class="sb-swatch__chips" aria-hidden="true">{chips}</span><span class="sb-swatch__body">'
                         f'<span class="sb-swatch__name">{esc(k)}</span><span class="sb-swatch__val">{vals}</span>'
                         f'<span class="sb-swatch__desc">{esc(v.get("description", ""))}</span>'
                         + (f'<span class="sb-swatch__ratio">{badges}</span>' if badges else '') + '</span></button>')
        out.append(section(label, f'<div class="sb-swatches">{"".join(cards)}</div>', slug(label)))
    page('grundlagen/farben.html', 'Farben', '\n'.join(out), 'f-farben', ('Grundlagen',))

# ---------------------------------------------------------------- Typografie
def typo_page():
    out = [head('Grundlagen', 'Typografie', 'Systemschriften, feste Größenstufen und gesperrte Versalien nur per Stil.')]
    fam = ''.join(f'<li><strong>{n}</strong>: <code class="odsv-code-inline">{esc(", ".join(FLAT[f"--odsv-font-family-{n}"]["dark"]))}</code></li>' for n in ('display', 'text', 'mono'))
    out.append(section('Schriften', f'<p class="odsv-body">Es wird keine Schrift ausgeliefert. Die Stapel nehmen die Systemschrift des Geräts.</p><ul class="odsv-list">{fam}</ul>'))
    samples = {'display': 'Kennzahlen', 'headline': 'Laufzeit', 'title': 'Akku und Laufzeit', 'subtitle': 'Alle Werte beziehen sich auf das dritte Quartal.',
               'body': 'Erst danach folgt Fließtext in normaler Schreibweise, höchstens 640 Pixel breit.', 'body-small': 'Erklärtext in Karten und Tabellen.',
               'small': 'Quelle: Beispieldaten · Stand 17.11.2026', 'caption': 'Stand 17.11.2026', 'eyebrow': 'Quartalsbericht', 'label': 'E-Mail-Adresse',
               'chip': 'Neu', 'kpi': '1.284', 'kpi-small': '98 %', 'number': '07', 'button': 'Projekt starten', 'button-small': 'Bericht öffnen',
               'wordmark': 'Produktname', 'code': 'odsv-btn--primary'}
    rows = []
    for key, sample in samples.items():
        t = FLAT.get(f'--odsv-text-{key}')
        if not t: continue
        v = t['dark']
        def r(x):
            """Alias wie {font.size.display} in einen lesbaren Wert auflösen (rem → px, clamp → Spanne)."""
            x = str(x)
            if x.startswith('{'): x = str(FLAT.get('--odsv-' + x[1:-1].replace('.', '-'), {}).get('dark', x))
            m = re.match(r'clamp\(([\d.]+)rem,.*,\s*([\d.]+)rem\)', x)
            if m: return f'fluid {float(m.group(1)) * 16:g}–{float(m.group(2)) * 16:g} px'.replace('.', ',')
            m = re.fullmatch(r'([\d.]+)rem', x)
            if m: return f'{float(m.group(1)) * 16:g} px'.replace('.', ',')
            return x.replace('.', ',') if re.fullmatch(r'-?[\d.]+(em)?', x) else x
        style = ';'.join(f'{p}:var(--odsv-text-{key}-{s})' for p, s in (('font-family', 'family'), ('font-size', 'size'), ('font-weight', 'weight'),
                                                                         ('letter-spacing', 'tracking'), ('line-height', 'leading'), ('text-transform', 'transform')))
        rows.append(f'<div class="sb-type__row"><p class="sb-type__sample" style="{style}">{esc(sample)}</p>'
                    f'<div class="sb-type__meta"><code>text.{esc(key)}</code><span>{esc(r(v["fontSize"]))} · {esc(r(v["fontWeight"]))}</span>'
                    f'<span>Laufweite {esc(r(v["letterSpacing"]))} · Zeile {esc(r(v["lineHeight"]))}</span></div></div>')
    out.append(section('Stile', f'<div class="sb-type">{"".join(rows)}</div>'))
    sizes = [(k, v) for k, v in FLAT.items() if k.startswith('--odsv-font-size-')]
    def rem_px(x):
        m = re.fullmatch(r'([\d.]+)rem', str(x)); return f'{float(m.group(1)) * 16:g}'.replace('.', ',') + ' px' if m else 'fluid'
    out.append(section('Größenstufen', table('Schriftgrößen', ['Variable', 'Wert', 'Pixel'], [[f'<code class="odsv-code-inline">{esc(k)}</code>', esc(v['dark']),
                       esc(rem_px(v['dark']))] for k, v in sizes], num=(2,))))
    ch = next((c for c in CHAPTERS if c['num'] == 4), None)
    if ch:
        m3 = re.search(r'### 4\.3.*?(?=\n### |\Z)', ch['body'], re.S)
        if m3: out.append(f'<div class="sb-md">{markdown(m3.group(0))}</div>')
    page('grundlagen/typografie.html', 'Typografie', '\n'.join(out), 'f-typografie', ('Grundlagen',))

# ---------------------------------------------------------------- Raster und Maße
def px(v):
    m = re.fullmatch(r'([\d.]+)px', str(v)); return float(m.group(1)) if m else None

def scale_rows(prefix, bar=True):
    rows = []
    for k, v in FLAT.items():
        if not k.startswith(prefix): continue
        val = v['dark']; p = px(val)
        b = f'<span class="sb-scale__bar" style="width:var({k})"></span>' if bar and p is not None and p <= 960 else '<span></span>'
        rows.append(f'<div class="sb-scale__row"><code>{esc(k)}</code><span class="sb-scale__val">{esc(val)}</span>{b}</div>')
    return '<div class="sb-scale">' + ''.join(rows) + '</div>'

def list_table(prefix, caption):
    return table(caption, ['Variable', 'Wert', 'Einsatz'], [[f'<code class="odsv-code-inline">{esc(k)}</code>', esc(v['dark'] if not isinstance(v['dark'], (list, dict)) else json.dumps(v['dark'])),
                 esc(v.get('description', ''))] for k, v in FLAT.items() if k.startswith(prefix)])

def raster_page():
    out = [head('Grundlagen', 'Raster und Maße', '4er-Abstandsskala, große Radien und feste Bediengrößen.')]
    out.append(section('Abstände', scale_rows('--odsv-space-')))
    radii = ''.join(f'<div class="sb-radius"><div class="sb-radius__box" style="border-radius:var({k})"></div><code>{esc(k)}</code><span class="sb-scale__val">{esc(v["dark"])} · {esc(v.get("description", ""))}</span></div>'
                    for k, v in FLAT.items() if k.startswith('--odsv-radius-'))
    out.append(section('Radien', f'<div class="sb-radii">{radii}</div>'))
    out.append(section('Layout', list_table('--odsv-layout-', 'Layout-Maße')))
    out.append(section('Größen', list_table('--odsv-size-', 'Bedien- und Elementgrößen')))
    out.append(section('Rand- und Strichstärken', list_table('--odsv-border-', 'Rand- und Strichstärken')))
    page('grundlagen/raster.html', 'Raster und Maße', '\n'.join(out), 'f-raster', ('Grundlagen',))

def effekte_page():
    out = [head('Grundlagen', 'Effekte und Bewegung', 'Tiefe entsteht über Flächen, nicht über Schatten. Bewegung erklärt einen Wechsel und endet.')]
    sh = ''.join(f'<div class="sb-shadow"><div class="sb-shadow__box" style="box-shadow:var({k})"></div><code class="odsv-code-inline">{esc(k)}</code><span class="sb-scale__val">{esc(v.get("description", ""))}</span></div>'
                 for k, v in FLAT.items() if k.startswith('--odsv-shadow-'))
    out.append(section('Schatten', f'<p class="odsv-body">Nur für Überlagerungen und Leuchtsäume. Karten haben keinen Schatten.</p><div class="sb-shadows">{sh}</div>'))
    def mv(v):
        d = v['dark']; return f'cubic-bezier({", ".join(str(x) for x in d)})' if isinstance(d, list) else str(d)
    out.append(section('Bewegung', table('Bewegungs-Tokens', ['Variable', 'Wert', 'Einsatz'], [[f'<code class="odsv-code-inline">{esc(k)}</code>', esc(mv(v)), esc(v.get('description', ''))]
                       for k, v in FLAT.items() if k.startswith('--odsv-motion-')])
                       + '<p class="odsv-small odsv-muted">Bei <code class="odsv-code-inline">prefers-reduced-motion: reduce</code> setzt <code class="odsv-code-inline">tokens.css</code> alle Dauern auf 0,01 ms.</p>'))
    out.append(section('Deckkraft und Unschärfe', list_table('--odsv-opacity-', 'Deckkraft') + list_table('--odsv-blur-', 'Unschärfe')))
    out.append(section('Ebenen (z-index)', list_table('--odsv-z-', 'Ebenen')))
    out.append(section('Breakpoints', list_table('--odsv-breakpoint-', 'Breakpoints') + '<p class="odsv-small odsv-muted">Media Queries können kein <code class="odsv-code-inline">var()</code>; im CSS stehen 600 / 768 / 1024 / 1280 px.</p>'))
    page('grundlagen/effekte.html', 'Effekte und Bewegung', '\n'.join(out), 'f-effekte', ('Grundlagen',))

def icons_page():
    btns = ''.join(f'<button class="sb-icon" type="button" data-sb-copy="&lt;svg class=&quot;odsv-icon&quot; aria-hidden=&quot;true&quot;&gt;&lt;use href=&quot;#odsv-icon-{n}&quot;/&gt;&lt;/svg&gt;" data-sb-copy-label="Snippet" aria-label="Snippet für Icon {esc(n)} kopieren">{icon(n)}<span>{esc(n)}</span></button>' for n in ICON_NAMES)
    out = [head('Grundlagen', 'Icons', 'Strich-Icons im 24-px-Raster, 2 px Strich, runde Enden. Klick kopiert das Snippet.'),
           f'<div class="sb-icons">{btns}</div>',
           section('Einsatz', ul(['Größen: 18 px in Buttons, 22 px als Icon-Button und in der Navigation, 44–52 px in Kacheln mit 2,4 px Strich.',
                                  'Farbe über `currentColor`; ein Icon steht nie allein für eine Handlung ohne Namen.',
                                  'Sprite einbinden: Inhalt von `assets/icons.svg` in den `body` kopieren (über `file://` blockiert der Browser externe `<use>`-Verweise).']))]
    page('grundlagen/icons.html', 'Icons', '\n'.join(out), 'f-icons', ('Grundlagen',))

def signets_page():
    groups = {}
    for s in SIGNETS: groups.setdefault(s['group'], []).append(s)
    out = [head('Grundlagen', 'Signets', 'Basis-Signet, acht Themen und acht Situationen aus derselben Grammatik.')]
    for g, items in groups.items():
        cards = ''.join(f'<li><div class="odsv-signet-card"><svg class="odsv-signet-card__svg" viewBox="0 0 400 400" preserveAspectRatio="xMaxYMid slice" role="img" aria-label="Signet {esc(s["name"])}"><use href="#{s["id"]}"/></svg>'
                        f'<p class="odsv-wordmark">{esc(s["name"])}</p></div><p class="odsv-body-small">{esc(s["meaning"])}</p>'
                        f'<p class="odsv-small"><code class="odsv-code-inline">#{esc(s["id"])}</code> · <a class="odsv-link" href="{{P}}assets/signets/{esc(s["id"])}.svg" download>SVG laden</a></p></li>' for s in items)
        out.append(section(g, f'<ul class="sb-signets" role="list">{cards}</ul>', slug(g)))
    ch = next((c for c in CHAPTERS if c['num'] == 10), None)
    if ch:
        m6 = re.search(r'\*\*Einsatz\*\*.*?(?=\n### |\Z)', ch['body'], re.S)
        if m6: out.append(f'<div class="sb-md">{markdown(m6.group(0))}</div>')
    page('grundlagen/signets.html', 'Signets', '\n'.join(out), 'f-signets', ('Grundlagen',))

# ---------------------------------------------------------------- Richtlinien
def guideline_pages():
    lst = ''.join(f'<li><a class="odsv-link" href="{{P}}richtlinien/{c["slug"]}.html">{c["num"]}. {esc(c["title"])}</a></li>' for c in CHAPTERS)
    intro = markdown(SPEC_INTRO.split('\n', 1)[1] if SPEC_INTRO.startswith('#') else SPEC_INTRO)
    page('richtlinien/index.html', 'Richtlinien', head('Richtlinien', 'Spezifikation', f'ODSV {esc(VERSION)} in {len(CHAPTERS)} Kapiteln. Werte stehen in den Tokens, hier stehen die Regeln.')
         + f'<div class="sb-md">{intro}</div>' + section('Kapitel', f'<ol class="odsv-list">{lst}</ol>'), 'r-index', ('Richtlinien',))
    for i, c in enumerate(CHAPTERS):
        toc = []; body = markdown(c['body'], toc)
        tochtml = ('<nav class="sb-toc" aria-label="Abschnitte"><p class="odsv-eyebrow">Auf dieser Seite</p><ul>'
                   + ''.join(f'<li><a href="#{h}">{esc(t)}</a></li>' for h, t in toc) + '</ul></nav>') if len(toc) > 1 else ''
        prev = f'<a class="odsv-btn odsv-btn--ghost odsv-btn--sm" href="{{P}}richtlinien/{CHAPTERS[i - 1]["slug"]}.html">← {esc(CHAPTERS[i - 1]["title"])}</a>' if i else '<span></span>'
        nxt = f'<a class="odsv-btn odsv-btn--ghost odsv-btn--sm" href="{{P}}richtlinien/{CHAPTERS[i + 1]["slug"]}.html">{esc(CHAPTERS[i + 1]["title"])} →</a>' if i + 1 < len(CHAPTERS) else ''
        page(f'richtlinien/{c["slug"]}.html', c['title'],
             head(f'Kapitel {c["num"]}', c['title'], f'Aus der ODSV-Spezifikation {esc(VERSION)}.') + tochtml + f'<div class="sb-md">{body}</div><nav class="sb-pager" aria-label="Kapitel blättern">{prev}{nxt}</nav>',
             f'r-{c["slug"]}', ('Richtlinien',))
    agents = read('AGENTS.md'); agents = agents.split('\n', 1)[1] if agents.startswith('#') else agents
    toc = []; body = markdown(agents, toc)
    page('richtlinien/agents.html', 'Für AI-Agents', head('Richtlinien', 'Für AI-Agents', 'Entscheidungsbaum, Muss-Regeln, Ablauf und Definition of Done für Agents, die mit ODSV bauen.')
         + f'<div class="sb-md">{body}</div>', 'r-agents', ('Richtlinien',))

# ---------------------------------------------------------------- Präsentationen, Downloads, Start
def pptx_page():
    rows = [[esc(L['name']), f'<code class="odsv-code-inline">{esc(L["spec_id"])}</code>', esc(L['use']), 'ja' if L.get('progress') else '–', 'ja' if L.get('footer') else '–'] for L in LAYOUTS['layouts']]
    img = '<img class="sb-img" src="{P}assets/pptx-overview.png" alt="Übersicht aller Folienlayouts der ODSV-Vorlage" loading="lazy">' if os.path.exists(src('pptx/_preview/overview.png')) else ''
    code = '''import sys; sys.path.insert(0, 'pptx'); from odsv_pptx import Deck
d = Deck()
d.slide('Titel', eyebrow='Bericht · Q3 2026', title='Kennzahlen', sub='Was im dritten Quartal zählt.')
assert not d.check(), d.check()
d.save('out.pptx')'''
    out = [head('Medien', 'Präsentationen', f'PowerPoint-Vorlage 16:9 mit {len(LAYOUTS["layouts"])} Layouts, nur dunkel.'), img,
           section('Layouts', table('Folienlayouts', ['Layout', 'ID', 'Zweck', 'Leiste', 'Fuß'], rows)),
           section('Mit Python bauen', f'<p class="odsv-body">Der Helfer <code class="odsv-code-inline">pptx/odsv_pptx.py</code> füllt die Platzhalter nach Rollen und prüft Zeichengrenzen.</p><div class="sb-md"><pre tabindex="0"><code>{esc(code)}</code></pre></div>'),
           '<p><a class="odsv-btn odsv-btn--primary" href="{P}assets/ODSV-Vorlage.potx" download>Vorlage herunterladen</a></p>']
    page('praesentationen.html', 'Präsentationen', '\n'.join(out), 'pptx', ('Medien',))

DOWNLOADS = [('tokens.css', 'web/tokens.css', 'Alle Tokens als CSS-Variablen, dunkel und hell'), ('odsv.css', 'web/odsv.css', 'Komponentenbibliothek'),
             ('odsv.js', 'web/odsv.js', 'Verhalten: Theme, Umschalter, Tabs, Checkliste, Sheet'), ('odsv-charts.js', 'web/odsv-charts.js', 'Diagramme als SVG: Linie, Balken, Donut, Sparkline'),
             ('icons.svg', 'web/icons.svg', 'Sprite mit Icons und Signets'), ('tokens.json', 'tokens/tokens.json', 'Quelle der Tokens (DTCG)'),
             ('components.json', 'catalog/components.json', 'Komponentenkatalog maschinenlesbar'), ('ODSV-Vorlage.potx', 'pptx/ODSV-Vorlage.potx', 'PowerPoint-Vorlage')]

def size_de(n):
    return f'{n / 1024:.0f} KB'.replace('.', ',') if n < 1024 * 1024 else f'{n / 1048576:.1f} MB'.replace('.', ',')

def downloads_page():
    items = ''.join(f'<li><div><strong>{esc(name)}</strong><span>{esc(desc)} · {size_de(os.path.getsize(src(path)))}</span></div>'
                    f'<a class="odsv-btn odsv-btn--ghost odsv-btn--sm" href="{{P}}assets/{esc(name)}" download>{icon("download")}Laden</a></li>' for name, path, desc in DOWNLOADS if os.path.exists(src(path)))
    snippet = '''<html lang="de" data-theme="dark">
<head>
  <link rel="stylesheet" href="tokens.css">
  <link rel="stylesheet" href="odsv.css">
  <script src="odsv.js"></script>            <!-- im head, ohne defer -->
  <script src="odsv-charts.js" defer></script>
</head>'''
    out = [head('Start', 'Downloads', 'Alles, was ein Projekt zum Einbinden braucht.'), f'<ul class="sb-files">{items}</ul>',
           section('Einbinden', f'<div class="sb-md"><pre tabindex="0"><code>{esc(snippet)}</code></pre></div>')]
    page('downloads.html', 'Downloads', '\n'.join(out), 'downloads', ('Start',))

def index_page():
    n_ex = sum(len(c['examples']) for c in COMPS)
    cards = [('grundlagen/farben.html', str(sum(1 for v in FLAT.values() if v['type'] == 'color')), 'Farb-Tokens', 'Rollen für Grund, Text, Akzent, Status und Diagramme in zwei Themes.'),
             ('komponenten/button.html', str(len(COMPS)), 'Komponenten', f'{n_ex} Storys mit Vorschau, Code und Regeln.'),
             ('grundlagen/icons.html', str(len(ICON_NAMES)), 'Icons', 'Strich-Icons im 24-px-Raster als Sprite.'),
             ('grundlagen/signets.html', str(len(SIGNETS)), 'Signets', 'Basis, Themen und Situationen einer Familie.'),
             ('praesentationen.html', str(len(LAYOUTS['layouts'])), 'Folienlayouts', 'PowerPoint-Vorlage mit Python-Helfer.'),
             ('richtlinien/index.html', str(len(CHAPTERS)), 'Kapitel Spezifikation', 'Ton, Farbe, Typografie, Raster, Diagramme, Barrierefreiheit.')]
    cardhtml = ''.join(f'<a class="sb-cardlink" href="{{P}}{h}"><span class="sb-cardlink__num">{n}</span><span class="sb-cardlink__title">{esc(t)}</span><span class="sb-cardlink__text">{esc(d)}</span></a>' for h, n, t, d in cards)
    principles = ['**Schwarz ist die Bühne.** Tiefe über Flächenstufen, nie über Schatten.', '**Ein Akzent, eine Bedeutung.** Gelb heißt „hier handeln“ oder „hier schauen“.',
                  '**Dreiklang.** Eyebrow, Versalien-Headline, grauer Zweitsatz.', '**Linie statt Fläche.** Icons und Illustrationen sind Strichzeichnungen.',
                  '**Fortschritt ist sichtbar.** Segmentierte Leiste, Schrittnummer, Zähler.', '**Ehrlich vor elegant.** Warnungen, Grenzen und Quellen stehen sichtbar da.']
    hero = (f'<section class="sb-hero"><header class="odsv-hgroup"><p class="odsv-eyebrow">OneDay Super Visuals · Design-System · Version {esc(VERSION)}</p>'
            f'<h1 class="odsv-display">ODSV</h1><p class="odsv-sub">Dunkel, gesperrte Versalien, ein gelber Akzent – für Websites, Dashboards und Präsentationen.</p>'
            f'<div class="odsv-cluster"><a class="odsv-btn odsv-btn--primary" href="{{P}}komponenten/button.html">Komponenten ansehen</a>'
            f'<a class="odsv-btn odsv-btn--ghost" href="{{P}}downloads.html">{icon("download")}Dateien laden</a></div></header>'
            f'<div class="odsv-signet-card"><svg class="odsv-signet-card__svg" viewBox="0 0 400 400" preserveAspectRatio="xMaxYMid slice" role="img" aria-label="ODSV-Signet: vier Bögen um einen gelben Punkt"><use href="#odsv-signet"/></svg><p class="odsv-wordmark">ODSV<br>Design-System</p></div></section>')
    out = [hero, f'<div class="sb-cards">{cardhtml}</div>', section('Prinzipien', ul(principles)),
           section('So arbeitest du mit der Seite', ul(['Links die Navigation, Taste `/` springt in die Suche.', 'Jede Komponente zeigt ihre Storys live. Je Story lassen sich Theme und Breite (390, 768, voll) umschalten, der Code ist darunter kopierbar.',
                                                      'Das Theme oben rechts gilt für die Seite und alle Storys, die du nicht einzeln umgestellt hast.', 'Der Pfeil-Knopf öffnet eine Story isoliert in einem neuen Tab, gut zum Teilen eines einzelnen Zustands.']))]
    page('index.html', 'Einführung', '\n'.join(out), 'index', (), 'ODSV Design-System: Komponenten, Tokens, Icons, Signets und Richtlinien.')

# ---------------------------------------------------------------- Ablauf
def copy_assets():
    a = os.path.join(OUT, 'assets'); os.makedirs(os.path.join(a, 'signets'), exist_ok=True)
    for name, path, _ in DOWNLOADS:
        if os.path.exists(src(path)): shutil.copyfile(src(path), os.path.join(a, name))
    for f in ('site.css', 'site.js'): shutil.copyfile(src('tools/site', f), os.path.join(a, f))
    for f in os.listdir(src('web/signets')):
        if f.endswith('.svg'): shutil.copyfile(src('web/signets', f), os.path.join(a, 'signets', f))
    if os.path.exists(src('pptx/_preview/overview.png')): shutil.copyfile(src('pptx/_preview/overview.png'), os.path.join(a, 'pptx-overview.png'))
    write('.nojekyll', '')

def main():
    global OUT
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0]); ap.add_argument('--out', default='site'); args = ap.parse_args()
    OUT = os.path.join(ROOT, args.out) if not os.path.isabs(args.out) else args.out
    if os.path.isdir(OUT):
        if not os.path.exists(os.path.join(OUT, '.nojekyll')) and os.listdir(OUT):
            sys.exit(f'{OUT} existiert und ist kein von build_site.py erzeugter Ordner – abgebrochen.')
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    copy_assets()
    index_page(); downloads_page()
    colors_page(); typo_page(); raster_page(); effekte_page(); icons_page(); signets_page()
    for c in COMPS: comp_page(c)
    guideline_pages(); pptx_page()
    n = sum(len(fs) for _, _, fs in os.walk(OUT))
    print(f'Website: {os.path.relpath(OUT, ROOT)}/ · {len(COMPS)} Komponenten, {sum(len(c["examples"]) for c in COMPS)} Storys, {len(CHAPTERS)} Kapitel, {n} Dateien')

if __name__ == '__main__':
    main()
