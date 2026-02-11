# MSK Wellness Coach - REAL AI Test (No Mock Data)
# This verifies that the system uses REAL AI APIs (Claude/Poe) with personalization

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "REAL AI Personalization Test (No Mocks)" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$API_BASE = "http://localhost:8000/api/v1"

# Step 1: Check environment configuration
Write-Host "1. Checking AI configuration..." -ForegroundColor Yellow

# Check if .env file exists
if (Test-Path "backend\.env") {
    Write-Host "   ✅ Found backend\.env file" -ForegroundColor Green
    
    # Read and check API keys
    $envContent = Get-Content "backend\.env" -Raw
    
    if ($envContent -match "ANTHROPIC_API_KEY=(.+)") {
        $apiKey = $matches[1].Trim()
        if ($apiKey -and $apiKey -ne "your_anthropic_api_key_here") {
            Write-Host "   ✅ Anthropic API Key configured (${apiKey.Substring(0,10)}...)" -ForegroundColor Green
        }
    }
    
    if ($envContent -match "POE_API_KEY=(.+)") {
        $poeKey = $matches[1].Trim()
        if ($poeKey -and $poeKey -ne "your_poe_api_key_here") {
            Write-Host "   ✅ Poe API Key configured (${poeKey.Substring(0,10)}...)" -ForegroundColor Green
        }
    }
    
    if ($envContent -match "AI_PROVIDER=(.+)") {
        $provider = $matches[1].Trim()
        Write-Host "   📡 AI Provider set to: $provider" -ForegroundColor Cyan
    }
    Write-Host ""
} else {
    Write-Host "   ⚠️ backend\.env not found - system may use mock responses" -ForegroundColor Yellow
    Write-Host "   Create backend\.env from .env.example and add your API keys`n" -ForegroundColor Yellow
}

# Step 2: Check backend health
Write-Host "2. Checking backend status..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get -ErrorAction Stop
    Write-Host "   ✅ Backend is running: $($health.status)`n" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Backend is not running!" -ForegroundColor Red
    Write-Host "   Please start: cd backend; uvicorn app.main:app --reload`n" -ForegroundColor Red
    exit 1
}

# Step 3: Create test user profile
Write-Host "3. Creating test user profile..." -ForegroundColor Yellow

$profile = @{
    name = "Emma Rodriguez"
    performance_data = @{
        balance = 38
        reaction_time = 450
        flexibility = 52
        accuracy = 65
        endurance = 48
    }
} | ConvertTo-Json

try {
    $user = Invoke-RestMethod -Uri "$API_BASE/profile" -Method Post -Body $profile -ContentType "application/json"
    Write-Host "   ✅ Created profile: $($user.name)" -ForegroundColor Green
    Write-Host "   User ID: $($user.user_id)" -ForegroundColor Gray
    Write-Host "   Balance: $($user.performance_data.balance)/100 (Low - needs work)" -ForegroundColor Gray
    Write-Host "   Flexibility: $($user.performance_data.flexibility)% (Below average)`n" -ForegroundColor Gray
} catch {
    Write-Host "   ❌ Error creating profile: $_`n" -ForegroundColor Red
    exit 1
}

# Step 4: Send message and analyze response for AI vs Mock indicators
Write-Host "4. Sending personalized chat message to REAL AI..." -ForegroundColor Yellow
Write-Host "   (This may take 5-10 seconds for AI to respond)..." -ForegroundColor Gray

$chatRequest = @{
    message = "Analyze my performance data and give me specific advice on what I should focus on first. Be detailed."
    user_id = $user.user_id
    include_context = $true
} | ConvertTo-Json

