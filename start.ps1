# PowerShell startup script for Windows
Write-Host "🚀 Starting MSK Wellness AI Chatbot" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
try {
    docker info | Out-Null
    Write-Host "✅ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
    exit 1
}
Write-Host ""

# Check if .env exists
if (-not (Test-Path .env)) {
    Write-Host "⚠️  .env file not found. Creating from template..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "✅ .env file created" -ForegroundColor Green
}

Write-Host "📦 Starting services with Docker Compose..." -ForegroundColor Cyan
Write-Host ""

# Start services
docker-compose up -d

Write-Host ""
Write-Host "⏳ Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check service health
Write-Host ""
Write-Host "🔍 Checking service status..." -ForegroundColor Cyan
docker-compose ps

Write-Host ""
Write-Host "==================================" -ForegroundColor Green
Write-Host "✅ Services Started!" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Access points:" -ForegroundColor Cyan
Write-Host "   • Frontend:  http://localhost:5173" -ForegroundColor White
Write-Host "   • Backend:   http://localhost:8000" -ForegroundColor White
Write-Host "   • API Docs:  http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "📋 Useful commands:" -ForegroundColor Cyan
Write-Host "   • View logs:     docker-compose logs -f" -ForegroundColor White
Write-Host "   • Stop services: docker-compose down" -ForegroundColor White
Write-Host "   • Restart:       docker-compose restart" -ForegroundColor White
Write-Host ""
Write-Host "🎉 Ready to use! Open http://localhost:5173 in your browser" -ForegroundColor Green
Write-Host ""
Write-Host "Press any key to open in browser..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
Start-Process "http://localhost:5173"
