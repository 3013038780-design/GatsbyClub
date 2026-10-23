from pathlib import Path
from copy import deepcopy
from collections import Counter
import json,re
from docx import Document
from docx.shared import Pt,Cm,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH,WD_BREAK,WD_TAB_ALIGNMENT,WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT,WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
B=Path(__file__).resolve().parent;src=B/'原版备份/中国高端线下社群市场研究报告.docx';out=B.parent/'交付文件/中国高端线下社群市场研究报告.docx'
d=Document(src)
def stfont(s,cn,size,bold=False,color='000000'):
 s.font.name='Arial';s.font.size=Pt(size);s.font.bold=bold;s.font.italic=False;s.font.color.rgb=RGBColor.from_string(color)
 rf=s.element.get_or_add_rPr().get_or_add_rFonts();rf.set(qn('w:eastAsia'),cn);rf.set(qn('w:ascii'),'Arial');rf.set(qn('w:hAnsi'),'Arial')
 for x in ['asciiTheme','hAnsiTheme','eastAsiaTheme','cstheme']:rf.attrib.pop(qn('w:'+x),None)
def fontxml(r,cn,size,bold=False,color='000000'):
 pr=r.find(qn('w:rPr'))
 if pr is None:pr=OxmlElement('w:rPr');r.insert(0,pr)
 for name in ['rFonts','sz','szCs','b','bCs','color','i','iCs','spacing','position','kern','u','caps','smallCaps']:
  for x in list(pr.findall(qn('w:'+name))):pr.remove(x)
 rf=OxmlElement('w:rFonts');rf.set(qn('w:ascii'),'Arial');rf.set(qn('w:hAnsi'),'Arial');rf.set(qn('w:eastAsia'),cn);pr.append(rf)
 for name,val in [('sz',str(int(size*2))),('szCs',str(int(size*2))),('b','1' if bold else '0'),('color',color)]:
  x=OxmlElement('w:'+name);x.set(qn('w:val'),val);pr.append(x)
def pformat(p,size=11,line=18.5,after=6,before=0):
 f=p.paragraph_format;f.line_spacing=Pt(line);f.space_before=Pt(before);f.space_after=Pt(after);f.left_indent=Cm(0);f.right_indent=Cm(0);f.first_line_indent=Cm(0);f.keep_together=False;f.keep_with_next=False;f.widow_control=True
 for x in p._p.xpath('./w:pPr/w:pBdr | ./w:pPr/w:shd'):x.getparent().remove(x)
 f.page_break_before=False
for sec in d.sections:
 sec.page_width=Cm(21);sec.page_height=Cm(29.7);sec.top_margin=Cm(2.1);sec.bottom_margin=Cm(2);sec.left_margin=Cm(2.2);sec.right_margin=Cm(2.2);sec.header_distance=Cm(.9);sec.footer_distance=Cm(.9)
for name,cn,size,bold in [('Normal','Songti SC',11,False),('Title','Heiti SC',24,True),('Subtitle','Heiti SC',13,False),('Heading 1','Heiti SC',17,True),('Heading 2','Heiti SC',14,True),('Heading 3','Heiti SC',11.5,True)]:
 stfont(d.styles[name],cn,size,bold);d.styles[name].paragraph_format.line_spacing=Pt(18.5)
for name,cn,size,color in [('Research Source','Songti SC',9.5,'555555'),('Research Table','Songti SC',10,'000000'),('Research TOC','Songti SC',11,'000000')]:
 if name not in d.styles:d.styles.add_style(name,WD_STYLE_TYPE.PARAGRAPH)
 stfont(d.styles[name],cn,size,False,color)
# One numbering convention for all chapter and institution headings.
renames={'重点对标对象的选择依据':'3.2 重点对标对象的选择依据','钻石婚恋及钻石精英会':'4.1 钻石婚恋及钻石精英会','大超说媒':'4.2 大超说媒','陌上花开HIMMR的线下业务':'4.3 陌上花开 HIMMR 线下业务','我主良缘':'4.4 我主良缘','金凤凰深港婚恋':'4.5 金凤凰深港婚恋','收入和工作量怎样同时算':'7.2 收入与交付工作量测算','试点要记录的绩效':'7.3 试点绩效指标','资料入口':'附录二 资料入口','附录 研究方法与待补证据':'附录一 研究方法与待补证据'}
for p in d.paragraphs:
 if p.style.name.startswith('Heading') and p.text in renames:p.text=renames[p.text]
