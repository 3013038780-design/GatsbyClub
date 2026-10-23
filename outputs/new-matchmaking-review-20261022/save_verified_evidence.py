from pathlib import Path
import csv,json
B=Path(__file__).resolve().parent
profile='https://www.douyin.com/user/MS4wLjABAAAALIHRWrJxwmo4LaeEqAPHHfrBlL_lexxrdc83OeXvSuysOixUI_5ys_rm2RCBgFX6'
rows=[['大超说媒','粉丝','7.2万','抖音号dachaoshuomei05；主页显示值',profile],['大超说媒','获赞','166.1万','账号主页累计获赞显示值',profile],['大超说媒','作品','337','账号当前作品标签',profile],['大超说媒','择偶定位','999','大超本人；主页未注明服务时长及退改',profile],['大超说媒','择偶定位','199','机构老师；主页未注明服务时长及退改',profile],['大超说媒','活动预告','10.11深圳；10.18北京清北；10.25上海高净值','品牌主页招募；预告和已举办分开',profile],['陌上花开','App银桃主','199元','iOS商品页；展示未标期限','https://apps.apple.com/cn/app/id6449488341'],['陌上花开','App金桃主','499元','iOS商品页；展示未标期限','https://apps.apple.com/cn/app/id6449488341'],['陌上花开','活动规模','每年500+场；累计参与10万+','官网自述；统计截止期未标，非2026已举办核算','https://www.himmr.tech/'],['青藤之恋','线上精选嘉宾','40元/10位','iOS公开商品；非顾问婚介','https://apps.apple.com/cn/app/id1472343551'],['青藤之恋','曝光','108元/档','iOS公开商品','https://apps.apple.com/cn/app/id1472343551'],['恋爱主理人','牵线','99元/次；239元/3次；369元/5次','武汉荟友同一经营主体的新产品；不另计独立机构','https://apps.apple.com/cn/app/id6762596550'],['恋爱主理人','服务承诺','3天未牵上线退还次数','商店开发者描述；非承诺3天恋爱成功','https://apps.apple.com/cn/app/id6762596550'],['牵手','VIP','29元/周；60元/月；138元/3个月','iOS自动订阅公开商品','https://apps.apple.com/cn/app/id1475216610'],['牵手','查看谁喜欢我','46元/周；88元/月；188元/3个月','与VIP单独列商品','https://apps.apple.com/cn/app/id1475216610']]
with (B/'近期婚恋平台核查明细.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['机构或产品','字段','页面数值或内容','口径','来源网址','采集日期']);w.writerows([r+['2026-10-22'] for r in rows])
posts=[['还是得有一个清晰的画像','2026-09-30 12:29',832,71,283,107,'https://www.douyin.com/video/7690856197508205903'],['十一不出京的来相亲','2026-09-27 21:06',73,3,3,6,'https://www.douyin.com/video/7690200643226913187']]
with (B/'大超说媒已核验互动.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['标题','发布时间','点赞','评论','收藏','分享','视频链接','采集日期','口径']);w.writerows([p+['2026-10-22','浏览器视频页实时显示；两条用途不同的样本，不作全账号均值'] for p in posts])
(B/'核查说明.txt').write_text('本轮以当前抖音页面、品牌官网、App Store开发者页面为主要来源。Crawl4AI六次尝试中五页取得正文，青藤协议页未取得正文。大超抖音由已登录浏览器核对；没有把它写成MediaCrawler批量抓取。主页可见56条作品卡片，只有两条已核对完整互动字段。旧价格及2011年旅行不作为当前产品证据。\n')
print('Saved 15 evidence records and 2 verified posts.')
