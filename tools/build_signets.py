#!/usr/bin/env python3
"""ODSV-Signetfamilie – erzeugt die Themen-Signets nach der Konstruktionsgrammatik des Basis-Signets.

Grammatik (gilt für jede Variante, SPEC 10.4):
  1. viewBox 0 0 400 400, genau vier Striche (Pfade) à 26 Einheiten, runde Enden und Ecken.
  2. Farbfolge fest: Strich 1 signet-1 (Pink) → 2 signet-2 (Orange) → 3 signet-3 (Hellorange) → 4 signet-4 (Gelb);
     von außen/hinten/groß nach innen/vorne/klein.
  3. Genau ein gefüllter Punkt (signet-dot, Gelb, r 24–34) als Fokus: Ziel, Gipfel, Knoten, Cursor, Sonne.
  4. Motiv schwerpunktmäßig rechts; darf rechts angeschnitten sein (Karte nutzt xMaxYMid slice).
     Sichtbereich y 50–350 (bleibt auch in 4:3-Querformat sichtbar), links nicht unter x 120.
  5. Wortmarken-Zone x < 240 und y > 300 bleibt frei.
  6. Abstand paralleler Striche Mitte–Mitte ≥ 40 (lichte Weite ≥ 14); keine Füllflächen außer dem Punkt.
  7. Bedeutung über eine einfache, bekannte Form; keine Schrift, keine Marken, keine Personen.

Aufruf: python3 tools/build_signets.py  → schreibt die Symbole in web/icons.svg (zwischen Markern)
                                          und catalog/signets.json (Namen, Thema, Bedeutung).
"""
import math, json, re, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
SW = 26

def arc(cx, cy, r, a0, a1):
    """Kreisbogen von Winkel a0 nach a1 (Grad, 0 = rechts, gegen den Uhrzeigersinn = negativ y)."""
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy - r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy - r * math.sin(math.radians(a1))
    large = 1 if abs(a1 - a0) % 360 > 180 else 0
    sweep = 0 if a1 > a0 else 1
    return f'M{x0:.1f} {y0:.1f}A{r} {r} 0 {large} {sweep} {x1:.1f} {y1:.1f}'

def poly(pts, closed=False):
    d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts)
    return d + ('Z' if closed else '')

def smooth(pts, closed=False, t=0.5):
    """Catmull-Rom → kubische Bézier (weiche Linie durch die Punkte)."""
    P = pts[:]
    n = len(P)
    if closed: P = [P[-1]] + P + [P[0], P[1]]
    else: P = [P[0]] + P + [P[-1]]
    d = f'M{P[1][0]:.1f} {P[1][1]:.1f}'
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) * t / 3, p1[1] + (p2[1] - p0[1]) * t / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * t / 3, p2[1] - (p3[1] - p1[1]) * t / 3)
        d += f'C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}'
    return d + ('Z' if closed else '')

def circle_path(cx, cy, r):
    return f'M{cx - r:.1f} {cy:.1f}a{r} {r} 0 1 0 {2 * r:.1f} 0a{r} {r} 0 1 0 {-2 * r:.1f} 0Z'

# ---------------------------------------------------------------- Varianten
def base():
    # Original (Signal / Wirkung): vier Bögen um den Punkt am rechten Rand
    return ['M266.8 52.6A180 180 0 0 0 266.8 347.4', 'M289.7 85.3A140 140 0 0 0 289.7 314.7',
            'M312.6 118.1A100 100 0 0 0 312.6 281.9', 'M335.6 150.9A60 60 0 0 0 335.6 249.1'], (400, 200, 34)

def sparkle_sides(cx, cy, R, waist=0.16):
    tips = [(cx, cy - R), (cx + R, cy), (cx, cy + R), (cx - R, cy)]
    out = []
    for i in range(4):
        a, b = tips[i], tips[(i + 1) % 4]
        c = (cx + (a[0] - cx + b[0] - cx) * waist, cy + (a[1] - cy + b[1] - cy) * waist)
        out.append(f'M{a[0]:.1f} {a[1]:.1f}Q{c[0]:.1f} {c[1]:.1f} {b[0]:.1f} {b[1]:.1f}')
    return out

