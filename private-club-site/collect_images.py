from urllib.request import Request,urlopen
from urllib.parse import urljoin
from html.parser import HTMLParser
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json
ROOT=Path(__file__).parent
PAGES={
'modernist':'https://www.modernist.club/gallery',
'supper':'https://thesupperclubinc.com/',
'parlor':'https://parlor.social/',
'mandala':'https://www.mandala.club/',
'pallmall':'https://www.67pallmall.com/the-singapore-club/',
'battery':'https://thebatterysf.com/',
'carlyle':'https://www.carlyleandco.com/',
'estelle':'https://estellecommunity.com/',
'arts':'https://theartsclub.co.uk/arts-culture/',
'offline':'https://www.theoffline-club.com/retreat-locations/5-day-retreat-in-france',
'secret':'https://www.secretcinema.com/about',
'crystal':'https://the-crystal-maze.com/london/the-experience/',
'taskmaster':'https://taskmaster.tv/shows',
'gamechanger':'https://watch.dropout.tv/game-changer-new',
'devilsplan':'https://about.netflix.com/en/news/the-devils-plan-death-room-trailer',
'culinary':'https://media.netflix.com/en/only-on-netflix/81728365',
'loveblind':'https://www.netflix.com/tudum/articles/love-is-blind-pods',
'jetlag':'https://nebula.tv/jetlag/season/3',
'amazing':'https://www.cbs.com/shows/amazing_race/about/',
}
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.og=[];self.img=[]
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='meta' and a.get('property',a.get('name')) in ['og:image','twitter:image']:self.og.append(a.get('content',''))
  if t=='img':
   u=a.get('src',a.get('data-src',''))
   if u and not u.startswith('data:'):self.img.append((u,a.get('alt','')))
def get(item):
 k,u=item
 try:
  s=urlopen(Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=25).read().decode('utf8','ignore');p=Parser();p.feed(s)
  return k,dict(page=u,og=[urljoin(u,x) for x in p.og],images=[(urljoin(u,x),a) for x,a in p.img[:35]])
 except Exception as e:return k,dict(page=u,error=str(e))
with ThreadPoolExecutor(max_workers=8) as ex:out=dict(ex.map(get,PAGES.items()))
(ROOT/'image_candidates.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
for k,v in out.items():print(k,json.dumps(v,ensure_ascii=False)[:1700])
