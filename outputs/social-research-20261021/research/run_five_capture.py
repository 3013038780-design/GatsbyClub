"""Run an isolated MediaCrawler job for the community research project."""
import argparse, asyncio, base64, io, json, os, runpy, sys
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

WORKSPACE=Path(__file__).resolve().parents[3]
REPO=WORKSPACE/'tools/MediaCrawler'
OUTPUT=WORKSPACE/'outputs/five-offline-matchmaking-20261022/social-platforms'
AUTH=WORKSPACE/'.research-private'

parser=argparse.ArgumentParser()
parser.add_argument('--platform',choices=['xhs','dy','bili'],required=True)
parser.add_argument('--keywords',default='京城俱乐部')
parser.add_argument('--limit',type=int,default=20)
parser.add_argument('--help-upstream',action='store_true')
parser.add_argument('--batch',action='store_true')
parser.add_argument('--creator-sample',action='store_true')
parser.add_argument('--discover',action='store_true')
parser.add_argument('--profile-probe',action='store_true')
args=parser.parse_args()
if not 1<=args.limit<=30:parser.error('单次试采数量须为1到30')
OUTPUT.mkdir(exist_ok=True);AUTH.mkdir(mode=0o700,exist_ok=True)
AUTH.chmod(0o700)
os.chdir(REPO);sys.path.insert(0,str(REPO))
node=Path('/Users/olivialee/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin')
os.environ['PATH']=str(node)+os.pathsep+os.environ.get('PATH','')
import config
config.PLATFORM=args.platform
config.KEYWORDS=args.keywords
config.ENABLE_CDP_MODE=False
config.CDP_CONNECT_EXISTING=False
config.HEADLESS=False
config.SAVE_LOGIN_STATE=True
config.USER_DATA_DIR='community_research_%s'
config.ENABLE_IP_PROXY=False
config.DISABLE_SSL_VERIFY=False
config.SAVE_DATA_OPTION='jsonl'
config.SAVE_DATA_PATH=str(OUTPUT)
config.CRAWLER_MAX_NOTES_COUNT=args.limit
config.MAX_CONCURRENCY_NUM=1
config.CRAWLER_MAX_SLEEP_SEC=5
config.ENABLE_GET_MEDIA=False
config.ENABLE_GET_COMMENTS=False
config.CRAWLER_MAX_COMMENTS_COUNT_SINGLENOTES=10
config.ENABLE_GET_SUB_COMMENTS=False
config.ENABLE_GET_WORDCLOUD=False
config.XHS_SPECIFIED_NOTE_URL_LIST=[]
config.XHS_CREATOR_ID_LIST=[]
config.DY_SPECIFIED_ID_LIST=[]
config.DY_CREATOR_ID_LIST=[]
config.BILI_SPECIFIED_ID_LIST=[]
config.BILI_CREATOR_ID_LIST=[]
config.CREATOR_MODE=False
config.START_DAY='2026-07-25'
config.END_DAY='2026-10-22'

if args.help_upstream:
 sys.argv=['main.py','--help'];runpy.run_path(str(REPO/'main.py'),run_name='__main__');sys.exit(0)

# User confirmed possession of the author's written commercial authorization in chat.
manifest=dict(platform=args.platform,keywords=args.keywords,limit=args.limit,
 collected_at=datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(),
 commercial_authorization='User confirmed existing written authorization in this conversation',
 official_account_verification='Required before inclusion in core brand sample',
 browser='isolated project profile; user authorized local login persistence',
 comments='No comment bodies collected; visible interaction counters only')
(OUTPUT/f'job-{args.platform}.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(OUTPUT/f"job-{args.platform}-{datetime.now(ZoneInfo('Asia/Shanghai')).strftime('%H%M%S')}.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
from tools import utils
from PIL import Image
# The public homepage keeps background resources open; DOM readiness is sufficient.
# Preserve platform challenges for manual completion by the user.
from playwright.async_api import Page, BrowserContext
_goto = Page.goto
async def project_goto(self, url, **kwargs):
 kwargs.setdefault('wait_until', 'domcontentloaded')
 kwargs.setdefault('timeout', 45000)
 return await _goto(self, url, **kwargs)
Page.goto = project_goto
_init_script = BrowserContext.add_init_script
async def project_init_script(self, script=None, *, path=None):
 if path and str(path).endswith('stealth.min.js'):
  return
 return await _init_script(self, script=script, path=path)
BrowserContext.add_init_script = project_init_script
def save_qrcode(image_data):
 if isinstance(image_data,str):
  if ',' in image_data:image_data=image_data.split(',',1)[1]
  raw=base64.b64decode(image_data)
 else:raw=image_data
 image=Image.open(io.BytesIO(raw)).convert('RGB')
 path=AUTH/f'login-{args.platform}.png';image.save(path);path.chmod(0o600)
 print(f'LOGIN_QRCODE_READY platform={args.platform} path={path}',flush=True)
utils.show_qrcode=save_qrcode
if args.batch and args.platform=='xhs':
 from community_xhs_batch import install_batch
 install_batch(OUTPUT,args.keywords.split(','),args.limit)
if args.creator_sample and args.platform=='xhs':
 from five_creator_sample import install
 install(OUTPUT,args.limit)
if args.discover and args.platform=='xhs':
 from community_discovery import install_discovery
 install_discovery(OUTPUT,args.keywords.split(','),args.limit)
if args.profile_probe and args.platform=='xhs':
 from community_discovery import install_profile_probe
 install_profile_probe(OUTPUT)
sys.argv=['main.py','--platform',args.platform,'--lt','qrcode','--type','search','--keywords',args.keywords,'--save_data_option','jsonl']
runpy.run_path(str(REPO/'main.py'),run_name='__main__')
