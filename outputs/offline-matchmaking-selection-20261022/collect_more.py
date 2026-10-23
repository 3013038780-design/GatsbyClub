import asyncio,json,hashlib,re
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from urllib.parse import urljoin,urlparse
from crawl4ai import AsyncWebCrawler,BrowserConfig,CrawlerRunConfig,CacheMode
B=Path(__file__).parent
SEEDS=[('钻石婚恋', 'https://www.zuanshi.com/new/loveCustomization'), ('钻石婚恋', 'https://www.zuanshi.com/webActivity/newActivityList'), ('MarryU', 'https://m.51marryyou.com/'), ('上海爱之都', 'https://shshjxh.com/org_41'), ('上海都市白领', 'https://shshjxh.com/m_org_11'), ('上海才子佳人', 'https://shshjxh.com/m_org_52'), ('上海圣爱', 'https://shshjxh.com/m_org_8'), ('上海爱缘', 'https://shshjxh.com/m_org_53'), ('上海巾帼园', 'https://shshjxh.com/m_org_2'), ('如爱单身俱乐部', 'https://www.ruailove.com/'), ('爱重奏', 'https://www.aichongzou.com/'), ('爱重奏', 'https://www.aichongzou.com/chanpinyufuwu/38'), ('爱重奏', 'https://www.aichongzou.com/chanpinyufuwu/39'), ('爱重奏', 'https://www.aichongzou.com/chanpinyufuwu/40'), ('爱重奏', 'https://www.aichongzou.com/chanpinyufuwu/41'), ('MeetKnow', 'https://meetknow.com/activities/history'), ('MeetKnow', 'https://meetknow.com/activities/beijing/high-asset'), ('百合佳缘线下VIP', 'https://vip.jiayuan.com/index.html')]
async def main():
 rows=json.loads((B/'网页采集记录.json').read_text());queue=list(SEEDS);seen=set();follow={}
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
