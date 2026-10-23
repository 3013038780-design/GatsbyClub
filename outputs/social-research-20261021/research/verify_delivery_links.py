from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime
import json,csv,requests,re
B=Path(__file__).resolve().parents[1]
links=json.loads((B/'research/pdf-links.json').read_text())
urls=list(dict.fromkeys(x['target'] for x in links if x['kind']=='网址'))
def check(u):
 try:
  with requests.get(u,timeout=(8,16),stream=True,allow_redirects=True,headers={'User-Agent':'Mozilla/5.0'}) as r:
   content=b''
   for chunk in r.iter_content(4096):
    content+=chunk
    if len(content)>65536:break
   text=content.decode(r.encoding or 'utf-8',errors='replace')
   title=re.search(r'<title[^>]*>(.*?)</title>',text,re.I|re.S)
   title=re.sub(r'\s+',' ',title.group(1)).strip() if title else ''
   status='HTTP可达' if r.status_code<400 else 'HTTP访问受限或异常'
   if 'xiaohongshu.com' in u:status+='；需浏览器登录核查正文'
   if any(t in title.lower() for t in ['captcha','access denied','verify','just a moment','验证','登录']):status+='；验证或登录页'
   return [u,r.status_code,r.url,title,status,'2026-10-21']
 except Exception as e:return [u,'','','','网络请求失败：'+type(e).__name__,'2026-10-21']
rows=[]
with ThreadPoolExecutor(max_workers=8) as ex:
 for f in as_completed([ex.submit(check,u) for u in urls]):rows.append(f.result())
rows.sort(key=lambda r:urls.index(r[0]))
o=B/'交付资料/数据明细/PDF资料链接检查.csv'
with o.open('w',encoding='utf-8-sig',newline='') as f:csv.writer(f).writerows([['PDF链接网址','HTTP状态','最终网址','页面标题','检查结果','检查日期']]+rows)
(B/'research/pdf-url-checks.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
print(json.dumps({'unique_urls':len(rows),'http_below_400':sum(isinstance(r[1],int) and r[1]<400 for r in rows),'other':[[r[0],r[1],r[4]] for r in rows if not isinstance(r[1],int) or r[1]>=400]},ensure_ascii=False))
