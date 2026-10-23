from pathlib import Path
import json,re,csv,shutil,requests
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
B=Path(__file__).resolve().parents[1]
d=json.loads((B/'research/交付工作簿数据.json').read_text()); sheets={s['name']:s for s in d['sheets']}
c=json.loads((B/'community-supplement/curated-data.json').read_text()); ct={s['name']:s for s in c['tables']}
fresh=json.loads((B/'collection-thirty-refresh-20261021/collection.json').read_text())
R=[]
def add(name,kind,city,who,rights,acq,event,performance,judgment,url):
 R.append(dict(name=name,kind=kind,city=city,who=who,rights=rights,acq=acq,event=event,performance=performance,judgment=judgment,url=url))
add('京城俱乐部','综合会员会所','北京','在北京有商务接待、跨国交流和家庭休闲需求的商务人士；官网同时服务会员家人。','餐饮、健身、商务文化交流及家人活动；家庭参加名额和具体会籍包另查条款。','官网会籍咨询；官网记载与使馆、商会合作，用论坛及文化活动让潜在会员接触俱乐部。','官网列商务论坛、文化及家庭活动；本轮未取得可逐时复原的单场完整回顾。','官方历史记载1994年10月14日开业；当前网站保留会籍及活动栏目，付费会员和续会结果未公开。','适合研究一个固定场所如何同时容纳商务接待和家庭生活，价格结构尚不足以直接照搬。','https://thecapitalclub.com/zh-hans/julebulishi/')
add('HIGHER CLUB','精选年轻会员社群','杭州、上海及跨城','官网称成员以16—25岁企业家二代为主，有海外学习背景；这是机构描述，非独立客户调查。','闭门晚宴、创始人对谈、品牌共创、艺术与私人博物馆体验；成员申请和品牌入驻分两条业务线。','官网展示创始团队、家族企业背景及场景；申请入口引导微信联系并备注申请；品牌合作另走尽调与付费入驻。','官网描述由创始团队组织闭门晚宴和小范围对谈；没有取得带日期、人数及环节时间的实际执行记录。','官网称2023年成立、可触达150+高净值资源；未披露付费会员口径、年度收入与续费。','客群比我们的全关系阶段定位更年轻，可研究二代与品牌场景，但不应据官网家族企业市值判断会员消费或转化。','https://www.higherclub.cn/')
add('黑骑士球员俱乐部','高尔夫与生活会员','深圳','按打球、居住及纯社交需求分层的球会申请者；官网未公开实际客户年龄及财富分布。','钻石、黑钻石、居住、社交四类会籍；不同使用目的单独命名，具体次数与带客权限需完整合同。','官网会籍介绍和会服团队咨询，根据使用需求推荐等级。','官网可确认球场和会籍服务；本轮未取得一场会员活动的完整招募—现场—回访记录。','官网介绍27洞球场及四类会籍；设施数量和产品类别可确认，会员数及出场活跃未披露。','值得学的是把只想社交的人与重度运动使用者分开，避免一份会员费承诺所有服务。','https://www.tpc.com.cn/membership')
add('观澜湖','运动与生活方式会员','深圳、东莞','已有球会会员及12岁以上业余球手；赛事按年龄、性别和差点分组，另有家庭兴趣活动。','会籍之外卖10场赛事套餐；会员等级影响价格；搭配住宿、生日礼遇、其他运动及生活方式活动。','官网会员生活栏目与公众号活动详情→预约或赛事报名；嘉宾10人同报赠1个名额。','2026高球马拉松：报名选套餐→预订→凭卡或证件登记→8月31日前完成9场选拔赛→晋级→9月23日决赛及颁奖晚宴。','2026为第23届，官方有当届落幕记录；本届去重人数、会员复购及利润未披露。','在大群体里用连续赛事形成反复见面，比只办一次聚会更值得学习。','https://www.missionhillschina.com/golfathon/')
add('南沙游艇会','航海与家庭会员','广州南沙','有帆船、游艇租赁或泊位需求的人，以及希望一家人使用泳池健身和参加主题活动的客户；个人与公司分别申请。','一年及三年短期会籍配1主卡1附属卡；长期普通会籍与海事会籍分开，后者多泊位申请权；租船、餐饮和课程按各自优惠消费。','官网完整价目与会员申请表→提交基本信息及推荐人→会籍联系；未填写表单。','官网已有2026第二、三季度会员活动回顾；第三季度9月24日回顾以图片为主，完整顺序、人数和回访尚未提取。','2011年成立，官网列352个湿泊位、120个干仓位；2026连续季度活动可见，实际付费会员及续费未披露。','特别适合学短期体验会籍、家属卡及按使用需求区分等级；并不需要自有游艇才能设计社群权益。','https://www.nanshamarina.com/membership/128.html')
add('上海罗斯福会所','葡萄酒雪茄与私人会所','上海','有私人宴请、葡萄酒与雪茄兴趣的商务及生活方式客户；另接待互惠球会持卡会员。','会所、雪茄廊、图书室、屋顶及酒窖私人访问；互惠协议列预约品鉴、私人聚会及特定服务费减免。','官网展示场地与餐饮；皇家曼谷体育会2026互惠协议带来持卡会员，按提前预约提供体验。','互惠会员先预约→提交聚会主题、人数与菜单偏好→会所确认；这是公布的接待安排，单场实际分钟级流程未披露。','皇家曼谷体育会公布2026年4月1日至12月31日互惠安排；本地付费会员及活动频次未披露。','研究重点是兴趣设施、私人接待和异地俱乐部互惠，不能把普通餐厅到店客流当社群会员。','https://www.rbsc.org/member-benefits/roosevelt-club-shanghai/')
add('伟事达中国','教练与私人董事会','全国／本地小组','CE面向最高决策者，服务业年收入3000万元、25人起或商贸制造1亿元、50人起；SE面向更早期经营者；KE面向关键高管。','CE每年5—6次两天小组、10—12小时一对一和5—6次专家分享；SE每年9天小组、9小时教练及4次专家；分层订阅。','官网按企业规模及岗位展示套餐和价格→咨询→匹配产品与主席；渠道成交数据未披露。','产品标准：12—16位非竞争同行组成小组，由教练主持；CE两天讨论和专家输入，另有一对一；具体单场议程未取得。','中国页面自述全球40国、45000+成员；中国本地有效会员和续费结果未披露。','可学按经营阶段定价、固定小组与一对一组合；需要有能力持续追问企业问题的教练。','https://www.oldchair.cn/wsdhy_jiage')
add('领教工坊','私人董事会','中国主要城市','希望讨论经营、领导力与个人家庭问题的民营企业掌舵人；同组避免直接竞争。','固定小组与领教、召集人长期服务；运营岗位说明按15—20人、全年6次、每次两天安排。','官网产品与案例→扫码咨询→提交材料→电话访谈→面试→录取；入会流程位于官网加入页的私董会报名部分。','标准交付：企业访谈→收集问题→定制议程→两天讨论→形成行动计划→召集人跟进→安排下一次；非某场实到记录。','官网可确认小组人数和年度交付安排；公开岗位的留存职责不作为已实现续费率。','最值得学召集人的会前调研和会后跟进，这决定私董会能否超越一次听课。','https://www.clec.com.cn/p/sirendongshihui.html')
add('YPO','全球企业领导者会员组织','全球及中国分会','一般准入要求45岁前加入、最高经营负责人并承担损益与人事决策；企业销售收入等规模门槛另列，不按个人资产入会。','同伴网络、学习与全球分会活动；全球入会和年费分开，地方分会另收费。','官网会员资格→个人信息→公司信息→审查与费用确认→分会接洽；各地实际面谈安排依分会。','有固定同伴交流及学习产品；本轮未取得中国具体分会一场活动的可复原完整回顾。','官网自述全球38000+成员；全球数字和收费不能代表中国分会人数与全部年度成本。','与EO一起比较高要求会员筛选和全球地方两层收费，国内实际交付还需分会材料。','https://www.ypo.org/become-a-member/')
add('中国企业家俱乐部','企业家理事与企业网络','全国','主要企业创始人及核心决策者；理事层与绿色公司联盟应分开看。','理事交流、绿色经营与企业互访；会员类别、治理角色及活动权限需分层核对。','官网理事、企业案例、访问活动形成信任；本轮未取得普通公开申请到付费的完整规则。','以企业访问与经营对话为主要学习对象；未取得一场带完整时间表的近期接待执行记录。','官网当前称近70位理事；2025机构报告的联盟和访问数据另有统计期，不并成当前付费人数。','适合学头部企业之间的互访和议题设计，进入门槛依赖组织者已有企业资源。','https://www.daonong.com/about')
add('创合汇','学习与多主题社群','全国','创投俱乐部面向年营收500万元以上的创始人、联合创始人、合伙人和CEO；战略工作坊以企业高管团队为单位。','投资学堂、路演、论坛、私董会、闭门会、参访六模块；俱乐部列全年4场好项目路演优先参与。','课程顾问保荐或校友推荐→企业资料→资质审核→缴费→开营；官网顾问和申请入口承接。','战略解码工作坊3天2夜、最多10家企业，每个细分行业限一家；公开申请链条明确，课内逐时流程未披露。','官网自述30+社群、100000+成员，未标统计截止与付费去重；历史活动报名数不作2026实到。','与我们的多产品设想接近；值得学以共同企业问题串联产品，不能把产品目录本身当成交叉销售效果。','https://www.chuanghehui.com/view/club')
add('亚布力中国企业家论坛','企业家论坛及会员网络','全国','企业创始人、董事长及经营负责人；官网理事名录和历届论坛嘉宾可核对其商业角色。','会员、企业会员、菁英会员与年度合作等分列；论坛、交流及合作权益按类别配置。','官网理事与论坛内容→合作／会员栏目→联系组织方；合作赞助与个人会员两条业务分开。','2026夏季年会官网有开闭幕和创新、AI、健康、消费、全球化等论坛板块；尚未取得单场活动实到和会后联系流程。','2026夏季年会为第26届；当届议程证明持续组织会议，年费会员数及续费未披露。','可学用企业家内容与固定年度节点维系品牌；不能把论坛参会规模直接当日常社群活跃。','https://www.cefco.cn/phone/cooperation/index.html')
add('德申汇','分区商务俱乐部','全国及跨境','有真实企业身份、希望拓展经营联系的经营者；平台要求真实填写企业认证，不以A8为公开统一门槛。','线上企业展示、企业认证与线下授证俱乐部组合，按地区形成持续活动。','官网及企业展示→注册与企业认证→俱乐部接洽；地方会员发展和保留另由组织运营。','官网有友约等地方活动回顾；年度线上会议汇报会员发展和留存。单场完整招募、签到、交流、回访顺序未全部取得。','2024—2025年度会议披露7月1日留存用户9922；80%是年度保留目标，未作为完成值。','可学地方组织与平台身份的连接；实际客户层次更宽，不能直接作为高净值社群的客单价参照。','https://detion.com/news/3527')
add('中欧国际工商学院','商学院学习与校友组织','上海、北京、深圳及海外','HEMBA披露过半学员为创业者或来自家族企业，前三行业智能制造、信息科技、医疗健康；MBA与EMBA客群分别看。','GEMBA、HEMBA、EMBA等独立项目，学费按完整课程收取；课程期间建立班级关系，校友活动另按各次规则。','官网咨询申请；小红书认证号用行业、海归、科技小聚引导留言私信，课程部邮件确认；招生评审后收费。','2026年10—11月MBA小聚预告：13:30—16:00、约20席→报名→邮件确认→校友在读生分享→交流；预告尚非实际实到。','认证小红书账号粉丝29849；已采24条内容。课程分层及学费明确，社交内容转学费的成交数据未公开。','可学用行业小聚让准客户体验人群质量，再进入正式申请；我们不能照搬学历与校友资格背书。','https://cn.ceibs.edu/gemba/tuition-fees')
add('北大汇丰EDP','高管教育与校友兴趣组织','深圳及异地活动','参加具体EDP课程的企业经营者和高管及其校友；跑团活动另开放6—16岁亲子组。','课程与征戈会等兴趣组织相接；班级是组队单元，校友可承担组织岗位。不同课程收费分别查。','学院官网课程内容→招生咨询；班级与校友社群动员参加赛事，不能把校友赛事报名当新课程成交。','2026年3月7日班际驿传：25人筹委会→16队组队→每队6人至少1女性→2.3公里环道3小时接力→完赛总结。','2026单场16队、筹委会25人；征11回顾近60队员、四天三夜122公里。均为各场规模。','值得学让会员成为组织者，班级关系通过运动和亲子持续；比新增一个旅行套餐更能解释社群延续。','https://edp.phbs.pku.edu.cn/info/1271/13221.htm')
add('清华五道口','金融高管教育与校友组织','北京及异地模块','金融机构高管、企业经营者；金融EMBA及一带一路等课程各有对象，不能混用学员比例。','金融学习、企业案例、校友企业访问与海外模块；按具体课程录取和收费，非一张普通社交年卡。','官网项目简章、课程与校友企业内容→招生咨询→申请选拔→录取；各项目条件分列。','当前官网有2026课堂与校友企业参访记录；尚未取得单次参访的完整时间表和接待层级。','现有课程与参访持续发布；有效校友会员、活动参与分母及续费不适用普通年卡口径。','可学按产业与经营问题设计参访，品牌与教授资源属于进入条件，不能只复制行程。','https://emba.pbcsf.tsinghua.edu.cn/index.htm')
add('交大高金','金融EMBA与校友组织','上海','有资历的企业高管及经营者，购买金融与综合管理教育；个人财富和婚姻状态非本次可确认画像。','金融EMBA课程和学院资源；项目学费按一整个教育项目收取，差旅及其他项目按招生条款。','官网项目特色、课程与学员内容→招生咨询→报考与评审→录取缴费。','以课程模块与同学交流为核心；本轮未取得有完整招募、分组、接待和回访的单场校友活动。','2026金融EMBA官方学费82.8万元；当前校友去重活动人数及单独社群收入未取得。','与长江中欧比较课程准入和客户支付预算，不能把学费全部解释为购买社交关系。','https://emba.saif.sjtu.edu.cn/emba_mobile/content/show/236-887.html')
add('上海财经大学商学院','金融EMBA与校友组织','上海','2026金融EMBA面向企业经营者及金融或企业中高层；学历与工作年限按当届招生规则。','金融EMBA课程、讲义及学院教育资源按简章配置；项目收费不是校友社群年费。','官网招生简章及商界精英计划→申请→20分钟个人评估和60分钟小组商业认知环节→后续录取。','已公开招生评估方式；实际班级活动及企业参访完整执行流程未取得。','2026金融EMBA官网明确学费48.8万元；当届实际招收结构和校友活动活跃未披露。','有助比较不同商学院价格与选拔，不代表我们的社会化会员能使用相同招生与学历产品。','https://cob.sufe.edu.cn/websites/MBA/Admissions/EMBA-Financial-2026/index.html')
add('深商联','地方企业与细分社群','深圳','深圳企业经营者；木棉会专门组织女性文化健康活动，菁英会面向年轻深商。','商界服务之下分女性、年轻经营者等小组织，活动包括主题沙龙、生日晚宴、文化之旅及资源交流。','官网企业故事及活动→组织和会员服务接洽；细分组织继续动员，实际渠道成交未披露。','菁英会介绍称每年10余项中小活动，未标统计年；木棉会列艺术沙龙文化之旅。单场完整回顾未取得。','官网称服务3000多家企业、40余工作人员；服务对象规模不等于当前缴费人数。','可学在大社群内按生活阶段与兴趣拆小组，商业和生活需求才有具体承接者。','https://www.shenshang.org/sgcc/about-sgcc')
add('深圳市侨商国际联合会','侨商身份与商业组织','深圳','在深圳注册投资的侨商、港澳及相关企业和个人，申请依身份与经营联系审核。','普通会员和理事等组织职务分层会费；组织服务及专项活动，具体免费名额未披露。','官网身份说明和会费→下载申请表→提交材料→会员部门审核；单位和个人申请分开。','可确认入会申请手续，单次活动的签到、议程和回访没有完整公开记录。','官网公开普通会员每年3000元至常务副会长5万元等档次；有效会员、续费和活跃未披露。','适合研究身份筛选与组织职务收费；职务会费与服务套餐等级的含义不同。','https://www.socia.org/Member/user/Chamber.html')
add('上海美国商会','国际商务会员组织','上海及长三角','在中美有合法商业联系的公司；个人会员面向21岁以上在华外籍居民并需全职工作证明。','公司卡按规模配置主卡与附卡；个人12个月会籍；活动、研究、委员会和商务政策服务结合，部分活动另收费。','官网公开会员档次→申请；委员会和行业会议展示资源；在册公司员工按卡参与活动。','公开青少年项目2026年7月9—10日两天，有会员子女与非会员差价及取消期限；这是单独付费活动，不等于成人会费。','官网自述3000+会员、1500家公司；统计截止未标。企业卡、个人及活动票应分别统计。','可学一份公司关系服务多位使用人，委员会形成持续议题；更适合商务维度。','https://www.amcham-shanghai.org/membership/resident')
add('中国美国商会','国际商务会员组织','北京及中国多城市','有中美商业联系的企业与在华经营负责人；公司、活动嘉宾及赞助伙伴需要分别识别。','会员商务交流、政策及行业活动；具体等级与使用人以申请条款；单次会议可额外收费。','官网和行业活动→会员咨询／活动报名；已取得2026四川活动的公开分档票价。','2026年6月25—26日四川活动按会员／非会员及含住宿与否分别报名；完整现场分时和回访资料未取得。','有2026实际活动产品与会员差价；全国有效会员、续费及每场实际人数本轮未取得。','与上海美商会比较单位会员和活动票，避免把赞助金额写成年费。','https://www.amchamchina.org/membership/')
add('上海新沪商联合会','企业家商会／历史收费参照','上海','以上海企业会员单位为基础，按普通会员、理事、副会长等组织职务分档。','单位会员关系及组织职务权利；本轮仅有历史政府会费公示，现行服务包和活动权益未取齐。','历史政府登记和会费公示可核对组织及收费；当前从发现到成交的运营路径未取得。','本轮未取得近期完整实际活动流程；不以通用商会流程补写。','2019年政府公示普通单位5000元／年、理事1万元等；2026现价及近期活跃未核实。','保留为历史职务会费参照，不进入当前品牌声量或经营表现排名。','https://mzj.sh.gov.cn/MZ_shetuan748_0-2-3-357-732/20200520/MZ_shetuan748_141531.html')
add('阿拉善SEE生态协会','企业家公益会员组织','全国地方项目','愿意持续捐赠并亲身参与环保的企业家；共同任务是环保，社交与企业互访发生在共同参与中。','会员有治理表决、选举等权利，参加联谊、企业互访、地方环保、海外考察及会员大会；公益捐赠与商业服务分开。','官网使命与会员名录→申请咨询；会员发展由会员推动，2025大会嘉许29位年度发展至少1人的会员。','2025会员大会：治理与监事报告→合法性宣布→三项讨论表决→会员嘉许与终身会员致敬；另有前夜培训和13个地方项目讨论。','截至2025年11月30日有效480人；大会现场111、现场委托85、线上92、线上委托30，共318，含委托出席率66.25%；10月末口径另存。','可学会员共同治理、推荐与参与贡献的可见回报；公益使命不能直接包装成付费社交承诺。','https://conservation.see.org.cn/news/dynamic/2025/1203/12953.html')
assert len(R)==24
orig6=[r[0] for r in sheets['六家对照']['rows']]; names=orig6+[r['name'] for r in R];assert len(set(names))==30
sources=sheets['来源台账']['rows']; urlids={r[2]:r[0] for r in sources}
def source(url,title,scope='2026-10-21公开页面',kind='机构原始资料'):
 if url in urlids:return urlids[url]
 sid='T%03d'%(1+sum(str(x[0]).startswith('T') for x in sources));sources.append([sid,title,url,title.split('｜')[0],scope,kind,title,'依页面标明时间及统计范围使用','2026-10-21']);urlids[url]=sid;return sid
