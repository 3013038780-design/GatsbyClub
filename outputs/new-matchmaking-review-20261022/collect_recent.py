import asyncio,json,hashlib,csv
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from crawl4ai import AsyncWebCrawler,BrowserConfig,CrawlerRunConfig,CacheMode
B=Path(__file__).resolve().parent;(B/'raw').mkdir(exist_ok=True)
urls=[('陌上花开','https://www.himmr.tech/'),('青藤之恋','https://qingtenglove.com/'),('青藤之恋规则','https://h5.huiyou027.com/lvy-user-agreement'),('恋爱主理人','https://apps.apple.com/cn/app/id6762596550'),('青藤之恋价格','https://apps.apple.com/cn/app/id1472343551'),('牵手价格','https://apps.apple.com/cn/app/id1475216610')]
async def main():
 rows=[]
 async with AsyncWebCrawler(config=BrowserConfig(headless=True,verbose=False)) as c:
  for brand,u in urls:
   try:
    r=await c.arun(url=u,config=CrawlerRunConfig(cache_mode=CacheMode.BYPASS,page_timeout=25000,wait_until='domcontentloaded',delay_before_return_html=1,verbose=False));key=hashlib.sha256(u.encode()).hexdigest()[:12];tx=str(r.markdown or '');(B/'raw'/f'{key}.md').write_text(tx);rows.append({'brand':brand,'url':u,'success':r.success,'status':r.status_code,'chars':len(tx),'file':key+'.md','time':datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(timespec='seconds')});print(brand,r.success,len(tx),flush=True)
   except Exception as e:rows.append({'brand':brand,'url':u,'success':False,'error':str(e)[:250]})
   (B/'crawl4ai_collection.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
asyncio.run(main())
