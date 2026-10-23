"""Restyle the delivered documents without regenerating research content."""
from pathlib import Path
from copy import deepcopy
import json,re,shutil
from docx import Document
from docx.shared import Cm,Pt,Inches,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH,WD_BREAK
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

ROOT=Path(__file__).resolve().parent.parent
QA=ROOT/'qa'/'format-revision';QA.mkdir(parents=True,exist_ok=True)
BASE=ROOT/'research'/'original-format';BASE.mkdir(exist_ok=True)
FILES=['中国高端社交市场研究正式报告.docx','高端社交公司合伙人决策摘要.docx','三家高端服务模式深度案例档案.docx']
BODY='Songti SC';HEAD='Heiti SC'
NUM=['一','二','三','四','五','六','七','八','九','十']

def node(parent,name,**attrs):
    old=parent.find(qn('w:'+name))
    e=old if old is not None else OxmlElement('w:'+name)
    for k,v in attrs.items():e.set(qn('w:'+k),str(v))
    if old is None:parent.append(e)
    return e

def rfont(run,size=12,bold=False,head=False,color='000000'):
    rp=run._element.get_or_add_rPr()
    rf=node(rp,'rFonts',ascii='Arial' if head else 'Times New Roman',hAnsi='Arial' if head else 'Times New Roman',eastAsia=HEAD if head else BODY,cs='Arial')
    for a in ['asciiTheme','hAnsiTheme','eastAsiaTheme','cstheme']:rf.attrib.pop(qn('w:'+a),None)
    for e in list(rp):
        if e.tag in [qn('w:rStyle'),qn('w:highlight'),qn('w:shd')]:rp.remove(e)
    run.font.size=Pt(size);run.font.bold=bold;run.font.italic=False;run.font.color.rgb=RGBColor.from_string(color)
    node(rp,'szCs',val=int(size*2))

