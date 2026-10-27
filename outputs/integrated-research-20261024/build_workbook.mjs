import fs from 'node:fs/promises';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const B=decodeURIComponent(new URL('.',import.meta.url).pathname),D=JSON.parse(await fs.readFile(B+'统一研究数据.json','utf8')),S=Object.fromEntries(D.sources.map(s=>[s.id,s]));
const w=Workbook.create(),links=[];let idx=0;
function make(name,title,sub,headers,rows,widths){
 const s=w.worksheets.add(name),n=idx++,last=String.fromCharCode(64+headers.length),end=rows.length+5;
 s.showGridLines=false;s.getRange(`A1:${last}${end}`).format={font:{name:'Arial',size:11,color:'#263746'},verticalAlignment:'top'};
 s.getRange(`A2:${last}2`).merge();s.getRange('A2').values=[[title]];s.getRange('A2').format={font:{size:17,bold:true},rowHeight:36};
 s.getRange(`A3:${last}3`).merge();s.getRange('A3').values=[[sub]];s.getRange('A3').format={wrapText:true,rowHeight:34,font:{size:10,color:'#536674'}};
 s.getRange(`A5:${last}5`).values=[headers];s.getRange(`A5:${last}5`).format={fill:'#263746',font:{color:'#FFFFFF',bold:true},wrapText:true,rowHeight:36,horizontalAlignment:'center'};
 s.getRange(`A6:${last}${end}`).values=rows;s.getRange(`A6:${last}${end}`).format.wrapText=true;
 widths.forEach((v,i)=>s.getRangeByIndexes(0,i,end,1).format.columnWidth=v);
 rows.forEach((row,i)=>{let lines=Math.max(...row.map((v,j)=>String(v??'').split('\n').reduce((a,t)=>a+Math.max(1,Math.ceil([...t].reduce((n,c)=>n+(/[^\x00-\xff]/.test(c)?1:.52),0)/(widths[j]*.43))),0)));s.getRange(`A${i+6}:${last}${i+6}`).format.rowHeight=Math.max(44,Math.min(405,lines*15.5+16));if(i%2===0)s.getRange(`A${i+6}:${last}${i+6}`).format.fill='#F1F4F6';});
 s.tables.add(`A5:${last}${end}`,true,'StudyTable'+n);s.freezePanes.freezeRows(5);s.freezePanes.freezeColumns(name==='对标产品'?2:1);return s;
}
function sourceLink(s,sheet,cell,key){let u=S[key]?.url;if(u){s.getRange(cell).values=[['查看原文 '+key]];links.push({sheet,cell,url:u});s.getRange(cell).format.font={color:'#245A85'};}else{s.getRange(cell).values=[['微信小程序实查\n见来源与缺口']];}}
const macro=make('市场调研','第一部分 市场调研','先读市场基础和口径，再看对标。空白金额为未取得；机构份额不以粉丝或注册数代替。',['分类','指标','数值','单位','统计时间','定义及研究用途','原文'],D.macro,[20,39,17,15,37,65,24]);
macro.getRange(`C6:C${D.macro.length+5}`).setNumberFormat('#,##0');D.macro.forEach((r,i)=>{if(typeof r[2]==='number'&&!Number.isInteger(r[2]))macro.getRange('C'+(i+6)).setNumberFormat('0.00');sourceLink(macro,0,'G'+(i+6),r[6]);});
const products=make('对标产品','第二部分 对标产品与收费','一个可比较产品一行；同品牌不同会籍不是不同公司。全部主对标与成熟参照共用同一字段。金额需结合币种、单位与包含项。',['方向','机构及产品','明确金额','单位 包含与另付','客户画像与准入','活动及服务流程','获客与经营证据','用途与研究判断','原文'],D.products,[17,30,16,48,60,55,63,48,23]);
products.getRange(`C6:C${D.products.length+5}`).setNumberFormat('#,##0');D.products.forEach((r,i)=>{if(typeof r[2]==='number'&&!Number.isInteger(r[2]))products.getRange('C'+(i+6)).setNumberFormat('0.00');sourceLink(products,1,'I'+(i+6),r[8]);});
const map=make('机构名录','完整机构名录与本轮用途',D.market.length+'条机构与品牌线索覆盖原有研究和新增候选；主对标、成熟参照与未深挖候选在用途栏区分。正和岛和优家荟按要求退出。',['机构','主要组织方式','地区','目标客户或品牌定位','本轮用途','原文'],D.market,[34,30,30,63,57,20]);
D.market.forEach((r,i)=>{if(r[5]?.startsWith('http')){links.push({sheet:2,cell:'F'+(i+6),url:r[5]});map.getRange('F'+(i+6)).values=[['查看原文']];}else map.getRange('F'+(i+6)).values=[['微信小程序']];});
const sources=D.sources.map(s=>[s.id,s.name,s.kind,s.period,s.note,s.url?'查看原文':'微信小程序或私有资料，无网页链接']);
const sourceSheet=make('来源与缺口','来源台账与需要补证的事项','包含继承资料和本轮采集。正文引用来源优先；旧资料的原日期保留，读取失败不会改写成已核实。',['编号','资料','证据类别','适用或采集时间','使用说明','资料入口'],sources,[15,40,34,41,75,22]);
D.sources.forEach((s,i)=>{if(s.url)links.push({sheet:3,cell:'F'+(i+6),url:s.url});});
const gr=sources.length+9,gaps=[
 ['BoL商务会籍','付费会员、续费、实际履约及运动含项','待品牌正式服务确认','不能由10万自述或年活动承诺代填'],
 ['BoL Selected','到场、复购及退改适用条款','后续以服务记录核实','会员价按用户决定停止追查，保留未公开；1688是展示价；已售29不作实到'],
 ['钻石婚恋','服务期限、次数、合同退改、单次派对价','待合同或正式报价','30／60／100万起为项目费'],
 ['婚恋旅行','同一产品的收费、承办关系、实际成团','待品牌完整产品及交付证据','有旅行入口或户外海报不等于旅行经营已成立'],
 ['客户画像','付费客户的年龄收入、性格兴趣分布','待客户访谈与机构脱敏统计','当前分品牌定位、单场准入和公开样例'],
 ['市场份额','同口径行业总收入及前五同期收入','待原始统计或可核财务','保留空白，不以平台声量补份额'],
 ['自身验证','目标客户付费反馈与供应商同条件报价','Olivia及格格后续核实','当前暂无已确认资源和访谈结论']
];
sourceSheet.getRange(`A${gr}:D${gr}`).values=[['对象','缺少什么','怎样补齐','当前处理']];sourceSheet.getRange(`A${gr}:D${gr}`).format={fill:'#263746',font:{bold:true,color:'#FFFFFF'},rowHeight:32};sourceSheet.getRange(`A${gr+1}:D${gr+gaps.length}`).values=gaps;sourceSheet.getRange(`A${gr+1}:D${gr+gaps.length}`).format={wrapText:true,rowHeight:95};
const num=v=>{if(v===null||v===undefined||v==='')return null;const x=String(v).replace(/,/g,'');if(/^\d+(\.\d+)?万\+?$/.test(x))return parseFloat(x)*10000;if(/^\d+(\.\d+)?$/.test(x))return Number(x);return v;};
const content=D.contents.map(r=>[r[0],r[1],r[2],r[3],...r.slice(4,8).map(num),r[8],'查看原文']);
const cs=make('内容互动','平台采集与互动证据','搜索卡片与完整正文分别记录，可能重复同一内容；空白不代表0。旧热帖按发布日期识别，不算当前活跃。没有花费与成交数据，不计算转化率。',['记录类型','账号','发布日期','标题','点赞','收藏','评论','分享','采集时间','原文'],content,[28,30,22,55,13,13,13,13,34,20]);
cs.getRange(`E6:H${content.length+5}`).setNumberFormat('#,##0');D.contents.forEach((r,i)=>{if(r[9])links.push({sheet:4,cell:'J'+(i+6),url:r[9]});});
w.recalculate();const check=await w.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|not implemented',options:{useRegex:true,maxResults:30},maxChars:3000});
await fs.writeFile(B+'qa/工作簿检查.txt',check.ndjson||String(check));
for(const[sheetName,range,key]of[['市场调研','A5:G10','市场调研'],['对标产品','A5:D8','对标收费'],['对标产品','E5:I8','对标画像流程'],['机构名录','A5:F10','机构名录'],['来源与缺口','A5:F9','来源'],['内容互动','A5:J10','互动']]){const blob=await w.render({sheetName,range,scale:1,format:'png'});await fs.writeFile(B+'qa/'+key+'.png',new Uint8Array(await blob.arrayBuffer()));}
for(const[sheetName,range,key]of[['市场调研',`A${D.macro.length}:G${D.macro.length+5}`,'新增婚恋规模'],['对标产品',`A${D.products.length+4}:I${D.products.length+5}`,'新增收费与流程']]){const blob=await w.render({sheetName,range,scale:1,format:'png'});await fs.writeFile(B+'qa/'+key+'.png',new Uint8Array(await blob.arrayBuffer()));}
for(const brand of ['Founder Feast','32号','The Offline Club']){const ix=D.products.findIndex(r=>r[1].startsWith(brand));if(ix>=0){const row=ix+6,blob=await w.render({sheetName:'对标产品',range:`B${row}:I${row}`,scale:1,format:'png'});await fs.writeFile(B+'qa/补写-'+brand.replaceAll(' ','')+'.png',new Uint8Array(await blob.arrayBuffer()));}}
const summaryBlob=await w.render({sheetName:'市场调研',range:`A${D.macro.length}:G${D.macro.length+5}`,scale:1,format:'png'});await fs.writeFile(B+'qa/结论.png',new Uint8Array(await summaryBlob.arrayBuffer()));
await fs.writeFile(B+'链接索引.json',JSON.stringify(links));const result=await SpreadsheetFile.exportXlsx(w);await result.save(B+'交付文件/高端线下社群市场调研与对标总表.xlsx');
console.log(JSON.stringify({sheets:5,products:D.products.length,institutions:D.market.length,sources:sources.length,content:content.length,links:links.length}));
