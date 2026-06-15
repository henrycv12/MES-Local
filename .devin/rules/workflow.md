# Workflow Rules

## Never touch without review
- `chroma_db/` — never delete unless doing a forced full re-ingest
- `COL_*` constants in `ingest_excel.py` — changing these breaks ingestion mapping
- `WO_COLLECTION` name — changing this orphans the existing vector DB

## Always test after changing
- After any change to `ingest_excel.py`: run a small test ingest and confirm record count
- After any change to `app.py`: restart Streamlit and run at least one query
- After adding RECENCY_KEYWORDS: test a "most recent" query to confirm re-ranking works

## Branch strategy
- `main` only — direct commits, no feature branches (small team, single developer)

## Who to notify
- TN PE Team lead before changing column mappings (impacts re-ingestion of all data)
- All PE engineers before changing the Ollama model default (affects response quality)

## Re-ingest policy
- Only re-ingest when: new Excel export with additional WOs, or column mapping changed
- Incremental ingest is safe to run anytime — it skips already-indexed records
- Full rebuild: delete `chroma_db/` then run `python ingest_excel.py`

