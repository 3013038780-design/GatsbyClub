import asyncio
from pathlib import Path
import collect_community as c
c.ROOT=Path(__file__).resolve().parents[1]/'collection-six-refresh-20261021'
c.ROOT.mkdir(exist_ok=True);(c.ROOT/'raw').mkdir(exist_ok=True)
c.MAX_FOLLOWUPS_PER_BRAND=0
c.SEEDS={
 '正和岛':['https://apps.apple.com/cn/app/%E6%AD%A3%E5%92%8C%E5%B2%9B/id525751375','https://www.zhisland.com/newmedia/guangxi2015/about.html'],
 '阿拉善SEE生态协会':['https://conservation.see.org.cn/Admission/Initiation/','https://conservation.see.org.cn/Admission/Association/','https://conservation.see.org.cn/news/dynamic/2025/1203/12953.html'],
 'EO华东':['https://member.eonetwork.org/chinaeast/about-our-chapter/','https://eonetwork.org/membership/forum/'],
 '木兰汇':['https://www.iceo.com.cn/zt/2026_mulannh/']}
c.PDFS=[('阿拉善SEE生态协会','https://conservation.see.org.cn/uploads/soft/240723/1-240H3143125.pdf')]
asyncio.run(c.main())
