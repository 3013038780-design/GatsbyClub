import json,html
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/'community-supplement'
d=json.loads((ROOT/'curated-data.json').read_text())
tables={t['name']:t for t in d['tables']}
def e(x):return html.escape(str(x if x is not None else '待补'))
def grid(headers,rows):
 return '<div class="table-wrap"><table><thead><tr>'+''.join('<th>'+e(x)+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+e(x)+'</td>' for x in r)+'</tr>' for r in rows)+'</tbody></table></div>'
parts=['''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>中国高端社群补充调研</title><style>
:root{--ink:#172c3a;--muted:#687580;--line:#dce3e8;--navy:#223c50}*{box-sizing:border-box}body{margin:0;background:#edf0f3;color:var(--ink);font:16px/1.85 "Songti SC","SimSun",serif}main{max-width:1100px;margin:35px auto;background:#fff;padding:54px 64px 70px;box-shadow:0 5px 24px #2434420a}h1,h2,h3,nav,th,.meta{font-family:"PingFang SC","Microsoft YaHei",sans-serif}h1{font-size:30px;line-height:1.45;margin:0 0 14px;font-weight:650}h2{font-size:22px;margin:44px 0 18px;padding-top:13px;border-top:2px solid var(--navy)}h3{font-size:17px;line-height:1.6;margin:25px 0 8px}p{margin:9px 0 16px}a{color:#295a7b;text-decoration:none}a:hover{text-decoration:underline}.meta{font-size:13px;color:var(--muted)}nav{display:flex;flex-wrap:wrap;gap:8px 21px;border-block:1px solid var(--line);padding:13px 0;margin:25px 0 30px;font-size:14px}.lead{font-size:18px;line-height:1.9}.table-wrap{overflow:auto;margin:16px 0 26px}table{border-collapse:collapse;width:100%;font:14px/1.75 "PingFang SC","Microsoft YaHei",sans-serif}th{background:#edf2f5;text-align:left;font-weight:600;color:#223c50}th,td{padding:11px 12px;border-bottom:1px solid var(--line);vertical-align:top;min-width:82px}td:first-child{font-weight:500}tbody tr:nth-child(even){background:#fafbfc}.source{font:12px/1.7 "PingFang SC",sans-serif;color:var(--muted);margin-top:6px}.event{border-left:3px solid #a8bbc8;padding:1px 0 1px 20px;margin:22px 0}.event p{margin-bottom:8px}.foot{margin-top:35px;padding-top:15px;border-top:1px solid var(--line)}@media(max-width:800px){main{margin:0;padding:28px 22px}h1{font-size:26px}body{font-size:16px}td{min-width:125px}}@media print{@page{size:A4;margin:21mm 18mm}body{background:#fff;font-size:12pt}main{padding:0;margin:0;box-shadow:none;max-width:none}h1{font-size:22pt}h2{font-size:16pt;break-after:avoid}h3{break-after:avoid}table{font-size:9pt;line-height:1.6}tr{break-inside:avoid}nav{display:none}.table-wrap{overflow:visible}a{color:inherit}.source{font-size:9pt}}
</style><main><div class="meta">创业市场研究 · 机构经营与社群运营专题</div><h1>中国高端社群补充调研</h1>''']
parts.append(f'<div class="meta">更新于 {e(d["generated_at"][:16].replace("T"," "))}　资料所属年份逐项列示</div>')
parts.append('<nav><a href="#takeaways">对公司的启示</a><a href="#brands">机构比较</a><a href="#price">价格和权益</a><a href="#people">客户和获客</a><a href="#events">活动交付</a><a href="#activity">规模与活跃</a><a href="#social">平台内容</a><a href="#gaps">待补数据</a><a href="#sources">来源</a></nav>')
parts.append('<p class="lead">本轮围绕“持续组织高端人群见面”补充机构资料，比较综合会员俱乐部、校友社群、企业家小组、女性社群和运动会员组织。价格、权益、客户、获客、交付与活跃度分别整理，明细见配套工作簿。</p>')
parts.append('<h2 id="takeaways">一、对拟设公司的启示</h2>')
for title,body in d['findings']:parts.append(f'<h3>{e(title)}</h3><p>{e(body)}</p>')
parts.append('<h2 id="brands">二、机构比较与研究重点</h2>')
parts.append('<p>六家核心对照分别覆盖综合生活方式、家庭会员、兴趣活动、学习校友、企业家同伴及女性社群。中欧、领教工坊、北大汇丰等保留为专题对照，补足定价、运营岗位和校友活动设计。</p>')
rows=tables['机构与研究重点']['rows']
parts.append(grid(['机构','研究层级与模式','规模与经营资料','具体研究价值'],[[r[0],r[1]+'；'+r[2],r[3],r[4]] for r in rows]))
parts.append('<h2 id="price">三、价格、收费结构与会员权益</h2>')
pr=tables['价格与收费']['rows']
parts.append(grid(['机构与产品','公开金额','适用时间及收费单位','包含与另付'],[[r[0]+' '+r[2],f'{r[3]:,} '+('元' if r[4]=='CNY' else '美元'),r[6]+'；'+r[5],r[7]+'。另付：'+r[8]+'。来源：'+r[10]] for r in pr if r[3] is not None]))
parts.append('<h3>三种收费逻辑值得分别比较</h3><p>香港马会体现会籍入会费加后续消费；EO体现年度会费加一次入会费；长江和中欧体现完整学习项目收费及校友关系。拟设公司的价格方案需要同时写清会员包含的服务频次、每场另付金额、伴侣及家属名额、差旅承担和退改条件。</p>')
parts.append(grid(['机构','产品层级','具体权益和使用方式'],[[r[0],r[1],r[2]+'。'+r[3]+'。'+r[4]+'。来源：'+r[5]] for r in tables['产品与会员权益']['rows']]))
parts.append('<h2 id="people">四、客户画像与获客路径</h2>')
parts.append(grid(['机构','资料反映的客户','需求及关系建立'],[[r[0],r[2],r[3]+'。'+r[4]+'。来源：'+r[6]] for r in tables['客户画像']['rows']]))
parts.append(grid(['机构','渠道与内容','可见转化及推荐'],[[r[0],r[1]+'。'+r[2],r[3]+'。'+r[4]+'。来源：'+r[6]] for r in tables['获客与转化']['rows']]))
parts.append('<h2 id="events">五、活动如何交付</h2>')
for r in tables['活动流程']['rows']:
 parts.append(f'<article class="event"><h3>{e(r[0])}：{e(r[1])}</h3><div class="meta">{e(r[2])}　{e(r[3])}</div><p><strong>对象与场景：</strong>{e(r[4])}</p><p><strong>环节：</strong>{e(r[5])}</p><p><strong>人员：</strong>{e(r[6])}</p><div class="source">来源 {e(r[8])}。待补：{e(r[7])}</div></article>')
