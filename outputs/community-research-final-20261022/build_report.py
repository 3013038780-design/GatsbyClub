from pathlib import Path
from copy import deepcopy
import json,re
from io import BytesIO
from docx import Document
from docx.shared import Pt,Cm,RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT
B=Path(__file__).parent;data=json.loads((B/'修订研究数据.json').read_text());S=data['sources'];d=Document();old=Document(B.parent/'matchmaking-review-20261022/交付文件/中国高端会员社群市场研究及创业可行性评估报告.docx')
sec=d.sections[0];sec.page_height=Cm(29.7);sec.page_width=Cm(21);sec.top_margin=Cm(2);sec.bottom_margin=Cm(1.9);sec.left_margin=Cm(2.2);sec.right_margin=Cm(2.2)
for name,size,font in [('Normal',11,'Songti SC'),('Title',24,'Heiti SC'),('Heading 1',17,'Heiti SC'),('Heading 2',14,'Heiti SC'),('Heading 3',12,'Heiti SC')]:
 st=d.styles[name];st.font.name=font;st.font.size=Pt(size);st.font.color.rgb=RGBColor.from_string('000000');st.element.get_or_add_rPr().rFonts.set(qn('w:eastAsia'),font);st.paragraph_format.line_spacing=Pt(18);st.paragraph_format.space_after=Pt(7)
def p(s,style=None):return d.add_paragraph(s,style)
def h(s,lev=1):
 q=d.add_heading(s,lev);q.paragraph_format.keep_with_next=True
 if lev==1:q.paragraph_format.page_break_before=True
 return q
def link(q,label,url):
 a=OxmlElement('w:hyperlink');a.set(qn('r:id'),q.part.relate_to(url,RT.HYPERLINK,is_external=True));r=OxmlElement('w:r');pr=OxmlElement('w:rPr');c=OxmlElement('w:color');c.set(qn('w:val'),'255878');pr.append(c);r.append(pr);t=OxmlElement('w:t');t.text=label;r.append(t);a.append(r);q._p.append(a)
def refs(keys):
 q=p('资料：');q.paragraph_format.line_spacing=Pt(13)
 for k in keys.split('/'):
  if k in S:link(q,k+' '+S[k][0]+'  ',S[k][1])
 for r in q.runs:r.font.size=Pt(9)
def table(head,rows,widths):
 t=d.add_table(rows=1,cols=len(head));t.autofit=False
 for c,w in zip(t.columns,widths):c.width=Cm(w)
 for c,v in zip(t.rows[0].cells,head):c.text=str(v)
 for rr in rows:
  for c,v in zip(t.add_row().cells,rr):c.text=str(v if v is not None else '未取得当期报价')
 for i,row in enumerate(t.rows):
  pr=row._tr.get_or_add_trPr();pr.append(OxmlElement('w:cantSplit'))
  if i==0:pr.append(OxmlElement('w:tblHeader'))
  for j,c in enumerate(row.cells):
   c.width=Cm(widths[j]);sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'E8EDF1' if i==0 else ('F6F8FA' if i%2==0 else 'FFFFFF'));c._tc.get_or_add_tcPr().append(sh)
   for q in c.paragraphs:
    q.paragraph_format.line_spacing=Pt(15);q.paragraph_format.space_after=Pt(5)
    for r in q.runs:r.font.size=Pt(10);r.bold=i==0
 p('');return t
def txt(el):return ''.join(x.text or '' for x in el.iter(qn('w:t')))
def copyrange(start,end):
 active=False
 for el in old.element.body:
  if txt(el)==end:break
  if txt(el)==start:active=True
  if active:
   ee=deepcopy(el)
   for hl in ee.iter(qn('w:hyperlink')):
    rid=hl.get(qn('r:id'))
    if rid and rid in old.part.rels:
     rel=old.part.rels[rid]
     if rel.is_external:hl.set(qn('r:id'),d.part.relate_to(rel.target_ref,RT.HYPERLINK,is_external=True))
   for blip in ee.iter(qn('a:blip')):
    rid=blip.get(qn('r:embed'))
    if rid and rid in old.part.rels:
     newrid,_=d.part.get_or_add_image(BytesIO(old.part.rels[rid].target_part.blob));blip.set(qn('r:embed'),newrid)
   d.element.body.insert(len(d.element.body)-1,ee)
