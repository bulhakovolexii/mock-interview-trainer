import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
export const STATE_DIR = path.resolve(process.env.INTERVIEW_STATE_DIR || path.join(ROOT, 'progress'));
export const RESULTS = ['correct', 'mostly_correct', 'partially_correct', 'incorrect', 'skipped'];
export const TOPICS = ['javascript', 'angular', 'node', 'express', 'html', 'css'];
export const TYPES = ['open', 'mcq', 'output', 'debug', 'coding'];

export function read(name, fallback) {
  const file = path.join(STATE_DIR, name);
  return fs.existsSync(file) ? JSON.parse(fs.readFileSync(file, 'utf8')) : structuredClone(fallback);
}
export function write(name, value) {
  fs.mkdirSync(STATE_DIR, { recursive: true });
  const file = path.join(STATE_DIR, name);
  const temp = `${file}.${process.pid}.tmp`;
  fs.writeFileSync(temp, JSON.stringify(value, null, 2) + '\n');
  fs.renameSync(temp, file);
}
export function appendHistory(event) {
  fs.mkdirSync(STATE_DIR, { recursive: true });
  fs.appendFileSync(path.join(STATE_DIR, 'history.jsonl'), JSON.stringify(event) + '\n');
}
export function loadBank() {
  const files = [...['html','css','javascript','angular','node','express'].map(x => `data/questions/${x}.json`), ...['javascript','angular','node-express'].map(x => `data/coding/${x}.json`)];
  return files.flatMap(file => JSON.parse(fs.readFileSync(path.join(ROOT, file), 'utf8')));
}
export const DEFAULTS = {
  'profile.json': { preferredLanguage: 'uk', mode: 'normal', focus: null, difficulty: 'junior', difficultyOverride: false, createdAt: null },
  'stats.json': { totalAnswered: 0, results: Object.fromEntries(RESULTS.map(x => [x,0])), byTopic: {}, bySubtopic: {}, byType: {}, concepts: {}, codingTasksAttempted: 0, codingTasksSolved: 0, recentQuestionIds: [], recentResults: [] },
  'missed.json': { concepts: {} },
  'review-queue.json': { items: [] },
  'current-session.json': { id: null, startedAt: null, mode: 'normal', target: null, answered: 0, results: Object.fromEntries(RESULTS.map(x => [x,0])), codingAttempted: 0, codingSolved: 0, pending: null, recentConcepts: [] },
};
export function initialize() {
  fs.mkdirSync(STATE_DIR, { recursive: true });
  for (const [file, value] of Object.entries(DEFAULTS)) if (!fs.existsSync(path.join(STATE_DIR,file))) {
    const copy = structuredClone(value);
    if (file === 'profile.json') copy.createdAt = new Date().toISOString();
    write(file, copy);
  }
  const history = path.join(STATE_DIR,'history.jsonl');
  if (!fs.existsSync(history)) fs.writeFileSync(history,'');
}
export function state() {
  initialize();
  return { profile: read('profile.json',DEFAULTS['profile.json']), stats: read('stats.json',DEFAULTS['stats.json']), missed: read('missed.json',DEFAULTS['missed.json']), review: read('review-queue.json',DEFAULTS['review-queue.json']), session: read('current-session.json',DEFAULTS['current-session.json']) };
}
export function save(s) {
  write('profile.json',s.profile); write('stats.json',s.stats); write('missed.json',s.missed); write('review-queue.json',s.review); write('current-session.json',s.session);
}
export function conceptKey(q) { return `${q.topic}/${q.subtopic}`; }
export function bucket(map,key) {
  return map[key] ||= { total: 0, correct: 0, mostly_correct: 0, partially_correct: 0, incorrect: 0, skipped: 0 };
}
export function score(bucketValue) {
  if (!bucketValue?.total) return 0;
  return (bucketValue.correct + .75*bucketValue.mostly_correct + .4*bucketValue.partially_correct) / bucketValue.total;
}
export function publicQuestion(q) {
  const keys = q.type === 'coding' ? ['id','topic','subtopic','difficulty','type','title','prompt','examples','constraints','expectedBehavior','starterCode'] : ['id','topic','subtopic','difficulty','type','question','snippet','options'];
  return Object.fromEntries(keys.filter(k => q[k] !== undefined).map(k => [k,q[k]]));
}
