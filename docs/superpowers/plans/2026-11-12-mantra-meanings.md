# Mantra meanings implementation plan

> **For agentic workers:** Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Show an English summary translation and an expandable word/meaning table on every existing mantra detail page.

**Architecture:** Store reviewed, mantra-specific study content separately from the existing dictionary, whose word mappings contain errors. Look up the content by the existing anuvakam/mantra route IDs. Render the summary below the recitation and a native, keyboard-accessible disclosure containing a two-column table. Sanskrit words use the existing script selector.

**Tech Stack:** Existing Angular 19 application, TypeScript, JSON, Jasmine/Karma, Node test runner; no new dependencies.

**Spec:** User request in this conversation: summary translation of every mantra in its website detail, plus a word/meaning table in an expandable section. English and collapsed-by-default are implementation choices consistent with existing English commentary.

## Global constraints

- Cover all 164 current mantra routes across 11 anuvakams.
- Preserve existing recitation, commentary, audio, editing, route IDs, and user changes.
- Translate the passage actually associated with each current route; do not silently renumber mantras.
- Write original concise English summaries using the Sanskrit and repository commentaries; check uncertain terms against references.
- Use ordered, distinct word forms, including particles; split sandhi for readability, retain meaningful compounds.
- Work in the current shared checkout for this continuation; no commits or publication requested.

## Review focus

- Every route has a nonempty summary and word list.
- Known bad dictionary mappings must not enter the new tables.
- Switching mantras must change both summary and rows and collapse the disclosure.
- Sanskrit script selection affects words but leaves English meanings unchanged.
- Long words and meanings fit a phone viewport; disclosure works with a keyboard.

### Task 1: Curated content

Files: create `src/mantra-meanings.json`, `scripts/mantra-meanings.test.js`.

- [x] Write and run coverage validation against all real route IDs; expect failure before data exists.
- [x] Author summary and ordered `{ word, meaning }` rows for each mantra, with separate content independent of the broken dictionary mappings.
- [x] Verify full coverage, nonempty text, uniqueness and known word meanings with `node --test scripts/mantra-meanings.test.js`.

### Task 2: Detail display

Files: modify `src/app/namakam.service.ts`, `src/app/mantra-detail/mantra-detail.component.{ts,html,css}`; create component spec.

- [x] Add component tests for rendered summary, word rows, route transitions and script selection; run before implementation.
- [x] Add typed `getMantraMeaning(anuvakamId, mantraId)` lookup and component state. Display Summary translation and a native details/summary Word meanings table.
- [x] Run full unit suite, content validation and production build; preview desktop/mobile and keyboard interaction if browser tooling is available.
- [x] Obtain fresh review and address material findings; record verification results below.

## Progress

- Recon: 164 current routes; dictionary mappings are unreliable, including इषवे, अस्तु, धन्वने. New study content will not reuse those meanings.
- Scope: current website assigns the opening earth-Rudras verse to 10_12. The summaries follow the displayed passages and existing routes; prior `src/namakam.json` corrections remain intact.

- Complete: 164 original summaries and 1,026 word rows; all three content checks pass.
- Complete: four new component tests cover missing legacy data, correct word mappings, route reset, script changes and unknown routes. Full suite: 19/19 passed in ChromeHeadless.
- Review: fresh read-only review found one material translation correction (10_5 उक्षितम्); verified both local commentaries and corrected to unborn child with a failing-then-passing regression check.
- Browser QA: Enter opens the native disclosure; navigation changes both summary and words and collapses it. Sanskrit-to-IAST selection works. 390px mobile table has no horizontal overflow; also inspected at desktop width.
- Production build passed. Warnings: unused RouterLink in AppComponent and initial bundle 1.22 MB exceeding the 1 MB warning threshold (below the 2 MB error threshold).
- No commits or deployment performed.

## Follow-up: table word interactions

User requested the same hover and click details as pada patha.

- Implemented identity-based dictionary matching and explicit aliases for spelling differences and split verbs; reused shared hover/click detail handlers.
- Added keyboard buttons, focus tooltips, Escape dismissal, panel scrolling, and route-state cleanup.
- Normalized string/array grammar references to prevent legacy entries crashing the shared detail views.
- Review correction: removed a false inflection link from सर्वाः to neuter-singular सर्वम्. Detailed dictionary data is unavailable for सर्वाः and योः; show their curated definition and a clear availability note.
- Fixed mobile tooltip clipping with available-height and viewport-width limits.
- Verification: 26/26 unit tests passed, content/link checks passed, and production build passed with the existing unused-import warning and an initial bundle warning (1.23 MB against 1 MB). Browser checks confirmed mouse hover, clicking, focus/Enter, Escape and mobile bounds.
- Fresh review performed; preexisting dictionary content quality was outside this interaction change. No deployment or commits.
