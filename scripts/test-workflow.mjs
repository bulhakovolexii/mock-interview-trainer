import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import assert from 'node:assert/strict';

const dir=fs.mkdtempSync(path.join(os.tmpdir(),'interview-state-test-'));
const env={...process.env,INTERVIEW_STATE_DIR:dir};
function run(script,...args) {
  const p=spawnSync(process.execPath,[`scripts/${script}.mjs`,...args],{cwd:path.resolve(import.meta.dirname,'..'),env,encoding:'utf8'});
  assert.equal(p.status,0,p.stderr);
  return JSON.parse(p.stdout);
}
try {
  const first=run('select-question');
  assert(first.question.id);
  assert.equal(first.question.expectedPoints,undefined);
  assert.equal(first.question.correctOption,undefined);
  assert.equal(first.question.hiddenTests,undefined);
  assert.equal(run('select-question').question.id,first.question.id,'pending survives fresh invocation');
  run('record-answer','skipped','--note','test skip');
  let queue=JSON.parse(fs.readFileSync(path.join(dir,'review-queue.json'),'utf8'));
  assert.equal(queue.items.length,1);
  assert.equal(queue.items[0].dueAfter,8);
  for(let i=0;i<7;i++) {run('select-question');run('record-answer','correct');}
  queue=JSON.parse(fs.readFileSync(path.join(dir,'review-queue.json'),'utf8'));
  assert(queue.items.some(x=>x.dueAfter<=8));
  const reviewed=run('select-question','--mode','review');
  assert.equal(`${reviewed.question.topic}/${reviewed.question.subtopic}`,queue.items[0].concept);
  run('record-answer','correct');
  queue=JSON.parse(fs.readFileSync(path.join(dir,'review-queue.json'),'utf8'));
  assert(queue.items[0].dueAfter>=24,'successful review grows interval');
  const stats=run('stats');
  assert.equal(stats.totalAnswered,9);
  assert.equal(stats.results.skipped,1);
  assert.equal(fs.readFileSync(path.join(dir,'history.jsonl'),'utf8').trim().split('\n').length,9);
  assert(stats.session.id,'first selection creates a session id');
  const quick=run('session','new','--mode','quick');
  assert.equal(quick.target,10);
  for(let i=0;i<10;i++) {run('select-question');run('record-answer','correct');}
  assert.equal(run('select-question').sessionComplete,true);
  assert.equal(run('session','summary').answered,10);
  console.log('Workflow passed: fresh selection, private fields, pending persistence, skip scheduling, due review, history and stats.');
} finally {fs.rmSync(dir,{recursive:true,force:true});}
