from pathlib import Path
import zipfile,re,json,collections,hashlib
from lxml import etree as E
from lxml import html as H
B=Path(__file__).parent;R=B.parents[1];Q=R/'outputs/integrated-research-20261024';docx=Q/'交付文件/高端线下社群市场调研与对标报告.docx';pdf=Q/'交付文件/高端线下社群市场调研与对标报告.pdf';W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
norm=lambda x:re.sub(r'\s+','',x or'')
with zipfile.ZipFile(docx) as z:
 root=E.fromstring(z.read('word/document.xml'));rels=E.fromstring(z.read('word/_rels/document.xml.rels'))
 expected=[]
 for p in root.find(W+'body').iter(W+'p'):
  text=''.join(p.itertext())
  if text=='阅读目录' or any(x.get(W+'anchor') for x in p.iter(W+'hyperlink')):continue
  if norm(text):expected.append(norm(text))
 external={x.get('Target')for x in rels if x.get('Type','').endswith('/hyperlink')}
soup=H.fromstring((B/'site/dist/research.html').read_text());actual=[norm(''.join(x.itertext()))for x in soup.xpath('//article//*[self::p or self::h1 or self::h2 or self::h3 or self::h4]')if norm(''.join(x.itertext()))];difference=collections.Counter(expected)-collections.Counter(actual);assert not difference,list(difference)[:3]
actual_urls={a.get('href')for a in soup.xpath('//article//a[@href]')};assert external<=actual_urls
q=json.loads((B/'qa/HTML内容核验.json').read_text());q.update(external_urls=sorted(external),docx_paragraphs_matched=len(expected),all_external_targets_preserved=True,source_docx_sha256=hashlib.sha256(docx.read_bytes()).hexdigest(),source_pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),stage='正文段落、37张表、4张图、目录和外链均已核对');(B/'qa/HTML内容核验.json').write_text(json.dumps(q,ensure_ascii=False,indent=2))
print('HTML body paragraphs matched:',len(expected),'external URL targets:',len(external))
