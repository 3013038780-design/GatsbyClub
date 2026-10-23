import json, re
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
B=Path(__file__).parent
T=ZoneInfo('Asia/Shanghai')
def jl(p):
 return [json.loads(s) for s in p.read_text().splitlines() if s.strip()] if p.exists() else []
raw=jl(B/'social-platforms/xhs/jsonl/search_contents_2026-10-22.jsonl')
cards=jl(B/'social-platforms/brand-search-cards.jsonl')
attrs={r['note_id']:r for r in jl(B/'social-platforms/content-attribution.jsonl')}
cardmap={r['note_url'].split('/')[-1]:r for r in cards}
contents=[]
seen=set()
for r in raw:
 if r['note_id'] in seen:continue
 seen.add(r['note_id'])
 a=attrs.get(r['note_id'],{});c=cardmap.get(r['note_id'],{})
 date=datetime.fromtimestamp(r['time']/1000,T).date().isoformat() if r.get('time') else None
 approved=['钻石婚恋','大超说媒','陌上花开HIMMR','乐乐学姐优质脱单·陌上花开HIMMR','金凤凰深港婚恋','我主良缘']
 status='待核验的品牌或主理人内容' if a.get('account_name') in approved else '消费者或其他账号线索'
 if r['source_keyword']=='陌上花开':status='排除 同名搜索混入花店及个人账号'
 if date and not '2026-07-25'<=date<='2026-10-22':status='排除 近90天以外'
 metrics={}
 for k,ck in [('点赞','liked_count'),('收藏','collected_count'),('评论','comment_count'),('分享','shared_count')]:
  value=c.get('metrics',{}).get(ck)
  if value is None or value=='':value=r.get('share_count' if k=='分享' else ck)
  metrics[k]=int(value) if str(value).isdigit() else None
 contents.append(dict(brand=r['source_keyword'],account=a.get('account_name',''),date=date,title=r['title'],body=r.get('desc',''),url=r['note_url'],metrics=metrics,sample_status=status,collected_at=datetime.fromtimestamp(r['last_modify_ts']/1000,T).isoformat()))
accounts=[]
for r in jl(B/'social-platforms/brand-account-candidates.jsonl'):
 if r['brand']=='陌上花开' or r['account_name'] not in approved:continue
 visible={v['type']:int(v['count']) for v in r.get('interactions',[]) if v.get('show') is not False and str(v.get('count')).isdigit()}
 accounts.append(dict(brand=r['brand'],name=r['account_name'],url=r['profile_url'],intro=r.get('basic_info',{}).get('desc'),public_fans=visible.get('fans'),public_likes_and_saves=visible.get('interaction'),verification='名称与简介匹配 机构认证及主体待复核',collected_at=r['collected_at']))
facts=[]
def fact(brand,product,price,unit,rights,client,source,**kw):
 facts.append(dict(brand=brand,product=product,price_yuan=price,unit=unit,rights=rights,customer=client,source=source,**kw))
z='https://www.zuanshi.com/new/loveCustomization'
fact('钻石婚恋','爱情定制标准版',300000,'项目标价 服务总期未列','高级顾问团队；万人资源库；爱情猎头；五审八核及26维鉴别与引荐；钻石精英会权益','严肃婚恋的高净值单身者',z,period=None,date_count=None,refund=None)
fact('钻石婚恋','爱情定制高级版',600000,'项目标价 服务总期未列','资深顾问团队；千人库；增加精英猎访、52维鉴别、关系复盘、深度测评和钻石私董会权益；含标准版','需要更深入筛选和关系跟进的定制客户 研究推断',z,period=None,date_count=None,refund=None)
fact('钻石婚恋','爱情定制尊享版',1000000,'项目起价','首席团队；定向独享资源与百人库；整体策划；特殊要求猎取；隐私权限；全员团队支援；含前两档','对寻访范围、特殊条件或保密要求更高的客户 研究推断',z,period=None,date_count=None,refund=None)
fact('钻石婚恋','家办整体幸福项目',10000000,'项目起价','家办专属团队；跨部门整体方案；家族择偶观梳理；其余多项验证会员可见','高净值家族 覆盖成长准备、婚恋和婚姻经营阶段',z,period=None,date_count=None,refund=None)
fact('大超说媒','本人择偶定位',999,'简介报价 次数和时长未列','大超本人提供择偶定位','希望梳理择偶要求与选择的单身客户','https://www.xiaohongshu.com/user/profile/6270c387000000002102a8b5',period=None,date_count=None,refund=None)
fact('大超说媒','红娘择偶定位',199,'简介报价 次数和时长未列','红娘提供定位','希望先获得咨询再决定是否参与后续服务的客户 研究推断','https://www.xiaohongshu.com/user/profile/6270c387000000002102a8b5',period=None,date_count=None,refund=None)
g='https://www.jfh999.com/about/20.html'
for name,rights in [
 ('网站注册会员','自助交友 无红娘服务'),('实名认证会员','与同级或低等级会员自助交友 无线下红娘'),
 ('普通VIP','红娘推荐国内会员 可多对一 优先推荐'),('高级VIP','一对一或多对一 优先推荐国内有房有车或公务员对象'),
 ('银卡VIP','资深红娘 推荐国内及港澳优质对象'),('金卡VIP','资深红娘 可安排香港见面 免费香港分支跟踪'),
 ('白金VIP','猎头部资深婚恋师多对一 优先推荐企业主高管 个性化方案'),('钻石VIP','总公司猎头经理多对一 中国及全球合作单位推荐 公司承担全球推广'),
 ('钻石王VIP','总公司猎头经理多对一 量身定制婚恋')]:
 fact('金凤凰深港婚恋',name,0 if name=='网站注册会员' else None,'网站注册免费 其他等级未公布完整报价',rights,'页面说明的是服务范围及拟推荐对象 未披露购买者年龄收入分布',g,period=None,date_count=None,refund=None)
