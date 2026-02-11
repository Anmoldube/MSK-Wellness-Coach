# SQLite Data Viewing Guide
Write-Host "=== How to View SQLite Data ===" -ForegroundColor Cyan
Write-Host ""

$dbPath = "backend\msk_chatbot.db"

Write-Host "Your database is located at:" -ForegroundColor Yellow
Write-Host "  $((Get-Item $dbPath).FullName)" -ForegroundColor Green
Write-Host ""

Write-Host "Option 1: DB Browser for SQLite (GUI - EASIEST)" -ForegroundColor Cyan
Write-Host "  1. Download from: https://sqlitebrowser.org/dl/" -ForegroundColor Gray
Write-Host "  2. Install it" -ForegroundColor Gray
Write-Host "  3. Open DB Browser" -ForegroundColor Gray
Write-Host "  4. File > Open Database > Select: $dbPath" -ForegroundColor Gray
Write-Host "  5. Click 'Browse Data' tab to see all your tables" -ForegroundColor Gray
Write-Host ""

Write-Host "Option 2: VS Code Extension (if using VS Code)" -ForegroundColor Cyan
Write-Host "  1. Install extension: 'SQLite' by alexcvzz" -ForegroundColor Gray
Write-Host "  2. Right-click on $dbPath" -ForegroundColor Gray
Write-Host "  3. Select 'Open Database'" -ForegroundColor Gray
Write-Host "  4. View tables in SQLite Explorer panel" -ForegroundColor Gray
Write-Host ""

Write-Host "Option 3: Command Line (SQLite CLI)" -ForegroundColor Cyan
Write-Host "  Download sqlite3.exe from: https://www.sqlite.org/download.html" -ForegroundColor Gray
Write-Host "  Then run:" -ForegroundColor Gray
Write-Host "    sqlite3 $dbPath" -ForegroundColor Yellow
Write-Host "    .tables" -ForegroundColor Yellow
Write-Host "    SELECT * FROM users;" -ForegroundColor Yellow
Write-Host ""

Write-Host "Option 4: Python Script (I can create one for you)" -ForegroundColor Cyan
Write-Host "  I already created 'tmp_rovodev_show_data.py'" -ForegroundColor Gray
Write-Host "  Run: python tmp_rovodev_show_data.py" -ForegroundColor Yellow
Write-Host ""

Write-Host "Option 5: Web-based SQLite Viewer" -ForegroundColor Cyan
Write-Host "  1. Go to: https://inloop.github.io/sqlite-viewer/" -ForegroundColor Gray
Write-Host "  2. Drag and drop: $dbPath" -ForegroundColor Gray
Write-Host "  3. Browse your data in browser" -ForegroundColor Gray
Write-Host ""

Write-Host "=== Quick Data Preview ===" -ForegroundColor Cyan
Write-Host "Running Python script to show your data now..." -ForegroundColor Yellow
Write-Host ""
