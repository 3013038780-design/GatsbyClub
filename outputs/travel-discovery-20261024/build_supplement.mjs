import fs from 'node:fs/promises';
import path from 'node:path';
import {Workbook, SpreadsheetFile} from '@oai/artifact-tool';

const out=decodeURIComponent(new URL('.',import.meta.url).pathname);
const source=path.resolve(out,'../../.research-private/travel-discovery-20261024');
const read=async n=>JSON.parse(await fs.readFile(path.join(source,n),'utf8'));
const heart=await read('心动计划产品核验.json');
const cards=(await fs.readFile(path.join(source,'social-platforms/discovery-search-cards.jsonl'),'utf8')).trim().split('\n').map(JSON.parse);
const notes=(await fs.readFile(path.join(source,'social-platforms/target-note-details.jsonl'),'utf8')).trim().split('\n').map(JSON.parse).filter(x=>x.data);
const rows=[
 ['心动计划\n草原恋综旅行',null,'人民币／人起','正文6,280；封面7,280。同一帖价格不一致。帖发布于2026-04-10，具体团期售价需确认。','年轻单身交友人群。另一帖要求3张生活照及自我介绍视频，介绍年龄、职业、性格和兴趣。未公开资产、收入门槛。','5天4晚、8人；同性两人一间；4早2正餐；商务车或中巴；主持人兼旅行管家。接送站与指定门票见配图。','接站破冰；沙漠体验；城市任务及共同做饭；草原晚宴夜话；告别送站。属于公开招募方案。','小红书315粉丝、571获赞与收藏。适合学筛选与互动设计。公司全名、实际成团和成交情况尚待核实。',heart['证据'][0]['来源']],
 ['奇语旅行\n济州岛拼车小团',null,'人民币／地面费','原文“1k+”。2月28日产品帖；尚无指定出发日期完整报价。','该产品不限年龄性别，接受一个人或朋友同行。偏好拍照、咖啡、小店、自由行氛围。职业、收入分布未披露。','4天3晚；市区四钻酒店、地面用车、门票及上岛费；机票自理。其他餐饮与房型按产品确认。','第1天接机自由活动；第2天牛岛等；第3天牧场、茶园及海岸；第4天自由活动送机。部分景点拼一日团。','抖音企业认证为深圳市奇语旅行文化有限公司，8,143粉丝、4.0万获赞、89作品。可学小团与内容表达。此产品未设置婚恋或验资筛选。','https://www.douyin.com/note/7611854005258612965'],
 ['星七Club\n金海湖单身一日团',198,'人民币／人','官网公开标价。4人成团，上限20人。','仅限单身。职业、收入、资产门槛未公开。','北京往返交通、领队、互动组织、名额及一日意外险。餐饮AA或自备，其他个人消费另付。','集合；湖边趣味破冰；户外活动。报名缴费锁位。主办取消全退，正常举办时个人退出不退为网页规则。','适合学短途活动的打包和收费说明。与A8定位有距离，放在活动及价格参照中。','https://www.xingqiclub.com/pd.jsp?fromColId=2&id=1360'],
 ['墨鱼旅行\n黄金VIP连续包月',23,'人民币／月','中国区App Store开发者披露，自动续订。','App按目的地、年龄、兴趣、职业等匹配旅行搭子。未披露付费会员的精确收入及资产分布。','App订阅费。黄金与蓝钻逐项权益仍需核对App内页面。旅行团费另收。','订阅、找搭子、选择行程。具体旅行的组织和付款规则须回到对应产品。','新抓招募帖披露：用免费旅行名额换创作者笔记，要求粉丝1,000以上，优先上海及周边。可学内容合作获客。','https://apps.apple.com/cn/app/id6467105543'],
 ['墨鱼旅行\n蓝钻VIP连续包月',38,'人民币／月','中国区App Store开发者披露，自动续订。','同上，未据订阅名称推定其为高资产客群。','App订阅费。与黄金档的逐项权益待查，不能视为免费旅行权益。','按App订阅及旅行产品分别购买。','与黄金档作为同一品牌的两个收费产品记录，不重复计算机构数量。','https://apps.apple.com/cn/app/id6467105543'],
 ['Other Way Round\n墨西哥城4日',1400,'英镑／人','2026-12-29至2027-01-01团期在列。定金200英镑；独住加225英镑；出发70天前付尾款。','主要30—49岁独自报名者，官网称90%以上独行。欢迎内向和外向者，要求愿意结识新人、参与文化及运动体验。未设资产门槛。','4天3晚、四星双床房、早餐及2午2晚、接送机、行程活动、主持人与当地专家。国际机票另付。','预订；行前70天信息问卷；10天前发日程；3天前建群；欢迎晚宴、城市美食、运河及文化体验。','官网自述每年500—1,000客人，人数通常4—15、平均10。适合学小团队与地接分工；品牌明确不定位奢华旅行。','https://www.otherwayround.travel/mexico-city-4-days/'],
 ['The Supper Club\nQuattro会籍',2500,'美元／年','另加入会费750美元；仅首次申请者。','愿为策划晚宴和交流付费的城市会员。该会籍页未披露精确收入或资产分布。','同一州每年4场活动。不含带客权益，不开放And Beyond周末旅行及国际旅行资格。','申请入会；选择所在州活动；预约参加。旅行须看可参加的会籍等级。','可学用次数及地区界定权益。此档明确不含旅行入口，不能拿来推算旅行收入。','https://members.thesupperclubinc.com/membership'],
 ['The Supper Club\nExplorer会籍',5000,'美元／年','另加入会费750美元。','跨城市参加会员活动的人群；精确职业收入分布未公开。','每年最多8场、可跨美国城市分会。具体旅行收费及包含项另看行程。','申请；预约各城市活动；按名额参加。','与Quattro比较的是活动次数和地域权益，属于会员收费结构参考。','https://members.thesupperclubinc.com/membership']
];
const wb=Workbook.create();
function make(name,title,headers,data,widths){
 const s=wb.worksheets.add(name),end=data.length+5,last=String.fromCharCode(64+headers.length);
 s.showGridLines=false;
 s.getRange(`A1:${last}${end}`).format={font:{name:'Arial',size:11,color:'#263746'},verticalAlignment:'center'};
 s.getRange('A2').values=[[title]];s.getRange('A2').format.font={name:'Arial',size:16,bold:true};s.getRange('A2').format.rowHeight=32;
 s.getRange(`A5:${last}5`).values=[headers];s.getRange(`A5:${last}5`).format={fill:'#263746',font:{name:'Arial',size:11,color:'#FFFFFF',bold:true},horizontalAlignment:'center',wrapText:true,rowHeight:36};
 s.getRange(`A6:${last}${end}`).values=data;s.getRange(`A6:${last}${end}`).format.wrapText=true;s.getRange(`A6:${last}${end}`).format.verticalAlignment='top';
 widths.forEach((v,i)=>s.getRangeByIndexes(0,i,end,1).format.columnWidth=v);
 data.forEach((row,i)=>{const lines=Math.max(...row.map((v,j)=>String(j===row.length-1?'查看原文':v instanceof Date?'2026-10-24 12:30':v??'').split('\n').reduce((n,t)=>n+Math.max(1,Math.ceil([...t].reduce((a,c)=>a+(/[^\x00-\xff]/.test(c)?1:.52),0)/(widths[j]*.45))),0)));s.getRange(`A${i+6}:${last}${i+6}`).format.rowHeight=Math.max(42,lines*15+14);if(i%2===0)s.getRange(`A${i+6}:${last}${i+6}`).format.fill='#F1F4F6';});
 s.tables.add(`A5:${last}${end}`,true,name==='产品与收费'?'ProductChecks':'ContentEvidence');s.freezePanes.freezeRows(5);s.freezePanes.freezeColumns(1);return s;
}
const main=make('产品与收费','社交旅行产品与收费核验',['机构及产品','公开标价','币种及单位','报价适用范围','客户与准入','包含及另付','组织流程','经营表现与判断','原文'],rows,[25,14,21,38,43,45,47,48,16]);
main.getRange('A3').values=[['采集日期：2026-10-24。金额按各自单位列示，具体团期与图文差异见报价说明。']];
main.getRange('B6:B13').setNumberFormat('#,##0');main.getRange('B6:B13').format.horizontalAlignment='right';
const n=(v)=>v===undefined||v===null||v===''?null:Number(v);
const localSerial=v=>new Date(v).getTime()/86400000+25569+8/24;
const content=cards.map(r=>['搜索卡片',r.keyword,r.account_name,r.title,n(r.metrics.liked_count),n(r.metrics.collected_count),n(r.metrics.comment_count),n(r.metrics.shared_count),null,localSerial(r.captured_at),r.note_url]);
for(const r of notes){const d=r.data,m=d.interact_info||{};content.push(['完整正文',r.keyword,r.account_name,d.title||'',n(m.liked_count),n(m.collected_count),n(m.comment_count),n(m.share_count),d.time?localSerial(d.time):null,localSerial(r.captured_at),r.note_url]);}
const raw=make('内容与互动','旅行专题平台采集记录',['记录类型','搜索词','账号','标题','点赞','收藏','评论','分享','发布北京时间','采集北京时间','原文'],content,[17,21,27,50,12,12,12,12,23,23,16]);
raw.getRange('A3').values=[['搜索卡片395条，去重内容340篇。完整正文另列6条，同一篇重复核验不重复计算篇数。']];
raw.getRange(`E6:H${content.length+5}`).setNumberFormat('#,##0');raw.getRange(`I6:J${content.length+5}`).setNumberFormat('yyyy-mm-dd hh:mm');
const links=[];
rows.forEach((r,i)=>{links.push({sheet:0,cell:'I'+(i+6),url:r[8]});main.getRange('I'+(i+6)).values=[['查看原文']];main.getRange('I'+(i+6)).format.font={color:'#245A85'};});
content.forEach((r,i)=>{links.push({sheet:1,cell:'K'+(i+6),url:r[10]});raw.getRange('K'+(i+6)).values=[['查看原文']];raw.getRange('K'+(i+6)).format.font={color:'#245A85'};});
wb.recalculate();
const inspection=await wb.inspect({kind:'table',range:'产品与收费!A5:D13',include:'values,formulas',tableMaxRows:9,tableMaxCols:4,maxChars:2500});
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|not implemented',options:{useRegex:true,maxResults:20},maxChars:1000});
await fs.writeFile(out+'qa/核验.json',JSON.stringify({searchRows:cards.length,uniqueSearchNotes:new Set(cards.map(x=>x.note_url)).size,fullNotes:notes.length,products:rows.length,main:inspection.ndjson,errors:errors.ndjson},null,2));
for(const [sheetName,range,key] of [['内容与互动','G5:K10','时间与链接']]){const blob=await wb.render({sheetName,range,scale:1,format:'png'});await fs.writeFile(out+'qa/'+key+'.png',new Uint8Array(await blob.arrayBuffer()));}
await fs.writeFile(out+'链接索引.json',JSON.stringify(links));
const result=await SpreadsheetFile.exportXlsx(wb);await result.save(out+'社交旅行产品与采集核验.xlsx');
console.log(JSON.stringify({products:rows.length,searchCards:cards.length,fullNotes:notes.length,output:out+'社交旅行产品与采集核验.xlsx'}));
