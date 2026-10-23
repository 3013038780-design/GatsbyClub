"""Verify selected facts against this batch's retained text and retain source context."""
from pathlib import Path
from html.parser import HTMLParser
import csv,json,re
ROOT=Path(__file__).resolve().parents[1]/'collection-20261021'
data=json.loads((ROOT/'collection.json').read_text())
class Links(HTMLParser):
 def __init__(self):super().__init__();self.rows=[];self.href=None;self.buf=[]
 def handle_starttag(self,tag,attrs):
  if tag=='a':self.href=dict(attrs).get('href');self.buf=[]
 def handle_data(self,s):
  if self.href:self.buf.append(s)
 def handle_endtag(self,tag):
  if tag=='a' and self.href:self.rows.append((self.href,''.join(self.buf).strip()));self.href=None
from urllib.parse import urljoin,urldefrag
rx=re.compile(r'活动|会籍|会员|校友|参访|赛事|年会|沙龙|之旅|品鉴|晚宴|艺术|高尔夫|membership|events',re.I)
existing={(r['机构'],r['详情网址']) for r in data['activity_links']}
for p in data['pages']:
 if p['状态']!='已采集' or not p['原文文件'].endswith('.md'):continue
 parser=Links();parser.feed((ROOT/p['原文文件']).with_suffix('.html').read_text())
 for href,title in parser.rows:
  url=urldefrag(urljoin(p['网址'],href))[0]
  if not rx.search(title) or not url.startswith('http') or len(title)>300:continue
  if (p['机构'],url) in existing:continue
  if re.search(r'登录|注册|隐私|login|privacy',title,re.I):continue
  existing.add((p['机构'],url));data['activity_links'].append(dict(机构=p['机构'],链接标题=title,详情网址=url,发现页=p['网址'],采集时间=data['collected_at'],状态='官网链接线索，尚未判断已举办'))
facts=[]
def add(brand,url,field,value,unit,description,pattern,time):
 for p in data['pages']:
  if p['网址']!=url or p['状态']!='已采集':continue
  path=ROOT/p['原文文件'];txt=(path.with_suffix('.txt') if path.suffix=='.pdf' else path).read_text()
  m=re.search(pattern,txt,re.S|re.I)
  if not m:return
  snippet=re.sub(r'\s+',' ',txt[max(0,m.start()-65):m.end()+120])
  page=''
  if path.suffix=='.pdf':
   before=txt[:m.start()];marks=re.findall(r'--- PDF第(\d+)页 ---',before);page=marks[-1] if marks else ''
  facts.append(dict(机构=brand,模块=field,数值=value,单位=unit,事实与适用条件=description,资料时间=time,来源=url,PDF页码=page,核对原文=snippet,采集时间=data['collected_at']))
  return
ck='https://www.ckgsb.com/emba/common_problems/'
add('长江商学院',ck,'价格',998000,'元/项目','2026年EMBA学费',r'2026年学费.{0,40}998,000','2026年')
add('长江商学院',ck,'价格',2000,'元/次','EMBA申请费，面试当天缴纳',r'申请费.{0,30}2,000','当前页面')
hk='https://member.hkjc.com/ecard/eHarmony_Jun25.pdf'
add('北京香港马会会所',hk,'价格',600000,'元/个人会籍入会费','个人入会费；2025年6月刊转述2024年生效标准',r'个人会籍.{0,35}60\s*万','2025年6月刊；2024-01-01生效')
add('北京香港马会会所',hk,'价格',1800000,'元/公司甲类入会费','公司甲类入会费，同段另列乙类130万元、丙类70万元',r'180\s*万.{0,80}130\s*万.{0,80}70\s*万','2025年6月刊；2024-01-01生效')
add('北京香港马会会所',hk,'价格',1300000,'元/公司乙类入会费','公司乙类入会费',r'180\s*万.{0,80}130\s*万.{0,80}70\s*万','2025年6月刊；2024-01-01生效')
add('北京香港马会会所',hk,'价格',700000,'元/公司丙类入会费','公司丙类入会费',r'180\s*万.{0,80}130\s*万.{0,80}70\s*万','2025年6月刊；2024-01-01生效')
url='https://www.tpc.com.cn/membership'
add('黑骑士球员俱乐部',url,'产品',4,'类会籍','钻石、黑钻石、居住、社交会籍',r'四类不同会籍.{0,200}社交会籍','页面未标生效日期')
add('黑骑士球员俱乐部','https://www.tpc.com.cn/abouttheplayersclub','设施',27,'洞','官网介绍的高尔夫球场洞数',r'27个锦标赛高尔夫球洞','页面未标统计日期')
eo='https://member.eonetwork.org/chinaeast/about-our-chapter/'
add('EO中国',eo,'会员规模',109,'名','EO China East分会页面会员数',r'109\s+Members','分会页面当前口径')
add('EO中国',eo,'价格',2630,'美元/年','EO全球年费，地方分会收费另查',r'2630\.00','分会页面当前口径')
add('EO中国',eo,'价格',3500,'美元/次','EO新会员一次性全球入会费',r'3500\.00','分会页面当前口径')
ph='https://edp.phbs.pku.edu.cn/info/1271/13221.htm'
add('北大汇丰EDP',ph,'活动参与',16,'支队伍','征戈会六周年庆暨第三届班际驿传参赛队伍',r'16支队伍','2026-03-07活动')
add('北大汇丰EDP',ph,'活动组织',25,'人','本次赛事筹备委员会人数',r'25人的筹备委员会','2026-03-07活动')
add('北大汇丰EDP',ph,'活动流程',6,'人/队','团体组每队6名队员，至少1名女队员；并设亲子组',r'每支队伍6名队员且至少含1名女队员','2026-03-07活动')
add('北大汇丰EDP',ph,'活动流程',3,'小时','团体组采用3小时不间断接力跑',r'3小时不间断接力跑','2026-03-07活动')
mul='https://www.iceo.com.cn/zt/2026_mulannh/'
add('木兰汇',mul,'成员规模',1000,'位左右','官方表述为近1000位成员',r'近\s*1000\s*位成员','2026年年会资料')
add('木兰汇',mul,'客群',112,'位','企业市值或估值20亿元以上的核心成员',r'核心成员\s*112\s*位','2026年年会资料')
data['verified_facts']=facts
(ROOT/'collection.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def csvout(name,rows):
 if not rows:return
 with (ROOT/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
csvout('已核对价格与运营数据.csv',facts);csvout('活动与会籍链接清单.csv',data['activity_links'])
summary=json.loads((ROOT/'summary.json').read_text())
for r in summary:r['活动会籍链接数']=sum(x['机构']==r['机构'] for x in data['activity_links'])
(ROOT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8');csvout('机构采集覆盖.csv',summary)
print(json.dumps({'verified_facts':len(facts),'activity_links':len(data['activity_links']),'facts':facts},ensure_ascii=False))
