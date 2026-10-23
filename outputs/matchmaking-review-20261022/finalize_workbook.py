from pathlib import Path
import json,re
from zipfile import ZipFile,ZIP_DEFLATED
from xml.etree import ElementTree as E
import openpyxl
B=Path(__file__).resolve().parent;P=B/'交付文件/中国高端会员社群市场研究数据工作簿_33家机构.xlsx';OLD=B.parent/'social-research-20261021/交付资料/正式文件/中国高端会员社群市场研究数据工作簿_30家机构.xlsx'
x=json.loads((B/'工作簿更新数据.json').read_text());ns='http://schemas.openxmlformats.org/spreadsheetml/2006/main';rn='http://schemas.openxmlformats.org/officeDocument/2006/relationships';pn='http://schemas.openxmlformats.org/package/2006/relationships'
E.register_namespace('',ns);E.register_namespace('r',rn)
def parts(p):
 with ZipFile(p) as z:return {k:z.read(k) for k in z.namelist()}
a=parts(OLD);b=parts(P)
def mapping(z):
 w=E.fromstring(z['xl/workbook.xml']);rels={r.attrib['Id']:r.attrib['Target'] for r in E.fromstring(z['xl/_rels/workbook.xml.rels'])}
 return {s.attrib['name']:'xl/'+rels[s.attrib['{'+rn+'}id']].lstrip('/') if not rels[s.attrib['{'+rn+'}id']].startswith('/xl/') else rels[s.attrib['{'+rn+'}id']].lstrip('/') for s in w.find('{'+ns+'}sheets')}
ma,mb=mapping(a),mapping(b)
def relpath(p):return str(Path(p).parent/'_rels'/(Path(p).name+'.rels'))
def links(z,path):
 rp=relpath(path);rels={r.attrib['Id']:r.attrib.get('Target','') for r in E.fromstring(z[rp])} if rp in z else {};rt=E.fromstring(z[path]);hl=rt.find('{'+ns+'}hyperlinks')
 return {} if hl is None else {n.attrib['ref']:rels.get(n.attrib.get('{'+rn+'}id',''),'') for n in hl}
newread=openpyxl.load_workbook(P);restored=0
for name,sp in mb.items():
 rt=E.fromstring(b[sp]);rp=relpath(sp);rels=E.fromstring(b[rp]) if rp in b else E.Element('{'+pn+'}Relationships')
 original_name={v:k for k,v in x['rename'].items()}.get(name,name)
 prior=links(b,sp)
 if original_name in ma:prior.update(links(a,ma[original_name]))
 for row in newread[name]:
  for c in row:
   if isinstance(c.value,str):
    urls=re.findall(r'https?://[^\s]+',c.value)
    if urls and c.coordinate not in prior:prior[c.coordinate]=urls[0]
 oldhl=rt.find('{'+ns+'}hyperlinks')
 if oldhl is not None:rt.remove(oldhl)
 hl=E.Element('{'+ns+'}hyperlinks')
 # Retain unrelated relationships (drawings, table parts, etc.).
 for item in list(rels):
  if item.attrib.get('Type','').endswith('/hyperlink'):rels.remove(item)
 for i,(ref,u) in enumerate(prior.items(),1):
  if not u.startswith(('http://','https://')):continue
  rid=f'ResearchSource{i}';E.SubElement(rels,'{'+pn+'}Relationship',{'Id':rid,'Type':rn+'/hyperlink','Target':u,'TargetMode':'External'});E.SubElement(hl,'{'+ns+'}hyperlink',{'ref':ref,'{'+rn+'}id':rid});restored+=1
 if len(hl):
  after={'printOptions','pageMargins','pageSetup','headerFooter','rowBreaks','colBreaks','customProperties','cellWatches','ignoredErrors','smartTags','drawing','legacyDrawing','legacyDrawingHF','picture','oleObjects','controls','webPublishItems','tableParts','extLst'}
  rt.insert(next((j for j,e in enumerate(rt) if e.tag.split('}')[-1] in after),len(rt)),hl)
 b[sp]=E.tostring(rt,encoding='utf-8',xml_declaration=True);b[rp]=E.tostring(rels,encoding='utf-8',xml_declaration=True)
# Public worksheet name setter is absent from the runtime; rename in OOXML without changing cells or formulas.
w=E.fromstring(b['xl/workbook.xml'])
for s in w.find('{'+ns+'}sheets'):
 if s.attrib['name'] in x['rename']:s.set('name',x['rename'][s.attrib['name']])
b['xl/workbook.xml']=E.tostring(w,encoding='utf-8',xml_declaration=True)
with ZipFile(P,'w',ZIP_DEFLATED) as z:
 for k,v in b.items():z.writestr(k,v)
old=openpyxl.load_workbook(OLD);new=openpyxl.load_workbook(P);changed=set(x['updates'])|set(x['appends']);unchanged=[]
for name in old.sheetnames:
 if name in changed:continue
 aa,bb=old[name],new[name]
 assert (aa.max_row,aa.max_column)==(bb.max_row,bb.max_column),name
 for row in aa:
  for c in row:
   y=bb[c.coordinate];assert c.value==y.value,(name,c.coordinate,c.value,y.value)
   assert c.number_format==y.number_format,(name,c.coordinate,'number_format')
   if c.hyperlink:assert y.hyperlink and c.hyperlink.target==y.hyperlink.target,(name,c.coordinate,'hyperlink')
 assert aa.freeze_panes==bb.freeze_panes,(name,'panes')
 unchanged.append(name)
names={new['33家机构对照'].cell(r,1).value for r in range(5,38)};assert len(names)==33
for tab in ['33家价格','会员权益','客户画像','获客方式','活动流程','经营表现','33家平台声量']:
 actual={new[tab].cell(r,1).value for r in range(5,new[tab].max_row+1)};assert names<=actual,(tab,names-actual)
assert new['经营测算']['B15'].value==old['经营测算']['B15'].value
errs=[(s.title,c.coordinate,c.value) for s in new for row in s for c in row if c.data_type=='e'];assert not errs,errs[:3]
lookup={new['市场机构地图'].cell(r,2).value for r in range(5,new['市场机构地图'].max_row+1)}
assert {'我主良缘','珍爱网','金凤凰深港婚恋'}<=lookup
summary=dict(institutions=33,primary_cases=8,worksheets=len(new.sheetnames),price_records=new['33家价格'].max_row-4,new_price_records=21,source_records=new['来源台账'].max_row-4,hyperlinks=restored,unchanged_sheets_verified=unchanged,formula_errors=errs)
(B/'qa/Excel验收.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));print(json.dumps(summary,ensure_ascii=False))