# Header and page fields
foot=sec.footer.paragraphs[0];foot.alignment=2;foot.add_run('内部讨论资料  |  ');f=OxmlElement('w:fldSimple');f.set(qn('w:instr'),'PAGE');foot._p.append(f)
p('中国高端会员社群市场研究报告','Title');p('收费方式 客户分层 组织模式与创业选择','Subtitle');p('合伙人讨论版\n2026年10月22日')
p('本报告服务于一家面向高资产客户的社群创业决策，覆盖婚恋、日常社交、学习、参访与旅行。修订重点是把收费拆到具体产品，把客户拆到具体使用场景，并重新评估互联网婚恋模式。')
p('建议优先研究大超说媒和HIMMR的单身产品，再借鉴马会的家庭及消费分层、长江的固定同学关系、木兰汇的女性经营者定位。青藤和牵手用于研究产品收费与匹配工具。七家分别解决不同经营问题，不作跨行业营收排名。')
p('本轮新增核查截至2026年10月22日；内容观察窗为7月25日至10月22日。抖音取得14条带日期及互动的可核验样本。小红书出现设备登录限制，本轮未取得新增指标；不能写作三平台完整90天采集。')
h('一 合伙人先讨论的四个问题')
for tx in ['主产品卖什么。会籍、活动票、顾问工时、牵线次数和旅行行程应分别定价，不能只说一个年费包所有服务。','首批客户是谁。企业经营者、受雇专业人士、年轻家庭成员、单身与已婚客户需要分别判断；先选能持续获得且能交付的一组。','客户为什么再来。单次看稀缺资源，长期看固定同伴、持续内容和实际服务，后者决定是否值得设年费。','哪些收入值得做。先算每场活动扣除供应商与执行工时后的贡献，再算会员服务及获客成本；公开粉丝、累计注册或年会票价不能直接填入利润模型。']:p(tx)
table(['建议优先级','对象及用途'],[['直接研究','大超说媒、HIMMR：单身客户如何筛选、报名、见面、再购买'],['组织借鉴','北京马会、长江商学院、木兰汇：家庭、固定班级、女性经营者的持续关系'],['产品借鉴','青藤之恋含恋爱主理人、牵手：付费动作、功能边界及线上到见面']],[3.5,13.1])
# Preserve macro facts and institutional taxonomy with original hyperlinks and periods.
copyrange('二 市场与客户需求','3.2 六家对标对象及其用途')
h('3.2 本轮重点对象如何选择',2)
p('我主良缘、金凤凰深港婚恋、珍爱网保留在35家机构名录及历史证据中，不再占据本轮深度婚恋样本。原因是当期收费、近90天交付及实际付费客户证据不足，不能靠旧合同报道支撑当前经营判断。正和岛、优家荟已删除。EO仅作固定小组的专项参考。')
for c in data['cases']:
 h(c[0],2);p(c[1]+'。'+c[2]+'。');p(c[4]);p('经营证据：'+c[3]);
 if c[5]:refs(c[5])
