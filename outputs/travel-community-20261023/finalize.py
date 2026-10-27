from pathlib import Path
import json,zipfile,shutil,csv
from lxml import etree as E
from pypdf import PdfReader
B=Path(__file__).resolve().parent;O=B/'deliverables';D=json.loads((B/'研究与产品数据.json').read_text())
for folder in ['report-final','summary-final','speech-final']:
 for p in (B/'qa'/folder).glob('*.pdf'):shutil.copy2(p,O/p.name)
# Native external links, preserving all table and drawing relationships.
f=O/'高端单身旅行与线下社群研究数据.xlsx';links=json.loads((B/'链接索引.json').read_text());ns='http://schemas.openxmlformats.org/spreadsheetml/2006/main';rn='http://schemas.openxmlformats.org/officeDocument/2006/relationships';pn='http://schemas.openxmlformats.org/package/2006/relationships'
with zipfile.ZipFile(f) as z:files={n:z.read(n) for n in z.namelist()}
for num in range(1,6):
 items=[x for x in links if x['sheet']==num-1]
 if not items:continue
 path=f'xl/worksheets/sheet{num}.xml';rp=f'xl/worksheets/_rels/sheet{num}.xml.rels';root=E.fromstring(files[path]);rels=E.fromstring(files[rp]) if rp in files else E.Element('{'+pn+'}Relationships',nsmap={None:pn})
 for e in list(root.findall('{'+ns+'}hyperlinks')):root.remove(e)
 for e in list(rels):
  if e.get('Id','').startswith('rIdResearch'):rels.remove(e)
 hs=E.Element('{'+ns+'}hyperlinks')
 for i,x in enumerate(items):
  rid='rIdResearch'+str(i+1);E.SubElement(hs,'{'+ns+'}hyperlink',ref=x['cell'],attrib={'{'+rn+'}id':rid});E.SubElement(rels,'{'+pn+'}Relationship',Id=rid,Type=rn+'/hyperlink',Target=x['url'],TargetMode='External')
 before=root.find('{'+ns+'}pageMargins')
 if before is None:
  before=next((e for e in root if E.QName(e).localname in ['drawing','tableParts','extLst']),None)
 if before is not None:root.insert(list(root).index(before),hs)
 else:root.append(hs)
 files[path]=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True);files[rp]=E.tostring(rels,xml_declaration=True,encoding='UTF-8',standalone=True)
with zipfile.ZipFile(f,'w',zipfile.ZIP_DEFLATED) as z:
 for n,v in files.items():z.writestr(n,v)
check={}
for p in O.glob('*.pdf'):
 r=PdfReader(p);urls=[a.get_object().get('/A',{}).get('/URI') for page in r.pages for a in page.get('/Annots',[])];urls=[str(x) for x in urls if x]
 check[p.name]={'pages':len(r.pages),'external_annotations':len(urls),'unique_urls':len(set(urls))}
with zipfile.ZipFile(O/'高端单身旅行与线下社群研究报告.docx') as z:
 rel=E.fromstring(z.read('word/_rels/document.xml.rels'));wordurls={a.get('Target') for a in rel if a.get('Type')==rn+'/hyperlink'}
pdf=PdfReader(O/'高端单身旅行与线下社群研究报告.pdf');pdfurls={str(a.get_object().get('/A',{}).get('/URI')) for page in pdf.pages for a in page.get('/Annots',[]) if a.get_object().get('/A',{}).get('/URI')}
check['word_pdf_link_difference']=sorted(wordurls-pdfurls)
assert not check['word_pdf_link_difference']
with zipfile.ZipFile(f) as z:
 names=E.fromstring(z.read('xl/workbook.xml')).find('{'+ns+'}sheets');check['sheet_names']=[a.get('name') for a in names]
 check['native_charts']=len([n for n in z.namelist() if '/charts/chart' in n and n.endswith('.xml')]);check['xlsx_hyperlinks']=len(links)
 check['native_sensitivity_tables']=sum(z.read(n).count(b't="dataTable"') for n in z.namelist() if n.startswith('xl/worksheets/sheet') and n.endswith('.xml'))
 assert len(names)==5 and check['native_charts']==1
(B/'qa/交付结构核查.json').write_text(json.dumps(check,ensure_ascii=False,indent=2))
H=O/'历史附件';H.mkdir(exist_ok=True);shutil.copy2(B.parent/'five-offline-matchmaking-20261022/交付文件/高端线下社群研究数据.xlsx',H/'前轮七表工作簿_20261022.xlsx')
with (O/'供应商询价回填.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['线路及日期','供应商及收款主体','旅行许可','人数','酒店房型及独住','含税总价','含税单人价','包含','不含','定金及尾款','退改及不可退成本','有效期','联系人','书面凭据'])
 for route in ['三亚2026-11-19至22四天三晚','北京周边2026-11-14至15两天一晚']:
  for n in [10,12,14,16]:w.writerow([route,'','',n,'每人独住基础房']+['']*9)
with (O/'客户访谈回填.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['匿名编号','客群与关系状态','年龄','工作岗位与节奏','收入自述及时间','个人总资产','个人可投资资产','家庭总资产','近年真实购买及价格','兴趣投入及频次','一对一或小组偏好','可出行日期','独住偏好','同行期待','晚宴1680选择与理由','旅行19800选择与理由','顾虑及退出原因','是否愿再次联系','访谈人及日期'])
 for i in range(1,13):w.writerow([f'访谈{i:02}']+['']*18)
(O/'交付说明.txt').write_text('高端单身旅行与线下社群研究 2026年10月23日\n\n先读决策摘要，再读正式报告；五表Excel包含对标、同线路成本、可调整模型、来源待补及既有36家名录。\n研究讨论网站.html为当前讨论入口，可离线打开，报价和初始测算与报告一致；历史国外案例网站及历史附件仅供回溯，不代表当前方案。\n\n试价1680／680／19800元为规划输入，尚待客户反馈。供应商询价和客户访谈未开展，两个CSV可直接回填；它们不会自动覆盖模型。\n模型可修改蓝字输入，三亚直接交付成本链接同线路费用表G6至G11，绿色为跨表公式。人数和价格、退款的敏感性采用Excel原生数据表；兼容性不足的软件可能只显示已计算缓存，建议用桌面Excel打开。现金保守按工时报酬全部支付估算。\n\n新增资料私有保存，未推送公开GitHub。原有资料保留。\n')
print(json.dumps(check,ensure_ascii=False))
