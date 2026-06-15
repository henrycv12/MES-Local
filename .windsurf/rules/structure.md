# Project Structure Rules

## Where new files go
- New ingestion scripts → root folder, named `ingest_*.py`
- New UI pages or tabs → extend `app.py` (single-file Streamlit app)
- New vault entries → appropriate `vault/` subfolder
- Workflow files → `.windsurf/workflows/`

## Folder purposes
- `./` — Python source files and entry point
- `./chroma_db/` — ChromaDB persistent storage (DO NOT edit manually, gitignored)
- `./vault/` — institutional memory: decisions, config, known issues
- `./.windsurf/rules/` — AI coding conventions for this project
- `./.windsurf/skills/` — task-specific context loaded per session
- `./.windsurf/workflows/` — repeatable procedures (commit, session start, audit)

## What does NOT belong in this repo
- `.xlsx` or `.xls` work order exports (may contain sensitive operational data)
- `.pdf` manuals
- `chroma_db/` vector database (large, regenerated locally)
- `.env` files or credentials
- Any file with employee names, equipment IDs, or production data
