$PSScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $PSScriptRoot

# Ask what you are changing today
$comment = Read-Host "Describe your major changes (for Version Control)"
Write-Host "--- Automated Build & Backup: PM Parts Room APP ---" -ForegroundColor Cyan

# 1. Capture the change in Git (Local Backup)
Write-Host "Step 1: Committing changes to Git..." -ForegroundColor Gray
git add .
git commit -m "$comment"
Write-Host "Step 1.1: Pushing changes to Remote..." -ForegroundColor Gray
git push

# 1.5 Update Entropy.json timestamp (if exists)
$entropyPath = Join-Path $PSScriptRoot "powerapp_extract\Entropy\Entropy.json"
if (Test-Path $entropyPath) {
    $txt = Get-Content $entropyPath -Raw
    $now = (Get-Date).ToUniversalTime().ToString("MM/dd/yyyy HH:mm:ss")
    $txt = $txt -replace '"HeaderLastSavedDateTimeUTC": ".*?"', "`"HeaderLastSavedDateTimeUTC`": `"$now`""
    Set-Content $entropyPath $txt -NoNewline
}

# 2. Pack the YAML back into the MSAPP file
Write-Host "Step 2: Packing YAML..." -ForegroundColor Gray
pac canvas pack --sources "powerapp_extract" --msapp "PM_Parts_Room_With_Chat.msapp"

# 3. Upload to Power Platform environment
Write-Host "Step 3: Uploading to Power Platform..." -ForegroundColor Gray
pac canvas publish --environment 5069cde4-642a-45c0-8094-d0c2dec10be3 --app-name "PM Parts Room APP" --msapp "PM_Parts_Room_With_Chat.msapp"

Write-Host "SUCCESS: Changes are LIVE and backed up in Git." -ForegroundColor Green
