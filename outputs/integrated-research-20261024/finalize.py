from pathlib import Path
from lxml import etree as E
from pypdf import PdfReader
import json,zipfile,shutil,csv,io
from urllib.parse import unquote
B=Path(__file__).parent;R=B.parents[1];O=B/'交付文件';D=json.loads((B/'统一研究数据.json').read_text());links=json.loads((B/'链接索引.json').read_text())
book=O/'高端线下社群市场调研与对标总表.xlsx';ns='http://schemas.openxmlformats.org/spreadsheetml/2006/main';rn='http://schemas.openxmlformats.org/officeDocument/2006/relationships';pn='http://schemas.openxmlformats.org/package/2006/relationships'
with zipfile.ZipFile(book)as z:files={n:z.read(n)for n in z.namelist()}
for num in range(1,6):
 items=[r for r in links if r['sheet']==num-1];f=f'xl/worksheets/sheet{num}.xml';rf=f'xl/worksheets/_rels/sheet{num}.xml.rels';root=E.fromstring(files[f]);rels=E.fromstring(files[rf])if rf in files else E.Element('{'+pn+'}Relationships',nsmap={None:pn})
 for e in root.findall('{'+ns+'}hyperlinks'):root.remove(e)
 for e in list(rels):
  if e.get('Id','').startswith('rIdStudy'):rels.remove(e)
 hs=E.Element('{'+ns+'}hyperlinks')
 for i,r in enumerate(items,1):
  rid='rIdStudy'+str(i);E.SubElement(hs,'{'+ns+'}hyperlink',ref=r['cell'],attrib={'{'+rn+'}id':rid});E.SubElement(rels,'{'+pn+'}Relationship',Id=rid,Type=rn+'/hyperlink',Target=r['url'],TargetMode='External')
 before=next((e for e in root if E.QName(e).localname in ['printOptions','pageMargins','pageSetup','headerFooter','drawing','tableParts','extLst']),None)
 root.insert(list(root).index(before),hs)if before is not None else root.append(hs)
 files[f]=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True);files[rf]=E.tostring(rels,xml_declaration=True,encoding='UTF-8',standalone=True)
with zipfile.ZipFile(book,'w',zipfile.ZIP_DEFLATED)as z:
 for n,v in files.items():z.writestr(n,v)
with zipfile.ZipFile(book)as z:
 verified=0
 for num in range(1,6):
  root=E.fromstring(z.read(f'xl/worksheets/sheet{num}.xml'));relmap={e.get('Id'):e.get('Target')for e in E.fromstring(z.read(f'xl/worksheets/_rels/sheet{num}.xml.rels'))}
  for e in root.findall('{'+ns+'}hyperlinks/{'+ns+'}hyperlink'):
   expected=next(r['url']for r in links if r['sheet']==num-1 and r['cell']==e.get('ref'));assert expected==relmap[e.get('{'+rn+'}id')];verified+=1
 assert verified==len(links)
 assert b'not implemented'not in b''.join(v for k,v in files.items()if k.endswith('.xml'))
pdf=B/'qa/delivery/高端线下社群市场调研与对标报告.pdf';reader=PdfReader(pdf);text='\n'.join(p.extract_text()or''for p in reader.pages)
assert '高端线下社群' in text and '亿元总资产家庭'in text
assert '市场调研'in text and '第二部分 对标'in text
with zipfile.ZipFile(O/'高端线下社群市场调研与对标报告.docx')as z:
 doclinks=[e.get('Target')for e in E.fromstring(z.read('word/_rels/document.xml.rels'))if e.get('Type','').endswith('/hyperlink')]
 docxml=E.fromstring(z.read('word/document.xml'));bookmarks=docxml.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}bookmarkStart')
pdflinks=[]
for page in reader.pages:
 for ref in page.get('/Annots',[]):
  a=ref.get_object().get('/A',{});u=a.get('/URI')
  if u:pdflinks.append(str(u))
