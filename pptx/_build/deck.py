import copy, json, subprocess
from lxml import etree
from pptx import Presentation
from pptx.util import Emu, Pt, Inches
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION, XL_TICK_MARK, XL_TICK_LABEL_POSITION
from pptx.oxml.ns import qn
import tpl
tpl.write_base('base.pptx')
ROLES={r['name']:r['map'] for r in json.load(open('roles.json'))} if False else None
L=tpl.build_layouts(); ROLES={l['name']:l['map'] for l in L}
prs=Presentation('base.pptx')
LAY={l.name:l for l in prs.slide_layouts}
A='http://schemas.openxmlformats.org/drawingml/2006/main'
P='http://schemas.openxmlformats.org/presentationml/2006/main'
def rgb(h): return RGBColor.from_string(h)
SERIES=['FFE94D','4797FF','EC3A78','2FCFC2','F5893A','B9A1FF','8FD46A']
def I(v): return Emu(int(round(v*914400)))

SECTIONS=[]
def new(layout,source=None,notes=None,section=None):
    s=prs.slides.add_slide(LAY[layout]); s._lname=layout
    # Fusszeile: Quelle + Foliennummer als echte Platzhalter
    lay=LAY[layout]
    have={p.placeholder_format.type for p in lay.placeholders}
    tree=s.shapes._spTree
    def add_ph(tp,idx,name,inner):
        xml=(f'<p:sp xmlns:p="{P}" xmlns:a="{A}"><p:nvSpPr><p:cNvPr id="{900+idx}" name="{name}"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr><p:ph type="{tp}" sz="quarter" idx="{idx}"/></p:nvPr></p:nvSpPr><p:spPr/><p:txBody><a:bodyPr/><a:lstStyle/>{inner}</p:txBody></p:sp>')
        tree.append(etree.fromstring(xml))
    from pptx.enum.shapes import PP_PLACEHOLDER as PH
    if PH.SLIDE_NUMBER in have:
        if source: add_ph('ftr',11,'Quelle',f'<a:p><a:pPr algn="r"/><a:r><a:rPr lang="de-DE" sz="1000" b="0" cap="all" spc="140"><a:solidFill><a:srgbClr val="8E8E93"/></a:solidFill><a:latin typeface="+mn-lt"/></a:rPr><a:t>{source}</a:t></a:r></a:p>')
        add_ph('sldNum',12,'Foliennummer','<a:p><a:pPr algn="r"/><a:fld id="{B6F15528-21DE-4FAA-801E-634DDDAF4B2B}" type="slidenum"><a:rPr lang="de-DE" sz="1000" cap="all" spc="140"><a:solidFill><a:srgbClr val="8E8E93"/></a:solidFill><a:latin typeface="+mn-lt"/></a:rPr><a:t>&#8249;#&#8250;</a:t></a:fld><a:endParaRPr lang="de-DE"/></a:p>')
    if notes: s.notes_slide.notes_text_frame.text=notes
    if section: SECTIONS.append((section,s.slide_id))
    return s
def ph(s,role):
    idx=ROLES[s._lname][role]
    for p in s.placeholders:
        if p.placeholder_format.idx==idx: return p
    raise KeyError(role)
def fmt_run(r,f):
    if 'color' in f: r.font.color.rgb=rgb(f['color'])
    if 'size' in f: r.font.size=Pt(f['size'])
    if 'bold' in f: r.font.bold=f['bold']
    rPr=r._r.get_or_add_rPr()
    if f.get('caps'): rPr.set('cap','all')
    if 'spc' in f: rPr.set('spc',str(f['spc']))
def put(s,role,content):
    shp=ph(s,role) if isinstance(role,str) else role
    tf=shp.text_frame
    paras=content if isinstance(content,list) else [content]
    for i,pc in enumerate(paras):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        runs=pc if isinstance(pc,list) else [(pc,{})]
        for t,f in runs:
            r=p.add_run(); r.text=t; fmt_run(r,f)
    return shp
def drop(s,role):
    shp=ph(s,role); shp._element.getparent().remove(shp._element)