# Preserve every research paragraph and external hyperlink while normalizing all runs.
bibliography=False; headings=[]; toc=[]
for p in list(d.paragraphs):
 text=p.text.strip();style=p.style.name
 if not text and not p._p.xpath('.//w:drawing'):
  p._p.getparent().remove(p._p);continue
 pformat(p)
 if style=='Title':
  p.paragraph_format.space_before=Pt(34);p.paragraph_format.space_after=Pt(16)
  cn,size,bold='Heiti SC',24,True
 elif style=='Subtitle':
  p.paragraph_format.space_after=Pt(18);cn,size,bold='Heiti SC',13,False
 elif style.startswith('Heading'):
  lev=int(style[-1]);cn,size,bold='Heiti SC',{1:17,2:14,3:11.5}[lev],True
  p.paragraph_format.space_before=Pt({1:18,2:13,3:10}[lev]);p.paragraph_format.space_after=Pt({1:10,2:7,3:5}[lev]);p.paragraph_format.line_spacing=Pt({1:24,2:21,3:18}[lev]);p.paragraph_format.keep_with_next=True;p.paragraph_format.keep_together=True
  # Chapter starts are explicit; company cases remain continuous within the chapter.
  if lev==1:p.paragraph_format.page_break_before=(text=='一 合伙人决策摘要')
  headings.append(p)
  if text=='附录二 资料入口':bibliography=True
 else:
  is_source=bibliography or text.startswith(('资料：','依据 ','打开资料'))
  cn,size,bold='Songti SC',9.5 if is_source else 11,False
  if is_source:
   p.style=d.styles['Research Source'];p.paragraph_format.line_spacing=Pt(14);p.paragraph_format.space_before=Pt(0);p.paragraph_format.space_after=Pt(7);p.paragraph_format.keep_together=True
  if p._p.xpath('.//w:drawing'):
   p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.keep_with_next=True;p.paragraph_format.line_spacing=1.0;p.paragraph_format.space_before=Pt(6);p.paragraph_format.space_after=Pt(7)
 for r in p._p.xpath('.//w:r'):
  color='255878' if r.getparent().tag==qn('w:hyperlink') else ('555555' if size==9.5 else '000000')
  fontxml(r,cn,size,bold,color)
# Keep a source line with the immediately preceding paragraph, avoiding isolated citations.
ps=list(d.paragraphs)
for i,p in enumerate(ps):
 if p.style.name=='Research Source' and i and not bibliography:
  pass
 # Skip the bibliography; its independent entries should flow normally.
 if p.text.startswith(('资料：','依据 ','打开资料')) and i and not re.match(r'^[A-Z]\d{2}',p.text):
  prev=ps[i-1]
  if prev.style.name=='Normal' and len(prev.text)<500:prev.paragraph_format.keep_with_next=True
# Tables use a single font, padding, header treatment and spacing.
for t in d.tables:
 t.alignment=WD_TABLE_ALIGNMENT.CENTER;t.autofit=False
 pr=t._tbl.tblPr
 for el in list(pr.findall(qn('w:tblBorders'))):pr.remove(el)
 bor=OxmlElement('w:tblBorders')
 for side in ['top','left','bottom','right','insideH','insideV']:
  x=OxmlElement('w:'+side);x.set(qn('w:val'),'single');x.set(qn('w:sz'),'4');x.set(qn('w:color'),'D9D9D9');bor.append(x)
 pr.append(bor)
 for i,row in enumerate(t.rows):
  tr=row._tr.get_or_add_trPr()
  for e in list(tr.findall(qn('w:trHeight'))):tr.remove(e)
  if not tr.findall(qn('w:cantSplit')):tr.append(OxmlElement('w:cantSplit'))
  if i==0 and not tr.findall(qn('w:tblHeader')):tr.append(OxmlElement('w:tblHeader'))
  for j,c in enumerate(row.cells):
   c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER;cp=c._tc.get_or_add_tcPr()
   for e in list(cp.findall(qn('w:shd')))+list(cp.findall(qn('w:tcMar'))):cp.remove(e)
   sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'E8EDF1' if i==0 else ('F6F8FA' if i%2==0 else 'FFFFFF'));cp.append(sh)
   mar=OxmlElement('w:tcMar')
   for side,val in [('top',80),('bottom',80),('left',100),('right',100)]:
    x=OxmlElement('w:'+side);x.set(qn('w:w'),str(val));x.set(qn('w:type'),'dxa');mar.append(x)
   cp.append(mar)
   for p in c.paragraphs:
    p.style=d.styles['Research Table'];pformat(p,line=15,after=0);p.paragraph_format.keep_together=True
    if len(t.rows)<=10 and i<len(t.rows)-1:p.paragraph_format.keep_with_next=True
    txt=p.text.strip();p.alignment=WD_ALIGN_PARAGRAPH.LEFT
    if i==0:p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    elif re.fullmatch(r'[\d,.\s]+(?:元|万元|人|次|场)?',txt):p.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    for r in p._p.xpath('.//w:r'):fontxml(r,'Heiti SC' if i==0 else 'Songti SC',10,i==0)
