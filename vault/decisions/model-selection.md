# Decision: Model Selection

## LLM
- **`llama3.2:1b`** — default. ~15–25s response on CPU. Sufficient for structured WO retrieval answers.
- **`llama3.2:3b`** — optional via sidebar. ~45–60s. Better reasoning for complex queries.
- **Ruled out:** `llama3` (8B) — maxed RAM on PE workstation during testing.

## Embedding model
- **`nomic-embed-text`** — chosen for strong semantic similarity on technical/maintenance text.
- Runs via Ollama, no separate Python library needed (avoids `sentence-transformers` which is incompatible with Python 3.13).

## Why not sentence-transformers
- Incompatible with Python 3.13 (scipy dependency fails to build)
- Would require separate model download outside Ollama
- `nomic-embed-text` via Ollama is equivalent quality for this use case