for r in R:r['sid']=source(r['url'],r['name']+'｜产品、客户及组织资料')
for p in fresh['pages']:source(p['网址'],p['机构']+'｜本轮网页复核')
extra=[('YPO','https://www.ypo.org/become-a-member/'),('上海美国商会','https://www.amcham-shanghai.org/membership/resident'),('上海美国商会','https://amcham-shanghai.glueup.cn/org/amcham/memberships/'),('YPO','https://www.ypo.org/membership-requirements/')]
raw=B/'collection-thirty-refresh-20261021/raw'
def fetch(item):
 name,url=item
 try:
  q=requests.get(url,timeout=25);soup=BeautifulSoup(q.text,'html.parser')
  for x in soup(['script','style']):x.decompose()
  txt=soup.get_text('\n',strip=True);f='supplement-'+str(extra.index(item)+1)+'.txt';(raw/f).write_text(txt)
  return {'机构':name,'网址':url,'状态':'已采集' if q.status_code<400 and len(txt)>300 else '正文不足','HTTP状态':q.status_code,'正文字数':len(txt),'采集时间':'2026-10-21','原文文件':'raw/'+f,'错误':''}
 except Exception as e:return {'机构':name,'网址':url,'状态':'失败','HTTP状态':None,'正文字数':0,'采集时间':'2026-10-21','原文文件':'','错误':str(e)[:100]}
