from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from xml.etree import ElementTree as ET
import json,re,csv,hashlib,html
B=Path(__file__).resolve().parents[1];O=B/'交付资料';P=O/'正式文件'
d=json.loads((B/'research/30家工作簿数据.json').read_text());f=P/'中国高端会员社群市场研究数据工作簿_30家机构.xlsx'
ns='http://schemas.openxmlformats.org/spreadsheetml/2006/main';rn='http://schemas.openxmlformats.org/officeDocument/2006/relationships';pn='http://schemas.openxmlformats.org/package/2006/relationships'
ET.register_namespace('',ns);ET.register_namespace('r',rn)
def col(n):
 s=''
 while n:n,r=divmod(n-1,26);s=chr(65+r)+s
 return s
with ZipFile(f)as z:parts={n:z.read(n)for n in z.namelist()}
count=0
for i,s in enumerate(d['sheets'],1):
 sp=f'xl/worksheets/sheet{i}.xml';rp=f'xl/worksheets/_rels/sheet{i}.xml.rels';root=ET.fromstring(parts[sp]);rels=ET.fromstring(parts[rp])if rp in parts else ET.Element('{'+pn+'}Relationships');links=ET.Element('{'+ns+'}hyperlinks')
 for ri,row in enumerate(s['rows'],5):
  for ci,v in enumerate(row,1):
   if isinstance(v,str)and re.fullmatch(r'https?://\S+',v):
    rid=f'PublicLink{ri}_{ci}';ET.SubElement(rels,'{'+pn+'}Relationship',{'Id':rid,'Type':rn+'/hyperlink','Target':v,'TargetMode':'External'});ET.SubElement(links,'{'+ns+'}hyperlink',{'ref':f'{col(ci)}{ri}','{'+rn+'}id':rid});count+=1
 if len(links):
  following={'printOptions','pageMargins','pageSetup','headerFooter','rowBreaks','colBreaks','customProperties','cellWatches','ignoredErrors','smartTags','drawing','legacyDrawing','legacyDrawingHF','picture','oleObjects','controls','webPublishItems','tableParts','extLst'}
  root.insert(next((j for j,e in enumerate(root)if e.tag.split('}')[-1]in following),len(root)),links);parts[sp]=ET.tostring(root,encoding='utf-8',xml_declaration=True);parts[rp]=ET.tostring(rels,encoding='utf-8',xml_declaration=True)
with ZipFile(f,'w',ZIP_DEFLATED)as z:
 for n,v in parts.items():z.writestr(n,v)
for p in P.glob('*.inspect.ndjson'):p.unlink()
# Compare all preserved worksheets against original workbook with a read-only library.
import openpyxl
old=openpyxl.load_workbook(P/'中国高端会员社群市场研究数据工作簿.xlsx');new=openpyxl.load_workbook(f)
changed={'文件与数据说明','六家对照','六家价格','会员权益','客户画像','获客方式','活动流程','经营表现','市场机构地图','来源台账','网页采集台账','证据缺口'}
preserved=[]
for name in old.sheetnames:
 if name in changed:continue
 a,b=old[name],new[name]
 assert a.max_row==b.max_row and a.max_column==b.max_column,name
 for row in a:
  for x in row:
   y=b[x.coordinate];assert x.value==y.value,(name,x.coordinate,x.value,y.value)
   assert x.number_format==y.number_format,(name,x.coordinate,'format')
   if x.hyperlink:assert y.hyperlink and x.hyperlink.target==y.hyperlink.target,(name,x.coordinate,'link')
 assert a.freeze_panes==b.freeze_panes,name
 assert len(a.tables)==len(b.tables),name
 preserved.append(name)
names=[new['30家机构对照'].cell(r,1).value for r in range(5,35)];assert len(set(names))==30
for name in ['30家价格','会员权益','客户画像','获客方式','活动流程','经营表现','30家平台声量']:
 s=new[name];actual={s.cell(r,1).value for r in range(5,s.max_row+1)};assert set(names)<=actual,(name,set(names)-actual)
assert new['经营测算']['B15'].value=='=IF(B7>0,ROUNDUP(B6/B7,0),"贡献须大于零")'
assert not any(c.data_type=='e'for s in new for row in s for c in row)
result={'institutions':30,'sheets':len(new.sheetnames),'price_records':new['30家价格'].max_row-4,'native_hyperlinks':count,'unchanged_sheets_compared':preserved,'coverage':'七个专题均覆盖30家','formula_error_cells':0}
(B/'research/30家工作簿验收.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
# Update the existing package directory while preserving all previous reports and raw data.
guide=O/'资料目录.html';t=guide.read_text()
if '本次更新：30家机构Excel' not in t:t=t.replace('<h2>正式文件</h2>','<h2>本次更新：30家机构Excel</h2><p>价格、会员权益、客户画像、获客方式、活动流程、经营表现与平台声量均列30家。六家案例文档保留为深度档案。</p><p><a href="正式文件/'+f.name+'">下载30家机构工作簿</a></p><h2>正式文件</h2>')
for label,value in [('市场机构地图',d['counts']['institutions']),('网页采集尝试',d['counts']['pages']),('公开网页正文存档',sum(1 for p in (O/'公开网页存档').rglob('*')if p.is_file()))]:t=re.sub(r'(<td>'+label+r'</td><td>)[^<]+',lambda m:m[1]+str(value),t)
guide.write_text(t)
(O/'交付说明.txt').write_text('请先打开 资料目录.html。\n本次Excel扩展至30家机构，27张工作表。请使用文件名带“30家机构”的新版。\n六家案例档案与正式报告维持此前版本；其六家为深度案例，不是全市场范围。\n新增30家机构扩展CSV在 数据明细/30家机构扩展，新增网页存档在 公开网页存档/30家扩展复核。\n资料截至2026年10月21日。\n')
with (O/'文件清单.csv').open('w',encoding='utf-8-sig',newline='')as h:
 w=csv.writer(h);w.writerow(['包内文件','字节数','SHA256'])
 for p in sorted(O.rglob('*')):
  if p.is_file()and p.name!='文件清单.csv':w.writerow([str(p.relative_to(O)),p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest()])
zipfile=B/'中国高端会员社群市场研究配套资料_30家机构.zip'
with ZipFile(zipfile,'w',ZIP_DEFLATED)as z:
 for p in sorted(O.rglob('*')):
  if p.is_file():z.write(p,'中国高端会员社群市场研究资料/'+str(p.relative_to(O)))
print(json.dumps({**result,'xlsx':str(f),'zip':str(zipfile)},ensure_ascii=False))
