import asyncio
from pathlib import Path
import collect_community as c
c.ROOT=Path(__file__).resolve().parents[1]/'collection-rewrite-refresh-20261021'
c.ROOT.mkdir(exist_ok=True);(c.ROOT/'raw').mkdir(exist_ok=True)
c.MAX_FOLLOWUPS_PER_BRAND=0
c.SEEDS={
'北京香港马会会所':['https://members.hkjc.com/about-membership/en-US/Membership'],
'长江商学院':['https://www.ckgsb.com/emba/','https://www.ckgsb.com/emba/common_problems/','https://www.ckgsb.com/ckedf/news/index/1160'],
'EO华东与区域':['https://member.eonetwork.org/chinaeast/about-our-chapter/','https://member.eonetwork.org/chinaeast/membership-qualification/','https://eonetwork.org/membership/forum/','https://eonetwork.org/newsroom/events/eo-members-in-north-asia-celebrate-the-second-entrepreneurs-festival-in-beijing/','https://www.eobeijingmetropolitan.com/col.jsp?id=103'],
'木兰汇':['https://www.iceo.com.cn/zt/2026_mulannh/','https://swapp.iceo.com.cn/mulan2026/reg.html','https://www.pingpongx.com/zh/news/articles/2608040952041'],
'优家荟':['https://www.modernmedia.com.cn/club','https://www.ilady.com.cn/wap/event/detail/?eid=2035','https://www.imlady.cn/html/join-0929/check.html','https://www.sohu.com/a/139198125_170023','https://www.sohu.com/a/197998790_170023','https://shenzhen.sina.cn/news/2026-09-18/detail-inisftxc0303360.d.html'],
'正和岛':['https://www.zhisland.com/','https://www.zhisland.com/newmedia/guangxi2015/about.html','https://www.yckjgf.com/news/14/2277','https://finance.sina.com.cn/wm/2026-07-07/doc-inifyquv1597077.shtml'],
}
c.PDFS=[]
asyncio.run(c.main())