h('四 收费和客户必须放在一起看')
p('以下按产品拆分客户。年龄分布、收入中位数、客户性格等，只有客户调查或可核验样本才能回答；公开页面未披露的字段直接保留缺口。不能用“金融从业者”推出年薪，也不能用愿意付费推出家产。下面的需求描述来自产品用途，不冒充实际买家统计。')
for brand in ['大超说媒','陌上花开HIMMR','青藤之恋','青藤之恋／恋爱主理人','牵手']:
 h(brand,2)
 ps=[x for x in data['products'] if x['brand']==brand]
 if brand=='大超说媒':p('它先用真人出镜讨论择偶、学历、资产与关系问题，再导向咨询、主题相亲和私人定制。五种产品面对的人不同：想厘清择偶要求的人、愿意向主理人付溢价的人、接受学历筛选的人、主动寻找高净值对象的人，以及愿意交给顾问持续推进的人。')
 elif brand=='陌上花开HIMMR':p('更具体地说，它把985／211、海外名校背景的人放进同一个认识异性的渠道，官网直接提到金融、互联网和高校行业。线上自己找、参加同城活动、交给红娘三条路径，对应不同时间投入和隐私需求。官网展示的医生、工程师、教授或摄影爱好者属于个人展示样本，不能扩大成买家职业比例。')
 elif brand=='青藤之恋':p('它面对希望认真恋爱的年轻用户，开发者特别点名名校毕业生、互联网从业者和体制内青年。订阅、精选推荐、曝光和虚拟币解决的是不同动作。现有公开商品还不能回答198元与568元分别买多久，报告不把这些价格改写成年费。')
 elif brand=='青藤之恋／恋爱主理人':p('这是青藤同一开发者的新产品，不另算一家机构。它替客户梳理条件、找人、传话和推进交流。客户买的是牵线次数，而不是包结婚、包见面或人工顾问无限服务。')
 else:p('牵手让用户按条件、观念、性格和生活爱好找人，再选择约会活动。VIP解决增加推荐及信息效率，“看谁喜欢我”解决反向筛选；两项各付一次。摄影、徒步、探店等是平台提供的兴趣或约会入口，不是已验证的全体付费用户爱好。')
 table(['具体产品','金额及收费单位','包含与边界'],[[x['product'],('未取得现价' if x['price'] is None else f"{x['price']:,}元")+'／'+x['unit'],x['rights']] for x in ps],[3.4,4.4,8.8])
 # Avoid repeating identical group descriptions for every SKU.
 seen=set();profile=[]
 for x in ps:
  if x['people'] in seen:continue
  seen.add(x['people']);profile.append([x['product'],x['people']])
 table(['对应产品或客群','已核实的客户条件与需求'],profile,[4.2,12.4])
 p('画像证据缺口：未取得这些产品实际付费客户的年龄分布、职业占比、年收入或资产分布，以及性格和兴趣调查。上述描述为品牌定位、报名条件或产品适用需求，不作为实际客户统计。')
 refs('/'.join(dict.fromkeys(k for x in ps for k in x['source'].split('/'))))
 if brand=='牵手':
  p('实际支出例子：同时订阅两项，按月60＋88＝148元；三个月138＋188＝326元；十二个月388＋488＝876元。上述合计不含虚拟道具。协议把月、季、年分别定义为31、93、372天；购买时付费，订阅到期前24小时自动续扣。')
 if brand=='青藤之恋／恋爱主理人':p('按当前套餐测算，每次分别99元、约79.67元、73.80元；5次套餐相对5次单购少126元。三天未牵上线退的是次数，不能写成现金退款。')
h('五 三类持续会员组织的完整案例')
p('以下保留前轮已经核验的会籍、课程、年会与实际活动资料，各条按自身日期使用。北京内地会籍与香港会籍仍分开，不把公司持有方式当作另一家机构。')
copyrange('4.1 北京香港马会会所','4.4 我主良缘')
h('六 获客 活动交付与经营表现')
h('6.1 大超的传播和成交入口',2)
p('主号03本轮观察为24万粉丝、1019.1万累计获赞、212个作品；05号为7.2万粉丝、166.1万累计获赞、337个作品。两个账号分别列数，未对品牌受众去重。看到观点视频的人先形成对主理人的信任，再通过主页、群聊入口或活动招募进入咨询和报名。实际咨询人数、活动付费及私定成交未公开。')
p('14条已核验视频中，深圳招募内容有3820赞、559评论、6639分享，分享明显高于点赞，说明活动招募本身也能被大量转发。另一条饮食与社交观点有8881评论，争论量很高，却没有相应成交证据。两类内容应分别评估：招募看咨询和报名，观点看触达及信任，不能都用评论量判断生意。')
refs('D01/D02')
h('6.2 其他三家的交付路径',2)
table(['对象','可见路径','经营数据到哪一步'],[['HIMMR','资料与认证→推荐或兴趣活动→自愿申请1V1→红娘推荐与复盘','官网称百万级用户、8城、每年500+活动及累计10万+参与；未标统计期，不能写成近90天实绩'],['青藤及恋爱主理人','标签与测试→推荐→互相喜欢后交流；AI产品再增加牵线及传话','青藤累计5000万注册为开发者自述；恋爱主理人仅4个iOS评分，不能沿用母产品规模'],['牵手','偏好及标签→推荐→选择散步／展览／咖啡→发出邀约','iOS约54万评分4.4；没有现行有效付费、MAU或续费的可靠披露']],[2.9,7.4,6.3])
refs('H01/Q01/Q02/T01/T03')
h('6.3 流程证据需要落实到场次',2)
p('10月18日大超公开视频能证明有实际相亲聚会，暂不写完整时长、轮换规则和实到人数。HIMMR官网展示多种活动形式，但未取得观察窗内两场完整招募与回顾配对资料。牵手的智能约会是产品路径，不能写成主办方组织了场活动。近90天活动明细和状态在Excel单独列出。')
h('七 婚恋与旅行的具体产品')
p('本轮找到两种近期报价：单身户外一日活动138元，以及温泉婚恋两天一夜388元。它们是产品设计的补充案例，组织方规模和A8客户基础尚无可靠证据，暂不升级为重点高端品牌。')
for a in data['activities'][3:]:
 h(a[0]+' '+a[3],2);p('日期与状态：'+a[1]+'，'+a[2]+'。收费'+str(a[4])+'元／人。');p('公开安排：'+a[5]+'。');p('客户条件与费用：'+a[6]+'。');q=p('活动原文：');link(q,'查看招募说明',a[7])
