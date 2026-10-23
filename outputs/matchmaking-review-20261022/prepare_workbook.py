import json,re
from pathlib import Path
from findings import BASE,SOURCES,PRICES,CASES,TRAVEL
D=json.loads((BASE.parent/'social-research-20261021/research/30家工作簿数据.json').read_text())
sheets={s['name']:s for s in D['sheets']};updates={}; appends={}
core=['北京香港马会会所','长江商学院','木兰汇','正和岛','优家荟','我主良缘','金凤凰深港婚恋','珍爱网']
url=lambda ids:'\n'.join(dict.fromkeys(SOURCES[k][1] for k in ids if k in SOURCES))
extra=[]
for c in CASES:
 name=c['name'];ss=c['sections'];portrait=' '.join(ss[0][1]);judgment=c['verdict'].replace('取消将其直接称为A8高端婚恋代表的判断','实际A8客群规模尚无公开验证').replace('不沿用全国直营扩张成功样板的定位','适合反向研究服务管理')
 extra.append([name,c['role'], next(' '.join(p) for t,p,ids in ss if t=='客户量和经营表现'), '专业婚恋与关系服务', '全国' if name!='金凤凰深港婚恋' else '深圳、香港及合作地区',portrait,judgment,url(ss[0][2])])
# Preserve all 30 institutions and append three rather than silently removing older research.
rows=[r[:] for r in sheets['30家机构对照']['rows']]+extra
for r in rows:r[1]=('主对标｜' if r[0] in core else '专题参考｜')+r[1]
updates['30家机构对照']={'rows':rows,'note':'33家机构，八家主对标已在入选理由中标明。婚恋专题复核2026-10-22，其他记录保留原日期。','title':'33家机构对照'}
price=[]
for n,prod,amt,cur,unit,period,rights,extra,ids,kind in PRICES:price.append([n,prod,amt,cur,unit,period,rights,extra,ids,url(ids.split()),kind])
appends['30家价格']=price
selectors={'会员权益':lambda t:'收费' in t or '权益' in t,'客户画像':lambda t:'服务谁' in t,'获客方式':lambda t:'获客' in t,'活动流程':lambda t:'流程' in t or '实际交付' in t or '旅游' in t,'经营表现':lambda t:'经营表现' in t or '具体学' in t or '启发' in t}
# My main case labels combine customer and acquisition; explicit marketing facts added below.
for tab,test in selectors.items():
 rr=[]
 for c in CASES:
  for title,ps,ids in c['sections']:
   if test(title):
    for i,p in enumerate(ps,1):rr.append([c['name'],title,i,p.replace('恋练同款','恋综同款'),url(ids)])
 appends[tab]=rr
appends['获客方式'] += [['我主良缘','获客入口与付费承接',1,'官网与App、单位联谊及活动报名承接接触，咨询后购买匹配及课程。派聚接本地与旅行社交；渠道花费、有效线索与成交未披露。',url(['M01','M02','M04','M07'])]]
metrics=[]
def metric(n,k,v,unit,scope,kind,ids):metrics.append([n,k,v,unit,scope,kind,ids,url(ids.split())])
metric('我主良缘','门店数量页面自述',62,'家','官网未标统计截止；不可当作当前核实营业数','企业规模自述','M03')
metric('我主良缘','城市覆盖页面自述',38,'座','同一官网关于页；未标统计截止','企业规模自述','M03')
metric('我主良缘','员工数页面自述',1700,'余人','关于页；另页2500余口径冲突，未合并','企业规模自述','M03')
metric('我主良缘','员工数另一页面自述',2500,'余人','招商页；与1700余口径未统一','企业规模自述','M04')
metric('金凤凰深港婚恋','官网目录累计条目',244,'条','2026-10-22目录；含讲座、培训、招募，不是全部已举办相亲','网页目录快照','M16')
metric('金凤凰深港婚恋','再婚专场报名',59,'人','2026-09-20活动；37男22女；网页累计报名，未取得实到','企业活动页面','M14')
metric('金凤凰深港婚恋','再婚专场男报名',37,'人','2026-09-20；宣传男30席，页面报名可超过','企业活动页面','M14')
metric('金凤凰深港婚恋','再婚专场女报名',22,'人','2026-09-20；宣传女30席','企业活动页面','M14')
metric('金凤凰深港婚恋','再婚专场男性报名比例',37/59,'比例','2026-10-22快照37／59；非现场性别比例','基于网页报名计算','M14')
metric('金凤凰深港婚恋','新年联谊报名',35,'人','2026-01-25活动；18男17女，未取得实到','企业活动页面','M15')
metric('珍爱网','官网累计用户自述',140000000,'超过人','2026-10-22主页，累计用户自述；非付费或月活','企业规模自述','M19')
metric('珍爱网','报道时深圳线下门店',1,'家','2025-03-25；当地报道时点，不外推全国或2026','媒体现场采访','M21')
metric('珍爱网','监管处罚金额',1700000,'CNY','2024-12-30监管发布第五案；非营业损失测算','监管原始发布','M23')
for c in CASES:
 for field in ['有效付费会员','近90天实际到场人数','年度收入','净利润','续费率','活动转婚介成交率','旅游复购率','A8客户数量']:
  metric(c['name'],field,None,'未披露','2026-10-22本轮公开资料未取得','未知','M01' if c['name']=='我主良缘' else 'M10' if c['name'].startswith('金凤凰') else 'M19')