fresh['pages']+=list(ThreadPoolExecutor(4).map(fetch,extra))
for name,url in extra:source(url,name+'｜本轮费用与资格复核')
overview=sheets['六家对照'];overview['name']='30家机构对照';overview['headers']=['机构','纳入研究的理由','最有价值的经营证据','类别','地区','具体客户','对我们公司的判断','资料入口']
overview['widths']=[28,46,62,26,24,66,68,52]
core={
 '北京香港马会会所':('综合会员会所','北京、跨地设施','个人会籍使用人、公司提名使用人及家属；分别解决接待、康体与家庭活动需求。','学习使用人、家庭附属卡与另付活动的清楚分层。'),
 'EO中国华东分会':('企业家固定小组','中国华东','符合企业营收及创始人、所有者条件的经营者；全球另有配偶及生活伴侣小组。','学习固定小组、保密规则与新成员培训。'),
 '长江商学院':('商学院与校友组织','全国及海外模块','官方称EMBA累计学员99%以上为企业核心决策层；通过教育选拔建立长期同学关系。','学习班级关系、企业互访和毕业后的长期组织。'),
 '木兰汇':('女性企业家社群','全国','女性企业家与商业经营者；官方2026介绍近1000位成员，112位核心成员企业市值或估值20亿元以上。','学习明确的女性经营者客群与年会、考察组合。'),
 '正和岛':('企业家社群与商业内容','全国及地方组织','以企业家及经营决策者为目标；已采同名平台账号的认证归属另列核验状态。','学习商业内容、企业访问与地方组织的连接。'),
 '优家荟':('女性生活与成长社群','城市及跨城活动','以女性为主要服务对象，围绕生活体验、学习成长与同行关系组织；实际资产分布未公开。','学习生活、成长与持续女性关系的产品组合。')}
