# Coding Style Rules

## Naming conventions
- Variables: `snake_case` (e.g. `top_k`, `wo_no`, `date_ts`)
- Functions: `snake_case` verbs (e.g. `retrieve_context`, `build_prompt`, `ingest_excel`)
- Constants: `UPPER_SNAKE_CASE` at top of file (e.g. `EMBED_MODEL`, `TOP_K`, `CHROMA_DIR`)
- Files: `snake_case.py`

## Patterns in use
- All column mappings defined as `COL_*` constants at top of `ingest_excel.py` — never hardcode column names inline
- `safe(row, col, default)` helper for all DataFrame cell reads — never access `.iloc` or `[]` directly
- ChromaDB always accessed via `PersistentClient` — never in-memory client
- Ollama batch embed via `ollama.embed(model, input=[...])` — never loop `ollama.embeddings()` one at a time
- Recency detection via `RECENCY_KEYWORDS` set in `app.py` — add new keywords there only

## What NOT to do
- Do not use `ollama.embeddings()` in a loop — always use `ollama.embed()` with a batch list
- Do not delete and recreate the ChromaDB collection on every ingest — use incremental upsert
- Do not hardcode column names inside functions — always use `COL_*` constants
- Do not use streaming Ollama calls on Windows — use `stream=False`
- Do not commit `.xlsx`, `.pdf`, or `chroma_db/` — these are gitignored

