import asyncio,json
from pathlib import Path
import collect_community as c
B=Path(__file__).resolve().parents[1]
c.ROOT=B/'collection-thirty-refresh-20261021';c.ROOT.mkdir(exist_ok=True);(c.ROOT/'raw').mkdir(exist_ok=True)
c.MAX_FOLLOWUPS_PER_BRAND=0
c.SEEDS={
'京城俱乐部':['https://thecapitalclub.com/zh-hans/julebulishi/','https://thecapitalclub.com/membership/','https://thecapitalclub.com/clubactiveties/'],
'HIGHER CLUB':['https://www.higherclub.cn/'],
'黑骑士球员俱乐部':['https://www.tpc.com.cn/membership','https://www.tpc.com.cn/abouttheplayersclub'],
'观澜湖':['https://www.missionhillschina.com/golfathon/'],
'南沙游艇会':['https://www.nanshamarina.com/','https://www.nanshamarina.com/membership/128.html','https://www.nanshamarina.com/membership/132.html','https://www.nanshamarina.com/news/show-302.html'],
'上海罗斯福会所':['https://cn.rooseveltclub.cn/','https://www.rbsc.org/member-benefits/roosevelt-club-shanghai/'],
'伟事达中国':['https://www.oldchair.cn/wsdhy_jiage'],
'领教工坊':['https://www.clec.com.cn/p/sirendongshihui.html','https://www.clec.com.cn/jiaruwomen.html'],
'YPO':['https://www.ypo.org/membership-requirements/','https://www.ypo.org/membership-benefits/'],
'中国企业家俱乐部':['https://www.daonong.com/about'],
'创合汇':['https://www.chuanghehui.com/view/club','https://www.chuanghehui.com/view/zlyzx'],
'亚布力中国企业家论坛':['https://www.cefco.cn/about/index.html'],
'德申汇':['https://www.detion.com/about','https://detion.com/news/3527'],
'中欧国际工商学院':['https://cn.ceibs.edu/gemba/tuition-fees','https://cn.ceibs.edu/hemba/faq'],
'北大汇丰EDP':['https://edp.phbs.pku.edu.cn/','https://edp.phbs.pku.edu.cn/info/1271/13221.htm'],
'清华五道口':['https://emba.pbcsf.tsinghua.edu.cn/index.htm'],
'交大高金':['https://emba.saif.sjtu.edu.cn/emba_mobile/content/show/236-887.html'],
'上海财经大学商学院':['https://cob.sufe.edu.cn/websites/MBA/Admissions/EMBA-Financial-2026/index.html'],
'深商联':['https://www.shenshang.org/sgcc/about-sgcc','https://www.shenshang.org/understand/entrepreneur/club'],
'深圳市侨商国际联合会':['https://www.socia.org/Member/user/Chamber.html'],
'上海美国商会':['https://www.amcham-shanghai.org/en/membership'],
'中国美国商会':['https://www.amchamchina.org/membership/'],
'上海新沪商联合会':['https://mzj.sh.gov.cn/MZ_shetuan748_0-2-3-357-732/20200520/MZ_shetuan748_141531.html'],
'阿拉善SEE生态协会':['https://conservation.see.org.cn/Admission/','https://conservation.see.org.cn/news/dynamic/2025/1203/12953.html'],
}
c.PDFS=[]
asyncio.run(c.main())
