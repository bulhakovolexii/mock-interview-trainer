# Junior Fullstack interview workspace

Open Codex in this directory and type **`Починаємо інтерв'ю`**. Codex reads `AGENTS.md` and the saved progress, then asks one question at a time in chat. Answer in Ukrainian or English.

Useful requests: `continue interview`, `Давай 10 питань по JavaScript`, `focus angular`, `review missed`, `stats`, `weak topics`, `full mock interview`, `session summary`, `stop interview`. For coding: `Зробив задачу: solutions/debounce.js` (or any path inside this project). The interviewer will inspect and, when appropriate, test your file.

The bank lives in `data/questions/` and `data/coding/`. Progress lives in `progress/` as readable JSON and JSONL. `current-session.json` keeps a pending question across Codex sessions. `history.jsonl` is the answer log; `review-queue.json` schedules spaced review. The project has no runtime dependencies or database.

To expand the bank with AI or add a topic such as React, follow [the expansion guide](docs/EXPANDING_THE_BANK.md). You can ask Codex to carry out the guide directly; it includes a ready-to-use React request and protects existing progress.

`npm run validate` checks the bank; `npm run stats` prints saved statistics; `npm run next` safely prints only the public part of the pending/next question. Codex records evaluations with `node scripts/record-answer.mjs correct|mostly_correct|partially_correct|incorrect|skipped`.

`npm run new-session` resets only current session counters and pending question, preserving learning history. For a 10-question interview use `node scripts/session.mjs new --mode quick`; for a 35-question mock use `node scripts/session.mjs new --mode full`. To reset **all** learning history deliberately, back up and remove the files in `progress/`, then run `npm run stats` to initialize fresh files. This is intentionally not an npm script. Candidate solution files under `solutions/` are ignored by Git; progress files are not ignored, so you can version them if you choose.
