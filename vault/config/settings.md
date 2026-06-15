# System Configuration

## Active settings

| Setting | Value |
|---|---|
| LLM model | `llama3.2:1b` (default), `llama3.2:3b` (quality) |
| Embedding model | `nomic-embed-text` |
| ChromaDB path | `./chroma_db/` |
| Collection name | `work_orders` |
| Top-K | 6 (default), adjustable 3–15 in sidebar |
| Embed batch size | 100 texts per `ollama.embed()` call |
| DB insert batch | 500 records per `ChromaDB.add()` call |
| Max text per record | 1,500 characters (truncated before embedding) |

## Excel column mapping

| Constant | Excel Column |
|---|---|
| `COL_NO` | `No` |
| `COL_DATE` | `Maint. Plan Date` |
| `COL_TYPE` | `Maint. Type` |
| `COL_LINE` | `Line` |
| `COL_GROUP` | `Group` |
| `COL_EQUIP_ID` | `ID` |
| `COL_EQUIP` | `Equipment` |
| `COL_TITLE` | `Maint. Title` |
| `COL_CAUSE` | `Cause of failure(reason)` |
| `COL_RESOLUTION` | `Resolution & Result` |
| `COL_PREVENTION` | `Measures to Prevent Recurrence` |
| `COL_TECHNICIAN` | `Result Registrant` |
| `COL_DURATION` | `Maint. Time (Min)` |
| `COL_DOWNTIME` | `Stop Time (Min)` |
| `COL_PARTS` | `Spare Parts` |
| `COL_CATEGORY` | `Categorization Type` |
| `COL_SYMPTOMS` | `Failure symptoms` |
| `COL_FAILURE_CAUSE` | `Failure Cause` |
| `COL_ACTION` | `Action Info` |