p('玉渡山场次招募还明确：不含餐、自带野餐，活动前一天12点前可全退，之后不退且不可延期。它把认识异性的机会嵌入交通、分组、午餐、游园与返程。对新公司最值得学习的是每一段如何帮助成员自然接触，而不是把普通行程加上“高端相亲”名称。')
p('青藤的七夕文创合作和大超的香港生活内容，都不足以认定已经形成收费旅行产品。牵手的徒步、展览与咖啡约会也是同城见面入口，与带队多日旅行分开比较。')
h('八 我们应该卖给谁 怎样验证')
p('先把潜在客户分成以下产品线，再做真实客户调查。这里是本公司待验证的客户假设，不是竞品已有客户统计。每条线要取得年龄分布、岗位、可自主支配预算和付费理由后，才决定是否推出。')
table(['拟服务客户','具体购买理由','应验证的个人信息与付费'],[['单身企业经营者','需要可信的人选、隐私和时间安排；有可能购买小范围活动或顾问服务','实岁、婚史及子女、经营岗位、收入与流动资产口径、当年婚恋预算；愿意付哪一项'],['单身专业人士','收入可能较高但圈子窄，先看教育和生活方式是否相近','城市、行业岗位、工作时间、年龄偏好；不要把高学历直接当A8'],['有伴侣或已婚经营者及配偶','共同旅行、朋友关系、学习及家庭休闲；不进入单身匹配','谁决定与付款、两人时间、子女年龄、是否独立参加、家庭卡使用及活动频次'],['年轻家庭成员','共同兴趣、同龄朋友、家庭资源之外的独立社交','本人年龄工作、资金来源、可自主预算、是否真愿持续参加；与家长需求分开']],[3.5,6.2,6.9])
p('性格不能只记MBTI。访谈要问最近一次陌生人聚会中的实际行为：是否主动开口、愿不愿被主持人点名、偏好几人聊天、是否接受公开展示、何种交流会不舒服。爱好要记过去三个月实际参加次数与消费，而不是只勾选“高尔夫、旅行、艺术”。收入记录税前或税后、个人或家庭；资产记录净资产或可投资资产，得到同意后再收集。')
p('试点建议：先做一个清晰客群的收费同城活动，再测试同一批人的第二次购买；有稳定重复参与后测试两日旅行。顾问匹配另签服务内容和收费，伴侣与已婚客户另设生活活动。首期不同时承诺六项无限服务。')
p('合伙人绩效先看：合格申请、付费报名、实到、第二次付款、每场贡献、每位服务工时与退款。暂不设缺少样本支撑的行业转化目标；先用两场真实收费活动建立基线。')
h('附录 资料与数据口径')
p('Excel共6张表：重点判断、收费与客群、活动与旅行、近90天内容、市场与机构、资料来源。包含35家名录、47条产品收费与客群记录、14条新增可核验内容。旧28张表的所有明细另存CSV，保留原期与核验状态，不与当前事实混排。')
p('未采纳的现行经营结论包括：以2011年等旧报道代表今天；以2024活动票价代替2026现价；统计截止显示0001年的第三方账号汇总；无法获得原报告的方法不明MAU；把旅游预告写成实际成行。有效付费、转化、续费和利润未取得可靠披露时留缺口，判断仍按已见到的产品、活动和价格展开。')
for k,v in S.items():
 q=p(k+' '+v[0]+'\n'+v[2]+'；'+v[3]+'。 ');link(q,'打开原文',v[1])
# Ensure copied heading hierarchy clean without stale main counts.
for q in d.paragraphs:
 if q.style.name.startswith('Heading') and re.match(r'4\.[123] ',q.text):q.text=re.sub(r'^4\.([123]) ',r'5.\1 ',q.text)
for stname in ['Title','Subtitle']:
 st=d.styles[stname];pr=st.element.find(qn('w:pPr'))
 if pr is not None:
  for border in list(pr.findall(qn('w:pBdr'))):pr.remove(border)
 st.font.color.rgb=RGBColor.from_string('000000')
for q in d.paragraphs:
 pr=q._p.find(qn('w:pPr'))
 if pr is not None:
  for border in list(pr.findall(qn('w:pBdr'))):pr.remove(border)
d.save(B/'交付文件/中国高端会员社群市场研究报告.docx')
print('saved')
