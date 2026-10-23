from pathlib import Path
import asyncio,html,json,zipfile,sys,re
from playwright.async_api import async_playwright

O=Path(__file__).resolve().parent
MEM='https://members.hkjc.com/about-membership/zh-HK/Membership?b_cid=SPLDSPA_hkjc-home_Footer'
RATE='https://member.hkjc.com/-/media/Sites/JCEW/member/image/common/Rate_Card.pdf'
FAM='https://members.hkjc.com/about-membership/zh-HK/membership-cards-and-signing-rights?tags=types-of-children-card'
FAQ='https://www.hkjc.com/en-us/faq/membership/privileges'
FORM='https://members.hkjc.com/-/media/Sites/JCEW/member/common/forms/MS_APP_003_TC.pdf'
GUIDE='https://mem.racingclub.hkjc.com/common/pdf/TheRacingClubMembersGuideS2526.pdf'
BJ='https://www.beijingclubhouse.com/zh-HK/rulesandregulations.aspx'
BJC='https://www.beijingclubhouse.com/zh-HK/images/membership/Application_Form_for_Children_Supplementary_Card.pdf'
BJS='https://www.beijingclubhouse.com/zh-hk/images/membership/Application_Form_for_Spouse_Supplementary_Card.pdf'
def bullets(xs):return '<ul>'+''.join('<li>'+x+'</li>'for x in xs)+'</ul>'
def card(tag,title,fee,monthly,items,foot=''):
 return f'<section class="card"><div class="tag">{tag}</div><h2>{title}</h2><div class="fee">{fee}</div><div class="monthly">{monthly}</div>{bullets(items)}'+(f'<div class="cardfoot">{foot}</div>'if foot else '')+'</section>'
def box(title,text):return f'<section class="box"><h3>{title}</h3><p>{text}</p></section>'
figs=[]
figs.append(dict(file='01_香港个人会籍权益',title='香港个人会籍：多付的钱换来什么',subtitle='按使用范围与参与方式分产品；入会费与月费分别收取。金额均为港元。',body='<div class="grid">'+
card('赛马与观赛','赛马会员','21万元','月费 1,050元',[
'使用跑马地、沙田马场会员区及会员厢房；可购买来宾入场证章。',
'可申请成为马主；买马、养马及相关审批另行办理。',
'沙田会所餐饮可于赛马日首场开跑前2小时至末场后半小时使用，另有每日7—11时银袋咖啡室权限。',
'可互惠使用北京会所及深圳马会骏心台；非赛马日另可使用指定马场餐厅。',
'可另购沙田、双鱼河会所年度特许计划，增加会所使用范围。',
'可为配偶及8—21岁未婚子女申请附属卡。'], '子女卡60元／人／年；家属使用范围随主会籍。')+
card('日常会所与家庭生活','全费会员','105万元','月费 3,150元',[
'包含赛马会员权益，并全面开放跑马地、沙田、双鱼河会所设施。',
'可日常使用餐饮、泳池、健身、球类等设施，依各场所预约与年龄规则。',
'可通过互惠安排使用北京会所及深圳马会骏心台。',
'可申请配偶附属卡、子女附属卡；配偶另可申请独立全费（S）。'], '配偶附属卡免费；子女卡120元／人／年。')+
card('配偶自己的独立会籍','全费会员（S）','52.5万元','月费 1,050元',[
'申请对象：全费会员的合资格配偶。',
'独立会籍，享有与全费会员相同的权益。',
'按自己的会籍身份使用设施，单独缴纳入会费与月费。',
'配偶附属卡依附主会员账户；全费（S）则是另一份独立会籍。'], '两种配偶安排须分开：免费附属卡与付费独立会籍。')+
card('围绕赛马组织兴趣社群','竞骏会会员','11.1万／16.8万元','18—30岁／31岁及以上；月费均1,700元',[
'使用跑马地、沙田马场的竞骏会专属场地。',
'通过专属赛驹体验、马房探访、专家交流、国际赛马之旅参与社群。',
'可互惠使用北京会所并预订客房；双鱼河需另购特许计划，限周一至五。',
'另有体育、品牌及生活方式活动，按活动名额和费用报名。',
'每套赛马证章中，有一枚可转用证章供配偶或来宾使用。'], '年龄档对应同类会籍优惠；子女附属卡的专用规则本轮未取得。')+
'</div>'+box('赛马会员可另购的两项会所权限','沙田会所特许计划26,000元／12个月，限周一至五及所有赛马日；双鱼河23,000元／12个月，可周一至日使用，申请视名额而定。餐饮、课程、活动和其他消费按项目另结算。'),sources=[('会籍与设施范围',MEM),('现行收费表',RATE),('家庭附属卡',FAQ),('竞骏会指南第44—47页',GUIDE)]))

