from detail import *
import re,datetime

src('X01','京城俱乐部小红书搜索观察','https://www.xiaohongshu.com/search_result_ai?keyword=京城俱乐部','小红书公开搜索','采集2026-10-21','平台搜索观察','有餐饮场景、着装和摄影线索，亦有同名误配。','搜索排序不代表全量，除个别记录外未逐篇阅读全文。')
src('X02','伟事达小红书搜索观察','https://www.xiaohongshu.com/search_result_ai?keyword=伟事达','小红书公开搜索','采集2026-10-21','平台搜索观察','教练、学习体验、峰会等内容。','含历史及相似名字，不能作为全量近期活跃。')
src('X03','耀悦高端旅行账号公开页','https://www.xiaohongshu.com/user/profile/63b3a40d0000000026005569','小红书账号自述','采集2026-10-21','平台账号快照','9507粉丝；4.3万获赞与收藏；账号称中青旅旗下品牌。','单一账号，非会员或客户；品牌认证主体未额外取得。')
notes=[]
for fn,brand,sid in [('capital_search.json','京城俱乐部','X01'),('vistage_search.json','伟事达中国','X02')]:
    path=ROOT/'research'/fn
    rows=json.loads(path.read_text()) if path.exists() else []
    for x in rows:
        card=x.get('card','').splitlines();date=next((s for s in card if re.search(r'\d{2}-\d{2}|天前|小时|昨天',s)),'未取得')
        val=card[-1] if card else ''
        count=int(val) if val.isdigit() else None
        excluded=bool(re.search('陈丽华|WESDAR|伟仕达',x['title']))
        status='排除 同名或无关' if excluded else '标题观察 待核正文与主体'
        notes.append([brand,x['title'],date,ASOF,'搜索标题卡片',count,None,None,'商业内容标识未核实',status,'https://www.xiaohongshu.com'+x['href'].split('?')[0],sid,'非随机搜索样本；月日年份未明示，不推定真实客户身份'])

raw=json.loads((ROOT/'research/travel_notes_raw.json').read_text())
like_values=[None,264,2,4,16,13,656,48,527,132,173,235,45,33,26,573,168,120,275,200]
for j,x in enumerate(raw,1):
    ax=x['ax'];d=re.findall(r'\d+ text ((?:编辑于 )?(?:(?:\d{4}-)?\d{2}-\d{2}|\d+天前|昨天[^\n]*|\d+小时前)[^\n]*)',ax)
    date=d[-1] if d else '日期未取得'
    sid=f'X03-{j:02}'
    title=x['title'];url=x['url']
    theme='目的地与资源'
    if re.search('假期|请3天|连休',title):theme='假期安排'
    elif re.search('早鸟|立减|送1|4间房',title):theme='优惠或稀缺资源'
    elif re.search('科考|巡护|保护区',title):theme='自然与科考'
    elif '如何选船' in title:theme='比较与选购指南'
    notes.append(['耀悦',title,date,ASOF,'逐篇正文及账号目录',like_values[j-1],None,None,'品牌自发内容；平台广告标识未核实',theme,url,sid,'月日未明示年份，按采集时上下文推定2026；编辑日与首发日区分'])
    src(sid,title,url,'耀悦高端旅行账号',date,'品牌内容自述',theme+'；正文已逐篇读取。','内容与报价为自述，不等于成交；无完整费用清单及订单数据。',access='浏览器逐篇正文可读，留存内部AX文本')

