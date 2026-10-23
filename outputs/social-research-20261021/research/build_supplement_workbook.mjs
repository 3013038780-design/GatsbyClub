import fs from 'node:fs/promises';
import path from 'node:path';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const root=path.resolve(import.meta.dirname,'../community-supplement');
const d=JSON.parse(await fs.readFile(path.join(root,'curated-data.json'),'utf8'));
const wb=Workbook.create();
const col=n=>{let r='';for(;n;n=Math.floor((n-1)/26))r=String.fromCharCode(65+(n-1)%26)+r;return r;};
const navy='#223C50',gray='#576574',pale='#F2F5F7';
const specs=[{name:'本轮发现',headers:['议题','研究发现与对公司的建议'],rows:d.findings,widths:[44,128]},...d.tables];
for(let index=0;index<specs.length;index++){
 const t=specs[index],s=wb.worksheets.add(t.name),end=col(t.headers.length),last=t.rows.length+4;
 s.showGridLines=false;s.tabColor=index<7?navy:'#8D9AA5';
 s.getRange(`A1:${end}${last}`).format={font:{name:'PingFang SC',size:11,color:'#243443'},wrapText:true,verticalAlignment:'top'};
 s.mergeCells(`A1:${end}1`);s.getRange('A1').values=[[t.name]];
 s.getRange(`A1:${end}1`).format={font:{name:'PingFang SC',size:18,bold:true,color:navy},rowHeight:36};
 s.mergeCells(`A2:${end}2`);s.getRange('A2').values=[[`中国高端社群补充调研　　数据更新（北京时间）：${d.generated_at.slice(0,16).replace('T',' ')}　　源ID对应“来源台账”`]];
 s.getRange(`A2:${end}2`).format={font:{size:10,color:gray},rowHeight:29};
 const rows=t.rows.map(r=>r.map((v,j)=>{
  // Excel stores a wall-clock serial without timezone. Preserve the source's Beijing time.
  if(/时间/.test(t.headers[j])&&typeof v==='string'&&/^202\d-\d\d-\d\dT/.test(v))return new Date(v.slice(0,19)+'Z');
  if(typeof v==='string'&&/^[=+@]/.test(v))return `'${v}`;
  return v??null;
 }));
 s.getRange(`A4:${end}${last}`).values=[t.headers,...rows];
 s.tables.add(`A4:${end}${last}`,true,`CommunityResearch${index+1}`);
 s.getRange(`A4:${end}4`).format={fill:navy,font:{bold:true,color:'#FFFFFF'},rowHeight:35};
 for(let j=0;j<t.headers.length;j++){
  s.getRange(`${col(j+1)}:${col(j+1)}`).format.columnWidth=t.widths[j]??30;
  if(['数值','金额','粉丝数','获赞与收藏累计','点赞','收藏','评论','分享'].includes(t.headers[j]))s.getRange(`${col(j+1)}5:${col(j+1)}${last}`).setNumberFormat('#,##0');
  if(/时间/.test(t.headers[j]))s.getRange(`${col(j+1)}5:${col(j+1)}${last}`).setNumberFormat('yyyy-mm-dd hh:mm');
 }
 for(let i=0;i<t.rows.length;i++){
  let lines=1;
  t.rows[i].forEach((v,j)=>{const cellLines=String(v??'').split('\n').reduce((total,line)=>{const units=[...line].reduce((a,c)=>a+(c.charCodeAt(0)>255?2:1),0);return total+Math.max(1,Math.ceil(units/Math.max(8,(t.widths[j]??30)-3)));},0);lines=Math.max(lines,cellLines);});
  s.getRange(`A${i+5}:${end}${i+5}`).format={rowHeight:Math.max(49,Math.min(245,lines*15+15)),fill:i%2?pale:'#FFFFFF',borders:{bottom:{style:'thin',color:'#E0E6EA'}}};
 }
 if(t.name==='规模与活跃度')for(let i=0;i<t.rows.length;i++){
  const row=t.rows[i];
  s.getRange(`C${i+5}`).setNumberFormat(row[3]==='比例'||(row[3]==='以上'&&typeof row[2]==='number'&&row[2]<=1)?'0.0%':'#,##0');
 }
 s.freezePanes.freezeRows(4);s.freezePanes.freezeColumns(1);
}
wb.recalculate();
const qa=path.join(root,'qa');await fs.mkdir(qa,{recursive:true});
const inspect=await wb.inspect({kind:'region',sheetId:'价格与收费',range:'A4:K10',maxChars:2500,tableMaxRows:7,tableMaxCols:11});
await fs.writeFile(path.join(qa,'价格核查.json'),JSON.stringify(inspect,null,2));
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#SPILL!',options:{useRegex:true,maxResults:50},maxChars:1200});
await fs.writeFile(path.join(qa,'公式检查.json'),JSON.stringify(errors,null,2));
for(const t of specs){
 const img=await wb.render({sheetName:t.name,range:`A1:${col(t.headers.length)}${Math.min(t.rows.length+4,7)}`,scale:1.1,format:'png'});
 await fs.writeFile(path.join(qa,`${t.name}.png`),new Uint8Array(await img.arrayBuffer()));
}
for(const name of ['本轮发现','机构与研究重点','价格与收费','产品与会员权益','客户画像','获客与转化','活动流程','规模与活跃度','来源台账']){
 const t=specs.find(t=>t.name===name);
 const img=await wb.render({sheetName:name,range:`A${Math.max(4,t.rows.length+2)}:${col(t.headers.length)}${t.rows.length+4}`,scale:1.1,format:'png'});
 await fs.writeFile(path.join(qa,`${name}-新增.png`),new Uint8Array(await img.arrayBuffer()));
}
const golf=await wb.render({sheetName:'价格与收费',range:'A22:K28',scale:1.1,format:'png'});
await fs.writeFile(path.join(qa,'观澜湖赛事价格.png'),new Uint8Array(await golf.arrayBuffer()));
const out=await SpreadsheetFile.exportXlsx(wb);await out.save(path.join(root,'高端社群补充调研工作簿.xlsx'));
console.log(JSON.stringify({exported:true,sheets:specs.map(t=>({name:t.name,rows:t.rows.length}))}));
