import asyncio
from pathlib import Path
import collect_community as c
c.ROOT=Path(__file__).resolve().parents[1]/'collection-followup-20261021'
c.ROOT.mkdir(exist_ok=True);(c.ROOT/'raw').mkdir(exist_ok=True)
c.MAX_FOLLOWUPS_PER_BRAND=0
c.SEEDS={
 '中欧国际工商学院':['https://cn.ceibs.edu/gemba/tuition-fees','https://cn.ceibs.edu/hemba/faq','https://cn.ceibs.edu.cn/execed/amp'],
 '领教工坊':['https://www.clec.com.cn/jiaruwomen.html','https://www.clec.com.cn/p/sirendongshihui.html','https://www.clec.com.cn/fuwuyujiazhi.html'],
 '观澜湖':['https://mp.weixin.qq.com/s/qbAZ3sUnmT7lAAS0BQtwPg','https://mp.weixin.qq.com/s/MVEK0BX4SrxyUzyCQ52z3g','https://mp.weixin.qq.com/s/P7XfqLyzvEELXZqBmMfGOg'],
 'EO中国':['https://eonetwork.org/newsroom-old/translations/2024-2025-annual-report-release-zh/'],
 '北京香港马会会所':['https://www.beijingclubhouse.com/zh-CN/membership-applyingformembership/index'],
}
c.PDFS=[('北京香港马会会所','https://www.beijingclubhouse.com/zh-HK/images/membership/Application_Form_for_Children_Supplementary_Card.pdf'),('长江商学院','https://ee.ckgsb.com/uploads/202512/16/1765873387437578.pdf')]
asyncio.run(c.main())
