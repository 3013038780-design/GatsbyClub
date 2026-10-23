"""Run an isolated MediaCrawler job for the community research project."""
import argparse, asyncio, base64, io, json, os, runpy, sys
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

WORKSPACE=Path(__file__).resolve().parents[3]
REPO=WORKSPACE/'tools/MediaCrawler'
OUTPUT=Path(__file__).resolve().parents[1]/'social-platforms'
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
config.ENABLE_GET_COMMENTS=True
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
config.START_DAY='2026-07-23'
config.END_DAY='2026-10-21'

if args.help_upstream:
 sys.argv=['main.py','--help'];runpy.run_path(str(REPO/'main.py'),run_name='__main__');sys.exit(0)

# User confirmed possession of the author's written commercial authorization in chat.
manifest=dict(platform=args.platform,keywords=args.keywords,limit=args.limit,
 collected_at=datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(),
 commercial_authorization='User confirmed existing written authorization in this conversation',
 official_account_verification='Required before inclusion in core brand sample',
 browser='isolated project profile; user authorized local login persistence',
 comments='first-level, up to 10 per post; not a representative customer survey')
(OUTPUT/f'job-{args.platform}.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
from tools import utils
from PIL import Image
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
 from community_xhs_batch import install_creator_sample
 install_creator_sample(OUTPUT,args.limit)
if args.discover and args.platform=='xhs':
 from community_discovery import install_discovery
 install_discovery(OUTPUT,args.keywords.split(','),args.limit)
if args.profile_probe and args.platform=='xhs':
 from community_discovery import install_profile_probe
 install_profile_probe(OUTPUT)
sys.argv=['main.py','--platform',args.platform,'--lt','qrcode','--type','search','--keywords',args.keywords,'--save_data_option','jsonl']
runpy.run_path(str(REPO/'main.py'),run_name='__main__')
