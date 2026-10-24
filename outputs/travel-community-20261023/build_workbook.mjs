import fs from 'node:fs/promises';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const B=decodeURIComponent(new URL('.',import.meta.url).pathname),d=JSON.parse(await fs.readFile(B+'研究与产品数据.json','utf8'));
const w=Workbook.create(),names=['对标主表','同线路费用','首发产品与测算','来源与待补','既有机构名录'];
for(const n of names){let s=w.worksheets.add(n);s.showGridLines=false;}
const links=[];let tn=0;
const font='Arial',ink='#243442',money='#,##0;(#,##0);"—"';
function table(name,title,headers,rows,widths){
 const s=w.worksheets.getItem(name),last=String.fromCharCode(64+headers.length),end=5+rows.length;
 s.getRange(`A1:${last}${end}`).format={font:{name:font,size:11,color:ink},verticalAlignment:'center'};
 s.getRange('A2').values=[[title]];s.getRange('A2').format.font={size:16,bold:true};s.getRange('A2').format.rowHeight=34;
 s.getRange(`A5:${last}5`).values=[headers];s.getRange(`A5:${last}5`).format={fill:ink,font:{bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:34,horizontalAlignment:'center'};
 if(rows.length)s.getRange(`A6:${last}${end}`).values=rows;
 for(let i=0;i<widths.length;i++)s.getRangeByIndexes(0,i,end,1).format.columnWidth=widths[i];
 if(rows.length){let body=s.getRange(`A6:${last}${end}`);body.format.wrapText=true;body.format.verticalAlignment='top';
  for(let i=0;i<rows.length;i++){const lines=Math.max(...rows[i].map((v,j)=>String(v??'').split('\n').reduce((n,t)=>n+Math.max(1,Math.ceil([...t].reduce((a,c)=>a+(/[^\x00-\xff]/.test(c)?1:.52),0)/Math.max(5,widths[j]*.46))),0)));s.getRange(`A${i+6}:${last}${i+6}`).format.rowHeight=Math.max(35,lines*15+10);}}
 for(let i=6;i<=end;i++)if(i%2===0)s.getRange(`A${i}:${last}${i}`).format.fill='#F4F6F8';
 s.tables.add(`A5:${last}${end}`,true,'ResearchProducts'+(++tn));s.freezePanes.freezeRows(5);s.freezePanes.freezeColumns(1);return s;
}
const source=Object.fromEntries(d.sources.map(x=>[x.id,x]));
const rows=d.cases.map(c=>[c.name+'\n'+c.group,c.product,c.customer,c.price,c.rights,c.flow,c.acquisition+'\n'+c.performance,c.judgment,c.sources.join('、')]);
for(const c of d.foreign)rows.push([c.name+'\n国外活动参考','会籍与活动',c.what,c.fees,'详见收费与活动说明',c.activity,'本轮未取得可核的利润及留存数据',c.judgment,c.sources.join('、')]);
const main=table('对标主表','高端单身旅行与社群对标',['机构及组织方式','产品','客户与准入','收费及单位','包含权益','组织流程','获客与经营表现','我们的判断','来源'],rows,[25,24,48,40,48,48,48,48,15]);
main.getRange('A3').values=[['国内12个对象13个产品，国外9个参考；产品逐行。BoL身份已由Olivia确认。']];
rows.forEach((r,i)=>{let u=source[r[8].split('、')[0]]?.url;if(u)links.push({sheet:0,cell:'I'+(i+6),url:u});});
const costRows=d.costs.map(r=>[...r.slice(0,6),null,r[6]]);
costRows.splice(5,0,['三亚','同上','同上','服务协调每人',500,1,null,'规划假设；使单人直接交付预算合计8700元']);
const cost=table('同线路费用','同线路费用与询价条件',['线路','研究日期','统一条件','成本项目','单价 元','数量','人均金额 元','价格状态'],costRows,[18,25,58,28,18,12,20,53]);
cost.getRange('A3').values=[['研究用日期，不是已确认排期；以下均为规划假设，未取得相同日期的三方成交报价。']];
for(let r=6;r<6+costRows.length;r++)cost.getRange(`G${r}`).formulas=[[`=E${r}*F${r}`]];
cost.getRange(`E6:G${costRows.length+5}`).setNumberFormat(money);cost.getRange(`E6:F${costRows.length+5}`).format.font={color:'#0000FF'};
cost.getRange('I5:K5').values=[['供应商或自订渠道','同口径单价 元','有效日期及条件']];cost.getRange('I5:K5').format={fill:ink,font:{color:'#FFFFFF',bold:true},wrapText:true};cost.getRange(`I6:K${costRows.length+5}`).format.fill='#FFF2CC';cost.getRange(`J6:J${costRows.length+5}`).setNumberFormat(money);cost.getRange('I1:I25').format.columnWidth=28;cost.getRange('J1:J25').format.columnWidth=25;cost.getRange('K1:K25').format.columnWidth=38;
const start=costRows.length+9;
const comp=[['路线','单身社交团','精品私家团','自行预订'],['三亚四天三晚','产品试价19800；机票自理','同口径报价未取得','机酒等实时价格未取得'],['北京周边两天一晚','仅研究方向，未设首发售价','同口径报价未取得','同口径价格未取得']];
cost.getRange(`A${start}:D${start+2}`).values=comp;cost.getRange(`A${start}:D${start}`).format={fill:ink,font:{bold:true,color:'#FFFFFF'}};cost.getRange(`A${start+1}:D${start+2}`).format={wrapText:true,rowHeight:55};

const m=w.worksheets.getItem('首发产品与测算');m.getRange('A1:H67').format={font:{name:font,size:11,color:ink},verticalAlignment:'center'};
m.getRange('A2').values=[['首发产品与单次经营测算']];m.getRange('A2').format.font={size:16,bold:true};m.getRange('A2').format.rowHeight=34;
m.getRange('A3').values=[['规划基准，可修改蓝字输入；成本与试价未获供应商或客户确认。']];
m.getRange('A5:D5').values=[['项目',...d.products.map(p=>p.name)]];m.getRange('A5:D5').format={fill:ink,font:{bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:42};
const labels={6:'试价 元／人',7:'付费人数',8:'人数上限',9:'单人直接交付成本',10:'单人获客预算',11:'固定交付及工时成本',12:'退款金额占收款比例',13:'筹备现场回访总工时',15:'含退款前销售额',16:'退款情景金额',17:'扣退款后收入',18:'直接交付成本',19:'获客支出',20:'固定交付及工时成本',21:'单次贡献',22:'贡献率',23:'保本人数 向上取整',25:'收款前筹备与获客现金',26:'客户首付款比例',27:'供应商预付直接成本比例',28:'供应商首次付款',29:'首付款到账后累计现金',30:'退款现金预留',31:'建议启动周转金',32:'完成及结清后的现金',33:'扣退款预留后可用现金'};
for(const [r,l]of Object.entries(labels))m.getRange('A'+r).values=[[l]];
for(let i=0;i<3;i++){
 const c=String.fromCharCode(66+i),p=d.products[i];
 const vals={6:p.price,7:p.base,8:p.capacity,9:p.var,10:p.cac,11:p.fixed,12:.03,13:p.hours,26:.3,27:.7};
 for(const[r,v]of Object.entries(vals)){m.getRange(c+r).values=[[v]];m.getRange(c+r).format={fill:'#FFF2CC',font:{color:'#0000FF'}};}
 const f={15:`${c}6*${c}7`,16:`${c}15*${c}12`,17:`${c}15-${c}16`,18:`${c}7*${c}9`,19:`${c}7*${c}10`,20:`${c}11`,21:`${c}17-SUM(${c}18:${c}20)`,22:`${c}21/${c}17`,23:`IF(${c}6*(1-${c}12)-${c}9-${c}10<=0,"无保本人数",ROUNDUP(${c}11/(${c}6*(1-${c}12)-${c}9-${c}10),0))`,25:`${c}11*40%+${c}19`,28:`${c}18*${c}27`,29:`${c}15*${c}26-${c}28-${c}20-${c}19`,30:`${c}15*${c}12`,31:`MAX(${c}25,-${c}29,0)+${c}30`,32:`${c}15-SUM(${c}18:${c}20)`,33:`${c}32-${c}30`};
 for(const[r,v]of Object.entries(f))m.getRange(c+r).formulas=[['='+v]];
 m.getRange(`${c}6:${c}33`).setNumberFormat(money);for(const r of [12,22,26,27])m.getRange(c+r).setNumberFormat('0.0%');
 m.getRange(`${c}7`).dataValidation={rule:{type:'whole',operator:'between',formula1:1,formula2:p.capacity}};
}
m.getRange('D9').formulas=[["=SUM('同线路费用'!G6:G11)"]];m.getRange('D9').format.font={color:'#008000'};
for(const r of [17,21,23,31,33])m.getRange(`A${r}:D${r}`).format={fill:'#E8EDF1',font:{bold:true},rowHeight:28};
m.getRange('A35').values=[['人数与票价变化后的单次贡献']];m.getRange('A35').format.font={bold:true};
// Each native table varies the actual model inputs and reads the one build above.
for(let i=0;i<3;i++){
 const c=String.fromCharCode(66+i),r=37+i*7,p=d.products[i];
 m.getRange('A'+r).values=[[p.name+'，左列低于预期／基准／满团人数']];
 m.getRange(`A${r+1}`).formulas=[[`=${c}21`]];m.getRange(`B${r+1}:D${r+1}`).values=[[Math.round(p.price*.85),p.price,Math.round(p.price*1.1)]];
 m.getRange(`A${r+2}:A${r+4}`).values=[[p.low],[p.base],[p.full]];
 m.dataTables.add(`A${r+1}:D${r+4}`,{rowInput:c+'6',columnInput:c+'7'});
 m.getRange(`A${r+1}:D${r+4}`).setNumberFormat(money);m.getRange(`A${r+1}`).setNumberFormat(';;;');
 m.getRange(`B${r+1}:D${r+1}`).format.fill='#E8EDF1';m.getRange(`A${r+2}:A${r+4}`).format.fill='#E8EDF1';
}
m.getRange('F37').values=[['旅行退款金额比例与人数对贡献的影响']];m.getRange('F38').formulas=[['=D21']];m.getRange('G38:I38').values=[[0,.03,.1]];m.getRange('F39:F41').values=[[10],[14],[16]];
m.dataTables.add('F38:I41',{rowInput:'D12',columnInput:'D7'});m.getRange('F38').setNumberFormat(';;;');m.getRange('G38:I38').setNumberFormat('0%');m.getRange('G39:I41').setNumberFormat(money);
m.getRange('F44:G47').values=[['旅行人数情景','单团贡献 元'],['低于预期10人',null],['基准14人',null],['满团16人',null]];m.getRange('G45:G47').formulas=[['=C53'],['=C54'],['=C55']];m.getRange('G45:G47').setNumberFormat(money);
const chart=m.charts.add('bar',m.getRange('F44:G47'));chart.title='旅行人数与单团贡献';chart.hasLegend=false;chart.setPosition('F49','M63');chart.titleTextStyle.typeface=font;chart.titleTextStyle.fontSize=14;chart.yAxis={numberFormatCode:'#,##0',numberFormatSourceLinked:false,textStyle:{typeface:font,fontSize:11}};chart.xAxis={axisType:'textAxis',textStyle:{typeface:font,fontSize:11}};chart.series.items[0].fill='#26475A';
m.getRange('F5').values=[['固定成本构成']];m.getRange('F6:G9').values=[['产品','元'],['晚宴工时70×100及场地1500',8500],['分享工时52×100、讲师2000及场地800',8000],['旅行工时190×150、团队机酒10500、场地5000与器材4000',48000]];
m.getRange('F6:G9').format.wrapText=true;m.getRange('F7:F9').format.rowHeight=58;
m.getRange('F12').values=[['现金口径']];m.getRange('F13').values=[['收款前先付40%固定成本及全部获客；首款到账后付70%直接成本并结清其余固定成本；尾款后结清。退款比例仅为情景，按全部交付成本已发生保守计算。']];m.getRange('F13:H17').merge();m.getRange('F13:H17').format={wrapText:true,verticalAlignment:'top'};
m.getRange('F20').values=[['贡献不是公司净利润']];m.getRange('F21:H24').merge();m.getRange('F21').values=[['已含项目工时机会成本与获客预算，未计公司日常固定开支、税费及未售出活动的研发投入。旅行19800为研究试价，尚无愿付证明。']];m.getRange('F21:H24').format={wrapText:true,verticalAlignment:'top'};
m.getRange('A56').values=[['产品交付与后续购买']];
for(let i=0;i<3;i++){let r=58+i*3;m.getRange(`A${r}:D${r+1}`).merge();m.getRange(`A${r}`).values=[[d.products[i].name+'：'+d.products[i].rights+'\n后续：'+d.products[i].retention]];m.getRange(`A${r}:D${r+1}`).format={wrapText:true,verticalAlignment:'top',rowHeight:42};}
for(const[a,width]of[['A',38],['B',24],['C',24],['D',24],['E',3],['F',35],['G',18],['H',18],['I',18]])m.getRange(a+'1:'+a+'66').format.columnWidth=width;
m.getRange('A6:D33').format.rowHeight=26;
m.getRange('F26:H29').merge();m.getRange('F26').values=[['现金保守按项目工时报酬全部支付计算，包含合伙人工时预算。若延期支付，需按实际付款时间重算周转金。']];m.getRange('F26:H29').format={wrapText:true,verticalAlignment:'top'};

const sr=d.sources.map(s=>[s.id,s.name,s.kind,s.period,s.note,s.url||'用户私有资料，无公开链接']);
const so=table('来源与待补','来源与待补资料',['编号','资料','类别','适用时间','使用说明','原文入口'],sr,[12,36,25,34,67,55]);
for(let i=0;i<d.sources.length;i++)if(d.sources[i].url)links.push({sheet:3,cell:'F'+(i+6),url:d.sources[i].url});
let gr=sr.length+9;so.getRange(`A${gr}:E${gr}`).values=[['待补项目','具体内容','负责人','状态','取得什么证据']];so.getRange(`A${gr}:E${gr}`).format={fill:ink,font:{bold:true,color:'#FFFFFF'}};so.getRange(`A${gr+1}:E${gr+d.gaps.length}`).values=d.gaps;so.getRange(`A${gr+1}:E${gr+d.gaps.length}`).format={wrapText:true,rowHeight:70};
const ms=table('既有机构名录','既有36家机构及本轮用途',['机构','组织方式','地区','目标客户','本轮用途','原文'],d.market.map(r=>[r[0],r[1],r[2],r[3],/正和岛|优家荟/.test(r[0])?'按用户要求排除当前推荐，仅保留历史记录':r[0].includes('马会')||r[0].includes('长江')?'成熟产品体系参考，不能推定启动售价':r[6]+'；按本轮产品重新筛选',r[5]]),[30,28,28,55,55,50]);
d.market.forEach((r,i)=>{if(r[5]?.startsWith('http'))links.push({sheet:4,cell:'F'+(i+6),url:r[5]});});
w.recalculate();
const results={};for(let i=0;i<3;i++){const c=String.fromCharCode(66+i);results[d.products[i].id]={contribution:m.getRange(c+'21').values[0][0],breakeven:m.getRange(c+'23').values[0][0],cash:m.getRange(c+'31').values[0][0],sensitivity:m.getRange(`A${39+i*7}:D${41+i*7}`).values};}
const baseline=m.getRange('D21').values[0][0];m.getRange('D7').values=[[10]];w.recalculate();const test1=m.getRange('D21').values[0][0];if(Math.abs(test1-(19800*10*.97-10*9900-48000))>.01)throw Error('Demand test failed');m.getRange('D7').values=[[14]];m.getRange('D12').values=[[.1]];w.recalculate();const test2=m.getRange('D21').values[0][0];if(Math.abs(test2-(19800*14*.9-14*9900-48000))>.01)throw Error('Refund test failed');m.getRange('D12').values=[[.03]];w.recalculate();if(m.getRange('D21').values[0][0]!==baseline)throw Error('Restore failed');
cost.getRange('E6').values=[[1600]];w.recalculate();const testCost=m.getRange('D21').values[0][0];if(Math.abs(testCost-(baseline-14*300))>.01)throw Error('Hotel cost dependency test failed');cost.getRange('E6').values=[[1500]];w.recalculate();if(m.getRange('D21').values[0][0]!==baseline)throw Error('Cost restore failed');
await fs.writeFile(B+'模型核查.json',JSON.stringify({results,tests:{demand10:test1,refund10pct:test2,hotelIncrease100:testCost,restored:baseline},refundSensitivity:m.getRange('F38:I41').values},null,2));
await fs.writeFile(B+'qa/公式检查.txt',JSON.stringify(await w.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!',options:{useRegex:true,maxResults:50},maxChars:3000})));
for(const[name,range]of[['对标主表','A5:D8'],['同线路费用','A5:H11'],['首发产品与测算','A5:D33'],['来源与待补','A5:F9'],['既有机构名录','A5:F9']]){try{const p=await w.render({sheetName:name,range,scale:1,format:'png'});await fs.writeFile(B+'qa/'+name+'.png',new Uint8Array(await p.arrayBuffer()));}catch(e){console.log('render',name,String(e).slice(0,100));}}
const out=await SpreadsheetFile.exportXlsx(w);await out.save(B+'deliverables/高端单身旅行与线下社群研究数据.xlsx');await fs.writeFile(B+'链接索引.json',JSON.stringify(links));console.log(JSON.stringify(results));
const rightPreview=await w.render({sheetName:'首发产品与测算',range:'F37:M63',scale:1,format:'png'});await fs.writeFile(B+'qa/敏感性与图表.png',new Uint8Array(await rightPreview.arrayBuffer()));
