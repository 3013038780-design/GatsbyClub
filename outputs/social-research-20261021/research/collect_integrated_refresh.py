import asyncio
from pathlib import Path
import collect_community as c
c.ROOT=Path(__file__).resolve().parents[1]/'collection-integrated-refresh-20261021'
c.ROOT.mkdir(exist_ok=True);(c.ROOT/'raw').mkdir(exist_ok=True)
c.MAX_FOLLOWUPS_PER_BRAND=0
c.SEEDS={
 '宏观互联网':['https://www.cnnic.net.cn/','https://imgs-b2b.100ec.cn/detail--6658734.html'],
 '高净值生活':['https://www.hurun.net/zh-CN/Info/Detail?num=CSX6BTOMEWY4'],
 '长江商学院':['https://www.ckgsb.com/emba/common_problems/','https://embaminiweb.ckgsb.com/'],
 '中欧':['https://cn.ceibs.edu/node/99'],
 'EO':['https://member.eonetwork.org/chinaeast/about-our-chapter/','https://eonetwork.org/one/governance-financial-reporting/annual-reports'],
 'SEE':['https://conservation.see.org.cn/news/dynamic/2025/1203/12953.html','https://conservation.see.org.cn/Admission/','https://conservation.see.org.cn/Basic/Articles/'],
 '新候选YPO':['https://www.ypo.org/','https://www.ypo.org/membership-requirements/'],
 '木兰汇':['https://www.iceo.com.cn/zt/2026_mulannh/'],
 '旅行许可':['https://www.samr.gov.cn/zw/zfxxgk/fdzdgknr/bgt/art/2023/art_55b4bbc9a30547a9912e7ed61ffa7e20.html'],
}
c.PDFS=[('SEE2024审计','https://conservation.see.org.cn/uploads/soft/250409/1-250409203446.pdf'),('长江2026简章','https://www.ckgsb.edu.cn/uploads/embavideo/2026EMBAmanual.pdf')]
asyncio.run(c.main())
