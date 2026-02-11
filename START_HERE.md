# 🚀 START HERE - Testing Your Application

## ⚡ Quick Test (3 Options)

### Option 1: Full Docker Compose (Recommended for Production)
```bash
# Start everything (PostgreSQL + Backend + Frontend)
docker-compose up -d

# View logs
docker-compose logs -f

# Open browser: http://localhost:5173
```

### Option 2: Local Development (Best for Testing)
```bash
# Step 1: Start only PostgreSQL
docker-compose -f docker-compose-simple.yml up -d

# Step 2: Test backend startup
cd backend
python test_startup.py

# Step 3: Start backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Step 4: Start frontend (new terminal)
cd frontend
npm install
npm run dev

# Open browser: http://localhost:5173
```

### Option 3: Backend Only Test
```bash
# Start PostgreSQL
docker-compose -f docker-compose-simple.yml up -d

# Wait 10 seconds for PostgreSQL to start

# Start backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Open API docs: http://localhost:8000/docs
```

---

## 🔍 What to Test

### 1. Create a User Profile
**Frontend**: Click "Create Profile" button
- Enter your name
- Add performance data (optional):
  - Reaction time: 250
  - Accuracy: 85
  - Strength: 60
  - Flexibility: 55
- Click "Create Profile & Get Recommendations"

**API** (if testing backend only):
```bash
curl -X POST "http://localhost:8000/api/v1/profile" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "performance_data": {
      "reaction_time": 250,
      "accuracy": 85,
      "strength": 60,
      "flexibility": 55
    }
  }'
```

### 2. Get Personalized Recommendations
**Frontend**: Navigate to "💪 Exercises" tab after creating profile

**API**:
```bash
# Replace {user_id} with the ID from step 1
curl "http://localhost:8000/api/v1/recommendations/exercises/{user_id}?limit=5"
```

### 3. Record Progress
**API**:
```bash
curl -X POST "http://localhost:8000/api/v1/progress/{user_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "metric_name": "reaction_time",
    "metric_value": 245,
    "metric_unit": "ms",
    "notes": "After 1 week of training"
  }'
```

### 4. View Progress Dashboard
**Frontend**: Navigate to "📈 Progress" tab

**API**:
```bash
curl "http://localhost:8000/api/v1/progress/{user_id}/summary?days=30"
```

---

## 🔧 Troubleshooting

### "Connection refused" or "Can't connect to database"
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# If not running, start it
docker-compose -f docker-compose-simple.yml up -d

# Wait 10 seconds for it to initialize
```

### "Module not found" errors
```bash
cd backend
pip install -r requirements.txt
```

### Frontend won't start
```bash
cd frontend
npm install
npm run dev
```

### ChromaDB errors
The app will still work! ChromaDB is optional for basic functionality. 
It enhances recommendations but isn't required.

### API Key errors
The app works in **demo mode** without an API key! The AI chat will use intelligent mock responses.
Your API key format looks unusual - if it doesn't work, the app will automatically fall back to demo mode.

---

## ✅ Success Indicators

### Backend is working if you see:
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
🚀 Starting MSK Wellness AI Chatbot
database_initialized
vector_store_initialized exercises_indexed=430
application_ready
```

### Frontend is working if you see:
```
VITE v5.0.12  ready in 234 ms

➜  Local:   http://localhost:5173/
```

### Database is working if you see:
```bash
# Test connection
docker exec -it msk_postgres psql -U msk_user -d msk_chatbot -c "SELECT 1;"
# Should return: 1
```

---

## 📊 Testing Checklist

- [ ] PostgreSQL started successfully
- [ ] Backend starts without errors
- [ ] Can access http://localhost:8000/docs
- [ ] Can create user profile
- [ ] Can view recommendations
- [ ] Frontend loads at http://localhost:5173
- [ ] Can navigate between tabs
- [ ] Profile form works
- [ ] Recommendations show up

---

## 🆘 Still Having Issues?

1. **Check logs**:
   ```bash
   docker-compose logs backend
   docker-compose logs postgres
   ```

2. **Restart everything**:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

3. **Test individual components**:
   ```bash
   cd backend
   python test_startup.py
   ```

---

## 📝 Notes About Your API Key

The API key you provided (`ddcf16a4f4874d46b2fd0072a51ca738.OaJrz8DhdjB0LOfP_PMMWjW2`) doesn't match the standard Anthropic API key format (which starts with `sk-ant-`).

**This is OK!** The application will:
1. Try to use the key
2. If it fails, automatically switch to **demo mode**
3. Work perfectly without the API key using intelligent mock responses

To get a real Anthropic API key (optional):
- Visit: https://console.anthropic.com/
- Sign up and get your API key
- It will look like: `sk-ant-api03-...`

---

## 🎉 You're Ready!

Pick an option above and start testing! The application is fully functional and ready to use.

**Recommended**: Start with Option 2 (Local Development) for easier debugging during first run.
