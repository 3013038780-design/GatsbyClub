from pathlib import Path
import os,sys,asyncio,json
W=Path(__file__).resolve().parents[2];repo=W/'tools/MediaCrawler';out=W/'outputs/new-matchmaking-review-20261022/mediacrawler';out.mkdir(exist_ok=True)
os.chdir(repo);sys.path.insert(0,str(repo));os.environ['PATH']='/Users/olivialee/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin:'+os.environ['PATH']
import config
config.PLATFORM='dy';config.ENABLE_CDP_MODE=False;config.CDP_CONNECT_EXISTING=False;config.HEADLESS=True;config.SAVE_LOGIN_STATE=True;config.USER_DATA_DIR='community_research_%s';config.ENABLE_IP_PROXY=False;config.SAVE_DATA_OPTION='jsonl';config.SAVE_DATA_PATH=str(out);config.CRAWLER_MAX_NOTES_COUNT=60;config.MAX_CONCURRENCY_NUM=1;config.CRAWLER_MAX_SLEEP_SEC=3;config.ENABLE_GET_MEDIA=False;config.ENABLE_GET_COMMENTS=False;config.CRAWLER_TYPE='creator';config.DY_CREATOR_ID_LIST=['https://www.douyin.com/user/MS4wLjABAAAALIHRWrJxwmo4LaeEqAPHHfrBlL_lexxrdc83OeXvSuysOixUI_5ys_rm2RCBgFX6']
from media_platform.douyin.core import DouYinCrawler
async def run():
 crawler=DouYinCrawler()
 try:await asyncio.wait_for(crawler.start(),timeout=150)
 except Exception as e:print('COLLECTION_STOP',type(e).__name__,str(e)[:200],flush=True)
 finally:
  try:await crawler.close()
  except Exception:pass
asyncio.run(run())
