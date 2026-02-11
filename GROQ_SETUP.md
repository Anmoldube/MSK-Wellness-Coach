# 🚀 Groq API Setup Guide

## Why Groq?

✅ **SUPER FAST** - 10x faster than other APIs (< 1 second responses!)  
✅ **FREE TIER** - Generous free quota (no credit card needed)  
✅ **POWERFUL** - Llama 3.3 70B, Mixtral 8x7B models  
✅ **EASY** - Simple OpenAI-compatible API  

---

## 🔑 Step 1: Get Your Groq API Key

### Option A: Create New Account (2 minutes)

1. **Visit:** https://console.groq.com/
2. **Sign up** with Google/GitHub/Email
3. **Go to API Keys:** https://console.groq.com/keys
4. **Click:** "Create API Key"
5. **Copy** the key (starts with `gsk_...`)

### Option B: Use Existing Account

If you already have a Groq account:
1. **Login:** https://console.groq.com/
2. **Navigate to:** API Keys section
3. **Copy** your existing key

---

## ⚙️ Step 2: Configure Your Application

### Update `backend/.env` file:

```bash
# Change AI provider to groq
AI_PROVIDER=groq

# Add your Groq API key
GROQ_API_KEY=gsk_your_actual_key_here

# Choose your model (optional - defaults to llama-3.3-70b-versatile)
GROQ_MODEL=llama-3.3-70b-versatile
```

### Available Models:

| Model | Speed | Quality | Best For |
|-------|-------|---------|----------|
| **llama-3.3-70b-versatile** | Fast | High | General use (recommended) |
| **llama-3.1-8b-instant** | Ultra Fast | Good | Quick responses |
| **mixtral-8x7b-32768** | Fast | High | Long context |
| **llama-3.1-70b-versatile** | Fast | High | Complex tasks |

---

## 🧪 Step 3: Test Groq Integration

### Install Groq Package:

```powershell
cd backend
pip install groq
```

### Restart Backend:

```powershell
# Stop current backend (Ctrl+C)

# Restart
uvicorn app.main:app --reload
```

### You Should See:

```
🔧 INITIALIZING LLM CLIENT
================================
   AI_PROVIDER from settings: 'groq'
   ✓ Provider is 'groq' - attempting to initialize Groq client...
   GROQ_API_KEY exists: True
   GROQ_API_KEY length: 56
   ✅ Groq client initialized with model: llama-3.3-70b-versatile
================================
```

---

## ✅ Step 4: Verify It's Working

### Method 1: Quick PowerShell Test

```powershell
# Create a test user
$profile = @{
    name = "Test User"
    performance_data = @{
        balance = 40
        reaction_time = 400
    }
} | ConvertTo-Json

$user = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/profile" `
    -Method Post -Body $profile -ContentType "application/json"

# Chat with Groq
$chat = @{
    message = "Analyze my balance and give me advice"
    user_id = $user.user_id
    include_context = $true
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/chat/message" `
    -Method Post -Body $chat -ContentType "application/json"

Write-Host $response.message
```

### Method 2: Run Test Script

```powershell
.\tmp_rovodev_test_real_ai.ps1
```

### What to Look For:

✅ **Response time:** < 2 seconds (Groq is FAST!)  
✅ **Personalization:** Uses your name and specific metrics  
✅ **Natural language:** Conversational, not templated  
✅ **Console shows:** "✅ USING GROQ API"  

---

## 🎯 Groq Free Tier Limits

| Metric | Limit |
|--------|-------|
| **Requests per minute** | 30 |
| **Requests per day** | 14,400 |
| **Tokens per minute** | 60,000 |
| **Tokens per day** | 6,000,000 |

**Translation:** More than enough for development and testing! 🎉

---

## 🔍 Troubleshooting

### Issue: "Import error: No module named 'groq'"

**Solution:**
```powershell
cd backend
pip install groq
```

### Issue: "GROQ_API_KEY is None or empty"

**Solution:**
1. Check `backend/.env` file exists
2. Verify line: `GROQ_API_KEY=gsk_...`
3. No quotes needed around the key
4. Restart backend after changing .env

### Issue: "Rate limit exceeded"

**Solution:**
- Free tier limit reached
- Wait 1 minute and try again
- Or upgrade to paid tier (still cheap!)

### Issue: Still seeing mock responses

**Check:**
1. `AI_PROVIDER=groq` in `.env`
2. API key is correct (56 characters, starts with `gsk_`)
3. Backend restarted after .env changes
4. Console shows "✅ Groq client initialized"

---

## 💡 Pro Tips

### 1. Choose the Right Model

```bash
# For speed (< 0.5 seconds)
GROQ_MODEL=llama-3.1-8b-instant

# For quality (1-2 seconds)
GROQ_MODEL=llama-3.3-70b-versatile

# For long conversations
GROQ_MODEL=mixtral-8x7b-32768
```

### 2. Monitor Usage

- **Dashboard:** https://console.groq.com/
- **View:** Request counts, token usage, errors

### 3. Test Personalization

```bash
# Always include user_id and context for personalized responses
{
  "message": "What does my report say?",
  "user_id": "your-user-id",
  "include_context": true  # IMPORTANT!
}
```

---

## 🆚 Groq vs Other Providers

| Feature | Groq | Claude | Poe |
|---------|------|--------|-----|
| **Speed** | ⚡⚡⚡ Ultra Fast | 🐌 Slow | 🐌 Slow |
| **Free Tier** | ✅ Generous | ❌ Limited | ✅ Yes |
| **Setup** | ✅ Easy | ✅ Easy | ⚠️ Complex |
| **Cost** | $ Very Cheap | $$$ Expensive | $$ Moderate |
| **Quality** | ✅ Excellent | ✅ Excellent | ✅ Good |

**Recommendation:** Use Groq for development! Fast, free, and excellent quality.

---

## 📚 Example .env Configuration

```bash
# Complete Groq configuration
AI_PROVIDER=groq
GROQ_API_KEY=gsk_abc123xyz789...
GROQ_MODEL=llama-3.3-70b-versatile

# Keep other keys for fallback (optional)
ANTHROPIC_API_KEY=sk-ant-api03-...
POE_API_KEY=k8kfIIZGNx...

# Database
DATABASE_URL=sqlite+aiosqlite:///./msk_chatbot.db

# File uploads
UPLOAD_DIR=./data/uploads
MAX_UPLOAD_SIZE=10485760
```

---

## 🎉 Success Checklist

- [ ] Groq account created
- [ ] API key obtained (starts with `gsk_`)
- [ ] `backend/.env` updated with key
- [ ] `AI_PROVIDER=groq` set
- [ ] `groq` package installed (`pip install groq`)
- [ ] Backend restarted
- [ ] Console shows "✅ Groq client initialized"
- [ ] Test message sent and received
- [ ] Response includes user's name and metrics
- [ ] Response time < 2 seconds

---

## 🔗 Useful Links

- **Groq Console:** https://console.groq.com/
- **API Docs:** https://console.groq.com/docs
- **Models:** https://console.groq.com/docs/models
- **Rate Limits:** https://console.groq.com/docs/rate-limits
- **Python SDK:** https://github.com/groq/groq-python

---

## 🎯 Next Steps

Once Groq is working:

1. ✅ **Test personalization** - Create profiles with different metrics
2. ✅ **Try different models** - Compare speed vs quality
3. ✅ **Test the frontend** - Full user experience at http://localhost:5173
4. ✅ **Monitor usage** - Check dashboard for request counts

**Groq + MSK Wellness Coach = Lightning Fast Personalized Health Advice! ⚡💪**
