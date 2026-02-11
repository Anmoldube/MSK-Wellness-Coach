# Quick Groq Test - Verify it's working!

Write-Host "`n🧪 Quick Groq API Test`n" -ForegroundColor Cyan

# Check if backend is running
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get -ErrorAction Stop
    Write-Host "✅ Backend is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend not running. Start it first:" -ForegroundColor Red
    Write-Host "   cd backend" -ForegroundColor Yellow
    Write-Host "   uvicorn app.main:app --reload`n" -ForegroundColor Yellow
    exit 1
}

# Create test user
Write-Host "Creating test user..." -ForegroundColor Yellow
$profile = @{
    name = "Alex"
    performance_data = @{ balance = 35; flexibility = 50 }
} | ConvertTo-Json

$user = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/profile" -Method Post -Body $profile -ContentType "application/json"
Write-Host "✅ User created: $($user.name) (ID: $($user.user_id))`n" -ForegroundColor Green

# Send chat message
Write-Host "Sending message to Groq AI..." -ForegroundColor Yellow
$startTime = Get-Date

$chat = @{
    message = "Analyze my balance score and give me one specific exercise recommendation."
    user_id = $user.user_id
    include_context = $true
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/chat/message" -Method Post -Body $chat -ContentType "application/json"
    $duration = ((Get-Date) - $startTime).TotalSeconds
    
    Write-Host "✅ Response received in $([math]::Round($duration, 2)) seconds" -ForegroundColor Green
    
    if ($duration -lt 2) {
        Write-Host "⚡ ULTRA FAST - Groq is working perfectly!" -ForegroundColor Green
    }
    
    Write-Host "`n📄 Response:" -ForegroundColor Cyan
    Write-Host "─────────────────────────────────────" -ForegroundColor Gray
    Write-Host $response.message -ForegroundColor White
    Write-Host "─────────────────────────────────────`n" -ForegroundColor Gray
    
    # Check for personalization
    if ($response.message -match "Alex|35") {
        Write-Host "✅ Personalized response (uses name/metrics)" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Response may not be personalized" -ForegroundColor Yellow
    }
    
    Write-Host "`n🎉 Groq API is working perfectly!" -ForegroundColor Green
    Write-Host "Now try the full app at http://localhost:5173`n" -ForegroundColor Cyan
    
} catch {
    Write-Host "❌ Error: $_" -ForegroundColor Red
    Write-Host "`nCheck backend console for errors`n" -ForegroundColor Yellow
}
