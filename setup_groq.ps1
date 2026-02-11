# Quick Groq Setup Script
# This script helps you set up Groq API in 2 minutes!

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚀 Groq API Quick Setup" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Groq is:" -ForegroundColor Yellow
Write-Host "  ⚡ 10x FASTER than other AI APIs" -ForegroundColor Green
Write-Host "  💰 FREE generous tier (no credit card)" -ForegroundColor Green
Write-Host "  🧠 Powerful models (Llama 3.3 70B)" -ForegroundColor Green
Write-Host "  ✅ Easy setup (2 minutes)`n" -ForegroundColor Green

# Check if API key already exists
$envPath = "backend\.env"
if (Test-Path $envPath) {
    $envContent = Get-Content $envPath -Raw
    if ($envContent -match "GROQ_API_KEY=gsk_[a-zA-Z0-9]+") {
        Write-Host "✅ Groq API key already configured!" -ForegroundColor Green
        Write-Host "   Found in: $envPath`n" -ForegroundColor Gray
        
        $continue = Read-Host "Do you want to update it? (y/N)"
        if ($continue -ne "y" -and $continue -ne "Y") {
            Write-Host "`n✅ Setup complete! Your Groq API is ready to use." -ForegroundColor Green
            Write-Host "`nNext steps:" -ForegroundColor Yellow
            Write-Host "  1. cd backend" -ForegroundColor White
            Write-Host "  2. pip install groq" -ForegroundColor White
            Write-Host "  3. uvicorn app.main:app --reload" -ForegroundColor White
            Write-Host "  4. Test with: .\tmp_rovodev_test_real_ai.ps1`n" -ForegroundColor White
            exit 0
        }
    }
}

Write-Host "Step 1: Get Your API Key" -ForegroundColor Yellow
Write-Host "  1. Open: https://console.groq.com/keys" -ForegroundColor White
Write-Host "  2. Sign up/Login (Google/GitHub/Email)" -ForegroundColor White
Write-Host "  3. Click 'Create API Key'" -ForegroundColor White
Write-Host "  4. Copy the key (starts with 'gsk_')`n" -ForegroundColor White

Write-Host "Opening Groq Console in your browser..." -ForegroundColor Cyan
Start-Sleep -Seconds 2
Start-Process "https://console.groq.com/keys"

Write-Host "`n" -ForegroundColor White
Write-Host "Step 2: Enter Your API Key" -ForegroundColor Yellow
Write-Host "  (Press Enter to skip and set it manually later)" -ForegroundColor Gray

$apiKey = Read-Host "`nPaste your Groq API key here"

if ([string]::IsNullOrWhiteSpace($apiKey)) {
    Write-Host "`n⚠️ No API key provided." -ForegroundColor Yellow
    Write-Host "   You can add it manually to: backend\.env" -ForegroundColor Yellow
    Write-Host "   Line: GROQ_API_KEY=your_key_here`n" -ForegroundColor Yellow
    exit 0
}

# Validate key format
if (-not ($apiKey -match "^gsk_[a-zA-Z0-9_-]+$")) {
    Write-Host "`n⚠️ Warning: API key doesn't match expected format (gsk_...)" -ForegroundColor Yellow
    $confirm = Read-Host "Continue anyway? (y/N)"
    if ($confirm -ne "y" -and $confirm -ne "Y") {
        exit 0
    }
}

# Update .env file
Write-Host "`nStep 3: Updating configuration..." -ForegroundColor Yellow

if (Test-Path $envPath) {
    $envContent = Get-Content $envPath -Raw
    
    # Check if GROQ_API_KEY line exists
    if ($envContent -match "GROQ_API_KEY=.+") {
        # Replace existing key
        $envContent = $envContent -replace "GROQ_API_KEY=.+", "GROQ_API_KEY=$apiKey"
        Write-Host "  ✅ Updated existing GROQ_API_KEY" -ForegroundColor Green
    } else {
        # Add new key after AI_PROVIDER line
        $envContent = $envContent -replace "(AI_PROVIDER=groq)", "`$1`nGROQ_API_KEY=$apiKey`nGROQ_MODEL=llama-3.3-70b-versatile"
        Write-Host "  ✅ Added GROQ_API_KEY to .env" -ForegroundColor Green
    }
    
    # Save updated content
    Set-Content -Path $envPath -Value $envContent -NoNewline
    Write-Host "  ✅ Configuration saved to: $envPath" -ForegroundColor Green
} else {
    Write-Host "  ❌ Error: backend\.env not found!" -ForegroundColor Red
    Write-Host "  Please create it from .env.example first`n" -ForegroundColor Red
    exit 1
}

# Install groq package
Write-Host "`nStep 4: Installing Groq package..." -ForegroundColor Yellow
try {
    $pipOutput = pip show groq 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Groq package already installed" -ForegroundColor Green
    } else {
        Write-Host "  Installing groq package..." -ForegroundColor Cyan
        pip install groq --quiet
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✅ Groq package installed successfully" -ForegroundColor Green
        } else {
            Write-Host "  ⚠️ Failed to install groq package" -ForegroundColor Yellow
            Write-Host "  Please run manually: pip install groq" -ForegroundColor Yellow
        }
    }
} catch {
    Write-Host "  ⚠️ Could not check/install groq package" -ForegroundColor Yellow
    Write-Host "  Please run manually: pip install groq" -ForegroundColor Yellow
}

# Success message
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "✅ GROQ SETUP COMPLETE!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Configuration:" -ForegroundColor Yellow
Write-Host "  ✅ AI Provider: Groq" -ForegroundColor Green
Write-Host "  ✅ Model: llama-3.3-70b-versatile (70B parameters!)" -ForegroundColor Green
Write-Host "  ✅ API Key: Configured (${apiKey.Substring(0,10)}...)" -ForegroundColor Green
Write-Host "  ✅ Speed: ⚡ ULTRA FAST (< 1 second responses)" -ForegroundColor Green
Write-Host "  ✅ Cost: 💰 FREE tier`n" -ForegroundColor Green

Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Start/Restart your backend:" -ForegroundColor White
Write-Host "     cd backend" -ForegroundColor Cyan
Write-Host "     uvicorn app.main:app --reload`n" -ForegroundColor Cyan

Write-Host "  2. Test it works:" -ForegroundColor White
Write-Host "     .\tmp_rovodev_test_real_ai.ps1`n" -ForegroundColor Cyan

Write-Host "  3. You should see in console:" -ForegroundColor White
Write-Host "     ✅ Groq client initialized" -ForegroundColor Green
Write-Host "     ✅ USING GROQ API" -ForegroundColor Green
Write-Host "     ✅ GROQ API CALL SUCCESSFUL`n" -ForegroundColor Green

Write-Host "Troubleshooting:" -ForegroundColor Yellow
Write-Host "  • Not working? Check: backend\.env has GROQ_API_KEY=gsk_..." -ForegroundColor Gray
Write-Host "  • See guide: GROQ_SETUP.md" -ForegroundColor Gray
Write-Host "  • Get help: https://console.groq.com/docs`n" -ForegroundColor Gray

Write-Host "🎉 Ready to chat with LIGHTNING FAST AI! ⚡" -ForegroundColor Cyan
