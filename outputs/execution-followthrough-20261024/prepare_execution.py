from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json
B=Path(__file__).parent;R=B.parents[1]
url='https://www.marriott.com.cn/search/availabilityCalendar.mi?lengthOfStay=3&fromDate=2026-11-19&toDate=2026-11-22&numberOfRooms=1&numberOfAdults=1&childrenCount=0&clusterCode=none&isHwsGroupSearch=true&propertyCode=SYXXR&useRewardsPoints=false&flexibleDateSearch=false'
base=dict(hotel='三亚亚龙湾瑞吉度假酒店',checkin='2026-11-19',checkout='2026-11-22',nights=3,rooms=1,adults=1,room='瑞吉青樾湾景观房 一张特大床 港景 阳台',area_sqm=73,currency='CNY',taxes_included=True,source_url=url,captured_at=datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(),source_type='万豪官网查询结果及房价详情；浏览器实查',scope='1间客房、1位成人的零售公开价；未证明可按此价取得14间房；不是旅行社或酒店团体书面报价')
rows=[]
for key,name,total,night,bfast,member,prepay,ref in [
 ('SR-PRE','预付含早餐',7240,2413,'页面写早餐；人数未单列',False,6210,'预订不可更改；显示2026-10-25 23:59前可免费取消，之后预付款不退'),
 ('SR-FLEX','普通灵活退改',7520,2506,'该档未写包含早餐',False,6450,'明细显示2026-10-25 23:59后取消预计扣6450元，即全部晚数房费'),
 ('SR-MFLEX','会员灵活退改',7144,2381,'该档未写包含早餐',True,None,'本次未展开该会员档独立条款，不套用普通档退款日'),
 ('SR-BB','普通含早套餐',7870,2623,'每天2成人及2位6岁以下儿童早餐；本次按1位成人查询',False,6750,'明细显示2026-10-25 23:59后取消预计扣6750元，即全部晚数房费'),
 ('SR-MBB','会员含早套餐',7478,2492,'每天2人早餐',True,None,'该会员档退款及预付款时点未独立展开'),
 ('SR-TWIN','双大床预付含早',7004,2334,'页面写早餐；人数未单列',False,None,'该双床档明细未独立展开；不能直接套用特大床全部条款')
]:
 row=dict(base,id=key,rate_name=name,total=total,display_avg_nightly=night,breakfast=bfast,membership_required=member,displayed_prepayment=prepay,cancellation=ref)
 if key=='SR-TWIN':row['room']='瑞吉青樾湾景观房 两张大床 港景 阳台'
 if key=='SR-BB':row['included']=['首日欢迎水果和迷你吧','每次入住一次双人皮划艇','入夜马刀开香槟仪式','彩虹滑梯和小火车体验','30分钟家庭旅拍、7张电子照及15秒视频','免税优惠券和免税城班车','连住至少2晚另含一次双人珊瑚观光船'];row['evidence']=['瑞吉-含早含税套餐价.txt','瑞吉-7870含早套餐完整条款.txt']
 else:row['included']=[]
 row['payment_note']='页面预付款以税前房费金额列示，余下税费付款时点未单独说明；现金模型按含税全价占用保守测算。'
 rows.append(row)
