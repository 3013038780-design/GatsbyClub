import fs from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import {FileBlob,SpreadsheetFile} from '@oai/artifact-tool';
const b=path.dirname(fileURLToPath(import.meta.url));
const plan=JSON.parse(await fs.readFile(b+'/删除两家工作簿计划.json','utf8'));
const w=await SpreadsheetFile.importXlsx(await FileBlob.load(b+'/交付文件/中国高端会员社群市场研究数据工作簿_33家机构.xlsx'));
function col(n){let s='';while(n){n--;s=String.fromCharCode(65+n%26)+s;n=Math.floor(n/26)}return s;}
for(const [name,x] of Object.entries(plan.changes)){
 const s=w.worksheets.getItem(name),c=col(x.cols);
 for(let i=0;i<x.keep.length;i++)if(x.keep[i]!==i+5)s.getRange(`A${x.keep[i]}:${c}${x.keep[i]}`).copyTo(s.getRange(`A${i+5}:${c}${i+5}`),'all');
 s.getRange(`A5:${c}${x.rows.length+4}`).values=x.rows;
 if(x.rows.length+4<x.oldRows)s.getRange(`A${x.rows.length+5}:${c}${x.oldRows}`).clear({applyTo:'all'});
 for(const [a,v] of x.top)s.getRange(a).values=[[v]];
 for(const t of [...s.tables.items])t.delete();
 s.tables.add(`A4:${c}${x.rows.length+4}`,true,'Revised_'+Object.keys(plan.changes).indexOf(name)).showFilterButton=true;
}
w.recalculate();
console.log((await w.inspect({kind:'table',range:'33家机构对照!A5:D10',include:'values,formulas',tableMaxRows:6,tableMaxCols:4,maxChars:1500})).ndjson);
console.log((await w.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:10},maxChars:500})).ndjson);
await(await SpreadsheetFile.exportXlsx(w)).save(b+'/交付文件/中国高端会员社群市场研究数据工作簿_31家机构.xlsx');
const im=await w.render({sheetName:'33家机构对照',range:'A4:D10',scale:1,format:'png'});await fs.writeFile(b+'/qa/删除两家后机构对照.png',new Uint8Array(await im.arrayBuffer()));
