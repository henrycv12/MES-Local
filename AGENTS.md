# Architecture

## Overview
GMES Agent is a Retrieval-Augmented Generation (RAG) system. Work order records are embedded into a local vector DB at ingest time. At query time, the user's question is embedded, the top-K most semantically similar work orders are retrieved, and a local LLM generates an answer grounded in those records.

## Module responsibilities

| File | Role |
|---|---|
| `app.py` | Streamlit UI, query rewriting, query embedding, ChromaDB retrieval, prompt building, Azure OpenAI LLM call (Ollama fallback) |
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
    → Azure OpenAI embed(query) → query vector  [fallback: ollama.embed()]
    → ChromaDB.query(top_k) → matching WO chunks
    → [recency re-rank if "recent/latest/last" in query]
    → build_messages(query, items, history)
    → Azure OpenAI gpt-4o chat → answer text  [fallback: ollama.chat(llama3.2:1b)]
    → Streamlit display + expandable source WOs
```

## External dependencies
- **Azure OpenAI** — primary provider for both embeddings and LLM. Credentials in `.env` (gitignored)
  - `text-embedding-3-small` via `embed-model` deployment
  - `gpt-4o` via `gpt-4o` deployment
- **Ollama** — fallback only if `.env` is missing (`ollama serve` must be running)
  - `llama3.2:1b` (fallback LLM)
  - `nomic-embed-text` (fallback embeddings)
- **ChromaDB** — file-based, no server needed, stored in `./chroma_db/`
- **GMES** — source of work order exports (manual export, `.xlsx` or `.csv`)

## Key constants (app.py)
- `WO_COLLECTION = "work_orders"` — ChromaDB collection name
- `EMBED_MODEL = "nomic-embed-text"` — Ollama fallback only
- `AZURE_LLM_DEPLOY = "gpt-4o"` — Azure OpenAI chat deployment
- `OLLAMA_MODEL = "llama3.2:1b"` — fallback only
- `TOP_K = 15` — work orders retrieved per query
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