def ai():
    # Funke: ein Vierstrahl-Stern, jede Seite ein Strich (Farbfolge im Uhrzeigersinn ab oben), Punkt = Kern
    cx, cy = 276, 184
    return sparkle_sides(cx, cy, 112, 0.12), (cx, cy, 26)

def network():
    # Netz: vier Verbindungen vom Knoten (Punkt) zu Endknoten (Ring gehört zum Strich)
    hx, hy = 290, 186
    ends = [(152, 100, 22), (332, 84, 20), (182, 262, 20), (390, 292, 22)]
    paths = []
    for (ex, ey, rr) in ends:
        ang = math.atan2(ey - hy, ex - hx)
        sx, sy = hx + 56 * math.cos(ang), hy + 56 * math.sin(ang)
        tx, ty = ex - rr * math.cos(ang), ey - rr * math.sin(ang)
        paths.append(f'M{sx:.1f} {sy:.1f}L{tx:.1f} {ty:.1f}' + circle_path(ex, ey, rr))
    return paths, (hx, hy, 32)

def data():
    # Daten: vier steigende Säulen, Punkt über der höchsten
    base_y = 286
    xs = [196, 252, 308, 364]
    hs = [36, 74, 112, 150]
    paths = [f'M{x} {base_y}L{x} {base_y - h}' for x, h in zip(xs, hs)]
    return paths, (364, base_y - 150 - 56, 26)

def code():
    # Code: vier verschachtelte spitze Klammern, Punkt = Cursor
    cy, paths = 186, []
    for x, h in [(192, 106), (242, 79), (292, 52), (342, 26)]:
        w = h * 0.62
        paths.append(poly([(x + w, cy - h), (x, cy), (x + w, cy + h)]))
    return paths, (398, cy, 26)

def swarm():
    # Schwarm: vier Flugbahnen laufen spiralförmig auf den gemeinsamen Punkt zu (Koordination, Multi-Agent)
    cx, cy, r0, r1, turn = 284, 184, 128, 58, 100
    paths = []
    for a0 in (135, 45, -45, -135):
        pts = []
        for k in range(61):
            u = k / 60; r = r0 - (r0 - r1) * u; a = math.radians(a0 - turn * u)
            pts.append((cx + r * math.cos(a), cy - r * math.sin(a)))
        paths.append(smooth(pts[::6]))
    return paths, (cx, cy, 26)

def mountains():
    # Berge: ein Grat aus vier Abschnitten (links Pink → rechts Gelb), Punkt = Sonne zwischen den Gipfeln
    pts = [(150, 286), (210, 182), (266, 248), (332, 108), (410, 236)]
    return [poly([pts[i], pts[i + 1]]) for i in range(4)], (250, 100, 26)

def bike():
    # Fahrrad: gestreckte, ruhige Geometrie – kleinere Räder mit weitem Radstand (Vorderrad rechts angeschnitten),
    # Tretlager auf der Achslinie, Oberrohr waagrecht und niedrig, Sattel und Lenker auf gleicher Höhe.
    # Strich 1 Hinterrad · 2 Vorderrad · 3 Rahmen (offener Hinterbau, Hauptdreieck, Gabel) · 4 Sattel und Lenker; Punkt = Tretlager.
    r, y = 56, 232
    R, F = (176, y), (368, y)                   # Radstand 192 = 2r + 80
    B = (268, y)                                # Tretlager auf der Achslinie
    S, H = (244, 156), (346, 156)               # Oberrohr waagrecht, Rahmen flach
    top = 124                                   # Sattel und Lenker auf einer Höhe
    frame = (f'M{R[0]} {R[1]}L{B[0]} {B[1]}L{S[0]} {S[1]}L{H[0]} {H[1]}L{B[0]} {B[1]}'
             f'M{H[0]} {H[1]}L{F[0]} {F[1]}')
    seat = f'M{S[0]} {S[1]}L{S[0] - 6} {top}M{S[0] - 38} {top}L{S[0] + 12} {top}'
    bar = f'M{H[0]} {H[1]}L{H[0] - 6} {top}L{H[0] + 30} {top}'
    return [circle_path(*R, r), circle_path(*F, r), frame, seat + bar], (B[0], B[1], 24)

