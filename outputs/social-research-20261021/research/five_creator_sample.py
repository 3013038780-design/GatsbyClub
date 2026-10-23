"""Bounded homepage sampling of the five-brand research accounts."""
import asyncio,json
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
def install(output:Path,limit:int):
 from media_platform.xhs.core import XiaoHongShuCrawler
 from store import xhs as xhs_store
 from var import source_keyword_var
 allowed={'钻石婚恋','大超说媒','陌上花开HIMMR','乐乐学姐优质脱单·陌上花开HIMMR','金凤凰深港婚恋','我主良缘'}
 def append(file,row):
  with (output/file).open('a') as f:f.write(json.dumps(row,ensure_ascii=False)+'\n')
 async def search(self):
  accounts={r['profile_url']:r for r in map(json.loads,(output/'brand-account-candidates.jsonl').read_text().splitlines()) if r['account_name'] in allowed}
  file=output/'xhs/jsonl/search_contents_2026-10-22.jsonl'
  existing={r['note_id']:r for r in map(json.loads,file.read_text().splitlines())} if file.exists() else {}
  for url,a in accounts.items():
   brand=a['brand'];name=a['account_name'];source_keyword_var.set(brand)
   print('FIVE_CREATOR_START',name,flush=True)
   now=datetime.now(ZoneInfo('Asia/Shanghai')).isoformat()
   try:
    result=await self.xhs_client.get_notes_by_creator(creator=url.rsplit('/',1)[-1],cursor='',page_size=30,xsec_source='pc_user')
    notes=result.get('notes',[])
    for i,n in enumerate(notes,1):
     append('creator-posted-cards.jsonl',dict(brand=brand,account=name,rank=i,note_id=n.get('note_id') or n.get('id'),title=n.get('display_title',''),metrics=n.get('interact_info',{}),collected_at=now))
    saved=0;older=0;reused=0
    for n in notes[:limit]:
     id=n.get('note_id') or n.get('id')
     if not id:continue
     if id in existing:
      reused+=1
      append('content-attribution.jsonl',dict(brand=brand,note_id=id,account_name=name,profile_url=url,verification='名称与简介匹配 主体待核验',sampling='主页顺序采样 既有正文复用',collected_at=now))
      if not n.get('interact_info',{}).get('sticky'):
       date=datetime.fromtimestamp(existing[id].get('time',0)/1000,ZoneInfo('Asia/Shanghai')).date().isoformat()
       older=older+1 if date<'2026-07-25' else 0
       if older>=3:break
      continue
     detail=await self.get_note_detail_async_task(note_id=id,xsec_source='pc_user',xsec_token=n.get('xsec_token',''),semaphore=asyncio.Semaphore(1))
     if detail:
      await xhs_store.update_xhs_note(detail);saved+=1
      append('content-attribution.jsonl',dict(brand=brand,note_id=id,account_name=name,profile_url=url,verification='名称与简介匹配 主体待核验',sampling='主页首屏最近发布 可能包含置顶 非全量',collected_at=now))
      date=datetime.fromtimestamp(detail.get('time',0)/1000,ZoneInfo('Asia/Shanghai')).date().isoformat()
      if not n.get('interact_info',{}).get('sticky'):
       older=older+1 if date<'2026-07-25' else 0
      if older>=3:break
     await asyncio.sleep(5)
    append('batch-status.jsonl',dict(brand=brand,stage='creator_sample',account=name,cards=len(notes),new_details=saved,reused_details=reused,collected_at=now))
    print('FIVE_CREATOR_DONE',name,'cards',len(notes),'new',saved,'reused',reused,flush=True)
   except Exception as e:
    append('batch-status.jsonl',dict(brand=brand,stage='creator_sample',error=type(e).__name__,collected_at=now))
    print('FIVE_CREATOR_ERROR',name,type(e).__name__,flush=True)
    if type(e).__name__ in ('PlatformAccessError','IPBlockError'):break
   await asyncio.sleep(5)
 XiaoHongShuCrawler.search=search