def progress(s,k,n=7):
    for i in range(k+1):
        sh=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,I(tpl.seg_x(i,n)),I(0.3),I(tpl.seg_w(n)),I(0.04))
        sh.adjustments[0]=0.5; sh.fill.solid(); sh.fill.fore_color.rgb=rgb('FFFFFF'); sh.line.fill.background(); sh.name=f'Fortschritt aktiv {i+1}'; sh.shadow.inherit=False
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
# --- Charts ---
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
def add_chart(s,ctype,cats,series,alt='Diagramm',**kw):
    cd=CategoryChartData(); cd.categories=cats
    for n,v in series: cd.add_series(n,v)
    gf=ph(s,'chart').insert_chart(ctype,cd)
    gf.name='Diagramm'; set_alt(gf,alt)
    style_chart(gf.chart,**kw)
    return gf
def set_alt(shape_,txt):
    shape_._element.xpath('.//p:cNvPr')[0].set('descr',txt)

WH='FFFFFF'; MUT='A1A1A6'; SEC='CCCCCC'; ACC='FFE94D'
LBL={'size':11,'caps':True,'spc':165,'color':SEC}
CT={'size':20,'bold':True,'color':WH}
# 1 Titel
s=new('Titel',section='Einstieg')
put(s,'eyebrow','Präsentationsvorlage · ODSV 1.0')
t=put(s,'title','Design-System')
put(s,'sub','Ein Akzent. Eine Aussage pro Folie.')
put(s,'meta','Stand 17.11.2026 · Version 1.0')
# 2 Kapitel
s=new('Kapiteltrenner',source='Quelle: ODSV-Spezifikation',section='Kapitel')
progress(s,3)
put(s,'number','4'); put(s,'eyebrow','Kapitel 4 von 7'); put(s,'title','Layouts'); put(s,'sub','Sechzehn Masterlayouts für jeden Folientyp.')
# 3 Agenda
s=new('Agenda',section='Kapitel'); progress(s,0)
put(s,'eyebrow','Überblick'); put(s,'title','Agenda'); put(s,'sub','Sechs Kapitel, ein roter Faden.')
put(s,'body',['Grundlagen und Prinzipien','Farben und Typografie','Raster und Abstände','Layouts und Platzhalter','Diagramme und Tabellen','Prüfliste vor der Übergabe'])
aside=ph(s,'aside')
put(s,aside,[[('Dauer',LBL)],[('45 Minuten',{'size':20,'bold':True,'color':WH})],[('Format',LBL)],[('16:9, 13,33 × 7,5 in',{'size':20,'bold':True,'color':WH})],[('Umfang',LBL)],[('18 Folien',{'size':20,'bold':True,'color':WH})]])
for i,p in enumerate(aside.text_frame.paragraphs):
    p.space_after=Pt(4 if i%2==0 else 18)
# 4 Inhalt einspaltig
s=new('Inhalt einspaltig',source='Quelle: ODSV-Spezifikation',section='Inhalt'); progress(s,5)
put(s,'eyebrow','Grundprinzip'); put(s,'title','Eine Aussage'); put(s,'sub','Jede Folie beantwortet genau eine Frage.')
put(s,'body',['Der Titel formuliert die Kernaussage, nicht das Thema.','Höchstens fünf Aufzählungspunkte pro Folie.','Zahlen stehen immer mit Einheit und Quelle.','Gelb markiert nur das Wichtigste.','Details gehören in die Notizen oder den Anhang.'])
aside=ph(s,'aside')
put(s,aside,[[('Hinweis',LBL)],[('Platzhalter nutzen',CT)],[('Texte nur in die vorgesehenen Platzhalter setzen. So bleiben Gliederung, Lesereihenfolge und Layoutwechsel intakt.',{'color':MUT})]])
aside.text_frame.paragraphs[0].space_after=Pt(6); aside.text_frame.paragraphs[1].space_after=Pt(10)
# 5 Zwei Spalten
s=new('Zwei Spalten',section='Inhalt'); progress(s,2)
put(s,'eyebrow','Gegenüberstellung'); put(s,'title','Zwei Spalten'); put(s,'sub','Zwei gleichwertige Inhalte nebeneinander.')
put(s,'label0','Ausgangslage'); put(s,'title0','Was heute gilt')
put(s,'text0',['Eigene Vorlagen je Team','Farben und Schriften frei gewählt','Diagramme ohne feste Farbreihenfolge','Hoher Abstimmungsaufwand'])
put(s,'label1','Zielbild'); put(s,'title1','Was künftig gilt')
put(s,'text1',['Eine Vorlage mit 16 Layouts','Theme-Farben und Arial als Standard','Feste Diagrammpalette in sechs Farben','Prüfliste vor jeder Übergabe'])
# 6 KPI
s=new('KPI drei Zahlen',source='Beispieldaten – nicht für Auswertungen',section='Daten'); progress(s,1)
put(s,'eyebrow','Beispieldaten · Kennzahl'); put(s,'label','Zufriedenheit')
put(s,'value',[[('92',{}),(' %',{'color':WH})]])
put(s,'sentence','der Befragten bewerten die Vorlage als gut oder sehr gut.')
for k,(l,v) in enumerate((('Befragte','248'),('Rücklauf','61 %'),('Zeitraum','Q3 2026'))):
    put(s,f'tl{k}',l); put(s,f'tv{k}',v)
