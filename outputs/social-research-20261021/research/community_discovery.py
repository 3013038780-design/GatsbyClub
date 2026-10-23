"""Discover beyond the supplied brand list, preserving platform search scope."""
import asyncio,json
from datetime import datetime
from zoneinfo import ZoneInfo

def install_discovery(output,keywords,limit):
 from media_platform.xhs.core import XiaoHongShuCrawler
 from media_platform.xhs.help import get_search_id
 from media_platform.xhs.field import SearchSortType
 def save(name,row):
  with (output/name).open('a') as f:f.write(json.dumps(row,ensure_ascii=False)+'\n')
 async def search(self):
  profiled=set()
  for keyword in keywords:
   for label,sort in [('热度',SearchSortType.MOST_POPULAR),('最新',SearchSortType.LATEST)]:
    stamp=datetime.now(ZoneInfo('Asia/Shanghai')).isoformat()
    try:
     response=await self.xhs_client.get_note_by_keyword(keyword=keyword,search_id=get_search_id(),page=1,sort=sort)
     items=[r for r in response.get('items',[]) if r.get('model_type')=='note']
     for rank,item in enumerate(items,1):
      card=item.get('note_card',{});user=card.get('user',{});uid=user.get('user_id','');name=user.get('nickname','')
      save('discovery-search-cards.jsonl',dict(keyword=keyword,sort=label,rank=rank,title=card.get('display_title',''),account_name=name,profile_url='https://www.xiaohongshu.com/user/profile/'+uid,note_url='https://www.xiaohongshu.com/explore/'+item.get('id',''),metrics=card.get('interact_info',{}),captured_at=stamp,verification='待核验机构主体'))
      if uid and uid not in profiled and len(profiled)<8 and any(t in name.lower() for t in ['俱乐部','社群','游艇','商学','同学会','会所','商会','高尔夫','club','kupu']) and not any(t in name for t in ['电竞','陪玩','观察员','保险','培训师']):
       profiled.add(uid)
       try:
        info=await self.xhs_client.get_creator_info(uid,user.get('xsec_token','') or item.get('xsec_token',''),'pc_search')
        if info:save('discovery-account-candidates.jsonl',dict(keyword=keyword,account_name=name,profile_url='https://www.xiaohongshu.com/user/profile/'+uid,basic_info=info.get('basicInfo',{}),interactions=info.get('interactions',[]),captured_at=stamp,verification='待核验机构主体'))
       except Exception as exc:
        save('discovery-status.jsonl',dict(keyword=keyword,stage='profile',error=type(exc).__name__))
        if type(exc).__name__ in ['IPBlockError','PlatformAccessError','RetryError']:return
       await asyncio.sleep(15)
     save('discovery-status.jsonl',dict(keyword=keyword,sort=label,search_cards=len(items),captured_at=stamp))
     print(f'DISCOVERY_DONE {keyword} {label} cards={len(items)}',flush=True)
    except Exception as exc:
     save('discovery-status.jsonl',dict(keyword=keyword,sort=label,error=type(exc).__name__,captured_at=stamp));print(f'DISCOVERY_ERROR {keyword} {type(exc).__name__}',flush=True)
     # Upstream retry wrappers can hide a verification response. Stop this batch.
     if type(exc).__name__ in ['IPBlockError','PlatformAccessError','RetryError']:return
    await asyncio.sleep(15)
 XiaoHongShuCrawler.search=search

def install_profile_probe(output):
 from media_platform.xhs.core import XiaoHongShuCrawler
 async def search(self):
  names={'Kupu-kupu','SHE ACE CLUB',"The Queen's Circle",'不上班姐姐俱乐部 【北京总部】'}
  candidates={}
  for line in (output/'discovery-search-cards.jsonl').read_text().splitlines():
   row=json.loads(line)
   if row['account_name'] in names:candidates[row['profile_url']]=row
  for url,row in candidates.items():
   try:
    info=await self.xhs_client.get_creator_info(url.rsplit('/',1)[-1])
    if info:
     data=dict(keyword=row['keyword'],account_name=row['account_name'],profile_url=url,basic_info=info.get('basicInfo',{}),interactions=info.get('interactions',[]),captured_at=datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(),verification='品牌候选，主体与高端客户定位待核验')
     with (output/'discovery-account-candidates.jsonl').open('a') as f:f.write(json.dumps(data,ensure_ascii=False)+'\n')
     print('PROFILE_PROBE_DONE '+row['account_name'],flush=True)
   except Exception as exc:
    print('PROFILE_PROBE_ERROR '+row['account_name']+' '+type(exc).__name__,flush=True)
    if type(exc).__name__ in ['PlatformAccessError','IPBlockError','RetryError']:return
   await asyncio.sleep(15)
 XiaoHongShuCrawler.search=search
