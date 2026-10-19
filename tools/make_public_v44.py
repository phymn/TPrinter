"""Make the public-safe edition of TPrinter v4.4 from the private build.
Removes every embedded image (printer photos, part photos, representative photos,
service-manual drawings, large viewer images and callout data). Names stay.
Usage: python3 make_public_v44.py private.html lexmark-repair-app.html"""
import re,sys
src,dst=sys.argv[1],sys.argv[2]
h=open(src,encoding='utf-8').read()
def blank(var,val):
    global h
    m=re.search(r'const '+var+r'\s*=\s*',h); assert m,var
    i=m.end(); j=h.index(';\n',i)
    h=h[:i]+val+h[j:]
blank('IMG_MX826','null'); blank('IMG_MS823','null')
for v in ('FAM_IMG','PART_IMG','PART_REP','ILL_IMG','PART_ILL'): blank(v,'{}')
h=re.sub(r'<script type="text/plain" id="big(?:ill)?-[^"]+">[^<]*</script>\n?','',h)
h=re.sub(r'<script>const CALLOUT=.*?;</script>\n?','<script>const CALLOUT={};</script>\n',h)
h=h.replace('v4.4 (added topguns, system type models, FRU pictures)</footer>','v4.4 public edition (model and FRU names; no photos or manual drawings)</footer>')
h=h.replace('<title>TPrinter v4.4 ·','<title>TPrinter v4.4 public ·')
assert 'data:image/jpeg;base64' not in h and 'data:image/webp' not in h.replace('"data:image/webp;base64,"+','')
open(dst,'w',encoding='utf-8').write(h)
print(len(h))
