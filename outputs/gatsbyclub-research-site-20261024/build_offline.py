from pathlib import Path
import base64,re,zipfile,json,hashlib
R=Path('/Users/olivialee/Documents/ChatGPT/社区平台');B=R/'outputs/gatsbyclub-research-site-20261024';D=B/'dist';O=B/'交付文件';O.mkdir(exist_ok=True)
def data(p,mime):return 'data:'+mime+';base64,'+base64.b64encode(p.read_bytes()).decode()
s=(D/'index.html').read_text();s=s.replace('<link rel="stylesheet" href="style.css">','<style>'+(D/'style.css').read_text()+'</style>');s=s.replace('<script src="app.js"></script>','<script>'+(D/'app.js').read_text()+'</script>')
for p in (D/'assets').iterdir():
 if p.suffix.lower() in ['.png','.jpg','.jpeg']:
  uri=data(p,'image/png'if p.suffix=='.png'else'image/jpeg');s=s.replace('assets/'+p.name,uri)
for n,m in [('report.pdf','application/pdf'),('research.xlsx','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),('speech.pdf','application/pdf')]:
 uri=data(D/n,m);s=s.replace('href="'+n+'"','href="'+uri+'" download="'+{'report.pdf':'高端线下社群市场调研与对标报告.pdf','research.xlsx':'高端线下社群市场调研与对标总表.xlsx','speech.pdf':'合伙人讨论讲解稿.pdf'}[n]+'"')
s=s.replace('<title>GatsbyClub｜把合适的人聚在一起</title>','<title>高端线下社群市场调研与对标｜离线阅读版</title>')
s=s.replace('资料核对截至 2026.10.24 · 66家机构线索 · 52条产品记录','离线阅读版 · 文字图片无需联网 · 资料截至2026.10.24')
s=s.replace('<p>官网截图、活动商品页和用户提供的小程序截图用于解释真实产品。','<p>文字、图片和交互已全部内嵌，无需联网；原始官网链接需要网络。附件也随资料包单独提供。官网截图、活动商品页和用户提供的小程序截图用于解释真实产品。')
file=O/'高端线下社群市场调研与对标_直接打开.html';file.write_text(s)
readme='''打开说明

1. 电脑：双击“高端线下社群市场调研与对标_直接打开.html”，用Chrome、Edge或Safari打开。
2. 手机：下载后选择“用浏览器打开”。微信文件预览可能不执行HTML交互，可保存到手机后用浏览器打开。
3. 正文、图片、三方向切换与图片放大无需网络，不需要登录。跳往原始官网时需要网络。
4. 若手机不方便打开HTML，直接阅读同包内PDF；PDF、Excel和讲稿均已单独提供。
'''
(O/'打开说明.txt').write_text(readme)
zp=O/'高端线下社群_离线阅读及附件.zip'
with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED)as z:
 z.write(file,file.name);z.writestr('打开说明.txt',readme)
 for n,dest in [('report.pdf','高端线下社群市场调研与对标报告.pdf'),('research.xlsx','高端线下社群市场调研与对标总表.xlsx'),('speech.pdf','合伙人讨论讲解稿.pdf')]:z.write(D/n,dest)
assert not re.search(r'(?:src|data-image)="(?!data:)[^"]+"',s)
(B/'qa/离线文件核验.json').write_text(json.dumps({'html':file.name,'html_bytes':file.stat().st_size,'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'images_and_scripts_embedded':True,'attachments_embedded':True,'zip':zp.name},ensure_ascii=False,indent=2))
print(file);print('HTML bytes',file.stat().st_size)
