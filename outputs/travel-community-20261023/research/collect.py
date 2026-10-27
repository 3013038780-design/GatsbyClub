from pathlib import Path
import requests,concurrent.futures,json,hashlib,datetime
from bs4 import BeautifulSoup
B=Path(__file__).resolve().parent
urls=['https://www.32hike.com/aboutus.html','https://www.hike32.com/','https://home.54traveler.com/','https://www.youxiake.com/','https://www.ruailove.com/party/89.html','https://www.ruailove.com/party/','https://www.ruailove.com/about/1.html','https://www.zuanshi.com/new/loveCustomization','https://www.zuanshi.com/webContent/question','https://www.zuanshi.com/webActivity/newActivityList','https://www.liangyuan.com/','https://www.jfh999.com/party/311.html','https://meetknow.com/activities/beijing','https://www.xsms-club.com/','https://www.sohu.com/a/1055933312_121626427','https://jinrishangye.com/8357/','https://www.modernist.club/','https://members.thesupperclubinc.com/membership','https://thesupperclubinc.com/terms-of-services','https://parlor.social/Parlor%20Membership.pdf','https://www.mandala.club/','https://www.mandala.club/enquire','https://www.67pallmall.com/the-singapore-club/membership/','https://www.67pallmall.com/67-trips/','https://legacy.thebatterysf.com/societies','https://thebatterysf.com/events','https://www.carlyleandco.com/','https://estellecommunity.com/','https://www.theartsclub.co.uk/membership/','https://theartsclub.co.uk/arts-culture/']
def get(url):
 k=hashlib.sha256(url.encode()).hexdigest()[:12]
 try:
  r=requests.get(url,timeout=25,headers={'User-Agent':'Mozilla/5.0'});r.encoding=r.apparent_encoding if 'charset' not in r.headers.get('content-type','') else r.encoding
  ext='pdf' if 'pdf' in r.headers.get('content-type','') else 'html';(B/(k+'.'+ext)).write_bytes(r.content)
  s=BeautifulSoup(r.text,'html.parser') if ext=='html' else None
  if s:
   for t in s(['script','style','nav','footer']):t.decompose()
   (B/(k+'.txt')).write_text(s.get_text('\n',strip=True))
  return {'url':url,'status':r.status_code,'final_url':r.url,'collected':'2026-10-23','file':k+'.'+ext,'bytes':len(r.content),'title':s.title.get_text() if s and s.title else ''}
 except Exception as e:return {'url':url,'error':str(e),'collected':'2026-10-23'}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:rows=list(pool.map(get,urls))
(B/'网页核查.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print(json.dumps([{k:r.get(k) for k in ['url','status','bytes','error']} for r in rows],ensure_ascii=False))