def outdoor():
    # Outdoor: Zelt mit gekreuzten Stangen, Eingang und Boden; Punkt = Sonne
    g = 284
    left = f'M180 {g}L298 68'          # Stange links, kreuzt über dem First
    right = f'M384 {g}L266 68'         # Stange rechts
    door = f'M246 {g}L282 206L318 {g}'
    ground = f'M156 {g}L404 {g}'
    return [left, right, door, ground], (372, 98, 26)

def route():
    # Route: Serpentine bergauf in vier Abschnitten, Punkt = Ziel
    x0, x1, r = 182, 332, 31
    ys = [280, 218, 156, 94]
    paths = [
        f'M{x0 - 14} {ys[0]}L{x1} {ys[0]}A{r} {r} 0 0 0 {x1} {ys[1]}',
        f'M{x1} {ys[1]}L{x0} {ys[1]}A{r} {r} 0 0 1 {x0} {ys[2]}',
        f'M{x0} {ys[2]}L{x1} {ys[2]}A{r} {r} 0 0 0 {x1} {ys[3]}',
        f'M{x1} {ys[3]}L{x0 + 62} {ys[3]}',
    ]
    return paths, (x0 + 4, ys[3], 26)


# ---------------------------------------------------------------- Situationen (Erzähl-Signets, keine Statusanzeige)
def success():
    # Erfolg: Haken führt zum Punkt (Ziel erreicht), drei Strahlen feiern ihn
    P = (334, 150)
    rays = []
    for ang, l0, l1 in ((90, 46, 80), (30, 46, 80), (150, 46, 76)):
        x0, y0 = P[0] + l0 * math.cos(math.radians(ang)), P[1] - l0 * math.sin(math.radians(ang))
        x1, y1 = P[0] + l1 * math.cos(math.radians(ang)), P[1] - l1 * math.sin(math.radians(ang))
        rays.append(f'M{x0:.1f} {y0:.1f}L{x1:.1f} {y1:.1f}')
    check = poly([(178, 222), (228, 272), (304, 186)])
    return rays + [check], (P[0], P[1], 26)

def fail():
    # Fail: Kurve steigt in drei Abschnitten und bricht dann steil ein; Punkt = Aufschlag
    pts = [(140, 250), (200, 186), (248, 214), (318, 104)]
    paths = [poly([pts[i], pts[i + 1]]) for i in range(3)]
    paths.append(f'M318 104L356 236')
    return paths, (366, 290, 26)

def conflict():
    # Konflikt: zwei Pfeile prallen aufeinander; Punkt = Reibungsstelle
    y = 188
    left_shaft, left_head = f'M130 {y}L232 {y}', f'M200 {y - 40}L240 {y}L200 {y + 40}'
    right_shaft, right_head = f'M424 {y}L340 {y}', f'M372 {y - 40}L332 {y}L372 {y + 40}'
    return [left_shaft, left_head, right_head, right_shaft], (286, y, 24)

def agreement():
    # Einigung: zwei Wege laufen zusammen und gehen gemeinsam weiter; Punkt = Treffpunkt
    M = (262, 190)
    upper = f'M140 92C200 92 220 {M[1]} {M[0]} {M[1]}'
    lower = f'M140 288C200 288 220 {M[1]} {M[0]} {M[1]}'
    joint = f'M{M[0] + 38} {M[1]}L388 {M[1]}'
    head = f'M354 {M[1] - 34}L392 {M[1]}L354 {M[1] + 34}'
    return [upper, lower, joint, head], (M[0], M[1], 26)

