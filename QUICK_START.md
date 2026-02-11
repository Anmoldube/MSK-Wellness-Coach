# 🚀 Quick Start Guide

## Start in 3 Steps

### 1. Copy Environment File
```bash
cp .env.example .env
```

### 2. Start All Services
```bash
docker-compose up -d
```

### 3. Open Your Browser
Go to: **http://localhost:5173**

---

## First Time Setup

1. **Create Your Profile**
   - Enter your name (required)
   - Add your gaming/sports performance data:
     - Reaction time (e.g., 250 ms)
     - Accuracy (e.g., 85%)
     - Endurance, strength, flexibility, balance (0-100)
   - Click "Create Profile"

2. **Get Personalized Recommendations**
   - Navigate to the "💪 Exercises" tab
   - View AI-powered recommendations based on your data
   - See WHY each exercise is recommended for you

3. **Track Your Progress**
   - Navigate to the "📈 Progress" tab
   - Record your metrics over time
   - Watch your improvement!

---

## What's Running?

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432

---

## Stop Services
```bash
docker-compose down
```

## View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f postgres
```

---

## Need Help?

Check the full documentation in `README_IMPLEMENTATION.md`
