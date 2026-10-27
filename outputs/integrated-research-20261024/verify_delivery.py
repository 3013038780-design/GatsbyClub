from pathlib import Path
import json,zipfile,re,math
from lxml import etree as E
from pypdf import PdfReader
B=Path(__file__).parent;O=B/'交付文件';D=json.loads((B/'统一研究数据.json').read_text());n={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'};w='{'+n['w']+'}'
with zipfile.ZipFile(O/'高端线下社群市场调研与对标报告.docx') as z:r=E.fromstring(z.read('word/document.xml'))
heads={x.get(w+'name'):''.join(x.getparent().itertext())for x in r.findall('.//w:bookmarkStart',n)};anchors=[x.get(w+'anchor')for x in r.findall('.//w:hyperlink',n)if x.get(w+'anchor')]
pdf=PdfReader(O/'高端线下社群市场调研与对标报告.pdf');pages={p.indirect_reference.idnum:i for i,p in enumerate(pdf.pages)};dest=[]
for i,p in enumerate(pdf.pages):
 for a in p.get('/Annots',[]):
  a=a.get_object()
  if a.get('/Dest'):dest.append((i,-float(a['/Rect'][3]),pages[a['/Dest'][0].idnum]))
dest.sort();assert len(dest)==len(anchors)==16
norm=lambda s:re.sub(r'\s+','',s or'')
for key,(_,_,target)in zip(anchors,dest):assert norm(heads[key])in norm(pdf.pages[target].extract_text()),(key,target)
text=''.join(p.extract_text()or''for p in pdf.pages)
for value in ['1625','1095','1125','8215.6','95','FTLO','研究判断','项目贡献']:assert value in text,value
assert len(D['market'])==len(set(x[0]for x in D['market']))
ids={s['id']for s in D['sources']};assert all(x[8]in ids for x in D['products']);assert all(s in ids for c in D['cases']for s in c['sources'])
ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with zipfile.ZipFile(O/'高端线下社群市场调研与对标总表.xlsx')as z:
 shared=[]
 if 'xl/sharedStrings.xml'in z.namelist():shared=[''.join(x.itertext())for x in E.fromstring(z.read('xl/sharedStrings.xml'))]
 root=E.fromstring(z.read('xl/worksheets/sheet2.xml'));cells={c.get('r'):c for c in root.findall('.//s:sheetData/s:row/s:c',ns)}
 def read(ref):
  c=cells.get(ref)
  if c is None:return None
  if c.get('t')=='inlineStr':return ''.join(c.find('s:is',ns).itertext())
  v=c.find('s:v',ns)
  if v is None:return None
  return shared[int(v.text)]if c.get('t')=='s'else v.text
 for i,row in enumerate(D['products'],6):
  for j,want in enumerate(row[:8]):
   got=read(chr(65+j)+str(i))
   if want is None:assert got in [None,''],(i,j,got)
   elif isinstance(want,(float,int)):assert math.isclose(float(got),want,abs_tol=1e-8),(i,j)
   else:assert got==want,(i,j)
assert math.isclose(35104-19800*.1*14*.97,8215.6,abs_tol=1e-8)
q=json.loads((B/'qa/交付核验.json').read_text());q.update(pdf_internal_targets_verified=16,workbook_product_cells_verified=len(D['products'])*8,visual_review='27个变更页逐页视觉复核，23页与40页版本正文一致并沿用此前视觉复核；4张图表与新增Excel视图已检查。',new_web_tasks=12,new_web_valid=11,soft_404_excluded=1,conclusion_rows=len(D['conclusions']),report_stage='PDF内容、图表、目录及链接核验通过，进入HTML与口语稿制作。');(B/'qa/交付核验.json').write_text(json.dumps(q,ensure_ascii=False,indent=2))
(B/'qa/逐页复核结果.json').write_text(json.dumps(dict(pages=len(pdf.pages),changed_pages=json.loads((B/'qa/本轮补写页面差异.json').read_text())['changed_pages'],changed_pages_visually_reviewed=True,unchanged_page_texts=23,graphs=4,no_blank_pages=all(len(p.extract_text()or'')>100 for p in pdf.pages)),ensure_ascii=False,indent=2))
print('Verified:',len(pdf.pages),'pages,',len(D['products'])*8,'product cells,16 TOC destinations')
