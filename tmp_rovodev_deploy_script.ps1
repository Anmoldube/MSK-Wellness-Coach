# MSK Wellness Coach - Vercel Deployment Script
# This script deploys your chatbot to Vercel WITHOUT using GitHub

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  MSK Wellness Coach - Vercel Deploy   " -ForegroundColor Cyan
Write-Host "  No GitHub Required!                  " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Node.js is installed
Write-Host "[1/6] Checking Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "  ✅ Node.js installed: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Node.js not found!" -ForegroundColor Red
    Write-Host "  Please install Node.js from: https://nodejs.org" -ForegroundColor Red
    exit 1
}

# Install Vercel CLI
Write-Host ""
Write-Host "[2/6] Installing Vercel CLI..." -ForegroundColor Yellow
try {
    npm install -g vercel
    Write-Host "  ✅ Vercel CLI installed" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Failed to install Vercel CLI" -ForegroundColor Red
    Write-Host "  Try running as Administrator" -ForegroundColor Yellow
    exit 1
}

# Login to Vercel
Write-Host ""
Write-Host "[3/6] Login to Vercel..." -ForegroundColor Yellow
Write-Host "  Opening browser for login..." -ForegroundColor Cyan
Write-Host "  (If browser doesn't open, follow the link in terminal)" -ForegroundColor Cyan
vercel login

if ($LASTEXITCODE -ne 0) {
    Write-Host "  ❌ Login failed" -ForegroundColor Red
    exit 1
}
Write-Host "  ✅ Logged in successfully" -ForegroundColor Green

# Get API Key from user
Write-Host ""
Write-Host "[4/6] Configure API Key..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Choose your AI provider:" -ForegroundColor Cyan
Write-Host "  1. Groq (Recommended - Fast & Free)" -ForegroundColor White
Write-Host "     Get key: https://console.groq.com/keys" -ForegroundColor Gray
Write-Host "  2. POE" -ForegroundColor White
Write-Host "     Get key: https://poe.com/api_key" -ForegroundColor Gray
Write-Host "  3. Anthropic" -ForegroundColor White
Write-Host "     Get key: https://console.anthropic.com/" -ForegroundColor Gray
Write-Host ""

$choice = Read-Host "Enter choice (1/2/3)"

switch ($choice) {
    "1" {
        $AI_PROVIDER = "groq"
        Write-Host "  Selected: Groq" -ForegroundColor Green
        $API_KEY = Read-Host "Enter your Groq API Key (starts with gsk_)"
        $KEY_NAME = "GROQ_API_KEY"
    }
    "2" {
        $AI_PROVIDER = "poe"
        Write-Host "  Selected: POE" -ForegroundColor Green
        $API_KEY = Read-Host "Enter your POE API Key"
        $KEY_NAME = "POE_API_KEY"
        $POE_BOT = Read-Host "Enter POE bot name (default: GPT-4o-Mini)"
        if ([string]::IsNullOrWhiteSpace($POE_BOT)) {
            $POE_BOT = "GPT-4o-Mini"
        }
    }
    "3" {
        $AI_PROVIDER = "anthropic"
        Write-Host "  Selected: Anthropic" -ForegroundColor Green
        $API_KEY = Read-Host "Enter your Anthropic API Key"
        $KEY_NAME = "ANTHROPIC_API_KEY"
    }
    default {
        Write-Host "  Invalid choice. Defaulting to Groq" -ForegroundColor Yellow
        $AI_PROVIDER = "groq"
        $API_KEY = Read-Host "Enter your Groq API Key"
        $KEY_NAME = "GROQ_API_KEY"
    }
}

# Deploy to Vercel
Write-Host ""
Write-Host "[5/6] Deploying to Vercel..." -ForegroundColor Yellow
Write-Host "  This will upload your code and build the app..." -ForegroundColor Cyan
Write-Host ""

# First deployment (creates the project)
vercel --yes

if ($LASTEXITCODE -ne 0) {
    Write-Host "  ❌ Deployment failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "  ✅ Initial deployment complete" -ForegroundColor Green

# Add environment variables
Write-Host ""
Write-Host "[6/6] Setting up environment variables..." -ForegroundColor Yellow

# AI Provider
Write-Host "  Adding AI_PROVIDER..." -ForegroundColor Cyan
Write-Output $AI_PROVIDER | vercel env add AI_PROVIDER production

# API Key
Write-Host "  Adding $KEY_NAME..." -ForegroundColor Cyan
Write-Output $API_KEY | vercel env add $KEY_NAME production

# POE Bot Name (if applicable)
if ($AI_PROVIDER -eq "poe") {
    Write-Host "  Adding POE_BOT_NAME..." -ForegroundColor Cyan
    Write-Output $POE_BOT | vercel env add POE_BOT_NAME production
}

# Database and storage paths
Write-Host "  Adding database configuration..." -ForegroundColor Cyan
Write-Output "sqlite+aiosqlite:///./tmp/msk_chatbot.db" | vercel env add DATABASE_URL production
Write-Output "/tmp/chromadb" | vercel env add CHROMA_PERSIST_DIR production
Write-Output "/tmp/uploads" | vercel env add UPLOAD_DIR production

Write-Host "  ✅ Environment variables configured" -ForegroundColor Green

# Final production deployment
Write-Host ""
Write-Host "Deploying to production with environment variables..." -ForegroundColor Yellow
vercel --prod

if ($LASTEXITCODE -ne 0) {
    Write-Host "  ❌ Production deployment failed" -ForegroundColor Red
    exit 1
}

# Success!
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  🎉 DEPLOYMENT SUCCESSFUL! 🎉         " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your chatbot is now live!" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Vercel will show your URL above (https://xxx.vercel.app)" -ForegroundColor White
Write-Host "  2. Test health endpoint: https://your-app.vercel.app/health" -ForegroundColor White
Write-Host "  3. View API docs: https://your-app.vercel.app/docs" -ForegroundColor White
Write-Host "  4. Use the chatbot: https://your-app.vercel.app" -ForegroundColor White
Write-Host ""
Write-Host "Useful commands:" -ForegroundColor Yellow
Write-Host "  vercel ls          - List your deployments" -ForegroundColor White
Write-Host "  vercel logs        - View logs" -ForegroundColor White
Write-Host "  vercel --prod      - Update deployment" -ForegroundColor White
Write-Host "  vercel open        - Open in browser" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
