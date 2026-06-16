---
name: deployment
description: Triggered when deploying or setting up GMES Agent on a new machine
---

## Requirements
- Windows 10/11
- Python 3.10+ (tested on 3.13.3)
- [Ollama](https://ollama.com) installed and running

## Setup steps
1. Clone repo: `git clone https://github.com/henrycv12/GMES-Agent`
2. Install dependencies: `pip install -r requirements.txt`
3. Pull Ollama models:
   ```
   ollama pull nomic-embed-text
   ollama pull llama3.2:1b
   ```
4. Drop GMES Excel export (`.xlsx`) into the project folder
5. Run ingest: `python ingest_excel.py`
6. Launch app: `streamlit run app.py`

## Notes
- `chroma_db/` is created automatically on first ingest — do not copy between machines
- Each machine must run its own ingest from the same Excel export
- No internet connection required after setup
- Ollama must be running (`ollama serve`) before starting the app
