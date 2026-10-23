from pathlib import Path
import json,zipfile,shutil,csv
from lxml import etree as E
from openpyxl import load_workbook
from pypdf import PdfReader
B=Path(__file__).parent;D=json.loads((B/'修订研究数据.json').read_text());out=B/'交付文件';xlsx=out/'高端社群市场研究_35家机构与收费客群.xlsx'
# The artifact runtime cannot calculate HYPERLINK; attach standard external OOXML links.
ns='http://schemas.openxmlformats.org/spreadsheetml/2006/main';rn='http://schemas.openxmlformats.org/officeDocument/2006/relationships';pn='http://schemas.openxmlformats.org/package/2006/relationships'
maps={3:[(8,i+5,r[7]) for i,r in enumerate(D['activities'])],4:[(10,i+5,r[9]) for i,r in enumerate(D['posts'])],5:[(6,i+5,r[5]) for i,r in enumerate(D['market']) if isinstance(r[5],str) and r[5].startswith('http') and '\n' not in r[5]],6:[(5,i+5,v[1]) for i,v in enumerate(D['sources'].values())]}
with zipfile.ZipFile(xlsx) as z:files={n:z.read(n) for n in z.namelist()}
for n,links in maps.items():
 path=f'xl/worksheets/sheet{n}.xml';root=E.fromstring(files[path]);rels=E.Element('{'+pn+'}Relationships',nsmap={None:pn});hs=E.Element('{'+ns+'}hyperlinks')
 for i,(col,row,url) in enumerate(links):
  rid='rIdResearch'+str(i+1);E.SubElement(hs,'{'+ns+'}hyperlink',ref=chr(64+col)+str(row),attrib={'{'+rn+'}id':rid});E.SubElement(rels,'{'+pn+'}Relationship',Id=rid,Type=rn+'/hyperlink',Target=url,TargetMode='External')
 # hyperlink belongs before print/page/drawing elements
 idx=next((i for i,e in enumerate(root) if E.QName(e).localname in ['printOptions','pageMargins','pageSetup','headerFooter','drawing','legacyDrawing','tableParts','extLst']),len(root));root.insert(idx,hs)
 files[path]=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True);files[f'xl/worksheets/_rels/sheet{n}.xml.rels']=E.tostring(rels,xml_declaration=True,encoding='UTF-8',standalone=True)
with zipfile.ZipFile(xlsx,'w',zipfile.ZIP_DEFLATED) as z:
 for n,b in files.items():z.writestr(n,b)
shutil.copy2(B/'qa/report2/中国高端会员社群市场研究报告.pdf',out/'中国高端会员社群市场研究报告.pdf')
# A clean copy of all prior public research records; remove excluded organizations.
arc=out/'历史公开明细';arc.mkdir(exist_ok=True)
for f in (B/'旧版明细存档').glob('*.csv'):
 with f.open(encoding='utf-8-sig',newline='') as inp, (arc/f.name).open('w',encoding='utf-8-sig',newline='') as dst:
  w=csv.writer(dst)
  for r in csv.reader(inp):
   if not any(x in '|'.join(r) for x in ['正和岛','优家荟']):w.writerow(r)
shutil.copy2(B/'修订研究数据.json',out/'本轮结构化核查数据.json')
(out/'阅读说明.txt').write_text('2026年10月22日修订版\n先读PDF第四章收费与客户分层，再看第六至八章。\nExcel只有6张工作表，先看收费与客群。每行是一个产品，不是一个模糊品牌画像。\n35家名录、47项收费与客群记录、14条本轮抖音核验内容。\n金额为空表示无当前可靠报价，不是免费。\n年龄、职业、收入、性格、兴趣的实际付费客户分布尚未取得，不能将本报告定位描述当作完成的精准画像。\n旧公开明细单独归档，按原时间和原核验状态使用；历史记录不是本轮新采集。\n本轮小红书设备登录受限；无新增可核验数据。不声称完成三平台90天全量采集。\nPDF和Excel均含原文链接；网站仍可能要求登录。\n',encoding='utf-8')
# Structural checks with read-only openpyxl.
w=load_workbook(xlsx,data_only=False,read_only=False);errors=[];ln=0
for s in w:
 for row in s:
  for c in row:
   if c.hyperlink:ln+=1
   if c.data_type=='e':errors.append((s.title,c.coordinate,c.value))
assert not errors,errors
assert len(w.sheetnames)==6
assert sum(1 for row in w['收费与客群'].iter_rows(min_row=5) if row[0].value)==47
pdf=PdfReader(out/'中国高端会员社群市场研究报告.pdf');urls=[a.get_object().get('/A',{}).get('/URI') for p in pdf.pages for a in p.get('/Annots',[])];assert len([u for u in urls if u])==94
print('Excel6表，47产品，35机构，14内容；外链',ln,'PDF页',len(pdf.pages),'链接',len([u for u in urls if u]))
for f in out.glob('*.inspect.ndjson'):f.unlink()
with zipfile.ZipFile(B/'高端社群市场研究修订资料_20261022.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in out.rglob('*'):
  if f.is_file():z.write(f,f.relative_to(out))