core_rows=[]
for row in overview['rows']:
 n=row[0];kind,city,who,judgment=core[n]
 us=[v for rr in sheets['会员权益']['rows'] if rr[0]==n for v in str(rr[4]).split('\n') if v.startswith('http')]
 core_rows.append(row+[kind,city,who,judgment,us[0] if us else ''])
overview['rows']=core_rows
overview['rows'] += [[r['name'],r['rights'].split('；')[0],r['performance'],r['kind'],r['city'],r['who'],r['judgment'],r['url']] for r in R]
overview['note']='30家研究对象：原六家深度案例＋24家扩展对照；按服务方式分类，不设综合排名。2026年10月21日复核。'
for tab,key,label in [('会员权益','rights','产品与实际使用边界'),('客户画像','who','谁会购买或参加'),('获客方式','acq','公开可见的客户进入路径'),('活动流程','event','已公开活动或标准服务流程'),('经营表现','performance','规模、参与及持续经营证据')]:
 for r in R:sheets[tab]['rows'].append([r['name'],label,1,r[key],r['url']])
 if tab=='经营表现':
  for r in R:sheets[tab]['rows'].append([r['name'],'我们的判断',2,r['judgment'],r['url']])
 sheets[tab]['note']='覆盖30家；原六家详细记录保留。公开事实、已公布安排与研究判断在内容模块中分别标明。'
