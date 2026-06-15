# Project Context

## What this project does
MES Local is a fully offline AI maintenance assistant for LG Electronics TN Production Engineering. It indexes 7-year historical work order exports from GMES (EMS system) into a local vector database and answers natural-language troubleshooting questions from PE engineers — identifying past failures, root causes, and resolutions without any cloud dependency.

## Current status
- **Working:** Work order ingestion from Excel/CSV (incremental), ChromaDB vector search, Streamlit chat UI, Ollama LLM answering, recency-aware retrieval, Azure OpenAI batch embedding
- **In progress:** Testing with real work order data; response quality validation
- **Broken:** Nothing known
- **Pending:** Export summary feature, PM checklist generator, recurring failures dashboard

## Tech stack
- **LLM:** Ollama `llama3.2:1b` (local, CPU) — switchable to `llama3.2:3b` via sidebar
- **Embeddings:** Azure OpenAI `text-embedding-3-small` (auto-detected from `.env`; falls back to Ollama `nomic-embed-text`)
- **Vector DB:** ChromaDB (persistent local, `./chroma_db/`)
- **UI:** Streamlit
- **Data source:** GMES export (`.xlsx` or `.csv`) — 19,000+ work orders
- **Python:** 3.13.3 on Windows

## Key file map
- **Entry point:** `app.py` — Streamlit chat UI
- **Ingestion:** `ingest_excel.py` — reads Excel/CSV, embeds via Azure OpenAI, stores in ChromaDB (incremental)
- **Config:** `.env` — Azure OpenAI credentials (gitignored)
- **Legacy:** `ingest.py` — PDF ingestion (FIKE manual, not in active use)
- **DB:** `./chroma_db/` — persistent vector store (gitignored)
- **Data:** `Excel_Export_[...].xlsx/.csv` — GMES work order export (gitignored)

## Known issues
- Full ingest of 19,000+ records takes ~4–5 min with Azure OpenAI; ~45 min with Ollama CPU fallback
- Ollama `llama3.2:1b` response time ~15–25s; `3b` ~45–60s
- ChromaDB `get()` with offset used to detect existing IDs — may be slow on very large collections
- Windows asyncio ProactorEventLoop bug mitigated with `WindowsSelectorEventLoopPolicy`
- Azure OpenAI key stored in `.env` — must be rotated if exposed; never commit `.env`