# 7 Diagramm Säule (Fokus)
s=new('Diagramm',source='Beispieldaten – nicht für Auswertungen',section='Daten'); progress(s,1)
put(s,'eyebrow','Beispieldaten · Säulen'); put(s,'title','Abstimmung dauert am längsten'); put(s,'sub','Zeitbedarf je Projektphase, in Tagen.')
cats=['Analyse','Konzept','Entwurf','Abstimmung','Review','Freigabe','Übergabe']; vals=[2,3,3,6,2,4,2]
add_chart(s,XL_CHART_TYPE.COLUMN_CLUSTERED,cats,[('Tage',vals)],alt='Säulendiagramm: Zeitbedarf je Projektphase in Tagen, Abstimmung am längsten (6)',kind='bar',point_colors=['636366' if v!=6 else ACC for v in vals],labels=True,vmax=8)
put(s,'ilabel','Kernaussage'); put(s,'itext','Eine Phase braucht doppelt so lange wie die meisten.'); put(s,'inote','Fokus-Muster: eine Säule in Gelb, alle anderen in Grau.')
# 8 Diagramm Linie (zwei Reihen)
s=new('Diagramm',source='Beispieldaten – nicht für Auswertungen',section='Daten'); progress(s,1)
put(s,'eyebrow','Beispieldaten · Linien'); put(s,'title','Aufrufe steigen im Herbst'); put(s,'sub','Seitenaufrufe je Monat, in Tausend.')
add_chart(s,XL_CHART_TYPE.LINE,['Jan','Feb','Mär','Apr','Mai','Jun','Jul','Aug','Sep','Okt','Nov'],[('2026',[3,3,4,4,5,5,6,7,9,12,14]),('2025',[2,2,3,3,3,4,4,5,6,8,9])],alt='Liniendiagramm: Aufrufe je Monat 2026 und 2025, 2026 liegt durchweg darüber',kind='line',colors=[ACC,'8E8E93'],legend=True,vmax=16)
put(s,'ilabel','Kernaussage'); put(s,'itext','Die Linie des laufenden Jahres liegt durchweg über dem Vorjahr.'); put(s,'inote','Vergleichsreihe in Grau, Marker nur am letzten Punkt.')
# 9 Diagramm gestapelt (4 Reihen in Reihenfolge)
s=new('Diagramm',source='Beispieldaten – nicht für Auswertungen',section='Daten'); progress(s,1)
put(s,'eyebrow','Beispieldaten · Gestapelt'); put(s,'title','Suche bringt die meisten Aufrufe'); put(s,'sub','Aufrufe nach Kanal und Quartal, in Tausend.')
add_chart(s,XL_CHART_TYPE.COLUMN_STACKED,['Q1','Q2','Q3','Q4'],[('Suche',[6,7,9,14]),('Direkt',[3,3,4,6]),('Verweise',[2,2,3,4]),('Sonstige',[1,1,2,2])],alt='Gestapeltes Säulendiagramm: Aufrufe nach Kanal und Quartal',kind='stack',legend=True,labels=True,colors=[ACC,'4797FF','EC3A78','2FCFC2'])
put(s,'ilabel','Kernaussage'); put(s,'itext','Farbreihenfolge: Gelb, Blau, Pink, Türkis.'); put(s,'inote','Reihenfolge nie umsortieren. Höchstens 4 Reihen direkt beschriftet.')
# 10 Bild vollflächig
s=new('Bild vollflächig',section='Bild')
pic=ph(s,'image').insert_picture('assets/foto-platzhalter.jpg'); set_alt(pic,'Platzhalterbild: abstrakter Horizont als Linienzeichnung vor dunklem Farbverlauf')
ov=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,0,I(7.5*0.55),I(13.333),I(7.5*0.45)); ov.name='Verlauf unten (Lesbarkeit)'; ov.line.fill.background(); ov.shadow.inherit=False
sp=ov._element.spPr
for c in list(sp):
    if c.tag in (qn('a:solidFill'),qn('a:noFill')): sp.remove(c)
