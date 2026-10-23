from pathlib import Path
import json,base64,shutil
ROOT=Path(__file__).parent;D=ROOT/'dist';A=D/'assets'
old=ROOT.parent/'club_research_20261019'
credits=json.load(open(A/'image-credits.json'))
credits['estelle']['caption']='Estelle Community 官网旗下空间品牌插画'
credits['carlyle-space']['caption']='Carlyle & Co 官网灯饰插画 本站未采用'
(A/'image-credits.json').write_text(json.dumps(credits,ensure_ascii=False,indent=2))
# Images are archived under dist/assets; no private attachment directories are required.
research=json.load(open(ROOT/'research_data.json'))
# Embed every used image so the HTML is portable and works without a server.
assets={}
for p in A.glob('*.jpg'):
 if p.stem in ['jetlag','carlyle-space']:continue
 assets['assets/'+p.name]='data:image/jpeg;base64,'+base64.b64encode(p.read_bytes()).decode()
js=(ROOT/'app.js').read_text()
js=js.replace('src="assets/bol-${n}.jpg"','src="${EMBEDDED[\'assets/bol-\'+n+\'.jpg\']}"')
for c in credits.values():
 if c.get('file') in assets:c['file']=assets[c['file']]
data='const RESEARCH='+json.dumps(research,ensure_ascii=False)+';\nconst CREDITS='+json.dumps(credits,ensure_ascii=False)+';\nconst EMBEDDED='+json.dumps({k:v for k,v in assets.items() if 'bol-' in k})+';'
page=(ROOT/'template.html').read_text().replace('/* STYLES */',(ROOT/'styles.css').read_text()).replace('/* DATA */',data.replace('</','<\\/')).replace('/* APP */',js)
page=page.replace('data-library-page="4">打开原始案例比较','data-library-page="3">打开原始案例比较')
for k,v in assets.items():page=page.replace('src="'+k+'"','src="'+v+'"')
(D/'index.html').write_text(page)
out=ROOT.parent/'club_research_20261019/output/北京香港私享俱乐部商业计划交互版.html'
out.write_text(page)
if (ROOT/'.openai/hosting.json').exists():
 manifest=json.loads((ROOT/'.openai/hosting.json').read_text());manifest['static']={'directory':'dist'};(ROOT/'.openai/hosting.json').write_text(json.dumps(manifest,indent=2))
print('HTML generated',len(page.encode()),'bytes',len(assets),'embedded images')
