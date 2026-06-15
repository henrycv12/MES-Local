---
description: Triggered when diagnosing errors, unexpected behavior, or failed runs
---

## Before starting
1. Read `vault/known-issues/` — may already be documented
2. Read `CONTEXT.md` — check current known broken items
3. Identify which module is failing: `app.py` (UI/query), `ingest_excel.py` (ingestion), or ChromaDB

## Common failure modes

### Ingest fails
- Column not found → check `COL_*` constants match actual Excel headers exactly
- Ollama not running → run `ollama serve` first
- ChromaDB permission error → close Streamlit app before re-ingesting

### App fails to start
- "Collection not found" → `chroma_db/` missing or `work_orders` collection not created yet — run `python ingest_excel.py`
- Asyncio error on Windows → confirm `asyncio.WindowsSelectorEventLoopPolicy()` is set at top of `app.py`
- Ollama model not found → run `ollama pull llama3.2:1b` and `ollama pull nomic-embed-text`

### Wrong query results
- Old/wrong dates → re-ingest after deleting `chroma_db/` (ensures `date_ts` metadata is present)
- Missing recency re-rank → check `RECENCY_KEYWORDS` set in `app.py` includes the trigger word used

## After fixing
- Update `vault/known-issues/` — remove resolved issue or add new one
- Update `CONTEXT.md` status if applicable
