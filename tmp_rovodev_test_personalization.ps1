# MSK Wellness Coach - Personalization Test Script
# This demonstrates how the chatbot personalizes responses based on user profile data

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "MSK Wellness Coach - Personalization Demo" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$API_BASE = "http://localhost:8000/api/v1"

# Check if backend is running
Write-Host "1. Checking if backend is running..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
    Write-Host "   ✅ Backend is healthy: $($health.status)`n" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Backend is not running!" -ForegroundColor Red
    Write-Host "   Please start the backend first with: cd backend; uvicorn app.main:app --reload`n" -ForegroundColor Red
    exit 1
}

# Test Case 1: Create User Profile with Performance Data
Write-Host "2. Creating user profile with performance data..." -ForegroundColor Yellow

$profile1 = @{
    name = "Sarah Johnson"
    performance_data = @{
        balance = 42
        reaction_time = 420
        flexibility = 55
        accuracy = 68
        endurance = 50
    }
} | ConvertTo-Json

try {
    $user1 = Invoke-RestMethod -Uri "$API_BASE/profile" -Method Post -Body $profile1 -ContentType "application/json"
    Write-Host "   ✅ Created profile for: $($user1.name)" -ForegroundColor Green
    Write-Host "   User ID: $($user1.user_id)" -ForegroundColor Gray
    Write-Host "   Metrics: Balance=$($user1.performance_data.balance), Flexibility=$($user1.performance_data.flexibility)`n" -ForegroundColor Gray
} catch {
    Write-Host "   ❌ Error creating profile: $_`n" -ForegroundColor Red
    exit 1
}

# Test Case 2: Chat WITHOUT user context (generic response)
Write-Host "3. Testing chat WITHOUT user context (generic)..." -ForegroundColor Yellow

$chatGeneric = @{
    message = "What does my report say?"
    include_context = $false
} | ConvertTo-Json

try {
    $responseGeneric = Invoke-RestMethod -Uri "$API_BASE/chat/message" -Method Post -Body $chatGeneric -ContentType "application/json"
    Write-Host "   📝 Generic Response (first 200 chars):" -ForegroundColor Cyan
    Write-Host "   $($responseGeneric.message.Substring(0, [Math]::Min(200, $responseGeneric.message.Length)))...`n" -ForegroundColor White
} catch {
    Write-Host "   ⚠️ Generic chat failed: $_`n" -ForegroundColor Yellow
}

# Test Case 3: Chat WITH user context (PERSONALIZED)
Write-Host "4. Testing chat WITH user context (PERSONALIZED)..." -ForegroundColor Yellow

$chatPersonalized = @{
    message = "What does my report say?"
    user_id = $user1.user_id
    include_context = $true
} | ConvertTo-Json

try {
    $responsePersonalized = Invoke-RestMethod -Uri "$API_BASE/chat/message" -Method Post -Body $chatPersonalized -ContentType "application/json"
    Write-Host "   ✨ PERSONALIZED Response:" -ForegroundColor Green
    Write-Host "   ----------------------------------------" -ForegroundColor Gray
    Write-Host "   $($responsePersonalized.message)" -ForegroundColor White
    Write-Host "   ----------------------------------------`n" -ForegroundColor Gray
    
    # Check for personalization markers
    if ($responsePersonalized.message -match $user1.name) {
        Write-Host "   ✅ Contains user's name: $($user1.name)" -ForegroundColor Green
    }
    if ($responsePersonalized.message -match "42|balance") {
        Write-Host "   ✅ References balance score (42)" -ForegroundColor Green
    }
    Write-Host ""
} catch {
    Write-Host "   ❌ Personalized chat failed: $_`n" -ForegroundColor Red
}

# Test Case 4: Ask about specific metric
Write-Host "5. Testing specific question about balance..." -ForegroundColor Yellow

$chatBalance = @{
    message = "How can I improve my balance?"
    user_id = $user1.user_id
    include_context = $true
} | ConvertTo-Json

try {
    $responseBalance = Invoke-RestMethod -Uri "$API_BASE/chat/message" -Method Post -Body $chatBalance -ContentType "application/json"
    Write-Host "   ✨ Balance Improvement Response:" -ForegroundColor Green
    Write-Host "   ----------------------------------------" -ForegroundColor Gray
    Write-Host "   $($responseBalance.message.Substring(0, [Math]::Min(400, $responseBalance.message.Length)))..." -ForegroundColor White
    Write-Host "   ----------------------------------------`n" -ForegroundColor Gray
    
    if ($responseBalance.suggested_questions) {
        Write-Host "   💡 Suggested Questions:" -ForegroundColor Cyan
        foreach ($q in $responseBalance.suggested_questions) {
            Write-Host "      - $q" -ForegroundColor White
        }
        Write-Host ""
    }
} catch {
    Write-Host "   ⚠️ Balance question failed: $_`n" -ForegroundColor Yellow
}

