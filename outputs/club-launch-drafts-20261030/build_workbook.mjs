import fs from 'node:fs/promises';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const B=decodeURIComponent(new URL('.',import.meta.url).pathname),w=Workbook.create();
const a=w.worksheets.add('单场活动'),m=w.worksheets.add('会员交付'),p=w.worksheets.add('人员薪酬'),c=w.worksheets.add('启动现金');
const ink='#243E35',fmt='#,##0.00;(#,##0.00);"—"';
function value(s,cell,x){s.getRange(cell).values=[[x]];}
function input(s,cell,x){value(s,cell,x);s.getRange(cell).format={fill:'#FFF2CC',font:{color:'#0000FF'}};}
function formula(s,cell,f,cross=false){s.getRange(cell).formulas=[['='+f]];s.getRange(cell).format.font.color=cross?'#008000':'#000000';}
function band(s,r,last='G'){s.getRange(`C${r}:${last}${r}`).format={fill:ink,font:{bold:true,color:'#FFFFFF'},rowHeight:30};}
for(const s of[a,m,p,c]){s.showGridLines=false;s.getRange('A1:B80').format.columnWidth=3;s.getRange('C1:G80').format={font:{name:'Arial',size:11,color:ink},rowHeight:25,verticalAlignment:'center'};s.getRange('C1:C80').format.columnWidth=34;s.getRange('D1:G80').format.columnWidth=20;s.getRange('D5:G80').setNumberFormat(fmt);s.freezePanes.freezeRows(7);}
function title(s,t,note){value(s,'C2',t);s.getRange('C2').format={font:{size:16,bold:true},rowHeight:36};value(s,'C3',note);s.getRange('C3').format={font:{size:10,color:'#66746A'},rowHeight:25};}
function labels(s,rows){for(const[r,t]of Object.entries(rows))value(s,'C'+r,t);}
title(a,'单场主题下午茶测算','黄色蓝字可改。人民币预算示例，未扣公司税费和其他固定开支。');
labels(a,{5:'单场贡献',6:'建议成行人数',7:'指标与输入',14:'实际参加人数',15:'研究试价 元/人',16:'退款金额预留比例',17:'支付手续费预算比例',18:'单人获客预算',19:'单人茶点预算',20:'单人物料预算',21:'场地预算',22:'主持预算',23:'摄影预算',24:'执行工时预算',25:'其他固定预算',26:'建议成行人数',28:'输入是否有效',29:'未扣退款收款额',30:'退款预留',31:'扣退款后收款',32:'茶点与物料支出',33:'固定交付支出',34:'获客支出',35:'支付手续费',36:'单场贡献',37:'贡献率',38:'单人边际贡献',39:'财务保本人数',41:'成行提示'});
band(a,7);for(const[r,x]of Object.entries({14:12,15:880,16:.03,17:.006,18:80,19:200,20:40,21:1800,22:1000,23:800,24:480,25:300,26:10}))input(a,'D'+r,x);
for(const r of[16,17,37])a.getRange('D'+r).setNumberFormat('0.0%');
formula(a,'D28','AND(COUNT(D14:D26)=13,MIN(D14:D26)>=0,D15>0,D16<1,D17<1,D26>0,D14=INT(D14),D26=INT(D26))');
const af={29:'D14*D15',30:'D29*D16',31:'D29-D30',32:'D14*SUM(D19:D20)',33:'SUM(D21:D25)',34:'D14*D18',35:'D31*D17',36:'D31-SUM(D32:D35)',37:'IF(D31>0,D36/D31,"无收款")',38:'D15*(1-D16)*(1-D17)-SUM(D18:D20)',39:'IF(D38>0,ROUNDUP(D33/D38,0),"本价格无法保本")',41:'IF(D14>=D26,"达到建议人数，另核客户结构","低于建议人数，先决定改期或获客试办")'};
for(const[r,f]of Object.entries(af))formula(a,'D'+r,`IF(D28,${f},"需补有效输入")`);
formula(a,'D5','D36');formula(a,'D6','D26');
value(a,'F14','来源：本次预算建议');value(a,'F16','场地1800不是Lust/梵悦报价');value(a,'F18','未自动赠送年费会籍');value(a,'F20','支付手续费按扣退款收款测算');value(a,'F22','执行480元为6小时×80预算');value(a,'F24','实际工时和供应价格回来后替换');
a.getRange('D41:G42').merge();a.getRange('D41:G42').format.wrapText=true;
a.getRange('D36').conditionalFormats.add('cellIs',{operator:'lessThan',formula:0,format:{fill:'#FCE8E6',font:{color:'#A12720'}}});

