# ⚡ Quick Deploy to Vercel (5 Minutes)

**Super fast deployment guide - for those who want to get started NOW!**

---

## 🎯 What You Need

1. GitHub account
2. Vercel account (sign up at [vercel.com](https://vercel.com))
3. API Key - Get ONE of these:
   - **Groq** (recommended): https://console.groq.com/keys
   - **POE**: https://poe.com/api_key
   - **Anthropic**: https://console.anthropic.com/

---

## 🚀 Deploy in 5 Steps

### Step 1: Push to GitHub (2 minutes)
```powershell
git init
git add .
git commit -m "Initial commit"
# Create repo on github.com/new
git remote add origin https://github.com/YOUR_USERNAME/msk-wellness-coach.git
git push -u origin main
```

### Step 2: Import to Vercel (1 minute)
1. Go to [vercel.com/new](https://vercel.com/new)
2. Click **"Import Project"**
3. Select your GitHub repo
4. Click **"Import"**

### Step 3: Add Environment Variables (1 minute)
In the Vercel import screen, add:

**For Groq (recommended):**
```
AI_PROVIDER = groq
GROQ_API_KEY = your_groq_key_here
```

**For POE:**
```
AI_PROVIDER = poe
POE_API_KEY = your_poe_key_here
POE_BOT_NAME = GPT-4o-Mini
```

**For Anthropic:**
```
AI_PROVIDER = anthropic
ANTHROPIC_API_KEY = your_anthropic_key_here
```

### Step 4: Deploy (1 minute)
Click **"Deploy"** and wait!

### Step 5: Test (30 seconds)
Once deployed, open your app at: `https://your-project.vercel.app`

---

## ✅ That's It!

Your chatbot is live! 🎉

**Need more details?** See [VERCEL_DEPLOYMENT_GUIDE.md](./VERCEL_DEPLOYMENT_GUIDE.md)

**Having issues?** Check the troubleshooting section in the full guide.
