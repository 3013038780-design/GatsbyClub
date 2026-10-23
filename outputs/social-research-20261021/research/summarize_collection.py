"""Create a readable local collection index and source archive."""
from pathlib import Path
import csv,html,json,zipfile,re
ROOT=Path(__file__).resolve().parents[1]/'collection-20261021'
data=json.loads((ROOT/'collection.json').read_text())
summary=json.loads((ROOT/'summary.json').read_text())
esc=lambda s:html.escape(str(s))
success=sum(p['状态']=='已采集' for p in data['pages'])
coverage=''.join('<tr>'+''.join(f'<td>{esc(r[k])}</td>' for k in ['机构','成功页数','失败页数','证据片段数','活动会籍链接数'])+'</tr>' for r in summary)
details=[]
verified=''.join(f'<tr><td>{esc(r["机构"])}</td><td>{esc(r["事实与适用条件"])}</td><td><b>{esc(r["数值"])}</b> {esc(r["单位"])}</td><td>{esc(r["资料时间"])}<br><a href="{esc(r["来源"])}">原始来源</a>{" · PDF第"+str(r["PDF页码"])+"页" if r["PDF页码"] else ""}</td></tr>' for r in data.get('verified_facts',[]))
for row in summary:
 brand=row['机构'];pages=[p for p in data['pages'] if p['机构']==brand]
 good=[p for p in pages if p['状态']=='已采集']; ev=[e for e in data['evidence'] if e['机构']==brand]
 links=''.join(f'<li><a href="{esc(p["网址"])}">{esc(p["网址"])}</a>　<span class="muted">{esc(p["状态"])}</span></li>' for p in pages)
 table=''.join(f'<tr><td>{esc(e["字段"])}</td><td>{esc(e["原文片段"])}</td><td><a href="{esc(e["来源"])}">原始来源</a>{" · PDF第"+str(e["PDF页码"])+"页" if e["PDF页码"] else ""}</td></tr>' for e in ev)
 details.append(f'<section><h2>{esc(brand)}</h2><p>成功采集 {len(good)} 页；检索到 {len(ev)} 条字段相关片段。</p><details><summary>采集页面</summary><ul>{links}</ul></details><details><summary>展开待复核原文片段</summary><table><thead><tr><th>研究字段</th><th>原文片段</th><th>出处</th></tr></thead><tbody>{table}</tbody></table></details></section>')
body=f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>高端社群公开资料采集结果</title><style>
body{{font-family:"Songti SC","SimSun",serif;color:#20252b;background:#f4f5f7;margin:0;line-height:1.8;font-size:16px}}main{{max-width:1040px;margin:32px auto;background:white;padding:48px 56px}}h1,h2,h3,summary,th{{font-family:"PingFang SC","Microsoft YaHei",sans-serif}}h1{{font-size:28px;line-height:1.4;margin:0 0 12px}}h2{{font-size:21px;margin:32px 0 12px}}p{{margin:12px 0}}.muted{{color:#65707a;font-size:14px}}.lead{{font-size:18px}}table{{border-collapse:collapse;width:100%;table-layout:fixed;font-size:15px;margin:20px 0}}th,td{{border:1px solid #d9dfe5;padding:12px 14px;vertical-align:top;overflow-wrap:anywhere}}th{{background:#edf1f5;text-align:left}}th:first-child{{width:20%}}section{{border-top:1px solid #d9dfe5;margin-top:30px}}a{{color:#24577c;text-underline-offset:3px}}summary{{cursor:pointer;font-weight:600;padding:10px 0}}li{{overflow-wrap:anywhere}}@media(max-width:700px){{main{{padding:26px 18px;margin:0}}table{{font-size:13px}}th,td{{padding:8px}}}}
</style><main><p class="muted">创业市场研究 · 公开资料采集批次 / 2026年10月21日</p><h1>高端社群公开资料采集结果</h1><p class="lead">本批覆盖 {len(summary)} 家候选机构，成功保存 {success} 个网页或PDF来源。</p><p>已安装并应用 Crawl4AI、Playwright 和 PyMuPDF。数据保留原始网页正文、PDF文件、采集时间与PDF页码；采集范围为官网、公开会籍规则、活动新闻和官方会员刊。</p><h2>采集覆盖</h2><table><thead><tr><th>机构</th><th>成功页数</th><th>失败页数</th><th>字段片段</th><th>会籍及活动链接</th></tr></thead><tbody>{coverage}</tbody></table><p class="muted">字段片段是自动检索出的研究线索，含导航或重复内容，需逐条复核；链接清单尚未逐条确定活动日期和举办状态。本批尚未形成近一年完整活动统计。小红书检索页本次连接中断，社交账号互动指标另行采集。</p><h2>数据文件</h2><ul><li><a href="机构采集覆盖.csv">机构采集覆盖.csv</a></li><li><a href="网页采集台账.csv">网页采集台账.csv</a></li><li><a href="价格权益及运营证据.csv">价格权益及运营证据.csv</a></li><li><a href="活动与会籍链接清单.csv">活动与会籍链接清单.csv</a></li></ul>{''.join(details)}</main></html>'''
body=body.replace('<h2>采集覆盖</h2>',f'<h2>已核对的价格与运营数据</h2><table><thead><tr><th>机构</th><th>事实与适用条件</th><th>数据</th><th>时间与来源</th></tr></thead><tbody>{verified}</tbody></table><p><a href="已核对价格与运营数据.csv">下载已核对数据表</a></p><h2>采集覆盖</h2>')
(ROOT/'采集结果索引.html').write_text(body,encoding='utf-8')
(ROOT/'使用说明.txt').write_text('本批次为公开资料采集结果。\n先打开采集结果索引.html查看覆盖情况；CSV文件可由Excel打开。\nraw目录保存网页正文、HTML和PDF；collection.json保存结构化采集记录。\n价格权益及运营证据.csv是自动检索片段，需逐条复核后进入正式报告。\n活动与会籍链接清单.csv含活动及会籍线索，尚未逐条核定举办日期与实际人数。\n小红书本轮检索页连接中断，未取得本轮品牌互动数据。\n',encoding='utf-8')
archive=ROOT.parent/'高端社群首批采集数据.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for p in ROOT.rglob('*'):
  if p.is_file() and p.name!='run.log':z.write(p,p.relative_to(ROOT))
print(json.dumps({'institutions':len(summary),'sources':len(data['pages']),'success':success,'snippets':len(data['evidence']),'links':len(data['activity_links']),'archive':str(archive),'index':str(ROOT/'采集结果索引.html')},ensure_ascii=False))
