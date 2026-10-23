"""Keep the isolated research login windows open for user-operated sign-in."""
import asyncio,json,sys
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[3]
PRIVATE=ROOT/'.research-private'
async def main():
 platform=sys.argv[1]
 profile=ROOT/'tools/MediaCrawler/browser_data'/('community_research_'+platform)
 profile.mkdir(parents=True,exist_ok=True);profile.chmod(0o700)
 async with async_playwright() as p:
  opts=dict(user_data_dir=str(profile),headless=False,viewport={'width':1280,'height':900})
  if platform=='bili':opts['channel']='chrome'
  ctx=await p.chromium.launch_persistent_context(**opts)
  page=await ctx.new_page()
  url={'dy':'https://www.douyin.com/','bili':'https://passport.bilibili.com/login','xhs':'https://www.xiaohongshu.com/explore'}[platform]
  try:await page.goto(url,wait_until='commit',timeout=45000)
  except Exception as e:print('NAVIGATION_STATUS '+type(e).__name__,flush=True)
  print('LOGIN_WINDOW_OPEN '+platform,flush=True)
  if platform=='dy':
   try:await page.get_by_role('button',name='登录',exact=True).click(timeout=20000)
   except Exception:pass
  for tick in range(180):
   if tick in [1,3,6]:
    try:
     shot=PRIVATE/('signin-window-'+platform+'.png')
     await page.screenshot(path=str(shot));shot.chmod(0o600)
     print('LOGIN_SCREENSHOT_READY '+platform,flush=True)
    except Exception:pass
   try:
    cookies={c['name']:c['value'] for c in await ctx.cookies()}
    signed=(cookies.get('LOGIN_STATUS')=='1') if platform=='dy' else bool(cookies.get('SESSDATA')) if platform=='bili' else False
    if signed:
     (PRIVATE/('signin-'+platform+'.json')).write_text(json.dumps({'platform':platform,'session_saved':True,'api_validation':'pending','time':datetime.now().isoformat()}))
     print('LOGIN_SESSION_SAVED '+platform,flush=True)
     await asyncio.sleep(3);await ctx.close();return
   except Exception:break
   await asyncio.sleep(5)
  await ctx.close()
asyncio.run(main())