appends['经营指标明细']=metrics
source=[]
for sid,(title,u,scope,kind) in SOURCES.items():source.append([sid,title,u,'见资料名称',scope,kind,scope,'保留原年份、原主体及证据类别','2026-10-22'])
appends['来源台账']=source
appends['30家平台声量']=[[c['name'],None,None,None,None,'2026-10-22未新增验证指标；MediaCrawler访问首页超时','粉丝、评论、分享未填零'] for c in []]
# Adopt actual original column schema for platform gap rows.
hs=sheets['30家平台声量']['headers'];plat=[]
for c in CASES:
 r=['']*len(hs);r[0]=c['name']
 for i,h in enumerate(hs):
  if i==0:continue
  if '状态' in h or '判断' in h or '说明' in h or '限制' in h:r[i]='本轮小红书访问超时，未新增已验证账号及互动；不以零代未知'
  elif '日期' in h or '时间' in h:r[i]='2026-10-22'
  elif '入口' in h or '网址' in h:r[i]=SOURCES['M01' if c['name']=='我主良缘' else 'M10' if c['name'].startswith('金凤凰') else 'M19'][1]
  else:r[i]=None
 plat.append(r)
appends['30家平台声量']=plat
# Update all relevant explanatory notes and preserve historical raw sheets.
updates['文件与数据说明']={'rows':sheets['文件与数据说明']['rows']+[['婚恋与旅游专题','2026-10-22','新增三家婚恋深查、21项价格记录和旅游对照；主对标调整为八家，Excel扩为33家。'],['平台补抓结果','本轮未新增','MediaCrawler访问小红书首页超时；旧数据保留原采集日期；不补造粉丝及分享。']],'note':'本轮婚恋专题更新；原宏观和平台样本保留统计时期。','title':'文件与数据说明'}
# Replace one stale note in guide rows and clarify main selection.
for r in updates['文件与数据说明']['rows']:
 if r[0] in ['六家独立案例','六家深度案例']:r[:]=['八家独立案例',8,'五家会员／学习／生活方式组织及三家婚恋机构；EO改为专题参考。']
 if r[0]=='时间':r[:]=['时间','2026-10-22专题更新','婚恋本轮新增，其他内容按各自原统计与采集时间。']
 if r[0]=='正式报告':r[:]=['正式报告','八家对标及婚恋旅游专题','本轮重写样本选择、比较与进入建议，页数见PDF。']
 if r[0]=='价格更新':r[:]=['价格更新','33家价格表','婚恋价格按商品、活动、历史合同与单方线索分列。']