# Append original structured supplementary evidence in the same readable prose schema.
mapping=[('产品与会员权益','会员权益'),('客户画像','客户画像'),('获客与转化','获客方式'),('活动流程','活动流程'),('规模与活跃度','经营表现')]
def urls(sid):
 ids=set(re.findall(r'[A-Z]\d+',sid));return list(dict.fromkeys(x[2] for x in sources if x[0] in ids))
for src,dst in mapping:
 for row in ct[src]['rows']:
  n=row[0];n='中欧国际工商学院' if n in ['中欧HEMBA','中欧AMP','中欧MBA'] else n
  if n not in names:continue
  # Six deep cases have newer rewritten content; add only additional institutions.
  if n in orig6:continue
  text='；'.join(str(x) for x in row[1:-1] if x is not None)
  sheets[dst]['rows'].append([n,'补充原始字段｜'+src,2,text,'\n'.join(urls(row[-1]))])
prices=sheets['六家价格'];prices['name']='30家价格';prices['note']='会籍入会费、年费、教育项目学费、单场票价分别记录。金额为数字；未公开的保留空白；历史价格注明年份。'
for row in ct['价格与收费']['rows']:
 if row[0] in names and row[0] not in orig6:
  if row[0]=='创合汇':continue # gifted marketing value is not an actual price
  u=urls(row[-1]);prices['rows'].append([row[0],row[2],row[3],row[4],row[5],row[6],row[7],row[8]+'；'+row[9],row[-1],u[0] if u else '', '历史价格' if '2019' in row[6] else ('公开报价' if row[3] is not None else '未公开取得金额')])
