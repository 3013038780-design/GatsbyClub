from pathlib import Path
from urllib.request import Request,urlopen
from concurrent.futures import ThreadPoolExecutor
from PIL import Image,ImageOps,ImageDraw
from io import BytesIO
import json,shutil
ROOT=Path(__file__).parent;A=ROOT/'dist/assets';v=json.load(open(ROOT/'image_candidates.json'))
items={
'mandala':('https://static.wixstatic.com/media/70c7f9_7d6ea104c985449596da5b8c3e994911~mv2.jpg','https://www.mandala.club/','Mandala Club 官网空间照'),
'modernist':(v['modernist']['images'][1][0],v['modernist']['page'],'Modernist 官方图库活动照'),
'parlor':(v['parlor']['og'][0],v['parlor']['page'],'Parlor 官网分享图'),
'battery':(v['battery']['og'][0],v['battery']['page'],'The Battery 官网分享图'),
'carlyle':('https://api.carlyleandco.com/media/ylep0l5i/1-home-page-about-us_low3.jpg',v['carlyle']['page'],'Carlyle & Co 官网图片'),
'estelle':(v['estelle']['og'][0],v['estelle']['page'],'Estelle Community 官网图片'),
'arts':(v['arts']['images'][5][0],v['arts']['page'],'The Arts Club 官网一层空间照'),
'offline':(v['offline']['images'][29][0],v['offline']['page'],'The Offline Club 法国旅行官网图片'),
'secret':(v['secret']['images'][5][0],v['secret']['page'],'Secret Cinema 官网 Bridgerton 图片'),
'crystal':(v['crystal']['og'][0],v['crystal']['page'],'The Crystal Maze Live 官网图片'),
'gamechanger':(v['gamechanger']['images'][1][0],v['gamechanger']['page'],'Game Changer 官方节目缩略图 Last Talent Standing'),
'jetlag':(v['jetlag']['og'][0],v['jetlag']['page'],'Jet Lag 第三季 Nebula 官方分享图'),
'amazing':(v['amazing']['og'][0],v['amazing']['page'],'The Amazing Race CBS 官网分享图'),
'devilsplan':('https://images.ctfassets.net/4cd45et68cgf/YZtrXZMbcSKvAu3qg1oT9/65785e88520431b68300bf5115472789/The_Devil-s_Plan_Death_Room.jpg','https://about.netflix.com/news/the-devils-plan-death-room-trailer','The Devil’s Plan 第二季 Netflix 官方海报'),
'fortune':('https://www.itv.com/presscentre/system/files/styles/half_width/private/2025-07/04_desktopctv_railtilelandscape_withlogo_1920x1080_artloader.jpg?itok=c2wDYE_K','https://www.itv.com/presscentre/media-packs/fortune-hotel-s2-press-pack','The Fortune Hotel 第二季 ITV 官方宣传图'),
'mandala-dining':(v['mandala']['images'][12][0].split('/v1/')[0],v['mandala']['page'],'Mandala Club Members Bar 官网空间照'),
'mandala-pitch':(v['mandala']['images'][29][0].split('/v1/')[0],v['mandala']['page'],'Mandala Club Proudly Pitch a Friend 官方活动图'),
}
def get(item):
 k,(url,page,caption)=item
 try:
  raw=urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=25).read();im=ImageOps.exif_transpose(Image.open(BytesIO(raw))).convert('RGB');im.thumbnail((1800,1500));im.save(A/f'{k}.jpg',quality=88,optimize=True)
  return k,dict(file=f'assets/{k}.jpg',url=url,page=page,caption=caption,size=im.size)
 except Exception as e:return k,dict(error=str(e),url=url,page=page,caption=caption)
with ThreadPoolExecutor(max_workers=8) as ex:r=dict(ex.map(get,items.items()))
(A/'image-credits.json').write_text(json.dumps(r,ensure_ascii=False,indent=2))
thumb=Image.new('RGB',(1000,((len(r)+3)//4)*190),'#f4efdf');d=ImageDraw.Draw(thumb)
for i,(k,x) in enumerate(r.items()):
 if 'file' in x:
  im=Image.open(ROOT/'dist'/x['file']);im.thumbnail((244,150));thumb.paste(im,((i%4)*250,(i//4)*190))
 d.text(((i%4)*250+3,(i//4)*190+155),k,fill='black')
thumb.save(ROOT/'image-review.jpg')
for k,x in r.items():print(k,x.get('size',x.get('error')))