fact('金凤凰深港婚恋','9月20日深港二婚专场',99,'元每人 单场','大梅沙高档酒店场地及茶歇；14时至17时；轮转交流；招募30男30女','深圳香港 离异及再婚意向单身者 未列年龄职业收入准入','https://www.jfh999.com/party/311.html',period='2026-09-20',registered_men=37,registered_women=22,actual_attendance=None)
segments=[
 dict(brand='钻石婚恋',product='总体官网定义',age=None,job='企业家 金融家 体育及文艺演艺人士等',asset='个人或家庭财产1000万元以上 或个人条件极优秀',personality=None,hobby=None,type='机构定位',source='https://www.zuanshi.com/webContent/question'),
 dict(brand='钻石精英会',product='2026年9月500强名企海归专场 男嘉宾',age=None,job='500强名企 海归 企业经营者 人才等 任选条件',asset='资产5000万元或年入100万元等仅为可选资格 企业纳税百万 员工50人等也可',personality='海报要求积极健康 有责任感和家庭意愿',hobby=None,type='活动招募条件',source='https://www.zuanshi.com/webActivity/newActivityDetail?id=eb19e98e3e5642f3a51907c180b4930c',poster='533049c8e41a'),
 dict(brand='钻石精英会',product='2026年9月500强名企海归专场 女嘉宾',age='00后 海报出生年份口径',job=None,asset=None,education='本科以上 名校优先',height='168厘米以上',personality='海报要求自律自信 家庭责任感 原生家庭幸福有爱',hobby=None,type='活动招募条件',source='https://www.zuanshi.com/webActivity/newActivityDetail?id=eb19e98e3e5642f3a51907c180b4930c',poster='533049c8e41a'),
 dict(brand='钻石私董会',product='第74场亿元单身局',age=None,job='科技创业经营者 上市公司董事长股东及家族二代等',asset='资产亿元以上或个人综合条件极优秀 招募可选项包括年入500万 企业估值亿元等',personality='男士责任感家庭担当 女士情绪稳定独立重家庭 均为招募描述',hobby=None,type='2026-10-24未来活动招募',source='https://www.zuanshi.com/webActivity/newActivityDetail?id=b4a2dc587c604ac59cfa6ccfc05193ab',poster='11bfeb9a0143、294283e27d2b'),
 dict(brand='钻石私董会',product='2026年10月山野悦享局',age='1980年至2000年出生',job='事业稳定',asset='男士提交存款房产股票等证明 金额未列 女士面试',height='男180厘米以上 女165厘米以上',personality='要求情感专一 阅历丰富 男阳光有活力 女思想独立',hobby='男士运动健身 属报名偏好',type='未来活动招募 非已成行旅行',source='https://www.zuanshi.com/webActivity/newActivityDetail?id=8f6c2d32f22b42aaa234cf665d3e4f02',poster='1f8c2475ee62'),
 dict(brand='HIMMR',product='同城交友活动',age=None,job='金融 互联网 高校等',asset=None,education='985 211 海外QS100等 官网定位',personality=None,hobby='桌游 摇摆舞 飞盘 依据活动类别 未披露客户实际爱好比例',type='机构定位及产品类型',source='https://www.himmr.tech/'),
 dict(brand='HIMMR',product='王牌1V1',age=None,job=None,asset=None,personality=None,hobby=None,motivation='注重隐私 希望高效 但时间少 异性圈子窄 缺乏恋爱经验',type='官网适用对象',source='https://www.himmr.tech/'),
 dict(brand='金凤凰深港婚恋',product='9月20日二婚专场',age=None,job=None,asset=None,personality=None,hobby=None,motivation='离异后谨慎重建关系 希望扩大深圳香港交友范围 海报诉求',type='活动招募',source='https://www.jfh999.com/party/311.html')
]
segments.extend([
 dict(brand='HIMMR',product='2026-10-21回国假期1V1匹配',age='先收集年龄 页面未给范围',job='在美国工作的华人男性 科技大厂或AI公司等',asset='仅称收入稳定 未列金额或资产线',personality=None,hobby=None,motivation='圈子同质化 借回国假期集中见面 并在推荐前确认双方未来是否愿意海外生活',type='机构近期产品招募定位',source='https://www.xiaohongshu.com/explore/6ad89198000000003103aa3d'),
 dict(brand='HIMMR',product='2026-08-24公开男嘉宾样例',age=None,job='互联网公司AI算法岗位',asset=None,education='清华电子工程本科 UCLA硕士 UIUC博士',personality='机构介绍为生活规律踏实',hobby=None,type='公开嘉宾样例 非整体画像及非已核实付费者',source='https://www.xiaohongshu.com/explore/6a8b24210000000003029321'),
 dict(brand='金凤凰深港婚恋',product='2026-08-22公开征婚样例',age='1995年生 约30至31岁',job='深圳事业单位',asset=None,education='硕士 本科211',personality='机构介绍为温婉善良 重视家庭',hobby='公园 爬山 短途旅行 羽毛球 瑜伽 舞蹈 游泳 象棋',type='机构公开介绍的单一样例 非整体客户分布',source='https://www.xiaohongshu.com/explore/6a89457f0000000014026d62'),
 dict(brand='金凤凰深港婚恋',product='2026-08-20公开征婚样例',age='1996年生 约29至30岁',job=None,asset='帖称香港住房为父母名下 个人收入未列',personality='机构介绍为性格温和',hobby='音乐 唱歌 旅游 美食 摄影',type='机构公开介绍的单一样例 非已核验付费者',source='https://www.xiaohongshu.com/explore/6a8666c1000000000b032a7a'),
])
data=dict(as_of='2026-10-22',window=['2026-07-25','2026-10-22'],priority=['钻石婚恋／钻石精英会','大超说媒','陌上花开HIMMR线下业务','我主良缘','金凤凰深港婚恋'],products=facts,segments=segments,accounts=accounts,contents=contents,
 issues=[
  dict(source='https://www.xiaohongshu.com/explore/6a754c540000000025013f6a',issue='标题写75岁 正文写75年 出生年份与标题年龄冲突 尚未采用年龄'),
  dict(source='https://www.zuanshi.com/webActivity/newActivityDetail?id=b4a2dc587c604ac59cfa6ccfc05193ab',issue='模板同时显示活动结束和报名成功 但海报日期为2026-10-24 截至10-22仍按未来招募 不是实际活动回顾'),
  dict(source='HIMMR小红书搜索',issue='关键词陌上花开混入花店个人 该批全部排除 已改HIMMR搜索'),
  dict(source='小红书账号接口',issue='show为false的粉丝字段不对外报告'),
  dict(source='https://www.xiaohongshu.com/user/profile/5f03d342000000000100684b',issue='账号简介获奖年数与官网不一致 年资奖项不作当前规模或服务质量证明'),
 ],
 interpretation_rules=['一个产品一条价格 不用活动票替代顾问合同','角色区分购买者、报名条件、拟推荐对象、客户自述','空值为尚未核实 不填0','隐藏粉丝字段不对外报告','仅有招募时不写为实际交付'],
 remaining=['五家各补两场近期活动招募与实际回顾','大超活动票及定制、HIMMR线下活动及1V1、我主良缘顾问、金凤凰各VIP的当前价格','核对品牌及主理人账号主体后做主页内容采样','目前未完成五家各20至30条近90天机构样本','当前真实付费人数 复购 续费及财务披露仍需补证','把婚恋五家补入正式报告 保留会所商学院等原线下对标与市场地图','简化Excel 保留35家以上机构和原始证据索引 不以本次五家替换总市场'])
(B/'五家深挖工作数据.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
print(json.dumps({'products':len(facts),'segments':len(segments),'accounts':len(accounts),'content_records':len(contents),'90d_brand_candidates':sum(r['sample_status']=='待核验的品牌或主理人内容' for r in contents)},ensure_ascii=False))