def price(n,product,amount,unit,rights,limits,url,currency='CNY',period='2026-10-21页面；未标生效日'):
 prices['rows'].append([n,product,amount,currency,unit,period,rights,limits,source(url,n+'｜费用及权益'),url,'公开报价'])
np='https://www.nanshamarina.com/membership/128.html'
for p,v,u,rt,lm in [('短期一年会籍',23000,'份／一年','1主卡1附属卡；家庭康体设施、租艇与培训会员价、优先活动','租船培训另付，餐饮按优惠规则'),('短期三年会籍',48000,'份／三年','1主卡1附属卡；短期会籍列明权益','不是每年4.8万元；额外消费另付'),('普通个人会籍',200000,'整份／一次','普通会籍；无泊位租赁申请权','另付管理费1200元／季；有效至2040-01-01'),('普通公司单提名会籍',240000,'整份／一次','1名公司提名使用人；普通会籍','另付管理费1200元／季；不是每人年费'),('海事个人会籍',780000,'整份／一次','海事权益及泊位租赁申请权','另付管理费1500元／季；泊位按规则收费'),('海事公司单提名会籍',860000,'整份／一次','1名公司提名使用人；海事权益','另付管理费1500元／季'),('普通会籍管理费',1200,'份／季度','维持普通会籍','年四季；餐饮等另消费'),('海事会籍管理费',1500,'份／季度','维持海事会籍','年四季；餐饮等另消费')]:price('南沙游艇会',p,v,u,rt,lm,np)
vp='https://www.oldchair.cn/wsdhy_jiage'
for p,v,rt in [('CE年度会员',148000,'最高经营决策者；5—6次两天小组、10—12小时教练、5—6次专家分享'),('CE Plus年度会员起价',158000,'更高规格CE Plus；官网为起价'),('SE年度会员',96000,'9次一日小组、9小时教练、4次专家'),('KE年度会员',78000,'关键高管产品；按具体项目安排'),('CE／SE初始费',3000,'入会初始费，年度费另付')]:price('伟事达中国',p,v,'人／一次' if '初始' in p else '人／年',rt,'CE与SE另收初始费；CE Plus为起价',vp,period='官网2026产品')
for p in ['全球一次入会费','全球年度会费']:price('YPO',p,4790,'人／一次' if '一次' in p else '人／年','全球组织层收费','地方分会费另付；年费按财年比例，接纳后不退；特定月份加入另含下财年',extra[0][1],'USD')
price('上海财经大学商学院','2026金融EMBA学费',488000,'人／完整项目','金融EMBA教育项目','非社群年费；其他项目不同',next(r['url'] for r in R if r['name']=='上海财经大学商学院'),period='2026级')
price('交大高金','2026金融EMBA学费',828000,'人／完整项目','金融EMBA教育项目','非社群年费；附加费用按项目条款',next(r['url'] for r in R if r['name']=='交大高金'),period='2026级')
au=extra[1][1]
for p,v,rt in [('Leadership Alliance',90000,'1主卡＋不限附卡'),('CEO Circle',60000,'邀请制；1主卡＋3附卡'),('Large Corporate',28000,'中国营收超过5亿美元；1主卡＋4附卡'),('Medium Corporate',22000,'中国营收100万—5亿美元；1主卡＋3附卡'),('Small Corporate',16500,'中国营收少于100万美元；1主卡＋2附卡')]:price('上海美国商会',p,v,'公司／会籍报价；期限见申请条款',rt,'公司卡不等于该金额每位个人；单独活动可能另收费',au)
price('上海美国商会','个人会籍',5000,'人／12个月','在华外籍居民21岁以上；全职工作证明','不可退款；身份限制；活动另按规则',extra[2][1])
price('上海美国商会','Global Circle',1000,'公司／会籍报价；期限见申请条款','尚无中国机构的跨国公司；1主卡＋1附卡','以美元收费；非中国个人会员报价',au,'USD')
# Other price records already collected in the original source model.
base=json.loads((B/'research/data.json').read_text())
for row in base['prices']:
 if isinstance(row,list) and row[0]=='中国美国商会':
  prices['rows'].append([row[0],row[2],row[3],row[4],row[5],row[6],row[7],row[8]+'；'+row[9],row[-2],next(iter(urls(row[-2])),'') ,'公开活动报价'])
