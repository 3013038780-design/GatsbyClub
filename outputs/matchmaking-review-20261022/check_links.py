from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import requests,json,csv
from findings import SOURCES,BASE
from urllib.parse import quote

def check(item):
 k,(title,u,scope,kind)=item
 try:
  r=requests.get(u,timeout=12,headers={'User-Agent':'Mozilla/5.0'});status=r.status_code
  return [k,title,u,status,r.url,'可连接' if status<400 else '受限或HTTP异常；源内容另以网页工具核对']
 except Exception as e:return [k,title,u,'连接失败','',type(e).__name__]
rows=list(ThreadPoolExecutor(4).map(check,SOURCES.items()))
with (BASE/'qa/新增来源链接检查.csv').open('w',encoding='utf-8-sig',newline='') as f:csv.writer(f).writerows([['编号','名称','原文网址','本次HTTP结果','最终网址','说明']]+rows)
(BASE/'qa/新增来源链接检查.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print('checked',len(rows),'HTTP<400',sum(isinstance(r[3],int) and r[3]<400 for r in rows))
