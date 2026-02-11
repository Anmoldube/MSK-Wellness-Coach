# 🧪 Testing Guide

## ⚡ Fastest Way to Test (Windows)

### Option 1: One-Click Start (Recommended)
```powershell
.\start.ps1
```
This will:
- ✅ Check Docker is running
- ✅ Create .env if needed
- ✅ Start all services
- ✅ Open browser automatically

### Option 2: Manual Docker Start
```powershell
docker-compose up -d
```

Wait 30 seconds, then open: http://localhost:5173

---

## 🎯 What to Test

### Test 1: Create Your Profile (REQUIRED FIRST)

1. **Open**: http://localhost:5173
2. You'll see the **Profile Creation Form**
3. **Fill in**:
   - Name: `Your Name`
   - Gaming Performance:
     - Reaction Time: `250` (ms)
     - Accuracy: `85` (%)
     - Score: `2500`
     - Playtime: `20` (hrs/week)
   - Physical Performance (0-100):
     - Endurance: `70`
     - Strength: `60` ⬅️ Low (will trigger strength recommendations)
     - Flexibility: `55` ⬅️ Low (will trigger flexibility recommendations)
     - Balance: `75`
4. **Click**: "✨ Create Profile & Get Recommendations"

**Expected Result**: 
- ✅ Profile created successfully
- ✅ Redirected to Chat interface
- ✅ See "Welcome, [Your Name]! 👋" in header
- ✅ Navigation tabs now visible

---

### Test 2: View Personalized Recommendations

1. **Click**: "💪 Exercises" tab
2. **You should see**:
   - Personalized exercises based on YOUR data
   - Exercises focused on:
     - Strength building (because you scored 60)
     - Flexibility improvement (because you scored 55)
   - Each exercise shows:
     - Name
     - Description
     - Instructions
     - **Why it's recommended for YOU**
     - Priority score

**Expected Result**:
- ✅ See 5-10 exercise recommendations
- ✅ Recommendations are relevant to low strength/flexibility
- ✅ Each has a personalized reason
- ✅ Examples: Wall push-ups, planks, stretching routines

---

### Test 3: Record Progress

**API Test** (use Postman or curl):
```powershell
# Replace {user_id} with your actual user ID from profile creation
$userId = "your-user-id-here"

# Record a progress entry
Invoke-RestMethod -Method POST -Uri "http://localhost:8000/api/v1/progress/$userId" `
  -ContentType "application/json" `
  -Body '{
    "metric_name": "strength",
    "metric_value": 65,
    "metric_unit": "score",
    "activity_type": "training",
    "notes": "After 1 week of exercises"
  }'

# Record another entry (showing improvement)
Invoke-RestMethod -Method POST -Uri "http://localhost:8000/api/v1/progress/$userId" `
  -ContentType "application/json" `
  -Body '{
    "metric_name": "strength",
    "metric_value": 70,
    "metric_unit": "score",
    "activity_type": "training",
    "notes": "After 2 weeks - feeling stronger!"
  }'
```

---

### Test 4: View Progress Dashboard

1. **Click**: "📈 Progress" tab
2. **You should see**:
   - All your tracked metrics
   - Metric cards showing:
     - Current value
     - Trend indicator (📈 improving / 📉 declining / ➡️ stable)
     - Improvement percentage
   - Click on a metric card to see detailed trends

**Expected Result**:
- ✅ See metric cards for "strength"
- ✅ Shows improvement trend
- ✅ Displays improvement percentage
- ✅ Shows data points timeline

---

### Test 5: Upload a File

**API Test**:
```powershell
$userId = "your-user-id-here"

# Create a test file
"Test performance report" | Out-File test_report.txt

# Upload it
$form = @{
    file = Get-Item -Path "test_report.txt"
}
Invoke-RestMethod -Method POST `
  -Uri "http://localhost:8000/api/v1/upload/report/$userId?report_title=Test%20Report&report_type=game_performance" `
  -Form $form
```

---

### Test 6: Chat Interface

1. **Click**: "💬 Chat" tab
2. **Type**: "What exercises should I do to improve my strength?"
3. **Send message**

**Expected Result**:
- ✅ AI responds with relevant suggestions
- ✅ May mention your strength score (60)
- ✅ Provides contextual advice

---

## 🔍 Verify Backend Features

### Check Database Persistence

