from pathlib import Path
import zipfile,json,shutil,re,hashlib
from lxml import etree as E
from pypdf import PdfReader
from urllib.parse import unquote
B=Path(__file__).parent;R=B.parents[1];O=B/'交付文件';book=O/'启动产品与费用测算.xlsx';links=json.loads((B/'链接索引.json').read_text());ns='http://schemas.openxmlformats.org/spreadsheetml/2006/main';rn='http://schemas.openxmlformats.org/officeDocument/2006/relationships';pn='http://schemas.openxmlformats.org/package/2006/relationships'
with zipfile.ZipFile(book)as z:files={n:z.read(n)for n in z.namelist()}
for num in [2]:
 items=[r for r in links if r['sheet']==num-1];f=f'xl/worksheets/sheet{num}.xml';rf=f'xl/worksheets/_rels/sheet{num}.xml.rels';root=E.fromstring(files[f]);rels=E.fromstring(files[rf])if rf in files else E.Element('{'+pn+'}Relationships',nsmap={None:pn})
 for e in root.findall('{'+ns+'}hyperlinks'):root.remove(e)
 for e in list(rels):
  if e.get('Id','').startswith('rIdLaunch'):rels.remove(e)
 hs=E.Element('{'+ns+'}hyperlinks')
 for i,r in enumerate(items,1):
  rid='rIdLaunch'+str(i);E.SubElement(hs,'{'+ns+'}hyperlink',ref=r['cell'],attrib={'{'+rn+'}id':rid});E.SubElement(rels,'{'+pn+'}Relationship',Id=rid,Type=rn+'/hyperlink',Target=r['url'],TargetMode='External')
 before=next((e for e in root if E.QName(e).localname in ['printOptions','pageMargins','pageSetup','headerFooter','drawing','tableParts','extLst']),None);root.insert(list(root).index(before),hs)if before is not None else root.append(hs);files[f]=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True);files[rf]=E.tostring(rels,xml_declaration=True,encoding='UTF-8',standalone=True)
with zipfile.ZipFile(book,'w',zipfile.ZIP_DEFLATED)as z:
 for n,v in files.items():z.writestr(n,v)
with zipfile.ZipFile(book)as z:
 root=E.fromstring(z.read('xl/worksheets/sheet2.xml'));assert len(root.findall('{'+ns+'}hyperlinks/{'+ns+'}hyperlink'))==len(links)
pdf=B/'qa/meeting/高端线下社群合伙人会议讲解稿.pdf';shutil.copy2(pdf,O/pdf.name);reader=PdfReader(pdf);assert len(reader.pages)==5
urls=[]
for p in reader.pages:
 for ref in p.get('/Annots',[]):
  a=ref.get_object().get('/A',{});u=a.get('/URI')
  if u:urls.append(str(u))
with zipfile.ZipFile(O/'高端线下社群合伙人会议讲解稿.docx')as z:targets=[e.get('Target')for e in E.fromstring(z.read('word/_rels/document.xml.rels'))if e.get('Type','').endswith('/hyperlink')]
assert set(map(unquote,targets))<=set(map(unquote,urls))
site=B/'site/dist';shutil.copy2(O/'高端线下社群合伙人会议讲解稿.docx',site/'meeting.docx');shutil.copy2(book,site/'launch.xlsx')
pack=R/'outputs/integrated-research-20261024/交付文件/高端线下社群调研资料包.zip'
with zipfile.ZipFile(pack)as z:entries={n:z.read(n)for n in z.namelist()}
note='附录含五页口语讲稿、完整HTML阅读版和可调整启动测算。试价与成本情景属于初案，供应商团体报价和客户付费反馈尚未确认。'
readme=entries['阅读说明.txt'].decode()
readme=re.sub(r'\n附录含[^\n]*','',readme)
entries['阅读说明.txt']=(readme.rstrip()+'\n\n'+note+'\n新增官网补查发布结构化字段、原文链接和哈希；完整抓取仅本机保存。\n').encode()
for name in ['启动产品与费用测算.xlsx','高端线下社群合伙人会议讲解稿.docx','高端线下社群合伙人会议讲解稿.pdf']:entries['初案附件/'+name]=(O/name).read_bytes()
for f in (R/'.research-private/execution-followthrough-20261024').glob('瑞吉-*'):
 if f.suffix in ['.png','.txt']:entries['初案附件/酒店报价证据/'+f.name]=f.read_bytes()
