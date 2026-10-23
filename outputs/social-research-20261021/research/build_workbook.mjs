import fs from 'node:fs/promises';
import path from 'node:path';
import { Workbook, SpreadsheetFile } from '@oai/artifact-tool';
const root=path.resolve(import.meta.dirname,'..');
const d=JSON.parse(await fs.readFile(path.join(import.meta.dirname,'data.json'),'utf8'));
const wb=Workbook.create(), navy='#233D55', pale='#EFF4F8', gray='#566575';
const col=n=>{let s='';for(;n;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s;};
const views=[];
function sheet(name,headers,rows,widths,note){
 const s=wb.worksheets.add(name),end=col(headers.length),last=rows.length+4;
 s.showGridLines=false;s.tabColor=navy;
 s.getRange(`A1:${end}${last}`).format={font:{name:'PingFang SC',size:11,color:'#202D38'},wrapText:true,verticalAlignment:'center'};
 const titleEnd=col(Math.min(headers.length,6));
 s.mergeCells(`A1:${titleEnd}1`);s.getRange('A1').values=[[name]];s.getRange(`A1:${end}1`).format={font:{name:'PingFang SC',size:18,bold:true,color:navy},rowHeight:34};
 s.mergeCells(`A2:${titleEnd}2`);s.getRange('A2').values=[[`采集截止 2026-10-21　|　${note}`]];s.getRange(`A2:${end}2`).format={font:{size:10,color:gray},rowHeight:42};
 s.getRange(`A4:${end}${last}`).values=[headers,...rows.map(r=>r.map(v=>v===undefined?null:v))];
 s.tables.add(`A4:${end}${last}`,true,`ResearchTable${views.length+1}`);
 s.getRange(`A4:${end}4`).format={fill:navy,font:{bold:true,color:'#FFFFFF',size:11},rowHeight:32};
 s.getRange(`A5:${end}${last}`).format={rowHeight:76,borders:{preset:'all',style:'thin',color:'#DDE4EA'}};
 for(let i=0;i<headers.length;i++)s.getRange(`${col(i+1)}:${col(i+1)}`).format.columnWidth=widths[i]??24;
 // Estimate height from Chinese display width to preserve long evidence text in Excel.
 for(let i=0;i<rows.length;i++){
  let lines=1;rows[i].forEach((v,j)=>{const t=String(v??'');let units=[...t].reduce((a,c)=>a+(c.charCodeAt(0)>255?2:1),0);lines=Math.max(lines,Math.ceil(units/Math.max(8,(widths[j]??24)-2)));});
  s.getRange(`A${i+5}:${end}${i+5}`).format.rowHeight=Math.max(52,Math.min(250,lines*15+14));
 }
 s.freezePanes.freezeRows(4);s.freezePanes.freezeColumns(Math.min(2,headers.length));
 views.push({name,rows:rows.length,cols:headers.length,last});return s;
}
sheet('阅读与结论',['项目','本轮结果','解释与使用方法'],[
 ['研究用途','高端社交创业与合伙人决策','先全国宏观，再细分模式和京沪深条件，最后三家案例；三家不是经营优劣排名'],
 ['市场地图','41个机构或品牌体系','品牌去重；包含直接、相邻及替代服务；历史或未核实状态保留'],
 ['比较层','15家结构化比较；32条价格记录','价格含未知和异常；只有不同权益下的报价，不能计算统一行业均价'],
 ['深度层','京城俱乐部 伟事达中国 耀悦','306个A—F字段；每个未知保留，不把字段存在当已核实'],
 ['内容样本','耀悦20篇逐篇正文；另两家35条搜索观察','搜索样本有同名排除和旧内容，不等于合格近90天样本；不可作情感或活跃率总体统计'],
 ['活动证据','6条记录；48个流程阶段','包含回顾、合作会面、产品设计，不等于六场实际活动已完整核实'],
 ['建议方向','优先验证城市兴趣社交；旅行合作；私董和婚恋独立','条件性研究建议，需要真实购买、重复参与、交付能力证据'],
 ['经营模型','D4选择1保守 2基准 3扩展；蓝字可编辑','全部为研究假设；模型结果不是竞品或拟公司已实现经营数据'],
 ['索引方式','S为案头来源 X为平台观察/正文 E为活动 G为缺口','每项源ID对应来源台账；统计时点、定义和访问限制保留；同源转载不重复计独立证据'],
 ['关键未知','有效付费会员 续费 CAC 利润 实际成交','未知不等于零；粉丝不当会员，标价不当成交'],
 ['后续验证','优先补书面报价与目标客户实付证据','本轮未外联、购买、填咨询表单；后续动作清单见证据缺口'],
 ['单位','价格保留原币；模型为人民币元','USD与CNY不混加；人数、人次、家庭和用户分开']
],[24,53,86],'先读此页，再看来源与缺口；结论有明确证据边界');
const model=wb.worksheets.add('经营模型');model.showGridLines=false;model.tabColor='#277568';
model.getRange('B2:H52').format={font:{name:'PingFang SC',size:11,color:'#111111'},wrapText:true,verticalAlignment:'center'};
model.getRange('B:B').format.columnWidth=3;model.getRange('C:C').format.columnWidth=38;model.getRange('D:G').format.columnWidth=20;model.getRange('H:H').format.columnWidth=55;
model.mergeCells('C2:H2');model.getRange('C2').values=[['年度经营情景模型']];model.getRange('C2:H2').format={font:{size:19,bold:true,color:navy},rowHeight:36};
model.getRange('C4:D4').values=[['情景选择 1保守 2基准 3扩展',2]];
model.getRange('D4').dataValidation={rule:{type:'list',values:['1','2','3']}};
model.getRange('D4').format={font:{color:'#0000FF',bold:true},fill:'#FFF2CC'};
model.mergeCells('E4:H4');model.getRange('E4').values=[['蓝色为研究假设输入；黑色为公式结果。没有竞品实绩输入。']];
model.getRange('C7:H7').values=[['指标','当前情景','保守','基准','扩展','定义与假设']];model.getRange('C7:H7').format={fill:navy,font:{bold:true,color:'#FFFFFF'}};
const inputs=[
 ['全年等效付费会员 人',60,100,160,'按服务周期折算，不等于年末会员或新增会员'],
 ['年费 元每人',12000,18000,24000,'独立付费活动另计，是否接受须客户验证'],
 ['每月付费活动 场',2,3,4,'会员包含活动不得重复收款；本例全部为额外售票'],
 ['每场实付参与 人次',12,16,20,'不以社群人数或报名意向代替'],
 ['活动票 元每人次',800,1200,1600,'无免费名额与折扣混合；不是行业均价'],
 ['活动人均直接成本',500,650,800,'餐饮物料等，按实际含税报价修改'],
 ['每场固定直接成本',2500,3500,5000,'场地与主持执行，不与年固定人员成本重复'],
 ['每会员年度服务变动成本',1800,2400,3000,'不含已经在活动直接成本内的项目'],
 ['年度固定人员及管理成本',600000,900000,1400000,'应含创始人合理薪酬；固定场地需另加入'],
 ['全年新增实付客户 人',60,100,160,'与等效会员不是同一概念，本例暂设同数'],
 ['新增客户获客成本',2500,3500,5000,'假设值；无公开竞品有效线索与成本分母'],
 ['会费退款准备比例',.10,.08,.06,'简化扣减，非合同实际退费或会计计提'],
 ['期初可用现金',1000000,1000000,1000000,'拟投入假设，不表示已有资金'],
 ['一次性启动支出',200000,200000,200000,'现金支出，不在本例年度经营余额中折旧'],
 ['未来交付现金留存比例',.25,.25,.25,'对净会费收款留存的管理假设，非会计合同负债']
];
model.getRange('C8:C22').values=inputs.map(r=>[r[0]]);model.getRange('E8:H22').values=inputs.map(r=>r.slice(1));
model.getRange('D8:D22').formulas=inputs.map((_,i)=>[`=INDEX(E${i+8}:G${i+8},1,$D$4)`]);
model.getRange('E8:G22').format={font:{color:'#0000FF'},fill:'#EEF5FE'};
model.getRange('C7:H45').format.rowHeight=38;model.getRange('H8:H22').format.font={size:10,color:gray};
model.getRange('D8:G45').setNumberFormat('#,##0;[Red](#,##0);"—"');model.getRange('D19:G19').setNumberFormat('0.0%');model.getRange('D22:G22').setNumberFormat('0.0%');
const results=[
 ['全年付费活动 场','=D10*12','活动数并非经营效果本身'],
 ['会费毛收款 等效口径','=D8*D9','简化全年收款假设，实际须按合同月份确认'],
 ['会费退款准备','=D27*D19','管理情景扣减'],
 ['净会费收款 等效口径','=D27-D28','模型同时用作等效经营收入，非会计收入确认'],
 ['活动票收入','=D26*D11*D12','活动额外收费的可交付席位'],
 ['活动直接成本','=D26*(D11*D13+D14)','人数变动与单场固定直接成本'],
 ['活动贡献','=D30-D31','固定管理成本尚未扣除'],
 ['会员年度服务成本','=D8*D15','与活动成本分开'],
 ['固定人员与管理成本','=D16','不含启动现金支出'],
 ['新增客户获客预算','=D17*D18','盈亏平衡测算中暂固定此预算'],
 ['税前年度经营余额','=D29+D32-D33-D34-D35','未含税、借贷、折旧及可能新增固定场地'],
 ['每等效会员单位贡献','=D9*(1-D19)-D15','活动贡献独立扣抵固定成本'],
 ['盈亏平衡等效会员 人','=IF(D37<=0,"不可达",MAX(0,ROUNDUP((D34+D35-D32)/D37,0)))','当前活动贡献及获客预算固定，人数改变需重算获客'],
 ['全年付费席位 人次','=D26*D11','不代表去重参加人数'],
 ['席位除以会员 次每人','=IF(D8<=0,"无会员分母",D39/D8)','只有全部席位供会员时才代表平均可用次数'],
 ['期初现金','=D20','资金投入假设'],
 ['启动支出现金','=D21','仅列现金影响'],
 ['简化期末现金','=D41+D36-D42','假定年度收入全额收妥且成本当年支付'],
 ['未来交付现金留存','=D29*D22','管理假设，并非按合同计算未履约余额'],
 ['扣留存后可用现金','=D43-D44','不能代替按月现金流与法定收入确认']
];
model.getRange('C26:C45').values=results.map(r=>[r[0]]);model.getRange('D26:D45').formulas=results.map(r=>[r[1]]);model.getRange('H26:H45').values=results.map(r=>[r[2]]);model.getRange('H26:H45').format.font={size:10,color:gray};
model.getRange('D40').setNumberFormat('0.00');for(const r of [29,32,36,38,43,45])model.getRange(`C${r}:H${r}`).format={fill:pale,font:{bold:true}};
model.getRange('D36').conditionalFormats.add('cellIs',{operator:'lessThan',formula:0,format:{font:{color:'#C00000'},fill:'#FCECEC'}});
model.mergeCells('C48:H49');model.getRange('C48').values=[['所有数字为可编辑的研究假设。该年度等效模型用于比较定价、容量和成本条件；不是月度现金流预测。正式预算需补入分月招募、合同履约和收入确认、真实退款、税费、旅行合作净收入、固定租赁与供应商付款节奏。']];model.getRange('C48:H49').format={rowHeight:29,font:{size:10,color:gray}};model.freezePanes.freezeRows(7);
sheet('15家比较',['机构ID','机构','城市或覆盖','类别','主要产品','收费模式','品牌目标客户','公开权益','获客入口','交付主体','有效付费会员','经营经济性','分析及限制','源ID'],d.comparisons,[12,22,23,24,35,26,34,44,34,30,22,22,53,18],'不是同类排行榜；会员和经济性未知不记零');
const priceSheet=sheet('价格权益',['机构','城市或目的地','产品或等级','金额','币种','收费单位','报价或有效期','包含权益','不包含或未核','额外条件及费用','退改','证据类别','源ID','采集日'],d.prices,[24,28,38,16,10,17,25,55,45,52,43,37,19,16],'价格单位和权益必须一起读；未知金额为空；异常不纳入价格锚');
priceSheet.getRange(`D5:D${d.prices.length+4}`).setNumberFormat('#,##0');
sheet('产品分类',['机构ID','机构','产品类别','核心需求','收费模式','期限频次及权益','线上线下比例','预约候补','关系状态及带客','体验咨询入口','自有合作交付','交叉销售证据','源ID'],d.products,[12,23,38,34,28,50,22,22,48,38,36,43,19],'机构定位与实际客户分开；产品并列不证明交叉销售');
sheet('客户画像',['画像ID','需求分层','职业身份定位','关系状态','核心需求','购买触发 假设','选择标准','源ID','证据与待验边界','重要限制'],d.personas,[12,25,34,32,38,43,46,25,60,42],'非虚构人物；实际预算年龄资产占比未取得，三家逐字段见字段核验');
sheet('获客路径',['机构','公开渠道及入口','可见内容主题','访问或留资','咨询与成交边界','筛选','体验转付费率','获客成本','转介绍成交','机制与实绩区别','源ID'],d.acquisition,[23,44,43,38,48,40,24,24,24,42,25],'完整漏斗保留未知；无有效线索成交与花费不算CAC');
sheet('活动记录',['活动ID','机构','活动名称','时间或团期','地点','记录类型','目标人群','天数','人均报价','到场情况','可见安排','源ID','证据限制'],d.events,[12,21,35,30,23,33,34,12,17,38,68,19,53],'实际回顾、合作会面、产品设计分开；不把预告当已举办');
sheet('活动流程',['活动ID','机构','活动名称','阶段','已知环节或未知','证据性质','源ID'],d.flows,[12,22,35,22,88,58,22],'48个环节保留；未披露步骤不补写为竞品实际SOP');
sheet('用户与活跃',['机构','指标','观察值或未知','定义与证据限制','源ID'],d.metrics,[24,30,62,75,35],'粉丝、人数、人次和会员分开；不从集团投资损益反推品牌利润');
sheet('内容样本',['机构或检索词','标题','页面显示日期','采集日','采集深度','可见互动值','评论数','收藏数','商业标识','主题或状态','公开链接','源ID','样本限制'],d.notes,[23,58,28,16,29,17,15,15,48,46,58,19,65],'55条记录不等于55篇合格内容；仅耀悦20条逐篇正文；空白互动为未取得而非零');
sheet('宏观数据',['指标','统计年','数值','单位','地区','源ID','证据类别','口径与限制'],d.macro,[35,14,20,15,18,15,24,85],'不同市场不能相加；用户非付费会员；第三方方法限制在来源表');
const imap=d.institutions.map(o=>[o.id,o.name,o.category,o.city,o.model,o.target,o.role,o.status,o.group,o.source]);
sheet('机构地图',['机构ID','品牌或机构','分类','城市或覆盖','模式','目标客户定位','比较关系','状态及限制','去重体系','源ID'],imap,[12,28,28,30,40,42,27,43,28,19],'41条去重体系，不是41家直接竞品；跨城业务须核实当地实际供给');
sheet('来源台账',['源ID','标题','发布或提供主体','统计期或发布时间','证据类别','关键发现','限制','访问方式','采集日','链接'],d.sources.map(s=>[s.id,s.title,s.publisher,s.period,s.kind,s.finding,s.limit,s.access,s.collected,s.url]),[15,58,34,30,26,80,85,60,16,75],'101条可追溯记录含20篇平台笔记；来源数不等于独立研究数');
sheet('证据缺口',['缺口ID','模块','待解问题','当前不足','下一步具体证据','决策影响','动作状态'],d.gaps,[12,20,55,70,65,62,27],'后续验证清单；本轮不外联、不购买、不填写咨询表单');
sheet('字段核验',['案例','模块','字段','已知值或未知','源ID或检查来源','核验状态','查找范围及剩余证据'],d.fields,[23,20,25,88,35,24,70],'三家各102字段 共306条；部分证据不是完整核实');
const mode=wb.worksheets.add('收费模式比较');mode.showGridLines=false;mode.tabColor='#277568';
mode.getRange('C2:H42').format={font:{name:'PingFang SC',size:11},wrapText:true,verticalAlignment:'center',rowHeight:40};
mode.getRange('C:C').format.columnWidth=33;mode.getRange('D:G').format.columnWidth=22;mode.getRange('H:H').format.columnWidth=63;
mode.mergeCells('C2:H2');mode.getRange('C2').values=[['收费模式与敏感性比较']];mode.getRange('C2').format.font={size:18,bold:true,color:navy};
mode.mergeCells('C3:H3');mode.getRange('C3').values=[['研究假设；共同沿用经营模型D4所选情景的团队、获客和活动配置。不同模式实际应重新匹配成本和客户，不是四项可直接相加的收入。']];
mode.getRange('C6:H6').values=[['指标','纯按次','会费含活动','会费另付活动','定制净服务','计算与边界']];mode.getRange('C6:H6').format={fill:navy,font:{color:'#FFFFFF',bold:true}};
const ml=[
 ['净会费收款',0,"='经营模型'!D29","='经营模型'!D29",0,'等效全年口径；保留原模型退款准备'],
 ['活动票收入',"='经营模型'!D30",0,"='经营模型'!D30",0,'会费包含活动时，票不重复计收入'],
 ['定制组织净服务费',0,0,0,'=G24*G25*G26','仅组织服务收入，不把旅行供应商代收款当收入'],
 ['活动直接成本',"='经营模型'!D31","='经营模型'!D31","='经营模型'!D31",0,'包含活动也必须承担交付成本'],
 ['会员服务变动成本',0,"='经营模型'!D33","='经营模型'!D33",0,'按次模式不提供持续会员服务'],
 ['定制项目直接成本',0,0,0,'=G24*(G25*G27+G28)','组织人力、执行及单项目固定直接成本'],
 ['固定人员及管理成本',"='经营模型'!D34","='经营模型'!D34","='经营模型'!D34","='经营模型'!D34",'为便于比较暂固定；不表示每种模式都应配同一团队'],
 ['新增客户获客预算',"='经营模型'!D35","='经营模型'!D35","='经营模型'!D35","='经营模型'!D35",'独立假设，定制客户数变化须同步重做获客预算'],
 ['合计模式收入','=SUM(D7:D9)','=SUM(E7:E9)','=SUM(F7:F9)','=SUM(G7:G9)','四种互斥模式演示，不是合并预测'],
 ['扣直接交付后贡献','=D15-D10-D11-D12','=E15-E10-E11-E12','=F15-F10-F11-F12','=G15-G10-G11-G12','固定管理和获客尚未扣除'],
 ['税前年度经营余额','=D16-D13-D14','=E16-E13-E14','=F16-F13-F14','=G16-G13-G14','未含税、折旧及现金时点；不是实绩']
];
mode.getRange('C7:C17').values=ml.map(r=>[r[0]]);mode.getRange('H7:H17').values=ml.map(r=>[r[5]]);
for(let i=0;i<ml.length;i++)for(let j=1;j<=4;j++){const a=`${col(j+3)}${i+7}`,v=ml[i][j];if(typeof v==='string'){mode.getRange(a).formulas=[[v]];mode.getRange(a).format.font={color:v.includes('经营模型')?'#008040':'#111111'};}else mode.getRange(a).values=[[v]];}
mode.getRange('D7:G17').setNumberFormat('#,##0;[Red](#,##0);"—"');mode.getRange('C17:H17').format={fill:pale,font:{bold:true}};
mode.getRange('D17:G17').conditionalFormats.add('cellIs',{operator:'lessThan',formula:0,format:{font:{color:'#C00000'}}});
mode.mergeCells('C20:H21');mode.getRange('C20').values=[['四种模式只比较收费机制改变后的算术影响。纯按次需要足够票价、人数和频次覆盖持续成本；会费含活动要核算席位与免费交付；混合收费需验证客户是否接受；定制净服务必须有可单独收费的组织价值。']];
mode.getRange('C23:H23').values=[['定制净服务假设',null,null,null,'输入','口径']];mode.getRange('C23:H23').format={fill:navy,font:{bold:true,color:'#FFFFFF'}};
const custom=[['全年项目 次',12,'不是公开市场发生量'],['每项目实付客户 人',4,'去重新增与重复项目另需拆分'],['每人净组织收入 元',6000,'不包含旅行行程或机票代收款'],['每人组织变动成本 元',2000,'专业组织与服务成本假设'],['每项目固定直接成本 元',12000,'执行及差旅等；不与年度固定团队重复']];
mode.getRange('C24:C28').values=custom.map(x=>[x[0]]);mode.getRange('G24:H28').values=custom.map(x=>x.slice(1));mode.getRange('G24:G28').format={font:{color:'#0000FF'},fill:'#EEF5FE'};mode.getRange('G24:G28').setNumberFormat('#,##0');
mode.mergeCells('C31:H32');mode.getRange('C31').values=[['下表仅改变全年等效会员人数与年费，沿用当前情景退款率、会员服务单位成本、活动贡献、固定团队及获客预算。获客预算暂固定，人数变化时应重新验证；非统计置信区间。蓝色为可编辑研究假设。']];
mode.getRange('C35:F38').values=[['会员人数 / 年费',12000,18000,24000],[60,null,null,null],[100,null,null,null],[160,null,null,null]];mode.getRange('C35:F35').format={fill:navy,font:{color:'#FFFFFF',bold:true}};
mode.getRange('D35:F35').format.font={color:'#66B3FF',bold:true};mode.getRange('C36:C38').format.font={color:'#0000FF'};
mode.getRange('D36:F38').formulas=[36,37,38].map(r=>['D','E','F'].map(c=>`=$C${r}*(${c}$35*(1-'经营模型'!$D$19)-'经营模型'!$D$15)+'经营模型'!$D$32-'经营模型'!$D$34-'经营模型'!$D$35`));
mode.getRange('D35:F38').setNumberFormat('#,##0;[Red](#,##0);"—"');mode.getRange('D36:F38').conditionalFormats.add('colorScale',{colors:['#FBE4E1','#FFFFFF','#DCEFE7'],thresholds:['min','50%','max']});mode.getRange('C35:F38').format.borders={preset:'all',style:'thin',color:'#D9D9D9'};
mode.freezePanes.freezeRows(6);
wb.recalculate();
const check=[];
for(const [i,a] of inputs[0].slice(1,4).entries()){
 model.getRange('D4').values=[[i+1]];wb.recalculate();
 const x=inputs.map(r=>r[i+1]);const events=x[2]*12,net=x[0]*x[1]*(1-x[11]),cont=events*(x[3]*(x[4]-x[5])-x[6]);
 const expected=net+cont-x[0]*x[7]-x[8]-x[9]*x[10];const actual=model.getRange('D36').values[0][0];
 const expectedBE=Math.max(0,Math.ceil((x[8]+x[9]*x[10]-cont)/(x[1]*(1-x[11])-x[7])));const actualBE=model.getRange('D38').values[0][0];
 if(Math.abs(actual-expected)>.01 || actualBE!==expectedBE)throw Error(`模型校验失败 ${i+1} ${actual} ${expected}`);
 check.push({scenario:i+1,operating:actual,breakEven:actualBE,seats:model.getRange('D39').values[0][0]});
}
model.getRange('D4').values=[[2]];wb.recalculate();
const modeActual=mode.getRange('D17:G17').values[0];const modeExpected=[-1059200,-334400,356800,-1202000];
if(modeActual.some((v,i)=>Math.abs(v-modeExpected[i])>.01))throw Error('收费模式校验失败 '+modeActual);
if(mode.getRange('E37').values[0][0]!==356800)throw Error('敏感性基准格校验失败');
await fs.writeFile(path.join(root,'qa','model-check.json'),JSON.stringify(check,null,2));
const inspection=await wb.inspect({kind:'region',sheetId:'经营模型',range:'C26:H45',maxChars:7000,tableMaxRows:22,tableMaxCols:6});await fs.writeFile(path.join(root,'qa','workbook-inspect.json'),JSON.stringify(inspection,null,2));
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#N/A',options:{useRegex:true,maxResults:100},maxChars:3000});await fs.writeFile(path.join(root,'qa','workbook-errors.json'),JSON.stringify(errors,null,2));
const out=await SpreadsheetFile.exportXlsx(wb);await out.save(path.join(root,'中国高端社交市场研究数据工作簿.xlsx'));
console.log(JSON.stringify({exported:true,model:check,modes:modeActual,sheets:views.length+2}));
for(const v of views){
 const range=`A1:${col(Math.min(v.cols,6))}${Math.min(v.last,8)}`;
 const p=await wb.render({sheetName:v.name,range,scale:1.15,format:'png'});await fs.writeFile(path.join(root,'qa',`sheet-${v.name}.png`),new Uint8Array(await p.arrayBuffer()));
}
for(const range of ['C2:H22','C26:H49']){
 const p=await wb.render({sheetName:'经营模型',range,scale:1.15,format:'png'});await fs.writeFile(path.join(root,'qa',`model-${range.slice(0,3)}.png`),new Uint8Array(await p.arrayBuffer()));
}
for(const range of ['C2:H17','C20:H38']){
 const p=await wb.render({sheetName:'收费模式比较',range,scale:1.15,format:'png'});await fs.writeFile(path.join(root,'qa',`modes-${range.slice(0,3)}.png`),new Uint8Array(await p.arrayBuffer()));
}
console.log('Workbook previews complete');
