import json
from pathlib import Path
from collections import Counter
B=Path(__file__).parent
old=json.loads((B.parent/'community-research-final-20261022/修订研究数据.json').read_text())
new=json.loads((B/'五家深挖工作数据.json').read_text())
market=old['market'][:]
market.insert(0,['钻石婚恋／钻石精英会','高净值婚恋定制与单身圈层','上海及异地服务','官网定义个人或家庭财产1000万元以上或个人条件极优秀；活动各自有准入条件','婚恋专项优先研究；重点学定制项目与圈层分层','https://www.zuanshi.com/new/loveCustomization'])
priority={'钻石婚恋／钻石精英会','大超说媒','陌上花开HIMMR','我主良缘','金凤凰深港婚恋'}
market=[r+[('婚恋专项优先' if r[0] in priority else '持续社群主要参考' if r[0] in ['北京香港马会会所','长江商学院','木兰汇'] else '补充参考')] for r in market]
products=[]
for p in new['products']:
 missing=[]
 if p.get('period') is None:missing.append('完整服务期')
 if p.get('date_count') is None:missing.append('承诺介绍或约见次数')
 if p.get('refund') is None:missing.append('退改规则')
 if p['product']=='9月20日深港二婚专场':missing=['实到人数','实收收入','活动后转购']
 products.append([p['brand']+'\n'+p['product'],p['price_yuan'],p['unit'],p['rights'],'、'.join(missing),p['source']])
unknown=[
 ('大超说媒','高净值单身局','按单场参加','验资、面试等按场次；10月深圳活动和10月18日聚会有公开内容','本期票价、性别差价、人数、退改','https://www.douyin.com/user/MS4wLjABAAAAzS55hxJ4_NKjM9xZw8xHpGVx8sP-m2Bxy6ekRE2I7-Q'),
 ('大超说媒','一对一私人定制','定制服务','简介公开提供私人定制及精准匹配','总价、服务期、介绍次数、成功收费与退改','https://www.xiaohongshu.com/user/profile/6270c387000000002102a8b5'),
 ('HIMMR','同城线下活动','按场次','8分钟约会、桌游、摇摆舞、飞盘等','近期活动票价、名额及退改','https://www.himmr.tech/'),
 ('HIMMR','王牌1V1','顾问匹配','红娘陪伴、推荐、深度复盘与个性化指导','总价、合同期、承诺推荐次数、退款','https://www.himmr.tech/'),
 ('我主良缘','门店红娘及匹配方案','门店咨询后签约','品牌公开提供婚恋匹配、情感咨询和形象管理；各项是否包含须按合同','各城市产品名称、当前总价、期限、介绍次数、退改','https://www.7799520.com/'),
 ('我主良缘','派聚社交','旅行社交产品线','集团官网列为旅行社交品牌','当前在售行程、单价、包含项、旅行交付主体、成团回顾','https://www.liangyuan.com/')]
for brand,product,unit,rights,missing,url in unknown:products.append([brand+'\n'+product,None,unit,rights,missing,url])
for p in old['products']:
 if p['brand'] in ['大超说媒','陌上花开HIMMR']:continue
 products.append([p['brand']+'\n'+p['product'],p['price'],p['unit']+'；'+p['period'],p['rights'],'原核查期；按所引来源使用，线上产品为补充参考',p['source']])
profiles=[]
for p in new['segments']:
 profiles.append([p['brand']+'\n'+p['product'],(p.get('age') or '年龄未列')+'\n'+(p.get('job') or '职业未列')+'\n'+(p.get('education') or ''),p.get('asset') or '收入或资产未列',(p.get('personality') or '性格未列')+'\n'+(p.get('hobby') or '兴趣未列'),p['type']+'\n'+p.get('motivation','')+'\n'+p.get('height',''),p['source']])
profiles.extend([
 ['大超说媒\n定位咨询','年龄、岗位未列','个人收入与家庭资产分布未公开','内容谈择偶与关系；没有客户性格、兴趣统计','999本人／199红娘定位，对应不同咨询提供者；未核实买家构成','https://www.xiaohongshu.com/user/profile/6270c387000000002102a8b5'],
 ['大超说媒\n清北本科局','近期招募点名女生清北本科纯文化生；其他年龄职业条件未补齐','本期资产或收入条件未核实','未披露','学历专场；与高净值局分开，不能套用往年5000万元条件','https://www.douyin.com/user/MS4wLjABAAAAzS55hxJ4_NKjM9xZw8xHpGVx8sP-m2Bxy6ekRE2I7-Q'],
 ['我主良缘\n顾问及活动','品牌覆盖白领、公务员、企事业单位、企业主等；当前付费年龄、岗位占比未公开','A8准入与客户收入分布未公开','当前客户性格与兴趣分布未公开','品牌服务范围；尚不能拆出可靠的分产品实际付费画像','https://www.7799520.com/']])
