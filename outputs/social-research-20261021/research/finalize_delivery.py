from pathlib import Path
from io import BytesIO
from zipfile import ZipFile,ZIP_DEFLATED
import json,csv,hashlib,html,re,shutil
from xml.etree import ElementTree as ET
B=Path(__file__).resolve().parents[1];O=B/'交付资料';P=O/'正式文件';data=json.loads((B/'research/交付工作簿数据.json').read_text())
f=P/'中国高端会员社群市场研究数据工作簿.xlsx'
ns='http://schemas.openxmlformats.org/spreadsheetml/2006/main';rn='http://schemas.openxmlformats.org/officeDocument/2006/relationships';pn='http://schemas.openxmlformats.org/package/2006/relationships'
ET.register_namespace('',ns);ET.register_namespace('r',rn)
def col(n):
 s=''
 while n:n,r=divmod(n-1,26);s=chr(65+r)+s
 return s
native=0
with ZipFile(f) as z:parts={n:z.read(n) for n in z.namelist()}
for i,s in enumerate(data['sheets'],1):
 sheetpath=f'xl/worksheets/sheet{i}.xml';relpath=f'xl/worksheets/_rels/sheet{i}.xml.rels';root=ET.fromstring(parts[sheetpath])
 rels=ET.fromstring(parts[relpath]) if relpath in parts else ET.Element('{'+pn+'}Relationships')
 links=root.find('{'+ns+'}hyperlinks')
 if links is None:links=ET.Element('{'+ns+'}hyperlinks')
 for ri,row in enumerate(s['rows'],5):
  for ci,v in enumerate(row,1):
   if isinstance(v,str) and re.fullmatch(r'https?://\S+',v):
    rid=f'PublicLink{ri}_{ci}';ET.SubElement(rels,'{'+pn+'}Relationship',{'Id':rid,'Type':rn+'/hyperlink','Target':v,'TargetMode':'External'})
    ET.SubElement(links,'{'+ns+'}hyperlink',{'ref':f'{col(ci)}{ri}','{'+rn+'}id':rid});native+=1
 if len(links):
  # OOXML hyperlink elements precede print and drawing elements.
  following={'printOptions','pageMargins','pageSetup','headerFooter','rowBreaks','colBreaks','customProperties','cellWatches','ignoredErrors','smartTags','drawing','legacyDrawing','legacyDrawingHF','picture','oleObjects','controls','webPublishItems','tableParts','extLst'}
  pos=next((j for j,e in enumerate(root) if e.tag.split('}')[-1] in following),len(root));root.insert(pos,links)
  parts[sheetpath]=ET.tostring(root,encoding='utf-8',xml_declaration=True);parts[relpath]=ET.tostring(rels,encoding='utf-8',xml_declaration=True)
with ZipFile(f,'w',ZIP_DEFLATED) as z:
 for n,v in parts.items():z.writestr(n,v)
# Remove the exporter diagnostic sidecar from the user delivery.
for p in P.glob('*.inspect.ndjson'):p.unlink()
counts=data['counts'];checks=json.loads((B/'research/pdf-url-checks.json').read_text());good=sum(isinstance(r[1],int) and r[1]<400 for r in checks)
for ext in ['json','csv']:
 shutil.copy2(B/f'social-platforms/统一内容指标.{ext}',O/f'数据明细/平台内容原始记录.{ext}')
guide='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>高端会员社群市场研究资料目录</title><style>body{font:16px/1.8 -apple-system,"PingFang SC",sans-serif;max-width:1000px;margin:48px auto;color:#222;padding:0 24px}h1{font-size:28px}h2{font-size:21px;margin-top:32px}a{color:#245c88}table{border-collapse:collapse;width:100%}td,th{border:1px solid #ddd;padding:10px;text-align:left}th{background:#f2f4f6}</style><h1>高端会员社群市场研究资料目录</h1><p>资料截至2026年10月21日。建议先读合伙人摘要，再查正式报告和数据工作簿。文件均保存在本资料包内。</p><h2>正式文件</h2><ul>'''
for p in sorted(P.iterdir()):
 if p.suffix in ['.docx','.pdf','.xlsx']:guide+=f'<li><a href="正式文件/{html.escape(p.name)}">{html.escape(p.name)}</a></li>'
