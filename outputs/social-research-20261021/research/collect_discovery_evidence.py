import asyncio
from pathlib import Path
import collect_community as c
c.ROOT=Path(__file__).resolve().parents[1]/'collection-discovery-evidence-20261021'
c.ROOT.mkdir(exist_ok=True);(c.ROOT/'raw').mkdir(exist_ok=True)
c.MAX_FOLLOWUPS_PER_BRAND=0
c.SEEDS={
 '阿拉善SEE生态协会':['https://conservation.see.org.cn/news/dynamic/2025/1203/12953.html','https://conservation.see.org.cn/Admission/'],
 '创合汇':['https://www.chuanghehui.com/view/zlyzx'],
 '德申汇':['https://www.detion.com/about','https://detion.com/news/3481','https://detion.com/news/3527'],
 '上海新沪商联合会':['https://mzj.sh.gov.cn/MZ_shetuan748_0-2-3-357-732/20200520/MZ_shetuan748_141531.html']}
c.PDFS=[]
asyncio.run(c.main())
