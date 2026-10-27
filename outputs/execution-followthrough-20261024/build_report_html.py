from pathlib import Path
from lxml import etree as E
import json,zipfile,base64,html,hashlib,re
B=Path(__file__).parent;R=B.parents[1];Q=R/'outputs/integrated-research-20261024';O=B/'site/dist';O.mkdir(parents=True,exist_ok=True)
qa=json.loads((Q/'qa/交付核验.json').read_text());assert qa['pdf_internal_targets_verified']==16 and qa['report_pages']==50
path=Q/'交付文件/高端线下社群市场调研与对标报告.docx'
z=zipfile.ZipFile(path);ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships','a':'http://schemas.openxmlformats.org/drawingml/2006/main'};W='{'+ns['w']+'}';rels={x.get('Id'):x.get('Target')for x in E.fromstring(z.read('word/_rels/document.xml.rels'))}
root=E.fromstring(z.read('word/document.xml'));toc=[];blocks=[];skip=False;heading_count=0;image_count=0;table_count=0;body_paragraphs=[]
def esc(s):return html.escape(s or'',quote=True)
def inline(el):
 out=[]
 for c in el:
  local=E.QName(c).localname
  if local=='r':
   texts=[]
   for x in c:
    name=E.QName(x).localname
    if name=='t':texts.append(esc(x.text))
    elif name=='br':texts.append('<br>')
    elif name=='tab':texts.append(' ')
    elif name=='drawing':
     global image_count
     for a in x.findall('.//a:blip',ns):
      rid=a.get('{'+ns['r']+'}embed');target=rels.get(rid,'');data=z.read('word/'+target);mime='image/png'if target.endswith('.png')else'image/jpeg';image_count+=1;texts.append('<img class="figure" alt="报告图表" src="data:'+mime+';base64,'+base64.b64encode(data).decode()+'">')
   s=''.join(texts)
   bold=c.find('w:rPr/w:b',ns)
   if bold is not None and bold.get(W+'val','1') not in ['0','false','off']:s='<strong>'+s+'</strong>'
   out.append(s)
  elif local=='hyperlink':
   target=rels.get(c.get('{'+ns['r']+'}id'),'');anchor=c.get(W+'anchor');s=inline(c)
   if anchor:out.append('<a href="#'+esc(anchor)+'">'+s+'</a>')
   elif target:out.append('<a href="'+esc(target)+'" target="_blank" rel="noopener noreferrer">'+s+'</a>')
   else:out.append(s)
 return ''.join(out)
for el in root.find('w:body',ns):
 typ=E.QName(el).localname
 if typ=='p':
  text=''.join(el.itertext());style=el.find('w:pPr/w:pStyle',ns);style=style.get(W+'val','')if style is not None else''
  if text=='阅读目录':skip=True;continue
  if skip:
   links=el.findall('w:hyperlink',ns)
   if links and any(x.get(W+'anchor')for x in links):
    for x in links:toc.append((x.get(W+'anchor'),''.join(x.itertext())))
    continue
   skip=False
  s=inline(el)
  if not s:continue
  body_paragraphs.append(text)
  bookmark=el.find('w:bookmarkStart',ns);anchor=bookmark.get(W+'name')if bookmark is not None else None
  if style.startswith('Heading'):
   heading_count+=1;level=int(style[-1])+1;anchor=anchor or 'heading-'+str(heading_count);blocks.append(f'<h{level} id="{esc(anchor)}">{s}</h{level}>')
  elif style=='Title':blocks.append('<h1 id="report-content">'+s+'</h1>')
  else:
   sizes=el.findall('.//w:rPr/w:sz',ns);small=bool(sizes)and all(int(x.get(W+'val','24'))<=18 for x in sizes);blocks.append('<p'+(' class="citation"'if small else'')+'>'+s+'</p>')
 elif typ=='tbl':
  table_count+=1;rows=[]
  for i,row in enumerate(el.findall('w:tr',ns)):
   cells=[]
   for cell in row.findall('w:tc',ns):
    tag='th'if i==0 else'td';cells.append('<'+tag+'>'+''.join('<p>'+inline(p)+'</p>'for p in cell.findall('w:p',ns))+'</'+tag+'>')
   rows.append('<tr>'+''.join(cells)+'</tr>')
  blocks.append('<div class="table-scroll"><table>'+''.join(rows)+'</table></div>')
