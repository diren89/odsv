# ODSV – Vorlagen-Paket (Theme, Master, Layouts) als rohes OOXML erzeugen
import zipfile, json
from xml.sax.saxutils import escape
EMU=914400
def e(v): return int(round(v*EMU))
NS='xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
T=json.load(open('/home/claude/odsv/tokens/pptx.json'))
CS=T['themes']['dark']['colorScheme']
BORDER='2C2C2E'
COLORS={'tx1':'<a:schemeClr val="tx1"/>','tx2':'<a:schemeClr val="tx2"/>','acc':'<a:schemeClr val="accent1"/>',
 'body':'<a:srgbClr val="E6E6E6"/>','sec':'<a:srgbClr val="CCCCCC"/>','faint':'<a:srgbClr val="8E8E93"/>','on':'<a:schemeClr val="bg1"/>'}
# key: (sz, bold, cap, spc, color, font, lnSpc%, spcAft pt, algn)
ST={
 'eyebrow':(12,0,1,240,'sec','mn',120,0,'l'),
 'headline':(28,1,1,420,'tx1','mj',120,0,'l'),
 'display':(44,1,1,880,'tx1','mj',115,0,'l'),
 'chapter':(54,1,1,1080,'tx1','mj',115,0,'l'),
 'sub':(18,0,0,0,'tx2','mn',130,0,'l'),
 'sub-large':(24,0,0,0,'tx2','mn',130,0,'l'),
 'body':(18,0,0,0,'body','mn',140,8,'l'),
 'body-small':(16,0,0,0,'body','mn',135,8,'l'),
 'body-small-muted':(16,0,0,0,'tx2','mn',135,6,'l'),
 'card-title':(20,1,0,0,'tx1','mj',120,0,'l'),
 'label':(11,0,1,165,'sec','mn',120,0,'l'),
 'kpi-hero':(120,1,0,0,'acc','mj',100,0,'l'),
 'kpi-tile':(28,1,0,0,'tx1','mj',110,0,'l'),
 'number-large':(72,1,0,0,'tx1','mj',100,0,'r'),
 'number':(40,1,0,0,'tx1','mj',100,0,'r'),
 'quote':(32,0,0,0,'tx1','mn',130,0,'l'),
 'agenda':(24,0,0,0,'tx1','mn',120,17.3,'l'),
 'button':(18,1,0,0,'on','mn',120,0,'ctr'),
 'prompt':(28,1,0,0,'tx1','mj',120,0,'ctr'),
 'contact':(16,0,0,0,'tx2','mn',135,0,'ctr'),
 'card-text':(16,0,0,0,'body','mn',135,8,'l'),
 'caption':(12,0,0,0,'faint','mn',120,0,'l'),
 'footer':(10,0,1,140,'faint','mn',120,0,'l'),
 'footer-r':(10,0,1,140,'faint','mn',120,0,'r'),
 'footer-c':(10,0,1,140,'faint','mn',120,0,'ctr'),
}
def defrpr(key,tag='a:defRPr'):
    sz,b,cap,spc,col,font,ln,aft,al=ST[key]
    a=f'<{tag} lang="de-DE" sz="{int(sz*100)}" b="{b}"'+(' cap="all"' if cap else ' cap="none"')+f' spc="{spc}" baseline="0"><a:solidFill>{COLORS[col]}</a:solidFill><a:latin typeface="+{font}-lt"/><a:ea typeface="+{font}-ea"/><a:cs typeface="+{font}-cs"/></{tag}>'
    return a
def lvl(key,bullet=None,marL=0,indent=0,n=1):
    sz,b,cap,spc,col,font,ln,aft,al=ST[key]
    bu='<a:buNone/>'
    if bullet=='dot': bu='<a:buClr><a:schemeClr val="accent1"/></a:buClr><a:buSzPct val="100000"/><a:buFont typeface="Arial"/><a:buChar char="&#8226;"/>'
    if bullet=='num': bu='<a:buClr><a:srgbClr val="A1A1A6"/></a:buClr><a:buSzPct val="100000"/><a:buFont typeface="+mj-lt"/><a:buAutoNum type="arabicPlain"/>'
    return (f'<a:lvl{n}pPr marL="{e(marL)}" indent="{e(indent)}" algn="{al}"><a:lnSpc><a:spcPct val="{ln*1000}"/></a:lnSpc><a:spcBef><a:spcPts val="0"/></a:spcBef>'
            f'<a:spcAft><a:spcPts val="{int(aft*100)}"/></a:spcAft>{bu}{defrpr(key)}</a:lvl{n}pPr>')
def lst(key,bullet=None,marL=0,indent=0):
    return '<a:lstStyle>'+lvl(key,bullet,marL,indent)+'</a:lstStyle>'
