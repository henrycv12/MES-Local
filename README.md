# GMES Agent — Maintenance Agent

**LG Electronics — TN Production Engineering Team**

An AI assistant that answers maintenance questions from GMES work order history using Azure OpenAI + Azure AI Search. Two interfaces available: React frontend (local development) and Copilot Studio (Power Platform integration).

## How it works

1. Export work orders from GMES as `.xlsx` or `.csv`
2. Run `python ingest_excel.py` — indexes records into Azure AI Search (incremental, skips already-indexed)
3. Ask questions via either interface:
   - **React Frontend**: Local Next.js app with direct Azure AI calls
   - **Copilot Studio**: Via Power Automate → Azure Functions backend
4. The agent retrieves similar past work orders via semantic search and explains what was done

## Quick start

### React Frontend (local development)

```bash
# 1. Install frontend dependencies
cd frontend
npm install

# 2. Configure environment variables
# Copy .env.local.example to .env.local and fill in Azure credentials:
# AZURE_OPENAI_API_KEY=
# AZURE_OPENAI_ENDPOINT=
# AZURE_OPENAI_LLM_DEPLOYMENT=gpt-4o
# AZURE_OPENAI_REWRITE_DEPLOYMENT=gpt-4o
# AZURE_OPENAI_EMBED_DEPLOYMENT=embed-model
# AZURE_SEARCH_ENDPOINT=
# AZURE_SEARCH_KEY=
# AZURE_SEARCH_INDEX=work-orders

# 3. Start development server
npm run dev
# Open http://localhost:3000
```

### Data ingestion (shared by both interfaces)

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Configure Azure credentials in .env
# AZURE_OPENAI_API_KEY=
# AZURE_OPENAI_ENDPOINT=
# AZURE_OPENAI_EMBED_DEPLOYMENT=embed-model
# AZURE_SEARCH_ENDPOINT=
# AZURE_SEARCH_KEY=
# AZURE_SEARCH_INDEX=work-orders

# 3. Drop your GMES .xlsx export in this folder, then:
python ingest_excel.py
```

### Azure Functions backend (for Copilot Studio)

```bash
cd api
func start
# Or deploy to Azure:
func azure functionapp publish gmes-agent-api --python
```

## Project structure

| File/Folder | Purpose |
|---|---|
| `api/function_app.py` | Azure Functions HTTP trigger — query logic for Copilot Studio |
| `api/openapi.json` | OpenAPI spec for Power Automate custom connector |
| `ingest_excel.py` | Excel ingestion — embed and store work orders in Azure AI Search |
| `frontend/` | Next.js 14 React frontend — chat UI, API routes, localStorage history |
| `frontend/app/api/query/route.ts` | Next.js API route — replicates Azure Functions query logic |
| `frontend/components/` | React components: GmesThread, ChatSidebar, WoCards, WoModal |
| `mq.yaml` / `fb.yaml` | Copilot Studio topic YAMLs (Maintenance Query, Fallback) |
| `AGENTS.md` | Full architecture and module map |
| `vault/` | Institutional memory: config, decisions, known issues |
| `.devin/` | AI coding rules, skills, and workflow procedures |

## Stack

| Component | Tool |
|---|---|
| LLM | Azure OpenAI `gpt-4o` |
| Embeddings | Azure OpenAI `text-embedding-3-small` |
| Vector Search | Azure AI Search (semantic ranking) |
| History Storage | Azure Table Storage (Copilot Studio) / localStorage (React) |
| Frontend UI | Next.js 14 + React + `@assistant-ui/react` |
| Backend API | Azure Functions (Python) |
| Copilot Studio | Power Platform integration via Power Automate |
| Data source | GMES export (`.xlsx` or `.csv`) |

## Key features

- **Semantic search**: Retrieves top-K relevant work orders per query
- **Query intelligence**: Detects recency, count, and time-windowed queries automatically
- **Grounded answers**: System prompt enforces strict grounding to retrieved records only
- **Multi-conversation history**: localStorage persistence in React frontend
- **Work order citations**: Clickable cards with full WO modal display
- **Markdown formatting**: Tables, headers, code blocks styled for readability
- **Token optimization**: Truncated WO content, reduced history window for cost efficiency

## Maintained by

TN PE Team — henrycv12

