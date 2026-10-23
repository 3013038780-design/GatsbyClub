import asyncio
from pathlib import Path
import collect_community as c
c.ROOT=Path(__file__).resolve().parents[1]/'collection-discovery-20261021'
c.ROOT.mkdir(exist_ok=True);(c.ROOT/'raw').mkdir(exist_ok=True)
c.MAX_FOLLOWUPS_PER_BRAND=1
c.SEEDS={
 '创合汇':['https://www.chuanghehui.com/view/club','https://www.chuanghehui.cn/'],
 '中企会企业家俱乐部':['https://www.ceccclub.com/'],
 '阿拉善SEE生态协会':['https://conservation.see.org.cn/disclosure/Annual/','https://conservation.see.org.cn/admission/'],
 '三亚鸿洲国际游艇会':['https://www.visun-yacht.com/member.php'],
 '三亚半山半岛帆船港':['https://serenity-marina.com/Jo_index_gci_14.html'],
}
c.PDFS=[]
asyncio.run(c.main())
