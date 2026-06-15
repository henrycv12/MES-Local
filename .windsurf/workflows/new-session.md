---
/new-session
---

Run this at the start of every work session.

1. Read `CONTEXT.md` — understand current project state and what's pending
2. Read `AGENTS.md` — refresh architecture knowledge (RAG pipeline, module map)
3. Read `vault/known-issues/` — check for active bugs or workarounds
4. Check `chroma_db/` exists — if not, remind user to run `python ingest_excel.py` first
5. Ask the user: what are we working on today?
6. Load the relevant skill from `.windsurf/skills/` based on the task type
