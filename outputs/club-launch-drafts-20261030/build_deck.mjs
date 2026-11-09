import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
const B=decodeURIComponent(new URL('.',import.meta.url).pathname),S='/Users/olivialee/.codex/plugins/cache/openai-primary-runtime/presentations/26.1017.22136/skills/presentations';
const pres=Presentation.create({slideSize:{width:1280,height:720}}),font='Source Han Serif CN',ink='#243E35',muted='#5F6E65',accent='#A75A3B',paper='#F5F1E8';
function text(slide,s,x,y,width,height,size=28,color=ink,bold=false){const a=slide.shapes.add({geometry:'textbox',position:{left:x,top:y,width,height},fill:'none',line:{fill:'none',width:0}});a.text=s;a.text.style={typeface:font,fontSize:size,color,bold,wrap:'square',autoFit:'none',insets:0,verticalAlignment:'top'};return a;}
function slide(title,sub='',appendix=false){const s=pres.slides.add();s.background.fill=paper;text(s,title,70,62,1140,76,44,ink,true);if(sub)text(s,sub,72,151,1120,60,23,muted);text(s,(appendix?'合作讨论附页':'会员方案建议')+'  2026年10月30日',72,665,980,24,15,muted);text(s,String(pres.slides.items.length).padStart(2,'0'),1160,661,50,28,18,muted);s.speakerNotes.text='依据：docs/项目定位与业务共识.md，2026-10-27；outputs/club-launch-drafts-20261030/启动工作方案.md，2026-10-30。会籍配置、活动和交付为建议，不是已批准的对外承诺。';return s;}
function rows(s,list,y=235,gap=105){for(const[i,[head,body]]of list.entries()){text(s,head,74,y+i*gap,290,70,27,accent,true);text(s,body,392,y+i*gap,796,82,27,ink);}}
function table(s,values,y=245,height=270,widths){const t=s.tables.add({rows:values.length,columns:values[0].length,left:72,top:y,width:1136,height,values,columnWidths:widths});for(let i=0;i<values.length;i++)for(let j=0;j<values[i].length;j++){let c=t.getCell(i,j);c.fill=i===0?ink:(i%2?'#FFFFFF':paper);c.text.style={typeface:font,fontSize:24,color:i===0?'#FFFFFF':ink,bold:i===0,insets:12,verticalAlignment:'middle'};}t.borders.assign({style:'solid',fill:'#D8DDD1',width:1});return t;}
{
const s=pres.slides.add();s.background.fill=paper;text(s,'GATSBYCLUB',76,82,1000,48,24,accent);text(s,'俱乐部项目介绍',72,216,1120,110,64,ink,true);text(s,'线下交友与共同体验',76,355,1100,60,34);text(s,'会员方案与合作讨论',76,452,1100,40,24,muted);text(s,'项目名称待确认   2026年10月30日',76,610,1100,32,18,muted);s.speakerNotes.text='GatsbyClub是现有项目代号，不是本次确认的品牌名称。本演示供合伙人先修改再定稿，不使用竞争对手照片冒充本俱乐部实拍。';
}
rows(slide('在这里，可以怎样参加','按共同话题与参加目的认识彼此。'),[['交流正在做的事','主题餐桌、分享与讨论，认识相关经历的人。'],['一起体验生活','餐饮、艺术、运动和城市活动，给相处一个自然场景。'],['认真发展关系','有恋爱意愿的客户参加婚恋专场，伴侣可选择共同体验。']]);
rows(slide('适合的人','准入围绕教育、职业、资产、专业贡献或整体适配，具体按活动审核。'),[['付费参加者','愿意交流，有合适的时间和预算，希望扩大生活圈。'],['核心嘉宾','有专业内容、共同兴趣或活动贡献，愿意参与现场。'],['资源合作人','愿意链接合适客户和资源，能落实具体合作事项。']]);
rows(slide('活动内容','同一批客户，可以按自己的兴趣参加不同活动。'),[['主题餐桌','晚宴、下午茶、共同话题交流。'],['分享与运动','行业分享、艺术、网球、高尔夫等体验。'],['多日同行','旅行、游学及企业参访，按具体产品另行报名。']],225,115);
{
const s=slide('首场建议 主题下午茶','在北京认识几个聊得来的人，日期与场地待确认。');
text(s,'12人',78,252,320,86,58,accent,true);text(s,'3小时',455,252,320,86,58,accent,true);text(s,'880元/人',826,252,380,86,50,accent,true);
text(s,'建议规模',80,354,300,40,24);text(s,'主题交流与自由认识',455,354,330,48,24);text(s,'研究试价',832,354,350,40,24);
text(s,'包含茶点、主题引导、分组交流及基础物料。\n本场以普通交友为目的，不安排婚恋互选。',78,455,1100,100,28);
}
rows(slide('一次活动怎样认识彼此'),[['先了解','报名时说清自己的背景、兴趣和交流期待。'],['再相处','两人交流、分桌讨论与自愿换桌，主持人帮助接话。'],['结束后','自愿留下反馈和下次兴趣，双方同意后再建立联系。']]);
{
const s=slide('基础会员与理事权益建议','服务期暂按12个月讨论，具体权益及合同尚待确认。');
table(s,[['档位','价格框架','建议权益'],['基础会员','1,280元','2场沙龙、入会沟通与报名服务'],['理事会员','19,800元','12场沙龙、4场晚宴、2场体验及交流服务']],240,285,[210,220,706]);
text(s,'旅行、超出权益次数的活动及定制服务另行收费。',76,560,1120,55,24,muted);
}
rows(slide('会籍怎样使用'),[['报名与预约','按已公布日历选择活动，满员候补，特殊需求提前沟通。'],['每场说明','餐饮、器材、教练等含项分别写清，避免报名后产生误解。'],['使用与调整','本人权益、取消、延期与未使用权益处理，在确认文件中说明。']]);
rows(slide('怎样加入'),[['了解','先看活动主题、对象、规格与收费。'],['沟通与审核','用简短交流确认是否适合，再核实本场必要信息。'],['确认与参加','条款、收款及交付准备齐备后，再确认报名或会籍。']]);
rows(slide('隐私与现场体验'),[['信息有边界','只收集与审核和交付相关的资料，不公开敏感信息。'],['相处有选择','拍摄、换桌和交换联系方式尊重本人意愿。'],['服务有响应','主持与执行人员负责现场秩序、反馈和后续问题。']]);
rows(slide('旅行与游学方向','以下是产品构想，线路、承办及导师资源尚待核实。'),[['共同兴趣旅行','把同行者、现场组织与目的地服务分别设计。'],['企业参访与游学','先确认学习主题和真实交流机会，再安排旅行内容。'],['伴侣共同体验','按关系意愿设计活动，专业引导与服务边界另行确定。']]);
{
const s=slide('下一次见面','选择一个真正感兴趣的主题，再决定怎样长期参加。');text(s,'先了解主题和同行条件',78,250,1100,68,36,accent,true);text(s,'告诉我们想认识什么样的人、喜欢怎样的交流。\n具体活动开放后，由项目发起人说明安排与报名方式。',78,360,1100,140,30);text(s,'品牌名称、咨询入口与首场日期确认后补入正式对外版本。',78,560,1100,50,23,muted);
}
{
const s=slide('资源合作档价格与名额','以下价格与数量已统一，具体合作权益与名额规则仍待定。',true);
table(s,[['合作档','当前价格','配套名额'],['城市或资源合作','39,800元','3个名额'],['高阶资源合作','98,000元','6个名额']],240,270,[520,300,316]);text(s,'名额不自动等于现金返还、固定收益或公司股权。',76,560,1120,55,24,muted);
}
rows(slide('合作交付范围建议','按具体交付约定合作，外采费用另列。',true),[['39,800元档','本人理事权益、1场共创沙龙策划主持及3个名额。'],['98,000元档','本人理事权益、2场共创活动策划主持及6个名额。'],['共同确认','场地餐饮、制作、人员、内容、取消与额外费用分别写清。']]);
rows(slide('名额与收益待确认事项','先把规则和成本算清，再决定是否推出合作产品。',true),[['名额内容','基础或理事权益、审核、期限、本人及受邀者如何使用。'],['收益机制','推荐奖励、工作报酬及经营分配分别确认，不自动叠加。'],['交付与退出','履约标准、结算、退款、未完成事项及退出责任。']]);
rows(slide('合作确认流程','合作人身份与公司的股权投资安排分别处理。',true),[['确认适配','说明真实资源、能投入的时间与可执行的合作事项。'],['核算与约定','选定名额内容和交付清单，核算成本，交律师审定文件。'],['开始合作','批准预算和收款安排后执行，按实际交付与反馈复盘。']]);
await fs.mkdir(B+'qa/slides',{recursive:true});for(const[i,s]of pres.slides.items.entries()){const blob=await pres.export({slide:s,format:'png',scale:1});await fs.writeFile(B+`qa/slides/slide-${String(i+1).padStart(2,'0')}.png`,new Uint8Array(await blob.arrayBuffer()));}
await(await PresentationFile.exportPptx(pres)).save(B+'.build/candidate.pptx');
const{finalizePresentation}=await import(pathToFileURL(S+'/container_tools/artifact_tool_utils.mjs').href);
const final=B+'交付文件/俱乐部企业介绍与合作方案.pptx';
await finalizePresentation({workspaceDir:B,candidatePath:B+'.build/candidate.pptx',finalPath:final,pythonExecutable:'/Users/olivialee/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3',integrityValidatorPath:S+'/container_tools/inspect_presentation_package_integrity.py',layoutValidatorPath:S+'/container_tools/inspect_presentation_layout_geometry.py',layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit','--require-native-table-slide','7','--require-native-table-slide','13'],explicitTotalSlideCount:16,requiredNativeTableOwnerSlides:[7,13],fontPolicy:{basis:'design',families:[font]},verifyArtifactToolImport:true,receiptPath:B+'qa/PPT核验.json'});
console.log('Final editable PPTX exported',pres.slides.items.length);
