import { loadBank, TOPICS, TYPES, ROOT } from './interview-state.mjs';
import fs from 'node:fs';
import path from 'node:path';
const bank=loadBank(), ids=new Set(), errors=[];
for (const q of bank) {
  if (!q.id||ids.has(q.id)) errors.push(`duplicate/missing id: ${q.id}`); ids.add(q.id);
  for (const key of ['topic','subtopic','difficulty','type','source','tags']) if(q[key]===undefined) errors.push(`${q.id}: missing ${key}`);
  if(!TOPICS.includes(q.topic)) errors.push(`${q.id}: invalid topic`);
  if(!TYPES.includes(q.type)) errors.push(`${q.id}: invalid type`);
  if(!['easy','junior','junior_plus'].includes(q.difficulty)) errors.push(`${q.id}: invalid difficulty`);
  if(!q.source?.url||!q.source?.type) errors.push(`${q.id}: invalid source`);
  if(q.type==='coding') {
    for(const key of ['title','prompt','examples','constraints','expectedBehavior','evaluationNotes','hiddenTests','conceptsTested']) if(!q[key]?.length) errors.push(`${q.id}: missing coding ${key}`);
  } else {
    if(!q.question||!q.expectedPoints?.length) errors.push(`${q.id}: missing question/answer`);
    if(q.type==='mcq' && (q.options?.length!==4||!['A','B','C','D'].includes(q.correctOption)||new Set(q.options).size!==4)) errors.push(`${q.id}: invalid MCQ`);
    if(q.type==='output' && (!q.snippet||!q.expectedOutput)) errors.push(`${q.id}: missing output metadata`);
    if(q.type==='debug' && !q.snippet) errors.push(`${q.id}: missing debugging snippet`);
  }
}
const files=['html','css','javascript','angular','node','express'].map(x=>`data/questions/${x}.json`).concat(['javascript','angular','node-express'].map(x=>`data/coding/${x}.json`));
for(const file of files) {const data=JSON.parse(fs.readFileSync(path.join(ROOT,file),'utf8'));if(!Array.isArray(data)||!data.length)errors.push(`${file}: empty`);}
if(errors.length){console.error(errors.join('\n'));process.exit(1)}
console.log(`Valid: ${bank.length} unique questions/tasks; ${bank.filter(x=>x.type==='coding').length} coding tasks.`);
