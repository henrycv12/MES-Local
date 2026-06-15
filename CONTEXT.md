# Project Context

## What this project does
MES Local is a fully offline AI maintenance assistant for LG Electronics TN Production Engineering. It indexes 7-year historical work order exports from GMES (EMS system) into a local vector database and answers natural-language troubleshooting questions from PE engineers — identifying past failures, root causes, and resolutions without any cloud dependency.

## Current status
- **Working:** Work order ingestion from Excel (incremental), ChromaDB vector search, Streamlit chat UI, Ollama LLM answering, recency-aware retrieval, batch embedding
- **In progress:** Testing with real work order data; response quality validation
- **Broken:** Nothing known
- **Pending:** Export summary feature, PM checklist generator, recurring failures dashboard

## Tech stack
- **LLM:** Ollama `llama3.2:1b` (local, CPU) — switchable to `llama3.2:3b` via sidebar
- **Embeddings:** `nomic-embed-text` via `ollama.embed()` batch API
- **Vector DB:** ChromaDB (persistent local, `./chroma_db/`)
- **UI:** Streamlit
- **Data source:** GMES Excel export (`.xlsx`) — 7,475+ work orders
- **Python:** 3.13.3 on Windows

## Key file map
- **Entry point:** `app.py` — Streamlit chat UI
- **Ingestion:** `ingest_excel.py` — reads Excel, embeds, stores in ChromaDB (incremental)
- **Legacy:** `ingest.py` — PDF ingestion (FIKE manual, not in active use)
- **DB:** `./chroma_db/` — persistent vector store (gitignored)
- **Data:** `Excel_Export_[...].xlsx` — GMES work order export (gitignored)

## Known issues
- First full ingest of 7,475 records takes ~5–6 minutes (batch embedding)
- Ollama `llama3.2:1b` response time ~15–25s; `3b` ~45–60s
- ChromaDB `get()` with offset used to detect existing IDs — may be slow on very large collections
- Windows asyncio ProactorEventLoop bug mitigated with `WindowsSelectorEventLoopPolicy`