guide+='</ul><h2>数据范围</h2><table><tr><th>资料</th><th>数量</th><th>说明</th></tr>'
for label,note,count in [('市场机构地图','包含候选、替代机构及相邻服务',counts['institutions']),('平台内容明细','逐条保留账号归属与核验状态',counts['platform_contents']),('扩展内容线索','搜索卡片记录，含重复内容和个人发布者',counts['discovery_records']),('网页采集尝试','包括复核和失败记录',counts['pages']),('公开网页正文存档','按采集批次保存，不代表独立网址数',counts['raw']),('自动提取片段','供定位和回到原文复核',counts['excerpts'])]:guide+=f'<tr><td>{label}</td><td>{count}</td><td>{note}</td></tr>'
guide+='</table><h2>查看明细及原文</h2><p>Excel各专题表提供筛选，来源台账“打开原文”已添加原生超链接。数据明细文件夹提供CSV版；公开网页存档文件夹保存已取得的正文，可按网页采集台账中的相对路径查找。未取得的原文没有补造文件。</p><ul>'
for p in sorted((O/'数据明细').glob('*.csv')):guide+=f'<li><a href="数据明细/{html.escape(p.name)}">{html.escape(p.name)}</a></li>'
guide+='</ul><h2>PDF链接检查</h2>'
guide+=f'<p>正式报告PDF保留190处网址链接及13处目录跳转，涉及51个不同网址。网络检查{good}个取得低于400的HTTP响应，4个出现超时或证书连接失败。HTTP响应仅说明本次连接结果，平台内容可能另需登录。</p>'
guide+='<p>实际点击验证：在macOS预览中点击报告第14页“2026年会票价及权益”，经阅读器确认后在Chrome打开木兰年会原始报名页，并看到票价与权益正文。点击结果截图及逐条网址检查在数据明细中。</p><p><a href="数据明细/PDF资料链接检查.csv">逐条链接检查</a>　<a href="数据明细/PDF外链点击验证.png">外链实际点击截图</a></p>'
guide+='<h2>后续工作</h2><p>正式报价、机构访谈、客户访谈、活动体验和收费试点的待验证字段，见Excel的证据缺口及后续验证表。本套为已有研究的整理交付。</p></html>'
(O/'资料目录.html').write_text(guide,encoding='utf-8')
(O/'交付说明.txt').write_text('请先打开 资料目录.html。\n正式文件包含报告PDF与Word、合伙人摘要、六家案例档案及25张表的Excel工作簿。\n数据明细为CSV；公开网页存档为采集取得的公开正文。\n报告链接实际点击验证及逐条网络检查见数据明细。\n资料截止2026年10月21日。\n',encoding='utf-8')
manifest=[]
for p in sorted(O.rglob('*')):
 if p.is_file() and p.name!='文件清单.csv':manifest.append([str(p.relative_to(O)),p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest()])
with (O/'文件清单.csv').open('w',encoding='utf-8-sig',newline='') as out:csv.writer(out).writerows([['包内文件','字节数','SHA256']]+manifest)
zipfile=B/'中国高端会员社群市场研究配套资料.zip'
with ZipFile(zipfile,'w',ZIP_DEFLATED) as z:
 for p in sorted(O.rglob('*')):
  if p.is_file():z.write(p,'中国高端会员社群市场研究资料/'+str(p.relative_to(O)))
print(json.dumps({'zip':str(zipfile),'size':zipfile.stat().st_size,'files':len(manifest)+1,'native_excel_links':native,**counts},ensure_ascii=False))
