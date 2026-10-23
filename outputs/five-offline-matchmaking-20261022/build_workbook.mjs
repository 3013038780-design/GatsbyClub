import fs from 'node:fs/promises';
import {Workbook,SpreadsheetFile} from '/Users/olivialee/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
const B=decodeURIComponent(new URL('.',import.meta.url).pathname);
const d=JSON.parse(await fs.readFile(B+'正式报告数据.json','utf8'));
const wb=Workbook.create();
const links=[];
let sheetIndex=0;
function urlFrom(value){if(typeof value!=='string')return null;if(value.startsWith('https://')||value.startsWith('http://'))return value.split('\n')[0];return d.sources[value.split('/')[0]]?.[1]||null;}
function sheet(name,headers,rows,widths,note){
 const s=wb.worksheets.add(name);s.showGridLines=false;const end=String.fromCharCode(64+headers.length);
 s.getRange(`A1:${end}${rows.length+5}`).format.font={name:'Microsoft YaHei',size:11,color:'#243442'};
 s.getRange('A2').values=[[name]];s.getRange('A2').format.font={size:16,bold:true};s.getRange('A2').format.rowHeight=32;
 s.getRange('A3').values=[[note]];s.getRange('A3').format.font={size:10,color:'#596570'};s.getRange('A3').format.rowHeight=26;
 s.getRange(`A5:${end}5`).values=[headers];s.getRange(`A5:${end}5`).format={fill:'#234458',font:{name:'Microsoft YaHei',size:11,bold:true,color:'#FFFFFF'},rowHeight:32,verticalAlignment:'center',horizontalAlignment:'center',wrapText:true};
 s.getRange(`A6:${end}${rows.length+5}`).values=rows;
 const body=s.getRange(`A6:${end}${rows.length+5}`);body.format.wrapText=true;body.format.verticalAlignment='center';body.format.rowHeight=name==='内容明细'?52:84;
 for(let c=0;c<headers.length;c++)s.getRangeByIndexes(0,c,rows.length+5,1).format.columnWidth=widths[c];
 for(let i=0;i<rows.length;i++){
  const r=i+6;if(i%2===0)s.getRange(`A${r}:${end}${r}`).format.fill='#F2F5F7';
  const target=urlFrom(rows[i].at(-1));if(target){const cell=String.fromCharCode(64+headers.length)+r;links.push({sheet:name,cell,url:target});s.getRange(cell).values=[['打开原文']];s.getRange(cell).format.font={color:'#235E84'};}
 }
 s.tables.add(`A5:${end}${rows.length+5}`,true,'ResearchTable'+(++sheetIndex));
 body.format.autofitRows();
 s.freezePanes.freezeRows(5);s.freezePanes.freezeColumns(1);
 return s;
}
const market=sheet('机构总览',['机构','组织方式','地区','客户及主要需求','研究用途','原文'],d.market.map(r=>[r[0],r[1],r[2],r[3],r[6]+'。'+r[4],r[5]]),[25,22,22,52,48,14],'36家机构；婚恋专项优先五家，原有会所、商学院及其他线下社群继续保留。');
const prices=sheet('收费权益',['机构及产品','金额 元','怎样收费及适用期','具体包含什么','尚未明确的合同内容','原文'],d.prices,[27,15,29,55,39,14],'先读此表。每行一个收费项目；空白金额表示尚未取得可靠报价，0表示明确免费。');
prices.getRange(`B6:B${d.prices.length+5}`).setNumberFormat('#,##0');prices.getRange(`B6:B${d.prices.length+5}`).format.horizontalAlignment='center';prices.getRange(`B6:B${d.prices.length+5}`).format.font={bold:true};
sheet('客户画像',['机构及产品或样例','年龄 职业 学历','收入与资产','性格与兴趣','描述对象及参加需求','原文'],d.profiles,[28,38,35,44,40,14],'分别标注机构定位、活动准入与公开样例；不把拟匹配对象的条件当成购买者画像。');
const acts=d.activities.map(r=>[r[0],/^\d{4}-\d{2}-\d{2}$/.test(r[1])?new Date(r[1]+'T12:00:00Z'):r[1],...r.slice(2)]);
const act=sheet('活动旅行',['机构','活动日期','记录状态','产品','元每人','公开流程','包含项 人群及人数','原文'],acts,[22,17,20,30,17,49,53,14],'日期相同不等于实际成行；预告、报名与回顾分别标注，10月24日以后的活动为未来招募。');
act.getRange(`B6:B${acts.length+5}`).setNumberFormat('yyyy-mm-dd');
const accounts=d.accounts.map(a=>[a.brand+'\n'+a.name,a.public_fans,a.public_likes_and_saves,'获赞与收藏合计',null,new Date(a.collected_at),a.verification,a.url]);
accounts.push(['大超说媒 抖音03',240000,10191000,'累计获赞',212,new Date('2026-10-22T12:00:00Z'),'前轮浏览器核验复用；与05号不作受众去重相加','https://www.douyin.com/user/MS4wLjABAAAAzS55hxJ4_NKjM9xZw8xHpGVx8sP-m2Bxy6ekRE2I7-Q']);
accounts.push(['大超说媒 抖音05',72000,1661000,'累计获赞',337,new Date('2026-10-22T12:00:00Z'),'前轮浏览器核验复用；与03号不作受众去重相加','https://www.douyin.com/user/MS4wLjABAAAALIHRWrJxwmo4LaeEqAPHHfrBlL_lexxrdc83OeXvSuysOixUI_5ys_rm2RCBgFX6']);
accounts.push(['我主良缘 抖音同名账号',3021,8756,'累计获赞',558,new Date('2026-10-22T12:00:00Z'),'主体未确认；可见首个非置顶样例为2024-08-15，不计本期活跃','https://www.douyin.com/user/MS4wLjABAAAA0OK7GRxomszaWxKkdVQTdRYFFH-AiQmGQVu8rME0Sec']);
const as=sheet('账号声量',['品牌及账号','粉丝数','累计互动数','累计指标口径','作品数','采集时间','账号核验与使用说明','原文'],accounts,[29,15,18,24,14,19,52,14],'账号快照各自列示；隐藏字段留空，累计互动不填成评论、分享或当期成交。');
as.getRange(`B6:C${accounts.length+5}`).setNumberFormat('#,##0');as.getRange(`E6:E${accounts.length+5}`).setNumberFormat('#,##0');as.getRange(`F6:F${accounts.length+5}`).setNumberFormat('yyyy-mm-dd');
const posts=d.posts.map(r=>[r[0],r[1],r[2],new Date(r[3]+'T12:00:00Z'),...r.slice(4)]);
const content=sheet('内容明细',['品牌','账号','平台','发布日期','内容主题','点赞','评论','收藏','分享','原文'],posts,[23,31,14,19,66,13,13,13,13,16],`观察窗2026-07-25至10-22；小红书${d.counts.current_xhs}条本轮样本，抖音14条复用，按内容去重。`);
content.getRange(`D6:D${posts.length+5}`).setNumberFormat('yyyy-mm-dd');content.getRange(`F6:I${posts.length+5}`).setNumberFormat('#,##0');
const m=wb.worksheets.add('经营测算');m.showGridLines=false;m.getRange('A1:I25').format.font={name:'Microsoft YaHei',size:11,color:'#243442'};
m.getRange('A2').values=[['会员规模和活动产能演示']];m.getRange('A2').format.font={size:16,bold:true};m.getRange('A3').values=[['蓝色为可修改假设；每位贡献已扣直接交付和归因获客成本，不是售价或竞品实绩。']];
m.getRange('A5:D12').values=[['输入参数','数值','单位','含义'],['年度固定成本',1800000,'元','演示参数'],['每位年度贡献',20000,'元每人','扣直接交付与归因获客成本'],['会员人数',60,'人','服务容量演示'],['每组人数',10,'人','固定小组'],['每组全年次数',10,'次','每组年度安排'],['每人开放活动名额',6,'席每年','额外开放活动权益'],['每场开放活动座位',20,'席','开放活动容量']];
m.getRange('A14:D20').values=[['计算结果',null,'单位','计算逻辑'],['盈亏平衡会员数',null,'人','固定成本除以单位贡献，向上取整'],['固定组数量',null,'组','会员数除以组人数，向上取整'],['固定组全年场次',null,'场','组数乘以每组全年次数'],['开放活动全年场次',null,'场','总名额除以单场容量，向上取整'],['全年合计活动场次',null,'场','固定组与开放活动相加'],['年度经营结余',null,'元','会员人数乘单位贡献，减固定成本']];
m.getRange('B15').formulas=[['=IF(AND(ISNUMBER(B6),ISNUMBER(B7),B6>=0,B7>0),ROUNDUP(B6/B7,0),"请补成本与正贡献")']];
m.getRange('B16').formulas=[['=IF(AND(ISNUMBER(B8),ISNUMBER(B9),B8>=0,B9>0),ROUNDUP(B8/B9,0),"请补人数与组容量")']];
m.getRange('B17').formulas=[['=IF(AND(ISNUMBER(B16),ISNUMBER(B10),B10>=0),B16*B10,"请补组活动次数")']];
m.getRange('B18').formulas=[['=IF(AND(ISNUMBER(B8),ISNUMBER(B11),ISNUMBER(B12),B8>=0,B11>=0,B12>0),ROUNDUP(B8*B11/B12,0),"请补开放活动参数")']];
m.getRange('B19').formulas=[['=IF(AND(ISNUMBER(B17),ISNUMBER(B18)),B17+B18,"请补交付参数")']];
m.getRange('B20').formulas=[['=IF(AND(ISNUMBER(B6),ISNUMBER(B7),ISNUMBER(B8),B6>=0,B7>0,B8>=0),B8*B7-B6,"请补经营参数")']];
for(const r of ['A5:D5','A14:D14'])m.getRange(r).format={fill:'#234458',font:{bold:true,color:'#FFFFFF'},rowHeight:32};
m.getRange('A6:D20').format.rowHeight=34;m.getRange('B6:B12').format.font={color:'#2357AF'};m.getRange('B15:B20').format.font={color:'#000000'};m.getRange('B6:B20').setNumberFormat('#,##0;(#,##0);"—"');
for(const [i,w] of [42,23,18,58,3,24,23].entries())m.getRangeByIndexes(0,i,25,1).format.columnWidth=w;
m.getRange('F5:G7').values=[['项目','金额 元'],['会员年度贡献',null],['固定成本',null]];m.getRange('G6').formulas=[['=IF(AND(ISNUMBER(B7),ISNUMBER(B8),B7>0,B8>=0),B7*B8,NA())']];m.getRange('G7').formulas=[['=IF(AND(ISNUMBER(B6),B6>=0),B6,NA())']];m.getRange('G6:G7').setNumberFormat('#,##0');
const chart=m.charts.add('bar',m.getRange('F5:G7'));chart.title='年度贡献与固定成本';chart.titleTextStyle.typeface='Microsoft YaHei';chart.titleTextStyle.fontSize=14;chart.hasLegend=false;chart.xAxis={axisType:'textAxis',textStyle:{typeface:'Microsoft YaHei',fontSize:11}};chart.yAxis={numberFormatCode:'#,##0',numberFormatSourceLinked:false,textStyle:{typeface:'Microsoft YaHei',fontSize:10}};chart.setPosition('F9','J21');
m.getRange('A23').values=[['来源：本项目容量演示假设。按全部权益使用估计，不含尚未设定的私人匹配和旅行工时。']];
wb.recalculate();
const check=await wb.inspect({kind:'region',sheetId:'经营测算',range:'A14:B20',maxChars:2500});await fs.writeFile(B+'qa/model-inspect.ndjson',check.ndjson);
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:50},maxChars:2000});await fs.writeFile(B+'qa/error-scan.ndjson',errors.ndjson);
// Meaningful input change and missing-input checks, then restore the delivered case.
const base=m.getRange('B15:B20').values;
m.getRange('B8').values=[[90]];wb.recalculate();const changed=m.getRange('B15:B20').values;
if(changed[4][0]!==117||changed[5][0]!==0)throw new Error('90-member case failed '+JSON.stringify(changed));
m.getRange('B7').values=[[null]];wb.recalculate();if(typeof m.getRange('B15').values[0][0]!=='string')throw new Error('Missing contribution not exposed');
m.getRange('B7').values=[[20000]];m.getRange('B8').values=[[60]];wb.recalculate();
if(m.getRange('B19').values[0][0]!==78||m.getRange('B20').values[0][0]!==-600000)throw new Error('Base case restore failed');
await fs.writeFile(B+'qa/model-input-check.json',JSON.stringify({base,changed,restored:m.getRange('B15:B20').values},null,2));
await (await SpreadsheetFile.exportXlsx(wb)).save(B+'交付文件/高端线下社群研究数据.xlsx');
await fs.writeFile(B+'工作簿链接映射.json',JSON.stringify(links,null,2));
for(const name of ['机构总览','收费权益','客户画像','活动旅行','账号声量','内容明细','经营测算']){const range=name==='经营测算'?'A1:J24':`A1:${name==='内容明细'?'J':name==='活动旅行'||name==='账号声量'?'H':'F'}9`;const img=await wb.render({sheetName:name,range,scale:1,format:'png'});await fs.writeFile(B+'qa/'+name+'.png',new Uint8Array(await img.arrayBuffer()));}
console.log('saved workbook',d.counts,'hyperlinks',links.length);
