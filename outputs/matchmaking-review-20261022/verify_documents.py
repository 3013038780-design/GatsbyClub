from pathlib import Path
import json,re,shutil
from PIL import Image,ImageDraw
import pymupdf as f
from zipfile import ZipFile
from xml.etree import ElementTree as E
B=Path(__file__).resolve().parent;O=B/'交付文件';Q=B/'qa';results={}
for typ in ['report','cases','summary']:
 pdf=max((Q/typ).glob('*.pdf'),key=lambda p:p.stat().st_mtime);d=f.open(pdf);n=len(d);texts=[p.get_text() for p in d]
 for i,t in enumerate(texts):
  assert len(re.findall('[\u4e00-\u9fff]',t))>25,(typ,i,'Chinese missing')
 assert not any(len(t)<70 for t in texts),(typ,'near empty page')
 links=[lk for p in d for lk in p.get_links()];external=[x['uri'] for x in links if x.get('uri')];internal=[x for x in links if x.get('kind')==1]
 assert external,(typ,'links missing')
 assert not any(any(m in t for m in ['turn210search','<citation','[[NAVIGATION]]']) for t in texts)
 if typ=='report':
  toc=json.loads((Q/'目录页码.json').read_text());norm=lambda t:re.sub(r'\s+','',t)
  for title,page in toc.items():assert norm(title) in norm(texts[page-1]),(title,page)
  assert len(internal)>=len(toc),(len(internal),len(toc))
  for brand in ['我主良缘','金凤凰深港婚恋','珍爱网']:assert brand in ''.join(texts)
  assert all(n not in ''.join(texts) for n in ['正和岛','优家荟'])
 # Scan text geometry for clipping against physical page bounds.
 clipped=[]
 for i,p in enumerate(d):
  for bl in p.get_text('dict')['blocks']:
   for line in bl.get('lines',[]):
    for span in line['spans']:
     x0,y0,x1,y1=span['bbox']
     if x0 < -1 or y0 < -1 or x1 > p.rect.width+1 or y1 > p.rect.height+1:clipped.append((i+1,span['text'][:40]))
 assert not clipped,(typ,clipped)
 shutil.copy2(pdf,O/pdf.name)
 # Remove stale renders left by older longer revisions.
 for file in (Q/typ).glob('page-*.png'):
  if int(file.stem.split('-')[-1])>n:file.unlink()
 files=sorted((Q/typ).glob('page-*.png'),key=lambda p:int(p.stem.split('-')[-1]));overview=Q/(typ+'-overview');overview.mkdir(exist_ok=True)
 for file in overview.glob('*.jpg'):file.unlink()
 for start in range(0,len(files),6):
  canvas=Image.new('RGB',(1800,1700),'#d8d8d8');dr=ImageDraw.Draw(canvas)
  for j,p in enumerate(files[start:start+6]):
   im=Image.open(p);im.thumbnail((590,810));x=(j%3)*600;y=(j//3)*850;canvas.paste(im,(x,y+28));dr.text((x+12,y+8),p.stem,fill='black')
  canvas.save(overview/f'{start+1:02d}.jpg',quality=92)
 results[typ]={'pages':n,'external_links':len(external),'unique_urls':len(set(external)),'internal_links':len(internal),'clipped_text':clipped,'pdf':str(O/pdf.name)}
(Q/'PDF验收.json').write_text(json.dumps(results,ensure_ascii=False,indent=2));print(json.dumps(results,ensure_ascii=False))