title(m,'会员交付与名额成本','仅为建议配置。名额数已确认，名额等级未定；不把赠送名额计成新增收款。');
value(m,'C4','名额类型 1基础 2理事');input(m,'D4',2);m.getRange('D4').setNumberFormat('0');m.getRange('D4').dataValidation={rule:{type:'whole',operator:'between',formula1:1,formula2:2}};
m.getRange('C7:G7').values=[['项目','基础','理事','合作39,800','合作98,000']];band(m,7);
for(const[r,t]of Object.entries({8:'每档收款价格',9:'本人全年履约成本',10:'配套名额人数',11:'名额单人履约成本',12:'配套名额总成本',13:'合作服务成本',14:'直接履约成本合计',15:'单档获客预算',16:'普通会员销售佣金比例',17:'支付手续费预算比例',18:'销售佣金',19:'支付手续费',20:'直接贡献 未扣公司固定开支',21:'直接贡献率',23:'履约输入是否有效',25:'履约单价及权益数量',26:'沙龙每席分摊成本',27:'晚宴每席分摊成本',28:'兴趣体验每席分摊成本',29:'年度服务每小时成本',30:'基础入会沟通成本',31:'理事交流沟通每次成本',32:'基础沙龙次数',33:'基础年度服务小时',34:'理事沙龙次数',35:'理事晚宴次数',36:'理事体验次数',37:'理事交流沟通次数',38:'理事年度服务小时',40:'基础单人年履约成本',41:'理事单人年履约成本',44:'付费销售人数 假设',46:'理事等级服务人数 含名额',47:'基础等级服务人数 含名额',48:'实际服务人数',49:'年度签约收款情景',50:'年度承诺履约预算',51:'获客佣金及支付预算',52:'年度直接贡献',54:'活动席位及产能',55:'沙龙',56:'晚宴',57:'兴趣体验',58:'产能判断',60:'年度沙龙场次',61:'每场沙龙人数',62:'年度晚宴场次',63:'每场晚宴人数',64:'年度体验场次',65:'每场体验人数'}))value(m,'C'+r,t);
for(const[r,x]of Object.entries({26:120,27:800,28:600,29:80,30:120,31:120,32:2,33:2,34:12,35:4,36:2,37:4,38:22,60:24,61:12,62:4,63:20,64:4,65:16}))input(m,'D'+r,x);
formula(m,'D23','AND(COUNT(D26:D38)=13,MIN(D26:D38)>=0,OR(D4=1,D4=2))');
formula(m,'D40','IF(D23,D26*D32+D30+D29*D33,"缺少履约输入")');formula(m,'D41','IF(D23,D26*D34+D27*D35+D28*D36+D31*D37+D29*D38,"缺少履约输入")');
for(const[i,col]of['D','E','F','G'].entries()){
 input(m,col+'8',[1280,19800,39800,98000][i]);value(m,col+'10',[0,0,3,6][i]);m.getRange(col+'10').setNumberFormat('0');
 input(m,col+'13',[0,0,5000,20000][i]);input(m,col+'15',[300,1500,3000,5000][i]);input(m,col+'16',i<2?.05:0);formula(m,col+'17',"'单场活动'!D17",true);m.getRange(col+'16:'+col+'17').setNumberFormat('0.0%');m.getRange(col+'21').setNumberFormat('0.0%');
 const f={9:i===0?'$D$40':'$D$41',11:i<2?'0':'IF($D$4=1,$D$40,$D$41)',12:`${col}10*${col}11`,14:`SUM(${col}9,${col}12:${col}13)`,18:`${col}8*${col}16`,19:`${col}8*${col}17`,20:`${col}8-${col}14-${col}15-${col}18-${col}19`,21:`IF(${col}8>0,${col}20/${col}8,"缺少价格")`};
 for(const[r,expr]of Object.entries(f))formula(m,col+r,`IF($D$23,${expr},"缺少履约输入")`);
}
m.getRange('D8:G8').format.font.color='#000000';value(m,'F24','3/6个名额不可直接转成销售收入');
m.getRange('C44:G44').values=[['付费人数假设','基础','理事','合作39,800','合作98,000']];band(m,44);
for(const[i,col]of['D','E','F','G'].entries())input(m,col+'45',[6,8,4,2][i]);m.getRange('D45:G45').setNumberFormat('0');
const mf={46:'E45+F45+G45+IF($D$4=2,F45*F10+G45*G10,0)',47:'D45+IF($D$4=1,F45*F10+G45*G10,0)',48:'SUM(D46:D47)',49:'SUMPRODUCT(D8:G8,D45:G45)',50:'SUMPRODUCT(D14:G14,D45:G45)',51:'SUMPRODUCT(D15:G15,D45:G45)+SUMPRODUCT(D18:G18,D45:G45)+SUMPRODUCT(D19:G19,D45:G45)',52:'D49-D50-D51'};
for(const[r,f]of Object.entries(mf))formula(m,'D'+r,`IF(AND($D$23,COUNT(D45:G45)=4,MIN(D45:G45)>=0),${f},"缺少人数或履约输入")`);
m.getRange('C54:G54').values=[['活动席位及产能','全年需求','全年容量','余缺席位','说明']];band(m,54);
for(const[r,need,cap]of[[55,'D46*D34+D47*D32','D60*D61'],[56,'D46*D35','D62*D63'],[57,'D46*D36','D64*D65']]){formula(m,'D'+r,`IF(ISNUMBER(D46),${need},"待补")`);formula(m,'E'+r,cap);formula(m,'F'+r,`IF(ISNUMBER(D${r}),E${r}-D${r},"待补")`);value(m,'G'+r,'负值须增场或重配权益');}
formula(m,'D58','IF(COUNT(F55:F57)=3,IF(MIN(F55:F57)>=0,"本假设容量满足","席位不足，需增场或调整"),"待补输入")');m.getRange('D58:G58').merge();m.getRange('D58:G58').format.wrapText=true;
m.getRange('D20:G20').conditionalFormats.add('cellIs',{operator:'lessThan',formula:0,format:{fill:'#FCE8E6',font:{color:'#A12720'}}});m.getRange('F55:F57').conditionalFormats.add('cellIs',{operator:'lessThan',formula:0,format:{fill:'#FCE8E6',font:{color:'#A12720'}}});
value(m,'F27','沙龙120＝场次成本按席分摊假设');value(m,'F29','4次理事沟通＋22小时服务');value(m,'F31','名额全部使用，按足额预留');value(m,'F33','全年活动成本不再重复相加');value(m,'F35','公司人员与税费尚未扣除');value(m,'F37','合作服务5000/20000为预算');
for(const s of[a,m,p,c])s.getRange('F1:G80').format.columnWidth=24;

