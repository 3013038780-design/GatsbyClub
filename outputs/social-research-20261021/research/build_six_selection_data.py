import json,statistics
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'six-community-review';OUT.mkdir(exist_ok=True)
now=datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(timespec='seconds')
S=[
 ['K01','北京香港马会会所2025年6月会刊','https://member.hkjc.com/ecard/eHarmony_Jun25.pdf','入会费p158；活动p33—40；价格自2024-01-01起'],
 ['K02','北京香港马会会所子女附属卡申请表','https://www.beijingclubhouse.com/zh-HK/images/membership/Application_Form_for_Children_Supplementary_Card.pdf','p1；8—21岁及120元年费'],
 ['K03','长江商学院EMBA费用与申请','https://www.ckgsb.com/emba/common_problems/','2026级学费及申请费'],
 ['K04','长江商学院EMBA项目','https://www.ckgsb.com/emba/','累计学员与核心决策者结构'],
 ['K05','EO China East分会资料','https://member.eonetwork.org/chinaeast/about-our-chapter/','2026-10-21；人数、年龄、全球收费'],
 ['K06','EO Forum服务设计','https://eonetwork.org/membership/forum/','6—10人、月度聚会、培训与伴侣小组'],
 ['K07','EO 2024至2025年度报告官方发布','https://eonetwork.org/newsroom-old/translations/2024-2025-annual-report-release-zh/','2024-07至2025-06；全球续会91.6%；本轮已读完整发布正文'],
 ['K08','2026商界木兰年会及木兰汇介绍','https://www.iceo.com.cn/zt/2026_mulannh/','近1000成员、112核心、29省市；三日公布议程'],
 ['K09','正和岛App开发者介绍与内购价','https://apps.apple.com/cn/app/%E6%AD%A3%E5%92%8C%E5%B2%9B/id525751375','当前上架页面自述；统计截止日未标；内购价为数字产品'],
 ['K10','正和岛2015广西活动入会说明','https://www.zhisland.com/newmedia/guangxi2015/about.html','2015历史入会制度、权益与3万元年费，不作2026报价'],
 ['K11','阿拉善SEE 2025会员大会履职报告','https://conservation.see.org.cn/news/dynamic/2025/1203/12953.html','2025-10-31数据；2025-12-03发布'],
 ['K12','阿拉善SEE 2024年中理事会公报','https://conservation.see.org.cn/uploads/soft/240723/1-240H3143125.pdf','2024上半年166场、338会员、2412人次；PDFp2'],
 ['K13','阿拉善SEE入会与活动类型','https://conservation.see.org.cn/Admission/','会员交流、企业互访、环保行动、国际考察及会员大会'],
 ['K14','阿拉善SEE会员公约','https://conservation.see.org.cn/Admission/Association/','会员活动、企业绿色实践、组织治理及交流边界'],
 ['K15','EO中国华东分会资格','https://member.eonetwork.org/chinaeast/membership-qualification/','创始人或所有者资格、企业营收及入会流程'],
 ['K16','2026长江港澳台EMBA招生简章','https://ee.ckgsb.com/uploads/202512/16/1765873387437578.pdf','p5—6；两年、每月一个周末四天；港澳台项目安排'],
]
cases=[
 dict(name='北京香港马会会所',priority='首要',learn='高端生活方式与家庭会员体系',reason='与你们同时服务单身、伴侣及已婚人群的设想最接近，可学习权益分层、带客、家庭参与和文化活动。',performance='2025会刊留有茶沙龙、悦读会和周年市集的实际回顾；个人及公司会籍有明确入会价。当前有效会员和续费数据待补。',price='个人入会费60万元；公司甲／乙／丙类180万／130万／70万元。2025年6月会刊所列，标准自2024年起。子女附属卡120元／年。',rights='个人、公司会籍及家属使用规则；餐饮、康体、文化活动与附属卡。另列年费、餐饮及活动支出，按具体权益核价。',customer='个人会员、企业会籍使用人及家属；核心需求是商务接待、日常生活、文化交流和家庭共同参与。',acquisition='官网与会刊展示会籍和活动；现有会员推荐申请人；会籍顾问承接。成功推荐设消费券奖励，茶沙龙与品牌共同举办。',flow='2025年4月8日茶沙龙：茶文化介绍→制茶视频→两种茶品鉴→西点介绍→四款拼配DIY茶包→茶叙交流。主持、品牌和餐饮人员共同交付。',judgment='最值得学的是把会员关系融入日常生活。文化、餐饮和家庭权益让不同关系阶段的人都有参加理由。初创可先借合作场地验证活动与服务，重资产会所建设后置。',transfer='设计个人与伴侣参与规则、带客名额及会员推荐机制；以高质量接待和交流组织建立体验标准。',sources=['K01','K02']),
 dict(name='长江商学院',priority='首要',learn='高端客户筛选与长期同学关系',reason='A8以上企业家客群的重要参照；明确身份、共同学习和固定相处时间，能够形成长期关系。',performance='官网披露EMBA历年累计13000余名学员，99%以上为企业核心决策层。小红书EMBA认证账号3304粉丝；采集24条，23条为近90天内容。',price='2026级EMBA学费99.8万元／人，申请费2000元。收费单位为完整教育项目。',rights='系统课程、教材讲义、课间茶点、图书馆网络等学院资源；班级学习与校友交流连接在读及毕业后的关系。',customer='企业核心决策者及高级管理者，付费动机包含经营管理、全球视野与同行连接。岗位、企业经历和学习需求是可参考的筛选维度。',acquisition='教授观点、校友实战、出海与企业案例→机构号私信咨询／预约评估→申请、考试面试→录取缴费→班级及校友平台。',flow='港澳台2026简章列两年学习、每月一个周末集中四天；课程、小组讨论和实战活动形成重复共处。具体参访行程和毕业后活动权益分别核对。',judgment='关系深度来自共同投入、重复见面和共同任务。99.8万元包含教育与学院品牌价值，拟设社群应按自己的交付与客户收益重新定价。',transfer='建立入会面谈、同组匹配、固定见面日历和共同项目；先明确成员能给彼此带来什么。',sources=['K03','K04','K16']),
 dict(name='EO中国华东分会',priority='首要',learn='固定小组与持续付费的服务机制',reason='六家中最适合拆解小规模初创交付的方法：成员资格、同伴主持、保密、培训和月度见面。',performance='China East页面2026年10月21日列109名会员，平均年龄44岁。EO全球2024／2025财年续会率91.6%，全球会员略超2万；两层范围分开列示。',price='全球年费2630美元，一次性入会费3500美元；首年全球两项合计6130美元。地方分会收费与活动费另核。',rights='全球Forum为6—10人固定小组、每月聚会，新参与者8小时培训；全球服务另设配偶及生活伴侣Forum和学习、探索活动。',customer='一般为未满50岁入会的企业创始人、联合创始人、所有者或控股股东，公司年营收超过100万美元；风投企业另有条件。',acquisition='分会介绍与成员网络→资格核对→联系分会与面谈→接纳→入会及Forum培训。中国华东具体推荐奖励和成交率待补。',flow='资格沟通与接纳→新成员培训→Forum培训→固定小组→受训同伴主持月度交流→以保密规则分享个人及经营经历。此为全球产品设计。',judgment='最有价值的是把主持人训练、交流规则和稳定节奏做成服务。拟设公司需要指定谁负责每组关系维护、缺席跟进和续费服务。',transfer='先建立稳定同伴小组，明确主持、保密、参与和回访规则；企业家与伴侣可设置不同小组并保留共同活动。',sources=['K05','K06','K07','K15']),
 dict(name='木兰汇',priority='重点',learn='高端女性客户的独立价值与活动组合',reason='女性企业家有自己的事业、学习与同行需求，能帮助你们把女性客户设计为独立的付费和参与主体。',performance='2026官方专题披露近1000位成员，覆盖29省市；企业市值或估值20亿元以上的核心成员112位。木兰年会自2009年起，2026为第18届。',price='本轮未取得可核对的现行会籍费或2026年会票价；年会注册入口已查，页面未取得有效报价。',rights='年会、项目路演、木兰之夜、商业对谈、主题论坛和考察构成活动组合；会籍包含次数及年会权益另待核。',customer='女性企业家、公司管理者和商业女性；通过企业、职业与共同议题组织成员，需求集中于同行关系、商业表达、资源和成长。',acquisition='《中国企业家》媒体品牌、女性商业人物与议题传播→年会专题→注册与商务合作入口→活动参加。会员转化结果待补。',flow='2026公布议程：4月17日上午签到、下午路演、18—21点木兰之夜；18日论坛与对谈；19日上午三条安吉考察路线选一。',judgment='路演让成员被看见，晚宴增加熟悉度，论坛提供内容，考察延长共处。这些环节有清楚分工，比把多项活动堆在同一日更值得借鉴。',transfer='建立独立女性主题与成员展示机制；旅行、学习和商业访问围绕女性会员真实议题设计。',sources=['K08']),
 dict(name='正和岛',priority='重点',learn='内容入口与分层商业连接产品',reason='六家中最接近企业家社交平台的组织样本，适合研究内容、数字学习、地方组织与高门槛客户如何承接。',performance='当前App开发者介绍自述：深度服务年营收亿元以上客户企业9000余家，App在线服务企业家等超100万人，新媒体矩阵服务商业人群超1100万。',price='当前App内购列学习卡1598元／年、金卡海邻3998元／年、直播单场198元。核心线下岛邻会籍现价待核；2015官方页3万元／年仅存历史栏。',rights='数字内容与直播构成低门槛产品；2015官方制度列地方组织、活动发起参与、部落创建、学习互助与展示机会。现行线下权益需正式版本补齐。',customer='企业家、创业者和高管；开发者介绍重点服务企业年营收亿元以上客户。数字内容受众与核心线下会员分别研究。',acquisition='商业人物与经营议题内容→App、学习或直播产品→会员申请与服务承接。2015公开入会流程为提交个人企业资料及推荐人→审核→通知→缴费→确认。',flow='历史官方页可复原入会流程，但尚无同等完整的近期单场交付手册。已确认App承载内容与商业连接；近期活动的破冰、分组与回访仍待补。',judgment='值得学的是产品层级与商业网络，暂不把它的小红书获客效果评为领先。同名账号粉丝66299，本轮近90天9条样本的可见评论和分享量较少。',transfer='将大众内容、付费体验与筛选会员分层；分别记录每层客户与转化，避免把所有关注者都放入高端会员池。',sources=['K09','K10']),
 dict(name='阿拉善SEE生态协会',priority='重点',learn='共同事业驱动的会员参与和续费',reason='新增资料中，会员、续费、收入及参与记录最具体；适合学习高端成员为什么愿意长期投入同一组织。',performance='2025年10月31日：有效会员475位，其中终身会员233位，续费率70%，会费收入2280万元，公益参与15310小时。2024上半年另记166场会员活动、338位会员及2412参与人次。',price='当前入会指南说明按时缴纳会费，本轮尚未取得现行完整收费及捐赠标准。报告直接披露2025会费收入2280万元，不据此倒推人均会费。',rights='会员联谊、企业互访、环保行动、海外考察和会员大会；参与组织治理、提出建议并投票，会员公约明确共同目标与交流边界。',customer='愿意投入环保及社会责任的企业领导者。成员选择受到共同价值观、持续参与意愿及企业身份影响。',acquisition='环保项目与企业家参与传播→了解入会→申请→参与项目及会员活动→企业互访与组织治理→会员嘉许及续费。此为公开入口与活动组合，不填报转化率。',flow='2025会员大会回顾：治理团队履职报告→监事会报告→三项表决→会员嘉许及终身会员致敬。日常活动另含自然保护行动及会员企业互访。',judgment='持续关系需要成员能贡献、能参与、能获得认可。公益组织的会费和治理机制有自身制度背景；拟设公司可学习参与设计和服务指标。',transfer='让会员共同策划活动、分享经验、发起主题和承担志愿角色；月度记录到场、重复参与、推荐和续费。',sources=['K11','K12','K13','K14'])]