# Keep prose and citations visibly separated from table borders.
for t in d.tables:
 nxt=t._tbl.getnext()
 if nxt is not None and nxt.tag==qn('w:p'):
  from docx.text.paragraph import Paragraph
  q=Paragraph(nxt,t._parent)
  if not q.style.name.startswith('Heading'):q.paragraph_format.space_before=Pt(6)
# Add a clear subsection to the opening product comparison in chapter seven.
for t in d.tables:
 if t.cell(0,0).text=='可选方向':
  p=d.add_paragraph('7.1 首发产品与进入条件','Heading 2');t._tbl.addprevious(p._p);pformat(p,line=21,before=13,after=7);p.paragraph_format.keep_with_next=True;p.paragraph_format.keep_together=True
  for r in p._p.xpath('.//w:r'):fontxml(r,'Heiti SC',14,True)
  break
# Bookmarks and a one-page linked contents list.
for i,p in enumerate(headings,1):
 name='section_'+str(i);start=OxmlElement('w:bookmarkStart');start.set(qn('w:id'),str(2000+i));start.set(qn('w:name'),name);end=OxmlElement('w:bookmarkEnd');end.set(qn('w:id'),str(2000+i));p._p.insert(1 if p._p.pPr is not None else 0,start);p._p.append(end)
 if p.style.name=='Heading 1' or p.text.startswith('附录二') or re.match(r'^[45]\.\d ',p.text):toc.append((p.text,name,p.style.name=='Heading 1' or p.text.startswith('附录二')))
anchor=headings[0]._p
p=d.add_paragraph('目录','Heading 1');pformat(p,line=24,before=0,after=18);p.paragraph_format.page_break_before=True;p.paragraph_format.keep_with_next=True
for r in p._p.xpath('.//w:r'):fontxml(r,'Heiti SC',17,True)
anchor.addprevious(p._p)
for text,name,major in toc:
 p=d.add_paragraph(style='Research TOC');pformat(p,line=21,after=7 if major else 2,before=7 if major else 0);p.paragraph_format.keep_together=True;p.paragraph_format.left_indent=Cm(0 if major else .6);p.paragraph_format.tab_stops.add_tab_stop(Cm(16.4),WD_TAB_ALIGNMENT.RIGHT,WD_TAB_LEADER.DOTS)
 hl=OxmlElement('w:hyperlink');hl.set(qn('w:anchor'),name);r=OxmlElement('w:r');x=OxmlElement('w:t');x.text=text;r.append(x);fontxml(r,'Heiti SC' if major else 'Songti SC',11.5 if major else 10.5,major);hl.append(r);p._p.append(hl);p.add_run('\t')
 f=OxmlElement('w:fldSimple');f.set(qn('w:instr'),'PAGEREF '+name+' \\h');r=OxmlElement('w:r');x=OxmlElement('w:t');x.text='1';r.append(x);fontxml(r,'Songti SC',10.5);f.append(r);p._p.append(f);anchor.addprevious(p._p)
for sec in d.sections:
 for p in sec.header.paragraphs:p.clear()
 p=sec.header.paragraphs[0];p.add_run('中国高端线下社群市场研究报告');pformat(p,line=12,after=0)
 for r in p._p.xpath('.//w:r'):fontxml(r,'Songti SC',8.5,False,'666666')
 for p in sec.footer.paragraphs:p.clear()
 p=sec.footer.paragraphs[0];p.alignment=WD_ALIGN_PARAGRAPH.RIGHT;pformat(p,line=12,after=0)
 p.add_run('第 ');f=OxmlElement('w:fldSimple');f.set(qn('w:instr'),'PAGE');p._p.append(f);p.add_run(' 页')
 for r in p._p.xpath('.//w:r'):fontxml(r,'Songti SC',9,False,'666666')
# No hyperlink underline residue or title borders.
for p in d.paragraphs:
 if p.style.name.startswith(('Title','Subtitle','Heading')):
  for e in p._p.xpath('./w:pPr/w:pBdr'):e.getparent().remove(e)
settings=d.settings.element;x=settings.find(qn('w:updateFields'))
if x is None:x=OxmlElement('w:updateFields');settings.append(x)
x.set(qn('w:val'),'true')
d.save(out)
print('Saved',out,'TOC entries',len(toc))