grad=etree.fromstring(f'<a:gradFill xmlns:a="{A}" rotWithShape="1"><a:gsLst><a:gs pos="0"><a:srgbClr val="000000"><a:alpha val="0"/></a:srgbClr></a:gs><a:gs pos="100000"><a:srgbClr val="000000"><a:alpha val="85000"/></a:srgbClr></a:gs></a:gsLst><a:lin ang="5400000" scaled="0"/></a:gradFill>')
sp.find(qn('a:prstGeom')).addnext(grad)
# Verlauf unter Text legen: direkt hinter die Texte (nach dem Bild)
tree=s.shapes._spTree; tree.remove(ov._element); pic._element.addnext(ov._element)
put(s,'eyebrow','Bildfolie'); put(s,'title','Ein Bild, ein Satz'); put(s,'sub','Text steht nur auf dem abgedunkelten Bereich.')
# 11 Bild in Karte
s=new('Bild in Karte',source='Platzhalterbild',section='Bild'); progress(s,3)
put(s,'eyebrow','Bild und Text'); put(s,'title','Bild in Karte')
put(s,'body',['Das Bild sitzt in einer Karte mit 28 pt Radius.','Der Text links erklärt, was das Bild zeigt.','Jedes Bild bekommt einen Alternativtext.'])
pic=ph(s,'image').insert_picture('assets/foto-platzhalter.jpg'); set_alt(pic,'Platzhalterbild: abstrakte Linienzeichnung')
pg=pic._element.spPr.find(qn('a:prstGeom'))
if pg is None:
    pg=etree.fromstring(f'<a:prstGeom xmlns:a="{A}" prst="roundRect"><a:avLst><a:gd name="adj" fmla="val 6512"/></a:avLst></a:prstGeom>'); pic._element.spPr.append(pg)
ln=etree.fromstring(f'<a:ln xmlns:a="{A}" w="9525"><a:solidFill><a:srgbClr val="2C2C2E"/></a:solidFill></a:ln>'); pic._element.spPr.append(ln)
# 12 Zitat
s=new('Zitat',source='Quelle: Dieter Rams, „Weniger, aber besser“ (1995)',section='Inhalt'); progress(s,4)
put(s,'quote','Weniger, aber besser.')
put(s,'name','Dieter Rams'); put(s,'role','Industriedesigner')
# 13 Prozess
s=new('Prozess vier Schritte',section='Inhalt'); progress(s,3)
for i in range(4):
    sh=shape(s,MSO_SHAPE.ROUNDED_RECTANGLE,tpl.seg_x(i,4),2.2,tpl.seg_w(4),0.04,fill='FFFFFF',name=f'Schritt-Segment aktiv {i+1}',adj=0.5)
put(s,'eyebrow','Vorgehen'); put(s,'title','In vier Schritten'); put(s,'sub','Von der Gliederung zur fertigen Präsentation.')
steps=[('list','Gliedern','Kernaussagen festlegen, eine pro Folie.'),('layout','Layout wählen','Passendes Masterlayout aus der Vorlage einsetzen.'),('chart','Inhalte füllen','Texte und Diagramme in die Platzhalter setzen.'),('check','Prüfen','Folien rendern und jede einzeln ansehen.')]
for k,(ic,t,x) in enumerate(steps):
    put(s,f'n{k}',str(k+1)); put(s,f't{k}',t); put(s,f'x{k}',x)
    icon(s,ic,tpl.MX+k*3.05+0.28,2.95)
