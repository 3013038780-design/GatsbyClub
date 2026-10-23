import asyncio,json,hashlib,re
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from crawl4ai import AsyncWebCrawler,BrowserConfig,CrawlerRunConfig,CacheMode
B=Path(__file__).resolve().parent
URLS=[('HIMMR会员商品','https://apps.apple.com/cn/app/id6449488341'),('青藤会员权益','https://h5.huiyou027.com/doc-viewer/?dockey=VIP_AGREEMENT'),('青藤自动续费','https://h5.huiyou027.com/lvy-vip-subscription-agreement'),('牵手权益协议','https://h5.qianshouapp.cn/value-added-service.html'),('HIMMR服务入口','https://mp.howimetmrright.com/'),('大超第三方观察','https://dy3.feigua.cn/bloggeropen/B54A9E5AAAED4A7B'),('青藤七夕互动','https://sz.ifeng.com/c/8vYMuTPbesM'),('牵手8月产品说明','https://news.bjd.com.cn/2026/08/20/11923870.shtml'),('单身需求调查','https://www.iimedia.cn/c400/111840.html')]
async def main():
 rows=[]
 async with AsyncWebCrawler(config=BrowserConfig(headless=True,verbose=False)) as c:
  for name,u in URLS:
   try:
    r=await c.arun(url=u,config=CrawlerRunConfig(cache_mode=CacheMode.BYPASS,page_timeout=20000,wait_until='domcontentloaded',delay_before_return_html=1,verbose=False));key=hashlib.sha256(u.encode()).hexdigest()[:12];tx=str(r.markdown or '');(B/'raw'/f'{key}.md').write_text(tx);(B/'raw'/f'{key}.html').write_text(r.html or '');rows.append(dict(name=name,url=u,success=r.success,chars=len(tx),file=key+'.md',collected=datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(timespec='seconds')));print(name,r.success,len(tx),flush=True)
   except Exception as e:rows.append(dict(name=name,url=u,success=False,error=str(e)[:120]));print(name,'ERROR',flush=True)
   (B/'采集记录.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
asyncio.run(main())