def idea():
    # Idee: Glühbirne mit Fassung und Strahlen; Punkt = Glühfaden
    cx, cy, r = 284, 184, 70
    bulb = arc(cx, cy, r, -48, 228)                                  # offen nach unten
    a0 = math.radians(-48); x0, y0 = cx + r * math.cos(a0), cy - r * math.sin(a0)
    neck = f'M{x0:.1f} {y0:.1f}L{x0 - 8:.1f} {y0 + 40:.1f}L{2 * cx - x0 + 8:.1f} {y0 + 40:.1f}L{2 * cx - x0:.1f} {y0:.1f}'
    base = f'M{cx - 22} {y0 + 82:.1f}L{cx + 22} {y0 + 82:.1f}'
    rays = ''
    for ang in (90, 35, 145):
        xa, ya = cx + (r + 30) * math.cos(math.radians(ang)), cy - (r + 30) * math.sin(math.radians(ang))
        xb, yb = cx + (r + 50) * math.cos(math.radians(ang)), cy - (r + 50) * math.sin(math.radians(ang))
        rays += f'M{xa:.1f} {ya:.1f}L{xb:.1f} {yb:.1f}'
    return [bulb, neck, base, rays], (cx, cy, 24)

def question():
    # Frage: Fragezeichen aus drei Bogenabschnitten und Hals; Punkt = Punkt des Fragezeichens
    cx, cy, r = 288, 132, 62
    a1 = arc(cx, cy, r, 160, 80)
    a2 = arc(cx, cy, r, 80, 0)
    a3 = f'M{cx + r} {cy}C{cx + r} {cy + 54} {cx} {cy + 40} {cx} {cy + 96}'
    stem = f'M{cx} {cy + 96}L{cx} {cy + 118}'
    return [a1, a2, a3, stem], (cx, cy + 176, 26)

def progress():
    # In Arbeit: vier Bogenstücke eines Rings mit Lücken, im Uhrzeigersinn kürzer werdend; Punkt = Mitte
    cx, cy, r = 284, 186, 104
    spans = [(100, 10), (-10, -80), (-100, -150), (-170, -200)]
    return [arc(cx, cy, r, a0, a1) for a0, a1 in spans], (cx, cy, 26)

def restart():
    # Neustart: Kreispfeil im Uhrzeigersinn aus drei Abschnitten, Pfeilspitze am Ende in Laufrichtung; Punkt = Mitte
    cx, cy, r = 282, 188, 98
    segs = [arc(cx, cy, r, 120, 30), arc(cx, cy, r, 10, -80), arc(cx, cy, r, -100, -195)]
    th = math.radians(-195)                                   # Endpunkt (links oben)
    ex, ey = cx + r * math.cos(th), cy - r * math.sin(th)
    tx, ty = math.sin(th), math.cos(th)                       # Laufrichtung im Uhrzeigersinn (Bildschirmkoordinaten)
    wings = []
    for sgn in (1, -1):
        a_ = math.atan2(ty, tx) + math.pi + sgn * math.radians(42)
        wings.append((ex + 46 * math.cos(a_), ey + 46 * math.sin(a_)))
    head = f'M{wings[0][0]:.1f} {wings[0][1]:.1f}L{ex:.1f} {ey:.1f}L{wings[1][0]:.1f} {wings[1][1]:.1f}'
    return segs + [head], (cx, cy, 26)