assert set(map(unquote,doclinks))<=set(map(unquote,pdflinks)),(set(map(unquote,doclinks))-set(map(unquote,pdflinks)))
assert len(bookmarks)==16
shutil.copy2(pdf,O/pdf.name)
qa=dict(report_pages=len(reader.pages),report_external_unique_urls=len(set(doclinks)),pdf_external_annotations=len(pdflinks),report_all_external_targets_preserved=True,internal_contents=16,workbook_sheets=5,workbook_native_links=verified,workbook_all_targets_verified=True,institutions=len(D['market']),products=len(D['products']),raw_content_rows=len(D['contents']),web_tasks=len(D['ledger']),web_success=sum(bool(x.get('success'))for x in D['ledger']),notes='平台可能要求登录；超链接结构验证与所有网址匿名可访问为不同检查')
(B/'qa/交付核验.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
readme='''高端线下社群市场调研与对标 2026年10月24日

先读正式PDF；Word可编辑；Excel先看市场调研和对标产品两张表，其余为追溯附件。
重点是5家机构6条产品线，商业、婚恋与旅行分用途。完整名录保留{institutions}条机构与品牌线索，各条核验深度见用途栏。
资料包包含本轮公开网页采集、平台公开内容、BoL实查截图和原研究结构化记录。未包含登录状态、Cookie、浏览器档案或用户会议记录。
BoL网页链接不可用：请在微信搜索BoL万象博联，打开VIP与Selected活动；截图在证据/BoL。
小红书和抖音原文可能要求登录；平台页面和签名链接可能随时间变化。
报价的适用日、单位和包含项请见正文与Excel。前轮研究试价与财务模型为历史规划，未替换成已成交事实。
本包报告与总Excel使用同一份研究数据，作为本次统一版本。
'''
readme=readme.replace('{institutions}',str(len(D['market'])))
pack=O/'高端线下社群调研资料包.zip'
with zipfile.ZipFile(pack,'w',zipfile.ZIP_DEFLATED)as z:
 z.writestr('阅读说明.txt',readme)
 for name in ['高端线下社群市场调研与对标报告.docx','高端线下社群市场调研与对标报告.pdf','高端线下社群市场调研与对标总表.xlsx']:z.write(O/name,name)
 z.write(B/'统一研究数据.json','数据/统一研究数据.json');z.write(B/'qa/交付核验.json','数据/交付核验.json')
 for key in ['macro','products','market','contents']:
  s=io.StringIO();wr=csv.writer(s);headers={'macro':['分类','指标','数值','单位','统计时间','定义及用途','来源编号'],'products':['方向','机构及产品','明确金额','单位与权益','客户画像','活动流程','获客及经营证据','研究判断','来源编号'],'market':['机构或品牌','组织方式','地区','目标客户','研究用途','原文'],'contents':['记录类型','账号','发布日期','标题','点赞','收藏','评论','分享','采集时间','原文']};wr.writerow(headers[key]);wr.writerows(D[key]);z.writestr('数据/'+key+'.csv','\ufeff'+s.getvalue())
 # Strict allowlist: only public evidence, never crawler browser state or auth configuration.
 for folder,label in [('integrated-research-20261024','本轮商业婚恋'),('travel-discovery-20261024','旅游补查')]:
  base=R/'.research-private'/folder
  for sub in ['web-raw','social-platforms','public-product-images']:
   p=base/sub
   if p.exists():
    for f in p.iterdir():
     if f.is_file()and f.suffix in ['.jsonl','.md','.html','.webp','.png']and not any(t in f.name.lower()for t in ['cookie','login','state','session','token']):z.write(f,'证据/'+label+'/'+sub+'/'+f.name)
  for name in ['网页采集台账.json','补充网页采集台账.json','心动计划产品核验.json','奇语旅行跨平台核验.json','定向正文核验.json']:
   if (base/name).exists():z.write(base/name,'证据/'+label+'/'+name)
 base=R/'.research-private/execution-followthrough-20261024'
 for sub in ['web-raw','public-product-images','social-platforms']:
  folder=base/sub
  if folder.exists():
   for f in folder.iterdir():
    if not f.is_file()or f.suffix not in ['.md','.html','.jsonl','.jpg','.webp']:continue
    if any(t in f.name.lower()for t in ['login','cookie','session','state','contact']):continue
    target='证据/追加商业婚恋/'+sub+'/'+f.name
    if f.suffix=='.jsonl':
     def clean(v):
      if isinstance(v,dict):return {k:clean(x)for k,x in v.items()if k.lower()not in ['source_token','xsec_token','cookie','cookies','password','access_token','refresh_token']}
      if isinstance(v,list):return [clean(x)for x in v if not(isinstance(x,dict)and x.get('show')is False)]
      return v
     lines=[json.dumps(clean(json.loads(x)),ensure_ascii=False)for x in f.read_text().splitlines()if x.strip()];z.writestr(target,'\n'.join(lines)+'\n')
    else:z.write(f,target)
 for name in ['商业婚恋补查台账.json']:
  if(base/name).exists():z.write(base/name,'证据/追加商业婚恋/'+name)
 base=R/'.research-private/bol-research-20261024'
 for f in base.iterdir():
  if f.is_file()and(f.suffix=='.png'and f.name.startswith(('vip-','selected-'))or f.name=='会籍实查.json'):z.write(f,'证据/BoL/'+f.name)
 fresh=R/'.research-private/conclusion-refresh-20261024'
 if (fresh/'网页采集台账.json').exists():z.write(fresh/'网页采集台账.json','证据/结论补查/网页采集台账.json')
 user_bol=R/'.research-private/execution-followthrough-20261024/user-bol-evidence'
 if user_bol.exists():
  for f in user_bol.iterdir():
   if f.is_file()and f.suffix in ['.jpg','.json']:z.write(f,'证据/BoL用户补充/'+f.name)
 for rel,label in [('outputs/five-offline-matchmaking-20261022/正式报告数据.json','历史/婚恋结构化记录.json'),('outputs/travel-community-20261023/研究与产品数据.json','历史/旅行及国外案例记录.json'),('.research-private/benchmark-selection-20261024/候选选择及研究判断.json','历史/前轮候选及取舍.json')]:z.write(R/rel,label)
print(json.dumps(qa,ensure_ascii=False));print('Package',round(pack.stat().st_size/1024/1024,2),'MB')
