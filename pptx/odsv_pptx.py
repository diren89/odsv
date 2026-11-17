#!/usr/bin/env python3
"""ODSV 1.0 – PowerPoint-Helfer für Menschen und AI-Agents.

Baut Präsentationen auf pptx/ODSV-Vorlage.potx, ausschließlich über die Layout-Platzhalter (Rollen),
mit Fortschrittsleiste, Quelle/Foliennummer, ODSV-Diagrammen und -Tabellen sowie einer Inhaltsprüfung.
Rollen, Platzhalter-idx und Zeichengrenzen je Layout: catalog/pptx-layouts.json.

    from odsv_pptx import Deck
    d = Deck()                                         # Vorlage laden
    d.slide('Titel', eyebrow='Quartalsbericht · Q3 2026', title='Kennzahlen', sub='Ein Satz, der erklärt.')
    s = d.slide('Diagramm', chapter=2, source='Quelle: Beispieldaten', eyebrow='Vertrieb',
                title='Q4 liegt vorn', sub='Umsatz je Quartal, in Mio. €',
                ilabel='Kernaussage', itext='Q4 wächst am stärksten.', inote='Fokus-Muster: eine Säule gelb.')
    d.chart(s, 'bar', ['Q1','Q2','Q3','Q4'], {'Umsatz': [1.2, 1.4, 1.5, 2.1]}, highlight=3, alt='Säulen: Q4 mit 2,1 am höchsten')
    print(d.check())                                   # Liste von Befunden (leer = ok)
    d.save('bericht.pptx'); d.render_png('vorschau')   # optional: PNG je Folie (LibreOffice nötig)

Text-Werte: str (ein Absatz), list[str] (mehrere Absätze/Aufzählung) oder list[list[(text, format)]] für Läufe.
format-Schlüssel: color (Hex ohne #), size (pt), bold, caps, spc (1/100 pt Laufweite).
"""
import os, re, json, shutil, subprocess, tempfile, zipfile, pathlib
from lxml import etree
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, PP_PLACEHOLDER
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION, XL_TICK_MARK
from pptx.oxml.ns import qn

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
TEMPLATE = HERE / 'ODSV-Vorlage.potx'
A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
SERIES = ['FFE94D', '4797FF', 'EC3A78', '2FCFC2', 'F5893A', 'B9A1FF', '8FD46A']   # = accent1–6 + Slot 7
CONTEXT, NEUTRAL = '636366', '8E8E93'
MX, CW, SEG_N, SEG_GAP = 0.667, 12.0, 7, 0.08                                       # Folienraster (Zoll)
TABLE_STYLE_ID = '{5A1D0E00-0D5B-4C1A-9C0D-0D5B00000001}'
def rgb(h): return RGBColor.from_string(h)
def I(v): return Emu(int(round(v * 914400)))
def seg_w(n): return (CW - (n - 1) * SEG_GAP) / n
def seg_x(i, n): return MX + i * (seg_w(n) + SEG_GAP)

def _layouts_spec():
    p = ROOT / 'catalog' / 'pptx-layouts.json'
    return {l['name']: l for l in json.loads(p.read_text())['layouts']} if p.exists() else {}

def spPr_none(parent, before=None):
    sp=etree.SubElement(parent,qn('c:spPr')); etree.SubElement(sp,qn('a:noFill')); ln=etree.SubElement(sp,qn('a:ln')); etree.SubElement(ln,qn('a:noFill'))
    return sp
