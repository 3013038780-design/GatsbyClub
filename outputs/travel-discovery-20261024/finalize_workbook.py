"""Add native source links after Artifact Tool export (HYPERLINK evaluator unavailable)."""
from pathlib import Path
import json,zipfile
from lxml import etree as E

b=Path(__file__).parent
book=b/'社交旅行产品与采集核验.xlsx'
links=json.loads((b/'链接索引.json').read_text())
ns='http://schemas.openxmlformats.org/spreadsheetml/2006/main'
rn='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
pn='http://schemas.openxmlformats.org/package/2006/relationships'
with zipfile.ZipFile(book) as z:files={n:z.read(n) for n in z.namelist()}
for num in (1,2):
    items=[r for r in links if r['sheet']==num-1]
    filename=f'xl/worksheets/sheet{num}.xml'
    relfile=f'xl/worksheets/_rels/sheet{num}.xml.rels'
    root=E.fromstring(files[filename])
    rels=E.fromstring(files[relfile]) if relfile in files else E.Element('{'+pn+'}Relationships',nsmap={None:pn})
    for e in root.findall('{'+ns+'}hyperlinks'):root.remove(e)
    for e in list(rels):
        if e.get('Id','').startswith('rIdResearch'):rels.remove(e)
    hs=E.Element('{'+ns+'}hyperlinks')
    for i,r in enumerate(items,1):
        rid='rIdResearch'+str(i)
        E.SubElement(hs,'{'+ns+'}hyperlink',ref=r['cell'],attrib={'{'+rn+'}id':rid})
        E.SubElement(rels,'{'+pn+'}Relationship',Id=rid,Type=rn+'/hyperlink',Target=r['url'],TargetMode='External')
    before=next((e for e in root if E.QName(e).localname in ['printOptions','pageMargins','pageSetup','headerFooter','drawing','tableParts','extLst']),None)
    root.insert(list(root).index(before),hs) if before is not None else root.append(hs)
    files[filename]=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
    files[relfile]=E.tostring(rels,xml_declaration=True,encoding='UTF-8',standalone=True)
with zipfile.ZipFile(book,'w',zipfile.ZIP_DEFLATED) as z:
    for n,v in files.items():z.writestr(n,v)
with zipfile.ZipFile(book) as z:
    count=0
    for num in (1,2):
        root=E.fromstring(z.read(f'xl/worksheets/sheet{num}.xml'))
        rels=E.fromstring(z.read(f'xl/worksheets/_rels/sheet{num}.xml.rels'))
        relmap={r.get('Id'):r.get('Target') for r in rels}
        for e in root.findall('{'+ns+'}hyperlinks/{'+ns+'}hyperlink'):
            target=relmap[e.get('{'+rn+'}id')]
            expected=next(r['url'] for r in links if r['sheet']==num-1 and r['cell']==e.get('ref'))
            assert target==expected
            count+=1
    assert count==409
    sheet=E.fromstring(z.read('xl/worksheets/sheet1.xml'))
    cell=sheet.find('.//{'+ns+'}c[@r="B8"]')
    assert cell is not None and cell.find('{'+ns+'}v').text=='198'
    assert b'HYPERLINK is not implemented' not in b''.join(z.read(n) for n in z.namelist() if n.endswith('.xml'))
(b/'qa/链接核验.json').write_text(json.dumps({'原生超链接':count,'逐项比对URL':'通过','金额B8':198,'工作表数量':2,'平台说明':'小红书及抖音链接可能需要登录；本机已实查关键原文。'},ensure_ascii=False,indent=2))
print('Native source links verified:',count)
