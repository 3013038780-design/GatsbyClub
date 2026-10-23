import {Workbook} from '@oai/artifact-tool';const w=Workbook.create();w.worksheets.add('x');console.log(w.help('range.hyperlink',{include:'index,examples,notes',maxChars:2500}).ndjson);
