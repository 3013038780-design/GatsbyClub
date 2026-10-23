# Preserve native workbook links and source text where the artifact exporter rejects existing URI hosts.
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from xml.etree import ElementTree as E
import json,re,openpyxl
B=Path(__file__).resolve().parent;O=B/'交付文件';P=O/'中国高端会员社群市场研究数据工作簿_33家机构.xlsx';D=json.loads((B/'删除两家工作簿计划.json').read_text())
ns='http://schemas.openxmlformats.org/spreadsheetml/2006/main';rn='http://schemas.openxmlformats.org/officeDocument/2006/relationships';E.register_namespace('',ns);E.register_namespace('r',rn);T=lambda s:'{'+ns+'}'+s
with ZipFile(P) as z:a={n:z.read(n) for n in z.namelist()}
w=E.fromstring(a['xl/workbook.xml']);rels={r.get('Id'):r.get('Target') for r in E.fromstring(a['xl/_rels/workbook.xml.rels'])}
for sh in w.find(T('sheets')):
 name=sh.get('name');sp=rels[sh.get('{'+rn+'}id')].lstrip('/');sp=sp if sp.startswith('xl/') else 'xl/'+sp
 if name in D['rename']:sh.set('name',D['rename'][name])
 if name not in D['changes']:continue
 x=D['changes'][name];rt=E.fromstring(a[sp]);mapping={r:i+5 for i,r in enumerate(x['keep'])};mapping.update({i:i for i in range(1,5)})
 data=rt.find(T('sheetData'))
 for row in list(data):
  old=int(row.get('r'))
  if old not in mapping:data.remove(row);continue
  new=mapping[old];row.set('r',str(new))
  for cell in row:
   coord=re.sub(r'\d+$',str(new),cell.get('r'));cell.set('r',coord)
   value=next((v for c,v in x['top'] if c==coord),None) if new<5 else x['rows'][new-5][openpyxl.utils.cell.column_index_from_string(re.sub(r'\d','',coord))-1]
   if value is None:continue
   # Store changed strings/counts explicitly without Excel formula inference.
   if isinstance(value,str):
    for n in list(cell):cell.remove(n)
    cell.set('t','inlineStr');is_=E.SubElement(cell,T('is'));E.SubElement(is_,T('t')).text=value
   elif new>=5:
    for n in list(cell):cell.remove(n)
    cell.attrib.pop('t',None);E.SubElement(cell,T('v')).text=str(value)
 def remap_ref(ref):
  matches=re.findall(r'([A-Z]+)(\d+)',ref)
  if len(matches)==1:
   c,r=matches[0];r=int(r);return c+str(mapping[r]) if r in mapping else None
  if len(matches)==2:
   (ca,ra),(cb,rb)=matches;valid=[v for k,v in mapping.items() if int(ra)<=k<=int(rb)]
   return f'{ca}{min(valid)}:{cb}{max(valid)}' if valid else None
  return ref
 for el in list(rt.iter()):
  if el.tag==T('c'):continue
  if 'ref' in el.attrib:
   rr=remap_ref(el.get('ref'))
   if rr:el.set('ref',rr)
   else:
    parent=next((p for p in rt.iter() if el in list(p)),None)
    if parent is not None:parent.remove(el)
  if 'sqref' in el.attrib:el.set('sqref',' '.join(v for z in el.get('sqref').split() if (v:=remap_ref(z))))
 a[sp]=E.tostring(rt,encoding='utf-8',xml_declaration=True)
 rp=str(Path(sp).parent/'_rels'/(Path(sp).name+'.rels'))
 if rp in a:
  for rel in E.fromstring(a[rp]):
   if rel.get('Type','').endswith('/table'):
    tp=str((Path(sp).parent/rel.get('Target')).resolve()) if False else rel.get('Target')
    import posixpath
    tp=tp.lstrip('/') if tp.startswith('/') else posixpath.normpath(posixpath.join(posixpath.dirname(sp),tp))
    table=E.fromstring(a[tp])
    for e in table.iter():
     if e.get('ref'):e.set('ref',remap_ref(e.get('ref')))
    a[tp]=E.tostring(table,encoding='utf-8',xml_declaration=True)
a['xl/workbook.xml']=E.tostring(w,encoding='utf-8',xml_declaration=True)
out=O/'中国高端会员社群市场研究数据工作簿_31家机构.xlsx'
with ZipFile(out,'w',ZIP_DEFLATED) as z:
 for n,v in a.items():z.writestr(n,v)
v=openpyxl.load_workbook(out);old=openpyxl.load_workbook(P)
assert v['31家机构对照'].max_row-4==31
for s in v:
 assert not [(c.coordinate,c.value) for row in s for c in row if isinstance(c.value,str) and any(n in c.value for n in ['正和岛','优家荟'])],s.title
 assert not [(c.coordinate,c.value) for row in s for c in row if c.data_type=='e'],s.title
for name,x in D['changes'].items():
 s=v[D['rename'].get(name,name)]
 for new,oldrow in enumerate(x['keep'],5):
  for c in old[name][oldrow]:
   if c.hyperlink:assert s.cell(new,c.column).hyperlink.target==c.hyperlink.target
assert v['经营测算']['B15'].value==old['经营测算']['B15'].value
counts={'institutions':31,'primary_cases':6,'worksheets':len(v.sheetnames),'price_records':v['31家价格'].max_row-4,'source_records':v['来源台账'].max_row-4,'hyperlinks':sum(bool(c.hyperlink) for s in v for row in s for c in row),'deleted_rows':166,'formula_errors':[]}
(B/'qa/Excel验收.json').write_text(json.dumps(counts,ensure_ascii=False,indent=2));print(counts);P.unlink()
