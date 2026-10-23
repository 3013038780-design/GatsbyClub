from pathlib import Path
from docx import Document
from docx.oxml.ns import qn
import json,html
ROOT=Path(__file__).parent;OLD=ROOT.parent/'club_research_20261019';doc=Document(OLD/'output/北京香港私享社交俱乐部研究与商业方案.docx')
pages=[];cur=None
for e in doc.element.body:
 if e.tag==qn('w:p'):
  text=''.join(e.itertext()) if False else ''.join(t.text or '' for t in e.iter(qn('w:t')))
  if not text.strip():continue
  pp=e.find(qn('w:pPr'));br=pp is not None and pp.find(qn('w:pageBreakBefore')) is not None
  st=pp.find(qn('w:pStyle')) if pp is not None else None;style=st.get(qn('w:val')) if st is not None else ''
  if cur is None or br:
   cur={'tag':text,'title':'','blocks':[]};pages.append(cur);continue
  if style in ['Title','Heading1'] and not cur['title']:cur['title']=text;continue
  links=[]
  for h in e.iter(qn('w:hyperlink')):
   rid=h.get(qn('r:id'))
   if rid in doc.part.rels:links.append(doc.part.rels[rid].target_ref)
  cur['blocks'].append({'type':'h' if style.startswith('Heading') else 'p','text':text,'links':links})
 elif e.tag==qn('w:tbl'):
  rows=[]
  for tr in e.findall(qn('w:tr')):
   rows.append([''.join(t.text or '' for t in tc.iter(qn('w:t'))) for tc in tr.findall(qn('w:tc'))])
  cur['blocks'].append({'type':'table','rows':rows})
sources=json.load(open(OLD/'source_register.json'))
(ROOT/'research_data.json').write_text(json.dumps({'pages':pages,'sources':sources},ensure_ascii=False))
print(len(pages),'chapters',len(sources),'sources')
