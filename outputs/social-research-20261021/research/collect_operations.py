import asyncio
from pathlib import Path
import collect_community as c
c.ROOT=Path(__file__).resolve().parents[1]/'collection-operations-20261021'
c.ROOT.mkdir(exist_ok=True);(c.ROOT/'raw').mkdir(exist_ok=True)
c.MAX_FOLLOWUPS_PER_BRAND=0
c.SEEDS={'EO全球':['https://eonetwork.org/membership/forum/'],'深商联':['https://www.shenshang.org/understand/entrepreneur/club'],'长江商学院':['https://www.ckgsb.com/emba/article/detail.html?articleid=25324']}
c.PDFS=[]
asyncio.run(c.main())
