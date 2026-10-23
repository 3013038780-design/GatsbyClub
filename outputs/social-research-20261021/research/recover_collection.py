"""Recover completed source records if a later download stalls."""
import json,hashlib
from collect_community import ROOT,NOW,SEEDS,PDFS,evidence,save_csv,PATTERNS
pages=[];snippets=[]
for line in (ROOT/'run.log').read_text().splitlines():
 if not line.startswith('{'):continue
 try:r=json.loads(line)
 except ValueError:continue
 if 'url' not in r:continue
 fid=hashlib.sha256(r['url'].encode()).hexdigest()[:14]
 good=r['status']=='已采集'
 pages.append(dict(机构=r['brand'],网址=r['url'],状态=r['status'],HTTP状态='',正文字数=r['chars'],采集时间=NOW,原文文件=f'raw/{fid}.md' if good else '',错误='' if good else '失败或正文不足；详见运行日志'))
 if good:snippets.extend(evidence(r['brand'],r['url'],(ROOT/'raw'/f'{fid}.md').read_text()))
for brand,url in PDFS:
 fid=hashlib.sha256(url.encode()).hexdigest()[:14];p=ROOT/'raw'/f'{fid}.txt'
 if p.exists():
  import re
  text=p.read_text()
  parts=re.split(r'--- PDF第(\d+)页 ---',text)
  for i in range(1,len(parts),2):snippets.extend(evidence(brand,url,parts[i+1],int(parts[i])))
  pages.append(dict(机构=brand,网址=url,状态='已采集',HTTP状态='',正文字数=len(text),采集时间=NOW,原文文件=f'raw/{fid}.pdf',错误=''))
 else:pages.append(dict(机构=brand,网址=url,状态='采集失败',HTTP状态='',正文字数=0,采集时间=NOW,原文文件='',错误='下载未完成，已停止本次请求'))
data=dict(collected_at=NOW,pages=pages,evidence=snippets,activity_links=[])
(ROOT/'collection.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
save_csv('网页采集台账.csv',pages,['机构','网址','状态','HTTP状态','正文字数','采集时间','原文文件','错误'])
save_csv('价格权益及运营证据.csv',snippets,['机构','字段','原文片段','来源','PDF页码','采集时间','证据类型'])
summary=[]
for brand in SEEDS:
 own=[p for p in pages if p['机构']==brand];ev=[p for p in snippets if p['机构']==brand]
 summary.append(dict(机构=brand,成功页数=sum(p['状态']=='已采集' for p in own),失败页数=sum(p['状态']!='已采集' for p in own),证据片段数=len(ev),活动会籍链接数=0,**{k:sum(r['字段']==k for r in ev) for k in PATTERNS}))
(ROOT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
save_csv('机构采集覆盖.csv',summary,['机构','成功页数','失败页数','证据片段数','活动会籍链接数',*PATTERNS])
print(json.dumps({'sources':len(pages),'success':sum(p['状态']=='已采集' for p in pages),'snippets':len(snippets)}))
