from pathlib import Path
import json,html,shutil,zipfile,hashlib
R=Path('/Users/olivialee/Documents/ChatGPT/社区平台'); B=R/'outputs/club-launch-drafts-20261030'; D=B/'交付文件'
x=json.loads((B/'启动方案内容.json').read_text()); esc=html.escape
shutil.copy2(B/'qa/manual/俱乐部启动工作方案.pdf',D/'俱乐部启动工作方案.pdf')
for p in D.glob('*.ndjson'):shutil.move(str(p),str(B/'qa'/p.name))
nav=[];sections=[]
for i,p in enumerate(x['pages'],1):
 nav.append(f'<a href="#s{i}">{i:02d} {esc(p["title"])}</a>')
 content=''.join(f'<p>{esc(v)}</p>' for v in p.get('paras',[]))
 if p.get('rows'):
  content+='<div class="table"><table><thead><tr>'+''.join('<th>'+esc(v)+'</th>' for v in p['headers'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+esc(str(v))+'</td>' for v in row)+'</tr>' for row in p['rows'])+'</tbody></table></div>'
 # Preserve all canonical footnote paragraphs, regardless of key name.
 for k,v in p.items():
  if k not in ('title','paras','headers','rows'):
   for s in (v if isinstance(v,list) else [v]):
    if isinstance(s,str):content+='<p class="note">'+esc(s)+'</p>'
 sections.append(f'<section id="s{i}"><div class="num">{i:02d} / 19</div><h2>{esc(p["title"])}</h2>{content}</section>')