activities=[
 ['钻石精英会','2026-08-22','招募资料','QS海归名校单身社交局',None,'学历审核、访谈、证件与工作资产验证；现场逐时议程未列','学历与综合背景条件见海报；8月31日账号另有同主题帖，正文不足以核实完整交付','https://www.zuanshi.com/webActivity/newActivityDetail?id=056bdd2152d24fa1b9dd983ea9e4a473'],
 ['钻石精英会','2026-09-19','招募资料','500强名企海归单身派对',None,'五证核验、男士资产资料、女士面试及婚姻意愿访谈；现场逐时议程未列','男性多种准入任选；女性00后、168厘米以上、本科以上','https://www.zuanshi.com/webActivity/newActivityDetail?id=eb19e98e3e5642f3a51907c180b4930c'],
 ['钻石私董会','2026-10-24','未来招募','第74场资产亿元单身局',None,'审核及访谈；活动场地定向通知','标题场次数为品牌自述，不能据此填本期举办74场','https://www.zuanshi.com/webActivity/newActivityDetail?id=b4a2dc587c604ac59cfa6ccfc05193ab'],
 ['钻石私董会','2026-10-24','未来招募','山野见己悦享局',None,'男士提交资产资料、女士面试；详细出行线路和天数未列','1980至2000年生；海报有户外生活体验表达，但没有完整在售旅行方案','https://www.zuanshi.com/webActivity/newActivityDetail?id=8f6c2d32f22b42aaa234cf665d3e4f02'],
 ['金凤凰深港婚恋','2026-09-20','招募及报名快照','深港二婚离异联谊会',99,'报名→网上或现场支付→签到→轮转交流→自愿后续联系；14至17时','99元含酒店与茶歇；计划30男30女；网页报名37男22女；实到未公开','https://www.jfh999.com/party/311.html'],
 *[a for a in old['activities'] if a[0] not in ['青藤之恋','牵手']],
 ['如爱单身俱乐部','2026-10-18','旅行招募及报名快照','盘锦一日出游','男115 女95','按公开旅行活动招募；详细现场交付未核实','网页报名18；一般本地单身客群，作为旅行组织参考','https://www.ruailove.com/party/89.html']]
content=[r for r in new['contents'] if r['sample_status']=='待核验的品牌或主理人内容']
posts=[[r['brand'],r['account'],'小红书',r['date'],r['title'],r['metrics']['点赞'],r['metrics']['评论'],r['metrics']['收藏'],r['metrics']['分享'],r['url']] for r in content]
posts.extend(old['posts'])
sources=old['sources'].copy()
extra=[('Z01','钻石爱情定制收费权益','https://www.zuanshi.com/new/loveCustomization','本次官网正文；现挂网项目报价'),('Z02','钻石官网定义及审核文件','https://www.zuanshi.com/webContent/question','官网现行页面；未标更新日'),('Z03','钻石家族幸福服务','https://www.zuanshi.com/webindex/familyOffice','官网现行产品说明'),('Z04','钻石近期活动目录','https://www.zuanshi.com/webActivity/newActivityList','2026年8至10月招募目录'),('G01','金凤凰会员分级权益','https://www.jfh999.com/about/20.html','官网现行服务说明'),('G02','金凤凰活动费与会费说明','https://www.jfh999.com/about/8.html','官网现行规则'),('G03','金凤凰9月20日专场','https://www.jfh999.com/party/311.html','活动招募海报及报名快照'),('G04','金凤凰收费标准与报名流程','https://www.jfh999.com/about/24.html','页面未展示完整数字报价'),('W01','我主良缘品牌矩阵','https://www.liangyuan.com/','官网；派聚社交为旅行社交品牌'),('W02','我主良缘活动入口','https://www.7799520.com/party','官网活动页；本次正文未返回有效场次明细')]
for id,name,url,kind in extra:sources[id]=[name,url,'2026-10-22核查',kind]
for i,a in enumerate(new['accounts'],1):sources[f'X{i:02}']=[a['name']+'小红书主页',a['url'],a['collected_at'],'名称与简介匹配；主体认证未单独取得']
result=dict(market=market,prices=products,profiles=profiles,activities=activities,posts=posts,sources=sources,accounts=new['accounts'],evidence=new,legacy=old,counts=dict(current_xhs=len(content),douyin_reused=len(old['posts']),market=len(market),price_rows=len(products)),
 review='五家为优先研究对象；比较的是服务与客户路径，不评最权威或经营最好。')
(B/'正式报告数据.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(result['counts'])