# 14 Vergleich
s=new('Vergleich',section='Inhalt'); progress(s,4)
put(s,'eyebrow','Häufiger Fehler'); put(s,'title','Richtig / Falsch'); put(s,'sub','Platzhalter nutzen. Keine freien Textfelder.')
put(s,'head0','Richtig'); put(s,'title0','Im Platzhalter'); put(s,'text0',['Text erbt Schrift, Größe und Farbe.','Die Lesereihenfolge bleibt erhalten.','Layoutwechsel ohne Nacharbeit.'])
put(s,'head1','Falsch'); put(s,'title1','Freies Textfeld'); put(s,'text1',['Formatierung muss von Hand gepflegt werden.','Screenreader lesen in falscher Reihenfolge.','Beim Layoutwechsel verrutscht der Inhalt.'])
icon(s,'ok',tpl.MX+0.3,2.62); icon(s,'no',6.767+0.3,2.62)
rr(s,tpl.MX,2.35,5.9,4.3,0.28,ACC,lw=1.5,name='Empfehlung (Rand)')
# 15 Tabelle
s=new('Tabelle',source='Quelle: ODSV-Spezifikation, Kapitel 9',section='Daten'); progress(s,1)
put(s,'eyebrow','Referenz'); put(s,'title','Textstile'); put(s,'sub','Größen und Laufweiten der Folientypografie.')
rows=[('Textstil','Größe','Hinweis'),('Kapitel','54 pt','Versalien, Laufweite 0,2 em'),('Display','44 pt','Versalien, Laufweite 0,2 em'),('Headline','28 pt','Versalien, Laufweite 0,15 em'),('Untertitel','18 pt','Grau, Satzschreibung'),('Fließtext','18 pt','Zeilenabstand 1,4'),('Eyebrow','12 pt','Versalien, Laufweite 0,2 em')]
gf=ph(s,'table').insert_table(len(rows),3); gf.name='Tabelle'
tbl=gf.table
tblPr=tbl._tbl.tblPr
for a in ('bandRow','firstRow','firstCol'): tblPr.set(a,'1' if a!='bandRow' else '0')
sid=tblPr.find(qn('a:tableStyleId'))
if sid is None: sid=etree.SubElement(tblPr,qn('a:tableStyleId'))
sid.text=tpl.TABLE_STYLE_ID
gf.width=I(12.0); gf.left=I(tpl.MX); gf.top=I(2.35)
for j,w in enumerate((3.4,3.6,5.0)): tbl.columns[j].width=I(w)
def cell_border(c,bottom,color):
    tcPr=c._tc.get_or_add_tcPr()
    for t in ('a:lnL','a:lnR','a:lnT','a:lnB'):
        for old in tcPr.findall(qn(t)): tcPr.remove(old)
    xml=''
    for t in ('lnL','lnR','lnT'): xml+=f'<a:{t} xmlns:a="{A}" w="0"><a:noFill/></a:{t}>'
    xml+=f'<a:lnB xmlns:a="{A}" w="9525"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill></a:lnB>'
    els=[etree.fromstring(f'<root xmlns:a="{A}">{xml}</root>')[i] for i in range(4)]
    for i,el in enumerate(els): tcPr.insert(i,el)
    for f in tcPr.findall(qn('a:solidFill')): tcPr.remove(f)
    nf=etree.SubElement(tcPr,qn('a:noFill'))
for i,row in enumerate(rows):
    tbl.rows[i].height=I(0.42 if i==0 else 0.48)
    for j,val in enumerate(row):
        c=tbl.cell(i,j); c.margin_left=c.margin_right=0 if j==0 else I(0.1); c.margin_left=I(0.0 if j==0 else 0.1); c.vertical_anchor=__import__('pptx.enum.text',fromlist=['x']).MSO_ANCHOR.MIDDLE
        p=c.text_frame.paragraphs[0]; r=p.add_run(); r.text=val
        if i==0: fmt_run(r,{'size':11,'caps':True,'spc':165,'color':SEC})
        elif j==0: fmt_run(r,{'size':14,'bold':True,'color':WH})
        else: fmt_run(r,{'size':14,'color':'E6E6E6' if j==1 else MUT})
        if j==1: p.alignment=__import__('pptx.enum.text',fromlist=['x']).PP_ALIGN.RIGHT if False else None
        cell_border(c,True,'48484A' if i==0 else '2C2C2E')