root=ROOT/'social-platforms';attr={}
for l in (root/'content-attribution.jsonl').read_text().splitlines():
 r=json.loads(l);attr[r.get('note_id')]=r
notes=json.loads((root/'统一内容指标.json').read_text());accounts={}
for l in (root/'brand-account-candidates.jsonl').read_text().splitlines():
 r=json.loads(l);accounts[r['profile_url']]=r
social=[]
for name,uid in [('长江商学院','662761820000000007005cc2'),('正和岛','61cd9c79000000001000ddc6')]:
 url='https://www.xiaohongshu.com/user/profile/'+uid;a=accounts[url]
 rs=[r for r in notes if attr.get(r['内容ID'],{}).get('profile_url')==url and r.get('发布时间','')[:10]>='2026-07-23']
 metric={}
 for f in ['点赞','评论','分享']:
  vals=[r[f] for r in rs if r.get(f) is not None];metric[f]={'可见条数':len(vals),'合计':sum(vals),'中位数':statistics.median(vals) if vals else None}
 social.append(dict(name=name,account=a['account_name'],fans=int(next(i['count'] for i in a['interactions'] if i['type']=='fans')),captured=a['collected_at'],window='2026-07-23至2026-10-21',sample=len(rs),metrics=metric,profile=url,verified=name=='长江商学院',notes=rs))
rejected=[['京城俱乐部','保留综合会所背景参考','现有资料以历史与服务介绍为主，当前成员和持续活动证据不及此次入选者'],['观澜湖','保留兴趣活动专项','第23届连续赛事和10场套餐值得学；六个深度名额优先覆盖更广的关系与组织机制'],['中欧国际工商学院','保留内容与招生专项','有29849粉丝认证号和约20席主题小聚，获客可学；与已指定长江的学习校友模式重叠'],['创合汇','保留产品组合专项','30+社群和10万+成员有参考价值，公开客群范围较广；高端生活与伴侣服务仍弱'],['Kupu-kupu','保留女性活动观察','10292粉丝，有女性空间和书影活动；本轮尚无高净值准入和持续付费规模证据'],['SHE ACE CLUB及The Queen’s Circle','保留新品牌线索','前者329粉丝；后者2063粉丝且为主理人运营号，暂不进入有体量品牌的六家深研名单']]
payload=dict(generated_at=now,selection_basis='机构主体与持续关系、与目标人群的联系、可学习的差异化能力、规模及实际经营证据',cases=cases,social=social,sources=S,rejected=rejected)
(OUT/'六家筛选依据及对标数据.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2))
print(OUT)