css='''*{box-sizing:border-box}html{scroll-behavior:auto;scroll-padding-top:var(--header-offset,90px)}body{margin:0;background:#f4f6f7;color:#202d35;font-family:"PingFang SC","Microsoft Yahei",sans-serif;font-size:16px;line-height:1.85}a{color:#245e7a;text-underline-offset:3px}a:hover{color:#123e53}header{position:sticky;top:0;z-index:5;background:#ffffffed;border-bottom:1px solid #d7dfe4;padding:12px 24px;display:flex;align-items:center;gap:15px;flex-wrap:wrap;backdrop-filter:blur(12px)}header strong{font-size:17px}header .tools{display:flex;gap:8px;align-items:center;margin-left:auto}input,button{font:inherit;border:1px solid #bacbd5;border-radius:5px;padding:6px 10px;background:#fff;color:#203e50}input{width:190px}button{cursor:pointer}button:focus-visible,a:focus-visible,input:focus-visible{outline:3px solid #d59b3a;outline-offset:3px}.layout{display:grid;grid-template-columns:245px minmax(0,980px);max-width:1300px;margin:26px auto;gap:24px;padding:0 20px}aside{position:sticky;top:100px;align-self:start;max-height:calc(100vh - 120px);overflow:auto;font-size:14px;line-height:1.6;padding:16px;background:#fff;border:1px solid #dde4e8;border-radius:8px}aside a{display:block;padding:6px 2px;text-decoration:none}aside .part{font-weight:700;margin-top:8px}article{min-width:0;background:white;border:1px solid #dde4e8;box-shadow:0 4px 22px #1c34480a;padding:44px 48px;border-radius:8px}h1{font-family:"Songti SC","Noto Serif CJK SC",serif;font-size:34px;line-height:1.4;margin:0 0 24px}h2{font-size:26px;border-bottom:2px solid #c8d7df;padding-bottom:10px;margin:50px 0 20px}h3{font-size:22px;line-height:1.6;margin:36px 0 16px;color:#183d50}h4{font-size:18px;line-height:1.7;margin:26px 0 12px}p{margin:12px 0 18px}p.citation{font-size:13px;line-height:1.75;color:#5c6d77}.figure{display:block;width:100%;height:auto;margin:20px auto}.table-scroll{overflow:auto;margin:20px 0 26px}table{border-collapse:collapse;width:100%;font-size:14px;line-height:1.75}td,th{border:1px solid #cbd6dc;padding:12px 13px;vertical-align:top;min-width:100px}th{background:#e8eff3;text-align:left}td p,th p{margin:0 0 5px}.download{display:flex;gap:10px;flex-wrap:wrap;padding:18px 0;border-bottom:1px solid #d9e2e8;margin-bottom:26px}.download a{padding:7px 12px;background:#f0f5f7;border-radius:5px;text-decoration:none;font-size:14px}.muted{color:#65747d;font-size:13px}mark{background:#ffe49a;border-radius:2px}mark.current{background:#e5ac42;color:#102c3d}#menu{display:none}#searchCount{font-size:12px;min-width:44px}footer{border-top:1px solid #d7dfe4;padding-top:24px;margin-top:48px;font-size:13px;color:#65747d}@media(max-width:900px){.layout{display:block;padding:0 12px;margin:14px auto}aside{display:none;position:relative;top:0;max-height:none;margin-bottom:16px}body.menu-open aside{display:block}article{padding:28px 22px}header{padding:10px 12px}header .tools{margin-left:0;width:100%;flex-wrap:wrap;gap:6px}header .tools input{flex:1;min-width:90px;width:110px}header button{font-size:14px;padding:6px 8px}#menu{display:inline-block}h1{font-size:28px}h2{font-size:24px}input{width:150px}table{min-width:650px}}@media print{header,aside,.download{display:none}.layout{display:block;margin:0;padding:0}article{border:0;padding:0;box-shadow:none}body{background:white;font-size:11pt}h2,h3,h4{break-after:avoid}tr,img{break-inside:avoid}a{color:inherit;text-decoration:none}.table-scroll{overflow:visible}table{font-size:9pt}mark{background:none}}'''
js='''history.scrollRestoration='manual';window.scrollTo(0,0);const header=document.querySelector('header');new ResizeObserver(()=>document.documentElement.style.setProperty('--header-offset',(header.offsetHeight+16)+'px')).observe(header);const article=document.querySelector('article');const input=document.querySelector('#search');let marks=[],index=-1;function clear(){article.querySelectorAll('mark').forEach(m=>m.replaceWith(document.createTextNode(m.textContent)));article.normalize();marks=[];index=-1;}function go(delta){if(!marks.length)return;index=(index+delta+marks.length)%marks.length;marks.forEach(m=>m.classList.remove('current'));marks[index].classList.add('current');marks[index].scrollIntoView({block:'center',behavior:'auto'});document.querySelector('#searchCount').textContent=(index+1)+'/'+marks.length;}function search(){clear();const query=input.value.trim();if(!query){document.querySelector('#searchCount').textContent='';return;}const walker=document.createTreeWalker(article,NodeFilter.SHOW_TEXT);const nodes=[];while(walker.nextNode())nodes.push(walker.currentNode);nodes.forEach(node=>{const text=node.nodeValue;let pos=0,at;const fragment=document.createDocumentFragment();let found=false;while((at=text.toLocaleLowerCase().indexOf(query.toLocaleLowerCase(),pos))!==-1){found=true;fragment.append(document.createTextNode(text.slice(pos,at)));const mark=document.createElement('mark');mark.textContent=text.slice(at,at+query.length);fragment.append(mark);marks.push(mark);pos=at+query.length;}if(found){fragment.append(document.createTextNode(text.slice(pos)));node.replaceWith(fragment);}});document.querySelector('#searchCount').textContent=marks.length?'0/'+marks.length:'无结果';go(1);}let timer;input.addEventListener('input',()=>{clearTimeout(timer);timer=setTimeout(search,160)});input.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();go(e.shiftKey?-1:1)}});document.querySelector('#next').onclick=()=>go(1);document.querySelector('#prev').onclick=()=>go(-1);document.querySelector('#print').onclick=()=>window.print();document.querySelector('#menu').onclick=()=>document.body.classList.toggle('menu-open');document.querySelectorAll('aside a').forEach(a=>a.addEventListener('click',()=>document.body.classList.remove('menu-open')));'''
nav='<a class="part" href="#report-content">研究摘要与结论</a>'+''.join('<a'+(' class="part"'if '部分'in label else'')+' href="#'+esc(anchor)+'">'+esc(label)+'</a>'for anchor,label in toc)
download='<div class="download"><a href="research.pdf">正式PDF</a><a href="research.xlsx">总Excel</a><a href="launch.xlsx">收费与费用测算</a><a href="speech.pdf">口语讲稿PDF</a><a href="meeting.docx">可编辑讲稿</a></div>'
page='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>高端线下社群市场调研与对标报告</title><style>'+css+'</style></head><body><header><button id="menu" aria-label="展开目录">目录</button><strong>高端线下社群调研</strong><div class="tools"><label for="search">查找</label><input id="search" placeholder="机构、价格或关键词"><span id="searchCount" aria-live="polite"></span><button id="prev" aria-label="上一个结果">上一个</button><button id="next" aria-label="下一个结果">下一个</button><button id="print">打印</button></div></header><div class="layout"><aside aria-label="报告目录">'+nav+'</aside><article>'+download+''.join(blocks)+'<footer>资料截至2026年10月24日。市场调研与对标分两部分；研究判断、品牌自述与测算假设在相应段落说明。</footer></article></div><script>'+js+'</script></body></html>'
(O/'高端线下社群市场调研与对标报告.html').write_text(page)
(O/'research.html').write_text(page)
(B/'qa/HTML内容核验.json').write_text(json.dumps(dict(source_docx_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),source_pdf_sha256=hashlib.sha256((Q/'交付文件/高端线下社群市场调研与对标报告.pdf').read_bytes()).hexdigest(),headings=heading_count,tables=table_count,images=image_count,toc=len(toc),body_paragraphs=len(body_paragraphs),external_urls=list(dict.fromkeys(rels.values())),stage='已从核验后的Word正文转换；待浏览器验收'),ensure_ascii=False,indent=2))
assert len(toc)==16 and image_count==4
print('HTML generated:',len(page),'characters,',table_count,'tables,',image_count,'figures')