parts.append('<h2 id="activity">六、规模、参与和续费</h2>')
mr=[]
for r in tables['规模与活跃度']['rows']:
 if r[2] is None:continue
 val=(str(round(r[2]*100,1))+'%'+('以上' if r[3]=='以上' else '')) if r[3] in ['比例','以上'] else f'{r[2]} {r[3]}' if r[3]=='年' else f'{r[2]:,} {r[3]}'
 mr.append([r[0],r[1],val,r[4]+'。'+r[5]+'。'+r[6]])
parts.append(grid(['机构','指标','数值','统计范围和来源'],mr))
parts.append('<h2 id="social">七、小红书机构账号与内容样本</h2>')
ar=tables['平台机构账号']
parts.append(grid([ar['headers'][i] for i in [1,2,3,7,8,4]],[[r[i] for i in [1,2,3,7,8,4]] for r in ar['rows'] if '移出' not in r[4]]))
content=tables['平台内容明细']['rows']
brandposts=[r for r in content if r[10]=='已核对主页认证标识的机构账号' and r[4][:10]>='2026-07-23' and '本科招生' not in r[12]]
brandposts.sort(key=lambda r:(r[6] or 0),reverse=True)
parts.append(f'<p>当前已归一化内容 {len(content)} 条。长江EMBA与中欧的认证账号各采集24条主页内容，其中各23条在近90天内。剔除中欧1条本科招生活动后，两家共 {len(brandposts)} 条近期相关内容。以下按样本内点赞排序展示，逐条保留互动、发布时间和原文链接。</p>')
parts.append(grid(['机构关键词','标题与发布时间','点赞','收藏','评论','分享'],[[r[1],r[3]+'；'+str(r[4])[:10],r[6],r[7],r[8],r[9]] for r in brandposts[:12]]))
parts.append('<h2 id="gaps">八、仍需补充的经营数据</h2>')
parts.append(grid(['模块','关键缺口','后续验证'],[[r[0],r[2],r[4]] for r in tables['待补数据']['rows']]))
parts.append('<h2 id="sources">来源与查阅</h2><p>配套工作簿按模块列示每条记录，源ID集中对应下列资料。原始网页、PDF和平台记录已保存在本项目；登录状态独立存放。</p>')
for r in tables['来源台账']['rows']:parts.append(f'<p class="source">{e(r[0])}　{e(r[1])}　<a href="{e(r[3])}" target="_blank" rel="noreferrer">{e(r[2])}</a>　{e(r[4])}；{e(r[7])}</p>')
parts.append('<p class="foot"><a href="高端社群补充调研工作簿.xlsx">打开配套工作簿</a></p></main></html>')
(ROOT/'高端社群补充调研.html').write_text(''.join(parts))
print(ROOT/'高端社群补充调研.html')