def style_chart(chart,kind,colors=None,point_colors=None,legend=False,labels=False,numfmt='General',vmax=None,overlap=None):
    cs=chart._chartSpace
    chart.font.size=Pt(12); chart.font.name='+mn-lt'; chart.font.color.rgb=rgb('8E8E93')
    # chartSpace / plotArea ohne Fläche
    rc=cs.find(qn('c:roundedCorners'))
    if rc is None:
        rc=etree.Element(qn('c:roundedCorners')); cs.insert(0 if cs.find(qn('c:date1904')) is None else 1,rc)
    rc.set('val','0')
    txPr=cs.find(qn('c:txPr'))
    sp=etree.Element(qn('c:spPr')); etree.SubElement(sp,qn('a:noFill')); ln=etree.SubElement(sp,qn('a:ln')); etree.SubElement(ln,qn('a:noFill'))
    txPr.addprevious(sp)
    pa=cs.find(qn('c:chart')).find(qn('c:plotArea'))
    sp2=etree.SubElement(pa,qn('c:spPr')); etree.SubElement(sp2,qn('a:noFill')); l2=etree.SubElement(sp2,qn('a:ln')); etree.SubElement(l2,qn('a:noFill'))
    chart.has_title=False
    va=chart.value_axis; ca=chart.category_axis
    va.has_major_gridlines=True; va.major_gridlines.format.line.color.rgb=rgb('2C2C2E'); va.major_gridlines.format.line.width=Pt(0.75)
    va.format.line.fill.background(); va.major_tick_mark=XL_TICK_MARK.NONE; va.minor_tick_mark=XL_TICK_MARK.NONE
    va.tick_labels.font.size=Pt(12); va.tick_labels.font.color.rgb=rgb('8E8E93'); va.tick_labels.number_format=numfmt; va.tick_labels.number_format_is_linked=False
    if vmax: va.maximum_scale=vmax
    va.minimum_scale=0
    ca.has_major_gridlines=False; ca.format.line.color.rgb=rgb('48484A'); ca.format.line.width=Pt(0.75)
    ca.major_tick_mark=XL_TICK_MARK.NONE; ca.minor_tick_mark=XL_TICK_MARK.NONE
    ca.tick_labels.font.size=Pt(12); ca.tick_labels.font.color.rgb=rgb('8E8E93')
    plot=chart.plots[0]
    if kind in('bar','stack'):
        plot.gap_width=60; plot.overlap=100 if kind=='stack' else 0
    chart.has_legend=legend
    if legend:
        chart.legend.position=XL_LEGEND_POSITION.TOP; chart.legend.include_in_layout=False
        chart.legend.font.size=Pt(12); chart.legend.font.color.rgb=rgb('CCCCCC')
        lg=chart.legend._element
        lay=lg.find(qn('c:layout'))
        if lay is None:
            lay=etree.Element(qn('c:layout')); lg.find(qn('c:legendPos')).addnext(lay)
        ml=etree.SubElement(lay,qn('c:manualLayout'))
        for t,v in (('xMode','edge'),('yMode','edge'),('x','0'),('y','0'),('w','0.7'),('h','0.1')):
            etree.SubElement(ml,qn('c:'+t)).set('val',v)
    for i,ser in enumerate(plot.series):
        c=(colors or SERIES)[i]
        if kind=='line':
            ser.format.line.color.rgb=rgb(c); ser.format.line.width=Pt(2.25); ser.smooth=False
            rnd_ln=ser.format.line._get_or_add_ln(); rnd_ln.set('cap','rnd')
            ser.marker.style=None
            from pptx.enum.chart import XL_MARKER_STYLE
            ser.marker.style=XL_MARKER_STYLE.NONE
            n=len(list(ser.values))
            pt=ser.points[n-1]; pt.marker.style=XL_MARKER_STYLE.CIRCLE; pt.marker.size=8
            pt.marker.format.fill.solid(); pt.marker.format.fill.fore_color.rgb=rgb(c); pt.marker.format.line.color.rgb=rgb(c)
        else:
            ser.format.fill.solid(); ser.format.fill.fore_color.rgb=rgb(c); ser.format.line.fill.background(); ser.invert_if_negative=False
            if point_colors:
                for j,pc in enumerate(point_colors):
                    ptf=ser.points[j].format; ptf.fill.solid(); ptf.fill.fore_color.rgb=rgb(pc); ptf.line.fill.background()
    if labels:
        plot.has_data_labels=True; dl=plot.data_labels
        dl.font.size=Pt(12); dl.font.color.rgb=rgb('000000' if kind=='stack' else 'CCCCCC'); dl.number_format=numfmt; dl.number_format_is_linked=False
        dl.position=XL_LABEL_POSITION.OUTSIDE_END if kind=='bar' else (XL_LABEL_POSITION.CENTER if kind=='stack' else XL_LABEL_POSITION.ABOVE)
        dl.show_value=True

