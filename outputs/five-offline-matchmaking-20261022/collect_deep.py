import asyncio, json, hashlib
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
B=Path(__file__).parent
SEEDS=[
 ('钻石婚恋','https://www.zuanshi.com/new/loveCustomization'),
 ('钻石婚恋','https://www.zuanshi.com/webActivity/newActivityList'),
 *[('钻石婚恋','https://www.zuanshi.com/webActivity/newActivityDetail?id='+i) for i in ['8f6c2d32f22b42aaa234cf665d3e4f02','b4a2dc587c604ac59cfa6ccfc05193ab','eb19e98e3e5642f3a51907c180b4930c','056bdd2152d24fa1b9dd983ea9e4a473']],
 ('HIMMR','https://www.himmr.tech/'),
 ('我主良缘','https://www.liangyuan.com/'),
 ('我主良缘','https://www.7799520.com/party'),
 ('金凤凰','https://www.jfh999.com/about/20.html'),
 ('金凤凰','https://www.jfh999.com/about/24.html'),
 ('金凤凰','https://www.jfh999.com/about/8.html'),
 ('金凤凰','https://www.jfh999.com/party/311.html'),
]
async def main():
 rows=[]
 async with AsyncWebCrawler(config=BrowserConfig(headless=True,verbose=False)) as crawler:
  for brand,url in SEEDS:
   key=hashlib.sha256(url.encode()).hexdigest()[:12]
   row=dict(brand=brand,url=url,collected_at=datetime.now(ZoneInfo('Asia/Shanghai')).isoformat())
   try:
    r=await crawler.arun(url=url,config=CrawlerRunConfig(cache_mode=CacheMode.BYPASS,page_timeout=20000,wait_until='domcontentloaded',delay_before_return_html=2,verbose=False))
    body=str(r.markdown or '')
    (B/'raw'/f'{key}.md').write_text(body)
    (B/'raw'/f'{key}.html').write_text(r.html or '')
    row.update(success=bool(r.success and len(body)>150),status=r.status_code,chars=len(body),file=f'{key}.md',links=r.links,media=r.media)
   except Exception as e:row.update(success=False,error=type(e).__name__)
   rows.append(row)
   (B/'网页采集记录.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
   print(brand,row.get('success'),row.get('chars'),url,flush=True)
asyncio.run(main())
