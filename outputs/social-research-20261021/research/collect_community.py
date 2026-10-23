"""Reproducible public-source collection; no login or external LLM required."""
import asyncio, csv, hashlib, html, json, re, sys
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from urllib.parse import urlparse, urljoin, urldefrag
import urllib.request
import time

ROOT = Path(__file__).resolve().parents[1] / 'collection-20261021'
ROOT.mkdir(exist_ok=True)
(ROOT/'raw').mkdir(exist_ok=True)
NOW = datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(timespec='seconds')
MAX_FOLLOWUPS_PER_BRAND=4
SEEDS = {
 '京城俱乐部':['https://thecapitalclub.com/zh-hans/julebulishi/','https://thecapitalclub.com/membership/','https://thecapitalclub.com/clubactiveties/'],
 '北京香港马会会所':['https://www.beijingclubhouse.com/zh-CN/aboutus-thebeijingclubhouse.aspx','https://www.beijingclubhouse.com/zh-CN/rulesandregulations.aspx'],
 '黑骑士球员俱乐部':['https://www.tpc.com.cn/membership','https://www.tpc.com.cn/abouttheplayersclub'],
 '观澜湖':['https://www.missionhillschina.com/memberlife/index.html','https://www.missionhillschina.com/golf-membership/members-activities/'],
 'HIGHER CLUB':['https://www.higherclub.cn/'],
 '雪茄客':['https://www.cigarambassador.com/home/'],
 '长江商学院':['https://www.ckgsb.com/emba/','https://www.ckgsb.com/emba/common_problems/'],
 '中欧国际工商学院':['https://cn.ceibs.cn/alumni'],
 'EO中国':['https://member.eonetwork.org/chinaeast/about-our-chapter/','https://eoshanghai.org/about-us/','https://eoshanghai.org/our-members/'],
 '北大汇丰EDP':['https://edp.phbs.pku.edu.cn/','https://edp.phbs.pku.edu.cn/info/1271/13221.htm'],
 '深商联':['https://www.shenshang.org/sgcc/about-sgcc'],
 '深圳侨商':['https://www.socia.org/Member/user/Chamber.html'],
 '正和岛':['https://www.zhisland.com/'],
 '领教工坊':['https://www.clec.com.cn/','https://www.clec.com.cn/p/guanyulingjiaogongfang.html'],
 '木兰汇':['https://www.iceo.com.cn/zt/2026_mulannh/'],
}
PDFS=[('北京香港马会会所','https://member.hkjc.com/ecard/eHarmony_Jun25.pdf'),('长江商学院','https://www.ckgsb.edu.cn/uploads/embavideo/2026EMBAmanual.pdf')]
PATTERNS={
 '价格收费':r'入会费|报名费|学费|年费|月费|会费|人民币|membership dues|annual dues|initiation fee',
 '产品权益':r'会员权益|会籍|附属卡|家庭|配偶|社交会籍|会员活动|membership|benefits',
 '客户与规模':r'会员.{0,18}[0-9,]+|[0-9,]+.{0,8}会员|校友.{0,12}[0-9,]+|成员|平均年龄|核心决策|Members as of',
 '获客与推荐':r'推荐|转介绍|申请入会|申请加入|微信公众号|小程序|体验会|Apply|referral',
 '活动与流程':r'签到|议程|活动回顾|邀请函|赛事|参访|晚宴|游学|报名|年会|续会|续费|出席',
}
LINK_RX=re.compile(r'活动|会籍|会员|收费|费用|章程|校友|参访|赛事|年会|membership|events|alumni|fees',re.I)
EXCLUDE=re.compile(r'登录|注册|申请入会|联系我们|立即申请|提交|login|sign.in|apply|contact|javascript:|mailto:|tel:',re.I)

def save_csv(name, rows, columns):
 with (ROOT/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=columns,extrasaction='ignore'); w.writeheader();w.writerows(rows)

def evidence(brand,url,txt,page=None):
 rows=[]; seen=set()
 for category,pat in PATTERNS.items():
  for m in re.finditer(pat,txt,re.I):
   excerpt=re.sub(r'\s+',' ',txt[max(0,m.start()-70):m.end()+200]).strip()
   key=(category,excerpt)
   if key in seen: continue
   seen.add(key)
   rows.append(dict(机构=brand,字段=category,原文片段=excerpt,来源=url,PDF页码=page or '',采集时间=NOW,证据类型='机构公开资料；待逐条复核'))
   if sum(x['字段']==category for x in rows)>=12:break
 return rows