figs.append(dict(file='02_香港配偶子女权益',title='香港家庭权益：配偶和孩子怎样使用',subtitle='适用重点：赛马会员、全费会员及香港公司代表；竞骏会的家属安排另依其专用规则。',body=
'<div class="grid">'+
card('配偶路径 A','配偶附属卡','免费','依附主会员的会籍与账户',[
'主会员或香港公司代表可以为配偶申请。',
'可使用与主会籍相应的设施；需先办卡，并提交婚姻及身份资料。',
'附属卡消费记入主会员账户，由主会员承担。',
'申请附属卡本身，不会增加主会籍原本没有的设施权限。'])+
card('配偶路径 B','独立全费会员（S）','52.5万元','月费 1,050元；仅全费会员的合资格配偶',[
'取得自己的独立会籍。',
'权益与全费会员相同，包括完整会所使用范围。',
'入会费与月费单独收取，须经会籍审批。',
'可通过互惠安排使用北京会所与深圳马会骏心台。'])+
card('孩子以参加课程活动为主','子女身份识别卡 MCID','免费','0—21岁范围内，按到期规则使用',[
'用于识别子女身份及参加马会课程活动。',
'本身没有签账权；主会员可授权参加课程当日300港元消费额度。',
'是否授权及相应消费支出，由主会员决定并承担。',
'除参加马会课程活动外，使用设施须由成年会员陪同。'], 'MCID与子女附属卡不能同时持有。')+
card('孩子可在指定场所签账','子女附属卡','60元／120元','每名子女每年；赛马会员／全费及公司代表',[
'适用8—21岁未婚子女；21岁生日所在月份结束时到期。',
'基本权限：在指定餐饮、运动设施签账；各设施仍有年龄要求。',
'基本权限下不可带客、不接受餐厅预订；课程由父母代报名。',
'18—21岁可由主会员另申请会所延伸及／或马场签账权限。'], '费用为港元；家属消费由主会员承担。')+
'</div><div class="band"><h3>18—21岁另行授权后，多了什么？</h3><p>会所延伸权限：增加指定餐厅与设施，可自行报名课程，并在规定日子带客。马场签账权限：可不由主会员陪同，在赛马日指定场所订座、签账及带客。两项均需另申请，依适用年龄、场所与来宾规则执行。</p></div>',sources=[('免费配偶卡与子女年费',FAQ),('家庭卡、场所和权限细则',FAM),('2026附属卡申请表',FORM),('MCID及卡种官方说明','https://member.hkjc.com/member/english/about-membership/membership-cards-and-signing-rights/members-children-identity-card-faq.aspx/1000')]))

figs.append(dict(file='03_香港公司会籍权益',title='香港公司会籍：A与B差在代表任期',subtitle='两类均由公司持有会籍；每份会籍登记一位惯常居港的全职员工。金额均为港元。',body=
'<div class="grid">'+
card('代表定期更换','公司 A 类','300万元','月费 3,150元',[
'一份会籍登记1名公司代表。',
'每位代表的任期最长36个月，之后须登记另一名员工。',
'代表享有与个人全费会员同等的设施使用权益。',
'公司可依人员变动申请更换代表，登记与变更须获批准。'])+
card('同一代表可以持续使用','公司 B 类','520万元','月费 3,150元',[
'一份会籍同样登记1名公司代表。',
'同一代表没有A类的36个月任期上限。',
'代表可持续使用，直至公司更换或马会依规则移除。',
'设施使用权益与A类相同，价差主要对应代表任期安排。'])+
'</div><div class="grid three">'+
box('代表本人能用什么','马场会员区、会员餐饮与会所休闲设施；通过互惠安排使用北京会所及深圳马会骏心台。')+
box('代表的配偶与孩子','可申请配偶附属卡及8—21岁未婚子女卡。配偶卡免费，子女卡每人每年120港元；消费依附代表账户。')+
box('公司还可以做什么','可用企业身份申请指定宴会场地，举办员工周年派对、春茗等非商业性质的社交娱乐活动，须经马会批准。')+
'</div><div class="band"><h3>B类的价差，对应同一代表的使用期限</h3><p>B类入会费比A类多220万元；两类均登记1名代表，月费相同。购买决策主要取决于：是否希望同一位高管长期保留使用资格。</p></div>'+box('申请与使用边界','公司会籍为邀请制；香港公司A／B与内地公司甲／乙／丙是两套分类。企业场地使用按指定活动范围、审批与收费执行。'),sources=[('公司会籍、代表任期与家属',MEM),('现行收费表',RATE),('公司申请与审核说明','https://www.hkjc.com/en-us/faq/membership/corporate-member'),('配偶卡收费说明',FAQ)]))

