#!/usr/bin/env python3
"""ODSV-Prüfung: JSON gültig · CSS-Variablen <-> tokens.json · WCAG-Kontraste · pptx.json stimmig.
Aufruf: python3 tools/check_tokens.py [--md]   (Exit 1 bei Fehler)"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_tokens as B

ROOT = B.ROOT
tok = json.load(open(os.path.join(ROOT, 'tokens.json'), encoding='utf-8'))
ppt = json.load(open(os.path.join(ROOT, 'pptx.json'), encoding='utf-8'))
css = open(os.path.join(ROOT, 'tokens.css'), encoding='utf-8').read()
errors = []


def get(path, theme='dark'):
    """Tokenwert mit Theme-Overrides (print erbt von light) und aufgelösten Aliassen"""
    chain = {'dark': [tok], 'light': [tok['theme']['light'], tok], 'print': [tok['theme']['print'], tok['theme']['light'], tok]}[theme]
    for root in chain:
        n = root
        try:
            for k in path.split('.'):
                n = n[k]
            v = n['$value']
        except (KeyError, TypeError):
            continue
        return get(v[1:-1], theme) if isinstance(v, str) and v.startswith('{') else v
    raise KeyError(path)


def rgba(h):
    h = h.lstrip('#')
    return [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)] + [int(h[6:8], 16) / 255 if len(h) == 8 else 1.0]


def over(fg, bg):
    """fg (ggf. transparent) über deckendem bg"""
    f, b = rgba(fg), rgba(bg)
    return '#%02X%02X%02X' % tuple(round((f[i] * f[3] + b[i] * (1 - f[3])) * 255) for i in range(3))


def lum(h):
    lin = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b, _ = rgba(h)
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def ratio(a, b):
    x, y = sorted([lum(a), lum(b)], reverse=True)
    return (x + 0.05) / (y + 0.05)


# ---------- 1. CSS <-> JSON ----------
base = {k: v for k, v in tok.items() if k != 'theme'}
names = {n for p, t in B.walk(base) for n, _ in B.decls(p, t)}
for th in ('light', 'print'):
    for p, t in B.walk(tok['theme'][th]):
        for n, _ in B.decls(p, t):
            if n not in names:
                errors.append('Theme %s überschreibt unbekanntes Token: %s' % (th, n))
in_css = set(re.findall(r'(--odsv-[a-z0-9-]+)', css))
for n in sorted(in_css - names):
    errors.append('CSS-Variable ohne Token in tokens.json: ' + n)
for n in sorted(names - in_css):
    errors.append('Token fehlt in tokens.css: ' + n)

# ---------- 2. Kontraste ----------
S = ['color.bg.base', 'color.surface.1', 'color.surface.2']
rows = []


def need(theme, fg, bgs, minimum, what, via=None):
    for bg in bgs:
        b = get(bg, theme)
        if len(b.lstrip('#')) == 8:
            b = over(b, get(via or 'color.surface.1', theme))
        f = over(get(fg, theme), b)
        r = ratio(f, b)
        ok = r >= minimum
        rows.append((theme, fg, bg, f, b, r, minimum, what, ok))
        if not ok:
            errors.append('Kontrast %s: %s auf %s = %.2f < %s (%s)' % (theme, fg, bg, r, minimum, what))


for th in ('dark', 'light'):
    for t in ('primary', 'body', 'secondary', 'muted', 'faint'):
        need(th, 'color.text.' + t, S, 4.5, 'Text')
    need(th, 'color.accent.text', S, 4.5, 'Akzent als Text')
    need(th, 'color.accent.line', S, 3, 'Akzent als Linie/Icon')
    need(th, 'color.border.control', S + ['color.surface.3'], 3, 'Rand Bedienelement')
    need(th, 'color.focus.ring', S, 3, 'Fokusring')
    need(th, 'color.focus.ring-on-accent', ['color.bg.base', 'color.surface.1'], 3, 'Fokusring um Akzentfläche')
    for k in ('bg', 'bg-end', 'hover', 'pressed'):
        need(th, 'color.action.primary.fg', ['color.action.primary.' + k], 4.5, 'Button primär')
        if k != 'bg-end':
            need(th, 'color.action.secondary.fg', ['color.action.secondary.' + k], 4.5, 'Button sekundär')
    need(th, 'color.action.ghost.fg', ['color.action.ghost.bg'], 4.5, 'Button ghost', via='color.bg.base')
    need(th, 'color.action.disabled.fg', ['color.action.disabled.bg'], 3, 'Button deaktiviert (freiwillig ≥ 3)')
    need(th, 'color.accent.on-tile', ['color.accent.tile-start', 'color.accent.tile-end'], 3, 'Icon auf gelber Kachel')
    for s in ('success', 'warning', 'danger', 'info'):
        need(th, 'color.status.%s.text' % s, S, 4.5, 'Status als Text')
        need(th, 'color.status.%s.base' % s, S, 3, 'Status als Icon/Fläche')
        need(th, 'color.status.%s.on' % s, ['color.status.%s.base' % s], 4.5, 'Text auf Statusfläche')
        need(th, 'color.text.body', ['color.status.%s.subtle' % s], 4.5, 'Fließtext im Callout')
        need(th, 'color.status.%s.text' % s, ['color.status.%s.subtle' % s], 4.5, 'Statuswort im Callout')
    need(th, 'color.progress.track', ['color.bg.base'], 3, 'Fortschritt: offenes Segment')
    need(th, 'color.progress.fill', ['color.progress.track-current'], 3, 'Fortschritt: Füllung auf Spur', via='color.bg.base')
    need(th, 'color.lineart.stroke', S, 3, 'Line-Art Hauptlinie')
    need(th, 'color.lineart.dim', S, 3, 'Line-Art Nebenlinie')
    need(th, 'color.lineart.on-marker', ['color.lineart.marker'], 4.5, 'Nummer auf Marke')
    for i in range(1, 8):
        need(th, 'dataviz.categorical.%d' % i, S[:2], 3, 'Diagrammfarbe')
    need(th, 'dataviz.neutral', S[:2], 3, 'Diagramm „Sonstige“')
    need(th, 'dataviz.sequential.1', S[:2], 2, 'Sequenziell, schwächste Stufe')
    need(th, 'dataviz.diverging.mid', S[:2], 2, 'Divergierend, Mitte')
    need(th, 'dataviz.axis-text', S[:2], 4.5, 'Achsentext')
need('print', 'color.text.body', ['color.bg.base'], 7, 'Druck Fließtext')
need('print', 'color.text.faint', ['color.bg.base'], 7, 'Druck Fußnote')
need('print', 'color.border.subtle', ['color.bg.base'], 3, 'Druck Kartenrand')

# inaktive Schritt-Karte: ganze Karte mit opacity.inactive über dem Grund
for th in ('dark', 'light'):
    a = get('opacity.inactive', th)
    al = '%02X' % round(a * 255)
    base_bg = get('color.bg.base', th)
    card = over(get('color.surface.1', th) + al, base_bg)
    for t in ('primary', 'body'):
        f = over(get('color.text.' + t, th) + al, card)
        r = ratio(f, card)
        rows.append((th, 'color.text.%s × opacity.inactive' % t, 'color.surface.1 × opacity.inactive', f, card, r, 4.5, 'Text in inaktiver Schritt-Karte', r >= 4.5))
        if r < 4.5:
            errors.append('Kontrast %s: Text %s in inaktiver Karte = %.2f < 4.5' % (th, t, r))

# ---------- 3. pptx.json ----------
E = ppt['units']['emuPerInch']
g, sl = ppt['grid'], ppt['slide']
if (sl['widthEmu'], sl['heightEmu']) != (12192000, 6858000):
    errors.append('pptx: Folienformat ist nicht 16:9 (12192000 × 6858000 EMU)')
if 2 * g['marginXEmu'] + 12 * g['columnWidthEmu'] + 11 * g['gutterEmu'] != sl['widthEmu']:
    errors.append('pptx: Ränder + Spalten + Lücken ergeben nicht die Folienbreite')
for c, v in g['columnX'].items():
    if abs(v['in'] * E - v['emu']) > 500:
        errors.append('pptx: columnX %s in/EMU weichen ab' % c)
for th, name in (('dark', 'dark'), ('light', 'light')):
    T = ppt['themes'][name]
    for i in range(1, 7):
        if T['colorScheme']['accent%d' % i] != get('dataviz.categorical.%d' % i, th).lstrip('#'):
            errors.append('pptx %s: accent%d ≠ dataviz.categorical.%d' % (name, i, i))
    for role, path in (('background', 'color.bg.base'), ('card', 'color.surface.1'), ('text.muted', 'color.text.muted'), ('accent.fill', 'color.accent.fill')):
        if T['roles'][role] != get(path, th).lstrip('#')[:6]:
            errors.append('pptx %s: Rolle %s ≠ %s' % (name, role, path))
for k, s in ppt['textStyles'].items():
    if s['spc'] != round(s['sizePt'] * s['trackingEm'] * 100):
        errors.append('pptx: spc von %s stimmt nicht' % k)
for l in ppt['layouts']:
    for k, p in l['placeholders'].items():
        if p['x'] < 0 or p['y'] < 0 or p['x'] + p['w'] > 13.334 or p['y'] + p['h'] > 7.501:
            errors.append('pptx: %s/%s liegt außerhalb der Folie' % (l['name'], k))
        if p.get('style') and p['style'] not in ppt['textStyles'] and p['style'] not in (
                'card', 'chart-frame', 'insight', 'image', 'lineart', 'segments', 'step-cards', 'grabber', 'kpi-tiles'):
            errors.append('pptx: unbekannter Stil %s in %s/%s' % (p['style'], l['name'], k))

# ---------- Ausgabe ----------
if '--md' in sys.argv:
    print('| Theme | Vordergrund | Hintergrund | Farben | Kontrast | Soll | Zweck |\n|---|---|---|---|---|---|---|')
    for th, fg, bg, f, b, r, m, what, ok in rows:
        print('| %s | `%s` | `%s` | %s auf %s | %s:1 | ≥ %s | %s%s |' % (th, fg, bg, f, b, ('%.2f' % r).replace('.', ','), m, what, '' if ok else ' – FEHLER'))
else:
    print('Tokens: %d · CSS-Variablen: %d · Kontrastprüfungen: %d (niedrigster Abstand zum Soll: %s)' % (
        len(names), len(in_css), len(rows), min(rows, key=lambda r: r[5] / r[6])[1:3]))
for e in errors:
    print('FEHLER:', e)
print('OK – alle Prüfungen bestanden' if not errors else '%d Fehler' % len(errors))
sys.exit(1 if errors else 0)
