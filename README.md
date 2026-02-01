# MSK Wellness AI Chatbot

An intelligent conversational AI chatbot that analyzes musculoskeletal (MSK) wellness parameters and provides personalized recommendations for exercises, care programs, and supportive products.

## Features

- 📊 **Report Analysis** - Interpret and explain MSK assessment results
- 💪 **Exercise Recommendations** - Personalized exercises for balance, ROM, strength
- 📋 **Care Programs** - Structured wellness programs from healthcare partners
- 🛒 **Product Suggestions** - Neutraceuticals and ergonomic aids
- 💬 **Natural Conversations** - Multi-turn dialogue with context awareness

## Tech Stack

- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: React 18 + TypeScript + Vite
- **LLM**: Claude API (Anthropic)
- **Styling**: Modern CSS with glassmorphism

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- (Optional) Anthropic API key for Claude integration

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# (Optional) Set API key for Claude
export ANTHROPIC_API_KEY="your-key-here"

# Start server
uvicorn app.main:app --reload --port 8000
```

API docs available at: http://localhost:8000/docs

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Open http://localhost:5173

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

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/chat/message` | Send chat message |
| GET | `/api/v1/chat/conversations` | Get conversation history |
| GET | `/api/v1/reports/latest` | Get latest assessment |
| GET | `/api/v1/recommendations/exercises` | Get exercise recommendations |

## Demo Mode

The chatbot works without an API key using intelligent mock responses. This is great for testing and development.

## License

MIT