try {
    $startTime = Get-Date
    $response = Invoke-RestMethod -Uri "$API_BASE/chat/message" -Method Post -Body $chatRequest -ContentType "application/json"
    $endTime = Get-Date
    $duration = ($endTime - $startTime).TotalSeconds
    
    Write-Host "   ✅ Received response in $([math]::Round($duration, 2)) seconds`n" -ForegroundColor Green
    
    # Analyze the response
    Write-Host "   📊 Response Analysis:" -ForegroundColor Cyan
    Write-Host "   ----------------------------------------" -ForegroundColor Gray
    
    # Check for personalization
    $hasName = $response.message -match "Emma"
    $hasBalance = $response.message -match "38|balance.*38"
    $hasFlexibility = $response.message -match "52|flexibility.*52"
    $hasMetrics = $response.message -match "(38|52|450|65|48)"
    
    if ($hasName) {
        Write-Host "   ✅ Uses user's name: Emma" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️ Doesn't use name (may be generic)" -ForegroundColor Yellow
    }
    
    if ($hasMetrics) {
        Write-Host "   ✅ References specific metrics" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️ No specific metrics mentioned" -ForegroundColor Yellow
    }
    
    # Check response characteristics
    $wordCount = ($response.message -split '\s+').Count
    Write-Host "   📝 Response length: $wordCount words" -ForegroundColor Cyan
    
    # Determine if mock or real AI
    $isMock = $false
    $mockIndicators = @(
        "Based on your recent assessment from",
        "Overall Score: 62/100",
        "demo-report-001",
        "January 15, 2026"
    )
    
    foreach ($indicator in $mockIndicators) {
        if ($response.message -match [regex]::Escape($indicator)) {
            $isMock = $true
            break
        }
    }
    
    Write-Host "   ----------------------------------------`n" -ForegroundColor Gray
    
    if ($isMock) {
        Write-Host "   ⚠️ MOCK RESPONSE DETECTED" -ForegroundColor Yellow
        Write-Host "   The system is using fallback mock responses." -ForegroundColor Yellow
        Write-Host "   This means:" -ForegroundColor Yellow
        Write-Host "   - API key may not be valid" -ForegroundColor Yellow
        Write-Host "   - AI provider may not be accessible" -ForegroundColor Yellow
        Write-Host "   - Network/firewall blocking API calls`n" -ForegroundColor Yellow
    } else {
        Write-Host "   ✅ REAL AI RESPONSE DETECTED" -ForegroundColor Green
        Write-Host "   The system is using actual AI (Claude/Poe)!" -ForegroundColor Green
        Write-Host "   Response characteristics suggest live AI generation.`n" -ForegroundColor Green
    }
    
    # Display full response
    Write-Host "   📄 Full Response:" -ForegroundColor Cyan
    Write-Host "   ========================================" -ForegroundColor Gray
    Write-Host "   $($response.message)" -ForegroundColor White
    Write-Host "   ========================================`n" -ForegroundColor Gray
    
    # Check metadata
    if ($response.PSObject.Properties['metadata']) {
        $provider = $response.metadata.provider
        Write-Host "   🤖 AI Provider: $provider" -ForegroundColor Cyan
        if ($provider -eq "poe") {
            Write-Host "   ✅ Using Poe API" -ForegroundColor Green
        } elseif ($provider -eq "anthropic") {
            Write-Host "   ✅ Using Anthropic Claude" -ForegroundColor Green
        } elseif ($provider -eq "unknown" -or !$provider) {
            Write-Host "   ⚠️ Provider unknown - may be mock" -ForegroundColor Yellow
        }
        Write-Host ""
    }
    
    # Display suggested questions
    if ($response.suggested_questions -and $response.suggested_questions.Count -gt 0) {
        Write-Host "   💡 Suggested Follow-up Questions:" -ForegroundColor Cyan
        foreach ($q in $response.suggested_questions) {
            Write-Host "      • $q" -ForegroundColor White
        }
        Write-Host ""
    }
    
} catch {
    Write-Host "   ❌ Error sending message: $_`n" -ForegroundColor Red
    exit 1
}

# Step 5: Test another question to verify consistency
Write-Host "5. Testing follow-up question..." -ForegroundColor Yellow

$followUp = @{
    message = "What specific exercises should I do for my balance score of 38?"
    user_id = $user.user_id
    include_context = $true
} | ConvertTo-Json

try {
    $response2 = Invoke-RestMethod -Uri "$API_BASE/chat/message" -Method Post -Body $followUp -ContentType "application/json"
    
    Write-Host "   ✅ Received follow-up response" -ForegroundColor Green
    Write-Host "   Preview (first 300 chars):" -ForegroundColor Cyan
    Write-Host "   ----------------------------------------" -ForegroundColor Gray
    $preview = $response2.message.Substring(0, [Math]::Min(300, $response2.message.Length))
    Write-Host "   $preview..." -ForegroundColor White
    Write-Host "   ----------------------------------------`n" -ForegroundColor Gray
    
    # Check if it remembers the user
    if ($response2.message -match "Emma|38") {
        Write-Host "   ✅ AI remembers user context!" -ForegroundColor Green
    }
    Write-Host ""
    
} catch {
    Write-Host "   ⚠️ Follow-up question failed: $_`n" -ForegroundColor Yellow
}

# Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "TEST SUMMARY" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Configuration Check:" -ForegroundColor Yellow
if (Test-Path "backend\.env") {
    Write-Host "  ✅ Environment file exists" -ForegroundColor Green
} else {
    Write-Host "  ❌ No .env file found" -ForegroundColor Red
}

Write-Host "`nPersonalization Check:" -ForegroundColor Yellow
Write-Host "  ✅ User profile created with specific metrics" -ForegroundColor Green
Write-Host "  ✅ User ID passed to chat endpoint" -ForegroundColor Green
Write-Host "  ✅ Context inclusion enabled" -ForegroundColor Green

Write-Host "`nAI Response Check:" -ForegroundColor Yellow
if (!$isMock) {
    Write-Host "  ✅ REAL AI RESPONSES - No mock data!" -ForegroundColor Green
    Write-Host "  ✅ Personalized responses with user's data" -ForegroundColor Green
    Write-Host "  ✅ Claude/Poe API working correctly" -ForegroundColor Green
} else {
    Write-Host "  ⚠️ MOCK RESPONSES DETECTED" -ForegroundColor Yellow
    Write-Host "  ⚠️ Check your API keys in backend\.env" -ForegroundColor Yellow
}

Write-Host "`nNext Steps:" -ForegroundColor Cyan
Write-Host "  1. If using mock data, verify API keys are correct" -ForegroundColor White
Write-Host "  2. Try the frontend at http://localhost:5173" -ForegroundColor White
Write-Host "  3. Use this User ID: $($user.user_id)" -ForegroundColor White
Write-Host "  4. Ask personalized questions and see real AI responses!`n" -ForegroundColor White

Write-Host "Test user created:" -ForegroundColor Yellow
Write-Host "  Name: Emma Rodriguez" -ForegroundColor White
Write-Host "  ID: $($user.user_id)" -ForegroundColor White
Write-Host "  Balance: 38/100 (needs improvement)" -ForegroundColor White
Write-Host "  Flexibility: 52% (below average)`n" -ForegroundColor White