class Ids:
    def __init__(s): s.n=1
    def __call__(s): s.n+=1; return s.n
def adj(r,w,h): return min(50000,int(round(r/min(w,h)*100000)))
def geom(shape,w,h,r):
    if shape=='round': return f'<a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val {adj(r,w,h)}"/></a:avLst></a:prstGeom>'
    return f'<a:prstGeom prst="{shape}"><a:avLst/></a:prstGeom>'
def fillx(f):
    if f is None: return '<a:noFill/>'
    if f=='card': return '<a:solidFill><a:schemeClr val="bg2"/></a:solidFill>'
    if f=='card2': return '<a:solidFill><a:srgbClr val="232325"/></a:solidFill>'
    if f=='acc': return '<a:solidFill><a:schemeClr val="accent1"/></a:solidFill>'
    if f=='btn': return '<a:gradFill rotWithShape="1"><a:gsLst><a:gs pos="0"><a:srgbClr val="FFE94D"/></a:gs><a:gs pos="100000"><a:srgbClr val="F5D400"/></a:gs></a:gsLst><a:lin ang="5400000" scaled="0"/></a:gradFill>'
    if f=='track': return '<a:solidFill><a:srgbClr val="616161"/></a:solidFill>'
    if f=='border': return '<a:solidFill><a:srgbClr val="2C2C2E"/></a:solidFill>'
    if f=='strong': return '<a:solidFill><a:srgbClr val="48484A"/></a:solidFill>'
    if f=='sub': return '<a:solidFill><a:srgbClr val="0A0A0A"/></a:solidFill>'
    if f=='white': return '<a:solidFill><a:schemeClr val="tx1"/></a:solidFill>'
    raise ValueError(f)
def lnx(l):
    if l is None: return '<a:ln><a:noFill/></a:ln>'
    return f'<a:ln w="9525"><a:solidFill><a:srgbClr val="{ {"border":"2C2C2E","strong":"48484A"}[l]}"/></a:solidFill></a:ln>'
def ph(ids,name,ptype,idx,box,style=None,prompt='',bullet=None,marL=0,indent=0,shape=None,r=0.28,fill=None,line=None,pad=(0,0,0,0),anchor='t',extra_lvl=''):
    x,y,w,h=box
    i=ids()
    typ=f' type="{ptype}"' if ptype else ''
    idxa=f' idx="{idx}"' if idx else ''
    sz=' sz="quarter"' if ptype in ('body',None,'chart','tbl','pic') and idx else ''
    sp=f'<a:xfrm><a:off x="{e(x)}" y="{e(y)}"/><a:ext cx="{e(w)}" cy="{e(h)}"/></a:xfrm>'
    if shape: sp+=geom(shape,w,h,r)
    if fill or shape: sp+=fillx(fill)+lnx(line)
    l,t,rr,b=pad
    body=f'<a:bodyPr lIns="{e(l)}" tIns="{e(t)}" rIns="{e(rr)}" bIns="{e(b)}" anchor="{anchor}"><a:noAutofit/></a:bodyPr>'
    ls=lst(style,bullet,marL,indent)[:-len('</a:lstStyle>')]+extra_lvl+'</a:lstStyle>' if style else '<a:lstStyle/>'
    prompt_x=f'<a:p><a:r><a:rPr lang="de-DE"/><a:t>{escape(prompt)}</a:t></a:r></a:p>' if prompt else '<a:p><a:endParaRPr lang="de-DE"/></a:p>'
    if ptype=='sldNum':
        prompt_x='<a:p><a:fld id="{B6F15528-21DE-4FAA-801E-634DDDAF4B2B}" type="slidenum"><a:rPr lang="de-DE"/><a:t>&#8249;#&#8250;</a:t></a:fld><a:endParaRPr lang="de-DE"/></a:p>'
    if ptype in ('pic','chart','tbl'):
        body='<a:bodyPr/>'
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="{escape(name)}"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr><p:ph{typ}{idxa}{sz}/></p:nvPr></p:nvSpPr>'
            f'<p:spPr>{sp}</p:spPr><p:txBody>{body}{ls}{prompt_x}</p:txBody></p:sp>')
def shp(ids,name,box,shape='rect',r=0.28,fill=None,line=None,lw=None,text=None):
    x,y,w,h=box; i=ids()
    ln=lnx(line)
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="{escape(name)}"/><p:cNvSpPr/><p:nvPr userDrawn="1"/></p:nvSpPr><p:spPr><a:xfrm><a:off x="{e(x)}" y="{e(y)}"/><a:ext cx="{e(w)}" cy="{e(h)}"/></a:xfrm>'
            f'{geom(shape,w,h,r)}{fillx(fill)}{ln}</p:spPr></p:sp>')
