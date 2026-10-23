import json,re,hashlib,requests
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin
B=Path(__file__).parent
dest=B/'posters';dest.mkdir(exist_ok=True)
rows=[]
for r in json.loads((B/'网页采集记录.json').read_text()):
 if 'newActivityDetail' not in r['url'] and '/party/311' not in r['url']:continue
 for image in BeautifulSoup((B/'raw'/r['file'].replace('.md','.html')).read_text(),'html.parser').find_all('img'):
  u=urljoin(r['url'],image.get('src',''))
  if not re.search(r'/2026\d{4}/',u):continue
  key=hashlib.sha256(u.encode()).hexdigest()[:12];p=dest/(key+'.jpg')
  try:
   response=requests.get(u,timeout=20);response.raise_for_status();p.write_bytes(response.content)
   rows.append(dict(brand=r['brand'],page=r['url'],image_url=u,file=str(p),status='downloaded for reading activity poster'))
   print(key,len(response.content),flush=True)
  except Exception as e:rows.append(dict(page=r['url'],image_url=u,error=type(e).__name__))
(dest/'来源.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
