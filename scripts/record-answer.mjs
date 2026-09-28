import { state, save, loadBank, appendHistory, RESULTS, bucket, conceptKey, score } from './interview-state.mjs';

const args=process.argv.slice(2);
const result=args[0];
if (!RESULTS.includes(result)) throw Error(`Usage: node scripts/record-answer.mjs <${RESULTS.join('|')}> [--note "brief note"]`);
const i=args.indexOf('--note');
const note=i>=0 ? args[i+1]||'' : '';
const s=state();
const pending=s.session.pending;
if (!pending) throw Error('No pending question. Run npm run next first.');
const q=loadBank().find(x=>x.id===pending.id);
if (!q) throw Error(`Unknown question ${pending.id}`);
const now=new Date().toISOString();
const concept=conceptKey(q);
const n=s.stats.totalAnswered+1;
s.stats.totalAnswered=n;
s.stats.results[result]++;
for (const [map,key] of [[s.stats.byTopic,q.topic],[s.stats.bySubtopic,concept],[s.stats.byType,q.type]]) {
  const b=bucket(map,key); b.total++; b[result]++;
}
const c=s.stats.concepts[concept] ||= {attempts:0,correctCount:0,incorrectCount:0,skippedCount:0,lastAskedAt:null,lastResult:null,nextReviewAfter:null,mastery:0};
c.attempts++;
if (result==='correct'||result==='mostly_correct') c.correctCount++;
if (result==='incorrect'||result==='partially_correct') c.incorrectCount++;
if (result==='skipped') c.skippedCount++;
c.lastAskedAt=now; c.lastResult=result;
c.mastery=Math.round(score(s.stats.bySubtopic[concept])*100)/100;
const old=s.review.items.find(x=>x.concept===concept);
s.review.items=s.review.items.filter(x=>x.concept!==concept);
if (result!=='correct' || old) {
  let gap;
  if (result==='correct') gap=Math.min(60,old?.level>=2?30:15);
  else if (result==='mostly_correct') gap=15;
  else if (result==='partially_correct') gap=8;
  else gap=old?.level ? 5 : 7;
  const level=result==='correct' ? (old?.level||0)+1 : 0;
  c.nextReviewAfter=n+gap;
  s.review.items.push({concept,questionId:q.id,dueAfter:n+gap,level,lastResult:result});
} else c.nextReviewAfter=null;
if (['incorrect','partially_correct','skipped'].includes(result)) {
  const missed=s.missed.concepts[concept] ||= {questionIds:[],misses:0,lastMissAt:null};
  if (!missed.questionIds.includes(q.id)) missed.questionIds.push(q.id);
  missed.misses++; missed.lastMissAt=now;
}
if (result==='correct' && c.correctCount>=3) delete s.missed.concepts[concept];
if (q.type==='coding') {s.stats.codingTasksAttempted++;s.session.codingAttempted++;if (['correct','mostly_correct'].includes(result)){s.stats.codingTasksSolved++;s.session.codingSolved++;}}
s.stats.recentQuestionIds.push(q.id);
s.stats.recentQuestionIds=s.stats.recentQuestionIds.slice(-30);
s.stats.recentResults ||= [];
s.stats.recentResults.push(result);
s.stats.recentResults=s.stats.recentResults.slice(-12);
s.session.answered++;s.session.results[result]++;
s.session.recentConcepts.push(concept);s.session.recentConcepts=s.session.recentConcepts.slice(-12);
s.session.pending=null;
// Small, transparent adaptation; interviewer can override via --difficulty.
if (!s.profile.difficultyOverride && s.stats.recentResults.length>=6) {
  const recent=s.stats.recentResults.slice(-8);
  const rate=recent.reduce((n,r)=>n+({correct:1,mostly_correct:.75,partially_correct:.4,incorrect:0,skipped:0}[r]),0)/recent.length;
  s.profile.difficulty=rate>.8?'junior_plus':rate<.4?'easy':'junior';
}
save(s);
appendHistory({at:now,sessionId:s.session.id,questionId:q.id,topic:q.topic,subtopic:q.subtopic,type:q.type,result,note});
console.log(JSON.stringify({recorded:q.id,result,totalAnswered:n,nextReviewAfter:c.nextReviewAfter,sessionAnswered:s.session.answered}));
