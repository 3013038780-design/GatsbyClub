import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {FileBlob,SpreadsheetFile} from '@oai/artifact-tool';
const b=path.dirname(fileURLToPath(import.meta.url));const w=await SpreadsheetFile.importXlsx(await FileBlob.load(b+'/交付文件/中国高端会员社群市场研究数据工作簿_31家机构.xlsx'));
const p=await w.render({sheetName:'31家机构对照',range:'A4:D10',scale:1,format:'png'});await fs.writeFile(b+'/qa/删除两家后机构对照.png',new Uint8Array(await p.arrayBuffer()));