for n in names:
 if not any(x[0]==n for x in prices['rows']):
  r=next(x for x in R if x['name']==n);prices['rows'].append([n,'会籍／具体课程或活动',None,'','未公开取得','2026-10-21复核','见会员权益表','已查官网产品、会籍及活动入口；未取得带期限的金额',r['sid'],r['url'],'未公开取得金额'])
# Typed business evidence supplementary table, including latest SEE attendance denominator.
metricrows=[r for r in ct['规模与活跃度']['rows'] if r[0] in names]
see=next(r['url'] for r in R if r['name']=='阿拉善SEE生态协会')
for label,n,unit,scope in [('有效会员',480,'人','2025-11-30'),('会员大会现场本人出席',111,'人','2025会员大会'),('会员大会现场委托',85,'人','2025会员大会'),('会员大会线上本人出席',92,'人','2025会员大会'),('会员大会线上委托',30,'人','2025会员大会'),('会员大会含委托出席率',.6625,'比例','318／480；含委托，不是现场实到率')]:metricrows.append(['阿拉善SEE生态协会',label,n,unit,scope,'官方活动回顾',source(see,'SEE｜会员大会回顾')])
new={'name':'经营指标明细','headers':ct['规模与活跃度']['headers']+['原文网址'],'rows':[r+[(urls(r[-1])or[''])[0]] for r in metricrows],'note':'数值保留原统计范围；最新SEE大会与10月末履职报告分别列示。','widths':[29,39,18,26,55,35,17,56]}
d['sheets'].insert(8,new)
# Social observations: only authenticated primary brand accounts count as official account comparisons.
account=sheets['平台账号'];print('accounts',account['headers'])
social=[]; posts=sheets['平台内容明细'];hs=posts['headers']
for n in names:
 aliases=[n]
 if n=='中欧国际工商学院':aliases+=['中欧MBA']
 pp=[r for r in posts['rows'] if r[1] in aliases and '已核对主页认证' in str(r[10])]
 ar=[r for r in account['rows'] if n in str(r) and '认证' in str(r) and '未核' not in str(r) and '待核' not in str(r)]
 fan=None;an='';u=''
 if n=='中欧国际工商学院':fan=29849;an='中欧国际工商学院';
 if n=='长江商学院':fan=3304;an='长江商学院EMBA（项目号）'
 if ar:u=next((x for x in ar[0] if isinstance(x,str) and x.startswith('http')),'')
 def total(i):
  vs=[r[i] for r in pp if isinstance(r[i],(float,int))];return sum(vs) if vs else None
 social.append([n,'小红书',an,fan,len(pp),total(6),total(7),total(8),total(9),'2026-10-21','机构认证样本' if pp else '未取得可确认机构主体的完整样本','仅已采样内容汇总；评论／分享空白表示未取得，非零；转化率未公开',u])
