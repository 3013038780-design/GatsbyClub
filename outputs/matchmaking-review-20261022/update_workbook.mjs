import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {FileBlob,SpreadsheetFile} from '@oai/artifact-tool';
const root=path.dirname(fileURLToPath(import.meta.url))+'/';
const input=path.resolve(root,'../social-research-20261021/交付资料/正式文件/中国高端会员社群市场研究数据工作簿_30家机构.xlsx');
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(input));
console.log((await wb.inspect({kind:'sheet',include:'id,name',maxChars:2300})).ndjson);
const im=await wb.render({sheetName:'30家机构对照',range:'A2:E8',scale:1,format:'png'});await fs.writeFile(root+'qa/原工作簿格式.png',new Uint8Array(await im.arrayBuffer()));
console.log(wb.help('worksheet.name',{include:'index,notes,examples',maxChars:1800}).ndjson);
await fs.writeFile(root+'qa/工作簿读取完成.txt','已读取原工作簿并渲染原格式');
const payload=JSON.parse(await fs.readFile(root+'工作簿更新数据.json','utf8'));
const baseData=JSON.parse(await fs.readFile(path.resolve(root,'../social-research-20261021/research/30家工作簿数据.json'),'utf8'));
const schema=Object.fromEntries(baseData.sheets.map(s=>[s.name,s]));
function col(n){let s='';while(n){n--;s=String.fromCharCode(65+n%26)+s;n=Math.floor(n/26)}return s;}
function fit(sh,rows,start,nc,widths){
 for(let i=0;i<rows.length;i++){
  let max=1;
  for(let j=0;j<nc;j++){
   const v=rows[i][j];if(v==null||typeof v==='number')continue;
   const w=widths?.[j]||(/来源|网址/.test(schema[sh.name]?.headers?.[j]||'')?58:55);
   const lines=String(v).split('\n').reduce((a,t)=>a+Math.max(1,Math.ceil([...t].reduce((n,c)=>n+(/[\u2e80-\uffff]/.test(c)?1.8:1),0)/(w*.94))),0);max=Math.max(max,lines);
  }
  sh.getRange(`A${start+i}:${col(nc)}${start+i}`).format.rowHeight=Math.min(390,Math.max(30,max*14+8));
 }
}
const changed=[];
for(const [name,config] of Object.entries(payload.updates)){
 const sh=wb.worksheets.getItem(name),s=schema[name],old=s.rows.length,nc=s.headers.length,n=config.rows.length;
 for(let i=old+5;i<=n+4;i++)sh.getRange(`A${old+4}:${col(nc)}${old+4}`).copyTo(sh.getRange(`A${i}:${col(nc)}${i}`),'all');
 sh.getRange(`A5:${col(nc)}${n+4}`).values=config.rows;
 sh.getRange('A2').values=[[config.title]];sh.getRange('A3').values=[[config.note]];
 sh.getRange(`A5:${col(nc)}${n+4}`).format.wrapText=true;sh.getRange(`A5:${col(nc)}${n+4}`).format.verticalAlignment='center';
 fit(sh,config.rows,5,nc,s.widths);
 for(const t of [...sh.tables.items])t.delete();
 sh.tables.add(`A4:${col(nc)}${n+4}`,true,'Updated_'+changed.length).showFilterButton=true;
 changed.push(name);
}
for(const [name,rows] of Object.entries(payload.appends)){
 if(!rows.length)continue;
 const sh=wb.worksheets.getItem(name),s=schema[name],nc=s.headers.length,start=s.rows.length+5,end=start+rows.length-1;
 for(let i=start;i<=end;i++)sh.getRange(`A${start-1}:${col(nc)}${start-1}`).copyTo(sh.getRange(`A${i}:${col(nc)}${i}`),'all');
 sh.getRange(`A${start}:${col(nc)}${end}`).values=rows;
 sh.getRange(`A${start}:${col(nc)}${end}`).format.wrapText=true;
 fit(sh,rows,start,nc,s.widths);
 // Match typed numeric fields and percentages in added evidence.
 if(name==='30家价格')sh.getRange(`C${start}:C${end}`).setNumberFormat('#,##0');
 if(name==='经营指标明细')for(let i=0;i<rows.length;i++)sh.getRange(`C${start+i}`).setNumberFormat(rows[i][3]==='比例'?'0.0%':'#,##0');
 sh.getRange('A3').values=[['2026-10-22新增婚恋专题。原记录保留原采集期；缺失数值留空，证据类别逐项注明。']];
 if(name.startsWith('30家'))sh.getRange('A2').values=[[name.replace('30家','33家')]];
 for(const t of [...sh.tables.items])t.delete();
 sh.tables.add(`A4:${col(nc)}${end}`,true,'Updated_'+changed.length).showFilterButton=true;
 changed.push(name);
}
const n=payload.new_sheet,sh=wb.worksheets.add(n.name),nc=n.headers.length,nr=n.rows.length;
sh.showGridLines=false;sh.tabColor='#28475D';sh.getRange(`A1:${col(nc)}${nr+4}`).format.font={name:'Arial',size:10,color:'#222222'};
sh.getRange('A2').values=[[n.name]];sh.getRange('A2').format.font={name:'Arial',size:14,bold:true,color:'#111111'};
sh.getRange('A3').values=[[n.note]];sh.getRange('A3').format.font={name:'Arial',size:10,color:'#666666'};
sh.getRange(`A4:${col(nc)}4`).values=[n.headers];sh.getRange(`A4:${col(nc)}4`).format={fill:'#28475D',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},rowHeight:30,wrapText:true,horizontalAlignment:'center',verticalAlignment:'center'};
sh.getRange(`A5:${col(nc)}${nr+4}`).values=n.rows;sh.getRange(`A5:${col(nc)}${nr+4}`).format.wrapText=true;
for(let j=0;j<nc;j++)sh.getRange(`${col(j+1)}1:${col(j+1)}${nr+4}`).format.columnWidth=n.widths[j];
sh.getRange(`A5:${col(nc)}${nr+4}`).format.verticalAlignment='center';fit(sh,n.rows,5,nc,n.widths);sh.tables.add(`A4:${col(nc)}${nr+4}`,true,'TravelMatchmaking').showFilterButton=true;sh.freezePanes.freezeRows(4);sh.freezePanes.freezeColumns(1);
wb.recalculate();
console.log((await wb.inspect({kind:'table',range:'30家价格!A95:G99',include:'values,formulas',tableMaxRows:5,tableMaxCols:7,maxChars:1800})).ndjson);
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:10},maxChars:600})).ndjson);
await fs.mkdir(root+'交付文件',{recursive:true});await(await SpreadsheetFile.exportXlsx(wb)).save(root+'交付文件/中国高端会员社群市场研究数据工作簿_33家机构.xlsx');
for(const name of ['30家机构对照','30家价格','会员权益','客户画像','获客方式','活动流程','经营表现','经营指标明细','来源台账','30家平台声量','活动环节明细','证据缺口','网页采集台账','市场机构地图',n.name]){
 const sh=wb.worksheets.getItem(name);const nc=Math.min(schema[name]?.headers.length||n.headers.length,5);
 let start=5,end=8;
 if(payload.appends[name]){start=schema[name].rows.length+5;end=Math.min(start+2,start+payload.appends[name].length-1);}
 else if(name==='30家机构对照'){start=35;end=37;}
 else if(name===n.name){start=4;end=9;}
 const preview=await wb.render({sheetName:name,range:`A${start}:${col(nc)}${end}`,scale:1,format:'png'});
 await fs.writeFile(root+'qa/'+name+'-更新.png',new Uint8Array(await preview.arrayBuffer()));
}
await fs.writeFile(root+'qa/workbook-change-list.json',JSON.stringify({changed,added:n.name}));
console.log('Workbook updated; original worksheets preserved.');
