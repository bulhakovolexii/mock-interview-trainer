import { state, save, STATE_DIR } from './interview-state.mjs';
import fs from 'node:fs';
import path from 'node:path';
const action=process.argv[2];
const s=state();
if(action==='new') {
  const mode=process.argv.includes('--mode') ? process.argv[process.argv.indexOf('--mode')+1] : 'normal';
  const target=process.argv.includes('--target') ? Number(process.argv[process.argv.indexOf('--target')+1]) : null;
  if(!['normal','focus','review','quick','full'].includes(mode)) throw Error('Invalid mode');
  if(target!==null && (!Number.isInteger(target)||target<1)) throw Error('Invalid target');
  s.session={id:new Date().toISOString(),startedAt:new Date().toISOString(),mode,target:target||(mode==='quick'?10:mode==='full'?35:null),answered:0,results:{correct:0,mostly_correct:0,partially_correct:0,incorrect:0,skipped:0},codingAttempted:0,codingSolved:0,pending:null,recentConcepts:[]};
  s.profile.mode=mode;
  s.profile.difficultyOverride=false;
  if(mode!=='focus') s.profile.focus=null;
  save(s);
  console.log(JSON.stringify({newSession:s.session.id,mode:s.session.mode,target:s.session.target}));
} else if(action==='stop') {
  s.session.stoppedAt=new Date().toISOString();
  save(s);
  console.log(JSON.stringify({stopped:true,answered:s.session.answered,pending:s.session.pending?.id||null}));
} else if(action==='summary') {
  const id=s.session.id;
  const history=fs.readFileSync(path.join(STATE_DIR,'history.jsonl'),'utf8').split('\n').filter(Boolean).map(JSON.parse).filter(x=>x.sessionId===id);
  const grouped={};
  for(const h of history) {const b=grouped[h.topic]||={total:0,strong:0,partial:0,missed:0};b.total++;if(['correct','mostly_correct'].includes(h.result))b.strong++;else if(h.result==='partially_correct')b.partial++;else b.missed++;}
  const weak=[...new Set(history.filter(x=>['incorrect','partially_correct','skipped'].includes(x.result)).map(x=>`${x.topic}/${x.subtopic}`))].slice(0,5);
  console.log(JSON.stringify({sessionId:id,answered:s.session.answered,byTopic:grouped,skippedConcepts:[...new Set(history.filter(x=>x.result==='skipped').map(x=>`${x.topic}/${x.subtopic}`))],revisionPriorities:weak,coding:{attempted:s.session.codingAttempted,solved:s.session.codingSolved}},null,2));
} else throw Error('Usage: node scripts/session.mjs new [--mode normal|focus|review|quick|full] [--target N] | summary | stop');
