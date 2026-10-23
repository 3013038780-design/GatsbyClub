from pathlib import Path
import json,zipfile,shutil,csv
from lxml import etree as E
from openpyxl import load_workbook
from pypdf import PdfReader
B=Path(__file__).resolve().parent;out=B/'交付文件';D=json.loads((B/'正式报告数据.json').read_text());xlsx=out/'高端线下社群研究数据.xlsx'
ns='http://schemas.openxmlformats.org/spreadsheetml/2006/main';rn='http://schemas.openxmlformats.org/officeDocument/2006/relationships';pn='http://schemas.openxmlformats.org/package/2006/relationships'
links=json.loads((B/'工作簿链接映射.json').read_text()); grouped={}
with zipfile.ZipFile(xlsx) as z:files={n:z.read(n) for n in z.namelist()}
work=E.fromstring(files['xl/workbook.xml']);sheetnums={s.get('name'):i+1 for i,s in enumerate(work.find('{'+ns+'}sheets'))}
for x in links:grouped.setdefault(sheetnums[x['sheet']],[]).append(x)
for num,rows in grouped.items():
 path=f'xl/worksheets/sheet{num}.xml';rp=f'xl/worksheets/_rels/sheet{num}.xml.rels';root=E.fromstring(files[path]);rels=E.fromstring(files[rp]) if rp in files else E.Element('{'+pn+'}Relationships',nsmap={None:pn})
 for el in list(root.findall('{'+ns+'}hyperlinks')):root.remove(el)
 for el in list(rels):
  if el.get('Id','').startswith('rIdResearch'):rels.remove(el)
 hs=E.Element('{'+ns+'}hyperlinks')
 for i,row in enumerate(rows):
  rid='rIdResearch'+str(i+1);E.SubElement(hs,'{'+ns+'}hyperlink',ref=row['cell'],attrib={'{'+rn+'}id':rid});E.SubElement(rels,'{'+pn+'}Relationship',Id=rid,Type=rn+'/hyperlink',Target=row['url'],TargetMode='External')
 idx=next((i for i,e in enumerate(root) if E.QName(e).localname in ['printOptions','pageMargins','pageSetup','headerFooter','drawing','legacyDrawing','tableParts','extLst']),len(root));root.insert(idx,hs)
 files[path]=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True);files[rp]=E.tostring(rels,xml_declaration=True,encoding='UTF-8',standalone=True)
with zipfile.ZipFile(xlsx,'w',zipfile.ZIP_DEFLATED) as z:
 for n,b in files.items():z.writestr(n,b)
shutil.copy2(B/'qa/report-release/中国高端线下社群市场研究报告.pdf',out/'中国高端线下社群市场研究报告.pdf')
# Read-only verification includes native tables, charts, source links and formulas.
w=load_workbook(xlsx,data_only=False);linkcheck=[]
for s in w:
 for row in s:
  for c in row:
   assert c.data_type!='e',(s.title,c.coordinate,c.value)
   if c.hyperlink:linkcheck.append((s.title,c.coordinate,c.hyperlink.target))
assert len(linkcheck)==len(links)==198
for x in links:assert w[x['sheet']][x['cell']].hyperlink.target==x['url']
assert len(w.sheetnames)==7 and len(w['经营测算']._charts)==1
assert sum(len(s.tables) for s in w)==6
expected={'机构总览':36,'收费权益':57,'客户画像':15,'活动旅行':9,'账号声量':8,'内容明细':73}
for k,n in expected.items():assert sum(1 for r in w[k].iter_rows(min_row=6) if r[0].value)==n,(k,n)
wc=load_workbook(xlsx,data_only=True);assert wc['经营测算']['B19'].value==78;assert wc['经营测算']['B20'].value==-600000
pdf=PdfReader(out/'中国高端线下社群市场研究报告.pdf');pdfurls=[a.get_object().get('/A',{}).get('/URI') for p in pdf.pages for a in p.get('/Annots',[])];pdfurls=[str(u) for u in pdfurls if u]
with zipfile.ZipFile(out/'中国高端线下社群市场研究报告.docx') as z:
 rel=E.fromstring(z.read('word/_rels/document.xml.rels'));wordurls=[x.get('Target') for x in rel if x.get('Type')==rn+'/hyperlink'];xml=z.read('word/document.xml').decode();assert all(bad not in xml for bad in ['正和岛','优家荟'])
assert set(wordurls).issubset(set(pdfurls)),set(wordurls)-set(pdfurls)
# All source records are public research data; login state is never copied.
arc=out/'历史公开明细';shutil.copytree(B.parent/'community-research-final-20261022/交付文件/历史公开明细',arc,dirs_exist_ok=True)
public={k:v for k,v in D.items() if k not in ['legacy','evidence']};(out/'本轮结构化研究数据.json').write_text(json.dumps(public,ensure_ascii=False,indent=2))
with (out/'资料来源索引.csv').open('w',encoding='utf-8-sig',newline='') as f:
 cw=csv.writer(f);cw.writerow(['编号','资料','链接','时间','证据说明']);cw.writerows([[k,*v] for k,v in D['sources'].items()])
with (out/'公开内容明细.csv').open('w',encoding='utf-8-sig',newline='') as f:
 cw=csv.writer(f);cw.writerow(['品牌','账号','平台','发布日期','内容','点赞','评论','收藏','分享','原文']);cw.writerows(D['posts'])
(out/'阅读说明.txt').write_text('中国高端线下社群市场研究资料｜2026年10月22日\n\n先读正式报告的一、四、六、七章，再用Excel对照具体收费和客户。\n研究重点是公司产品与经营决策。近期内容只补充观察活跃度和获客方式；历史资料按原年份使用。\nExcel保留七张表：机构总览、收费权益、客户画像、活动旅行、账号声量、内容明细、经营测算。\n36家机构地图；五家婚恋重点；57项收费权益；15条分层或客户样例；9项活动旅行；73条公开内容。\n金额空白代表未取得可靠报价，0代表明确免费。定位、活动准入、公开样例分别标注。\n经营测算是可修改的条件演示，未作为竞品实绩或本公司销售预测。\n历史公开明细保留既有研究成果，按原时间、来源和核验状态阅读。\nPDF、Word与Excel保留原文链接；已核对链接嵌入和转换一致。平台可能仍需登录，公开链接也可能后续失效。\n不包含登录状态、Cookie、浏览器目录或私人联系方式。\n',encoding='utf-8')
audit={'report_pages':len(pdf.pages),'word_distinct_urls':len(wordurls),'pdf_link_annotations':len(pdfurls),'xlsx_links':len(linkcheck),'native_tables':6,'native_charts':1,'row_counts':expected,'formula_tests':'60人=78场/负60万元；90人=117场/0元，缺输入提示已验证','scope':'研究报告优先，近期内容为补充','remaining_evidence':'四家完整合同报价、成交客户分布、实际到场与复购及利润仍为公开资料缺口；具体见报告附录。'}
(B/'qa/最终交付核验.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2));print(json.dumps(audit,ensure_ascii=False))
for f in out.glob('*.inspect.ndjson'):f.unlink()
with zipfile.ZipFile(B/'中国高端线下社群市场研究资料_20261022.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted(out.rglob('*')):
  if f.is_file():z.write(f,f.relative_to(out))
