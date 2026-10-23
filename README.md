# GatsbyClub 高端线下社群研究与商业方案

归档日期：2026年10月23日。研究资料主要核查截至2026年10月22日。

本仓库汇集“梳理中国婚恋市场调研来源”和“调研高端婚恋平台模式”两个聊天形成的项目成果：市场研究、机构对标、收费与客户分层、公开数据、线下活动与旅行设计、商业方案、财务模型、交互网站及讲解稿。

## 先看最新成果

- [正式研究报告 PDF](outputs/five-offline-matchmaking-20261022/交付文件/中国高端线下社群市场研究报告.pdf)
- [正式研究报告 Word](outputs/five-offline-matchmaking-20261022/交付文件/中国高端线下社群市场研究报告.docx)
- [研究数据 Excel](outputs/five-offline-matchmaking-20261022/交付文件/高端线下社群研究数据.xlsx)
- [本轮全套资料包](outputs/five-offline-matchmaking-20261022/中国高端线下社群市场研究资料_20261022.zip)
- [来源索引和公开明细](outputs/five-offline-matchmaking-20261022/交付文件/)

正式报告为23页排版修订版，包含17项可跳转目录。Excel包含36家机构、57项收费权益，另列客户画像、活动旅行、账号声量、内容明细和经营测算。婚恋专项重点研究钻石婚恋、大超说媒、HIMMR线下业务、我主良缘、金凤凰深港婚恋，同时保留会所、商学院和女性企业家社群参考。

近期平台动态用于补充活跃度和获客观察。历史资料按原年份阅读；企业自述、公开报价、分析假设和证据缺口依原稿标注。旧版样本选择和价格不能覆盖最新版结论。

## 网站和另一轮商业方案

- [网站源码与素材](private-club-site/)
- [交互网站离线 HTML](private-club-site/dist/index.html)：下载后用浏览器打开
- [商业计划交互版 HTML](club_research_20261019/output/北京香港私享俱乐部商业计划交互版.html)
- [北京香港私享社交俱乐部研究与商业方案 PDF](club_research_20261019/output/北京香港私享社交俱乐部研究与商业方案.pdf)
- [北京香港私享社交俱乐部研究与商业方案 Word](club_research_20261019/output/北京香港私享社交俱乐部研究与商业方案.docx)
- [网站讲解稿 Word](club_research_20261019/output/北京香港私享俱乐部网站讲解稿.docx)
- [财务模型](club_research_20261019/financial_model.json)及[逐月测算](club_research_20261019/financial_monthly.csv)
- [讲解稿内容和计算模型](club_research_20261019/speech_work/)

本地预览网站：

```bash
python3 -m http.server 8000 --directory private-club-site/dist
```

随后访问 `http://localhost:8000`。本次上传归档源码和成品，没有启用新的在线托管服务。

## 目录

| 路径 | 内容 |
| --- | --- |
| `outputs/five-offline-matchmaking-20261022/` | 最新研究报告、Excel、五家婚恋深挖、原文海报、公开采集、OCR和排版核验 |
| `outputs/offline-matchmaking-selection-20261022/` | 线下婚恋候选扩搜及选择依据 |
| `outputs/community-research-final-20261022/` | 上一轮综合报告和机构收费对照 |
| `outputs/matchmaking-review-20261022/` | 婚恋专项修订、案例档案、数据与历史版本 |
| `outputs/new-matchmaking-review-20261022/` | 新模式补充检索和采集记录 |
| `outputs/hkjc-membership-20261022/` | 香港赛马会会员、家属权益、消费收费及三图和四图资料 |
| `outputs/social-research-20261021/` | 宏观研究、机构地图、历轮报告和公开网页存档 |
| `private-club-site/` | 交互网站 HTML、CSS、JavaScript、数据、图片及构建脚本 |
| `club_research_20261019/` | 另一轮商业方案、财务模型、网站讲解稿及生成脚本 |
| `tools/MediaCrawler/` | 本次使用的第三方采集工具源码、原许可证及本地修订 |
| `archive/` | 归档范围、文件校验清单和工具来源 |

历轮版本、公开网页、数据文件、图表、海报、OCR和排版检查图片一并保留。日期较早的文件是研究过程存档；最终结论优先以上方“最新成果”为准。

## 工具与重建

本项目使用MediaCrawler采集公开平台内容，Crawl4AI及网页检索整理机构官网，Python和JavaScript脚本生成报告、Excel及网站。`tools/MediaCrawler/LICENSE`保留其原始授权条件；归档不改变第三方授权，也不构成对其他使用者的商业许可。工具基线和本地改动见[工具来源](archive/工具来源.md)。

报告和工作簿脚本沿用原Codex工作环境，部分运行时及文件路径需要在新的电脑上调整。为避免将账号状态和软件环境混入成果，仓库不包含浏览器登录资料、Cookie、密钥、二维码、Python虚拟环境、Node依赖、编译缓存和托管账号绑定配置。网站构建脚本已去除私人微信临时附件路径；所需图片保留在`dist/assets/`，图片来源见其中的`image-credits.json`。

文件内容、体积及SHA-256校验值见[文件清单](archive/文件清单.jsonl)。
