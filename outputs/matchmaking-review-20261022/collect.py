import requests,hashlib,json,time,re
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime
from zoneinfo import ZoneInfo
O=Path(__file__).resolve().parent;R=O/'raw';R.mkdir(exist_ok=True)
urls=[
('我主良缘','https://www.7799520.com/'),('我主良缘','https://www.liangyuan.com/'),('我主良缘','https://www.7799520.com/about.html'),('我主良缘','https://m.7799520.com/news/32674.html'),('我主良缘','https://www.7799520.com/party'),('我主良缘','https://www.7799520.com/zt/1811/merchants/'),
('金凤凰','https://www.jfh999.com/about/1.html'),('金凤凰','https://www.jfh999.com/about/20.html'),('金凤凰','https://www.jfh999.com/about/24.html'),('金凤凰','https://www.jfh999.com/about/8.html'),('金凤凰','https://www.jfh999.com/about/22.html'),('金凤凰','https://www.jfh999.com/about/19.html'),('金凤凰','https://www.jfh999.com/party/'),('金凤凰','https://www.jfh999.com/party/311.html'),('金凤凰','https://www.jfh999.com/party/302.html'),
('珍爱网','https://www.zhenai.com/'),('珍爱网','https://www.zhenai.com/n/directStore'),('珍爱网','https://i.zhenai.com/m/client/intro/agree.html'),('珍爱网','https://www.nbd.com.cn/articles/2025-03-25/3804555.html'),('珍爱网','https://www.samr.gov.cn/xw/zj/art/2024/art_035b6505eb7b46b5a49d06a4d8dd61c5.html'),
('金凤凰','https://travel.sznews.com/content/2019-06/24/content_22200827.htm'),('珍爱网','https://www.prnasia.com/story/48739-1.shtml'),('我主良缘','https://dzb.hxnews.com/2013-09/18/content_134472.htm'),('我主良缘','https://www.kankanews.com/detail/PlQazoPPVwv')]
rows=[]
for name,u in urls:
 key=hashlib.sha256(u.encode()).hexdigest()[:12]
 try:
  r=requests.get(u,timeout=20);r.encoding=r.apparent_encoding if 'charset' not in r.headers.get('content-type','') else r.encoding
  soup=BeautifulSoup(r.text,'html.parser')
  for el in soup(['script','style','noscript']):el.decompose()
  # These public institutional pages are retained for verification; personal member details are not extracted as research records.
  text=soup.get_text('\n',strip=True)
  (R/(key+'.html')).write_text(r.text);(R/(key+'.txt')).write_text(text)
  rows.append(dict(brand=name,url=u,final_url=r.url,status=r.status_code,title=soup.title.get_text() if soup.title else '',chars=len(text),file=key,collected_at=datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(timespec='seconds')))
  print(name,r.status_code,len(text),u,flush=True)
 except Exception as e:rows.append(dict(brand=name,url=u,status='error',error=str(e)))
 (O/'collection.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
 time.sleep(1)
