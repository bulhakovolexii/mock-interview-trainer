# Question bank format

Each JSON file is an array. Stable `id`, `topic`, `subtopic`, `difficulty` (`easy`, `junior`, `junior_plus`), `type`, `tags`, and `source` are required. Question types: `open`, `mcq`, `output`, `debug`, and `coding`.

Non-coding questions use `question`, `expectedPoints`, `commonMistakes`, and `followUps`. MCQ adds four `options` and `correctOption` (`A`–`D`). Output questions add `snippet` and `expectedOutput`. Debugging questions add `snippet`.

Coding tasks use `title`, `prompt`, `examples`, `constraints`, `expectedBehavior`, optional `starterCode`, `evaluationNotes`, `hiddenTests`, and `conceptsTested`. `hiddenTests` currently contains written criteria; the interviewer designs and runs relevant local cases after reading a submitted solution. Angular tasks accept a `.ts`, `.html`, or a small task directory. Express tasks use an in-memory repository.

Private answer fields stay in the bank for evaluation. `scripts/select-question.mjs` emits only public fields. Keep IDs stable after a question enters progress. `scripts/build-bank.py` is the editable source for the initial bank; rerunning it regenerates the initial arrays, so edit it when changing curated content.

State model: `review-queue.json` entries use `dueAfter`, a global answered-question count. A miss is due roughly seven later answers; another miss is due sooner, successful reviews move farther apart. `stats.json` stores counts and a simple mastery fraction by concept. `history.jsonl` is append-only. `current-session.json` stores the single pending ID. Helper writes use temporary files and rename for individual JSON files.