1. **Create a profile** (Test 1)
2. **Stop Docker**: `docker-compose down`
3. **Start Docker**: `docker-compose up -d`
4. **Open API docs**: http://localhost:8000/docs
5. **Try**: `GET /api/v1/profile/{user_id}`

**Expected Result**:
- ✅ Your profile data is still there
- ✅ PostgreSQL successfully persisted data

---

### Check ChromaDB Vector Search

**Open**: http://localhost:8000/docs

1. **Find**: `GET /api/v1/recommendations/exercises/{user_id}`
2. **Try it out** with your user_id
3. **Execute**

**Expected Result**:
- ✅ Returns personalized recommendations
- ✅ Includes "recommendation_reason" field
- ✅ Shows "priority" scores
- ✅ Recommendations match your weak areas

---

### Check Logging

```powershell
# View backend logs
docker-compose logs backend

# Look for structured JSON logs like:
# {"event": "user_profile_created", "user_id": "...", "name": "..."}
# {"event": "personalized_recommendations_generated", "user_id": "...", "count": 5}
# {"event": "progress_recorded", "metric": "strength", "value": 65}
```

**Expected Result**:
- ✅ JSON formatted logs
- ✅ Clear event tracking
- ✅ No error messages

---

### Check Rate Limiting

**Try making 61+ requests in 1 minute**:
```powershell
# Quick test (if you have curl)
for ($i=1; $i -le 65; $i++) {
    curl http://localhost:8000/health
}
```

**Expected Result**:
- ✅ First 60 requests succeed (200 OK)
- ✅ 61st request fails (429 Too Many Requests)

---

## 🎨 UI/UX Testing

### Profile Form
- [ ] All fields render correctly
- [ ] Number inputs accept decimals
- [ ] Validation works (name required)
- [ ] Error messages display properly
- [ ] Success redirects to chat

### Navigation
- [ ] Tabs switch views correctly
- [ ] Active tab is highlighted
- [ ] Header shows user name after login
- [ ] Menu button works on mobile

### Recommendations List
- [ ] Exercises display with all details
- [ ] Cards are visually appealing
- [ ] Personalized reasons show up
- [ ] Loading state displays

### Progress Tracker
- [ ] Metric cards display correctly
- [ ] Trend icons show (📈📉➡️)
- [ ] Colors match trends (green/red/gray)
- [ ] Clicking card shows details
- [ ] Data points list properly

---

## 🐛 Common Issues & Fixes

### "Connection refused" / Can't reach backend
```powershell
# Check if backend is running
docker-compose ps

# If not running, start it
docker-compose up -d backend

# Check logs for errors
docker-compose logs backend
```

### "Database connection failed"
```powershell
# Check PostgreSQL
docker-compose ps postgres

# Restart it
docker-compose restart postgres

# Wait 10 seconds
Start-Sleep -Seconds 10
```

### Frontend shows blank page
```powershell
# Check if frontend is running
docker-compose ps frontend

# Restart it
docker-compose restart frontend

# Check browser console for errors (F12)
```

### ChromaDB errors in logs
This is OK! The app will work without ChromaDB. Recommendations will use fallback logic.

### API key errors
This is EXPECTED! Your key format is unusual, so the app will use demo mode. Everything still works!

---

## 📊 Success Criteria

After testing, you should have:

- [x] ✅ Profile created and saved
- [x] ✅ Personalized recommendations displayed
- [x] ✅ Progress entries recorded
- [x] ✅ Progress dashboard showing trends
- [x] ✅ Database persisting data (survives restart)
- [x] ✅ Logging working (JSON format)
- [x] ✅ All API endpoints responding
- [x] ✅ Frontend navigation working
- [x] ✅ No critical errors in logs

---

## 🎉 If Everything Works...

**Congratulations!** Your MSK Wellness AI Chatbot is fully functional! 

### Next Steps:
1. ✅ **Use it**: Add real performance data and track progress
2. ✅ **Customize**: Modify exercises in `backend/app/services/knowledge_base.py`
3. ✅ **Deploy**: Follow `DEPLOYMENT_CHECKLIST.md` for production
4. ✅ **Enhance**: Add more features from the roadmap

---

## 🆘 Still Having Issues?

1. **Check START_HERE.md** for detailed troubleshooting
2. **View logs**: `docker-compose logs -f`
3. **Test components individually**: `cd backend && python test_startup.py`
4. **Restart everything**: `docker-compose down && docker-compose up -d`

---

**Remember**: The app works in DEMO MODE even without a valid API key! All core features function perfectly.