extra_quote=B/'携程同日核价.json'
if extra_quote.exists():rows.append(json.loads(extra_quote.read_text()))
old=json.loads((R/'outputs/travel-community-20261023/研究与产品数据.json').read_text())
models=[]
for p in old['products']:
 q=dict(p)
 q['price_status']='研究情景，未确认售价、资源和客户愿付'
 q['supply_status']='供应商书面报价与客户访谈未取得'
 if p['id']=='dinner':q['customer']='北京仅作测算城市；目标A8及以上、真实单身且有稳定关系意愿的人。个人或家庭资产口径、年龄带待合伙人确认。访谈分别覆盖经营者、接班二代、专业人士及离异后重建关系者。'
 elif p['id']=='talk':q['customer']='目标为A8及以上经营者、业务负责人及专业服务合伙人；单身、恋爱中、已婚均可。具体年龄带和资产口径待确认，围绕真实经营问题组织。'
 else:q['customer']='与婚恋晚宴服务同一批A8及以上、真实单身客户；周四至周日和独住为产品讨论条件，年龄带与个人或家庭资产口径待合伙人确认。'
 if p['id']=='travel':
  q.update(hotel_total_per_guest=7870,old_hotel_total_per_guest=4500,nights=3,rooms_per_guest=1,other_per_guest=3500,vehicle_per_batch=9800,vehicle_passenger_capacity=19,onsite_staff=3,hotel_prepaid_fraction=1,other_prepaid_fraction=.7,vehicle_prepaid_fraction=.7,deposit_fraction=.3,refund_fraction=.03,minimum_social_participants=12,model_date='2026-11-19至22日',fixed_cost_excludes_vehicle=48000,hotel_quote_id='SR-BB',hotel_scope=base['scope'],hotel_includes_breakfast=True)
  q['assumptions']={'meals':1600,'extra_experiences':1100,'insurance_materials':300,'coordination':500,'vehicle':'9800元来自旧基准14人×700，改按每批车辆固定预算；未经供应商报价','extra_experiences_note':'只买额外体验；已含皮划艇、珊瑚船、旅拍不能再次计入同一采购','staff':'3名为岗位安排假设；车辆19个乘客位不含司机，需取得对应车型与报价','fixed':'48000含筹备与现场工时报酬、团队机酒及项目场地物料；现金按项目工时报酬全部付出','hotel':'采用7870元三晚含早零售公开价作为成本情景，14间库存与团体适用性未确认'}
 else:
  q.update(refund_fraction=.03,deposit_fraction=.3,model_date='待合伙人确定',onsite_staff=3 if p['id']=='dinner' else 2)
 models.append(q)
def calculate(m,n,hotel=None,price=None,refund=None):
 from math import ceil
 price=m['price']if price is None else price;r=m['refund_fraction']if refund is None else refund
 gross=price*n
 if m['id']=='travel':
  h=m['hotel_total_per_guest']if hotel is None else hotel;hc=h*n;oc=m['other_per_guest']*n;vehicles=ceil((n+m['onsite_staff'])/m['vehicle_passenger_capacity']);vc=m['vehicle_per_batch']*vehicles
  costs=hc+oc+vc+m['fixed']+m['cac']*n
  early=m['fixed']*.4+m['cac']*n
  due=hc*m['hotel_prepaid_fraction']+oc*m['other_prepaid_fraction']+vc*m['vehicle_prepaid_fraction']+m['fixed']+m['cac']*n
  cash=max(early,due-gross*m['deposit_fraction'],0)+gross*r
  return dict(n=n,gross=gross,refund=gross*r,hotel=hc,other=oc,vehicle=vc,vehicle_batches=vehicles,fixed=m['fixed'],cac=m['cac']*n,contribution=gross*(1-r)-costs,cash=cash)
 costs=m['var']*n+m['cac']*n+m['fixed'];cash=max(m['fixed']*.4+m['cac']*n,.7*m['var']*n+m['fixed']+m['cac']*n-gross*.3,0)+gross*r
 return dict(n=n,gross=gross,refund=gross*r,direct=m['var']*n,fixed=m['fixed'],cac=m['cac']*n,contribution=gross*(1-r)-costs,cash=cash)
results={m['id']:[calculate(m,n)for n in [m['low'],m['base'],m['full']]]for m in models}
tm=next(m for m in models if m['id']=='travel')
breaks=[(n,calculate(tm,n)['contribution'])for n in range(1,tm['capacity']+1)]
travel_break=next((n for n,v in breaks if v>=0),None)
data=dict(updated_at=datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(),quotes=rows,models=models,results=results,travel_financial_break_even=travel_break,travel_social_minimum=12,travel_hotel_change_per_guest=3370,trip_operator_quote_status='两家书面供应商报价仍未取得；携程同日大床含早三晚7240.86元已在预订详情页核验，未提交订单；与官网赠送和取消条件不同',source_folder='.research-private/execution-followthrough-20261024',principles=['围绕同一批客户持续组织线下活动','研究报告保持市场调研与对标两部分','旧试价仅用于可调整情景，不是新的定价建议','外部咨询和客户访谈由已分工人员进行，不代造回复','本轮未订房、未留资、未付款、未外联'])
B.mkdir(parents=True,exist_ok=True);(B/'执行依据与测算数据.json').write_text(json.dumps(data,ensure_ascii=False,indent=2));print(json.dumps({'hotel_quote_total':7870,'models':results,'travel_break':travel_break},ensure_ascii=False))