title(p,'人员薪酬与外包预算','全职方案A。工资与比例是建议预算，非市场调查或已签用工条件。');
labels(p,{5:'月度人员及外包现金预算',7:'输入与计算',8:'固定底薪预算',9:'绩效上限预算',10:'绩效完成比例',11:'附加用工成本预留比例',12:'基础会员新签单数',13:'理事新签单数',14:'当月新签退款',15:'续费净到账',16:'新签计奖比例',17:'续费计奖比例',18:'图文篇数',19:'每篇预算',20:'摄影次数',21:'每次摄影预算',22:'员工成交归属比例',24:'输入是否有效',25:'新签净到账',26:'续费净到账',27:'新签佣金',28:'续费佣金',29:'绩效预算',30:'底薪及绩效',31:'附加用工预算',32:'内容与摄影外包',33:'固定人员含附加预算',34:'人员及外包合计',36:'无销售时月固定及外包预算'});band(p,7);
for(const[r,x]of Object.entries({8:6000,9:1000,10:.8,11:.25,12:8,13:2,14:3000,15:19800,16:.05,17:.02,18:8,19:200,20:2,21:800,22:1}))input(p,'D'+r,x);
for(const r of[10,11,16,17,22])p.getRange('D'+r).setNumberFormat('0.0%');
formula(p,'D24',"AND(COUNT(D8:D22)=15,MIN(D8:D22)>=0,D10<=1,D11<=1,D16<=1,D17<=1,D22<=1,D14<=D12*'会员交付'!D8+D13*'会员交付'!E8)");
const pf={25:"D12*'会员交付'!D8+D13*'会员交付'!E8-D14",26:'D15',27:'D25*D16*D22',28:'D26*D17*D22',29:'D9*D10',30:'D8+D29',31:'D30*D11',32:'D18*D19+D20*D21',33:'D30+D31',34:'SUM(D27:D28)+D32+D33',36:'D32+D33'};
for(const[r,f]of Object.entries(pf))formula(p,'D'+r,`IF(D24,${f},"需补有效输入")`,[25].includes(+r));formula(p,'D5','D34');
value(p,'F8','附加25%只是费用预留，不是法定费率');value(p,'F11','39,800/98,000合作档不自动计佣');value(p,'F14','按净到账计奖，归属比例另确认');value(p,'F17','退款不可超过本情景新签总额');value(p,'F20','年度会员表已有计佣，不重复叠加');value(p,'F23','与兼职3000/月方案分别选择');