async def main():
 from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
 browser=BrowserConfig(headless=True,verbose=False,ignore_https_errors=False)
 config=CrawlerRunConfig(cache_mode=CacheMode.BYPASS,page_timeout=35000,wait_until='domcontentloaded',delay_before_return_html=2,verbose=False)
 pages=[]; snippets=[]; activity=[]; seen=set();sem=asyncio.Semaphore(3)
 async with AsyncWebCrawler(config=browser) as crawler:
  async def collect(brand,url,depth=0):
   url=urldefrag(url)[0]
   if url in seen:return []
   seen.add(url)
   async with sem:
    try:
     result=await crawler.arun(url=url,config=config)
     txt=str(result.markdown or '')
     status='已采集' if result.success and len(txt.strip())>100 else '失败或正文不足'
     file_id=hashlib.sha256(url.encode()).hexdigest()[:14]
     if status=='已采集':
      (ROOT/'raw'/f'{file_id}.md').write_text(txt,encoding='utf-8')
      (ROOT/'raw'/f'{file_id}.html').write_text(result.html or '',encoding='utf-8')
      snippets.extend(evidence(brand,url,txt))
     pages.append(dict(机构=brand,网址=url,状态=status,HTTP状态=result.status_code,正文字数=len(txt),采集时间=NOW,原文文件=f'raw/{file_id}.md' if status=='已采集' else '',错误=str(result.error_message or '')[:180]))
     candidates=[]
     for link in result.links.get('internal',[])+result.links.get('external',[]):
      title=(link.get('text') or '').strip(); href=urldefrag(urljoin(url,link.get('href','')))[0]
      if not title or EXCLUDE.search(title+' '+href) or not LINK_RX.search(title):continue
      if href.lower().endswith(('.jpg','.png','.zip','.pdf')):continue
      activity.append(dict(机构=brand,链接标题=title,详情网址=href,发现页=url,采集时间=NOW,状态='链接线索，尚未判断已举办'))
      if href not in seen and urlparse(href).hostname==urlparse(url).hostname:candidates.append((brand,href,1))
     print(json.dumps({'brand':brand,'status':status,'chars':len(txt),'url':url},ensure_ascii=False),flush=True)
     return candidates if depth==0 else []
    except Exception as e:
     pages.append(dict(机构=brand,网址=url,状态='采集失败',HTTP状态='',正文字数=0,采集时间=NOW,原文文件='',错误=str(e)[:180]))
     print(json.dumps({'brand':brand,'error':str(e)[:120]},ensure_ascii=False),flush=True)
     return []
  first=await asyncio.gather(*(collect(b,u) for b,urls in SEEDS.items() for u in urls))
  follow=[]; per_brand={}; queue_seen=set()
  for links in first:
   for b,u,d in links:
    if u in seen or u in queue_seen or per_brand.get(b,0)>=MAX_FOLLOWUPS_PER_BRAND:continue
    queue_seen.add(u);per_brand[b]=per_brand.get(b,0)+1;follow.append((b,u,d))
  await asyncio.gather(*(collect(*row) for row in follow))
 # PDFs: extract each page, retaining page number with every snippet.
 import pymupdf as fitz
 for brand,url in PDFS:
  try:
   def download():
    started=time.monotonic();chunks=[]
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'CommunityResearch/1.0'}),timeout=12) as r:
     while True:
      if time.monotonic()-started>45:raise TimeoutError('PDF下载超过45秒，保留其他采集结果')
      block=r.read(65536)
      if not block:break
      chunks.append(block)
      if sum(map(len,chunks))>40000000:raise ValueError('PDF超过本批40MB下载上限')
    return b''.join(chunks)
   raw=await asyncio.to_thread(download)
   if not raw.startswith(b'%PDF'):raise ValueError('返回内容不是PDF')
   file_id=hashlib.sha256(url.encode()).hexdigest()[:14];path=ROOT/'raw'/f'{file_id}.pdf';path.write_bytes(raw)
   doc=fitz.open(path);texts=[]
   for n,p in enumerate(doc,1):
    txt=p.get_text();texts.append(f'\n--- PDF第{n}页 ---\n'+txt);snippets.extend(evidence(brand,url,txt,n))
   full='\n'.join(texts);(ROOT/'raw'/f'{file_id}.txt').write_text(full,encoding='utf-8')
   pages.append(dict(机构=brand,网址=url,状态='已采集',HTTP状态=200,正文字数=len(full),采集时间=NOW,原文文件=f'raw/{file_id}.pdf',错误=''))
   print(json.dumps({'brand':brand,'pdf_pages':len(doc),'chars':len(full)},ensure_ascii=False),flush=True)
  except Exception as e:pages.append(dict(机构=brand,网址=url,状态='采集失败',HTTP状态='',正文字数=0,采集时间=NOW,原文文件='',错误=str(e)[:180]))
 # Deduplicate identical records and links, keeping all original-page relationships on disk.
 activity=list({(r['机构'],r['详情网址']):r for r in activity}.values())
 payload=dict(collected_at=NOW,pages=pages,evidence=snippets,activity_links=activity)
 (ROOT/'collection.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
 save_csv('网页采集台账.csv',pages,['机构','网址','状态','HTTP状态','正文字数','采集时间','原文文件','错误'])
 save_csv('价格权益及运营证据.csv',snippets,['机构','字段','原文片段','来源','PDF页码','采集时间','证据类型'])
 save_csv('活动与会籍链接清单.csv',activity,['机构','链接标题','详情网址','发现页','采集时间','状态'])
 summary=[]
 for brand in SEEDS:
  own=[p for p in pages if p['机构']==brand];ev=[p for p in snippets if p['机构']==brand]
  summary.append(dict(机构=brand,成功页数=sum(p['状态']=='已采集' for p in own),失败页数=sum(p['状态']!='已采集' for p in own),证据片段数=len(ev),活动会籍链接数=sum(p['机构']==brand for p in activity),**{k:sum(r['字段']==k for r in ev) for k in PATTERNS}))
 save_csv('机构采集覆盖.csv',summary,['机构','成功页数','失败页数','证据片段数','活动会籍链接数',*PATTERNS])
 (ROOT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({'total_pages':len(pages),'success':sum(p['状态']=='已采集' for p in pages),'evidence':len(snippets),'links':len(activity),'output':str(ROOT)},ensure_ascii=False),flush=True)

if __name__=='__main__':asyncio.run(main())