figs.append(dict(file='04_内地会籍及家庭权益',title='内地会籍：人数、跨城与家庭权益',subtitle='这是北京香港马会会所会籍；四类主要使用范围相同，公司等级按登记代表人数区分。',body=
'<table><thead><tr><th>会籍</th><th>登记使用人</th><th>入会费／人民币</th><th>月费／人民币</th></tr></thead><tbody>'+''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{e}</td></tr>'for a,b,c,e in [('个人','个人会员本人','60万元','2,200元'),('公司丙类','1名公司代表','70万元','2,200元'),('公司乙类','2名公司代表','130万元','4,400元'),('公司甲类','3名公司代表','180万元','6,600元')])+'</tbody></table>'+
'<div class="grid">'+
box('四类共同的主要使用范围','北京会所及深圳马会骏心台；通过互惠安排使用香港部分指定会员设施。香港会所每自然年36天、每月最多7天；The Hilltop in The Valley不可于周末及香港公众假期使用。马场依公布规则全年使用。')+
box('配偶也可以使用','北京会所设配偶附属卡申请表。配偶可按会籍规则使用设施；申请需身份与关系资料。主会员承担配偶附属卡产生的消费与责任。配偶卡费未在所查申请表中列明。')+
box('孩子的卡与独自使用','8—21岁可申办子女附属卡，120元人民币／人／年。12—21岁另申请签账权后，可独自使用指定场所并签账；健身中心、高尔夫模拟室需14岁以上。12岁以下须由符合规则的成人全程陪同。')+
box('孩子具体能用什么','指定北京凱旋大厅、阅览室、酒廊、更衣室、按摩室、运动室、泳池及水力按摩池等；依年龄规则使用。子女卡不能带客、不接受餐厅预订；课程、教练及习艺室预约由主会员或配偶附属卡持有人办理。')+
'</div><div class="band"><h3>公司甲类的180万元，主要买到3位代表的使用资格</h3><p>甲、乙、丙的月费分别是6,600／4,400／2,200元，对应3／2／1名代表。个人会籍与公司会籍分别申请；公司会籍限获邀机构。代表的家属办卡资格与手续依会所审批，登记代表名额与家庭附属卡分开计算。</p></div>',sources=[('内地会籍、费用与香港互惠',MEM),('配偶附属卡申请表',BJS),('子女附属卡与120元年费',BJC),('年龄、签账及使用限制',BJ)]))

