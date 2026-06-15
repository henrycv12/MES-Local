# Architecture

## Overview
MES Local is a Retrieval-Augmented Generation (RAG) system. Work order records are embedded into a local vector DB at ingest time. At query time, the user's question is embedded, the top-K most semantically similar work orders are retrieved, and a local LLM generates an answer grounded in those records.

## Module responsibilities

| File | Role |
|---|---|
| `app.py` | Streamlit UI, query embedding, ChromaDB retrieval, prompt building, Ollama LLM call |
| `ingest_excel.py` | Reads Excel exports, sorts by date, embeds in batches, stores incrementally in ChromaDB |
| `ingest.py` | Legacy PDF ingestion (FIKE manual) — not actively used |

## Data flow

```
GMES Export (.xlsx or .csv)
    → ingest_excel.py
        → pd.read_excel() / pd.read_csv() → sort by date desc
        → Azure OpenAI embed(batch=500) → embeddings[]  [fallback: ollama.embed()]
        → ChromaDB collection "work_orders" (incremental upsert)

User query (Streamlit)
    → Azure OpenAI embed(query) → query vector  [fallback: ollama.embeddings()]
    → ChromaDB.query(top_k) → matching WO chunks
    → [recency re-rank if "recent/latest/last" in query]
    → build_prompt(query, items)
    → ollama.chat(llama3.2:1b) → answer text
    → Streamlit display + expandable source WOs
```

## External dependencies
- **Ollama** — must be running locally (`ollama serve`). Models needed:
  - `llama3.2:1b` (default LLM)
  - `llama3.2:3b` (optional, better quality)
  - `nomic-embed-text` (fallback embeddings only, if no `.env`)
- **Azure OpenAI** — `text-embedding-3-small` via `embed-model` deployment. Credentials in `.env` (gitignored)
- **ChromaDB** — file-based, no server needed, stored in `./chroma_db/`
- **GMES** — source of work order exports (manual export, `.xlsx` or `.csv`)

## Key constants (app.py)
- `WO_COLLECTION = "work_orders"` — ChromaDB collection name
- `EMBED_MODEL = "nomic-embed-text"` — Ollama fallback only
- `OLLAMA_MODEL = "llama3.2:1b"`
- `TOP_K = 6` — work orders retrieved per query
- `RECENCY_KEYWORDS` — triggers date re-ranking when matched in query
- `USE_AZURE` — auto-set from `.env`; switches embed provider

## Key constants (ingest_excel.py)
- `EMBED_BATCH = 500` — texts per embed API call
- `BATCH_SIZE = 500` — records per ChromaDB add() call
- `USE_AZURE` — auto-set from `.env`; switches embed provider
- Sort: `Maint. Plan Date` descending before embedding

## Deployment target
Local Windows machine (PE team workstation). Requires internet for Azure embed API calls.
Run with:
```
streamlit run app.py
```

