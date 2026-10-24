from pathlib import Path
import json
from docx import Document
from docx.shared import Pt,Cm,RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
B=Path(__file__).parent;R=B.parents[1];D=json.loads((R/'outputs/integrated-research-20261024/统一研究数据.json').read_text());F=json.loads((B/'执行依据与测算数据.json').read_text());O=B/'交付文件';O.mkdir(exist_ok=True)
d=Document();sec=d.sections[0];sec.top_margin=Cm(2);sec.bottom_margin=Cm(2);sec.left_margin=Cm(2.2);sec.right_margin=Cm(2.2);sec.page_width=Cm(21);sec.page_height=Cm(29.7)
for name,size,bold in [('Normal',11.5,False),('Title',22,True),('Heading 1',17,True),('Heading 2',13,True)]:
 st=d.styles[name];st.font.name='Source Han Serif CN';st.font.size=Pt(size);st.font.bold=bold;st.font.color.rgb=RGBColor(0,0,0);st.paragraph_format.line_spacing=Pt(19);st.paragraph_format.space_after=Pt(8)
 fonts=st.element.get_or_add_rPr().get_or_add_rFonts()
 for old in list(fonts.attrib):del fonts.attrib[old]
 for edge in st.element.xpath('.//w:pBdr'):edge.getparent().remove(edge)
 for k in ['ascii','hAnsi','eastAsia','cs']:fonts.set(qn('w:'+k),'Source Han Serif CN')
 if name=='Title':st.paragraph_format.line_spacing=Pt(30)
 if name.startswith('Heading'):st.paragraph_format.space_before=Pt(10);st.paragraph_format.keep_with_next=True
foot=sec.footer.paragraphs[0];foot.alignment=2;foot.add_run('合伙人会议讲解稿  ').font.size=Pt(9);field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');foot._p.append(field)
def p(t):d.add_paragraph(t)
def h(t):d.add_paragraph(t,'Heading 2')
def link(label,url):
 q=d.add_paragraph();q.paragraph_format.line_spacing=Pt(13);z=OxmlElement('w:hyperlink');z.set(qn('r:id'),q.part.relate_to(url,'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink',is_external=True));run=OxmlElement('w:r');prop=OxmlElement('w:rPr');col=OxmlElement('w:color');col.set(qn('w:val'),'255878');prop.append(col);size=OxmlElement('w:sz');size.set(qn('w:val'),'18');prop.append(size);run.append(prop);text=OxmlElement('w:t');text.text=label;run.append(text);z.append(run);q._p.append(z)
d.add_paragraph('高端线下社群合伙人会议讲解稿','Title');p('2026年10月24日  配合正式报告及总Excel使用')
d.add_paragraph('第一部分 市场调研','Heading 1')
h('先把我们做什么说清楚')
p('我们要围绕同一批A8及以上客户，长期组织线下活动。商业活动让经营者与专业人士交流，婚恋专场让真实单身者认识彼此，旅行提供更长的共同体验。今天讨论的是客户和服务的组合，不急着决定年费、首发城市或一个固定年龄带。个人还是家庭资产口径，也要明确。')
h('市场数据告诉了我们什么')
p('胡润报告估算内地亿元总资产家庭10.6万户，这是家庭口径。网经社估计2025年互联网婚恋市场103.5亿元、同比增长5.61%，是互联网口径。前者说明财富人群基础，后者提供婚恋付费市场背景；目前没有足够同口径收入数据计算线下高端社群前五份额。')
p('供给已经分成多种收费：会籍、活动席位、顾问定制、旅行团费和住宿升级。我们先比较客户究竟买到什么。每一类市场都保留成熟机构与小团队形式，不能把学费、年会票和会所入会费放在一起平均。')
h('这轮新增检索有什么用')
p('商业与婚恋追加157条搜索记录、154篇去重内容、9篇正文及5个账号主页。Pitch有较大内容声量，但当前会籍价和A8客群证据未齐；近佚公布98／118元桌游票，适合比较学历与年龄筛选、换桌和主持；崎悦提供了两天一夜的婚恋旅行形式线索，但完整团费和承办尚需核实。它们进入资料库，不因为新发现就替换现有主对标。')
link('市场规模原始发布',next(s['url']for s in D['sources']if s['id']=='E01'))
q=d.add_paragraph('第二部分 对标','Heading 1');q.paragraph_format.page_break_before=True
h('这五个品牌分别向谁学')
for t in ['BoL商务会籍：学同一品牌怎样安排酒会、沙龙、运动与另付私宴。488／2888元是年费层级，私宴单独收费。','BoL Selected：学单身审核和半天交付。该场展示1688元，顺序为手作茶叙、主持互动、晚宴和互选；用户补充截图已确认准入与流程；最终会员价仍缺结算规格证据，1288元位于价值栏。','钻石婚恋：学高资产筛选和服务深度。30万、60万、100万起是定制项目费；有顾问和猎头分工、约会辅导及关系巩固。我们尚不能照搬它的资源库和高价服务。','Founder Feast：学五人餐桌、人工筛选、订阅与餐费分账。温哥华39.99加元月费，餐酒另结；没有足够经营披露把它评为成功样板。','奇语与Other Way Round：前者学小团内容和目的地产品，后者学年龄带、行前问卷、建立同行群、定金尾款及独住升级。旅行供应与婚恋审核由不同能力承担。']:p(t)
h('先讨论两件事')
p('第一批具体邀请谁，他们为什么第一次付款？要把经营身份、生活阶段、关系意愿、活动主题和同行条件连起来。第二，什么体验会使他们再来？讨论固定小组、持续主题和共同经历，比先承诺全年多少场更有用。')
h('费用模型只作初案附件')
p('1680／680／19800元仍是研究试价。三亚四天三晚沿用11月19—22日作成本比较，瑞吉含早单人单房三晚官方含税零售价7870元；不是整团协议报价。按14位客人、3位工作人员及当前预算，旅行单团贡献35104元、周转需求141296元。成本变化应在模型中讨论，不据此认定客户已经愿付或公司已经盈利。')
p('下一步由Olivia取得同条件供应商报价和客户真实消费反馈，格格核实具体合作资源。当前没有确认供应商、访谈结论及团体报价。先对齐客群、产品和验证预算，再确定对外价格。')
link('钻石定制服务与分层报价',next(s['url']for s in D['sources']if s['id']=='C01'))
link('Founder Feast现行收费',next(s['url']for s in D['sources']if s['id']=='C03'))
out=O/'高端线下社群合伙人会议讲解稿.docx';d.save(out);print(out)
