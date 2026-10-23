from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from datetime import datetime
import json,csv,shutil,html,hashlib
from findings import BASE,SOURCES,PRICES,TRAVEL
O=BASE/'交付文件';oldroot=BASE.parent/'social-research-20261021/交付资料';old=oldroot/'正式文件';archive=oldroot/'历史版本/20261021';archive.mkdir(parents=True,exist_ok=True)
for p in old.glob('*'):
 if p.is_file() and p.suffix in ['.docx','.pdf','.xlsx'] and not (archive/p.name).exists():shutil.copy2(p,archive/p.name)
for p in O.glob('*.inspect.ndjson'):p.unlink()
# Portable CSV files for the newly collected evidence.
def csvwrite(name,header,rows):
 with (O/name).open('w',encoding='utf-8-sig',newline='') as f:csv.writer(f).writerows([header]+rows)
csvwrite('婚恋机构来源索引.csv',['编号','资料名称','原文网址','适用时间与范围','证据类别'],[[k,*v] for k,v in SOURCES.items()])
csvwrite('婚恋机构收费明细.csv',['机构','收费项目','金额','币种','收费单位','适用时间','包含权益','另付与限制','来源编号','证据类别'],PRICES)
csvwrite('婚恋与旅游结合对照.csv',['机构及项目','资料时期','已确认内容','仍缺什么','研究判断','来源编号'],TRAVEL)
cat=json.loads((BASE/'jfh-activity-catalog.json').read_text());csvwrite('金凤凰官网活动目录观察.csv',['活动标题','报名截止日','页面报名人数','原文网址','目录页码'],[[r['title'],r['deadline'],r['registrations'],r['url'],r['listing_page']] for r in cat])
shutil.copy2(BASE/'qa/新增来源链接检查.csv',O/'新增来源链接检查.csv')
# Detailed raw source archives stay in research folders; the deliverable contains original links and structured facts.
metrics=json.loads((BASE/'qa/PDF验收.json').read_text());report_pages=metrics['report']['pages'];external_links=metrics['report']['external_links']
files=sorted(p for p in O.iterdir() if p.suffix in ['.pdf','.docx','.xlsx','.csv'])
intro='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>高端会员社群市场研究资料目录</title><style>body{font:16px/1.8 -apple-system,"PingFang SC",sans-serif;max-width:1080px;margin:45px auto;padding:0 26px;color:#222}h1{font-size:28px}h2{font-size:21px;margin-top:30px}table{border-collapse:collapse;width:100%}th,td{border-bottom:1px solid #ddd;padding:10px;text-align:left}th{background:#e8edf1}a{color:#295878}</style><h1>高端会员社群市场研究资料目录</h1><p>2026年10月22日婚恋与旅游专题更新。正式报告33页、六家案例16页、合伙人摘要2页；工作簿31家机构、28张表、103条收费记录。旧记录保留原统计和采集日期。</p><h2>本次研究调整</h2><p>主对标为北京香港马会会所、长江商学院、木兰汇、正和岛、优家荟、我主良缘、金凤凰深港婚恋和珍爱网。EO保留为固定小组专题。三家婚恋机构分别用于研究产品组合、区域活动和规模服务转型，不按“高端”名称判断客群或经营质量。</p><p>旅游专题分别列品牌定位、室内联谊、景区一日相亲及多日旅行。历史产品明确年份；当前未取得的定制价、有效付费和财务字段在Excel保留。</p><h2>文件下载</h2><table><tr><th>文件</th><th>说明</th></tr>'''
intro=intro.replace('正式报告33页',f'正式报告{report_pages}页').replace('六家案例16页',f"六家案例{metrics['cases']['pages']}页")
notes={'.docx':'可编辑Word','.pdf':'可点击来源及目录的PDF','.xlsx':'31家机构及婚恋旅游专题','.csv':'可筛选的明细数据'}
for p in files:intro+=f'<tr><td><a href="{html.escape(p.name)}">{html.escape(p.name)}</a></td><td>{notes[p.suffix]}</td></tr>'
intro+='</table><h2>链接核验</h2><p>正式报告保留待核验处外部链接及13处目录跳转。28条新增来源进行网络连接检查，27条取得低于400的HTTP响应；监管总局页面对直接请求返回限制，正文已通过网页检索工具核对。PDF链接注释及目录目标已检查；网页是否要求登录由各网站决定。</p><h2>平台补抓</h2><p>本轮MediaCrawler访问小红书首页超时，没有新增经过核验的粉丝、评论和分享数据。Excel保留原平台样本，未用空值替代成零。Crawl4AI本轮渲染了我主良缘活动入口与珍爱首页。</p></html>'
intro=intro.replace('待核验处',str(external_links)+'处').replace('、正和岛、优家荟','')
(O/'资料目录.html').write_text(intro)
(O/'交付说明.txt').write_text('请先打开资料目录.html。\n正式报告和六家档案已加入三家婚恋深查及旅游专题，EO移为固定小组参考。\nExcel移除正和岛、优家荟，现有31家机构、103项收费记录；婚恋专题保留，保留实际值、历史合同、机构自述和未知的分类。\n原始登录状态、Cookie、个人会员明细及采集进程日志不进入资料包。\n研究核查截止2026年10月22日，旧资料保留原统计期。\n')
# Publish revised current files; old selections remain only in the history folder.
for stale in ['八家会员社群与婚恋机构对标案例档案.docx','八家会员社群与婚恋机构对标案例档案.pdf','中国高端会员社群市场研究数据工作簿_33家机构.xlsx']:
 if (old/stale).exists():(old/stale).unlink()
# Publish updated current files beside earlier materials, while keeping an archival copy.
for p in O.glob('*'):
 if p.suffix in ['.docx','.pdf','.xlsx']:shutil.copy2(p,old/p.name)
newdata=oldroot/'数据明细/婚恋与旅游专题20261022';newdata.mkdir(exist_ok=True)
for p in O.glob('*.csv'):shutil.copy2(p,newdata/p.name)
current_files=sorted(p for p in O.iterdir() if p.suffix in ['.docx','.pdf','.xlsx'])
rootindex=intro[:intro.index('<h2>文件下载</h2>')]+'<h2>当前正式文件</h2><ul>'
for p in current_files:rootindex+=f'<li><a href="正式文件/{html.escape(p.name)}">{html.escape(p.name)}</a></li>'
rootindex+='</ul><h2>新增来源及收费明细</h2><ul>'
for p in newdata.glob('*.csv'):rootindex+=f'<li><a href="数据明细/婚恋与旅游专题20261022/{html.escape(p.name)}">{html.escape(p.name)}</a></li>'
rootindex+='</ul><p>历史版本保留于历史版本文件夹；公开网页存档与此前全部数据明细继续保留。</p></html>'
(oldroot/'资料目录.html').write_text(rootindex);(oldroot/'交付说明.txt').write_text((O/'交付说明.txt').read_text())
# Check portable links and package integrity.
allfiles=sorted(p for p in O.iterdir() if p.is_file());zipname=BASE/'高端会员社群市场研究更新资料_20261022.zip'
with ZipFile(zipname,'w',ZIP_DEFLATED) as z:
 for p in allfiles:z.write(p,'高端会员社群市场研究资料/'+p.name)
with ZipFile(zipname) as z:assert z.testzip() is None
manifest=[{'file':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in allfiles]
(BASE/'qa/交付清单.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print(json.dumps({'zip':str(zipname),'files':len(allfiles),'bytes':zipname.stat().st_size,'current_files':[p.name for p in current_files]},ensure_ascii=False))
