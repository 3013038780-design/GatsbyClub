import asyncio,json,hashlib,re
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from urllib.parse import urljoin,urlparse
from crawl4ai import AsyncWebCrawler,BrowserConfig,CrawlerRunConfig,CacheMode
B=Path(__file__).parent
SEEDS=[('行业入口','https://shshjxh.com/m_channel_org'),('行业入口','https://www.bjhqxh.com/nd.jsp?id=562'),('钻石婚恋','https://www.zuanshi.com/webActivity/activityList'),('钻石婚恋','https://www.zuanshi.com/webindex/zuanshijiyin'),('HIMMR','https://www.himmr.tech/'),('我主良缘','https://www.7799520.com/'),('我主良缘','https://www.7799520.com/party'),('金凤凰','https://www.jfh999.com/party/'),('金凤凰','https://www.jfh999.com/party/311.html'),('珍爱网','https://www.zhenai.com/'),('珍爱网','https://www.zhenai.com/n/directStore'),('百合佳缘线下VIP','https://vip.jiayuan.com/index.html'),('Seekr','https://www.huodongxing.com/event/8873852954600'),('MeetKnow','https://meetknow.com/activities'),('MarryU','https://apps.apple.com/cn/app/id1121909088'),('旅行产品囍上媒捎','https://jinrishangye.com/8357/'),('旅行产品玉渡山','https://www.sohu.com/a/1055933312_121626427')]
async def main():
 rows=[];queue=list(SEEDS);seen=set();follow={}
 async with AsyncWebCrawler(config=BrowserConfig(headless=True,verbose=False)) as c:
  while queue:
   brand,u=queue.pop(0)
   if u in seen:continue
   seen.add(u);key=hashlib.sha256(u.encode()).hexdigest()[:12];stamp=datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(timespec='seconds')
   try:
    r=await c.arun(url=u,config=CrawlerRunConfig(cache_mode=CacheMode.BYPASS,page_timeout=18000,wait_until='domcontentloaded',delay_before_return_html=1,verbose=False));tx=str(r.markdown or '');(B/'raw'/f'{key}.md').write_text(tx);(B/'raw'/f'{key}.html').write_text(r.html or '')
    row=dict(brand=brand,url=u,success=bool(r.success and len(tx)>150),status=r.status_code,chars=len(tx),file=key+'.md',collected=stamp,links=[])
    for a in (r.links or {}).get('internal',[]):
     v=urljoin(u,a.get('href',''));t=a.get('text','')
     if brand in ['钻石婚恋','百合佳缘线下VIP','MeetKnow','金凤凰'] and re.search(r'activityDetail|/party/\d|/events/|/activity/|review|past',v) and v not in seen and follow.get(brand,0)<3:
      queue.append((brand,v));follow[brand]=follow.get(brand,0)+1;row['links'].append([t,v])
    rows.append(row);print(brand,row['success'],len(tx),u,flush=True)
   except Exception as e:rows.append(dict(brand=brand,url=u,success=False,error=type(e).__name__,collected=stamp));print(brand,'ERROR',type(e).__name__,flush=True)
   (B/'网页采集记录.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
asyncio.run(main())