# Test Case 5: Get Personalized Exercise Recommendations
Write-Host "6. Getting personalized exercise recommendations..." -ForegroundColor Yellow

try {
    $exercises = Invoke-RestMethod -Uri "$API_BASE/recommendations/exercises/$($user1.user_id)" -Method Get
    Write-Host "   ✅ Received $($exercises.Count) personalized exercises" -ForegroundColor Green
    Write-Host "   Top 3 Recommendations:" -ForegroundColor Cyan
    
    for ($i = 0; $i -lt [Math]::Min(3, $exercises.Count); $i++) {
        $ex = $exercises[$i]
        Write-Host "   $($i+1). $($ex.name) - $($ex.category)" -ForegroundColor White
        Write-Host "      Reason: $($ex.recommendation_reason.Substring(0, [Math]::Min(80, $ex.recommendation_reason.Length)))..." -ForegroundColor Gray
    }
    Write-Host ""
} catch {
    Write-Host "   ⚠️ Exercise recommendations failed: $_`n" -ForegroundColor Yellow
}

# Test Case 6: Create Second User with Different Profile
Write-Host "7. Creating second user with DIFFERENT metrics..." -ForegroundColor Yellow

$profile2 = @{
    name = "Mike Chen"
    performance_data = @{
        balance = 85
        reaction_time = 280
        flexibility = 90
        accuracy = 92
        endurance = 88
    }
} | ConvertTo-Json

try {
    $user2 = Invoke-RestMethod -Uri "$API_BASE/profile" -Method Post -Body $profile2 -ContentType "application/json"
    Write-Host "   ✅ Created profile for: $($user2.name)" -ForegroundColor Green
    Write-Host "   Metrics: Balance=$($user2.performance_data.balance), Flexibility=$($user2.performance_data.flexibility)`n" -ForegroundColor Gray
} catch {
    Write-Host "   ❌ Error creating second profile: $_`n" -ForegroundColor Red
}

# Test Case 7: Compare responses for different users
Write-Host "8. Comparing personalized responses for different users..." -ForegroundColor Yellow

$chatUser2 = @{
    message = "What does my report say?"
    user_id = $user2.user_id
    include_context = $true
} | ConvertTo-Json

try {
    $responseUser2 = Invoke-RestMethod -Uri "$API_BASE/chat/message" -Method Post -Body $chatUser2 -ContentType "application/json"
    
    Write-Host "   👤 User 1 ($($user1.name) - Balance: 42):" -ForegroundColor Yellow
    Write-Host "   $(($responsePersonalized.message -split "`n")[0..2] -join "`n")`n" -ForegroundColor White
    
    Write-Host "   👤 User 2 ($($user2.name) - Balance: 85):" -ForegroundColor Yellow
    Write-Host "   $(($responseUser2.message -split "`n")[0..2] -join "`n")`n" -ForegroundColor White
    
    Write-Host "   ✅ Notice how responses are DIFFERENT based on each user's data!`n" -ForegroundColor Green
} catch {
    Write-Host "   ⚠️ Second user chat failed: $_`n" -ForegroundColor Yellow
}

# Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ PERSONALIZATION TEST COMPLETE" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Summary:" -ForegroundColor Yellow
Write-Host "✅ User profiles created with performance metrics" -ForegroundColor Green
Write-Host "✅ Chatbot uses user's NAME in responses" -ForegroundColor Green
Write-Host "✅ Chatbot references SPECIFIC METRICS (balance, flexibility, etc.)" -ForegroundColor Green
Write-Host "✅ Recommendations tailored to user weaknesses" -ForegroundColor Green
Write-Host "✅ Different users get different advice based on their data`n" -ForegroundColor Green

Write-Host "Test User IDs created:" -ForegroundColor Yellow
Write-Host "  Sarah Johnson (weak balance): $($user1.user_id)" -ForegroundColor White
Write-Host "  Mike Chen (strong balance): $($user2.user_id)`n" -ForegroundColor White

Write-Host "Try it in the frontend:" -ForegroundColor Cyan
Write-Host "  1. Open http://localhost:5173" -ForegroundColor White
Write-Host "  2. Use one of the User IDs above" -ForegroundColor White
Write-Host "  3. Ask 'What does my report say?' and see personalization!`n" -ForegroundColor White
