# 🚀 Complete Vercel Deployment Guide for MSK Wellness Coach

This guide will walk you through deploying your **full-stack chatbot** to Vercel in simple steps - **no prior Vercel experience needed!**

## 📋 What You're Deploying

- ✅ **Frontend**: React app (static site on Vercel CDN)
- ✅ **Backend**: FastAPI Python API (Vercel Serverless Functions)
- ✅ **Database**: SQLite (serverless-friendly)
- ✅ **AI**: Your choice (Groq, POE, Anthropic)

---

## 🎯 Step 1: Prerequisites

### 1.1 Create a Vercel Account
1. Go to [vercel.com](https://vercel.com)
2. Click **"Sign Up"**
3. Sign up with **GitHub** (recommended) or email
4. Verify your email if needed

### 1.2 Install Vercel CLI (Optional but Recommended)
```powershell
npm install -g vercel
```

### 1.3 Get Your API Key
Choose **ONE** of these options:

**Option A: Groq (Recommended - Fast & Free)**
- Go to: https://console.groq.com/keys
- Sign up/login
- Click "Create API Key"
- Copy the key (starts with `gsk_...`)

**Option B: POE**
- Go to: https://poe.com/api_key
- Generate API key
- Copy the key

**Option C: Anthropic Claude**
- Go to: https://console.anthropic.com/
- Get API key
- Copy the key

---

## 🚀 Step 2: Deploy to Vercel

### Method A: Deploy via GitHub (Easiest!)

#### 2.1 Push Your Code to GitHub
```powershell
# Initialize git if not already done
git init
git add .
git commit -m "Ready for Vercel deployment"

# Create a new repository on GitHub (github.com/new)
# Then push your code
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

#### 2.2 Import to Vercel
1. Go to [vercel.com/new](https://vercel.com/new)
2. Click **"Import Project"**
3. Select your GitHub repository
4. Click **"Import"**

#### 2.3 Configure Build Settings
Vercel will auto-detect the project. Verify these settings:

- **Framework Preset**: Other
- **Root Directory**: `./` (leave as default)
- **Build Command**: `cd frontend && npm install && npm run build`
- **Output Directory**: `frontend/dist`
- **Install Command**: `npm install --prefix frontend && pip install -r backend/requirements-vercel.txt`

#### 2.4 Add Environment Variables
Click **"Environment Variables"** and add:

| Name | Value | Notes |
|------|-------|-------|
| `AI_PROVIDER` | `groq` | Or `poe`, `anthropic` |
| `GROQ_API_KEY` | `gsk_your_key_here` | Your actual API key |
| `DATABASE_URL` | `sqlite+aiosqlite:///./tmp/msk_chatbot.db` | Auto-configured |
| `CHROMA_PERSIST_DIR` | `/tmp/chromadb` | Auto-configured |
| `UPLOAD_DIR` | `/tmp/uploads` | Auto-configured |
| `DEBUG` | `false` | Production mode |

**For POE users, add:**
| Name | Value |
|------|-------|
| `POE_API_KEY` | `your_poe_key` |
| `POE_BOT_NAME` | `GPT-4o-Mini` |

**For Anthropic users, add:**
| Name | Value |
|------|-------|
| `ANTHROPIC_API_KEY` | `your_anthropic_key` |
| `CLAUDE_MODEL` | `claude-sonnet-4-20250514` |

#### 2.5 Deploy!
1. Click **"Deploy"**
2. Wait 2-3 minutes for build to complete
3. Your app will be live at `https://your-project.vercel.app`

---

### Method B: Deploy via Vercel CLI

```powershell
# Login to Vercel
vercel login

# Deploy
cd MSK-Wellness-Coach
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? (select your account)
# - Link to existing project? No
# - What's your project name? msk-wellness-coach
# - In which directory? ./
# - Override settings? No

# Add environment variables
vercel env add AI_PROVIDER
# Enter: groq

vercel env add GROQ_API_KEY
# Enter: your_actual_api_key

vercel env add DATABASE_URL
# Enter: sqlite+aiosqlite:///./tmp/msk_chatbot.db

vercel env add CHROMA_PERSIST_DIR
# Enter: /tmp/chromadb

vercel env add UPLOAD_DIR
# Enter: /tmp/uploads

# Deploy to production
vercel --prod
```

---

## 🎉 Step 3: Test Your Deployment

### 3.1 Check Health Endpoint
Open your browser and go to:
```
https://your-project.vercel.app/health
```

You should see: `{"status": "healthy"}`

### 3.2 Check API Documentation
```
https://your-project.vercel.app/docs
```

You should see the interactive FastAPI documentation.

### 3.3 Test the Frontend
```
https://your-project.vercel.app
```

You should see your chatbot interface!

### 3.4 Test a Chat Message
Open the chatbot and send a message like:
> "I'm a gamer experiencing wrist pain. What exercises can help?"

---

## 🔧 Step 4: Troubleshooting

### Problem: 404 Error on API Routes
**Solution**: Check that `vercel.json` is in the root directory and properly configured.

### Problem: Build Failed
**Solution**: Check build logs in Vercel dashboard:
1. Go to your project
2. Click "Deployments"
3. Click on failed deployment
4. Check logs for errors

Common fixes:
- Ensure `requirements-vercel.txt` exists
- Check that all dependencies are compatible
- Verify Python version (3.11+ recommended)

### Problem: API Returns 500 Error
**Solution**: Check Function Logs in Vercel:
1. Go to your project
2. Click "Functions"
3. Click on `api/index.py`
4. Check real-time logs

Common causes:
- Missing environment variables
- API key not set correctly
- Database connection issues

### Problem: CORS Errors
**Solution**: The config is already set to handle Vercel domains. If issues persist:
1. Check Vercel dashboard → Settings → Domains
2. Note your domain
3. Environment variables should auto-handle this

---

## 📊 Step 5: Monitor Your Deployment

### View Logs
```powershell
# Real-time logs
vercel logs

# Or view in dashboard
# Go to: Deployments → [Your Deployment] → Runtime Logs
```

### Check Analytics
- Go to your project dashboard
- Click "Analytics" tab
- View requests, errors, and performance

---

## 🔄 Step 6: Update Your Deployment

### Update Code
```powershell
# Make your changes
git add .
git commit -m "Update chatbot features"
git push

# Vercel will auto-deploy!
```

### Update Environment Variables
```powershell
# Via CLI
vercel env rm GROQ_API_KEY production
vercel env add GROQ_API_KEY production
# Enter new value

# Or via Dashboard:
# Project → Settings → Environment Variables → Edit
```

---

## 💡 Production Tips

### 1. Custom Domain (Optional)
1. Go to: Project → Settings → Domains
2. Click "Add"
3. Enter your domain (e.g., `wellness-coach.com`)
4. Follow DNS configuration instructions

### 2. Performance Optimization
The deployment is already optimized with:
- ✅ Code splitting
- ✅ Serverless functions
- ✅ Global CDN
- ✅ Automatic HTTPS

### 3. Monitoring
Set up monitoring:
1. Go to: Project → Settings → Integrations
2. Add monitoring tools (optional):
   - Sentry (error tracking)
   - LogDNA (logging)
   - DataDog (monitoring)

### 4. Database Persistence
**Important**: Vercel serverless functions use `/tmp` which is ephemeral. For production:

**Option A: Keep SQLite (Simple)**
- Data resets on cold starts
- Good for demos/prototypes
- No additional setup

**Option B: Use PostgreSQL (Production)**
- Persistent data
- Better for real users
- Options: Vercel Postgres, Supabase, Neon

To switch to PostgreSQL:
```powershell
# Add env variable
vercel env add DATABASE_URL
# Enter: postgresql+asyncpg://user:pass@host:5432/db
```

---

## 🎮 Usage Limits

### Vercel Free Tier (Hobby)
- ✅ 100 GB bandwidth/month
- ✅ 100 GB-hours serverless function execution
- ✅ Unlimited deployments
- ✅ HTTPS included

**Good enough for:**
- Personal projects
- Demos
- Low-moderate traffic apps (thousands of requests/day)

### Need More?
Upgrade to Vercel Pro ($20/month):
- 1 TB bandwidth
- 1000 GB-hours execution
- Priority support

---

## 📝 Environment Variables Reference

Here's the complete list you'll need in Vercel:

```env
# Required
AI_PROVIDER=groq
GROQ_API_KEY=gsk_your_key_here

# Auto-configured (optional to override)
DATABASE_URL=sqlite+aiosqlite:///./tmp/msk_chatbot.db
CHROMA_PERSIST_DIR=/tmp/chromadb
UPLOAD_DIR=/tmp/uploads
DEBUG=false
LOG_LEVEL=INFO
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=60
```

---

## ✅ Deployment Checklist

Before you deploy, make sure:

- [ ] Code is pushed to GitHub
- [ ] API key is ready (Groq/POE/Anthropic)
- [ ] Vercel account created
- [ ] `vercel.json` exists in root
- [ ] `requirements-vercel.txt` exists in backend folder
- [ ] `.vercelignore` is configured
- [ ] Environment variables prepared

After deployment:

- [ ] Test `/health` endpoint
- [ ] Test `/docs` API documentation
- [ ] Test frontend interface
- [ ] Send test chat message
- [ ] Check function logs
- [ ] Monitor analytics

---

## 🆘 Need Help?

### Vercel Documentation
- [Vercel Python Functions](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [Environment Variables](https://vercel.com/docs/projects/environment-variables)
- [Deployment Guide](https://vercel.com/docs/deployments/overview)

### Common Questions

**Q: Can I deploy without GitHub?**
A: Yes! Use `vercel` CLI or drag-and-drop in the Vercel dashboard.

**Q: How much does Vercel cost?**
A: Free tier is perfect for this project. Only upgrade if you exceed limits.

**Q: What about the database?**
A: SQLite works on Vercel but data is temporary. For production, use Vercel Postgres or Supabase.

**Q: How do I rollback a deployment?**
A: Go to Deployments → Previous deployment → Click "Promote to Production"

**Q: Can I use a different AI provider?**
A: Yes! Just change `AI_PROVIDER` environment variable and add the relevant API key.

---

## 🎊 You're All Set!

Your MSK Wellness Coach chatbot is now live on Vercel! 

**Your URLs:**
- Frontend: `https://your-project.vercel.app`
- API Docs: `https://your-project.vercel.app/docs`
- Health Check: `https://your-project.vercel.app/health`

Share your chatbot with the world! 🚀