# ------------------------------------------------------------------ Formen und Line-Art-Icons (wie die Vorlage)
def shape(s,kind,x,y,w,h,fill=None,line=None,lw=2.25,name=None,adj=None):
    sh=s.shapes.add_shape(kind,I(x),I(y),I(w),I(h)); sh.shadow.inherit=False
    if fill: sh.fill.solid(); sh.fill.fore_color.rgb=rgb(fill)
    else: sh.fill.background()
    if line: sh.line.color.rgb=rgb(line); sh.line.width=Pt(lw)
    else: sh.line.fill.background()
    if adj is not None: sh.adjustments[0]=adj
    if name: sh.name=name
    return sh
def rnd(sh):
    ln=sh._element.spPr.find(qn('a:ln'))
    if ln is not None:
        ln.set('cap','rnd')
        for t in ('a:round',):
            if ln.find(qn(t)) is None: etree.SubElement(ln,qn(t))
def poly(s,pts,x0,y0,color='FFFFFF',lw=2.25,close=False,name='Linie'):
    fb=s.shapes.build_freeform(I(x0+pts[0][0]),I(y0+pts[0][1]))
    fb.add_line_segments([(I(x0+x),I(y0+y)) for x,y in pts[1:]],close=close)
    sh=fb.convert_to_shape(); sh.fill.background(); sh.line.color.rgb=rgb(color); sh.line.width=Pt(lw); sh.name=name; sh.shadow.inherit=False
    rnd(sh); return sh
def arc(s,x,y,w,h,a1,a2,color,lw=2.25,name='Bogen'):
    sh=s.shapes.add_shape(MSO_SHAPE.ARC,I(x),I(y),I(w),I(h)); sh.shadow.inherit=False
    av=sh._element.spPr.find(qn('a:prstGeom')).find(qn('a:avLst'))
    for c in list(av): av.remove(c)
    for n,v in (('adj1',a1),('adj2',a2)):
        g=etree.SubElement(av,qn('a:gd')); g.set('name',n); g.set('fmla',f'val {int(v*60000)}')
    sh.fill.background(); sh.line.color.rgb=rgb(color); sh.line.width=Pt(lw); sh.name=name; rnd(sh); return sh
def circ(s,cx,cy,r,color='FFFFFF',lw=2.25,fill=None,name='Kreis'):
    return shape(s,MSO_SHAPE.OVAL,cx-r,cy-r,2*r,2*r,fill=fill,line=color if not fill else None,lw=lw,name=name)
def rr(s,x,y,w,h,r=0.1,color='FFFFFF',lw=2.25,name='Rahmen',fill=None):
    sh=shape(s,MSO_SHAPE.ROUNDED_RECTANGLE,x,y,w,h,fill=fill,line=color if color else None,lw=lw,name=name,adj=min(0.5,r/min(w,h))); return sh
# --- Line-Art-Icons (1,4 in) ---
def icon(s,kind,x,y,col='FFFFFF',acc='FFE94D'):
    if kind=='list':
        for k in range(3):
            circ(s,x+0.25,y+0.35+k*0.35,0.05,acc,fill=acc,name='Icon Aufzählungspunkt')
            poly(s,[(0.45,0.35+k*0.35),(1.2,0.35+k*0.35)],x,y,col,name='Icon Zeile')
    elif kind=='layout':
        rr(s,x+0.1,y+0.15,1.2,1.1,0.12,col,name='Icon Folie')
        poly(s,[(0.1,0.45),(1.3,0.45)],x,y,col,name='Icon Titelzone')
        rr(s,x+0.25,y+0.6,0.4,0.5,0.06,acc,name='Icon Platzhalter'); rr(s,x+0.75,y+0.6,0.4,0.5,0.06,col,name='Icon Platzhalter')
    elif kind=='chart':
        poly(s,[(0.15,0.15),(0.15,1.2),(1.3,1.2)],x,y,col,name='Icon Achsen')
        for k,h in enumerate((0.35,0.6,0.85)):
            rr(s,x+0.35+k*0.3,y+1.15-h,0.18,h,0.04,acc if k==2 else col,name='Icon Balken')
    elif kind=='check':
        circ(s,x+0.7,y+0.7,0.55,col,name='Icon Kreis'); poly(s,[(0.47,0.72),(0.64,0.9),(0.95,0.52)],x,y,acc,lw=3.0,name='Icon Haken')
    elif kind=='ok':
        circ(s,x+0.14,y+0.14,0.14,'30D158',lw=1.75,name='Icon Richtig'); poly(s,[(0.07,0.15),(0.12,0.21),(0.22,0.09)],x,y,'30D158',lw=1.75,name='Haken')
    elif kind=='no':
        circ(s,x+0.14,y+0.14,0.14,'FF453A',lw=1.75,name='Icon Falsch'); poly(s,[(0.08,0.08),(0.2,0.2)],x,y,'FF453A',lw=1.75,name='Kreuz'); poly(s,[(0.2,0.08),(0.08,0.2)],x,y,'FF453A',lw=1.75,name='Kreuz')