prices.append(['耀悦','南澳大利亚及墨尔本','南澳探索鎏金双境 四人私享',49500,'CNY','人/次 起','笔记显示09-11','10晚11天；阶段行程与酒店描述','机票 单房差 签证及完整包含待核','4人成行；团期单独确认',U,'账号正文报价 非成交','X03-09',ASOF])
prices.append(['耀悦','南极','A21麦哲伦探索号海空联航',119000,'CNY','人/次','笔记显示10-09','7晚8天；南极海空方案','国际交通 舱房 单房差等待核','船载客量不是本品牌成团人数',U,'账号正文报价 非成交','X03-03',ASOF])
prices.append(['耀悦','津巴布韦 博茨瓦纳 南非','春节三国9天 报价异常',13800,'CNY','人/次','2027-01-18至02-28出发窗口','正文列9天及多项高奢资源','完整费用待核','原文1.38万元与资源组合待核，不纳入价格锚',U,'异常 待书面核实','X03-01',ASOF])
events[4]=['E05','耀悦','南澳探索鎏金双境','笔记09-11 团期未定','南澳及墨尔本','公开招募产品正文','4人私享同行',11,49500,U,'1—4日墨尔本；5日列车；6—7日阿德；8—9日营地；10日自由；11日返程','X03-09','阶段行程，不证明出团或到场']
events[5]=['E06','耀悦','A21南极海空联航','笔记10-09 团期未定','南极','公开招募产品正文','主题旅行人群',8,119000,U,'以飞机串联南极半岛与邮轮；详细日程和集合待核','X03-03','产品设计；船载客量不能当品牌用户量']
flows=[r for r in flows if r[0] not in ['E05','E06']]
for e in events[4:]:
    for stage in stages:
        value=U
        if stage=='活动设计':value=f'{e[2]} {e[7]}天 报价{e[8]}元/人；费用包含待核'
        if stage=='主体环节':value=e[10]
        flows.append([e[0],e[1],e[2],stage,value,'品牌产品设计，非实际体验；不补造SOP',e[11]])
for row in metrics:
    if row[0]=='耀悦' and row[1]=='粉丝数':row[2]='9507';row[3]='单一账号采集快照，非品牌去重粉丝和会员';row[4]='X03'
for row in field_rows:
    if row[0]=='耀悦':
        upd={
        '旅行价格':('南澳49500元/人起；南极119000元/人；异常1.38万元另列','X03-09 X03-03 X03-01'),
        '旅行天数':('南澳11天；南极8天；原官网示例另列','X03-09 X03-03 S33'),
        '旅行人数':('南澳4人私享；不是实际成交人数','X03-09'),
        '住宿标准':('南澳含丽思卡尔顿与野奢营地等描述，房型清单待核','X03-09'),
        '公开渠道':('官网、微信顾问；小红书品牌自述账号可访问','S33 X03'),
        '内容主题':('20篇逐篇内容覆盖目的地 科考 假期 选购与优惠','X03-01至20'),
        '粉丝数':('9507 单一账号快照 2026-10-21','X03'),
        '主题与地点':('南澳11天与南极8天招募产品，非实际活动','X03-09 X03-03'),
        '时长及人数':('南澳11天4人私享；南极8天品牌人数未知','X03-09 X03-03'),
        '主体环节':('南澳有分阶段行程；南极有海空联航方案','X03-09 X03-03')}
        if row[2] in upd:row[3],row[4]=upd[row[2]];row[5]='已找到部分证据'
for row in acquisition:
    if row[0]=='耀悦':row[1]='官网 服务号 微信顾问 小红书品牌自述账号';row[-1]='S33 X03'
gaps.append(['G15','价格','非洲9天1.38万元异常','品牌笔记价格与资源叙述需书面确认','当前团期费用包含书面报价','不作为低价锚，不擅自修改为13.8万','待后续核实'])

# 当前公开文本与索引访问方式保留差异，不用HTTP200推定正文完整。
for s in sources:
    if s['id']=='S33':s['access']='官方站桌面文本成功留存；移动版动态显示不足';s['limit']='首页团期未标，完整包含未得；新笔记报价单列，不作为直接调价证据。'
    if s['id']=='S36':s['access']='完整PDF已下载并检索关联投资表';s['finding']='耀悦关联投资见年度报告127—128及203—204印刷页；不将权益法投资收益视为品牌营业收入。'
    if s['id']=='S10':s['access']='贝恩原始PDF完整下载并提取'

data=dict(asof=ASOF,sources=sources,institutions=institutions,macro=macro,prices=prices,comparisons=comparisons,products=products,personas=personas,acquisition=acquisition,events=events,flows=flows,metrics=metrics,gaps=gaps,fields=field_rows,notes=notes)
(ROOT/'research/data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
print({k:len(v) for k,v in data.items() if isinstance(v,list)})
