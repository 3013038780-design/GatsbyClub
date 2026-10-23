"""Append the observed expansion corpus and primary-source operating evidence."""
import json
from pathlib import Path

def extend(payload,root,now):
 tables=payload['tables'];by={t['name']:t for t in tables};social=root/'social-platforms'
 def add(name,row):
  if row not in by[name]['rows']:by[name]['rows'].append(row)
 sources=[
 ('C35','创合汇','https://www.chuanghehui.com/view/club','全球商学院共创联盟与创投俱乐部','未标统计截止日'),
 ('C36','创合汇','https://www.chuanghehui.com/view/activity','活动目录、报名人数与会员入口','目录含2022年及未标年份旧活动'),
 ('C37','阿拉善SEE生态协会','https://conservation.see.org.cn/news/dynamic/2025/1203/12953.html','2025会员大会与履职报告','2025-10-31经营统计；2025-12-03发布'),
 ('C38','阿拉善SEE生态协会','https://conservation.see.org.cn/Admission/','入会指南与会员活动类型','网页未标更新时间'),
 ('C39','德申汇','https://www.detion.com/about','关于德申','网页未标统计基期'),
 ('C40','德申汇','https://detion.com/news/3481','用户发展与成长教育联席会议','2024—2025年度；7月1日留存数'),
 ('C41','上海新沪商联合会','https://mzj.sh.gov.cn/MZ_shetuan748_0-2-3-357-732/20200520/MZ_shetuan748_141531.html','上海民政收费公示','2019-04-10历史会费标准'),
 ('C42','创合汇','https://www.chuanghehui.com/view/zlyzx','战略解码工作坊招生与增值权益','网页未标当届年份'),
 ('C43','德申汇','https://detion.com/news/3527','102A德申友约第二期活动','2024—2025年度8月15日活动回顾')]
 for code,b,u,title,period in sources:add('来源台账',[code,b,title,u,period,'中国大陆','政府公开资料' if code=='C41' else '机构公开资料','网页正文；Crawl4AI存档或原始页面核对',now])
 for b,kind,focus,url in [
 ('创合汇','学习与多主题社群','学习、私董会、参访和行业社群组合','https://www.chuanghehui.com/view/club'),
 ('阿拉善SEE生态协会','企业家公益会员组织','共同事业、参与机制、续费及企业互访','https://conservation.see.org.cn/Admission/'),
 ('德申汇','线上线下商务社群','分区俱乐部、会员发展及保留机制','https://www.detion.com/about'),
 ('上海新沪商联合会','企业家商会替代服务','分层会费、会员组织与商务学习','https://mzj.sh.gov.cn/MZ_shetuan748_0-2-3-357-732/20200520/MZ_shetuan748_141531.html')]:
  add('机构与研究重点',[b,'新增扩展对照；最终六家待重选',kind,{'创合汇':'30+社群组织、100000+成员；未标统计期','阿拉善SEE生态协会':'2025-10-31有效会员475、续费率70%','德申汇':'2024—2025年度会议披露7月1日留存9922人','上海新沪商联合会':'已取得2019年政府公示的分层会费'}[b],focus,{'创合汇':'C35 C36 C42','阿拉善SEE生态协会':'C37 C38','德申汇':'C39 C40 C43','上海新沪商联合会':'C41'}[b]])
 add('产品与会员权益',['创合汇','创投俱乐部','投资学堂、路演、论坛、私董会、闭门会、企业参访六模块','全年4场商学院好项目路演；优先参加活动','价格与其他权益使用限制待补','C35'])
 add('产品与会员权益',['阿拉善SEE生态协会','公益会员组织','联谊、企业互访、当地环保活动、海外考察、会员大会','环保参与、学习交流及组织治理权利','与商业社交服务分列为替代模式','C38'])
 add('客户画像',['创合汇','创投俱乐部目标资格','企业年收入500万元以上；创始人、联合创始人、合伙人、CEO等','投资与企业成长','资格说明；非实际客户资产核验','企业年收入不作为个人资产','C35'])
 add('获客与转化',['创合汇','官网→在线申请／顾问微信','官网俱乐部介绍、申请表入口、顾问咨询','课程顾问保荐或校友推荐→提交信息与企业介绍→资质审核→缴费→开营','工作坊每期最多10家企业且细分行业限一家','这是公开招生流程；成交结果待补','C35 C42'])
 add('活动流程',['创合汇','战略解码工作坊','标准产品及报名流程','网页未标当届年份','3天2夜；每期最多10家企业','顾问保荐或校友推荐→提交报名与企业介绍→资格审核→缴费→开营','具体课程小时安排未披露','企业团队学习；不等同10名社交活动客户','C42'])
 add('活动流程',['阿拉善SEE生态协会','2025会员大会','实际活动回顾','2025会员大会','现场及线上表决；具体到场总人数未披露','治理团队履职报告→监事会报告→三项表决→会员嘉许与终身会员致敬','包含现场与线上投票，组织权利与共同事业增强参与','治理会议案例，非商业社交售票活动','C37'])
 for label,val,unit in [('有效会员',475,'位'),('其中终身会员',233,'位'),('续费率',0.70,'比例'),('会费收入',22800000,'CNY'),('会员公益参与时长',15310,'小时'),('全年完成培训',6,'场'),('培训覆盖会员',150,'余名')]:
  add('规模与活跃度',['阿拉善SEE生态协会',label,val,unit,'2025履职报告；截至10月31日','机构披露；续费计算口径待补' if label=='续费率' else '官方履职报告披露','C37'])
 add('规模与活跃度',['德申汇','平台用户留存数据',9922,'人','2024—2025年度会议；7月1日快照','官方会议自述；历史数','C40'])
 add('规模与活跃度',['德申汇','年度保留率目标',0.80,'比例','2024—2025年度','计划目标，非完成结果','C40'])
 add('规模与活跃度',['创合汇','官网社群成员披露',100000,'以上','官网未标统计截止日','机构自述；未说明付费与去重','C35'])
 add('规模与活跃度',['创合汇','专属社群组织披露',30,'以上','官网未标统计截止日','组织数量','C35'])
 for tier,amount in [('会员单位',5000),('理事单位',10000),('常务理事单位',25000),('副会长单位',50000),('会长单位',500000),('监事长单位',100000),('监事单位',10000)]:
  add('价格与收费',['上海新沪商联合会','上海',tier+'历史会费',amount,'CNY','单位/年','2019-04-10公示；非2026现价','按组织职务层级收费','专项活动及附加费用未列','历史定价结构参考；现行标准待核','C41'])
 add('价格与收费',['创合汇','依工作坊','智卡会员赠送权益估值',980,'CNY','一年权益宣传价值','网页未标当届年份','工作坊赠送一年智卡会员','工作坊学费未公开取得','宣传价值；不是独立会籍报价或成交价格','C42'])
 def load(name):
  p=social/name
  return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []
 cards={}
 for r in load('discovery-search-cards.jsonl'):cards[(r['keyword'],r['sort'],r['note_url'])]=r
 def num(v):
  try:return int(str(v).replace(',',''))
  except (ValueError,TypeError):return None
 rows=[]
 for r in cards.values():
  m=r.get('metrics',{});rows.append(['小红书',r['keyword'],r['sort'],r['rank'],r['account_name'],r['title'],num(m.get('liked_count')),num(m.get('collected_count')),num(m.get('comment_count')),num(m.get('shared_count')),r['captured_at'],r['note_url'],r['profile_url'],'发现线索；主体、人群及发布时间待核'])
 rows.sort(key=lambda r:(r[1],r[2],r[3]))
 tables.append(dict(name='扩展内容线索',headers=['平台','发现关键词','排序','搜索位置','发布账号','内容标题','点赞','收藏','评论','分享','采集时间','内容链接','账号链接','研究状态'],rows=rows,widths=[15,26,15,14,36,72,15,15,15,15,29,65,65,50]))
 accounts={}
 for r in load('brand-account-candidates.jsonl'):
  r=dict(r,keyword=r.get('brand',''),captured_at=r.get('collected_at',''));accounts[r['profile_url']]=r
 for r in load('discovery-account-candidates.jsonl'):accounts[r['profile_url']]=r
 vp=social/'verified-brand-accounts.json'
 verified={a['profile_url']:a for a in json.loads(vp.read_text())} if vp.exists() else {}
 ar=[]
 for r in accounts.values():
  m={i.get('type'):i.get('count') for i in r.get('interactions',[])};name=r['account_name']
  excluded=any(t in name for t in ['保险','观察员','电竞','培训师','宛小','雅彤','研究员Daniel','爱订','情报局','老师','张坤','地产'])
  ar.append([name,num(m.get('fans')),num(m.get('interaction')),r['keyword'],'个人／供应商／偏离目标，排除核心样本' if excluded else '已核对机构认证标识' if r['profile_url'] in verified else '主理人运营号，单列；非已核验机构主号' if '主理人' in r.get('basic_info',{}).get('desc','') else '品牌候选，主体与高端客群待核验',r['captured_at'],r['profile_url'],r.get('basic_info',{}).get('desc','')])
 ar.sort(key=lambda r:(r[4].startswith('个人'),-(r[1] or 0)))
 tables.append(dict(name='扩展账号初筛',headers=['账号名称','粉丝数','获赞与收藏累计','发现关键词','初筛结论','采集时间','主页链接','主页业务自述'],rows=ar,widths=[44,18,24,25,62,29,88,85]))
 status={}
 for r in load('discovery-status.jsonl'):
  if r.get('sort'):status[(r['keyword'],r['sort'])]=r
 sr=[[k[0],k[1],r.get('search_cards'),r.get('captured_at'),r.get('error') or '已取得搜索卡片','每类别每排序第一页；不代表全平台穷尽'] for k,r in status.items()]
 tables.append(dict(name='扩展采集覆盖',headers=['关键词','排序','搜索卡片数','采集时间','状态','采样口径'],rows=sr,widths=[30,18,20,29,30,75]))
 dy=load('douyin-observed-content.jsonl')
 if dy:
  tables.append(dict(name='抖音已观察内容',headers=['发布账号','内容主题','点赞','收藏','评论','分享','可见发布日期','采集时间','来源','用途'],rows=[[r[k] for k in ['account','title','likes','favorites','comments','shares','published','captured_at','url','role']] for r in dy],widths=[35,90,18,18,18,18,27,29,80,60]))
 payload['findings'].append(['扩大机构发现与核对经营实绩','已补充类别词发现、账号粉丝快照及来源链接；阿拉善SEE披露2025年有效会员475位、续费率70%、会费收入2280万元。该数据列为公益会员组织经营对照，统计期明确保留。'])
 for row in by['待补数据']['rows']:
  if row[0]=='抖音与B站':row[3]='抖音已登录并观察搜索及视频互动；B站扫码尚未确认；两平台机构主号样本仍待补'