def hline(ids,name,x,y,w,color='border'):
    i=ids()
    return (f'<p:cxnSp><p:nvCxnSpPr><p:cNvPr id="{i}" name="{name}"/><p:cNvCxnSpPr/><p:nvPr userDrawn="1"/></p:nvCxnSpPr><p:spPr><a:xfrm><a:off x="{e(x)}" y="{e(y)}"/><a:ext cx="{e(w)}" cy="0"/></a:xfrm><a:prstGeom prst="line"><a:avLst/></a:prstGeom>'
            f'<a:ln w="9525">{fillx(color)}</a:ln></p:spPr></p:cxnSp>')
def text(ids,name,box,txt,style,align=None,anchor='t',spc=None,color=None):
    x,y,w,h=box; i=ids()
    sz,b,cap,sp,col,font,ln,aft,al=ST[style]
    al=align or al
    sp=sp if spc is None else spc
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="{escape(name)}"/><p:cNvSpPr txBox="1"/><p:nvPr userDrawn="1"/></p:nvSpPr><p:spPr><a:xfrm><a:off x="{e(x)}" y="{e(y)}"/><a:ext cx="{e(w)}" cy="{e(h)}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>'
            f'<p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" anchor="{anchor}"><a:noAutofit/></a:bodyPr><a:lstStyle/><a:p><a:pPr algn="{al}"/><a:r><a:rPr lang="de-DE" sz="{int(sz*100)}" b="{b}"'+(' cap="all"' if cap else '')+f' spc="{sp}"><a:solidFill>{COLORS[color or col]}</a:solidFill><a:latin typeface="+{font}-lt"/></a:rPr><a:t>{escape(txt)}</a:t></a:r></a:p></p:txBody></p:sp>')
def pic(ids,name,rid,box,descr,shape=None,r=0.28,line=None):
    x,y,w,h=box; i=ids()
    g=geom(shape,w,h,r) if shape else '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
    return (f'<p:pic><p:nvPicPr><p:cNvPr id="{i}" name="{name}" descr="{escape(descr)}"/><p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr userDrawn="1"/></p:nvPicPr>'
            f'<p:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill><p:spPr><a:xfrm><a:off x="{e(x)}" y="{e(y)}"/><a:ext cx="{e(w)}" cy="{e(h)}"/></a:xfrm>{g}{lnx(line)}</p:spPr></p:pic>')
GRP='<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'

# ---------- Raster ----------
MX=0.667; CW=12.0
def col_x(c): return MX+(c-1)*(0.8167+0.2)
def span_w(n): return n*0.8167+(n-1)*0.2
SEG_N=7; SEG_GAP=0.08
def seg_w(n): return (CW-(n-1)*SEG_GAP)/n
def seg_x(i,n): return MX+i*(seg_w(n)+SEG_GAP)

# ---------- Layout-Bausteine ----------
def progress_track(ids,n=7,y=0.3,name='Fortschritt'):
    out=''
    for i in range(n):
        out+=shp(ids,f'{name} Segment {i+1}',(seg_x(i,n),y,seg_w(n),0.04),'round',r=0.02,fill='track')
    return out
def head(ids,m,headline_prompt='Headline in Versalien',sub=True,eyebrow_y=0.62,hl_y=0.95,sub_y=1.65):
    s=ph(ids,'Eyebrow','body',13,(MX,eyebrow_y,12.0,0.3),'eyebrow','Eyebrow')
    s+=ph(ids,'Headline','title',0,(MX,hl_y,12.0,0.7),'headline',headline_prompt)
    m['eyebrow']=13; m['title']=0
    if sub:
        s+=ph(ids,'Zweitsatz','body',14,(MX,sub_y,8.95,0.45),'sub','Zweitsatz in normaler Schreibweise'); m['sub']=14
    return s
FOOT=lambda ids:(ph(ids,'Quelle','ftr',11,(4.733,6.95,5.9,0.25),'footer-r','')+ph(ids,'Foliennummer','sldNum',12,(11.85,6.95,0.817,0.25),'footer-r',''))
def card(ids,name,box,r=0.28,fill='card',line='border'): return shp(ids,name,box,'round',r,fill,line)

