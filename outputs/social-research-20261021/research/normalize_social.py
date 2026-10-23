"""Normalize observed public metrics without treating missing values as zero."""
import csv,json,re
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from urllib.parse import urlsplit,urlunsplit
ROOT=Path(__file__).resolve().parents[1]/'social-platforms'
FIELDS=['平台','候选机构关键词','内容ID','标题','正文','发布时间','采集时间','点赞','收藏','评论','分享','播放','投币','弹幕','是否品牌官方账号','账号粉丝数','来源']
def number(value):
 if value is None or str(value).strip().lower() in ('','none','null','nan','-'):return None
 s=str(value).strip().replace(',','').replace('+','')
 try:
  multiplier=10000 if s.endswith('万') else 1000 if s.lower().endswith('k') else 1
  return float(s[:-1])*multiplier if multiplier!=1 else int(s)
 except ValueError:return None
def date(value):
 try:
  n=float(value)
  if n>1e11:n/=1000
  return datetime.fromtimestamp(n,ZoneInfo('Asia/Shanghai')).isoformat()
 except (ValueError,TypeError,OSError):return ''
rows=[];records={}
for path in ROOT.rglob('*.jsonl'):
 for line in path.read_text(encoding='utf-8').splitlines():
  if not line.strip():continue
  r=json.loads(line)
  if not (('note_url' in r and 'note_id' in r) or ('aweme_url' in r and 'aweme_id' in r) or 'video_play_count' in r):continue
  platform='小红书' if 'note_url' in r else '抖音' if 'aweme_url' in r else 'B站'
  cid=str(r.get('note_id') or r.get('aweme_id') or r.get('video_id') or '')
  key=(platform,cid)
  if key in records and number(records[key].get('last_modify_ts')) is not None and (number(r.get('last_modify_ts')) or 0)<number(records[key].get('last_modify_ts')):continue
  records[key]=r
attribution={}
vp=ROOT/'verified-brand-accounts.json'
verified={a['profile_url']:a for a in json.loads(vp.read_text())} if vp.exists() else {}
fans={}
cp=ROOT/'brand-account-candidates.jsonl'
if cp.exists():
 for line in cp.read_text().splitlines():
  c=json.loads(line)
  fans[c['profile_url']]=next((number(i.get('count')) for i in c.get('interactions',[]) if i.get('type')=='fans'),None)
ap=ROOT/'content-attribution.jsonl'
if ap.exists():
 for line in ap.read_text().splitlines():
  a=json.loads(line);attribution[str(a.get('note_id',''))]=a
for (platform,cid),r in records.items():
  url=r.get('note_url') or r.get('aweme_url') or r.get('video_url') or ''
  u=urlsplit(url);url=urlunsplit((u.scheme,u.netloc,u.path,'',''))
  rows.append(dict(zip(FIELDS,[platform,r.get('source_keyword',''),cid,r.get('title',''),r.get('desc',''),date(r.get('time',r.get('create_time'))),date(r.get('last_modify_ts')),number(r.get('liked_count')),number(r.get('collected_count',r.get('video_favorite_count'))),number(r.get('comment_count',r.get('video_comment'))),number(r.get('share_count',r.get('video_share_count'))),number(r.get('video_play_count')),number(r.get('video_coin_count')),number(r.get('video_danmaku')),'待核验',None,url])))
  a=attribution.get(cid,{})
  if a:rows[-1]['候选机构关键词']=a.get('brand','');rows[-1]['是否品牌官方账号']='机构名称匹配，主体待核验' if a.get('account_name') else '非机构账号核心样本'
  if a.get('profile_url') in verified:
   rows[-1]['是否品牌官方账号']='已核对主页认证标识的机构账号'
   rows[-1]['账号粉丝数']=fans.get(a['profile_url'])
ROOT.mkdir(exist_ok=True)
(ROOT/'统一内容指标.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
with (ROOT/'统一内容指标.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader()
 for row in rows:
  w.writerow({k: "'"+v if isinstance(v,str) and v.startswith(('=','+','-','@')) else v for k,v in row.items()})
print(json.dumps({'normalized_content_rows':len(rows),'output':str(ROOT/'统一内容指标.csv')},ensure_ascii=False))
