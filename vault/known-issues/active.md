# Known Issues — Active

## [RESOLVED] Embedding bottleneck
- **Problem:** `ollama.embeddings()` called one record at a time — 7,475 records took hours
- **Fix:** Switched to `ollama.embed(input=[...])` batch API — 100 texts per call, ~5–6 min total
- **Status:** ✅ Resolved (commit cdc0f25)

## [RESOLVED] Wrong dates on recency queries
- **Problem:** LLM referenced 2020 records when asked for "most recent" — no date sorting
- **Fix:** Sort Excel by `Maint. Plan Date` descending before ingest; store `date_ts` epoch in metadata; re-rank by `date_ts` when recency keywords detected in query
- **Status:** ✅ Resolved (commit 711b46e) — requires re-ingest to populate `date_ts`

## [RESOLVED] Windows asyncio error
- **Problem:** `ConnectionResetError` / `ProactorBasePipeTransport` exception on Windows with streaming Ollama
- **Fix:** `asyncio.WindowsSelectorEventLoopPolicy()` at startup + `stream=False` in all Ollama calls
- **Status:** ✅ Resolved

## [ACTIVE] Response time ~15–25s
- **Problem:** `llama3.2:1b` on CPU takes 15–25s per query — KPI target is ≤5s
- **Workaround:** Use `llama3.2:1b` (not 3b). No GPU acceleration available on current workstation.
- **Future:** Consider GPU-enabled workstation or quantized model

## [ACTIVE] Manual GMES export required
- **Problem:** No automated nightly sync from GMES — engineer must manually export Excel
- **Workaround:** Export when new WOs need to be added; incremental ingest skips existing records
- **Future:** Automate export via GMES API if available