def pformat(p,size=12,line=20,after=4,before=0,indent=True,align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    f=p.paragraph_format;f.space_before=Pt(before);f.space_after=Pt(after);f.line_spacing=Pt(line)
    f.first_line_indent=Pt(24 if indent else 0);f.left_indent=Pt(0);f.right_indent=Pt(0);f.alignment=align;f.widow_control=True
    node(p._p.get_or_add_pPr(),'snapToGrid',val=0)

def source_text(doc):
    # Includes external hyperlink labels, table text and paragraph order.
    return [''.join(p.itertext()) for p in []] if False else [t.text or '' for t in doc._element.body.iter(qn('w:t'))]

def add_before(p,text,style='Heading 1'):
    pp=OxmlElement('w:p');p._p.addprevious(pp);new=Paragraph(pp,p._parent);new.style=style;new.add_run(text);return new

def highlight(p,text,size=12):
    if not text or text not in p.text:return
    raw=p.text
    # Used only on plain paragraphs, never paragraphs with hyperlinks or fields.
    if p._p.find('.//'+qn('w:hyperlink')) is not None:return
    p.clear();a,b=raw.split(text,1)
    if a:rfont(p.add_run(a),size)
    rfont(p.add_run(text),size,bold=True)
    if b:rfont(p.add_run(b),size)

result={}
for filename in FILES:
    original=BASE/filename
    if not original.exists():shutil.copy2(ROOT/filename,original)
    doc=Document(original);before_text=source_text(doc)
    is_report='正式报告' in filename;is_memo='摘要' in filename;is_cases=not(is_report or is_memo)
    sec=doc.sections[0]
    # A4 is used for the requested Chinese business-report layout.
    sec.page_width=Cm(21);sec.page_height=Cm(29.7)
    sec.left_margin=Cm(2.6);sec.right_margin=Cm(2.4);sec.top_margin=Cm(2.3);sec.bottom_margin=Cm(2.2)
    sec.header_distance=Cm(1.1);sec.footer_distance=Cm(1.05)
    for g in list(sec._sectPr.findall(qn('w:docGrid'))):sec._sectPr.remove(g)
    for s in doc.styles:
        for b in list(s._element.iter(qn('w:pBdr'))):b.getparent().remove(b)
        if s.type==1:
            s.font.name='Times New Roman';s.font.color.rgb=RGBColor(0,0,0)
            rf=node(s._element.get_or_add_rPr(),'rFonts',ascii='Times New Roman',hAnsi='Times New Roman',eastAsia=BODY)
            for a in ['asciiTheme','hAnsiTheme','eastAsiaTheme','cstheme']:rf.attrib.pop(qn('w:'+a),None)
    st=doc.styles['Normal'];st.font.size=Pt(12);st.font.bold=False
    st.paragraph_format.line_spacing=Pt(20);st.paragraph_format.space_after=Pt(4);st.paragraph_format.first_line_indent=Pt(24)
    st.paragraph_format.keep_with_next=False
    for name,size in [('Title',22),('Heading 1',16),('Heading 2',14),('Heading 3',12)]:
        s=doc.styles[name];s.font.name='Arial';s.font.size=Pt(size);s.font.bold=True
        rf=node(s._element.get_or_add_rPr(),'rFonts',ascii='Arial',hAnsi='Arial',eastAsia=HEAD)
        for a in ['asciiTheme','hAnsiTheme','eastAsiaTheme','cstheme']:rf.attrib.pop(qn('w:'+a),None)
        f=s.paragraph_format;f.first_line_indent=Pt(0);f.line_spacing=Pt(size+7);f.space_before=Pt(14 if name!='Title' else 0);f.space_after=Pt(6);f.keep_with_next=True

    # Preserve the numbered research sections while adding a short chapter hierarchy.
    added=[]
    if is_report:
        groups={1:'一　研究结论与方法',3:'二　宏观市场与需求',9:'三　细分市场与经营模式',17:'四　三家深度案例',20:'五　经济性与进入条件',22:'六　公司方向与后续验证',25:'七　验收结果与附件说明'}
        for pp in list(doc.paragraphs):
            m=re.match(r'^(\d{2})\s+(.+)$',pp.text)
            if m and pp.style.name=='Heading 1':
                idx=int(m.group(1))
                if idx in groups:added.append(add_before(pp,groups[idx]))
                pp.style='Heading 2'
        for pp in doc.paragraphs:
            if pp.text=='附件使用与验收':pp.style='Heading 2'
            if pp.text=='来源索引':pp.clear();pp.add_run('附录　来源索引')
    elif is_memo:
        for i,pp in enumerate([x for x in doc.paragraphs if x.style.name=='Heading 2']):
            pp.text=NUM[i]+'　'+pp.text

    in_sources=False;after_head=False
    for pp in doc.paragraphs:
        txt=pp.text.strip();sty=pp.style.name
        if not txt:
            pformat(pp,after=0,line=3,indent=False);continue
        if txt in ['附录　来源索引','来源索引']:in_sources=True
        if sty=='Title':
            pformat(pp,line=30,before=0,after=12,indent=False,align=WD_ALIGN_PARAGRAPH.CENTER)
            for r in pp.runs:rfont(r,22,True,True)
            pp.paragraph_format.keep_with_next=True
            continue
        if sty.startswith('Heading'):
            lev=int(sty.split()[-1]);size=16 if lev==1 else 14
            if is_memo:size=13
            if txt=='阅读导航':size=13
            pformat(pp,line=size+7,before=13 if lev==1 else 10,after=5,indent=False,align=WD_ALIGN_PARAGRAPH.LEFT)
            for r in pp.runs:rfont(r,size,True,True)
            pp.paragraph_format.keep_with_next=True;after_head=True;continue
        if txt.startswith('中国大陆'):
            pformat(pp,line=16,after=12,indent=False,align=WD_ALIGN_PARAGRAPH.CENTER)
            for r in pp.runs:rfont(r,10.5)
            continue
        if txt.startswith('证据索引'):
            pformat(pp,line=14,after=7,indent=False,align=WD_ALIGN_PARAGRAPH.LEFT)
            for r in pp.runs:rfont(r,9,color='505050')
            after_head=False;continue
        if in_sources:
            pformat(pp,line=14 if is_cases else 14.5,after=2 if is_cases else 3,indent=False,align=WD_ALIGN_PARAGRAPH.LEFT)
            pp.paragraph_format.keep_together=True
            for r in pp.runs:rfont(r,9.5,bold=bool(re.fullmatch(r'(S\d+|X\d+(?:-\d+)?)',r.text.strip())),color='333333')
            for rr in pp._p.findall('.//'+qn('w:hyperlink')+'/'+qn('w:r')):
                rp=node(rr,'rPr');rf=node(rp,'rFonts',ascii='Times New Roman',hAnsi='Times New Roman',eastAsia=BODY)
                for a in ['asciiTheme','hAnsiTheme','eastAsiaTheme','cstheme']:rf.attrib.pop(qn('w:'+a),None)
                node(rp,'sz',val=19);node(rp,'color',val='254E76')
            continue
        secondary=txt.startswith(('核验统计','每个字段后','记录类型','本轮未提交','会谈记录'))
        size=11 if secondary else 12
        pformat(pp,line=18 if secondary else 20,after=4,indent=not secondary)
        if txt.startswith('记录类型'):pp.paragraph_format.keep_with_next=True
        for r in pp.runs:rfont(r,size)
        if txt.startswith(('E01','E02','E03','E04','E05','E06')):
            pformat(pp,line=19,before=8,after=4,indent=False,align=WD_ALIGN_PARAGRAPH.LEFT)
            for r in pp.runs:rfont(r,11.5,True,True)
            pp.paragraph_format.keep_with_next=True
        elif is_memo:
            lead=re.split(r'[；。]',txt)[0]
            if 8<len(lead)<70:highlight(pp,lead,size)
        elif after_head and len(txt)>50:
            terms=['优先验证','第三方估算','不平均、不拼接','不能直接推导','不能视作中国婚恋收入','具体口径尚未定义','真实付费与交付证据','研究假设','实际客户','条件性建议']
            for term in terms:
                if term in txt:highlight(pp,term,size);break
        after_head=False

    # Tables use black type, pale headers and compact, consistent cells.
    for t in doc.tables:
        old=[float(c.width or Inches(1)) for c in t.columns]
        total=sum(old);usable=sec.page_width-sec.left_margin-sec.right_margin
        widths=[int(usable*w/total) for w in old]
        t.autofit=False
        for c,w in zip(t.columns,widths):c.width=w
        for i,row in enumerate(t.rows):
            row.height=None;pr=row._tr.get_or_add_trPr();node(pr,'cantSplit')
            if i==0:node(pr,'tblHeader')
            for j,cell in enumerate(row.cells):
                cell.width=widths[j];cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
                cp=cell._tc.get_or_add_tcPr()
                for e in list(cp):
                    if e.tag in [qn('w:shd'),qn('w:tcBorders'),qn('w:tcMar')]:cp.remove(e)
                node(cp,'shd',fill='E9ECEF' if i==0 else 'FFFFFF')
                borders=node(cp,'tcBorders')
                for edge in ['top','left','bottom','right']:node(borders,edge,val='single',sz=4,color='D9D9D9')
                mar=node(cp,'tcMar')
                for side,value in [('top',55),('bottom',55),('left',90),('right',90)]:node(mar,side,w=value,type='dxa')
                for pp in cell.paragraphs:
                    pformat(pp,line=15.5,after=0,indent=False,align=WD_ALIGN_PARAGRAPH.CENTER if i==0 else WD_ALIGN_PARAGRAPH.LEFT)
                    is_flow=len(t.columns)==2 and t.cell(0,0).text=='流程阶段'
                    pp.paragraph_format.keep_with_next=(i<2 or ((len(t.rows)<=5 or is_flow) and i<len(t.rows)-1))
                    is_unknown=pp.text=='未公开核实' or '已查未得' in pp.text
                    for r in pp.runs:rfont(r,10.5,bold=i==0,head=i==0,color='595959' if is_unknown and i>0 else '000000')
                    if i>0 and j==len(row.cells)-1 and re.match(r'^(S\d|X\d)',pp.text):
                        for r in pp.runs:rfont(r,9.5,color='505050')
    for part in [sec.header,sec.footer]:
        for pp in part.paragraphs:
            pformat(pp,line=13,after=0,indent=False,align=WD_ALIGN_PARAGRAPH.RIGHT)
            for r in pp.runs:rfont(r,9)
    if is_memo:
        for pp in doc.paragraphs:
            if pp.text.startswith('五　'):pp.paragraph_format.page_break_before=True
    # Keep evidence lines with the paragraph or final table row they document.
    for pp in doc.paragraphs:
        if not pp.text.startswith('证据索引'):continue
        pp.paragraph_format.keep_together=True
        prev=pp._p.getprevious()
        while prev is not None and prev.tag==qn('w:p') and not ''.join(prev.itertext()).strip():
            node(prev.get_or_add_pPr(),'keepNext');prev=prev.getprevious()
        if prev is not None and prev.tag==qn('w:p'):
            node(prev.get_or_add_pPr(),'keepNext')
        elif prev is not None and prev.tag==qn('w:tbl'):
            rr=prev.findall(qn('w:tr'))
            if rr:
                for cellp in rr[-1].findall('.//'+qn('w:p')):node(cellp.get_or_add_pPr(),'keepNext')
    # Confirm substantive original text remains present; only headings were grouped/numbered.
    old_tables=[[c.text for row in t.rows for c in row.cells] for t in Document(original).tables]
    assert old_tables==[[c.text for row in t.rows for c in row.cells] for t in doc.tables]
    original_plain=''.join(before_text)
    new_plain=''.join(source_text(doc))
    for pp in Document(original).paragraphs:
        if pp.style.name.startswith('Heading') or pp.style.name=='Title':continue
        if pp.text and not pp._p.findall('.//'+qn('w:hyperlink')):assert pp.text in new_plain,pp.text[:80]
    doc.save(ROOT/filename)
    result[filename]={'tables':len(doc.tables),'body_font':BODY,'heading_font':HEAD,'body_pt':12,'line_pt':20,'page':'A4','content_preserved':True,'chapter_groups_added':len(added)}
(QA/'document-style-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps(result,ensure_ascii=False))