css='''*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#f4f1e9;color:#233f36;font:17px/1.85 system-ui,-apple-system,"PingFang SC",sans-serif}aside{position:fixed;width:260px;inset:0 auto 0 0;overflow:auto;background:#213e35;color:white;padding:28px 20px}aside a{display:block;color:#eee;text-decoration:none;font-size:13px;line-height:1.6;padding:7px 0}main{margin-left:260px;padding:38px;max-width:1200px}header,section{background:#fffdf8;padding:32px 38px;margin-bottom:22px;border-radius:10px}h1{font-size:32px;line-height:1.5}h2{font-size:25px;line-height:1.5;margin-top:8px}.num{color:#a26542;font-size:13px}p{margin:18px 0}.note{color:#615c50;font-size:15px}.table{overflow-x:auto}table{border-collapse:collapse;min-width:620px;width:100%;font-size:15px}th{text-align:left;background:#e5ebe6}th,td{padding:13px 15px;vertical-align:top;border-bottom:1px solid #ddd}tr:nth-child(even){background:#f6f5ef}.tag{font-size:14px;color:#a26542}nav{display:none}@media(max-width:800px){aside{position:static;width:100%;max-height:none;padding:20px}aside a{display:inline-block;margin-right:18px;padding:4px 0}main{margin:0;padding:12px}header,section{padding:22px 18px}h1{font-size:27px}h2{font-size:23px}body{font-size:16px}.table{border-right:2px solid #ddd}}@media print{aside{display:none}main{margin:0;padding:0}section{break-before:page;border-radius:0}body{background:white}}'''
page='<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>俱乐部启动工作方案｜讨论稿</title><style>'+css+'</style><aside><b>启动工作方案</b><p>2026.10.30 · 合伙人讨论稿</p>'+''.join(nav)+'</aside><main><header><div class="tag">内部讨论与修改 · 尚未批准的配置保留为建议</div><h1>把俱乐部开起来，先把这八项工作说清楚</h1><p>定位客群、会员权益、成本、薪酬、排期、企业介绍、名字与外部对接。用目录跳转；手机上的宽表可以左右滑动。</p></header>'+''.join(sections)+'</main></html>'
(D/'俱乐部启动工作方案_直接打开.html').write_text(page)
readme='''# 俱乐部启动初稿资料包

2026-10-30 · 供两位合伙人修改，新增权益、工资、成本、活动均为建议或预算；基础文件的待定事项保持待定。

- 先看《俱乐部启动工作方案.pdf》（19页）；Word可改文字。
- 《俱乐部成本与薪酬测算.xlsx》仅4张表：单场活动、会员交付、人员薪酬、启动现金。黄色蓝字为输入；先选配套名额等级，再改人数和成本。不要覆盖公式。
- 《俱乐部企业介绍与合作方案.pptx》16页：前12页面向会员，后4页为合作讨论附页。正式使用前确认名称、权益、日期和联系人。
- HTML下载后直接用浏览器打开，无需账号或网络；手机宽表可左右滑动。

建议先讨论：首批客群、3/6个名额对应权益、全年供给和预算。当前假设下39,800元档配置3名理事会籍的直接贡献为-758.80元；20位付款者可能带来44位服务对象。不要把这些预算输出写成已验证业绩。

本轮没有预约场地、外联嘉宾、签约、收款或开户。律师收到的是业务需求清单，不是可直接签署的合同。品牌名称尚未核名。
'''
(D/'阅读说明.txt').write_text(readme)
zipfile_path=D/'俱乐部启动初稿_全套资料.zip'
with zipfile.ZipFile(zipfile_path,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(D.iterdir()):
  if p.is_file() and p.suffix!='.zip':z.write(p,p.name)
(B/'README.md').write_text('''# 俱乐部启动工作初稿

**2026-10-30 · 本轮建议稿，待合伙人修改。** 定位依据仍是[项目基础文件](../../docs/项目定位与业务共识.md)，不替代此前市场调研。

[下载全套](交付文件/俱乐部启动初稿_全套资料.zip) · [PDF](交付文件/俱乐部启动工作方案.pdf) · [可编辑Word](交付文件/俱乐部启动工作方案.docx) · [Excel](交付文件/俱乐部成本与薪酬测算.xlsx) · [PPT](交付文件/俱乐部企业介绍与合作方案.pptx) · [独立HTML](交付文件/俱乐部启动工作方案_直接打开.html)

| 工作 | 已完成的可修改稿 | 手册页 |
| --- | --- | --- |
| 客户与特色 | 人群假设、审核及访谈问题 | 2–3 |
| 会员权益 | 四档权益、预约、名额两种方案 | 4–6 |
| 员工与薪酬 | 工作职责、全职/前期方案、提成示例 | 7–8 |
| 交付成本 | 四表Excel，单场/全年/薪酬/现金模型 | 9–10 |
| 落地排期 | 六周排期、首场产品卡、当天流程 | 11–13 |
| 场地与背书 | Lust/梵悦询价表、合作分级和邀约文案 | 14–15 |
| 律师与合同 | 业务说明、合同需求和选律师问题 | 16 |
| 名称与收款 | 12个名字方向、订单收款准备流程 | 17 |
| 企业PPT | 16页可编辑会员介绍与合作附页 | 18 |
| 定案清单 | 分优先级的合伙人修改项 | 19 |

## 这版模型暴露的问题

- 配套名额等级影响很大：39,800元档若附3个完整理事名额，预算直接贡献-758.80元；基础名额方案为21,921.20元。名额等级仍待选。
- 默认20位付款者加配套名额，共44位服务对象；完整理事名额方案超出当前年度活动席位容量。
- 首场12人、880元/人的试价情景，单场贡献约1,962元；8人约亏152元。贡献尚未扣公司固定成本与税。
- 三个月无会员收款情景，当前启动准备额约64,988元；具体报价与人力条件待核实。

## 文件与核验

- `启动方案内容.json`为手册内容源，`prepare_content.py`生成内容，`build_manual.py`生成Word，`build_workbook.mjs`和`build_deck.mjs`生成Excel/PPT。
- 生成需要项目现有字体与bundled runtime；本地依赖不入库。表格和幻灯片使用artifact-tool，文档使用python-docx。
- `qa/`为19页手册、16页幻灯片及Excel检查；不需要发给客户。
- 新增建议没有变成当前销售承诺；没有实际签约、外联、收款或核名。历史研究和旧版测算保留原路径。
''')

print("Rebuilt deliverable package; repository navigation is maintained separately.")
