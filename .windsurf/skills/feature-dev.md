---
description: Triggered when adding new features or functionality to the project
---

## Before starting
1. Read `CONTEXT.md` — understand current state and pending features
2. Read `AGENTS.md` — understand which module is affected
3. Read `vault/decisions/` — understand why existing design choices were made

## Rules
- Follow `.windsurf/rules/coding-style.md` (batch embed, COL_* constants, no streaming)
- Follow `.windsurf/rules/structure.md` (where new files go)
- Do not modify `ingest_excel.py` and `app.py` in the same commit unless tightly coupled
- New features in `app.py` go after the `build_prompt()` function, before sidebar code

## Planned features (implement in this order)
1. **Recurring failures dashboard** — query by date range + equipment, show frequency
2. **Export Summary** — download AI answer + source WOs as Excel or PDF
3. **PM Checklist generator** — structured output mode from LLM
4. **Analytics tab** — top failure categories, MTTR, most affected lines

## After implementing
- Update `CONTEXT.md` — move feature from "Pending" to "Working"
- Add decision rationale to `vault/decisions/` if a new design choice was made
- Run `/commit` workflow before pushing
