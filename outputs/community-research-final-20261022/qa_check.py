from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
from pypdf import PdfReader
B=Path(__file__).parent
files=sorted((B/'qa/report2').glob('page-*.png'),key=lambda p:int(p.stem.split('-')[1]))
for start in range(0,len(files),6):
 out=Image.new('RGB',(1200,1100),'#aab0b5');dr=ImageDraw.Draw(out)
 for j,f in enumerate(files[start:start+6]):
  im=Image.open(f);im.thumbnail((390,510));x=(j%3)*400;y=(j//3)*550;out.paste(im,(x,y+22));dr.text((x+8,y+4),f.stem,fill='black')
 out.save(B/f'qa/report2-review-{start//6+1}.png')
files=list((B/'qa').glob('*.png'));files=[p for p in files if 'review-' not in p.name]
out=Image.new('RGB',(1500,1000),'#aab0b5')
for j,f in enumerate(files):
 im=Image.open(f);im.thumbnail((740,310));out.paste(im,((j%2)*750,(j//2)*330))
out.save(B/'qa/sheets-review.png')
pdf=PdfReader(B/'qa/report2/中国高端会员社群市场研究报告.pdf');links=[a.get_object().get('/A',{}).get('/URI') for p in pdf.pages for a in p.get('/Annots',[])];print('pages',len(pdf.pages),'url_annotations',len([u for u in links if u]));print('empty pages',[i+1 for i,p in enumerate(pdf.pages) if len(p.extract_text().strip())<15])
