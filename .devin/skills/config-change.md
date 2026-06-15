---
description: Triggered when changing models, column mappings, or system constants
---

## Config locations

| Setting | File | Constant |
|---|---|---|
| LLM model | `app.py` | `OLLAMA_MODEL` |
| Embedding model | `app.py` and `ingest_excel.py` | `EMBED_MODEL` |
| Top-K results | `app.py` | `TOP_K` |
| ChromaDB path | `app.py` and `ingest_excel.py` | `CHROMA_DIR` |
| Collection name | `app.py` and `ingest_excel.py` | `WO_COLLECTION` |
| Excel column names | `ingest_excel.py` | `COL_*` constants |
| Recency trigger words | `app.py` | `RECENCY_KEYWORDS` |
| Embed batch size | `ingest_excel.py` | `EMBED_BATCH` |
| DB insert batch size | `ingest_excel.py` | `BATCH_SIZE` |

## Impact of changes
- Changing `EMBED_MODEL` → **must delete `chroma_db/` and re-ingest** (embedding space changes)
- Changing `COL_*` → **must re-ingest** (text format of stored records changes)
- Changing `OLLAMA_MODEL` → no re-ingest needed, only affects answer quality/speed
- Changing `TOP_K` → no re-ingest needed, only affects context window size
- Changing `WO_COLLECTION` name → orphans existing DB, must re-ingest

