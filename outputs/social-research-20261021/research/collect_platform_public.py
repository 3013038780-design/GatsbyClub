import asyncio
from pathlib import Path
import collect_community as c
c.ROOT=Path(__file__).resolve().parents[1]/'collection-platform-public-20261021'
c.ROOT.mkdir(exist_ok=True);(c.ROOT/'raw').mkdir(exist_ok=True)
c.MAX_FOLLOWUPS_PER_BRAND=0
c.SEEDS={'中欧国际工商学院':['https://jingxuan.douyin.com/m/video/7681618473243462963','https://jingxuan.douyin.com/m/video/7632217189461921030','https://search.bilibili.com/all?keyword=%E4%B8%AD%E6%AC%A7%E5%9B%BD%E9%99%85%E5%B7%A5%E5%95%86%E5%AD%A6%E9%99%A2']}
c.PDFS=[]
asyncio.run(c.main())