def build_layouts():
    L=[]  # (name, xml_body, showMaster, rels, maproles, type)
    def add(name,body,show=True,rels=None,m=None,typ=None,foot=True): L.append(dict(name=name,body=body,show=show,rels=rels or [],map=m or {},type=typ,foot=foot))
    # 1 Titel
    ids=Ids(); m={}
    b=pic(ids,'Signet-Karte','rId2',(7.783,0.667,4.883,6.167),'Signet: konzentrische Bögen im Verlauf Pink, Orange, Gelb',shape='round',r=0.28,line='border')
    b+=text(ids,'Wortmarke Signet',(8.083,6.14,3.0,0.3),'ODSV','footer',spc=140)
    b+=ph(ids,'Eyebrow','body',13,(MX,2.25,6.917,0.3),'eyebrow','Eyebrow'); m['eyebrow']=13
    b+=ph(ids,'Titel','ctrTitle',0,(MX,2.65,6.917,1.75),'display','Titel'); m['title']=0
    b+=ph(ids,'Untertitel','subTitle',1,(MX,4.55,5.9,0.9),'sub-large','Untertitel in einem Satz'); m['sub']=1
    b+=ph(ids,'Meta','body',14,(MX,6.35,5.9,0.3),'eyebrow','Autor · Datum'); m['meta']=14
    add('Titel',b,show=False,rels=[('rId2','assets/signet-card.png')],m=m,typ='title',foot=False)
    # 2 Kapitel
    ids=Ids(); m={}
    b=progress_track(ids)
    b+=pic(ids,'Signet-Marke','rId2',(11.617,5.08,1.05,1.561),'Signet-Marke')
    b+=ph(ids,'Kapitelnummer','body',13,(9.817,0.62,2.85,1.2),'number-large','1'); m['number']=13
    b+=ph(ids,'Eyebrow','body',14,(MX,2.55,12.0,0.3),'eyebrow','Kapitel'); m['eyebrow']=14
    b+=ph(ids,'Kapiteltitel','title',0,(MX,2.9,12.0,1.9),'chapter','Kapiteltitel'); m['title']=0
    b+=ph(ids,'Zweitsatz','body',15,(MX,4.95,7.933,0.6),'sub-large','Zweitsatz'); m['sub']=15
    add('Kapiteltrenner',b,rels=[('rId2','assets/signet-mark.png')],m=m)
    # 3 Agenda
    ids=Ids(); m={}
    b=progress_track(ids)+head(ids,m)
    for i in range(6): b+=hline(ids,f'Haarlinie {i+1}',MX,2.35+0.6+0.7*i,7.933)
    b+=ph(ids,'Agenda-Liste','body',15,(MX,2.35,7.933,4.2),'agenda','Punkt eins',bullet='num',marL=0.8,indent=-0.8); m['body']=15
    b+=ph(ids,'Hinweis-Karte','body',16,(8.8,2.35,3.867,4.2),'card-text','Hinweis, Zeitangaben oder leer',shape='round',r=0.28,fill='card',line='border',pad=(0.3,0.3,0.3,0.3)); m['aside']=16
    add('Agenda',b,m=m)
    # 4 Inhalt einspaltig
    ids=Ids(); m={}
    b=progress_track(ids)+head(ids,m)
    b+=ph(ids,'Text','body',15,(MX,2.35,7.933,4.3),'body','Höchstens 5 Punkte oder 80 Wörter',bullet='dot',marL=0.3,indent=-0.3); m['body']=15
    b+=ph(ids,'Hinweis-Karte','body',16,(8.8,2.35,3.867,4.3),'card-text','Icon, Hinweis oder leer',shape='round',r=0.28,fill='card',line='border',pad=(0.3,0.3,0.3,0.3)); m['aside']=16
    add('Inhalt einspaltig',b,m=m)
    # 5 Zwei Spalten
    ids=Ids(); m={}
    b=progress_track(ids)+head(ids,m)
    for k,(x,side) in enumerate(((MX,'links'),(6.767,'rechts'))):
        b+=card(ids,f'Karte {side}',(x,2.35,5.9,4.3))
        b+=ph(ids,f'Label {side}','body',15+3*k,(x+0.3,2.65,5.3,0.25),'label','Label'); m[f'label{k}']=15+3*k
        b+=ph(ids,f'Karten-Headline {side}','body',16+3*k,(x+0.3,3.0,5.3,0.5),'card-title','Karten-Headline'); m[f'title{k}']=16+3*k
        b+=ph(ids,f'Text {side}','body',17+3*k,(x+0.3,3.7,5.3,2.65),'card-text','Text 16 pt, höchstens 5 Zeilen'); m[f'text{k}']=17+3*k
    add('Zwei Spalten',b,m=m)
    # 6 KPI
    ids=Ids(); m={}
    b=progress_track(ids)
    b+=ph(ids,'Eyebrow','body',13,(MX,0.62,12.0,0.3),'eyebrow','Eyebrow'); m['eyebrow']=13
    b+=ph(ids,'Zahl-Label (Folientitel)','title',0,(MX,1.95,12.0,0.3),'label','Label'); m['label']=0
    b+=ph(ids,'Zahl','body',15,(MX,2.3,12.0,2.1,),'kpi-hero','12'); m['value']=15
    b+=ph(ids,'Aussage','body',16,(MX,4.5,10.0,0.7),'sub-large','Ein Satz zur Zahl'); m['sentence']=16
    for k in range(3):
        x=MX+k*(3.867+0.1)  # 3 Kacheln à 4 Spalten
        x=MX+k*(3.8667+0.2)
        b+=card(ids,f'Kachel {k+1}',(x,5.4,3.8667,1.25),0.2)
        b+=ph(ids,f'Kachel {k+1} Label','body',17+2*k,(x+0.3,5.62,3.3,0.25),'label','Label'); m[f'tl{k}']=17+2*k
        b+=ph(ids,f'Kachel {k+1} Wert','body',18+2*k,(x+0.3,5.95,3.3,0.5),'kpi-tile','Wert'); m[f'tv{k}']=18+2*k
    add('KPI drei Zahlen',b,m=m)
    # 7 Diagramm
    ids=Ids(); m={}
    b=progress_track(ids)+head(ids,m)
    b+=card(ids,'Diagramm-Rahmen',(MX,2.35,7.933,4.3))
    b+=ph(ids,'Diagramm','chart',15,(MX+0.3,2.65,7.333,3.7),None,'Diagramm einfügen'); m['chart']=15
    b+=card(ids,'Aussage-Karte',(8.8,2.35,3.867,4.3))
    b+=ph(ids,'Aussage-Label','body',16,(9.1,2.65,3.267,0.25),'label','Kernaussage'); m['ilabel']=16
    b+=ph(ids,'Aussage','body',17,(9.1,3.0,3.267,1.8),'card-title','Aussage in einem Satz'); m['itext']=17
    b+=ph(ids,'Erläuterung','body',18,(9.1,4.9,3.267,1.5),'body-small-muted','Erläuterung, höchstens 25 Wörter'); m['inote']=18
    add('Diagramm',b,m=m)
    # 8 Bild vollflächig
    ids=Ids(); m={}
    b=ph(ids,'Bild','pic',13,(0,0,13.333,7.5),None,'Bild einfügen (randabfallend)'); m['image']=13
    b+=ph(ids,'Eyebrow','body',14,(MX,5.3,12.0,0.3),'eyebrow','Eyebrow'); m['eyebrow']=14
    b+=ph(ids,'Headline','title',0,(MX,5.63,12.0,0.7),'headline','Headline in Versalien'); m['title']=0
    b+=ph(ids,'Zweitsatz','body',15,(MX,6.3,8.95,0.45),'sub','Zweitsatz'); m['sub']=15
    add('Bild vollflächig',b,show=False,m=m)
    # 9 Bild in Karte
    ids=Ids(); m={}
    b=progress_track(ids)+head(ids,m,sub=False)
    b+=ph(ids,'Text','body',15,(MX,2.35,4.883,4.3),'body-small','Text, höchstens 60 Wörter',bullet='dot',marL=0.3,indent=-0.3); m['body']=15
    b+=ph(ids,'Bild','pic',16,(6.767,2.35,5.9,4.3),None,'Bild einfügen',shape='round',r=0.28,line='border'); m['image']=16
    add('Bild in Karte',b,m=m)
    # 10 Zitat
    ids=Ids(); m={}
    b=progress_track(ids)
    b+=text(ids,'Anführungszeichen',(MX,1.95,1.2,1.2),'“','number-large',align='l',color='acc')
    b+=ph(ids,'Zitat','body',13,(1.683,2.1,9.967,2.9),'quote','Zitat, normale Schreibweise, höchstens 30 Wörter'); m['quote']=13
    b+=ph(ids,'Name','body',14,(1.683,5.2,9.967,0.3),'eyebrow','Name'); m['name']=14
    b+=ph(ids,'Rolle','body',15,(1.683,5.52,9.967,0.35),'body-small-muted','Rolle, Quelle'); m['role']=15
    add('Zitat',b,m=m)
    # 11 Prozess
    ids=Ids(); m={}
    b=progress_track(ids)+head(ids,m)
    for k in range(4):
        x=MX+k*(2.85+0.2)
        b+=shp(ids,f'Schritt-Segment {k+1}',(seg_x(k,4),2.2,seg_w(4),0.04),'round',r=0.02,fill='track')
        b+=card(ids,f'Schritt-Karte {k+1}',(x,2.4,2.85,4.25))
        b+=ph(ids,f'Schritt {k+1} Nummer','body',15+3*k,(x+2.85-0.28-1.2,2.4+0.2,1.2,0.65),'number',str(k+1)); m[f'n{k}']=15+3*k
        b+=ph(ids,f'Schritt {k+1} Titel','body',16+3*k,(x+0.28,4.5,2.29,0.8),'card-title','Schritt-Titel'); m[f't{k}']=16+3*k
        b+=ph(ids,f'Schritt {k+1} Text','body',17+3*k,(x+0.28,5.35,2.29,1.1),'body-small-muted','Ein Satz, höchstens 15 Wörter'); m[f'x{k}']=17+3*k
    add('Prozess vier Schritte',b,m=m)
    # 12 Vergleich
    ids=Ids(); m={}
    b=progress_track(ids)+head(ids,m)
    for k,(x,side) in enumerate(((MX,'A'),(6.767,'B'))):
        b+=card(ids,f'Karte {side}',(x,2.35,5.9,4.3))
        b+=ph(ids,f'Kopf {side}','body',15+3*k,(x+0.3+0.5,2.65,4.5,0.3),'label',f'Option {side}'); m[f'head{k}']=15+3*k
        b+=ph(ids,f'Titel {side}','body',16+3*k,(x+0.3,3.25,5.3,0.5),'card-title','Titel'); m[f'title{k}']=16+3*k
        b+=ph(ids,f'Zeilen {side}','body',17+3*k,(x+0.3,3.95,5.3,2.4),'card-text','Bis zu 5 Zeilen, 16 pt'); m[f'text{k}']=17+3*k
    add('Vergleich',b,m=m)
    # 13 Tabelle
    ids=Ids(); m={}
    b=progress_track(ids)+head(ids,m)
    b+=ph(ids,'Tabelle','tbl',15,(MX,2.35,12.0,4.3),None,'Tabelle einfügen'); m['table']=15
    add('Tabelle',b,m=m)
    # 14 Abschluss
    ids=Ids(); m={}
    b=shp(ids,'Sheet',(3.717,1.75,5.9,4.2),'round',0.28,'card','border')
    b+=shp(ids,'Grabber',(6.467,1.95,0.4,0.055),'round',r=0.0275,fill='strong')
    b+=ph(ids,'Aufforderung (Folientitel)','title',0,(4.117,2.35,5.1,1.5),'prompt','Eine Aufforderung, ein Button',anchor='ctr'); m['prompt']=0
    b+=ph(ids,'Button','body',14,(5.067,4.05,3.2,0.6),'button','Zur Checkliste',shape='round',r=0.15,fill='btn',anchor='ctr'); m['button']=14
    b+=ph(ids,'Kontakt','body',15,(4.117,4.95,5.1,0.6),'contact','Kontakt, E-Mail, Web'); m['contact']=15
    b+=text(ids,'Wortmarke',(MX,6.95,12.0,0.25),'ODSV','footer-c',spc=140)
    add('Abschluss',b,show=False,m=m,foot=False)
    # 15 Nur Titel
    ids=Ids(); m={}
    b=progress_track(ids)+head(ids,m)
    add('Nur Titel',b,m=m)
    # 16 Leer
    ids=Ids()
    add('Leer',progress_track(ids),m={})
    return L

