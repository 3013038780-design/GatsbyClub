import fs from 'node:fs/promises';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const B=decodeURIComponent(new URL('.',import.meta.url).pathname),D=JSON.parse(await fs.readFile(B+'执行依据与测算数据.json','utf8')),w=Workbook.create();
const s=w.worksheets.add('启动测算'),q=w.worksheets.add('报价与条款'),p=w.worksheets.add('产品卡与分工');
const ink='#263746',money='#,##0;(#,##0);"—"',links=[];
for(const sh of[s,q,p]){sh.showGridLines=false;sh.getRange('A1:J85').format={font:{name:'Arial',size:11,color:ink},verticalAlignment:'center'};sh.freezePanes.freezeRows(5);}
function input(sh,cell,v){sh.getRange(cell).values=[[v]];sh.getRange(cell).format={fill:'#FFF2CC',font:{color:'#0000FF'}};}
function band(sh,r,a='A',b='D'){sh.getRange(`${a}${r}:${b}${r}`).format={fill:'#E7EDF1',font:{bold:true},rowHeight:28};}
function heading(sh,title,sub,last='I'){sh.getRange(`A2:${last}2`).merge();sh.getRange('A2').values=[[title]];sh.getRange('A2').format={font:{size:17,bold:true},rowHeight:35};sh.getRange(`A3:${last}3`).merge();sh.getRange('A3').values=[[sub]];sh.getRange('A3').format={wrapText:true,rowHeight:38,font:{size:10,color:'#536674'}};}
heading(s,'启动产品与交付测算','沿用研究试价，新增三晚含早零售价参照；蓝字为可修改预算。贡献已含项目工时预算，未扣公司日常开支和税费。');
s.getRange('A4').values=[['人数情景 1低于预期 2基准 3满团']];input(s,'B4',2);s.getRange('B4').dataValidation={rule:{type:'whole',operator:'between',formula1:1,formula2:3}};
s.getRange('A5:D5').values=[['单次经营项目',...D.models.map(x=>x.name)]];s.getRange('A5:D5').format={fill:ink,font:{bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:42};
s.getRange('F5:I5').values=[['人数输入','低于预期','基准','满团']];s.getRange('F5:I5').format={fill:ink,font:{color:'#FFFFFF',bold:true},wrapText:true,rowHeight:30};
D.models.forEach((m,i)=>{let r=i+6;s.getRange('F'+r).values=[[m.name]];for(const[c,v]of[['G',m.low],['H',m.base],['I',m.full]])input(s,c+r,v);});
const labels={6:'研究试价 元／人',7:'当前人数',8:'单人直接交付预算',9:'单人获客预算',10:'固定交付及工时预算',11:'退款金额占收款比例',12:'筹备现场回访总工时',13:'旅行产品人数下限',14:'现场岗位人数',16:'未扣退款收款额',17:'退款现金预留',18:'扣退款后收入',19:'直接交付支出',20:'车辆支出 单独按批计算',21:'获客支出',22:'固定及工时支出',23:'支出合计',24:'单次贡献',25:'贡献率',26:'财务保本人数',27:'人数与交付提示',29:'客户首付款比例',30:'其他直接成本预付比例',32:'首付款收入',33:'收首付款前筹备及获客现金',34:'首付款阶段累计应付支出',35:'首付款收支净额',36:'保守启动周转金',37:'完成后余额 扣退款预留'};
for(const[r,v]of Object.entries(labels))s.getRange('A'+r).values=[[v]];
for(const[cell,label,v]of[
 ['H11','每人三晚住宿预算',7870],['H12','正餐预算每人全程',1600],['H13','另购体验预算每人',1100],['H14','保险物料每人',300],['H15','协调服务每人',500],['H17','每批车辆全程预算',9800],['H18','每批车辆乘客位 不含司机',19],['H20','酒店含税全价现金预留比例',1],['H21','其他直接支出预付比例',.7],['H22','车辆预付比例',.7]
]){s.getRange('F'+cell.slice(1)).values=[[label]];input(s,cell,v);}
s.getRange('F10:I10').merge();s.getRange('F10').values=[['旅行的可修改成本输入']];band(s,10,'F','I');
s.getRange('F16:I16').merge();s.getRange('F16').values=[['已含早餐；皮艇、观光船及旅拍不重复采购。']];s.getRange('F16:I16').format={font:{size:10,color:'#536674'},wrapText:true,rowHeight:35};
s.getRange('F24:I27').merge();s.getRange('F24').values=[['住宿默认7870元来自报价表SR-BB，1人1房三晚含税含早零售价。14间库存与团体适用性未知；车辆9800元和其余成本仍为预算。酒店明细预付6750元，税费支付时点未单列，现金按全价占用保守处理。']];s.getRange('F24:I27').format={wrapText:true,verticalAlignment:'top'};
for(let i=0;i<3;i++){
 const c=String.fromCharCode(66+i),m=D.models[i],r=i+6;
 for(const[row,v]of Object.entries({6:m.price,9:m.cac,10:m.fixed,11:.03,12:m.hours,14:m.onsite_staff,29:.3,30:.7}))input(s,c+row,v);
 s.getRange(c+'7').formulas=[[`=CHOOSE($B$4,$G$${r},$H$${r},$I$${r})`]];
 if(i<2)input(s,c+'8',m.var);else s.getRange('D8').formulas=[['=IF(H11>0,H11+SUM(H12:H15),"缺少住宿预算")']];
 s.getRange(c+'13').values=[[i===2?12:'按场次审核']];
 let f={16:`${c}6*${c}7`,17:`${c}16*${c}11`,18:`${c}16-${c}17`,19:`${c}8*${c}7`,20:'0',21:`${c}9*${c}7`,22:`${c}10`,23:`SUM(${c}19:${c}22)`,24:`${c}18-${c}23`,25:`IF(${c}18>0,${c}24/${c}18,0)`,26:`IF(${c}6*(1-${c}11)-${c}8-${c}9>0,ROUNDUP(${c}10/(${c}6*(1-${c}11)-${c}8-${c}9),0),"无保本人数")`,32:`${c}16*${c}29`,33:`${c}10*40%+${c}21`,34:`${c}19*${c}30+${c}21+${c}22`,35:`${c}32-${c}34`,36:`MAX(${c}33,-${c}35,0)+${c}17`,37:`${c}16-${c}23-${c}17`};
 if(i===2)Object.assign(f,{19:'IF(ISNUMBER(D8),D8*D7,"缺少住宿预算")',20:'ROUNDUP((D7+D14)/H18,0)*H17',23:'IF(ISNUMBER(D19),SUM(D19:D22),"需补住宿预算")',24:'IF(ISNUMBER(D23),D18-D23,"需补住宿预算")',25:'IF(ISNUMBER(D24),D24/D18,"需补住宿预算")',26:'IF(ISNUMBER(D8),IF(COUNTIF(H36:H51,">=0")=0,"本范围未保本",MINIFS(E36:E51,H36:H51,">=0")),"需补住宿预算")',34:'IF(ISNUMBER(D8),H11*D7*H20+SUM(H12:H15)*D7*D30+D20*H22+D21+D22,"需补住宿预算")',35:'IF(ISNUMBER(D34),D32-D34,"需补住宿预算")',36:'IF(ISNUMBER(D35),MAX(D33,-D35,0)+D17,"需补住宿预算")',37:'IF(ISNUMBER(D23),D16-D23-D17,"需补住宿预算")'});
 for(const[row,v]of Object.entries(f))s.getRange(c+row).formulas=[['='+v]];
 s.getRange(c+'27').values=[[i===2?'看人数下限及报名结构':'另核实名和报名结构']];
 s.getRange(`${c}6:${c}37`).setNumberFormat(money);for(const n of[11,25,29,30])s.getRange(c+n).setNumberFormat('0.0%');
}
s.getRange('D27').formulas=[['=IF(D7>=D13,"达到人数下限；另核结构","低于产品人数下限")']];
s.getRange('D30').formulas=[['=H21']];s.getRange('D30').format={fill:'#FFFFFF',font:{color:ink}};
for(const r of[18,23,24,26,36,37])band(s,r);
s.getRange('A27:D27').format={wrapText:true,rowHeight:44};
for(const r of[20,33,34,35,36,37])s.getRange(`A${r}`).format.wrapText=true;
s.getRange('E35:H35').values=[['旅行人数','乘客位需求','车辆批次','单团贡献 元']];s.getRange('E35:H35').format={fill:ink,font:{bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:34};
for(let n=1;n<=16;n++){let r=n+35;s.getRange('E'+r).values=[[n]];s.getRange('F'+r).formulas=[[`=E${r}+$D$14`]];s.getRange('G'+r).formulas=[[`=ROUNDUP(F${r}/$H$18,0)`]];s.getRange('H'+r).formulas=[[`=IF(ISNUMBER($D$8),$D$6*E${r}*(1-$D$11)-E${r}*($D$8+$D$9)-G${r}*$H$17-$D$10,"需补住宿预算")`]];}
s.getRange('H36:H51').setNumberFormat(money);s.getRange('A40:C40').values=[['项目工时阶段','旅行团队工时','说明']];s.getRange('A41:C43').values=[['筹备',70,'预算，不是已测得工时'],['现场',96,'3人×4天×8小时'],['回访',24,'团队合计']];s.getRange('A44').values=[['旅行工时核对']];s.getRange('B44').formulas=[['=SUM(B41:B43)']];s.getRange('A40:C44').format={wrapText:true,rowHeight:27};
s.getRange('A46:D50').merge();s.getRange('A46').values=[['周转金假设：固定成本和项目工时预算全部按现金支出预留。合伙人工时若暂不支付，实际外部现金需求会降低，需按真实结算重算。酒店按含税全价、其他直接成本及车辆按70%预付。']];s.getRange('A46:D50').format={wrapText:true,verticalAlignment:'top'};
s.getRange('A54:I54').merge();s.getRange('A54').values=[['年度频次与人力承载  仅供改输入讨论']];band(s,54,'A','I');
s.getRange('A56:E56').values=[['产品','计划次数／年','每次团队工时','全年团队工时','现场岗位人数']];s.getRange('A56:E56').format={fill:ink,font:{bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:36};
D.models.forEach((m,i)=>{let r=i+57,c=String.fromCharCode(66+i);s.getRange('A'+r).values=[[m.name]];input(s,'B'+r,i===2?4:6);s.getRange('C'+r).formulas=[[`=${c}12`]];s.getRange('D'+r).formulas=[[`=B${r}*C${r}`]];s.getRange('E'+r).formulas=[[`=${c}14`]];});
for(const[r,label,v]of[[56,'可投入团队人数',2],[57,'每人每月可用项目工时',80],[58,'可投入月份',12]]){s.getRange('G'+r).values=[[label]];input(s,'I'+r,v);}
s.getRange('G59').values=[['全年项目工时容量']];s.getRange('I59').formulas=[['=I56*I57*I58']];s.getRange('G60').values=[['计划工时占用率']];s.getRange('I60').formulas=[['=SUM(D57:D59)/I59']];s.getRange('I60').setNumberFormat('0.0%');s.getRange('G61').values=[['旅行现场另需岗位']];s.getRange('I61').formulas=[['=MAX(D14-I56,0)']];
s.getRange('A63:I65').merge();s.getRange('A63').values=[['年度工时够，不代表两个团能同时开。旅行默认需要3个现场岗位；2人团队仍需外部人员。没有确认的日期、客户和供应商时，6／6／4次仅是人力情景，不能写成年度销售计划。所有项目收入均按独立单次收费，未叠加年费。']];s.getRange('A63:I65').format={wrapText:true,verticalAlignment:'top'};
for(const[a,width]of[['A',36],['B',25],['C',25],['D',27],['E',18],['F',36],['G',22],['H',23],['I',23]])s.getRange(`${a}1:${a}67`).format.columnWidth=width;
s.getRange('A6:D37').format.rowHeight=27;for(const r of[20,27,33,34,35,36,37])s.getRange(`A${r}:D${r}`).format.rowHeight=40;s.getRange('F11:G22').format.wrapText=true;s.getRange('G56:H61').format.wrapText=true;
heading(q,'三亚同日房型公开价格与条款','2026-11-19至22日，1房1成人；官网为含税总价，携程为预订详情页应付总价且未单列税费。均未确认14间库存或团体价。');
q.getRange('A5:I5').values=[['编号','房价及房型','三晚页面总价','显示每晚均价','包含早餐及活动','预付款及取消','适用与证据','观察时间','入口']];q.getRange('A5:I5').format={fill:ink,font:{bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:35};
const quoteLast=D.quotes.length+5;const qr=D.quotes.map(x=>[x.id,x.rate_name+'\n'+x.room,x.total,x.display_avg_nightly,x.breakfast+(x.included.length?'\n'+x.included.join('；'):''),(x.displayed_prepayment===null?'未独立展开预付款':'显示预付款'+x.displayed_prepayment+'元')+'\n'+x.cancellation,x.scope+'\n'+x.payment_note,x.captured_at.slice(0,16).replace('T',' '),'查看官网']);q.getRange(`A6:I${quoteLast}`).values=qr;q.getRange(`A6:I${quoteLast}`).format={wrapText:true,rowHeight:155,verticalAlignment:'top'};q.getRange(`C6:D${quoteLast}`).setNumberFormat('#,##0');q.tables.add(`A5:I${quoteLast}`,true,'QuoteTerms');
q.getRange(`A6:I${quoteLast}`).format.fill='#FFFFFF';for(let r=6;r<=quoteLast;r+=2)q.getRange(`A${r}:I${r}`).format.fill='#F1F4F6';
for(const[i,width]of[13,35,20,19,61,62,64,24,18].entries())q.getRangeByIndexes(0,i,20,1).format.columnWidth=width;
q.getRange('C'+quoteLast).setNumberFormat('#,##0.00');q.getRange(`A${quoteLast}:I${quoteLast}`).format.rowHeight=190;
D.quotes.forEach((x,i)=>links.push({sheet:1,cell:'I'+(i+6),url:x.source_url}));
q.getRange('A14:I16').merge();q.getRange('A14').values=[['普通含早套餐7870元用于当前住宿预算。万豪会员价、预付价、纯房价不互相替代。官网同房型1间价格不能保证整团获得同价；酒店资料及截图见资料包。携程同日含早大床三晚7240.86元已核验，免费取消截止10月24日23:59；套餐赠送与官网不同。']];q.getRange('A14:I16').format={wrapText:true,verticalAlignment:'top'};
heading(p,'首发产品卡与需要核实的分工','保留旧初案供讨论；客群、城市、日期、资产口径和试价尚未最终确定。商业活动可服务有伴侣及已婚客户，婚恋专场单独筛选。');
p.getRange('A5:G5').values=[['产品','客户及首次购买理由','研究试价及包含','交付流程','团队与工时','回来参加的理由','待确认与负责人']];p.getRange('A5:G5').format={fill:ink,font:{bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:35};
const pr=D.models.map(m=>[m.name,m.customer+'\n'+m.reason,m.price+'元／人，仅研究试价\n'+m.rights,m.flow.join('\n'),m.team+'\n团队合计'+m.hours+'小时',m.retention,'Olivia：客户访谈和同条件询价；格格：可兑现资源；双方：A8口径、城市、日期、预算与执行人员。']);p.getRange('A6:G8').values=pr;p.getRange('A6:G8').format={wrapText:true,verticalAlignment:'top',rowHeight:330};
for(const[i,width]of[29,63,65,83,57,60,62].entries())p.getRangeByIndexes(0,i,15,1).format.columnWidth=width;p.tables.add('A5:G8',true,'LaunchProducts');
p.getRange('A6:G8').format.fill='#FFFFFF';p.getRange('A6:G6').format.fill='#F1F4F6';p.getRange('A8:G8').format.fill='#F1F4F6';
w.recalculate();
const tests=[];
for(let code=1;code<=3;code++){s.getRange('B4').values=[[code]];w.recalculate();let got=s.getRange('D24').values[0][0],expected=D.results.travel[code-1].contribution;if(Math.abs(got-expected)>.01)throw Error('人数贡献未对齐 '+code+' '+got);tests.push({case:code,travelContribution:got,cash:s.getRange('D36').values[0][0]});}
s.getRange('B4').values=[[3]];s.getRange('H18').values=[[18]];w.recalculate();if(Math.abs(s.getRange('D24').values[0][0]-(D.results.travel[2].contribution-9800))>.01)throw Error('车辆跨档未扣整车');tests.push({vehicleStep:s.getRange('D20').values[0][0]});s.getRange('H18').values=[[19]];
s.getRange('H11').values=[[null]];w.recalculate();if(typeof s.getRange('D24').values[0][0]!=='string'||typeof s.getRange('D36').values[0][0]!=='string')throw Error('缺失房价未阻止虚假盈利');tests.push({missingHotel:s.getRange('D24').values[0][0]});s.getRange('H11').values=[[7870]];s.getRange('B4').values=[[2]];w.recalculate();
if(s.getRange('D26').values[0][0]!==9)throw Error('保本人数错误 '+s.getRange('D26').values[0][0]);
const baselineCash=s.getRange('D36').values[0][0];s.getRange('H21').values=[[.5]];w.recalculate();
const changedCash=s.getRange('D36').values[0][0],expectedCash=baselineCash-SUM_OTHER()*D.models[2].base*.2;
function SUM_OTHER(){return 1600+1100+300+500;}
if(Math.abs(changedCash-expectedCash)>.01||s.getRange('D30').values[0][0]!==.5)throw Error('旅行预付比例未联动');
tests.push({otherPrepay:.5,cash:changedCash,expectedCash});s.getRange('H21').values=[[.7]];w.recalculate();
const errors=await w.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|not implemented',options:{useRegex:true,maxResults:30},maxChars:1800});
await fs.writeFile(B+'qa/模型验证.json',JSON.stringify({tests,restoredContribution:s.getRange('D24').values[0][0],cash:s.getRange('D36').values[0][0],breakeven:s.getRange('D26').values[0][0],errorScan:errors.ndjson,annualUtilization:s.getRange('I60').values[0][0]},null,2));
for(const[sheetName,range,key]of[['启动测算','A4:D37','单次测算'],['启动测算','F5:I27','成本输入'],['启动测算','A54:I65','年度产能'],['启动测算','A40:D50','工时现金说明'],['报价与条款','A5:F8','报价条款'],['产品卡与分工','A5:D7','产品卡'],['报价与条款',`A${quoteLast}:I${quoteLast}`,'携程核价行']]){const blob=await w.render({sheetName,range,scale:1,format:'png'});await fs.writeFile(B+'qa/'+key+'.png',new Uint8Array(await blob.arrayBuffer()));}
await fs.writeFile(B+'链接索引.json',JSON.stringify(links));const out=await SpreadsheetFile.exportXlsx(w);await out.save(B+'交付文件/启动产品与费用测算.xlsx');console.log(JSON.stringify({contribution:s.getRange('D24').values[0][0],cash:s.getRange('D36').values[0][0],breakeven:s.getRange('D26').values[0][0],tests}));