d['sheets'].insert(9,{'name':'30家平台声量','headers':['机构','平台','认证账号','账号粉丝','已核验内容条数','样本点赞合计','样本收藏合计','样本评论合计','样本分享合计','采集时间','样本状态','统计口径','主页入口'],'rows':social,'note':'按已核验机构账号归属汇总，账号粉丝与帖子互动分开；当前不足以给30家按流量排名。','widths':[28,14,35,16,19,18,18,18,18,22,45,65,52]})
# Attach source snapshots and provenance; unchanged existing raw and model sheets stay intact.
target=B/'交付资料/公开网页存档/30家扩展复核';shutil.copytree(B/'collection-thirty-refresh-20261021/raw',target,dirs_exist_ok=True)
for p in fresh['pages']:
 sheets['网页采集台账']['rows'].append(['30家扩展复核',p['机构'],p['网址'],p['状态'],p['HTTP状态'],p['正文字数'],p['采集时间'],'公开网页存档/30家扩展复核/'+Path(p['原文文件']).name if p['原文文件'] else '',p['错误']])
for r in R:
 if not any(x[1]==r['name'] for x in sheets['市场机构地图']['rows']):sheets['市场机构地图']['rows'].append(['N'+str(len(sheets['市场机构地图']['rows'])+1),r['name'],r['kind'],r['city'],r['rights'],r['who'],r['sid'],'扩展对照','已查原始资料','30家研究对象',r['url']])
 sheets['证据缺口']['rows'].append([r['name'],'本轮已查产品、客户、公开费用及活动；资料入口见各专题表','实际付费成员、近90天去重实到、续费、获客支出、成交和利润未取得；单场流程缺失见活动流程'])
for s in [overview,prices]:
 pass
sheets['文件与数据说明']['rows'].append(['本次30家扩展',30,'主表及价格、权益、画像、获客、流程、经营表现均覆盖30个机构；六家档案继续保留，不代表30家均为直接竞品。'])
d['counts']['institutions']=len(sheets['市场机构地图']['rows']);d['counts']['pages']=len(sheets['网页采集台账']['rows']);d['counts']['comparison_institutions']=30
sheets['市场机构地图']['note']=str(d['counts']['institutions'])+'家机构与品牌线索；本次选取30家结构化对照，原六家保留深度案例。'
for row in sheets['文件与数据说明']['rows']:
 if row[0]=='市场机构地图':row[1]=d['counts']['institutions']
for s in d['sheets']:
 assert all(len(r)==len(s['headers']) for r in s['rows']),(s['name'],[(len(r),len(s['headers']))for r in s['rows']if len(r)!=len(s['headers'])][:2])
for tab in [overview,prices]+[sheets[t]for t in ['会员权益','客户画像','获客方式','活动流程','经营表现']]:assert set(names)<=set(r[0]for r in tab['rows']),tab['name']
(B/'research/30家工作簿数据.json').write_text(json.dumps(d,ensure_ascii=False,indent=2))
out=B/'交付资料/数据明细/30家机构扩展';out.mkdir(exist_ok=True)
for s in d['sheets']:
 with (out/(s['name']+'.csv')).open('w',encoding='utf-8-sig',newline='')as f:csv.writer(f).writerows([s['headers']]+s['rows'])
print(json.dumps({'institutions':30,'sheets':len(d['sheets'])+1,'price_rows':len(prices['rows']),'new_page_attempts':len(fresh['pages'])},ensure_ascii=False))
