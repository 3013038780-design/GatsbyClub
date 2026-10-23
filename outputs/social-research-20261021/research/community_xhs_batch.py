"""Bounded brand discovery using MediaCrawler's authenticated XHS client."""
import asyncio,json,re
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path

def install_batch(output:Path,keywords:list[str],limit:int):
 import config
 from media_platform.xhs.core import XiaoHongShuCrawler
 from media_platform.xhs.help import get_search_id
 from media_platform.xhs.field import SearchSortType
 from store import xhs as xhs_store
 from var import source_keyword_var
 aliases={
  '北京香港马会会所':['北京香港马会','香港马会会所'],
  '长江商学院':['长江商学院'],
  '中欧国际工商学院':['中欧国际工商学院','中欧EMBA'],
  '北大汇丰EDP':['北大汇丰','北京大学汇丰'],
  'EO企业家组织':['EO企业家','EO上海','EO Shanghai'],
  'HIGHER CLUB':['HIGHER CLUB','Higherclub'],
  'HIMMR':['HIMMR','himmr'],
  '金凤凰深港婚恋':['金凤凰深港','深港金凤凰','金凤凰婚介'],
 }
 def append(name,row):
  with (output/name).open('a',encoding='utf-8') as f:f.write(json.dumps(row,ensure_ascii=False)+'\n')
 async def search(self):
  for keyword in keywords:
   source_keyword_var.set(keyword)
   now=datetime.now(ZoneInfo('Asia/Shanghai')).isoformat()
   print(f'BRAND_START {keyword}',flush=True)
   terms=aliases.get(keyword,[keyword])
   try:
    result=await self.xhs_client.get_note_by_keyword(keyword=keyword,search_id=get_search_id(),page=1,sort=SearchSortType.LATEST)
    items=[i for i in result.get('items',[]) if i.get('model_type')=='note']
    # Preserve search position and account identity as discovery evidence, not verification.
    selected=[];candidates=[]
    for rank,item in enumerate(items,1):
     card=item.get('note_card',{});user=card.get('user',{});name=user.get('nickname','');title=card.get('display_title','')
     is_candidate=any(t.lower() in name.lower() for t in terms)
     related=any(t.lower() in (title+' '+name).lower() for t in terms)
     public_url='https://www.xiaohongshu.com/explore/'+str(item.get('id',''))
     append('brand-search-cards.jsonl',dict(brand=keyword,sort='latest',rank=rank,title=title,note_url=public_url,account_name=name if is_candidate else '',account_status='名称匹配，认证待核验' if is_candidate else '非品牌核心样本',collected_at=now,metrics=card.get('interact_info',{})))
     if is_candidate:candidates.append((user,item))
     if related:selected.append(item)
    selected=selected[:limit]
    seen_creators=set()
    for user,item in candidates[:2]:
     uid=user.get('user_id')
     if not uid or uid in seen_creators:continue
     seen_creators.add(uid)
     try:
      info=await self.xhs_client.get_creator_info(uid,user.get('xsec_token','') or item.get('xsec_token',''),'pc_search')
      if info:
       append('brand-account-candidates.jsonl',dict(brand=keyword,profile_url='https://www.xiaohongshu.com/user/profile/'+uid,account_name=user.get('nickname',''),basic_info=info.get('basicInfo',{}),interactions=info.get('interactions',[]),tags=info.get('tags',[]),verification='待人工核验机构主体及认证',collected_at=now))
     except Exception as e:append('batch-status.jsonl',dict(brand=keyword,stage='account',error=type(e).__name__,collected_at=now))
     await asyncio.sleep(5)
    saved=0
    for item in selected:
     detail=await self.get_note_detail_async_task(note_id=item.get('id'),xsec_source=item.get('xsec_source') or 'pc_search',xsec_token=item.get('xsec_token'),semaphore=asyncio.Semaphore(1))
     if detail:
      await xhs_store.update_xhs_note(detail);saved+=1
      user=detail.get('user',{});name=user.get('nickname','')
      append('content-attribution.jsonl',dict(brand=keyword,note_id=detail.get('note_id'),account_name=name if any(t.lower() in name.lower() for t in terms) else '',profile_url='https://www.xiaohongshu.com/user/profile/'+user.get('user_id','') if any(t.lower() in name.lower() for t in terms) else '',verification='待核验',sampling='关键词最新排序中的相关内容，非随机样本',collected_at=now))
     await asyncio.sleep(5)
    append('batch-status.jsonl',dict(brand=keyword,stage='search',search_cards=len(items),related_details=saved,institution_account_candidates=len(seen_creators),collected_at=now))
    print(f'BRAND_DONE {keyword} search_cards={len(items)} details={saved} accounts={len(seen_creators)}',flush=True)
   except Exception as e:
    append('batch-status.jsonl',dict(brand=keyword,stage='search',error=type(e).__name__,message=str(e)[:120],collected_at=now));print(f'BRAND_ERROR {keyword} {type(e).__name__}',flush=True)
    # Respect access restrictions; do not rotate accounts or retry around a block.
    if type(e).__name__ in ('IPBlockError','PlatformAccessError'):break
   await asyncio.sleep(5)
 XiaoHongShuCrawler.search=search

