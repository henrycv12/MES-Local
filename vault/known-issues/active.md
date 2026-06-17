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

## [RESOLVED] Response time ~15–25s
- **Problem:** `llama3.2:1b` on CPU took 15–25s per query — KPI target is ≤5s
- **Fix:** Switched to Azure OpenAI `gpt-4o` exclusively; Ollama removed from codebase
- **Status:** ✅ Resolved — response time now ~2–5s

## [ACTIVE] Azure AI Search storage limit — cannot index full database
- **Problem:** Azure AI Search free tier is capped at 50MB. Current index uses 11MB with only 10% of the WO database loaded. Full database (~110MB) exceeds the limit.
- **Options (must stay within Microsoft tenant — external vector DBs not allowed):**
  - **A — Upgrade to Basic tier**: ~$73/month, 2GB storage. No code changes.
  - **B — Recency split (free)**: Index only last 12–18 months in Azure AI Search (Copilot Studio path); keep full history in local ChromaDB (Streamlit path).
- **Workaround:** Do not ingest more than ~40% of the database until resolved.
- **Status:** ⛔ BLOCKED — architecture decision pending

## [ACTIVE] Manual GMES export required
- **Problem:** No automated nightly sync from GMES — engineer must manually export Excel
- **Workaround:** Export when new WOs need to be added; incremental ingest skips existing records
- **Blocker:** Requires HQ GMES API access — not an internal IT decision

