---
/audit
---

Run periodically for a project health check.

1. Scan all `.py` files for `TODO` and `FIXME` comments — list every one found
2. Compare `vault/known-issues/` against current code — flag anything resolved or newly broken
3. Check `.windsurf/rules/coding-style.md` conventions are being followed (batch embed, incremental ingest, COL_* constants)
4. Verify `.gitignore` still excludes `chroma_db/`, `*.xlsx`, `*.pdf`
5. Check `CONTEXT.md` status section is still accurate
6. Verify `AGENTS.md` data flow matches actual code in `app.py` and `ingest_excel.py`
7. Output a prioritized findings list:
   - **Critical**: things that could corrupt the vector DB or break ingestion
   - **Medium**: performance issues, outdated docs, stale vault entries
   - **Low**: cleanup, cosmetic issues, unused imports