title(c,'三个月启动现金预算','先按无会员收入测底线，不以未来收款替代履约资金。人民币预算。');
labels(c,{5:'未扣现有资金的启动准备额',6:'尚需资金',7:'输入与计算',8:'律师工作预算',9:'品牌及材料制作预算',10:'基础物料与工具预算',11:'账户与财税准备预算',12:'机动预算比例',13:'固定成本预留月数',14:'每月固定人员及外包',15:'首场供应预付比例',16:'首场额外退款现金预留',17:'已可动用启动资金',20:'一次准备预算',21:'三个月人员外包预算',22:'首场锁定与获客现金',23:'机动预算',24:'启动准备额',25:'尚需准备资金'});band(c,7);
for(const[r,x]of Object.entries({8:8000,9:3000,10:2000,11:1500,12:.15,13:3,15:.7,16:1000,17:0}))input(c,'D'+r,x);
formula(c,'D14',"'人员薪酬'!D36",true);for(const r of[12,15])c.getRange('D'+r).setNumberFormat('0.0%');
formula(c,'D19',"AND(COUNT(D8:D17)=10,MIN(D8:D17)>=0,D12<=1,D15<=1,ISNUMBER('单场活动'!D33))");value(c,'C19','输入是否有效');
const cf={20:'SUM(D8:D11)',21:'D13*D14',22:"('单场活动'!D32+'单场活动'!D33)*D15+'单场活动'!D34",23:'SUM(D20:D22)*D12',24:'SUM(D20:D23)+D16',25:'MAX(D24-D17,0)'};
for(const[r,f]of Object.entries(cf))formula(c,'D'+r,`IF(D19,${f},"需补有效输入")`,+r===22);formula(c,'D5','D24');formula(c,'D6','D25');
value(c,'F8','律师8000为预留，不是已取得报价');value(c,'F11','账户财税1500为预算占位');value(c,'F14','全职A方案含绩效0.8预留');value(c,'F17','不含未确认办公室与额外旅行团');value(c,'F20','工资现金与会员工时成本不重复加总');
for(const s of[a,m,p,c]){s.getRange('D5:G6').format.font.bold=true;s.getRange('F1:G80').format.font.size=10;s.getRange('D5:G80').format.rowHeight=25;}
a.getRange('C8:G13').format.rowHeight=4;
for(const r of[14,26,28,39])a.getRange('D'+r).setNumberFormat('0');
for(const r of[4,23,32,33,34,35,36,37,38,46,47,48,60,61,62,63,64,65])m.getRange('D'+r).setNumberFormat('0');
m.getRange('D55:F57').setNumberFormat('0');
for(const r of[12,13,18,20,24])p.getRange('D'+r).setNumberFormat('0');
c.getRange('D13').setNumberFormat('0');c.getRange('D19').setNumberFormat('0');
value(a,'C28','校验 1有效 0待补');value(m,'C23','校验 1有效 0待补');value(p,'C24','校验 1有效 0待补');value(c,'C19','校验 1有效 0待补');
w.recalculate();const tests=[];
function near(x,y,n){if(typeof x!=='number'||Math.abs(x-y)>.015)throw Error(n+' '+x+' expected '+y);}
for(const n of[8,10,12,16]){value(a,'D14',n);w.recalculate();let expected=n*880*.97*.994-n*320-4380;near(a.getRange('D36').values[0][0],expected,'event');tests.push({people:n,contribution:a.getRange('D36').values[0][0]});}value(a,'D14',12);
for(const code of[1,2]){value(m,'D4',code);w.recalculate();near(m.getRange('F20').values[0][0],code===1?21921.2:-758.8,'coop39');near(m.getRange('G20').values[0][0],code===1?61212:15852,'coop98');tests.push({slotType:code,coop39:m.getRange('F20').values[0][0],coop98:m.getRange('G20').values[0][0],served:m.getRange('D48').values[0][0],capacity:m.getRange('D58').values[0][0]});}
value(m,'D26',null);w.recalculate();if(typeof m.getRange('F20').values[0][0]!=='string')throw Error('missing fulfillment not blocked');value(m,'D26',120);value(m,'D4',2);value(a,'D21',null);w.recalculate();if(typeof a.getRange('D36').values[0][0]!=='string')throw Error('missing venue not blocked');value(a,'D21',1800);
w.recalculate();near(m.getRange('D40').values[0][0],520,'basic cost');near(m.getRange('D41').values[0][0],8080,'core cost');near(p.getRange('D27').values[0][0],2342,'commission');
const scan=await w.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!',options:{useRegex:true,maxResults:30},maxChars:2000});
await fs.writeFile(B+'qa/成本模型核验.json',JSON.stringify({tests,missing_inputs_blocked:true,basicCost:m.getRange('D40').values[0][0],coreCost:m.getRange('D41').values[0][0],salary:p.getRange('D34').values[0][0],startup:c.getRange('D24').values[0][0],formulaErrorScan:scan.ndjson},null,2));
for(const [sheetName,range,name]of[['单场活动','C5:G39','单场'],['会员交付','C4:G21','会员'],['会员交付','C44:G58','产能'],['人员薪酬','C7:G34','薪酬'],['启动现金','C5:G25','启动']]){const blob=await w.render({sheetName,range,scale:1,format:'png'});await fs.writeFile(B+'qa/'+name+'.png',new Uint8Array(await blob.arrayBuffer()));}
await(await SpreadsheetFile.exportXlsx(w)).save(B+'交付文件/俱乐部成本与薪酬测算.xlsx');console.log('Workbook tests passed',JSON.stringify(tests));