CSS='''*{box-sizing:border-box}body{margin:0;background:#edf1f5;color:#182b3e;font-family:"PingFang SC","Microsoft YaHei",sans-serif;font-size:25px;line-height:1.6}.page{width:1440px;background:#fff;padding:64px 68px 38px;border-top:12px solid #ba9248}.eyebrow{color:#667482;font-size:19px;letter-spacing:2px;margin-bottom:14px}.titleline{display:flex;align-items:flex-start;justify-content:space-between;gap:24px}h1{font-size:48px;line-height:1.3;letter-spacing:-1px;margin:0;font-weight:650}.num{font-size:27px;color:#987333;white-space:nowrap}.subtitle{font-size:25px;color:#536273;margin:20px 0 34px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:26px;margin-bottom:26px}.three{grid-template-columns:1fr 1fr 1fr}.card{background:#f5f7fa;border-top:4px solid #314e68;padding:28px 30px 26px}.tag{font-size:20px;color:#6c5b3e;margin-bottom:4px}h2{font-size:35px;line-height:1.4;margin:0 0 10px;font-weight:650}.fee{font-size:43px;font-weight:650;letter-spacing:-1px;line-height:1.4}.monthly{font-size:23px;color:#526274;margin:3px 0 15px}ul{padding-left:25px;margin:10px 0 0}li{margin:9px 0;padding-left:2px}.cardfoot{font-size:22px;border-top:1px solid #d7dee5;margin-top:18px;padding-top:13px;color:#4d5b69}.box{padding:24px 28px;border:1px solid #d7dee5;background:#fff}h3{font-size:28px;margin:0 0 10px;font-weight:650;line-height:1.4}p{margin:0}.band{background:#eaf0f5;padding:25px 30px;margin:28px 0}.band p{font-size:25px}.sources{margin-top:32px;border-top:1px solid #d7dee5;padding-top:18px;font-size:18px;line-height:1.7;color:#566777}.sources a{color:#365a7e;text-decoration:none;margin-right:20px}.meta{display:flex;justify-content:space-between;color:#6a7886;font-size:17px;margin-top:20px}.sources strong{font-weight:600}table{width:100%;border-collapse:collapse;margin:0 0 30px;font-size:27px}th{background:#29475f;color:#fff;text-align:left;padding:17px 22px;font-weight:550}td{padding:18px 22px;border-bottom:1px solid #d8e0e7}tr:nth-child(even)td{background:#f4f7fa}'''
async def main():
 async with async_playwright()as pw:
  browser=await pw.chromium.launch(headless=True)
  page=await browser.new_page(viewport={'width':1440,'height':1000},device_scale_factor=1.5)
  for i,f in enumerate(figs,1):
   src=''.join(f'<a href="{html.escape(u)}" target="_blank">[{j}] {html.escape(t)}</a>'for j,(t,u)in enumerate(f['sources'],1))
   markup=f'<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>{f["title"]}</title><style>{CSS}</style><main class="page"><div class="eyebrow">香港赛马会 · 会员体系与实际使用权益</div><div class="titleline"><h1>{f["title"]}</h1><span class="num">{i:02d} / {len(figs):02d}</span></div><p class="subtitle">{f["subtitle"]}</p>{f["body"]}<footer><div class="sources"><strong>官方资料</strong>　{src}</div><div class="meta"><span>研究整理 · 核对日期 2026年10月22日</span><span>{f.get("version","会籍收费表：2026年9月1日版")}</span></div></footer></main></html>'
   (O/(f['file']+'.html')).write_text(markup)
   await page.set_content(markup,wait_until='load');await page.evaluate('document.fonts.ready')
   issues=await page.evaluate('''()=>{let p=document.querySelector('.page');return {width:p.scrollWidth,height:p.scrollHeight,overflow:document.documentElement.scrollWidth>1440}}''')
   assert not issues['overflow'],issues
   await page.locator('.page').screenshot(path=str(O/(f['file']+'.png')))
   print(f['file'],issues)
  await browser.close()
 (O/'官方来源索引.json').write_text(json.dumps([{k:v for k,v in f.items()if k!='body'}for f in figs],ensure_ascii=False,indent=2))
 with zipfile.ZipFile(O/('香港赛马会会员体系与实际权益_三图.zip' if len(figs)==3 else '香港赛马会会籍与家庭权益_四图.zip'),'w',zipfile.ZIP_DEFLATED)as z:
  for f in figs:
   for ext in ['png','html']:z.write(O/(f['file']+'.'+ext),f['file']+'.'+ext)
  z.write(O/'官方来源索引.json','官方来源索引.json')
if __name__=='__main__':
 if '--three' in sys.argv:
  from three_figure_content import content
  figs=content(card,box,MEM,RATE,FAM,FAQ,FORM,GUIDE,BJ,BJC,BJS)
  for f in figs:
   f['body']=re.sub(r'(?<!\d)(?:18—21岁|12—21岁|8—21岁|21岁以下|14岁以上)',lambda m:'<span style="white-space:nowrap">'+m[0]+'</span>',f['body'])
  O=O/'三图修订版';O.mkdir(exist_ok=True)
  CSS+=' .section-title{font-size:31px;margin:30px 0 16px;color:#29475f} .closing-note{font-size:22px;color:#526274} .meta{gap:24px} .meta span:last-child{text-align:right;max-width:65%} table{font-size:25px} th,td{padding:16px 20px;vertical-align:top} th:first-child{width:21%}'
 asyncio.run(main())