def layout_xml(l):
    ids_extra=''
    foot=''
    if l['foot']:
        ids=Ids(); ids.n=90
        foot=FOOT(ids)
    typ=f' type="{l["type"]}"' if l['type'] else ''
    sm='' if l['show'] else ' showMasterSp="0"'
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<p:sldLayout {NS}{typ}{sm} preserve="1" userDrawn="1"><p:cSld name="{escape(l["name"])}"><p:spTree>{GRP}{l["body"]}{foot}</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>')

def theme_xml():
    c=CS
    def clr(k,v): return f'<a:{k}><a:srgbClr val="{v}"/></a:{k}>'
    cols=''.join(clr(k,c[k]) for k in ['dk1','lt1','dk2','lt2','accent1','accent2','accent3','accent4','accent5','accent6','hlink','folHlink'])
    fonts=lambda: '<a:latin typeface="Arial" panose="020B0604020202020204"/><a:ea typeface=""/><a:cs typeface=""/>'
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="ODSV Dark"><a:themeElements><a:clrScheme name="ODSV Dark">{cols}</a:clrScheme>
<a:fontScheme name="ODSV"><a:majorFont>{fonts()}</a:majorFont><a:minorFont>{fonts()}</a:minorFont></a:fontScheme>
<a:fmtScheme name="ODSV"><a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst>
<a:lnStyleLst><a:ln w="9525" cap="flat" cmpd="sng" algn="ctr"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:prstDash val="solid"/></a:ln><a:ln w="28575" cap="rnd" cmpd="sng" algn="ctr"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:prstDash val="solid"/><a:round/></a:ln><a:ln w="38100" cap="rnd" cmpd="sng" algn="ctr"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:prstDash val="solid"/><a:round/></a:ln></a:lnStyleLst>
<a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst>
<a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst></a:fmtScheme></a:themeElements>
<a:objectDefaults><a:spDef><a:spPr><a:solidFill><a:schemeClr val="bg2"/></a:solidFill><a:ln w="9525"><a:solidFill><a:srgbClr val="2C2C2E"/></a:solidFill></a:ln></a:spPr><a:bodyPr rtlCol="0" anchor="ctr"/><a:lstStyle/><a:style><a:lnRef idx="1"><a:schemeClr val="accent1"/></a:lnRef><a:fillRef idx="1"><a:schemeClr val="accent1"/></a:fillRef><a:effectRef idx="0"><a:schemeClr val="accent1"/></a:effectRef><a:fontRef idx="minor"><a:schemeClr val="tx1"/></a:fontRef></a:style></a:spDef><a:lnDef><a:spPr><a:ln w="28575"><a:solidFill><a:schemeClr val="tx1"/></a:solidFill></a:ln></a:spPr><a:bodyPr/><a:lstStyle/></a:lnDef></a:objectDefaults><a:extraClrSchemeLst/></a:theme>'''

def master_xml(layout_rids):
    ids=Ids()
    sp=ph(ids,'Titel','title',0,(MX,0.95,12.0,0.7),None,'Titel durch Klicken hinzufügen')
    sp+=ph(ids,'Text','body',1,(MX,2.35,7.933,4.3),None,'Text durch Klicken hinzufügen')
    sp+=ph(ids,'Quelle','ftr',3,(4.733,6.95,5.9,0.25),'footer-r','')
    sp+=ph(ids,'Foliennummer','sldNum',4,(11.85,6.95,0.817,0.25),'footer-r','')
    sp+=text(ids,'Wortmarke',(MX,6.95,3.0,0.25),'ODSV','footer',spc=140)
    lids=''.join(f'<p:sldLayoutId id="{2147483649+i}" r:id="{r}"/>' for i,r in enumerate(layout_rids))
    title_style='<p:titleStyle>'+lvl('headline')+'</p:titleStyle>'
    body_style='<p:bodyStyle>'+lvl('body','dot',0.3,-0.3,1)+''.join(lvl('body-small','dot',0.3+0.3*(n-1),-0.3,n) for n in range(2,6))+'</p:bodyStyle>'
    other='<p:otherStyle><a:defPPr><a:defRPr lang="de-DE"/></a:defPPr>'+''.join(f'<a:lvl{n}pPr marL="{e(0.5*(n-1))}" algn="l" defTabSz="914400" rtl="0" eaLnBrk="1" latinLnBrk="0" hangingPunct="1"><a:defRPr sz="1800" kern="1200"><a:solidFill><a:schemeClr val="tx1"/></a:solidFill><a:latin typeface="+mn-lt"/><a:ea typeface="+mn-ea"/><a:cs typeface="+mn-cs"/></a:defRPr></a:lvl{n}pPr>' for n in range(1,10))+'</p:otherStyle>'
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<p:sldMaster {NS}><p:cSld><p:bg><p:bgPr><a:solidFill><a:schemeClr val="bg1"/></a:solidFill><a:effectLst/></p:bgPr></p:bg><p:spTree>{GRP}{sp}</p:spTree></p:cSld>'
            f'<p:clrMap bg1="dk1" tx1="lt1" bg2="dk2" tx2="lt2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>'
            f'<p:sldLayoutIdLst>{lids}</p:sldLayoutIdLst><p:txStyles>{title_style}{body_style}{other}</p:txStyles></p:sldMaster>')

TABLE_STYLE_ID='{5A1D0E00-0D5B-4C1A-9C0D-0D5B00000001}'
def table_styles_xml():
    b=lambda tag,c='2C2C2E': f'<a:{tag}><a:ln w="9525" cmpd="sng"><a:solidFill><a:srgbClr val="{c}"/></a:solidFill></a:ln></a:{tag}>'
    nol=lambda tag: f'<a:{tag}><a:ln><a:noFill/></a:ln></a:{tag}>'
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<a:tblStyleLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" def="{TABLE_STYLE_ID}">'
      f'<a:tblStyle styleId="{TABLE_STYLE_ID}" styleName="ODSV Tabelle"><a:wholeTbl><a:tcTxStyle><a:fontRef idx="minor"/><a:srgbClr val="E6E6E6"/></a:tcTxStyle><a:tcStyle><a:tcBdr>{nol("left")}{nol("right")}{nol("top")}{b("bottom")}{b("insideH")}{nol("insideV")}</a:tcBdr><a:fill><a:noFill/></a:fill></a:tcStyle></a:wholeTbl>'
      f'<a:firstCol><a:tcTxStyle b="on"><a:fontRef idx="minor"/><a:srgbClr val="FFFFFF"/></a:tcTxStyle><a:tcStyle><a:tcBdr/></a:tcStyle></a:firstCol>'
      f'<a:firstRow><a:tcTxStyle><a:fontRef idx="minor"/><a:srgbClr val="CCCCCC"/></a:tcTxStyle><a:tcStyle><a:tcBdr>{b("bottom","48484A")}</a:tcBdr><a:fill><a:noFill/></a:fill></a:tcStyle></a:firstRow>'
      '</a:tblStyle></a:tblStyleLst>')

def write_base(path):
    L=build_layouts()
    n=len(L)
    ct=['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/><Default Extension="jpg" ContentType="image/jpeg"/>',
     '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>',
     '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>',
     '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>',
     '<Override PartName="/ppt/presProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presProps+xml"/>',
     '<Override PartName="/ppt/viewProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.viewProps+xml"/>',
     '<Override PartName="/ppt/tableStyles.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.tableStyles+xml"/>',
     '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>',
     '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>']
    for i in range(n): ct.append(f'<Override PartName="/ppt/slideLayouts/slideLayout{i+1}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>')
    ct.append('</Types>')
    R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
    z=zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED)
    z.writestr('[Content_Types].xml',''.join(ct))
    z.writestr('_rels/.rels',f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="{R}/officeDocument" Target="ppt/presentation.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/><Relationship Id="rId3" Type="{R}/extended-properties" Target="docProps/app.xml"/></Relationships>')
    z.writestr('docProps/core.xml','<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>ODSV Vorlage</dc:title><dc:creator>ODSV</dc:creator><dcterms:created xsi:type="dcterms:W3CDTF">2026-11-17T00:00:00Z</dcterms:created></cp:coreProperties>')
    z.writestr('docProps/app.xml','<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>Microsoft Office PowerPoint</Application></Properties>')
    rr=[f'<Relationship Id="rId{i+1}" Type="{R}/slideLayout" Target="../slideLayouts/slideLayout{i+1}.xml"/>' for i in range(n)]
    rr.append(f'<Relationship Id="rId{n+1}" Type="{R}/theme" Target="../theme/theme1.xml"/>')
    z.writestr('ppt/slideMasters/slideMaster1.xml',master_xml([f'rId{i+1}' for i in range(n)]))
    z.writestr('ppt/slideMasters/_rels/slideMaster1.xml.rels','<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'+''.join(rr)+'</Relationships>')
    z.writestr('ppt/theme/theme1.xml',theme_xml())
    for i,l in enumerate(L):
        z.writestr(f'ppt/slideLayouts/slideLayout{i+1}.xml',layout_xml(l))
        rel=f'<Relationship Id="rId1" Type="{R}/slideMaster" Target="../slideMasters/slideMaster1.xml"/>'
        for rid,tgt in l['rels']:
            rel+=f'<Relationship Id="{rid}" Type="{R}/image" Target="../media/{tgt.split("/")[-1]}"/>'
        z.writestr(f'ppt/slideLayouts/_rels/slideLayout{i+1}.xml.rels','<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'+rel+'</Relationships>')
    for f in ('signet-card.png','signet-mark.png'): z.write('assets/'+f,'ppt/media/'+f)
    z.writestr('ppt/presentation.xml',f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<p:presentation {NS} saveSubsetFonts="1"><p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst><p:sldSz cx="12192000" cy="6858000"/><p:notesSz cx="6858000" cy="9144000"/><p:defaultTextStyle><a:defPPr><a:defRPr lang="de-DE"/></a:defPPr></p:defaultTextStyle></p:presentation>')
    z.writestr('ppt/_rels/presentation.xml.rels',f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="{R}/slideMaster" Target="slideMasters/slideMaster1.xml"/><Relationship Id="rId2" Type="{R}/presProps" Target="presProps.xml"/><Relationship Id="rId3" Type="{R}/viewProps" Target="viewProps.xml"/><Relationship Id="rId4" Type="{R}/theme" Target="theme/theme1.xml"/><Relationship Id="rId5" Type="{R}/tableStyles" Target="tableStyles.xml"/></Relationships>')
    z.writestr('ppt/presProps.xml',f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<p:presentationPr {NS}/>')
    z.writestr('ppt/viewProps.xml',f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<p:viewPr {NS}><p:normalViewPr><p:restoredLeft sz="15620"/><p:restoredTop sz="94660"/></p:normalViewPr><p:gridSpacing cx="45720" cy="45720"/></p:viewPr>')
    z.writestr('ppt/tableStyles.xml',table_styles_xml())
    z.close()
    return L
if __name__=='__main__':
    L=write_base('base.pptx')
    json.dump([{'name':l['name'],'map':l['map']} for l in L],open('roles.json','w'),ensure_ascii=False,indent=1)
    print(len(L),'layouts')