# 16 Nur Titel: Komponenten
s=new('Nur Titel',section='Komponenten'); progress(s,5)
put(s,'eyebrow','Bausteine'); put(s,'title','Freie Gestaltung'); put(s,'sub','Karten, Kacheln, Chips und Buttons in ODSV-Maßen.')
x0=tpl.MX
# Karte mit Icon-Kachel (gelber Verlauf)
c=rr(s,x0,2.35,3.867,4.3,0.28,'2C2C2E',lw=0.75,name='Karte',fill='1C1C1E')
tile=rr(s,x0+0.3,2.65,1.0,1.0,0.23,None,name='Icon-Kachel',fill='FFD84D'); tile.line.fill.background()
spp=tile._element.spPr; 
for cc in list(spp):
    if cc.tag==qn('a:solidFill'): spp.remove(cc)
spp.find(qn('a:prstGeom')).addnext(etree.fromstring(f'<a:gradFill xmlns:a="{A}" rotWithShape="1"><a:gsLst><a:gs pos="0"><a:srgbClr val="FFD84D"/></a:gs><a:gs pos="100000"><a:srgbClr val="E0A800"/></a:gs></a:gsLst><a:lin ang="3600000" scaled="0"/></a:gradFill>'))
cxx,cyy=x0+0.7,3.15
for r_ in (0.12,0.24,0.36): arc(s,cxx-r_,cyy-r_,2*r_,2*r_,-50,50,'1A1500',lw=2.25,name='Icon Signal')
circ(s,cxx,cyy,0.045,'1A1500',fill='1A1500',name='Icon Punkt')
tb=s.shapes.add_textbox(I(x0+0.3),I(3.95),I(3.267),I(2.4)); tb.name='Kartentext'; tf=tb.text_frame; tf.word_wrap=True
tf.margin_left=tf.margin_right=tf.margin_top=tf.margin_bottom=0
p=tf.paragraphs[0]; r=p.add_run(); r.text='Kartentitel'; fmt_run(r,CT); p.space_after=Pt(8)
p=tf.add_paragraph(); r=p.add_run(); r.text='Karte: 28 pt Radius, Füllung Dunkelgrau, Rand 0,75 pt, Innenabstand 0,3 in.'; fmt_run(r,{'size':16,'color':MUT})
# Chips
cx=x0+4.067
tb=s.shapes.add_textbox(I(cx),I(2.35),I(3.867),I(0.3)); tb.name='Label'; tf=tb.text_frame; tf.word_wrap=True; tf.margin_left=tf.margin_top=tf.margin_right=tf.margin_bottom=0
r=tf.paragraphs[0].add_run(); r.text='Chips'; fmt_run(r,LBL)
for i,(t,fill,fc) in enumerate((('Neu',ACC,'000000'),('Pflicht','FFFFFF','000000'),('Optional','2C2C2E','FFFFFF'))):
    w=0.45+0.12*len(t)
    xx=cx+sum(0.45+0.12*len(q)+0.15 for q in ('Neu','Pflicht','Optional')[:i])
    ch=rr(s,xx,2.8,w,0.34,0.17,None,name=f'Chip {t}',fill=fill); ch.line.fill.background()
    ch.text_frame.margin_left=ch.text_frame.margin_right=0
    pp=ch.text_frame.paragraphs[0]; pp.alignment=__import__('pptx.enum.text',fromlist=['x']).PP_ALIGN.CENTER; rr_=pp.add_run(); rr_.text=t; fmt_run(rr_,{'size':10,'bold':True,'caps':True,'spc':120,'color':fc})
