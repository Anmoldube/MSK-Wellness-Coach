# MSK Wellness AI Chatbot 🎮💪

An intelligent AI-powered chatbot that analyzes **game/sport performance data** and provides **personalized exercise recommendations** to help athletes and gamers improve their physical performance.

## 🌟 Features

- 👤 **Simple Profile Creation** - No authentication, just enter your data
- 🎮 **Performance Data Input** - Gaming metrics (reaction time, accuracy, score)
- 💪 **AI-Powered Recommendations** - Personalized exercises based on YOUR data
- 📈 **Progress Tracking** - Track improvement over time with analytics
- 🔍 **Smart Matching** - ChromaDB vector search for relevant exercises
- 📁 **File Upload** - Upload performance reports (PDF, images, CSV)
- 💾 **Full Persistence** - PostgreSQL database, no data loss
- 🚀 **Production Ready** - Logging, error handling, rate limiting

## 🏗️ Tech Stack

- **Backend**: FastAPI (Python 3.11+) + SQLAlchemy + PostgreSQL
- **Frontend**: React 18 + TypeScript + Vite
- **AI/ML**: Anthropic Claude + ChromaDB Vector Search
- **Database**: PostgreSQL + ChromaDB
- **Styling**: Modern CSS with glassmorphism

## ⚡ Quick Start

### Prerequisites

- **Docker & Docker Compose** (recommended)
- OR: Python 3.11+ and Node.js 18+ (for local dev)

### 🚀 Option 1: Docker (One Command!)

**Windows:**
```powershell
.\start.ps1
```

**Mac/Linux:**
```bash
chmod +x start.sh
./start.sh
```

**Or manually:**
```bash
docker-compose up -d
```

Then open: **http://localhost:5173** 🎉

### 🛠️ Option 2: Local Development

**Step 1: Start PostgreSQL**
```bash
docker-compose -f docker-compose-simple.yml up -d
```

**Step 2: Backend**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Step 3: Frontend**
```bash
cd frontend
npm install
npm run dev
```

Open: http://localhost:5173

---

## 📖 Complete Documentation

- **[START_HERE.md](START_HERE.md)** - Testing guide with examples
- **[README_IMPLEMENTATION.md](README_IMPLEMENTATION.md)** - Full technical docs
- **[QUICK_START.md](QUICK_START.md)** - 3-step quick start
- **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Production deployment

## Project Structure

```
msk-chatbot/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI app
│   │   ├── api/endpoints/    # REST endpoints
│   │   ├── schemas/          # Pydantic models
│   │   └── services/         # Business logic (LLM, KB)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.tsx           # Main app
│   │   ├── components/chat/  # Chat UI components
│   │   ├── services/         # API client
│   │   └── hooks/            # React hooks
│   └── package.json
└── README.md
```

## 🎯 How It Works

1. **Create Profile** - Enter your name and performance data
2. **AI Analyzes** - System identifies strengths and weaknesses
3. **Get Recommendations** - Personalized exercises via AI vector search
4. **Track Progress** - Record metrics and see improvement trends

## 📋 API Endpoints

### Profile & Users
- `POST /api/v1/profile` - Create user profile
- `GET /api/v1/profile/{user_id}` - Get profile
- `PUT /api/v1/profile/{user_id}` - Update profile

### Personalized Recommendations ⭐
- `GET /api/v1/recommendations/exercises/{user_id}` - AI-powered exercises
- `GET /api/v1/recommendations/programs/{user_id}` - Care programs

### Progress Tracking ⭐
- `POST /api/v1/progress/{user_id}` - Record progress
- `GET /api/v1/progress/{user_id}/trends` - Get trends
- `GET /api/v1/progress/{user_id}/summary` - Analytics

### File Upload ⭐
- `POST /api/v1/upload/report/{user_id}` - Upload files
- `GET /api/v1/upload/reports/{user_id}` - List reports

### Chat
- `POST /api/v1/chat/message` - Send message
- `GET /api/v1/chat/conversations` - History

**Full API docs:** http://localhost:8000/docs

## 🔑 About the API Key

The app works in **demo mode** without an API key! Your provided key format is unusual, but the app will:
1. Try to use it
2. Fall back to demo mode if it fails
3. Still provide intelligent responses

For a real Anthropic key: https://console.anthropic.com/

## 📜 License

MIT
