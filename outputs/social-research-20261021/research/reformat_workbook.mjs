import fs from 'node:fs/promises';
import path from 'node:path';
import {FileBlob,SpreadsheetFile} from '@oai/artifact-tool';
const root=path.resolve(import.meta.dirname,'..'),qa=path.join(root,'qa/format-revision');
const file='中国高端社交市场研究数据工作簿.xlsx';
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(path.join(import.meta.dirname,'original-format',file)));
const layout=JSON.parse(await fs.readFile(path.join(import.meta.dirname,'workbook-layout.json'),'utf8'));
const col=n=>{let s='';for(;n;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s;};
const before=[];
for(const info of layout){
 const s=wb.worksheets.getItem(info.name),last=col(info.columns),used=s.getRange(`A1:${last}${info.rows}`);
 before.push({name:info.name,values:used.values,formulas:used.formulas});
 used.format.font={name:'PingFang SC',size:10.5};used.format.wrapText=true;used.format.verticalAlignment='center';s.showGridLines=false;
 if(s.tables.items.length){
  for(const t of s.tables.items)t.style='TableStyleLight1';
  const vals=used.values,widths=[];
  for(let j=1;j<=info.columns;j++){
   const spec=info.cols.find(x=>+x.min<=j&&+x.max>=j);const old=spec?+spec.width:24;
   const w=Math.max(11,Math.min(old,50));widths.push(w);s.getRange(`${col(j)}:${col(j)}`).format.columnWidth=w;
  }
  s.getRange(`A1:${last}1`).format={font:{name:'PingFang SC',size:16,bold:true,color:'#000000'},rowHeight:30};
  s.getRange(`A2:${last}2`).format={font:{size:10,color:'#505050'},rowHeight:32};
  s.getRange(`A3:${last}3`).format.rowHeight=8;
  s.getRange(`A4:${last}${info.rows}`).format.borders={preset:'all',style:'thin',color:'#D9D9D9'};
  s.getRange(`A4:${last}4`).format={fill:'#E9ECEF',font:{bold:true,color:'#000000'},rowHeight:30,horizontalAlignment:'center'};
  s.getRange(`A5:${last}${info.rows}`).format.fill='#FFFFFF';
  for(let r=5;r<=info.rows;r++){
   const row=vals[r-1]??[];let lines=1;
   row.forEach((v,j)=>{const text=String(v??'');const weight=[...text].reduce((a,c)=>a+(c.charCodeAt(0)>255?2:1),0);lines=Math.max(lines,Math.ceil(weight/Math.max(8,widths[j]-3)));});
   s.getRange(`A${r}:${last}${r}`).format.rowHeight=Math.max(28,lines*14+8);
  }
 }else{
  // Finance colors continue to distinguish inputs, linked data and formulas.
  used.format.rowHeight=31;
  s.getRange('C2:H2').format={font:{name:'PingFang SC',size:16,bold:true,color:'#000000'},rowHeight:31};
  for(const rr of (info.name==='经营模型'?['C7:H7']:['C6:H6','C23:H23','C35:F35']))s.getRange(rr).format={fill:'#E9ECEF',font:{bold:true,color:'#000000'},rowHeight:30};
  if(info.name==='经营模型'){
   for(const row of [3,5,6])s.getRange(`C${row}:H${row}`).format.rowHeight=8;
   s.getRange('C4:H4').format.rowHeight=34;s.getRange('H:H').format.columnWidth=50;
   s.getRange('E8:G22').format.fill='#F3F6FA';
   for(const r of [29,32,36,38,43,45])s.getRange(`C${r}:H${r}`).format.fill='#F2F2F2';
   s.getRange('C48:H49').format.rowHeight=27;
  }else{
   s.getRange('C3:H3').format.rowHeight=42;
   s.getRange('C20:H21').format.rowHeight=25;s.getRange('C31:H32').format.rowHeight=25;
   s.getRange('G24:G28').format.fill='#F3F6FA';s.getRange('C17:H17').format.fill='#F2F2F2';
   s.getRange('D35:F35').format.font={color:'#0000FF',bold:true};
  }
 }
}
wb.recalculate();
for(const [i,info] of layout.entries()){
 const s=wb.worksheets.getItem(info.name),used=s.getRange(`A1:${col(info.columns)}${info.rows}`);
 if(JSON.stringify(used.values)!==JSON.stringify(before[i].values)||JSON.stringify(used.formulas)!==JSON.stringify(before[i].formulas))throw Error('内容改变 '+info.name);
}
const inspection=await wb.inspect({kind:'table',range:'经营模型!C26:D45',include:'values,formulas',tableMaxRows:20,maxChars:2500});
await fs.writeFile(path.join(qa,'workbook-check.json'),JSON.stringify({contentPreserved:true,inspection},null,2));
await(await SpreadsheetFile.exportXlsx(wb)).save(path.join(root,file));
console.log('17 sheets restyled; values and formulas preserved');
for(const info of layout){
 const range=info.name==='经营模型'?'C2:H15':info.name==='收费模式比较'?'C2:H17':`A1:${col(Math.min(info.columns,6))}${Math.min(info.rows,8)}`;
 const p=await wb.render({sheetName:info.name,range,scale:1.2,format:'png'});await fs.writeFile(path.join(qa,`sheet-${info.name}.png`),new Uint8Array(await p.arrayBuffer()));
}
console.log('All previews saved');
