# OneDrive Sync Feature

Add a "Sync from OneDrive" button in the React frontend that triggers migration of new GMES export files from OneDrive to Azure AI Search.

## Architecture

**Deploy app to cloud PC (recommended - no IT action needed):**
- Deploy the entire stack (Next.js + migration script) to the cloud PC where OneDrive files are located
- Files are local to the app execution environment
- User accesses the web UI via browser from local PC
- React button → Next.js API route → Python migration script (local files) → Azure AI Search
- No file sharing between machines required

## Implementation Steps

### 1. Deploy app to cloud PC
- Clone/push the GMES Agent repo to the cloud PC
- Install Node.js and Python on cloud PC
- Install dependencies: `npm install` in `frontend/`, `pip install -r requirements.txt` at root
- Configure `.env` and `frontend/.env.local` with Azure credentials on cloud PC
- Run `npm run dev` from `frontend/` on cloud PC
- Access the app from local PC browser via cloud PC's IP/hostname

### 2. Create Next.js API route (`frontend/app/api/sync-onedrive/route.ts`)
- POST endpoint that:
  - Scans the local OneDrive folder `C:\Users\h.colmenaresvilchez\OneDrive - LG전자\LGE Support\GMES` for `.xlsx`, `.xls`, `.csv`, `.bak` files
  - Filters out files already processed (check against an archive folder or log)
  - If new files found, calls `migrate_to_search.py` with the file paths
  - After successful migration, moves files to `GMES/Archive/` subfolder
  - Returns progress updates (file count, status, errors)
- Use `child_process.exec` or `spawn` to run Python script synchronously
- Stream output back to frontend for progress display

### 3. Modify `migrate_to_search.py`
- Add `--file` argument to accept specific file path(s) instead of scanning current directory
- Keep existing `--recreate` argument
- Add support for processing only specified files (not all files in folder)

### 4. Add "Sync from OneDrive" button to React UI
- Add button to `nav.tsx` (next to Chat/Analytics links)
- Button triggers POST to `/api/sync-onedrive`
- Show loading state with progress indicator
- Display success/error message after completion
- Use existing theme colors for consistent styling

### 5. Add archive folder logic
- Create `GMES/Archive/` subfolder if it doesn't exist
- After successful migration, move processed files to archive
- Use timestamp in archive filename to prevent conflicts

## OneDrive Folder Structure

```
C:\Users\h.colmenaresvilchez\OneDrive - LG전자\LGE Support\GMES\
  ├── Excel_Export_2024-06-19.xlsx  (new file to process)
  ├── Excel_Export_2024-06-18.xlsx  (already processed)
  └── Archive\
      ├── Excel_Export_2024-06-18_20240619_120000.xlsx
      └── ...
```

## Error Handling

- Handle cases where OneDrive folder doesn't exist
- Handle file permission errors
- Handle migration script failures
- Return detailed error messages to frontend
- Log all operations for debugging
