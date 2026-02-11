# Complete fix for 404 error - Install dependencies and restart
Write-Host "🔧 MSK Wellness Chatbot - Complete Fix" -ForegroundColor Cyan
Write-Host "=" * 60

# Stop any running backend processes
Write-Host "`n1️⃣ Stopping any running backend..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.Path -like "*backend*" -or $_.CommandLine -like "*uvicorn*" } | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# Navigate to backend
Write-Host "2️⃣ Navigating to backend directory..." -ForegroundColor Yellow
cd backend

# Install all dependencies
Write-Host "3️⃣ Installing ALL dependencies (this may take 2-3 minutes)..." -ForegroundColor Yellow
Write-Host "   Please wait..." -ForegroundColor Gray

python -m pip install -r requirements.txt --quiet

if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Dependencies installed successfully!" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Installation had some warnings (this is usually OK)" -ForegroundColor Yellow
}

# Verify critical imports
Write-Host "`n4️⃣ Verifying installation..." -ForegroundColor Yellow
$testImport = python -c "import structlog, sqlalchemy, fastapi; print('OK')" 2>&1

if ($testImport -like "*OK*") {
    Write-Host "   ✅ All critical modules installed!" -ForegroundColor Green
} else {
    Write-Host "   ❌ Some modules are missing. Run manually:" -ForegroundColor Red
    Write-Host "      cd backend" -ForegroundColor Gray
    Write-Host "      pip install structlog sqlalchemy fastapi uvicorn" -ForegroundColor Gray
    exit 1
}

# Show what will happen
Write-Host "`n" + ("=" * 60) -ForegroundColor Green
Write-Host "✅ Ready to start backend!" -ForegroundColor Green
Write-Host ("=" * 60) -ForegroundColor Green

Write-Host "`n📋 The backend will start with these NEW endpoints:" -ForegroundColor Cyan
Write-Host "   • POST /api/v1/profile - Create user profile" -ForegroundColor White
Write-Host "   • GET  /api/v1/profile/{user_id} - Get profile" -ForegroundColor White
Write-Host "   • POST /api/v1/progress/{user_id} - Record progress" -ForegroundColor White
Write-Host "   • POST /api/v1/upload/report/{user_id} - Upload file" -ForegroundColor White

Write-Host "`n🚀 Starting backend server..." -ForegroundColor Cyan
Write-Host "   URL: http://localhost:8000" -ForegroundColor Gray
Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor Gray
Write-Host "`n   Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ("=" * 60) -ForegroundColor Cyan

Start-Sleep -Seconds 2

# Start the backend
uvicorn app.main:app --reload --port 8000
