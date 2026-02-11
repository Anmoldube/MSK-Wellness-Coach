# Diagnostic script to check what's wrong
Write-Host "🔍 Diagnosing the 404 Error..." -ForegroundColor Cyan
Write-Host "=" * 60

# Check Python
Write-Host "`n1️⃣ Checking Python..." -ForegroundColor Yellow
python --version
$pythonPath = (Get-Command python).Path
Write-Host "   Python location: $pythonPath" -ForegroundColor Gray

# Check if backend is running
Write-Host "`n2️⃣ Checking if backend is running..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/health" -TimeoutSec 2
    Write-Host "   ✅ Backend is running!" -ForegroundColor Green
    Write-Host "   Response: $($response | ConvertTo-Json)" -ForegroundColor Gray
} catch {
    Write-Host "   ❌ Backend is NOT running!" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Gray
}

# Check installed packages
Write-Host "`n3️⃣ Checking installed packages..." -ForegroundColor Yellow
$packages = @("fastapi", "uvicorn", "sqlalchemy", "structlog", "pydantic", "pydantic-settings")

cd backend

foreach ($pkg in $packages) {
    $installed = python -c "import $pkg; print($pkg.__version__)" 2>&1
    if ($installed -notlike "*Error*" -and $installed -notlike "*No module*") {
        Write-Host "   ✅ $pkg : $installed" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $pkg : NOT INSTALLED" -ForegroundColor Red
    }
}

# Check if files exist
Write-Host "`n4️⃣ Checking files..." -ForegroundColor Yellow
$files = @(
    "app/api/endpoints/__init__.py",
    "app/api/endpoints/profile.py",
    "app/api/endpoints/progress.py",
    "app/api/endpoints/upload.py"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "   ✅ $file exists" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $file MISSING" -ForegroundColor Red
    }
}

# Check __init__.py content
Write-Host "`n5️⃣ Checking __init__.py exports..." -ForegroundColor Yellow
$initContent = Get-Content "app/api/endpoints/__init__.py" -Raw
if ($initContent -like "*profile*" -and $initContent -like "*progress*" -and $initContent -like "*upload*") {
    Write-Host "   ✅ __init__.py exports new endpoints!" -ForegroundColor Green
} else {
    Write-Host "   ❌ __init__.py does NOT export new endpoints!" -ForegroundColor Red
    Write-Host "   Content:" -ForegroundColor Gray
    Write-Host $initContent -ForegroundColor Gray
}

# Try to import
Write-Host "`n6️⃣ Testing imports..." -ForegroundColor Yellow
$importTest = python -c "from app.api.endpoints import profile, progress, upload; print('SUCCESS')" 2>&1
if ($importTest -like "*SUCCESS*") {
    Write-Host "   ✅ All endpoints can be imported!" -ForegroundColor Green
} else {
    Write-Host "   ❌ Cannot import endpoints!" -ForegroundColor Red
    Write-Host "   Error:" -ForegroundColor Gray
    Write-Host $importTest -ForegroundColor Gray
}

Write-Host "`n" + ("=" * 60) -ForegroundColor Cyan
Write-Host "🎯 RECOMMENDATION:" -ForegroundColor Cyan
Write-Host ("=" * 60) -ForegroundColor Cyan

if ($importTest -like "*SUCCESS*") {
    Write-Host "✅ Everything looks good!" -ForegroundColor Green
    Write-Host "`nThe issue is likely that your backend wasn't restarted." -ForegroundColor Yellow
    Write-Host "`nNext steps:" -ForegroundColor Cyan
    Write-Host "1. Stop the backend (Ctrl+C)" -ForegroundColor White
    Write-Host "2. Run: .\FIX_404_COMPLETE.ps1" -ForegroundColor White
} else {
    Write-Host "❌ Dependencies are missing!" -ForegroundColor Red
    Write-Host "`nNext steps:" -ForegroundColor Cyan
    Write-Host "1. Run: .\FIX_404_COMPLETE.ps1" -ForegroundColor White
    Write-Host "   This will install everything and restart" -ForegroundColor Gray
}

Write-Host "`n"
