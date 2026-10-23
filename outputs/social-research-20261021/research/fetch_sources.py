from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request,json,re,html
from detail import ROOT,sources

ids={'S02','S10','S13','S15','S16','S22','S23','S25','S28','S29','S30','S31','S33','S34','S35','S36','S38','S40','S41','S42','S43','S44','S67','S70'}
out=ROOT/'research/primary';out.mkdir(exist_ok=True)
def get(s):
    try:
        url=urllib.parse.quote(s['url'],safe=':/?=&%')
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/130.0.0.0 Safari/537.36'})
        r=urllib.request.urlopen(req,timeout=18); raw=r.read()
        if 'pdf' in r.headers.get('content-type','').lower() or raw[:4]==b'%PDF':
            (out/(s['id']+'.pdf')).write_bytes(raw)
            from pypdf import PdfReader
            txt='\n'.join(p.extract_text() or '' for p in PdfReader(out/(s['id']+'.pdf')).pages)
        else:
            txt=raw.decode('utf-8',errors='replace')
            txt=re.sub(r'<(script|style|noscript)\b[^>]*>.*?</\1>','',txt,flags=re.S|re.I)
            txt=html.unescape(re.sub(r'<[^>]+>',' ',txt))
            txt=re.sub(r'\s+',' ',txt)
        (out/(s['id']+'.txt')).write_text(txt)
        return dict(id=s['id'],status=r.status,url=r.url,chars=len(txt))
    except Exception as e:return dict(id=s['id'],error=str(e)[:160])
with ThreadPoolExecutor(max_workers=6) as ex: results=list(ex.map(get,[s for s in sources if s['id'] in ids]))
(out/'fetch_status.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
print(json.dumps(results,ensure_ascii=False))