tb=s.shapes.add_textbox(I(cx),I(3.6),I(3.867),I(0.3)); tb.name='Label'; tf=tb.text_frame; tf.word_wrap=True; tf.margin_left=tf.margin_top=tf.margin_right=tf.margin_bottom=0
r=tf.paragraphs[0].add_run(); r.text='Buttons'; fmt_run(r,LBL)
b1=rr(s,cx,4.05,2.4,0.6,0.15,None,name='Button primär',fill='FFE94D'); b1.line.fill.background()
b1.text_frame.margin_left=b1.text_frame.margin_right=0
pp=b1.text_frame.paragraphs[0]; pp.alignment=__import__('pptx.enum.text',fromlist=['x']).PP_ALIGN.CENTER; rr_=pp.add_run(); rr_.text='Jetzt starten'; fmt_run(rr_,{'size':18,'bold':True,'color':'000000'})
b2=rr(s,cx,4.85,2.4,0.6,0.15,'48484A',lw=1.25,name='Button sekundär')
b2.text_frame.margin_left=b2.text_frame.margin_right=0
pp=b2.text_frame.paragraphs[0]; pp.alignment=__import__('pptx.enum.text',fromlist=['x']).PP_ALIGN.CENTER; rr_=pp.add_run(); rr_.text='Mehr erfahren'; fmt_run(rr_,{'size':18,'bold':True,'color':'FFFFFF'})
# Signet-Verlauf als Linie (Segmente)
sx=x0+8.133
tb=s.shapes.add_textbox(I(sx),I(2.35),I(3.867),I(0.3)); tb.name='Label'; tf=tb.text_frame; tf.word_wrap=True; tf.margin_left=tf.margin_top=tf.margin_right=tf.margin_bottom=0
r=tf.paragraphs[0].add_run(); r.text='Signet-Farben'; fmt_run(r,LBL)
for i,cc in enumerate(('EC3A78','EE6A2C','F09A35','F3C340','FFE94D')):
    sh=rr(s,sx+i*0.78,2.8,0.7,0.7,0.35,None,name=f'Signet-Farbe {i+1}',fill=cc); sh.line.fill.background()
tb=s.shapes.add_textbox(I(sx),I(3.8),I(3.867),I(2.5)); tb.name='Hinweis'; tf=tb.text_frame; tf.word_wrap=True; tf.margin_left=tf.margin_top=tf.margin_right=tf.margin_bottom=0
r=tf.paragraphs[0].add_run(); r.text='Der Verlauf Pink → Orange → Gelb gehört nur auf Titelfolie, Kapiteltrenner und Signet – nie auf Flächen oder Text.'; fmt_run(r,{'size':16,'color':MUT})
# 17 Leer
s=new('Leer',section='Komponenten'); progress(s,6)
tb=s.shapes.add_textbox(I(tpl.MX),I(3.3),I(12.0),I(0.9)); tb.name='Hinweis'; tf=tb.text_frame; tf.word_wrap=True; tf.margin_left=tf.margin_right=0
p=tf.paragraphs[0]; r=p.add_run(); r.text='Leere Folie'; fmt_run(r,{'size':12,'caps':True,'spc':240,'color':SEC}); p.space_after=Pt(10)
p=tf.add_paragraph(); r=p.add_run(); r.text='Schwarzer Grund, Fortschrittsleiste und Seitenfuß – der Rest gehört dir.'; fmt_run(r,{'size':24,'color':MUT})
# 18 Abschluss
s=new('Abschluss',section='Abschluss')
put(s,'prompt','Fertig. Jetzt die Prüfliste durchgehen.'); put(s,'button','Zur Prüfliste'); put(s,'contact','Fragen zur Vorlage? Siehe ODSV-Spezifikation, Kapitel 9.')

# Abschnitte (Sections) schreiben
ids_by_section={}
for name,sid in SECTIONS: ids_by_section.setdefault(name,[]).append(sid)
ext=etree.fromstring('<p:extLst xmlns:p="%s"><p:ext uri="{521415D9-36F7-43E2-AB2F-B90AF26B5E84}"><p14:sectionLst xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main">%s</p14:sectionLst></p:ext></p:extLst>'%(P,''.join('<p14:section name="%s" id="{%s}"><p14:sldIdLst>%s</p14:sldIdLst></p14:section>'%(n,'0B3A2C1D-0000-4000-8000-%012d'%(i+1),''.join('<p14:sldId id="%d"/>'%x for x in v)) for i,(n,v) in enumerate(ids_by_section.items()))))
prs.part._element.append(ext)
prs.save('../ODSV-Vorlage.pptx'); print('saved',len(prs.slides._sldIdLst))
