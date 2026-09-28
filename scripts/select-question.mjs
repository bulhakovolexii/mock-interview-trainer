import { state, save, loadBank, conceptKey, publicQuestion, score } from './interview-state.mjs';

const args = process.argv.slice(2);
const value = flag => { const i=args.indexOf(flag); return i>=0 ? args[i+1] : null; };
const s=state();
const bank=loadBank();
const byId=new Map(bank.map(q=>[q.id,q]));
if (!s.session.id) { s.session.id=new Date().toISOString(); s.session.startedAt=s.session.id; }
if (args.includes('--new-session')) {
  s.session={id:new Date().toISOString(),startedAt:new Date().toISOString(),mode:value('--mode')||s.profile.mode||'normal',target:Number(value('--target'))||null,answered:0,results:{correct:0,mostly_correct:0,partially_correct:0,incorrect:0,skipped:0},codingAttempted:0,codingSolved:0,pending:null,recentConcepts:[]};
}
const mode=value('--mode');
if (mode) { s.profile.mode=mode; s.session.mode=mode; }
const focus=value('--focus');
if (focus) { if (!['javascript','angular','node','express','html','css'].includes(focus)) throw Error('Invalid focus'); s.profile.focus=focus; s.profile.mode='focus'; s.session.mode='focus'; }
if (args.includes('--clear-focus')) { s.profile.focus=null; s.profile.mode='normal'; s.session.mode='normal'; }
const difficulty=value('--difficulty');
if (difficulty) { if (!['easy','junior','junior_plus'].includes(difficulty)) throw Error('Invalid difficulty'); s.profile.difficulty=difficulty; s.profile.difficultyOverride=true; }
if (s.session.target && s.session.answered >= s.session.target && !s.session.pending) {
  save(s); console.log(JSON.stringify({sessionComplete:true,answered:s.session.answered,mode:s.session.mode})); process.exit(0);
}
if (s.session.pending) {
  const q=byId.get(s.session.pending.id);
  if (!q) throw Error(`Pending question missing from bank: ${s.session.pending.id}`);
  save(s); console.log(JSON.stringify({pending:true,question:publicQuestion(q)},null,2)); process.exit(0);
}
const recent=new Set(s.stats.recentQuestionIds.slice(-18));
const due=s.review.items.filter(x=>x.dueAfter<=s.stats.totalAnswered).sort((a,b)=>a.dueAfter-b.dueAfter);
let selected=null, reviewOf=null;
const reviewMode=s.session.mode==='review';
const shouldReview=due.length && (reviewMode || Math.random()<.3);
if (shouldReview) {
  const entry=due[0];
  const candidates=bank.filter(q=>conceptKey(q)===entry.concept && !recent.has(q.id));
  selected=candidates.length ? candidates[Math.floor(Math.random()*candidates.length)] : byId.get(entry.questionId);
  reviewOf=entry.concept;
}
if (!selected) {
  const weights={javascript:40,angular:30,node:9,express:6,html:7.5,css:7.5};
  let pool=bank.filter(q=>!recent.has(q.id));
  if (!pool.length) pool=bank;
  if (reviewMode) {
    const weak=pool.filter(q=>s.missed.concepts[conceptKey(q)] || (s.stats.bySubtopic[conceptKey(q)]?.total>=2 && score(s.stats.bySubtopic[conceptKey(q)])<.65));
    if (weak.length) pool=weak;
  }
  const recentTypes=s.stats.recentQuestionIds.slice(-8).map(id=>byId.get(id)?.type);
  const recentCoding=recentTypes.slice(-3).filter(x=>x==='coding').length;
  const typeWeights={open:40,mcq:13,output:12,debug:15,coding:20};
  const targetRank={easy:0,junior:1,junior_plus:2}[s.profile.difficulty] ?? 1;
  const weighted=pool.map(q=>{
    let w=weights[q.topic] / bank.filter(x=>x.topic===q.topic).length;
    if (reviewMode && s.missed.concepts[conceptKey(q)]) w*=4;
    w*=typeWeights[q.type] / bank.filter(x=>x.type===q.type).length * 10;
    if (q.type==='coding' && recentCoding) w*=.05;
    if (s.session.recentConcepts.slice(-4).includes(conceptKey(q))) w*=.1;
    if (Math.abs(({easy:0,junior:1,junior_plus:2}[q.difficulty]??1)-targetRank)>0) w*=.6;
    const weak=s.stats.bySubtopic[conceptKey(q)];
    if (weak?.total>=2 && score(weak)<.6) w*=1.5;
    return [q,w];
  });
  // Normalize per topic so the type mix cannot silently skew the requested topic mix.
  const topicTotals={};
  for (const [q,w] of weighted) topicTotals[q.topic]=(topicTotals[q.topic]||0)+w;
  for (const pair of weighted) {
    const q=pair[0];
    let desired=weights[q.topic];
    if (s.session.mode==='focus' && s.profile.focus) desired=q.topic===s.profile.focus ? 75 : 25*weights[q.topic]/(100-weights[s.profile.focus]);
    pair[1]*=desired/topicTotals[q.topic];
  }
  const total=weighted.reduce((n,[,w])=>n+w,0);
  let pick=Math.random()*total;
  selected=weighted.find(([,w])=>(pick-=w)<=0)?.[0]||weighted.at(-1)[0];
}
s.session.pending={id:selected.id,selectedAt:new Date().toISOString(),reviewOf};
save(s);
console.log(JSON.stringify({pending:false,question:publicQuestion(selected)},null,2));