def install_creator_sample(output:Path,limit:int):
 from media_platform.xhs.core import XiaoHongShuCrawler
 from store import xhs as xhs_store
 from var import source_keyword_var
 def append(name,row):
  with (output/name).open('a',encoding='utf-8') as f:f.write(json.dumps(row,ensure_ascii=False)+'\n')
 async def search(self):
  accounts={}
  for line in (output/'brand-account-candidates.jsonl').read_text().splitlines():
   r=json.loads(line)
   if r['account_name'] in ['中欧国际工商学院','长江商学院EMBA','木兰汇','领教工坊','正和岛']:accounts[r['profile_url']]=r
  for url,account in accounts.items():
   name=account['account_name'];brand=account['brand'];source_keyword_var.set(brand)
   print(f'CREATOR_START {name}',flush=True)
   try:
    result=await self.xhs_client.get_notes_by_creator(creator=url.rsplit('/',1)[-1],cursor='',page_size=30,xsec_source='pc_user')
    notes=result.get('notes',[]);saved=0
    for rank,item in enumerate(notes,1):
     append('creator-posted-cards.jsonl',dict(brand=brand,account_name=name,rank=rank,note_id=item.get('note_id') or item.get('id'),title=item.get('display_title',''),metrics=item.get('interact_info',{}),collected_at=datetime.now(ZoneInfo('Asia/Shanghai')).isoformat()))
    for item in notes[:limit]:
     noteid=item.get('note_id') or item.get('id')
     if not noteid:continue
     detail=await self.get_note_detail_async_task(note_id=noteid,xsec_source='pc_user',xsec_token=item.get('xsec_token',''),semaphore=asyncio.Semaphore(1))
     if detail:
      await xhs_store.update_xhs_note(detail);saved+=1
      append('content-attribution.jsonl',dict(brand=brand,note_id=detail.get('note_id'),account_name=name,profile_url=url,verification='机构名称匹配，认证待核验',sampling='机构名称匹配账号主页最近发布，按作者采集',collected_at=datetime.now(ZoneInfo('Asia/Shanghai')).isoformat()))
     await asyncio.sleep(5)
    append('batch-status.jsonl',dict(brand=brand,stage='creator',account_name=name,posted_cards=len(notes),related_details=saved,collected_at=datetime.now(ZoneInfo('Asia/Shanghai')).isoformat()))
    print(f'CREATOR_DONE {name} posted_cards={len(notes)} details={saved}',flush=True)
   except Exception as e:
    print(f'CREATOR_ERROR {name} {type(e).__name__}',flush=True)
    append('batch-status.jsonl',dict(brand=brand,stage='creator',error=type(e).__name__,collected_at=datetime.now(ZoneInfo('Asia/Shanghai')).isoformat()))
    if type(e).__name__ in ('IPBlockError','PlatformAccessError'):break
   await asyncio.sleep(5)
 XiaoHongShuCrawler.search=search
