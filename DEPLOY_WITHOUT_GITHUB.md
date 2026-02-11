# 🚀 Deploy to Vercel WITHOUT GitHub

**Deploy directly from your local machine - no code pushing required!**

---

## 📋 What You Need

1. Node.js installed (check: `node --version`)
2. API Key (Groq/POE/Anthropic)
3. That's it!

---

## ⚡ Deploy in 3 Steps

### Step 1: Install Vercel CLI (1 minute)
```powershell
npm install -g vercel
```

Wait for installation to complete.

### Step 2: Login to Vercel (30 seconds)
```powershell
vercel login
```

This will:
- Open your browser
- Ask you to sign up/login (use email or GitHub)
- Verify your email
- You're logged in!

### Step 3: Deploy! (2 minutes)
```powershell
cd MSK-Wellness-Coach
vercel
```

**Answer the prompts:**
```
? Set up and deploy "MSK-Wellness-Coach"? [Y/n] 
→ Press Y (yes)

? Which scope do you want to deploy to?
→ Select your account

? Link to existing project? [y/N]
→ Press N (no, create new)

? What's your project's name?
→ msk-wellness-coach (or any name you want)

? In which directory is your code located?
→ Press Enter (current directory)

? Want to modify the settings? [y/N]
→ Press N (no)
```

Vercel will now:
1. Upload your code
2. Build the frontend
3. Deploy everything
4. Give you a URL!

---

## 🔑 Step 4: Add Environment Variables

After deployment, add your API key:

```powershell
# Add AI provider
vercel env add AI_PROVIDER
# When prompted, enter: groq
# Select: Production

# Add API key
vercel env add GROQ_API_KEY
# When prompted, enter: your_actual_groq_api_key
# Select: Production

# Add other required variables
vercel env add DATABASE_URL
# Enter: sqlite+aiosqlite:///./tmp/msk_chatbot.db
# Select: Production

vercel env add CHROMA_PERSIST_DIR
# Enter: /tmp/chromadb
# Select: Production

vercel env add UPLOAD_DIR
# Enter: /tmp/uploads
# Select: Production
```

---

## 🔄 Step 5: Redeploy with Environment Variables

```powershell
vercel --prod
```

This redeploys with your environment variables activated.

---

## ✅ You're Live!

Your chatbot is now deployed! Vercel will show you the URL:

```
✅  Production: https://msk-wellness-coach.vercel.app
```

### Test Your Deployment:
1. **Health Check**: https://your-app.vercel.app/health
2. **API Docs**: https://your-app.vercel.app/docs
3. **Chat Interface**: https://your-app.vercel.app

---

## 🔄 How to Update Your Deployment

Made changes to your code? Just run:

```powershell
cd MSK-Wellness-Coach
vercel --prod
```

That's it! Your changes are live.

---

## 📊 Useful Commands

```powershell
# View your deployments
vercel ls

# View logs (real-time)
vercel logs

# View environment variables
vercel env ls

# Remove a deployment
vercel remove msk-wellness-coach

# Open your deployment in browser
vercel open
```

---

## 🆘 Troubleshooting

### "Command 'vercel' not found"
```powershell
# Install globally
npm install -g vercel

# Or use npx (no installation needed)
npx vercel
```

### "Build failed"
Check the error in terminal. Common issues:
- Missing dependencies → Run `npm install` in frontend folder
- Python errors → Check `backend/requirements-vercel.txt`

### "API returns 500 errors"
Environment variables not set. Run:
```powershell
vercel env ls
```
Make sure all required variables are there.

### "Want to see logs"
```powershell
vercel logs --follow
```

---

## 🎯 Complete Setup Script

Here's everything in one go:

```powershell
# 1. Install Vercel CLI
npm install -g vercel

# 2. Login
vercel login

# 3. Navigate to project
cd MSK-Wellness-Coach

# 4. Deploy
vercel

# 5. Add environment variables
vercel env add AI_PROVIDER
# Enter: groq, Select: Production

vercel env add GROQ_API_KEY  
# Enter: your_key, Select: Production

vercel env add DATABASE_URL
# Enter: sqlite+aiosqlite:///./tmp/msk_chatbot.db, Select: Production

vercel env add CHROMA_PERSIST_DIR
# Enter: /tmp/chromadb, Select: Production

vercel env add UPLOAD_DIR
# Enter: /tmp/uploads, Select: Production

# 6. Deploy to production with env vars
vercel --prod

# Done! 🎉
```

---

## 💡 Pro Tips

1. **Keep your code private**: With CLI deployment, your code stays on your machine
2. **Quick updates**: Just run `vercel --prod` to update
3. **Preview deployments**: Run `vercel` (without --prod) for test deployments
4. **Environment variables**: Use `vercel env pull` to download them locally

---

## 🔐 Environment Variables Reference

You need these environment variables:

| Variable | Value | Required |
|----------|-------|----------|
| `AI_PROVIDER` | `groq` (or `poe`/`anthropic`) | ✅ Yes |
| `GROQ_API_KEY` | Your Groq API key | ✅ Yes (if using Groq) |
| `POE_API_KEY` | Your POE API key | Only if using POE |
| `ANTHROPIC_API_KEY` | Your Anthropic key | Only if using Anthropic |
| `DATABASE_URL` | `sqlite+aiosqlite:///./tmp/msk_chatbot.db` | Auto-set |
| `CHROMA_PERSIST_DIR` | `/tmp/chromadb` | Auto-set |
| `UPLOAD_DIR` | `/tmp/uploads` | Auto-set |

---

## 🎊 That's It!

No GitHub, no git, no pushing code. Just deploy directly from your machine!

**Need help?** Just ask or check Vercel docs: https://vercel.com/docs/cli
