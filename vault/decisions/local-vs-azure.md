# Decision: Local Stack vs Azure

## Context
Original project scope (2026 DX Project presentation) called for:
- Azure SQL Database (work order storage)
- Azure AI Search (semantic retrieval)
- Azure OpenAI GPT-4 (reasoning)
- Copilot Studio on Microsoft Teams (UI)

## Decision
Replace the entire Azure stack with a fully local, offline equivalent.

## Rationale
- Azure stack has ongoing cloud costs (estimated $314K/year labor savings offset by licensing)
- PE team workstation has no reliable internet dependency requirement
- Local stack achieves same functional goals: semantic search + LLM reasoning over work orders
- No data leaves the building — operational work order data stays on-premise
- Faster iteration: no cloud provisioning, no SSO/tenant configuration

## Local equivalent
| Azure | Local |
|---|---|
| Azure SQL Database | Excel export from GMES (manual, periodic) |
| Azure AI Search | ChromaDB + nomic-embed-text |
| Azure OpenAI GPT-4 | Ollama llama3.2:1b/3b |
| Copilot Studio / Teams | Streamlit web app |

## Trade-offs accepted
- No automatic nightly sync from GMES (manual Excel export required)
- LLM quality lower than GPT-4 (mitigated by good retrieval + prompting)
- Single-user local app vs multi-user Teams bot

