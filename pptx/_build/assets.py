from PIL import Image, ImageDraw, ImageFilter
import math
S=4
COL=[(236,58,120),(238,106,44),(240,154,53),(243,195,64)]
YEL=(255,233,77)
def arcs(img,cx,cy,k,span=(55,55,55,55),cap=True):
    outer=[500,391,281,173]; sw=72
    for i,(ro,c) in enumerate(zip(outer,COL)):
        ro*=k; w=sw*k; ri=ro-w; rm=ro-w/2; a=span[i]
        m=Image.new("L",img.size,0); md=ImageDraw.Draw(m)
        md.pieslice([cx-ro,cy-ro,cx+ro,cy+ro],180-a,180+a,fill=255)
        md.ellipse([cx-ri,cy-ri,cx+ri,cy+ri],fill=0)
        if cap:
            for sgn in (-1,1):
                t=math.radians(180+sgn*a); px=cx+rm*math.cos(t); py=cy-rm*math.sin(t)
                md.ellipse([px-w/2,py-w/2,px+w/2,py+w/2],fill=255)
        img.paste(Image.new(img.mode,img.size,c+((255,) if img.mode=="RGBA" else ())),(0,0),m)
    r=59*k
    ImageDraw.Draw(img).ellipse([cx-r,cy-r,cx+r,cy+r],fill=YEL+((255,) if img.mode=="RGBA" else ()))
# Signet-Karte: 4,883 x 6,167 in @ 300 dpi, Zentrum rechts am Rand
W,H=int(4.883*300),int(6.167*300)
img=Image.new("RGB",(W*S//2,H*S//2),(10,10,10))
k=(W*S//2)/624
arcs(img,(W*S//2)+ -0.0*k+ 18*k,(H*S//2)/2,k,span=(75,55,55,55))
img=img.resize((W,H),Image.LANCZOS); img.save("assets/signet-card.png")
# Signet-Marke transparent (quadratisch)
M=900
img=Image.new("RGBA",(M*2,M*2),(0,0,0,0))
k=(M*2)/(2*590)
arcs(img,M*2-60*k,M,k*0.95,span=(55,55,55,55))
bbox=img.getbbox(); img=img.crop(bbox).resize((M,int(M*(bbox[3]-bbox[1])/(bbox[2]-bbox[0]))),Image.LANCZOS)
img.save("assets/signet-mark.png"); print(img.size)
# Platzhalterfoto 16:9 (abstrakt, dunkel)
PW,PH=2400,1350
base=Image.new("RGB",(PW,PH),(8,8,10)); 
glow=Image.new("RGB",(PW,PH),(0,0,0)); g=ImageDraw.Draw(glow)
g.ellipse([1100,150,2300,1050],fill=(236,58,120)); g.ellipse([1500,350,2500,1150],fill=(240,154,53)); g.ellipse([300,600,1300,1300],fill=(40,60,120))
glow=glow.filter(ImageFilter.GaussianBlur(220))
base=Image.blend(base,glow,0.55)
# Linienwerk: abstrakter Horizont mit Kreis (neutrales Motiv) als Line-Art
l=Image.new("RGBA",(PW*2,PH*2),(0,0,0,0)); dd=ImageDraw.Draw(l)
def P(x,y): return (x*2,y*2)
ridge=[(0,980),(260,900),(470,940),(760,760),(980,860),(1220,640),(1480,820),(1700,720),(1960,880),(2180,820),(2400,900)]
dd.line([P(*p) for p in ridge],fill=(255,255,255,235),width=7,joint="curve")
ridge2=[(0,1080),(380,1010),(720,1060),(1100,960),(1500,1040),(1880,980),(2400,1060)]
dd.line([P(*p) for p in ridge2],fill=(255,255,255,130),width=5,joint="curve")
dd.ellipse([P(1580-150,430-150),P(1580+150,430+150)],outline=(255,255,255,235),width=7)
dd.line([P(0,1180),P(2400,1180)],fill=(255,255,255,90),width=4)
l=l.resize((PW,PH),Image.LANCZOS)
base=base.convert("RGBA"); base.alpha_composite(l); base.convert("RGB").save("assets/foto-platzhalter.jpg",quality=92)
