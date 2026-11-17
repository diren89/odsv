import sys,glob
from PIL import Image
fs=sorted(glob.glob('slide-raw-*.png')); sel=[int(x) for x in sys.argv[1:]]
ims=[Image.open(fs[i-1]) for i in sel]
w,h=ims[0].size; cols=2; rows=(len(ims)+1)//2
S=Image.new('RGB',(w*cols+10,h*rows+10*(rows-1)),(60,60,60))
for k,im in enumerate(ims): S.paste(im,((k%2)*(w+10),(k//2)*(h+10)))
S.save('/tmp/sheet.png')
