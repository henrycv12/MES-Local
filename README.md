# GMES Agent — Maintenance Agent

**LG Electronics — TN Production Engineering Team**

A fully local AI assistant that answers maintenance questions from 7 years of GMES work order history using Azure OpenAI + ChromaDB.

## How it works

1. Export work orders from GMES as `.xlsx`
2. Run `python ingest_excel.py` — indexes records into a local vector database (incremental, skips already-indexed)
3. Run `streamlit run app.py` — launch the chat interface
4. Ask questions — the agent retrieves similar past work orders and explains what was done

## Quick start

```bash
# 1. Pull Ollama models (one-time)
ollama pull nomic-embed-text
ollama pull llama3.2:1b

# 2. Install dependencies
pip install -r requirements.txt

# 3. Drop your GMES .xlsx export in this folder, then:
python ingest_excel.py

# 4. Launch
streamlit run app.py
```

## Project structure

| File/Folder | Purpose |
|---|---|
| `app.py` | Streamlit chat UI — query, retrieve, answer |
| `ingest_excel.py` | Excel ingestion — embed and store work orders |
| `requirements.txt` | Python dependencies |
| `CONTEXT.md` | Current project status — always up to date |
| `AGENTS.md` | Architecture and module map |
| `vault/` | Institutional memory: config, decisions, known issues |
| `.devin/` | AI coding rules, skills, and workflow procedures |

## Stack

| Component | Tool |
|---|---|
| LLM | Ollama `llama3.2:1b` (local CPU) |
| Embeddings | Azure OpenAI `text-embedding-3-small` (fast cloud) |
| Vector DB | ChromaDB (local persistent) |
| UI | Streamlit |
| Data source | GMES export (`.xlsx` or `.csv`) |

## Maintained by

TN PE Team — henrycv12