# Append activity steps with known rather than fabricated timing.
steps=[]
for order,stage,detail in [(1,'申请与筛选','招募深港本地单身、有稳定工作；计划40人男女各半'),(2,'签到','2026-01-25 14:30开始签到；办公室内活动'),(3,'破冰与交流','海报拟设趣味破冰、361度深谈、茶歇和主题互动；活动15:00至17:00，无各环节分时'),(4,'活动后','可按意愿申请情感咨询；未取得实际跟进人数')]:steps.append(['金凤凰深港婚恋','2026年1月深港联谊公布方案',order,stage,detail,'资料M15；公布安排，不是实际回顾'])
for order,stage,detail in [(1,'景区及签到','2019-06-23第30届；1300余参与来自主办媒体回顾'),(2,'多场景交流','破冰、玫瑰传情、舞台相亲、8分钟约会和深度交流，未给各区时间表'),(3,'现场结果','报道112对现场牵手；不是长期结婚或金凤凰独家会员成果')]:steps.append(['金凤凰深港婚恋','2019年第30届观音山实际回顾',order,stage,detail,'资料M17；多机构联办'])
appends['活动环节明细']=steps
# Add travel as a distinct comparison worksheet; it answers a new specific user question.
new_sheet={'name':'婚恋与旅游结合','headers':['机构及项目','资料时期','产品价格及交付','仍缺什么','研究判断','来源编号','原文网址'],'rows':[r+[url(r[5].split())] for r in TRAVEL],'note':'单日景区相亲、酒店联谊和多日旅行分别判断；不以活动名称或历史报名推断当期经营。','widths':[32,28,66,58,64,20,58]}
# Register institutions in market map without deleting previous discovery records.
hs=sheets['市场机构地图']['headers'];mp=[]
for j,c in enumerate(CASES,61):
 values={'机构编号':f'MM{j}','机构':c['name'],'类别':'专业婚恋服务','城市':'全国' if c['name']!='金凤凰深港婚恋' else '深圳、香港','经营方式':c['role'],'目标人群':c['sections'][0][1][0],'来源编号':'M01' if j==61 else 'M10' if j==62 else 'M19','研究关系':'八家主对标','资料状态':'2026-10-22专题核查','研究层级':'深度案例','原文网址':c['sections'][0][2]}
 row=[]
 for h in hs:
  v=values.get(h,'');row.append(url(v) if h=='原文网址' and isinstance(v,list) else v)
 mp.append(row)
existing=sheets['市场机构地图']['rows']; byname={r[1]:r for r in mp}
maprows=[]
for r in existing:
 if r[1] in byname:
  newer=byname.pop(r[1]);newer[0]=r[0];maprows.append(newer)
 else:
  r=r[:]
  if r[1] in core:r[7]='八家主对标';r[9]='深度案例'
  if 'EO' in str(r[1]):r[7]='固定小组专题';r[9]='专题参考'
  maprows.append(r)
maprows+=list(byname.values());updates['市场机构地图']={'rows':maprows,'note':'机构去重保留；八家主对标与EO专题分别标明。2026-10-22婚恋更新。','title':'市场机构地图'}
# Explicit gaps for the three new institutions and retain prior EO specialist gaps.
hs=sheets['证据缺口']['headers'];gaps=[]
for c in CASES:
 r=['']*len(hs);r[0]=c['name']
 if len(r)>1:r[1]='已取得当期官网、产品说明及可核对合同／活动证据'
 if len(r)>2:r[2]='当期完整顾问价、有效付费、实到、A8客户数、收入利润及旅游复购'
 gaps.append(r)
appends['证据缺口']=gaps
page=[]
for row in json.loads((BASE/'collection.json').read_text()):
 page.append(['婚恋深查20261022',row['brand'],row['url'],'已采集' if row.get('status')==200 else '访问失败或受限',row.get('status'),row.get('chars',0),row.get('collected_at','2026-10-22'),('raw/'+row['file']+'.txt') if row.get('file') else '',row.get('error','')])
appends['网页采集台账']=page
catalog=json.loads((BASE/'jfh-activity-catalog.json').read_text())
appends['活动与会籍线索']=[['婚恋深查20261022','金凤凰深港婚恋',r['title'],r['url'],'https://www.jfh999.com/party/','2026-10-22','公布活动／报名记录；截止'+r['deadline']+'；页面报名'+str(r['registrations'])+'人，非实到'] for r in catalog]
# Save payload with exact prior schemas and no confidential material.
payload={'updates':updates,'appends':appends,'new_sheet':new_sheet,'rename':{'30家机构对照':'33家机构对照','30家价格':'33家价格','30家平台声量':'33家平台声量'},'core':core}
(BASE/'工作簿更新数据.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2))
print('append counts', {k:len(v) for k,v in appends.items()});print('platform headers',sheets['30家平台声量']['headers'])
