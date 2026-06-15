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
GMES Export (.xlsx)
    → ingest_excel.py
        → pd.read_excel() → sort by date desc
        → ollama.embed(batch=100) → embeddings[]
        → ChromaDB collection "work_orders" (incremental upsert)

User query (Streamlit)
    → ollama.embeddings(query) → query vector
    → ChromaDB.query(top_k) → matching WO chunks
    → [recency re-rank if "recent/latest/last" in query]
    → build_prompt(query, items)
    → ollama.chat(llama3.2:1b) → answer text
    → Streamlit display + expandable source WOs
```

## External dependencies
- **Ollama** — must be running locally (`ollama serve`). Models needed:
  - `nomic-embed-text` (embeddings)
  - `llama3.2:1b` (default LLM)
  - `llama3.2:3b` (optional, better quality)
- **ChromaDB** — file-based, no server needed, stored in `./chroma_db/`
- **GMES** — source of work order Excel exports (manual export, not automated)

## Key constants (app.py)
- `WO_COLLECTION = "work_orders"` — ChromaDB collection name
- `EMBED_MODEL = "nomic-embed-text"`
- `OLLAMA_MODEL = "llama3.2:1b"`
- `TOP_K = 6` — work orders retrieved per query
- `RECENCY_KEYWORDS` — triggers date re-ranking when matched in query

## Key constants (ingest_excel.py)
- `EMBED_BATCH = 100` — texts per ollama.embed() call
- `BATCH_SIZE = 500` — records per ChromaDB add() call
- Sort: `Maint. Plan Date` descending before embedding

## Deployment target
Local Windows machine (PE team workstation). No internet required after initial model pull. Run with:
```
streamlit run app.py
```

