# Copilot Studio Migration Plan

Migrate MES Local from a local Streamlit app to a Microsoft Teams Copilot Studio agent backed by Azure Functions and Azure AI Search.

---

## Current State
- Streamlit UI on local Windows workstation
- ChromaDB local vector store (`./chroma_db/` — 19k WOs)
- Azure OpenAI: `embed-model` (text-embedding-3-small) + `gpt-4o`
- All logic in `app.py`

## Target State
- Copilot Studio agent in Microsoft Teams
- Azure Functions serverless backend (Python)
- Azure AI Search vector store (replaces ChromaDB)
- Same Azure OpenAI deployments reused

---

## Step 1 — Azure AI Search (replaces ChromaDB)
**Effort: Medium | Blocker for everything else**

1. Provision Azure AI Search resource (Free tier = 50MB, enough for 19k WOs)
2. Create index `work-orders` with fields:
   - `id` (string, key)
   - `content` (string, searchable)
   - `embedding` (Collection(Edm.Single), 1536 dims, vector search)
   - `wo_no`, `equipment`, `date`, `line`, `group`, `maint_type` (filterable)
3. Write `migrate_to_search.py` — reads ChromaDB, pushes all 19k docs to AI Search
4. Update `ingest_excel.py` — write to AI Search instead of ChromaDB
5. Test: query AI Search returns same results as ChromaDB

**Files to create:** `migrate_to_search.py`
**Files to modify:** `ingest_excel.py`, `requirements.txt`
**New env vars:** `AZURE_SEARCH_ENDPOINT`, `AZURE_SEARCH_KEY`, `AZURE_SEARCH_INDEX`

---

## Step 2 — Azure Functions API backend
**Effort: Medium**

Create `api/` folder:
```
api/
  function_app.py      # Azure Functions v2 HTTP trigger
  requirements.txt     # openai, azure-search-documents
  host.json
  local.settings.json  # gitignored
```

`POST /query` contract:
```json
Request:  { "question": "...", "history": [{"role":"user","content":"..."}] }
Response: { "answer": "...", "work_orders": [...], "query_used": "..." }
```

Logic mirrors `app.py`: rewrite_query → embed → AI Search → build_messages → GPT-4o

Deploy:
```
func azure functionapp publish mes-local-api
```

---

## Step 3 — Power Platform Custom Connector
**Effort: Low**

1. Export OpenAPI spec from Azure Functions
2. Power Platform → Custom Connectors → New from OpenAPI
3. Auth: API Key (Functions host key)
4. Test: invoke `/query` from connector test panel

---

## Step 4 — Copilot Studio Agent
**Effort: Low-Medium**

1. Create agent in Copilot Studio (copilot.microsoft.com)
2. Add custom connector as a Plugin Action
3. Create topic: "Maintenance Question"
   - Trigger: any input
   - Action: call `/query` with user message + conversation history
   - Response: display `answer` + `work_orders` cards
4. Publish to Teams channel

---

## Decision Required Before Starting

| Question | Options |
|---|---|
| Azure AI Search tier | **Free** (50MB, enough for 19k WOs) or **Basic** ($73/mo, SLA) |
| API auth for Copilot Studio | **Function host key** (simple) or **Azure AD** (more secure) |
| Keep Streamlit running in parallel? | Yes (during transition) or replace immediately |

---

## Sequence
```
Step 1 (AI Search) → Step 2 (Functions API) → Step 3 (Connector) → Step 4 (Copilot Studio)
```
Steps 3 and 4 are short once the API is live. Steps 1–2 are the main work (~2–3 sessions).
