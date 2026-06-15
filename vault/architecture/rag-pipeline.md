# RAG Pipeline Architecture

## Ingest pipeline
```
GMES Export (.xlsx)
  → pandas.read_excel()
  → Sort by Maint. Plan Date DESC
  → row_to_text() → formatted text block per WO
  → Check existing IDs in ChromaDB (skip duplicates)
  → ollama.embed(model="nomic-embed-text", input=batch[100])
  → chromadb.add(documents, embeddings, ids, metadatas)
     metadata: wo_no, date, date_ts, equipment, equip_id, line, group, maint_type, source
```

## Query pipeline
```
User types question in Streamlit
  → ollama.embeddings(model="nomic-embed-text", prompt=query)
  → is_recency_query(query)?
      YES → fetch top_k * 3, sort by date_ts DESC, take top_k
      NO  → fetch top_k directly
  → build_prompt(query, items) → structured prompt with WO context
  → ollama.chat(model="llama3.2:1b", stream=False)
  → Display answer + expandable "Work orders referenced" section
```

## ChromaDB collection schema
- **Collection:** `work_orders`
- **ID format:** `WO_{filename}_{wo_no}_{row_idx}`
- **Document:** Full formatted text of the work order
- **Metadata fields:** `source`, `wo_no`, `date`, `date_ts`, `equipment`, `equip_id`, `line`, `group`, `maint_type`
