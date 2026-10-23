import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { Workbook, SpreadsheetFile } from '@oai/artifact-tool';
const here=path.dirname(fileURLToPath(import.meta.url));
const data=JSON.parse(await fs.readFile(path.join(here,process.argv[2]||'交付工作簿数据.json'),'utf8'));
const out=path.join(here,'../交付资料/正式文件');
const qa=path.join(here,process.argv[3]||'qa-package-workbook');await fs.mkdir(qa,{recursive:true});
const wb=Workbook.create();
function col(n){let s='';while(n){n--;s=String.fromCharCode(65+n%26)+s;n=Math.floor(n/26)}return s}
function value(v){if(v===undefined)return null;if(typeof v==='string'&&v.startsWith('='))return "'"+v;return v}
function width(h,i){
 if(/网址|链接|入口|主页/.test(h))return 52;
 if(/具体|内容|说明|权益|片段|限制|人群|方式|判断|作用|主要|状态|依据/.test(h))return 58;
 if(/时间|日期/.test(h))return 26;
 if(/序号|年份|金额|粉丝|点赞|收藏|评论|分享|字数|状态码|HTTP/.test(h))return 15;
 return i===0?25:28;
}
for(let si=0;si<data.sheets.length;si++){
 const s=data.sheets[si],sh=wb.worksheets.add(s.name),nc=s.headers.length,nr=s.rows.length;
 sh.showGridLines=false;
 const full=sh.getRange(`A1:${col(nc)}${nr+4}`);full.format.font={name:'Arial',size:10,color:'#222222'};full.format.verticalAlignment='center';
 sh.getRange('A2').values=[[s.name]];sh.getRange('A2').format.font={name:'Arial',size:14,bold:true,color:'#111111'};
 sh.getRange('A3').values=[[s.note]];sh.getRange('A3').format.font={name:'Arial',size:10,color:'#666666'};
 sh.getRange('A3').format.rowHeight=20;
 const headers=sh.getRange(`A4:${col(nc)}4`);headers.values=[s.headers];headers.format={fill:'#28475D',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},horizontalAlignment:'center',verticalAlignment:'center',wrapText:true,rowHeight:30};
 let rows=s.rows.map(r=>Array.from({length:nc},(_,j)=>value(r[j])));
 const dates=new Set();
 rows=rows.map(r=>r.map((v,j)=>{
   if(/时间|日期/.test(s.headers[j])&&typeof v==='string'&&/^\d{4}-\d{2}-\d{2}(T|$)/.test(v)){
    const dt=new Date(v);if(!isNaN(dt)){dates.add(j);return dt}
   }return v;
 }));
 if(nr)sh.getRange(`A5:${col(nc)}${nr+4}`).values=rows;
 for(let j=0;j<nc;j++){
  const w=s.widths?.[j]??width(s.headers[j],j);sh.getRange(`${col(j+1)}1:${col(j+1)}${nr+4}`).format.columnWidth=w;
  const cells=sh.getRange(`${col(j+1)}5:${col(j+1)}${nr+4}`);cells.format.wrapText=true;
  if(rows.some(r=>typeof r[j]==='number'))cells.setNumberFormat(/年份|序号|顺序|HTTP/.test(s.headers[j])?'0':'#,##0');
  for(let ri=0;ri<rows.length;ri++){
   const v=rows[ri][j],cell=sh.getRange(`${col(j+1)}${ri+5}`);
   if(v instanceof Date)cell.setNumberFormat('yyyy-mm-dd hh:mm');
   else if(typeof v==='number'&&v>=1900&&v<=2100&&/时间|范围|年份/.test(s.headers[j]))cell.setNumberFormat('0');
   else if(typeof v==='number'&&!Number.isInteger(v)){
    const dp=Math.min(6,String(v).split('.')[1]?.length??1);cell.setNumberFormat('#,##0.'+'0'.repeat(dp));
   }
  }
 }
 if(s.name==='经营指标明细'){
  for(let i=0;i<rows.length;i++)if(rows[i][3]==='比例'||(/比例/.test(rows[i][1])&&typeof rows[i][2]==='number'&&rows[i][2]<=1))sh.getRange(`C${i+5}`).setNumberFormat('0.00%');
 }
 // Fitted heights, using both Chinese glyphs and Latin text in the estimate.
 for(let i=0;i<rows.length;i++){
  let lines=1;
  rows[i].forEach((v,j)=>{
   if(v===null||v instanceof Date)return;
   const w=s.widths?.[j]??width(s.headers[j],j);
   const text=String(v);const lengths=text.split('\n').map(t=>[...t].reduce((n,ch)=>n+(/[\u2e80-\uffff]/.test(ch)?1.8:1),0));
   const count=lengths.reduce((n,len)=>n+Math.max(1,Math.ceil(len/(w*.94))),0);lines=Math.max(lines,count);
  });
  sh.getRange(`A${i+5}:${col(nc)}${i+5}`).format.rowHeight=Math.min(390,Math.max(30,lines*14+8));
 }
 if(nr){const t=sh.tables.add(`A4:${col(nc)}${nr+4}`,true,`Research${si+1}`);t.showFilterButton=true;}
 sh.freezePanes.freezeRows(4);sh.freezePanes.freezeColumns(1);
 if(si<8)sh.tabColor='#28475D';
 if(s.name==='来源台账'){
  for(let i=0;i<nr;i++){
   const u=s.rows[i][2];if(typeof u==='string'&&u.startsWith('http')){sh.getRange(`C${i+5}`).values=[['打开原文']];sh.getRange(`C${i+5}`).format.font={name:'Arial',size:10,color:'#295878'};}
  }
 }
}
const sh=wb.worksheets.add('经营测算');sh.showGridLines=false;sh.tabColor='#66849A';
sh.getRange('A1:D22').format.font={name:'Arial',size:10,color:'#222222'};sh.getRange('A2').values=[['会员服务经营测算']];sh.getRange('A2').format.font={name:'Arial',size:14,bold:true};
sh.getRange('A3').values=[['蓝色数字可修改。参数来自正式报告的容量演示，不是报价或销售预测。']];
sh.getRange('A5:D12').values=[['输入参数','数值','单位','含义'],['年度固定成本',1800000,'元','条件测算'],['每位年度贡献',20000,'元／人','扣除直接交付及归因获客费用'],['会员人数',60,'人','权益容量演示'],['每组人数',10,'人','固定组'],['每组全年次数',10,'次','固定组见面'],['每人开放活动名额',6,'席／年','全年可使用名额'],['每场开放活动座位',20,'席','每场容量']];
sh.getRange('B6:B12').format.font={name:'Arial',size:10,color:'#0000FF'};sh.getRange('B6:B12').format.fill='#FFF4CC';
sh.getRange('A14:D19').values=[['计算结果','数值','单位','计算方法'],['盈亏平衡会员数',null,'人','固定成本除以每位贡献，向上取整'],['固定组数量',null,'组','会员人数除以每组人数，向上取整'],['固定组全年场次',null,'场','组数乘以每组全年次数'],['开放活动全年场次',null,'场','全年名额除以每场容量，向上取整'],['全年合计活动场次',null,'场','固定组加开放活动']];
sh.getRange('B15:B19').formulas=[['=IF(B7>0,ROUNDUP(B6/B7,0),"贡献须大于零")'],['=IF(B9>0,ROUNDUP(B8/B9,0),"组人数须大于零")'],['=B16*B10'],['=IF(B12>0,ROUNDUP(B8*B11/B12,0),"座位须大于零")'],['=SUM(B17:B18)']];
for(const rr of ['A5:D5','A14:D14'])sh.getRange(rr).format={fill:'#28475D',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},rowHeight:30};
sh.getRange('A1:A22').format.columnWidth=30;sh.getRange('B1:C22').format.columnWidth=18;sh.getRange('D1:D22').format.columnWidth=62;sh.getRange('A6:D19').format.rowHeight=30;sh.getRange('B6:B19').setNumberFormat('#,##0;(#,##0);"–"');
sh.getRange('A21').values=[['按所有权益均被使用估算场次，尚需另做日期排期和人员工时测算。']];
wb.recalculate();
if(sh.getRange('B15').values[0][0]!==90)throw new Error('Break-even mismatch');
sh.getRange('B7').values=[[10000]];wb.recalculate();
if(sh.getRange('B15').values[0][0]!==180)throw new Error('Input change did not recalculate');
sh.getRange('B7').values=[[20000]];wb.recalculate();
console.log((await wb.inspect({kind:'table',range:'经营测算!A14:D19',include:'values,formulas',tableMaxRows:6,tableMaxCols:4,maxChars:2200})).ndjson);
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:15},maxChars:1200})).ndjson);
await (await SpreadsheetFile.exportXlsx(wb)).save(path.join(out,process.argv[4]||'中国高端会员社群市场研究数据工作簿.xlsx'));
for(const s of [...data.sheets,{name:'经营测算',headers:['指标','数值','单位','说明']}]){
 const nc=Math.min(s.headers.length,5);const blob=await wb.render({sheetName:s.name,range:`A2:${col(nc)}${s.name==='经营测算'?19:Math.min(8,s.rows.length+4)}`,scale:1,format:'png'});
 await fs.writeFile(path.join(qa,s.name+'.png'),new Uint8Array(await blob.arrayBuffer()));
}
await fs.writeFile(path.join(qa,'counts.json'),JSON.stringify({sheets:data.sheets.length+1,records:data.sheets.reduce((a,s)=>a+s.rows.length,0),...data.counts},null,2));
if(process.argv[2]){
 for(const s of data.sheets.filter(x=>['30家机构对照','30家价格','会员权益','客户画像','获客方式','活动流程','经营表现','经营指标明细'].includes(x.name))){
  const end=s.rows.length+4,start=Math.max(5,end-3),nc=Math.min(s.headers.length,5);
  const blob=await wb.render({sheetName:s.name,range:`A${start}:${col(nc)}${end}`,scale:1,format:'png'});
  await fs.writeFile(path.join(qa,s.name+'-新增记录.png'),new Uint8Array(await blob.arrayBuffer()));
 }
}
console.log('Exported workbook and rendered all worksheets.');
