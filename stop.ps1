# PowerShell script to stop services
Write-Host "🛑 Stopping MSK Wellness AI Chatbot services..." -ForegroundColor Yellow
docker-compose down
Write-Host ""
Write-Host "✅ All services stopped" -ForegroundColor Green