def _fmt_run(r, f):
    if 'color' in f: r.font.color.rgb = rgb(f['color'])
    if 'size' in f: r.font.size = Pt(f['size'])
    if 'bold' in f: r.font.bold = f['bold']
    rPr = r._r.get_or_add_rPr()
    if f.get('caps'): rPr.set('cap', 'all')
    if 'spc' in f: rPr.set('spc', str(f['spc']))

def _set_alt(shape, txt):
    shape._element.xpath('.//p:cNvPr')[0].set('descr', txt)

def _plain(v):
    if isinstance(v, str): return v
    out = []
    for p in v:
        out.append(p if isinstance(p, str) else ''.join(t for t, _ in p))
    return '\n'.join(out)


class Deck:
    """Präsentation auf Basis der ODSV-Vorlage."""

    def __init__(self, template=TEMPLATE):
        tmp = tempfile.NamedTemporaryFile(suffix='.pptx', delete=False); tmp.close()
        with zipfile.ZipFile(template) as src, zipfile.ZipFile(tmp.name, 'w', zipfile.ZIP_DEFLATED) as dst:
            for it in src.infolist():
                data = src.read(it.filename)
                if it.filename == '[Content_Types].xml':
                    data = data.replace(b'presentationml.template.main+xml', b'presentationml.presentation.main+xml')
                dst.writestr(it.filename, data)
        self.prs = Presentation(tmp.name); os.unlink(tmp.name)
        self.layouts = {l.name: l for l in self.prs.slide_layouts}
        self.spec = _layouts_spec()
        self._filled = []          # (slide, layout, {rolle: text}) für check()
        self.sections = []

    # ---------------------------------------------------------------- Folien
    def slide(self, layout, chapter=None, chapters=SEG_N, source=None, notes=None, section=None, icons=None, signet=None, wordmark='ODSV', **content):
        """Neue Folie. layout = Name aus catalog/pptx-layouts.json (z. B. 'Titel', 'Diagramm').
        chapter: 0-basierter Index des aktiven Kapitels für die Fortschrittsleiste (0…6; Leiste hat 7 Segmente).
        source: Quellenzeile rechts unten. content: Rolle=Text (siehe Platzhalter-Rollen des Layouts).
        icons: nur 'Prozess vier Schritte' – vier Namen aus 'list', 'layout', 'chart', 'check'.
        signet: nur 'Titel' und 'Kapiteltrenner' – Signet aus pptx/signets/ (Themen: ai, network, data, code, mountains,
                bike, outdoor, route; Situationen: success, fail, conflict, agreement, idea, question, progress, restart;
                None/'basis' = Standard der Vorlage). Auf anderen Folien: Deck.mark(slide, name). wordmark: Text auf der Signet-Karte (Titel).
        Bei 'Vergleich' ist Spalte A die empfohlene (gelber Rand, ✓); Spalte B bekommt ✗."""
        if layout not in self.layouts:
            raise KeyError(f'Layout „{layout}“ unbekannt. Verfügbar: {", ".join(self.layouts)}')
        lay = self.layouts[layout]; s = self.prs.slides.add_slide(lay); s._odsv_layout = layout
        have = {p.placeholder_format.type for p in lay.placeholders}
        if PP_PLACEHOLDER.SLIDE_NUMBER in have:
            self._footer(s, source)
        if chapter is not None and self.spec.get(layout, {}).get('progress', True):
            self.progress(s, chapter, chapters)
        roles = self._roles(layout)
        for role, val in content.items():
            if role not in roles:
                raise KeyError(f'Rolle „{role}“ gibt es in „{layout}“ nicht. Rollen: {", ".join(roles)}')
            if role in ('chart', 'table', 'image'):
                raise ValueError(f'„{role}“ über d.{role}(…) befüllen, nicht als Text.')
            self.text(s, role, val)
        if layout == 'Vergleich':
            icon(s, 'ok', MX + 0.3, 2.62); icon(s, 'no', 6.767 + 0.3, 2.62)
            rr(s, MX, 2.35, 5.9, 4.3, 0.28, 'FFE94D', lw=1.5, name='Empfehlung (Rand)')
        self._filled.append((s, layout, {k: _plain(v) for k, v in content.items()}))
        if signet and signet != 'basis':
            self._signet(s, layout, signet, wordmark)
        if icons and layout == 'Prozess vier Schritte':
            for k, ic in enumerate(icons[:4]): icon(s, ic, MX + k * 3.05 + 0.28, 2.95)
        if notes: s.notes_slide.notes_text_frame.text = notes
        if section: self.sections.append((section, s.slide_id))
        return s

    SIGNETS = ('basis', 'ai', 'network', 'data', 'code', 'mountains', 'bike', 'outdoor', 'route',
               'success', 'fail', 'conflict', 'agreement', 'idea', 'question', 'progress', 'restart')
    SIGNET_NAMES = {'ai': 'KI', 'network': 'Netzwerk', 'data': 'Daten', 'code': 'Code', 'mountains': 'Berge', 'bike': 'Fahrrad',
                    'outdoor': 'Outdoor', 'route': 'Route', 'success': 'Erfolg', 'fail': 'Fail', 'conflict': 'Konflikt',
                    'agreement': 'Einigung', 'idea': 'Idee', 'question': 'Frage', 'progress': 'In Arbeit', 'restart': 'Neustart', 'basis': 'Basis'}

    def _signet(self, s, layout, name, wordmark):
        if name not in self.SIGNETS:
            raise KeyError(f'Signet „{name}“ unbekannt. Verfügbar: {", ".join(self.SIGNETS)}')
        meaning = self.SIGNET_NAMES[name]
        if layout == 'Titel':
            pic = s.shapes.add_picture(str(HERE / 'signets' / f'{name}-card.png'), I(7.783), I(0.667), I(4.883), I(6.167))
            _set_alt(pic, f'Signet {meaning}: vier Linien im Verlauf Pink, Orange, Gelb'); pic.name = f'Signet-Karte {meaning}'
            if wordmark:
                tb = s.shapes.add_textbox(I(8.083), I(6.14), I(3.0), I(0.3)); tb.name = 'Wortmarke Signet'
                tf = tb.text_frame; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
                tf.paragraphs[0].alignment = PP_ALIGN.LEFT
                r = tf.paragraphs[0].add_run(); r.text = wordmark
                _fmt_run(r, {'size': 10, 'caps': True, 'spc': 140, 'color': 'FFFFFF', 'bold': True})
        elif layout == 'Kapiteltrenner':
            cover = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, I(11.55), I(5.0), I(1.2), I(1.72))   # Standardmarke der Vorlage abdecken
            cover.fill.solid(); cover.fill.fore_color.rgb = rgb('000000'); cover.line.fill.background(); cover.shadow.inherit = False
            cover.name = 'Abdeckung Standardmarke'
            pic = s.shapes.add_picture(str(HERE / 'signets' / f'{name}-mark.png'), I(11.617), I(5.08), I(1.05), I(1.561))
            _set_alt(pic, f'Signet-Marke {meaning}'); pic.name = f'Signet-Marke {meaning}'
        else:
            raise ValueError('signet= gibt es nur für „Titel“ und „Kapiteltrenner“ – sonst Deck.mark(slide, name, x, y, h).')

    def mark(self, s, name, x=None, y=None, h=None):
        """Signet ohne Karte platzieren (Zoll). Ohne Position: auf Folien mit leerer Hinweis-Karte (Rolle 'aside')
        mittig in die Karte, sonst unten rechts. Höchstens eines je Folie; nie zusammen mit einem Themen-Signet."""
        if name not in self.SIGNETS: raise KeyError(f'Signet „{name}“ unbekannt. Verfügbar: {", ".join(self.SIGNETS)}')
        if any(sh.name.startswith('Signet') for sh in s.shapes): raise ValueError('Auf dieser Folie steht bereits ein Signet.')
        ratio = 900 / 1338
        if x is None and 'aside' in self._roles(s._odsv_layout):
            card = self.ph(s, 'aside')
            if not card.text_frame.text.strip():
                card.text_frame.text = '\u200b'                       # Karte bleibt als Fläche, kein leerer Platzhalter
                cx, cy, cw, chh = card.left / 914400, card.top / 914400, card.width / 914400, card.height / 914400
                h = h or min(chh * 0.78, cw / ratio * 0.9)
                x, y = cx + (cw - h * ratio) / 2 + 0.15, cy + (chh - h) / 2
        if x is None: x, y, h = 11.2, 5.05, h or 1.5
        h = h or 1.5
        pic = s.shapes.add_picture(str(HERE / 'signets' / f'{name}-mark.png'), I(x), I(y), I(h * ratio), I(h))
        _set_alt(pic, f'Signet {self.SIGNET_NAMES[name]}'); pic.name = f'Signet-Marke {self.SIGNET_NAMES[name]}'
        return pic

    def _roles(self, layout):
        sp = self.spec.get(layout)
        if sp: return {p['role']: p['idx'] for p in sp['placeholders']}
        return {p.name: p.placeholder_format.idx for p in self.layouts[layout].placeholders}

    def ph(self, s, role):
        idx = self._roles(s._odsv_layout)[role]
        for p in s.placeholders:
            if p.placeholder_format.idx == idx: return p
        raise KeyError(role)

    def text(self, s, role, content):
        shp = self.ph(s, role); tf = shp.text_frame
        paras = content if isinstance(content, list) else [content]
        for i, pc in enumerate(paras):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            for t, f in (pc if isinstance(pc, list) else [(pc, {})]):
                r = p.add_run(); r.text = t; _fmt_run(r, f)
        return shp

    def drop(self, s, role):
        """Optionalen Platzhalter unsichtbar machen (z. B. Hinweis-Karte). Er bleibt erhalten, damit weder PowerPoint
        noch LibreOffice den Layout-Platzhalter samt Aufforderungstext einblendet."""
        shp = self.ph(s, role)
        e = I(0.04)                                                   # etwas größer als die Layout-Karte, damit kein Rand durchscheint
        shp.left, shp.top, shp.width, shp.height = shp.left - e, shp.top - e, shp.width + 2 * e, shp.height + 2 * e
        spPr = shp._element.spPr
        for t in ('a:solidFill', 'a:gradFill', 'a:noFill', 'a:ln'):
            for old in spPr.findall(qn(t)): spPr.remove(old)
        for g in spPr.findall(qn('a:prstGeom')): spPr.remove(g)
        pg = etree.SubElement(spPr, qn('a:prstGeom')); pg.set('prst', 'rect'); etree.SubElement(pg, qn('a:avLst'))
        # Deckend in Folienschwarz statt transparent: LibreOffice zeigt sonst den Layout-Platzhalter darunter
        sf = etree.SubElement(spPr, qn('a:solidFill')); etree.SubElement(sf, qn('a:srgbClr')).set('val', '000000')
        ln = etree.SubElement(spPr, qn('a:ln')); etree.SubElement(ln, qn('a:noFill'))
        shp.text_frame.text = '\u00a0'; shp.name = 'Leer: ' + shp.name
        return shp

    def progress(self, s, k, n=SEG_N):
        """Fortschritt: Segmente 0…k weiß über der grauen Spur der Vorlage (7 Segmente)."""
        k = max(0, min(k, n - 1))
        for i in range(k + 1):
            sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, I(seg_x(i, n)), I(0.3), I(seg_w(n)), I(0.04))
            sh.adjustments[0] = 0.5; sh.fill.solid(); sh.fill.fore_color.rgb = rgb('FFFFFF'); sh.line.fill.background()
            sh.name = f'Fortschritt aktiv {i + 1}'; sh.shadow.inherit = False

    def _footer(self, s, source):
        tree = s.shapes._spTree
        def add_ph(tp, idx, name, inner):
            tree.append(etree.fromstring(f'<p:sp xmlns:p="{P}" xmlns:a="{A}"><p:nvSpPr><p:cNvPr id="{900 + idx}" name="{name}"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr><p:ph type="{tp}" sz="quarter" idx="{idx}"/></p:nvPr></p:nvSpPr><p:spPr/><p:txBody><a:bodyPr/><a:lstStyle/>{inner}</p:txBody></p:sp>'))
        run = '<a:rPr lang="de-DE" sz="1000" cap="all" spc="140"><a:solidFill><a:srgbClr val="8E8E93"/></a:solidFill><a:latin typeface="+mn-lt"/></a:rPr>'
        if source:
            src = source.replace('&', '&amp;').replace('<', '&lt;')
            add_ph('ftr', 11, 'Quelle', f'<a:p><a:pPr algn="r"/><a:r>{run}<a:t>{src}</a:t></a:r></a:p>')
        add_ph('sldNum', 12, 'Foliennummer', f'<a:p><a:pPr algn="r"/><a:fld id="{{B6F15528-21DE-4FAA-801E-634DDDAF4B2B}}" type="slidenum">{run}<a:t>&#8249;#&#8250;</a:t></a:fld><a:endParaRPr lang="de-DE"/></a:p>')

    # ---------------------------------------------------------------- Inhalte
    def chart(self, s, kind, categories, series, highlight=None, alt=None, legend=None, labels=None, vmax=None, numfmt='General'):
        """kind: 'bar' (Säulen), 'stack' (gestapelt), 'line'. series: {Name: [Werte]} in Farbreihenfolge.
        highlight: Index einer Kategorie (Fokus-Muster, nur bei einer Reihe) – Rest grau."""
        ctype = {'bar': XL_CHART_TYPE.COLUMN_CLUSTERED, 'stack': XL_CHART_TYPE.COLUMN_STACKED, 'line': XL_CHART_TYPE.LINE}[kind]
        cd = CategoryChartData(); cd.categories = categories
        for name, vals in series.items(): cd.add_series(name, vals)
        gf = self.ph(s, 'chart').insert_chart(ctype, cd); gf.name = 'Diagramm'
        _set_alt(gf, alt or f'Diagramm: {", ".join(series)}')
        n = len(series)
        pc = None
        if highlight is not None and n == 1:
            pc = [SERIES[0] if i == highlight else CONTEXT for i in range(len(categories))]
        colors = SERIES[:n] if kind != 'line' or n > 2 else ([SERIES[0], NEUTRAL] if n == 2 else SERIES[:1])
        style_chart(gf.chart, kind, colors=colors, point_colors=pc, legend=(n > 1) if legend is None else legend,
                    labels=(kind != 'line') if labels is None else labels, vmax=vmax, numfmt=numfmt)
        return gf

    def table(self, s, rows, widths=None, numeric_cols=()):
        """rows[0] = Kopfzeile. numeric_cols: Spalten-Indizes rechtsbündig."""
        shp = self.ph(s, 'table'); left, top, width = shp.left, shp.top, shp.width
        gf = shp.insert_table(len(rows), len(rows[0])); gf.name = 'Tabelle'; tbl = gf.table
        tblPr = tbl._tbl.tblPr; tblPr.set('firstRow', '1'); tblPr.set('bandRow', '0')
        sid = tblPr.find(qn('a:tableStyleId'))
        if sid is None: sid = etree.SubElement(tblPr, qn('a:tableStyleId'))
        sid.text = TABLE_STYLE_ID
        widths = widths or [width / len(rows[0])] * len(rows[0])
        for j, w in enumerate(widths): tbl.columns[j].width = int(w if w > 100 else I(w))
        for i, row in enumerate(rows):
            tbl.rows[i].height = I(0.42 if i == 0 else 0.48)
            for j, val in enumerate(row):
                c = tbl.cell(i, j); c.margin_left = I(0 if j == 0 else 0.1); c.margin_right = I(0.1); c.vertical_anchor = MSO_ANCHOR.MIDDLE
                p = c.text_frame.paragraphs[0]; r = p.add_run(); r.text = str(val)
                if j in numeric_cols: p.alignment = PP_ALIGN.RIGHT
                _fmt_run(r, {'size': 11, 'caps': True, 'spc': 165, 'color': 'CCCCCC'} if i == 0 else ({'size': 14, 'bold': True, 'color': 'FFFFFF'} if j == 0 else {'size': 14, 'color': 'E6E6E6'}))
                tcPr = c._tc.get_or_add_tcPr()
                for t in ('a:lnL', 'a:lnR', 'a:lnT', 'a:lnB', 'a:solidFill', 'a:noFill'):
                    for old in tcPr.findall(qn(t)): tcPr.remove(old)
                col = '48484A' if i == 0 else '2C2C2E'
                for k, x in enumerate(etree.fromstring(f'<r xmlns:a="{A}"><a:lnL w="0"><a:noFill/></a:lnL><a:lnR w="0"><a:noFill/></a:lnR><a:lnT w="0"><a:noFill/></a:lnT><a:lnB w="9525"><a:solidFill><a:srgbClr val="{col}"/></a:solidFill></a:lnB></r>')):
                    tcPr.insert(k, x)
                etree.SubElement(tcPr, qn('a:noFill'))
        return gf

    def image(self, s, path, alt):
        """Bild in den Bild-Platzhalter; alt ist Pflicht."""
        pic = self.ph(s, 'image').insert_picture(str(path)); _set_alt(pic, alt); return pic

    # ---------------------------------------------------------------- Prüfen, Speichern
    def check(self):
        """Prüft Zeichengrenzen, leere Pflicht-Platzhalter, Aufzählungslänge und Folien ohne Quelle bei Daten."""
        out = []
        for no, (s, layout, content) in enumerate(self._filled, 1):
            sp = {p['role']: p for p in self.spec.get(layout, {}).get('placeholders', [])}
            for role, txt in content.items():
                lim = (sp.get(role) or {}).get('maxChars')
                longest = max((len(l) for l in txt.split('\n')), default=0)
                if lim and longest > lim * (sp[role].get('lines') or 1):
                    out.append(f'Folie {no} ({layout}): „{role}“ hat {longest} Zeichen, Grenze {lim} × {sp[role].get("lines") or 1} Zeile(n).')
                if role in ('body', 'text0', 'text1') and txt.count('\n') >= 5:
                    out.append(f'Folie {no} ({layout}): „{role}“ hat mehr als 5 Punkte.')
            for role in ('title',):
                if role in sp and role not in content and layout not in ('Leer',):
                    out.append(f'Folie {no} ({layout}): Pflichtrolle „{role}“ ist leer.')
            for p in s.placeholders:
                if p.placeholder_format.idx in (11, 12) or p.name.startswith('Leer:'): continue
                if p.has_text_frame and not p.text_frame.text.replace('\u200b', '').strip() and p.text_frame.text != '\u200b' and p.placeholder_format.type not in (PP_PLACEHOLDER.PICTURE, PP_PLACEHOLDER.CHART, PP_PLACEHOLDER.TABLE, PP_PLACEHOLDER.OBJECT):
                    out.append(f'Folie {no} ({layout}): Platzhalter „{p.name}“ ist leer – befüllen oder d.drop(slide, rolle).')
            if layout in ('Diagramm', 'Tabelle', 'KPI drei Zahlen') and not any(sh.name == 'Quelle' for sh in s.shapes):
                out.append(f'Folie {no} ({layout}): Datenfolie ohne Quelle (source=…).')
        return out

    def save(self, path):
        if self.sections:
            ids = {}
            for name, sid in self.sections: ids.setdefault(name, []).append(sid)
            xml = ''.join('<p14:section name="%s" id="{0B3A2C1D-0000-4000-8000-%012d}"><p14:sldIdLst>%s</p14:sldIdLst></p14:section>' % (n, i + 1, ''.join('<p14:sldId id="%d"/>' % x for x in v)) for i, (n, v) in enumerate(ids.items()))
            ext = etree.fromstring(f'<p:extLst xmlns:p="{P}"><p:ext uri="{{521415D9-36F7-43E2-AB2F-B90AF26B5E84}}"><p14:sectionLst xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main">{xml}</p14:sectionLst></p:ext></p:extLst>')
            pres = self.prs.part._element
            for old in pres.findall(qn('p:extLst')): pres.remove(old)
            pres.append(ext)
        self.prs.save(str(path)); return path

    def render_png(self, outdir, dpi=80):
        """Rendert jede Folie als PNG (LibreOffice + pdftoppm nötig) – danach jede Folie ansehen."""
        outdir = pathlib.Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
        tmp = outdir / '_deck.pptx'; self.save(tmp)
        subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', str(outdir), str(tmp)], check=True, capture_output=True)
        subprocess.run(['pdftoppm', '-png', '-r', str(dpi), str(outdir / '_deck.pdf'), str(outdir / 'folie')], check=True)
        tmp.unlink(); (outdir / '_deck.pdf').unlink()
        return sorted(outdir.glob('folie-*.png'))


