#!/usr/bin/env python3
"""ODSV: erzeugt tokens/tokens.css aus tokens/tokens.json (einzige Quelle).
Aufruf: python3 tools/build_tokens.py   – ohne Abhängigkeiten."""
import json, os, re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tokens')
PREFIX = '--odsv-'
SUB = {'fontFamily': 'family', 'fontSize': 'size', 'fontWeight': 'weight',
       'letterSpacing': 'tracking', 'lineHeight': 'leading'}
REDUCED = {'instant', 'fast', 'base', 'slow', 'stage', 'camera', 'hint', 'stagger'}


def walk(node, path=()):
    """liefert (Pfad, Token) für alle Blätter"""
    for k, v in node.items():
        if k.startswith('$') or not isinstance(v, dict):
            continue
        if '$value' in v:
            yield path + (k,), v
        else:
            yield from walk(v, path + (k,))


def name(path):
    return PREFIX + '-'.join(path)


def ref(v):
    """{a.b.c} -> var(--odsv-a-b-c)"""
    if isinstance(v, str):
        return re.sub(r'\{([^}]+)\}', lambda m: 'var(%s)' % name(tuple(m.group(1).split('.'))), v)
    return v


def family(v):
    generic = {'sans-serif', 'serif', 'monospace', 'ui-monospace', '-apple-system', 'BlinkMacSystemFont'}
    return ', '.join(f if f in generic else '"%s"' % f for f in v)


def shadow(v):
    parts = v if isinstance(v, list) else [v]
    return ', '.join('%s %s %s %s %s' % (p['offsetX'], p['offsetY'], p['blur'], p['spread'], ref(p['color'])) for p in parts)


def decls(path, tok):
    """Token -> Liste (CSS-Name, Wert)"""
    t, v = tok.get('$type'), tok['$value']
    ext = tok.get('$extensions', {}).get('odsv', {})
    if t == 'typography':
        out = [(name(path + (SUB[k],)), ref(val)) for k, val in v.items()]
        out.append((name(path + ('transform',)), ext.get('textTransform', 'none')))
        return out
    if t == 'fontFamily':
        return [(name(path), family(v))]
    if t == 'cubicBezier':
        return [(name(path), 'cubic-bezier(%s)' % ', '.join('%g' % x for x in v))]
    if t == 'shadow':
        return [(name(path), shadow(v))]
    if t == 'gradient':
        stops = ', '.join('%s %g%%' % (ref(s['color']), s['position'] * 100) for s in v)
        return [(name(path), 'linear-gradient(%s, %s)' % (ext.get('angle', '180deg'), stops))]
    return [(name(path), ref(v) if isinstance(v, str) else '%g' % v)]


def dependents(base, overrides):
    """Alias-Variablen neu deklarieren, die (auch mittelbar) von überschriebenen Variablen abhängen.
    Nötig, weil var() dort aufgelöst wird, wo die Eigenschaft deklariert ist – sonst erbte ein
    helles Teilstück die dunkel aufgelösten Aliasse."""
    changed = {n for n, _ in overrides}
    out, grew = [], True
    while grew:
        grew = False
        for n, v in base:
            if n in changed:
                continue
            if any(r in changed for r in re.findall(r'var\((--[a-z0-9-]+)\)', v)):
                changed.add(n); out.append((n, v)); grew = True
    order = {n: i for i, (n, _) in enumerate(base)}
    return sorted(out, key=lambda d: order[d[0]])


def block(selector, pairs, indent=''):
    lines = ['%s%s {' % (indent, selector)]
    lines += ['%s  %s: %s;' % (indent, n, v) for n, v in pairs]
    lines.append('%s}' % indent)
    return '\n'.join(lines)


def build():
    tok = json.load(open(os.path.join(ROOT, 'tokens.json'), encoding='utf-8'))
    ver = tok['$extensions']['odsv']['version']
    themes = tok['theme']
    base = [d for p, t in walk({k: v for k, v in tok.items() if k != 'theme'}) for d in decls(p, t)]
    light = [d for p, t in walk(themes['light']) for d in decls(p, t)]
    prnt = [d for p, t in walk(themes['print']) for d in decls(p, t)]
    light = dependents(base, light) + light
    prnt = dependents(base, light + prnt) + light + prnt
    reduced = [(name(('motion', 'duration', k)), '0.01ms') for k in tok['motion']['duration'] if k in REDUCED]
    reduced.append((name(('motion', 'duration', 'spin')), '3000ms'))
    reduced += [(name(('motion', 'distance', k)), '0px') for k in tok['motion']['distance']]
    css = [
        '/* ODSV Design-Tokens v%s – ERZEUGT aus tokens.json (tools/build_tokens.py). Nicht von Hand ändern. */' % ver,
        '/* :root = dunkles Theme (Standard) · [data-theme="light"] = helles Theme · @media print = hell + Druck */',
        block(':root, [data-theme="dark"]', [('color-scheme', 'dark')] + base),
        '/* ---------- Helles Theme: nur Overrides ---------- */',
        block('[data-theme="light"]', [('color-scheme', 'light')] + light),
        '/* ---------- Druck: helles Theme + Druck-Overrides, unabhängig vom gesetzten Theme ---------- */',
        '@media print {\n' + block(':root, [data-theme]', [('color-scheme', 'light')] + list(dict(prnt).items()), '  ') + '\n}',
        '/* ---------- Reduzierte Bewegung: Dauern und Wege auf null ---------- */',
        '@media (prefers-reduced-motion: reduce) {\n' + block(':root, [data-theme]', reduced, '  ') + '\n}',
    ]
    out = os.path.join(ROOT, 'tokens.css')
    open(out, 'w', encoding='utf-8').write('\n'.join(css) + '\n')
    return len(base), len(light), len(prnt)


if __name__ == '__main__':
    print('tokens.css geschrieben: %d Basis-, %d Light-, %d Druck-Variablen' % build())
