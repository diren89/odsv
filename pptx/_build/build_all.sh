# Erzeugt ODSV-Vorlage.pptx, .potx und die Vorschau-PNGs. Aufruf: bash build_all.sh
set -e
cd "$(dirname "$0")"; python3 assets.py; python3 deck.py
python3 - <<'P'
import zipfile
src=zipfile.ZipFile('base.pptx'); dst=zipfile.ZipFile('../ODSV-Vorlage.potx','w',zipfile.ZIP_DEFLATED)
for it in src.infolist():
    data=src.read(it.filename)
    if it.filename=='[Content_Types].xml': data=data.replace(b'presentationml.presentation.main+xml',b'presentationml.template.main+xml')
    dst.writestr(it.filename,data)
dst.close()
P
S=/mnt/skills/public/pptx/scripts
python3 $S/office/validate.py ../ODSV-Vorlage.pptx | tail -2
cd ../_preview; rm -f *.png *.pdf; python3 $S/office/soffice.py --headless --convert-to pdf ../ODSV-Vorlage.pptx >/dev/null 2>&1
pdftoppm -png -r 110 ODSV-Vorlage.pdf slide
python3 - <<'P'
import glob
from PIL import Image
fs=sorted(glob.glob('slide-[0-9][0-9].png')); w,h=Image.open(fs[0]).size; tw=640; th=int(h*tw/w); cols=3; rows=(len(fs)+2)//3
S=Image.new('RGB',(cols*tw+(cols+1)*12,rows*th+(rows+1)*12),(40,40,40))
for k,f in enumerate(fs): S.paste(Image.open(f).resize((tw,th),Image.LANCZOS),(12+(k%cols)*(tw+12),12+(k//cols)*(th+12)))
S.save('overview.png')
P
