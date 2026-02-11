# Quick install and restart script
Write-Host "🔧 Installing dependencies..." -ForegroundColor Cyan

cd backend

# Install all requirements
pip install -r requirements.txt

Write-Host ""
Write-Host "✅ Dependencies installed!" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Starting backend..." -ForegroundColor Cyan
Write-Host ""

# Start backend
uvicorn app.main:app --reload --port 8000