comparison=B/'同线路报价核查补充.md'
if comparison.exists():entries['初案附件/'+comparison.name]=comparison.read_bytes()
activity_options=B/'初期活动形式选择.md'
if activity_options.exists():entries['初案附件/'+activity_options.name]=activity_options.read_bytes()
comparison_sources=R/'.research-private/execution-followthrough-20261024/trip-cost-comparison'
if comparison_sources.exists():
 for f in comparison_sources.glob('*'):
  if f.suffix in ['.md','.json']:entries['初案附件/同线路补查证据/'+f.name]=f.read_bytes()
for name in ['携程同日核价.json']:
 if (B/name).exists():entries['初案附件/'+name]=(B/name).read_bytes()
public_excerpt=R/'.research-private/execution-followthrough-20261024/resumed-login/携程结算页公开价格摘录.txt'
if public_excerpt.exists():entries['初案附件/酒店报价证据/'+public_excerpt.name]=public_excerpt.read_bytes()
for n in ['交付核验.json','内容覆盖核验.json','逐页复核结果.json']:entries['数据/'+n]=(R/'outputs/integrated-research-20261024/qa'/n).read_bytes()
for f in (B/'site/dist').rglob('*'):
 if f.is_file()and f.suffix in ['.html','.pdf','.docx','.xlsx','.jpg','.png']:entries['HTML阅读版/'+str(f.relative_to(B/'site/dist'))]=f.read_bytes()
for n in ['HTML内容核验.json','网站浏览器验收.json']:
 if(B/'qa'/n).exists():entries['数据/'+n]=(B/'qa'/n).read_bytes()
for n in ['计划验收审计.json']:
 entries['数据/'+n]=(R/'outputs/integrated-research-20261024/qa'/n).read_bytes()
# Keep the new full pages on this machine, publish source hashes and structured facts.
entries={n:v for n,v in entries.items()if not n.startswith('证据/结论补查/web-raw/')}
fresh=R/'.research-private/conclusion-refresh-20261024'
if(fresh/'网页采集台账.json').exists():entries['证据/结论补查/网页采集台账.json']=(fresh/'网页采集台账.json').read_bytes()
research=json.loads((R/'outputs/integrated-research-20261024/统一研究数据.json').read_text())
entries['证据/结论补查/结构化核验.json']=json.dumps({'sources':[x for x in research['sources']if re.fullmatch('R[0-9]+',x['id'])],'products':[x for x in research['products']if x[8].startswith('R')],'conclusions':research['conclusions'],'travel_forms':research['travel_forms']},ensure_ascii=False,indent=2).encode()
with zipfile.ZipFile(pack,'w',zipfile.ZIP_DEFLATED)as z:
 for n,v in entries.items():z.writestr(n,v)
with zipfile.ZipFile(pack)as z:assert z.testzip()is None
for f in O.glob('*.inspect.ndjson'):f.replace(B/'qa'/f.name)
(B/'qa/配套核验.json').write_text(json.dumps(dict(meeting_pages=5,meeting_links_preserved=True,model_native_links=len(links),package_files=len(entries),remote_page_updated=(R/'.research-private/execution-followthrough-20261024/Page同步核验.json').exists(),website_browser_qa_pending=not(B/'qa/网站浏览器验收.json').exists()),ensure_ascii=False,indent=2));print('Execution attachments verified')