VARIANTS = [
    ('odsv-signet', 'Basis', 'Signal / Wirkung', base, 'Standard für alle Themen'),
    ('odsv-signet-ai', 'Technik', 'KI', ai, 'Funke: Intelligenz, Generierung, Assistenz'),
    ('odsv-signet-network', 'Technik', 'Netzwerk', network, 'Knoten und Verbindungen: Vernetzung, Plattform, Integration'),
    ('odsv-signet-data', 'Technik', 'Daten', data, 'Steigende Säulen: Analyse, Kennzahlen, Wachstum'),
    ('odsv-signet-code', 'Technik', 'Code', code, 'Klammern und Cursor: Entwicklung, Software, Engineering'),
    ('odsv-signet-swarm', 'Technik', 'Schwarm', swarm, 'Flugbahnen sammeln sich am Punkt: Multi-Agent, Koordination, Zusammenarbeit'),
    ('odsv-signet-mountains', 'Lifestyle', 'Berge', mountains, 'Gestaffelte Grate und Sonne: Alpin, Wandern, Weitblick'),
    ('odsv-signet-bike', 'Lifestyle', 'Fahrrad', bike, 'Räder und Rahmen: Radfahren, Mobilität, Touren'),
    ('odsv-signet-outdoor', 'Lifestyle', 'Outdoor', outdoor, 'Zelt unter der Sonne: Draußen, Camping, Abenteuer'),
    ('odsv-signet-route', 'Lifestyle', 'Route', route, 'Geschwungene Strecke zum Ziel: Training, Tour, Fortschritt'),
    ('odsv-signet-success', 'Situation', 'Erfolg', success, 'Haken erreicht das Ziel, Strahlen feiern: Erfolg, Meilenstein, Abschluss'),
    ('odsv-signet-fail', 'Situation', 'Fail', fail, 'Kurve steigt und bricht ein: Misserfolg, Rückschlag, Learnings'),
    ('odsv-signet-conflict', 'Situation', 'Konflikt', conflict, 'Zwei Pfeile prallen aufeinander: Konflikt, Zielkonflikt, Reibung'),
    ('odsv-signet-agreement', 'Situation', 'Einigung', agreement, 'Zwei Wege werden einer: Einigung, Lösung, Zusammenarbeit'),
    ('odsv-signet-idea', 'Situation', 'Idee', idea, 'Glühbirne mit Strahlen: Idee, Innovation, Vorschlag'),
    ('odsv-signet-question', 'Situation', 'Frage', question, 'Fragezeichen: offene Frage, Unklarheit, Diskussion'),
    ('odsv-signet-progress', 'Situation', 'In Arbeit', progress, 'Ring aus Bogenstücken: in Arbeit, läuft, Zwischenstand'),
    ('odsv-signet-restart', 'Situation', 'Neustart', restart, 'Kreispfeil: Neustart, Iteration, Wiederholung'),
]

def symbol(sid, paths, dot):
    cols = ['var(--odsv-color-signet-1)', 'var(--odsv-color-signet-2)', 'var(--odsv-color-signet-3)', 'var(--odsv-color-signet-4)']
    body = ''.join(f'<path d="{d}" style="fill:none;stroke-width:{SW};stroke-linecap:round;stroke-linejoin:round;stroke:{c}"/>' for d, c in zip(paths, cols))
    if dot[2]: body += f'<circle cx="{dot[0]}" cy="{dot[1]}" r="{dot[2]}" style="fill:var(--odsv-color-signet-dot)"/>'
    return f'<symbol id="{sid}" viewBox="0 0 400 400" fill="none" stroke="none">{body}</symbol>'

if __name__ == '__main__':
    syms, meta = [], []
    for sid, group, name, fn, meaning in VARIANTS:
        paths, dot = fn()
        assert len(paths) == 4, sid
        syms.append(symbol(sid, paths, dot))
        meta.append({'id': sid, 'group': group, 'name': name, 'meaning': meaning, 'usage': f'<svg viewBox="0 0 400 400" role="img" aria-label="…"><use href="#{sid}"/></svg>'})
    p = ROOT / 'web' / 'icons.svg'; s = p.read_text()
    s = re.sub(r'<symbol id="odsv-signet".*?</symbol>', '', s, flags=re.S)
    s = re.sub(r'<!--SIGNETS-->.*?<!--/SIGNETS-->', '', s, flags=re.S)
    i = s.rstrip().rfind('</svg>')
    s = s[:i].rstrip() + '\n<!--SIGNETS-->' + ''.join(syms) + '<!--/SIGNETS-->\n</svg>\n'
    p.write_text(s)
    (ROOT / 'catalog').mkdir(exist_ok=True)
    (ROOT / 'catalog' / 'signets.json').write_text(json.dumps({'grammar': __doc__.split('Grammatik')[1].split('Aufruf')[0].strip(), 'signets': meta}, ensure_ascii=False, indent=1) + '\n')
    print(len(syms), 'Signets geschrieben')
