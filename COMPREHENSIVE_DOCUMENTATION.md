# 🏥 MSK Wellness Coach - Comprehensive Technical Documentation

**Version:** 1.0.0  
**Last Updated:** February 18, 2026  
**Author:** MSK Development Team

---

## 📑 Table of Contents

1. [Executive Summary](#executive-summary)
2. [System Architecture](#system-architecture)
3. [Technology Stack](#technology-stack)
4. [Core Components](#core-components)
5. [Database Schema](#database-schema)
6. [API Reference](#api-reference)
7. [AI & Machine Learning](#ai--machine-learning)
8. [Data Flow](#data-flow)
9. [Security & Performance](#security--performance)
10. [Deployment Guide](#deployment-guide)
11. [Development Guide](#development-guide)
12. [Troubleshooting](#troubleshooting)

---

## 📋 Executive Summary

### What is MSK Wellness Coach?

**MSK Wellness Coach** is an intelligent AI-powered chatbot system designed to analyze musculoskeletal (MSK) health data from gaming and sports performance metrics. It provides personalized exercise recommendations, tracks progress over time, and offers comprehensive wellness guidance through an interactive conversational interface.

### Key Value Propositions

- 🎯 **Personalized Health Insights**: AI analyzes individual performance data to provide tailored recommendations
- 💪 **Exercise Recommendations**: Smart matching of exercises based on user's specific weaknesses and goals
- 📈 **Progress Tracking**: Monitor improvement over time with detailed analytics and trend analysis
- 🤖 **Conversational AI**: Natural language interface powered by state-of-the-art LLM models
- 🔄 **Multi-Modal Input**: Accept text, uploaded reports (PDF, images), and structured performance data
- 📊 **Comprehensive Reporting**: Generate detailed health reports with risk assessments

### Target Users

- **Esports Athletes & Gamers**: Improve reaction time, posture, and prevent gaming-related injuries
- **Sports Enthusiasts**: Track and improve athletic performance metrics
- **Physical Therapists**: Monitor patient progress and recommend exercises
- **Wellness Coaches**: Provide data-driven recommendations to clients
- **General Users**: Anyone interested in improving musculoskeletal health

---


## ??? System Architecture

### High-Level Architecture

```
+-----------------------------------------------------------------+
�                        CLIENT LAYER                              �
�  +--------------------------------------------------------+     �
�  �         React 18 + TypeScript Frontend                 �     �
�  �  � ChatInterface  � Profile  � Dashboard  � Progress   �     �
�  +--------------------------------------------------------+     �
+-----------------------------------------------------------------+
                            � HTTPS/REST API
+---------------------------?-------------------------------------+
�                      API GATEWAY LAYER                           �
�  +--------------------------------------------------------+     �
�  �              FastAPI Application                        �     �
�  �  � CORS  � Rate Limiting  � Error Handling             �     �
�  +--------------------------------------------------------+     �
+-----------------------------------------------------------------+
                            �
+---------------------------?-------------------------------------+
�                    BUSINESS LOGIC LAYER                          �
�  +--------------+  +--------------+  +--------------+          �
�  � LLM Service  �  � Context Mgr  �  � Recommend.   �          �
�  �              �  �              �  � Engine       �          �
�  +--------------+  +--------------+  +--------------+          �
�  +--------------+  +--------------+  +--------------+          �
�  � Knowledge    �  � Vector Store �  � File Upload  �          �
�  � Base Service �  � (ChromaDB)   �  � Handler      �          �
�  +--------------+  +--------------+  +--------------+          �
+-----------------------------------------------------------------+
                            �
+---------------------------?-------------------------------------+
�                      DATA LAYER                                  �
�  +----------------+         +----------------+                  �
�  � SQLite Database�         � ChromaDB       �                  �
�  � (SQLAlchemy)   �         � Vector Store   �                  �
�  �                �         �                �                  �
�  � � Users        �         � � Embeddings   �                  �
�  � � Conversations�         � � Exercise     �                  �
�  � � Messages     �         �   Search       �                  �
�  � � Reports      �         �                �                  �
�  � � Progress     �         �                �                  �
�  +----------------+         +----------------+                  �
+-----------------------------------------------------------------+
                            �
+---------------------------?-------------------------------------+
�                    EXTERNAL SERVICES                             �
�  +--------------+  +--------------+  +--------------+          �
�  � Groq API     �  � Anthropic    �  � OpenAI       �          �
�  � (LLaMA 3.3)  �  � (Claude)     �  � (GPT-4)      �          �
�  +--------------+  +--------------+  +--------------+          �
+-----------------------------------------------------------------+
```

### Architecture Patterns

#### 1. **Layered Architecture**
- **Presentation Layer**: React frontend with component-based architecture
- **API Layer**: FastAPI with RESTful endpoints
- **Business Logic Layer**: Service-oriented architecture with specialized services
- **Data Layer**: Database abstraction using SQLAlchemy ORM

#### 2. **Microservice-Ready Design**
- Services are loosely coupled and communicate through well-defined interfaces
- Each service can be independently scaled or replaced
- Vector store (ChromaDB) operates independently

#### 3. **Repository Pattern**
- Database operations abstracted through SQLAlchemy models
- Easy to switch database backends (SQLite ? PostgreSQL)

#### 4. **Dependency Injection**
- FastAPI dependency injection for database sessions
- Service initialization separated from usage

---

## ?? Technology Stack

### Backend Technologies

#### **Core Framework**
- **FastAPI 0.104+**: Modern, high-performance Python web framework.
  - Automatic API documentation (OpenAPI/Swagger)
  - Built-in data validation with Pydantic
  - Async/await support for concurrent operations
  - Type hints for better code quality

#### **Database & ORM**
- **SQLite**: Lightweight embedded database for development
  - File-based storage (`msk_chatbot.db`)
  - Zero configuration required
  - Easily upgradeable to PostgreSQL for production
  
- **SQLAlchemy 2.0**: Python SQL toolkit and ORM
  - Async support with `asyncio`
  - Type-safe database models
  - Migration support via Alembic

#### **AI & Machine Learning**
- **Groq API**: Fast inference for LLaMA 3.3 70B model
  - 500+ tokens/second generation speed
  - Free tier available
  - Advanced reasoning capabilities

- **Anthropic Claude**: Alternative LLM provider
  - Claude Sonnet 4 (latest model)
  - Superior reasoning and long-context understanding
  - Function calling support

- **ChromaDB**: Vector database for semantic search
  - Embedding-based exercise recommendations
  - Similarity search for relevant content
  - Persistent storage of embeddings

#### **Utilities & Libraries**
- **Pydantic**: Data validation and settings management
- **structlog**: Structured logging for better observability
- **python-multipart**: File upload support
- **uvicorn**: ASGI server for production deployment

### Frontend Technologies

#### **Core Framework**
- **React 18**: Modern UI library with hooks
  - Functional components with hooks pattern
  - Concurrent rendering for better UX
  - Suspense for loading states

- **TypeScript**: Type-safe JavaScript
  - Compile-time type checking
  - Better IDE support and autocompletion
  - Reduced runtime errors

#### **Build Tools**
- **Vite**: Next-generation frontend build tool
  - Lightning-fast HMR (Hot Module Replacement)
  - Optimized production builds
  - Native ESM support

#### **Styling**
- **CSS Modules**: Component-scoped styling
- **Modern CSS Features**: Grid, Flexbox, Custom Properties
- **Glassmorphism Design**: Contemporary UI aesthetic

#### **State Management**
- **React Hooks**: `useState`, `useEffect`, `useCallback`, `useRef`
- **Custom Hooks**: `useChat` for chat functionality

### DevOps & Deployment

- **Docker**: Containerization for consistent environments
- **Docker Compose**: Multi-container orchestration
- **Vercel**: Serverless deployment platform (optional)
- **Git**: Version control

---


## ?? Core Components

### Backend Components

#### 1. **Database Models** (`app/models/`)

##### User Model (`user.py`)
```python
class User(Base):
    id: str (UUID)                    # Unique user identifier
    name: str                         # User's name
    created_at: DateTime              # Account creation timestamp
    updated_at: DateTime              # Last update timestamp
    performance_data: JSON            # User's game/sport metrics
    
    # Relationships
    reports: List[Report]             # User's assessment reports
    conversations: List[Conversation] # Chat history
    progress_records: List[Progress]  # Progress tracking data
```

**Performance Data Structure:**
```json
{
  "reaction_time": 250,        // milliseconds
  "accuracy": 85,              // percentage
  "score": 1200,              // game score
  "balance_score": 7,         // 0-10 scale
  "endurance": 75,            // percentage
  "rom_shoulder": 160         // degrees
}
```

##### Conversation Model (`conversation.py`)
```python
class Conversation(Base):
    id: str (UUID)                    # Conversation identifier
    user_id: str (FK)                 # Foreign key to User
    created_at: DateTime              # Session start time
    updated_at: DateTime              # Last message time
    title: str (optional)             # Conversation title
    
    # Relationships
    user: User
    messages: List[Message]           # Ordered message history

class Message(Base):
    id: str (UUID)                    # Message identifier
    conversation_id: str (FK)         # Foreign key to Conversation
    created_at: DateTime              # Message timestamp
    role: str                         # "user" or "assistant"
    content: Text                     # Message text content
    sequence: int                     # Message order in conversation
```

##### Report Model (`report.py`)
```python
class Report(Base):
    id: str (UUID)                    # Report identifier
    user_id: str (FK)                 # Foreign key to User
    created_at: DateTime              # Report generation time
    title: str                        # Report title
    report_type: str                  # "game_performance", "sport_assessment"
    metrics: JSON                     # Performance metrics data
    file_path: str (optional)         # Uploaded file path
    file_name: str (optional)         # Original filename
    analysis_summary: Text (optional) # AI-generated summary
    risk_score: float (optional)      # 0-100 risk assessment
```

##### Progress Model (`progress.py`)
```python
class Progress(Base):
    id: str (UUID)                    # Progress record identifier
    user_id: str (FK)                 # Foreign key to User
    recorded_at: DateTime             # Measurement timestamp
    metric_name: str                  # "reaction_time", "balance", etc.
    metric_value: float               # Measured value
    metric_unit: str (optional)       # "ms", "%", "score"
    activity_type: str (optional)     # "gaming", "training", "assessment"
    notes: Text (optional)            # User notes
    extra_data: JSON                  # Additional metadata
```

#### 2. **Services** (`app/services/`)

##### LLM Service (`llm_service.py`)
**Purpose**: Handles all AI interactions with language models

**Key Features:**
- Multi-provider support (Groq, Anthropic, OpenAI, Gemini, Poe)
- Conversation history management
- Context-aware responses
- Streaming support for real-time responses
- Function calling capabilities
- Fallback to mock responses when API unavailable

**Main Methods:**
```python
class LLMService:
    async def chat(
        user_message: str,
        conversation_history: List[Dict],
        include_context: bool = True,
        user_context: Dict = None
    ) -> Dict[str, Any]
    
    async def stream_chat(...) -> AsyncGenerator
    
    def _build_messages(
        user_message: str,
        history: List[Dict],
        system_context: str
    ) -> List[Dict]
```

**Provider Configuration:**
```python
# In config.py
AI_PROVIDER: str = "groq"  # or "anthropic", "openai", "gemini", "poe"

# Groq (Recommended - Fast & Free)
GROQ_API_KEY: str
GROQ_MODEL: str = "llama-3.3-70b-versatile"

# Anthropic Claude
ANTHROPIC_API_KEY: str
CLAUDE_MODEL: str = "claude-sonnet-4-20250514"

# OpenAI
OPENAI_API_KEY: str
OPENAI_MODEL: str = "gpt-4"
```

##### Context Manager (`context_manager.py`)
**Purpose**: Manages conversation state and user context

**Key Features:**
- Conversation context tracking
- User intent analysis
- Parameter extraction from messages
- Recommendation tracking
- Auto-cleanup of old conversations

**Main Methods:**
```python
class ContextManager:
    def get_or_create_context(conversation_id: str, user_id: str) -> Dict
    
    def add_message(conversation_id: str, role: str, content: str, metadata: Dict)
    
    def get_recent_messages(conversation_id: str, limit: int) -> List[Dict]
    
    def analyze_user_intent(message: str) -> Dict:
        # Returns:
        # {
        #     "primary_intent": "exercise_request",
        #     "parameters_mentioned": ["balance", "rom"],
        #     "action_requested": "improve",
        #     "sentiment": "neutral"
        # }
    
    def track_recommendation(conversation_id: str, recommendation_type: str, items: List)
    
    def cleanup_old_conversations(max_age_hours: int) -> int
```

##### Recommendation Engine (`recommendation_engine.py`)
**Purpose**: Generates personalized exercise recommendations using AI and vector search

**Key Features:**
- Performance data analysis
- Weakness identification
- Vector search for relevant exercises
- Priority-based ranking
- Personalized reasoning for each recommendation

**Main Methods:**
```python
class RecommendationEngine:
    def generate_recommendations(
        user_performance_data: Dict[str, Any],
        limit: int = 5
    ) -> List[Dict[str, Any]]
    
    def _analyze_performance(performance_data: Dict) -> Dict:
        # Returns analysis with:
        # - strengths: List[str]
        # - weaknesses: List[str]
        # - focus_areas: List[str]
        # - overall_health: str ("excellent", "good", "needs_improvement")
    
    def _create_search_query(analysis: Dict) -> str
    
    def _calculate_priority(exercise: Dict, analysis: Dict) -> float
```

**Analysis Logic:**
```python
# Performance thresholds
GOOD_THRESHOLDS = {
    "reaction_time": 200,      # < 200ms is good
    "accuracy": 80,            # > 80% is good
    "balance_score": 7,        # > 7/10 is good
    "endurance": 70,           # > 70% is good
    "rom_shoulder": 150,       # > 150� is good
}

# Identifies weaknesses below thresholds
# Generates targeted search queries
# Prioritizes exercises addressing multiple weaknesses
```

##### Vector Store (`vector_store.py`)
**Purpose**: Semantic search for exercises using ChromaDB

**Key Features:**
- Embedding-based similarity search
- Persistent storage
- Metadata filtering
- Collection management

**Main Methods:**
```python
class VectorStoreService:
    def search_exercises(query: str, n_results: int = 5) -> List[Dict]
    
    def add_exercise(exercise_id: str, description: str, metadata: Dict)
    
    def get_collection_stats() -> Dict
```

##### Knowledge Base (`knowledge_base.py`)
**Purpose**: Static knowledge repository for exercises, programs, and products

**Data Structure:**
```python
class KnowledgeBaseService:
    exercises: List[Dict] = [
        {
            "exercise_id": "ex_001",
            "name": "Single-Leg Balance",
            "category": "balance",
            "difficulty": "beginner",
            "description": "Stand on one leg for 30 seconds...",
            "duration": "30 seconds",
            "repetitions": "3 sets per leg",
            "equipment": "none",
            "benefits": ["improves balance", "strengthens ankles"],
            "contraindications": ["ankle injury", "severe vertigo"]
        },
        # ... 50+ exercises
    ]
    
    care_programs: List[Dict] = [...]  # Structured care programs
    
    products: List[Dict] = [...]       # Recommended products
```

#### 3. **API Endpoints** (`app/api/endpoints/`)

##### Chat Endpoints (`chat.py`)
```python
POST   /api/v1/chat/message           # Send message, get AI response
POST   /api/v1/chat/send              # Alias for /message
GET    /api/v1/chat/conversations     # List user conversations
GET    /api/v1/chat/conversations/{id} # Get specific conversation
DELETE /api/v1/chat/conversations/{id} # Delete conversation
```

**Request/Response:**
```python
# Request
{
    "message": "How can I improve my balance?",
    "conversation_id": "conv_123" (optional),
    "include_context": true,
    "user_id": "user_456"
}

# Response
{
    "message": "Based on your balance score of 6/10...",
    "conversation_id": "conv_123",
    "function_calls": [],
    "citations": [],
    "suggested_questions": [
        "What exercises can help?",
        "How often should I practice?"
    ]
}
```

##### Profile Endpoints (`profile.py`)
```python
POST   /api/v1/profile                # Create user profile
GET    /api/v1/profile/{user_id}      # Get profile
PUT    /api/v1/profile/{user_id}      # Update profile
DELETE /api/v1/profile/{user_id}      # Delete profile
```

##### Recommendations Endpoints (`recommendations.py`)
```python
GET /api/v1/recommendations/exercises?user_id={id}&target={param}
GET /api/v1/recommendations/programs?user_id={id}&focus_areas={areas}
GET /api/v1/recommendations/products?condition={condition}
```

##### Progress Endpoints (`progress.py`)
```python
POST /api/v1/progress/{user_id}              # Record progress
GET  /api/v1/progress/{user_id}              # Get all progress
GET  /api/v1/progress/{user_id}/trends       # Get trends analysis
GET  /api/v1/progress/{user_id}/summary      # Get summary stats
```

##### Upload Endpoints (`upload.py`)
```python
POST /api/v1/upload/report/{user_id}         # Upload file
GET  /api/v1/upload/reports/{user_id}        # List uploads
GET  /api/v1/upload/report/{report_id}       # Get specific report
```

---


### Frontend Components

#### 1. **Chat Components** (`src/components/chat/`)

##### ChatInterface.tsx
**Purpose**: Main chat container component

**Features:**
- Manages chat state using `useChat` hook
- Displays message list
- Handles message input
- Shows suggested questions
- Auto-scrolls to latest message

**Props:**
```typescript
interface ChatInterfaceProps {
    userId: string;  // Current user ID
}
```

##### MessageBubble.tsx
**Purpose**: Individual message display component

**Features:**
- Renders user/assistant messages with different styles
- Markdown rendering support
- Loading animation for AI responses
- Timestamp display
- Copy to clipboard functionality

**Props:**
```typescript
interface MessageBubbleProps {
    message: ChatMessage;
}

interface ChatMessage {
    id: string;
    role: 'user' | 'assistant';
    content: string;
    timestamp: Date;
    suggestedQuestions?: string[];
    isLoading?: boolean;
}
```

##### MessageInput.tsx
**Purpose**: Message input field with send button

**Features:**
- Multi-line text input
- Enter to send (Shift+Enter for new line)
- Character limit display
- Disabled state during loading
- Auto-focus on mount

**Props:**
```typescript
interface MessageInputProps {
    onSend: (message: string) => void;
    disabled: boolean;
    isLoading: boolean;
}
```

##### SuggestedQuestions.tsx
**Purpose**: Display clickable suggested questions

**Features:**
- Chip-style buttons
- Smooth fade-in animation
- Click to auto-fill and send

**Props:**
```typescript
interface SuggestedQuestionsProps {
    questions: string[];
    onSelect: (question: string) => void;
}
```

##### Sidebar.tsx
**Purpose**: Conversation history and navigation

**Features:**
- List of previous conversations
- New conversation button
- Search conversations
- Conversation metadata (date, message count)

#### 2. **Other Components**

##### ProfileForm.tsx (`src/components/profile/`)
**Purpose**: User profile creation and editing

**Features:**
- Name input
- Performance data inputs (reaction time, accuracy, etc.)
- Form validation
- Save/update functionality

##### ProgressTracker.tsx (`src/components/progress/`)
**Purpose**: Display progress trends over time

**Features:**
- Line charts for metrics
- Date range filtering
- Comparison with previous periods
- Export data functionality

##### RecommendationList.tsx (`src/components/recommendations/`)
**Purpose**: Display exercise/program recommendations

**Features:**
- Card-based layout
- Difficulty badges
- Equipment requirements
- Expand for details

##### ReportDashboard.tsx (`src/components/dashboard/`)
**Purpose**: Overview of user's health data

**Features:**
- Overall score visualization
- Risk level indicator
- Parameter breakdown
- Recent reports list

#### 3. **Custom Hooks** (`src/hooks/`)

##### useChat.ts
**Purpose**: Manage chat state and logic

**State Management:**
```typescript
const useChat = (userId: string) => {
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [conversationId, setConversationId] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [suggestedQuestions, setSuggestedQuestions] = useState<string[]>([]);
    
    // Returns:
    return {
        messages,
        isLoading,
        error,
        suggestedQuestions,
        sendMessage,
        clearConversation,
        messagesEndRef
    };
}
```

**Key Functions:**
- `sendMessage(content: string)`: Send user message and get AI response
- `clearConversation()`: Reset chat state
- Auto-scroll to bottom on new messages
- Initial welcome message on mount

#### 4. **Services** (`src/services/`)

##### api.service.ts
**Purpose**: API client for backend communication

**Methods:**
```typescript
class ApiService {
    // Chat
    async sendMessage(request: ChatRequest): Promise<ChatResponse>
    async getConversations(limit?: number)
    
    // Reports
    async getLatestReport(): Promise<AssessmentReport>
    async getReports(limit?: number)
    
    // Recommendations
    async getCarePrograms(focusAreas?: string[])
    async getExercises(targetParameter?: string)
    async getProducts(condition?: string)
    
    // Health
    async healthCheck(): Promise<{ status: string }>
}
```

**Error Handling:**
```typescript
private async request<T>(endpoint: string, options: RequestInit): Promise<T> {
    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || `HTTP ${response.status}`);
        }
        return response.json();
    } catch (error) {
        // Handle network errors, timeouts, etc.
    }
}
```

---

## ??? Database Schema

### Entity Relationship Diagram

```
+-----------------+
�     User        �
+-----------------�
� id (PK)         �?-----+
� name            �      �
� created_at      �      �
� updated_at      �      �
� performance_data�      �
+-----------------+      �
                         �
                         � 1:N
         +---------------+---------------------------------+
         �               �               �                 �
         ?               ?               ?                 ?
+-------------+  +--------------+  +----------+  +--------------+
�Conversation �  �   Report     �  � Progress �  �              �
+-------------�  +--------------�  +----------�  �              �
� id (PK)     �  � id (PK)      �  � id (PK)  �  �              �
� user_id (FK)�  � user_id (FK) �  �user_id   �  �              �
� created_at  �  � created_at   �  �          �  �              �
� updated_at  �  � title        �  �recorded  �  �              �
� title       �  � report_type  �  �  _at     �  �              �
+-------------+  � metrics      �  �metric    �  �              �
       �         � file_path    �  � _name    �  �              �
       � 1:N     � file_name    �  �metric    �  �              �
       �         � analysis     �  � _value   �  �              �
       ?         � risk_score   �  �metric    �  �              �
+-------------+  +--------------+  � _unit    �  �              �
�   Message   �                    �activity  �  �              �
+-------------�                    � _type    �  �              �
� id (PK)     �                    �notes     �  �              �
�conversation �                    �extra     �  �              �
�  _id (FK)   �                    � _data    �  �              �
� created_at  �                    +----------+  �              �
� role        �                                  �              �
� content     �                                  �              �
� sequence    �                                  �              �
+-------------+                                  +--------------+
```

### Table Definitions

#### users
```sql
CREATE TABLE users (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    performance_data JSON
);
```

#### conversations
```sql
CREATE TABLE conversations (
    id VARCHAR PRIMARY KEY,
    user_id VARCHAR NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    title VARCHAR,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

#### messages
```sql
CREATE TABLE messages (
    id VARCHAR PRIMARY KEY,
    conversation_id VARCHAR NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    role VARCHAR NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    sequence INTEGER NOT NULL,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
);
```

#### reports
```sql
CREATE TABLE reports (
    id VARCHAR PRIMARY KEY,
    user_id VARCHAR NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    title VARCHAR NOT NULL,
    report_type VARCHAR NOT NULL,
    metrics JSON,
    file_path VARCHAR,
    file_name VARCHAR,
    analysis_summary TEXT,
    risk_score FLOAT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

#### progress
```sql
CREATE TABLE progress (
    id VARCHAR PRIMARY KEY,
    user_id VARCHAR NOT NULL,
    recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    metric_name VARCHAR NOT NULL,
    metric_value FLOAT NOT NULL,
    metric_unit VARCHAR,
    activity_type VARCHAR,
    notes TEXT,
    extra_data JSON,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### Indexes

```sql
-- Performance optimization indexes
CREATE INDEX idx_messages_conversation ON messages(conversation_id, sequence);
CREATE INDEX idx_reports_user ON reports(user_id, created_at DESC);
CREATE INDEX idx_progress_user_metric ON progress(user_id, metric_name, recorded_at);
CREATE INDEX idx_conversations_user ON conversations(user_id, updated_at DESC);
```

---

## ?? API Reference

### Base URL

**Development:** `http://localhost:8000/api/v1`  
**Production:** `https://your-domain.com/api/v1`

### Authentication

Currently **no authentication required** (simplified for demo). In production, add:
- JWT tokens
- API keys
- OAuth2 integration

### Common Response Format

**Success Response:**
```json
{
    "data": { ... },
    "status": "success",
    "timestamp": "2026-02-18T20:00:00Z"
}
```

**Error Response:**
```json
{
    "detail": "Error message",
    "status_code": 400,
    "timestamp": "2026-02-18T20:00:00Z"
}
```

### Endpoint Details

#### Chat Endpoints

**POST /chat/message**

Send a message and receive AI response.

**Request Body:**
```json
{
    "message": "How can I improve my balance?",
    "conversation_id": "conv_123",  // optional
    "include_context": true,
    "user_id": "user_456"
}
```

**Response:**
```json
{
    "message": "Based on your balance score...",
    "conversation_id": "conv_123",
    "function_calls": [],
    "citations": [],
    "suggested_questions": [
        "What exercises help with balance?",
        "How often should I practice?"
    ]
}
```

**GET /chat/conversations**

List user's conversations.

**Query Parameters:**
- `limit` (int, default=10): Number of conversations to return
- `offset` (int, default=0): Pagination offset

**Response:**
```json
[
    {
        "conversation_id": "conv_123",
        "started_at": "2026-02-18T10:00:00Z",
        "message_count": 15,
        "last_message_preview": "Based on your assessment..."
    }
]
```

#### Profile Endpoints

**POST /profile**

Create new user profile.

**Request Body:**
```json
{
    "name": "John Doe",
    "performance_data": {
        "reaction_time": 250,
        "accuracy": 85,
        "score": 1200,
        "balance_score": 7,
        "endurance": 75
    }
}
```

**Response:**
```json
{
    "id": "user_789",
    "name": "John Doe",
    "created_at": "2026-02-18T10:00:00Z",
    "performance_data": { ... }
}
```

**GET /profile/{user_id}**

Get user profile.

**PUT /profile/{user_id}**

Update user profile.

#### Recommendations Endpoints

**GET /recommendations/exercises**

Get personalized exercise recommendations.

**Query Parameters:**
- `user_id` (required): User identifier
- `target_parameter` (optional): Specific parameter to target

**Response:**
```json
[
    {
        "exercise_id": "ex_001",
        "name": "Single-Leg Balance",
        "category": "balance",
        "difficulty": "beginner",
        "description": "Stand on one leg...",
        "duration": "30 seconds",
        "repetitions": "3 sets per leg",
        "equipment": "none",
        "benefits": ["improves balance", "strengthens ankles"],
        "recommendation_reason": "Your balance score of 6/10 indicates...",
        "priority": 0.95
    }
]
```

#### Progress Endpoints

**POST /progress/{user_id}**

Record progress measurement.

**Request Body:**
```json
{
    "metric_name": "reaction_time",
    "metric_value": 230,
    "metric_unit": "ms",
    "activity_type": "gaming",
    "notes": "After 2 weeks of practice"
}
```

**GET /progress/{user_id}/trends**

Get progress trends analysis.

**Response:**
```json
{
    "metrics": {
        "reaction_time": {
            "current": 230,
            "previous": 250,
            "change_percent": -8.0,
            "trend": "improving",
            "data_points": [
                {"date": "2026-02-01", "value": 250},
                {"date": "2026-02-15", "value": 230}
            ]
        }
    },
    "overall_improvement": 12.5
}
```

---


`## ?? AI & Machine Learning

### LLM Integration

#### Supported Providers

The system supports **5 different AI providers** with automatic fallback:

1. **Groq API** (Recommended - Fast & Free)
   - Model: LLaMA 3.3 70B Versatile
   - Speed: 500+ tokens/second
   - Context: 32K tokens
   - Free tier: Generous limits

2. **Anthropic Claude**
   - Model: Claude Sonnet 4
   - Superior reasoning
   - Context: 200K tokens
   - Function calling support

3. **OpenAI**
   - Model: GPT-4
   - Well-tested and reliable
   - Context: 128K tokens

4. **Google Gemini**
   - Model: Gemini Pro
   - Multi-modal capabilities
   - Free tier available

5. **Poe API**
   - Access to multiple models
   - Bot-based architecture
   - Various model options

#### Provider Configuration

**Environment Variables:**
```bash
# Choose provider
AI_PROVIDER=groq  # Options: groq, anthropic, openai, gemini, poe

# API Keys (only one required based on provider)
GROQ_API_KEY=gsk_xxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxx
OPENAI_API_KEY=sk-xxxxx
GEMINI_API_KEY=xxxxx
POE_API_KEY=xxxxx
```

**Automatic Initialization:**
```python
class LLMService:
    def _init_client(self):
        provider = settings.AI_PROVIDER.lower()
        
        if provider == "groq":
            from groq import Groq
            self.groq_client = Groq(api_key=settings.GROQ_API_KEY)
        elif provider == "anthropic":
            import anthropic
            self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        # ... other providers
```

### Prompt Engineering

#### System Prompt

The system uses a comprehensive system prompt that defines:

1. **Role Definition**: MSK wellness coach AI assistant
2. **Capabilities**: Analysis, recommendations, tracking
3. **Guidelines**: Safety-first, evidence-based, empathetic
4. **Response Format**: Markdown, actionable steps, follow-ups
5. **Parameter Definitions**: Medical terminology explanations
6. **Risk Levels**: Low/Moderate/High classification

**Key Sections:**
```python
SYSTEM_PROMPT = """
You are an expert musculoskeletal (MSK) wellness coach AI assistant.

## Your Capabilities
- Analyze MSK assessment parameters (Balance, Reaction Time, ROM, Strength)
- Recommend personalized care programs
- Suggest specific exercises
- Recommend supportive products
- Track conversation context

## Guidelines
1. Base recommendations on actual assessment data
2. Be encouraging and supportive
3. Explain technical terms simply
4. Prioritize safety
5. Use available tools
6. Cite sources
7. Acknowledge limitations

## Response Format
- Conversational and empathetic
- Markdown formatting
- Bullet points for lists
- Actionable next steps
- 2-3 follow-up questions
- Appropriate emojis (?? ?? ? ??)
"""
```

#### Context Management

**User Context Injection:**
```python
USER_CONTEXT_TEMPLATE = """
[User's Latest MSK Assessment - {assessment_date}]
Overall Score: {overall_score}/100
Risk Level: {risk_level}

Key Parameters:
{parameters_summary}

Areas of Concern:
{areas_of_concern}
"""
```

**Conversation History:**
```python
# Recent messages included for context
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": "Previous message 1"},
    {"role": "assistant", "content": "Previous response 1"},
    {"role": "user", "content": "Current message"}
]
```

#### Intent Classification

The system analyzes user messages to determine intent:

```python
def analyze_user_intent(message: str) -> Dict:
    intent_keywords = {
        "report_analysis": ["report", "assessment", "results", "score"],
        "exercise_request": ["exercise", "workout", "train", "improve"],
        "program_inquiry": ["program", "care program", "enroll"],
        "product_inquiry": ["product", "supplement", "buy"],
        "information_request": ["what is", "explain", "tell me about"]
    }
    
    # Parameter extraction
    parameter_keywords = {
        "balance": ["balance", "stability", "fall"],
        "reaction_time": ["reaction", "response", "reflex"],
        "rom": ["range of motion", "flexibility", "stretch"],
        "strength": ["strength", "power", "muscle"],
        "endurance": ["endurance", "stamina", "cardio"]
    }
    
    return {
        "primary_intent": "...",
        "parameters_mentioned": [...],
        "action_requested": "...",
        "sentiment": "..."
    }
```

### Vector Search (ChromaDB)

#### Purpose

Enable semantic search for exercises based on user needs rather than exact keyword matching.

#### Architecture

```python
class VectorStoreService:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIR
        )
        self.collection = self.client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION_NAME
        )
```

#### Embedding Process

```python
# When adding exercises to vector store
def add_exercise(exercise_id: str, description: str, metadata: Dict):
    # ChromaDB automatically generates embeddings
    self.collection.add(
        ids=[exercise_id],
        documents=[description],
        metadatas=[metadata]
    )
```

#### Search Process

```python
def search_exercises(query: str, n_results: int = 5) -> List[Dict]:
    # Semantic search using embeddings
    results = self.collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    return [
        {
            'id': results['ids'][0][i],
            'metadata': results['metadatas'][0][i],
            'distance': results['distances'][0][i]
        }
        for i in range(len(results['ids'][0]))
    ]
```

#### Example Query Flow

```
User Message: "I need to improve my balance"
    ?
Intent Analysis: {intent: "exercise_request", params: ["balance"]}
    ?
Search Query Generation: "balance exercises stability training"
    ?
Vector Search: ChromaDB finds semantically similar exercises
    ?
Results: [
    "Single-Leg Balance",
    "Tandem Walk",
    "Bosu Ball Training",
    ...
]
    ?
Priority Ranking: Based on user's specific data
    ?
Final Recommendations: Top 5 exercises with reasoning
```

### Recommendation Algorithm

#### Performance Analysis

```python
def _analyze_performance(performance_data: Dict) -> Dict:
    # Define thresholds
    thresholds = {
        "reaction_time": {"good": 200, "poor": 300},  # lower is better
        "accuracy": {"good": 80, "poor": 60},          # higher is better
        "balance_score": {"good": 7, "poor": 5},       # 0-10 scale
        "endurance": {"good": 70, "poor": 50},         # percentage
        "rom_shoulder": {"good": 150, "poor": 120}     # degrees
    }
    
    strengths = []
    weaknesses = []
    focus_areas = []
    
    for metric, value in performance_data.items():
        if metric in thresholds:
            good_threshold = thresholds[metric]["good"]
            poor_threshold = thresholds[metric]["poor"]
            
            # Determine if "higher is better" or "lower is better"
            if metric == "reaction_time":
                if value < good_threshold:
                    strengths.append(metric)
                elif value > poor_threshold:
                    weaknesses.append(metric)
                    focus_areas.append(metric)
            else:
                if value > good_threshold:
                    strengths.append(metric)
                elif value < poor_threshold:
                    weaknesses.append(metric)
                    focus_areas.append(metric)
    
    return {
        "strengths": strengths,
        "weaknesses": weaknesses,
        "focus_areas": focus_areas,
        "overall_health": determine_overall_health(strengths, weaknesses)
    }
```

#### Priority Calculation

```python
def _calculate_priority(exercise: Dict, analysis: Dict) -> float:
    priority = 0.5  # Base priority
    
    # Higher priority if addresses weakness
    exercise_targets = exercise.get("targets", [])
    for weakness in analysis["weaknesses"]:
        if weakness in exercise_targets:
            priority += 0.3
    
    # Adjust for difficulty vs user level
    if analysis["overall_health"] == "needs_improvement":
        if exercise["difficulty"] == "beginner":
            priority += 0.2
    elif analysis["overall_health"] == "excellent":
        if exercise["difficulty"] == "advanced":
            priority += 0.2
    
    # Bonus for no equipment needed
    if exercise["equipment"] == "none":
        priority += 0.1
    
    return min(priority, 1.0)  # Cap at 1.0
```

### Mock Response Fallback

When no API key is configured, the system provides intelligent mock responses:

```python
def _get_mock_response(user_message: str, user_context: Dict) -> Dict:
    message_lower = user_message.lower()
    
    # Context-aware responses
    if "balance" in message_lower:
        response = generate_balance_advice(user_context)
    elif "reaction time" in message_lower:
        response = generate_reaction_time_advice(user_context)
    elif "program" in message_lower:
        response = generate_program_recommendations(user_context)
    else:
        response = generate_general_advice(user_context)
    
    return {
        "message": response,
        "suggested_questions": get_relevant_follow_ups(message_lower)
    }
```

---

## ?? Data Flow

### Complete Request Flow

```
1. USER INTERACTION
   +- User types message in ChatInterface
   +- MessageInput captures text

2. FRONTEND PROCESSING
   +- useChat hook called
   +- User message added to state
   +- Loading state activated
   +- API request sent via apiService

3. API GATEWAY
   +- Request hits FastAPI endpoint
   +- CORS validation
   +- Rate limiting check
   +- Route to /chat/message endpoint

4. ENDPOINT HANDLER
   +- Validate request (Pydantic)
   +- Fetch user profile from cache
   +- Get or create conversation
   +- Call LLMService.chat()

5. LLM SERVICE PROCESSING
   +- Build conversation context
   +- Inject user performance data
   +- Format messages for LLM
   +- Call AI provider API
   +- Parse response

6. CONTEXT MANAGER
   +- Analyze user intent
   +- Extract parameters
   +- Track conversation state
   +- Add messages to history

7. RECOMMENDATION ENGINE (if needed)
   +- Analyze user performance
   +- Identify weaknesses
   +- Generate search query
   +- Query vector store
   +- Rank results by priority
   +- Format recommendations

8. RESPONSE GENERATION
   +- Combine LLM response
   +- Add recommendations
   +- Generate follow-up questions
   +- Create citations

9. DATABASE PERSISTENCE
   +- Save user message to DB
   +- Save assistant message to DB
   +- Update conversation timestamp

10. FRONTEND UPDATE
    +- Receive response from API
    +- Update messages state
    +- Update suggested questions
    +- Auto-scroll to bottom
    +- Clear loading state

11. USER SEES RESPONSE
    +- Message displayed with markdown formatting
```

### File Upload Flow

```
1. USER SELECTS FILE
   +- FileUpload component

2. VALIDATION
   +- Check file size (< 10MB)
   +- Check extension (.pdf, .jpg, .png, .csv)
   +- Preview generation

3. UPLOAD REQUEST
   +- FormData with file
   +- POST /upload/report/{user_id}

4. BACKEND PROCESSING
   +- Validate file
   +- Generate unique filename
   +- Save to ./data/uploads/
   +- Create Report record in DB
   +- Extract text (if PDF)

5. OPTIONAL: AI ANALYSIS
   +- Send extracted text to LLM
   +- Generate summary
   +- Calculate risk score
   +- Update Report record

6. RESPONSE
   +- Return report_id and metadata

7. FRONTEND UPDATE
   +- Show success message
   +- Update reports list
```

### Progress Tracking Flow

```
1. USER RECORDS METRIC
   +- ProgressTracker component

2. SUBMIT DATA
   +- metric_name: "reaction_time"
   +- metric_value: 230
   +- metric_unit: "ms"
   +- POST /progress/{user_id}

3. BACKEND PROCESSING
   +- Validate data
   +- Create Progress record
   +- Save to database

4. TREND ANALYSIS
   +- Query all progress for user
   +- Group by metric_name
   +- Calculate trends
   +- Compare with previous
   +- Generate insights

5. FRONTEND VISUALIZATION
   +- Fetch trends data
   +- Render line charts
   +- Show improvement percentage
```

---


## ?? Security & Performance

### Security Features

#### 1. **CORS (Cross-Origin Resource Sharing)**

```python
# Dynamic CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins(),  # Configurable origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Allowed origins in development
allowed_origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://frontend:5173"
]

# Production adds Vercel URLs
if VERCEL_URL:
    allowed_origins.append(f"https://{VERCEL_URL}")
```

#### 2. **Rate Limiting**

```python
class RateLimitMiddleware:
    def __init__(self, rate_limit_per_minute: int = 60):
        self.rate_limit = rate_limit_per_minute
        self.requests = defaultdict(list)
    
    async def __call__(self, request: Request, call_next):
        client_ip = request.client.host
        now = time.time()
        
        # Clean old requests
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if now - req_time < 60
        ]
        
        # Check limit
        if len(self.requests[client_ip]) >= self.rate_limit:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests"}
            )
        
        self.requests[client_ip].append(now)
        return await call_next(request)
```

#### 3. **Input Validation**

**Pydantic Models:**
```python
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)
    conversation_id: Optional[str] = Field(None, regex=r'^conv_[a-zA-Z0-9]+$')
    include_context: bool = True
    user_id: Optional[str] = Field(None, regex=r'^user_[a-zA-Z0-9]+$')
    
    @validator('message')
    def validate_message(cls, v):
        # Sanitize input
        v = v.strip()
        if not v:
            raise ValueError('Message cannot be empty')
        return v
```

#### 4. **File Upload Security**

```python
# File size limit
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB

# Allowed extensions
ALLOWED_EXTENSIONS = ['.pdf', '.jpg', '.jpeg', '.png', '.txt', '.csv']

# Validation
def validate_file(file: UploadFile):
    # Check extension
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, "Invalid file type")
    
    # Check size
    file.file.seek(0, 2)  # Seek to end
    size = file.file.tell()
    file.file.seek(0)  # Reset
    if size > MAX_UPLOAD_SIZE:
        raise HTTPException(400, "File too large")
    
    # Generate safe filename
    safe_name = f"{uuid.uuid4()}_{secure_filename(file.filename)}"
    return safe_name
```

#### 5. **Error Handling**

```python
class ErrorHandlerMiddleware:
    async def __call__(self, request: Request, call_next):
        try:
            return await call_next(request)
        except HTTPException as e:
            # Log HTTP exceptions
            logger.error("http_exception", status_code=e.status_code, detail=e.detail)
            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail}
            )
        except Exception as e:
            # Log unexpected errors
            logger.error("unexpected_error", error=str(e), trace=traceback.format_exc())
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"}
            )
```

#### 6. **SQL Injection Prevention**

**Using SQLAlchemy ORM (parameterized queries):**
```python
# SAFE - Parameterized
user = session.query(User).filter(User.id == user_id).first()

# UNSAFE - String concatenation (NOT used in our code)
# query = f"SELECT * FROM users WHERE id = '{user_id}'"  # ? NEVER DO THIS
```

#### 7. **API Key Protection**

```python
# Environment variables only
API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Never log API keys
logger.info("initializing_llm", provider="anthropic", key_length=len(API_KEY))
# ? Only logs length, not actual key

# Never return in responses
# ? Don't do: {"api_key": API_KEY}
```

### Performance Optimizations

#### 1. **Database Optimizations**

**Indexes:**
```python
# Add indexes for frequent queries
Index('idx_messages_conversation', Message.conversation_id, Message.sequence)
Index('idx_reports_user_date', Report.user_id, Report.created_at.desc())
Index('idx_progress_user_metric', Progress.user_id, Progress.metric_name)
```

**Connection Pooling:**
```python
# SQLAlchemy engine with pooling
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)
```

**Query Optimization:**
```python
# Eager loading to avoid N+1 queries
user = session.query(User).options(
    joinedload(User.reports),
    joinedload(User.conversations)
).filter(User.id == user_id).first()
```

#### 2. **Caching**

**In-Memory Cache for Frequent Data:**
```python
# Cache user profiles
_users_cache = {}

def get_user_cached(user_id: str):
    if user_id not in _users_cache:
        _users_cache[user_id] = fetch_user_from_db(user_id)
    return _users_cache[user_id]

# Cache expiration
CACHE_TTL = 300  # 5 minutes
```

**Vector Store Caching:**
```python
# ChromaDB persists to disk
self.client = chromadb.PersistentClient(
    path="./data/chromadb"  # Reused across restarts
)
```

#### 3. **Async/Await**

**Async Database Operations:**
```python
async def get_user(user_id: str, db: AsyncSession):
    result = await db.execute(
        select(User).filter(User.id == user_id)
    )
    return result.scalar_one_or_none()
```

**Async LLM Calls:**
```python
async def chat(self, user_message: str) -> Dict:
    # Non-blocking API call
    response = await self.groq_client.chat.completions.create(
        model=self.model,
        messages=messages
    )
    return response
```

#### 4. **Response Compression**

```python
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

#### 5. **Lazy Loading**

**Frontend:**
```typescript
// Load components only when needed
const ReportDashboard = lazy(() => import('./components/dashboard/ReportDashboard'));
const ProgressTracker = lazy(() => import('./components/progress/ProgressTracker'));

// Render with Suspense
<Suspense fallback={<LoadingSpinner />}>
    <ReportDashboard />
</Suspense>
```

#### 6. **Pagination**

```python
@router.get("/conversations")
async def get_conversations(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    conversations = list(conversations_db.values())[offset:offset + limit]
    return conversations
```

### Logging & Monitoring

#### Structured Logging

```python
import structlog

logger = structlog.get_logger()

# Rich context logging
logger.info(
    "chat_request_received",
    user_id=user_id,
    message_length=len(message),
    conversation_id=conversation_id,
    timestamp=datetime.utcnow()
)

logger.error(
    "llm_api_error",
    provider=provider,
    error=str(e),
    user_id=user_id,
    retry_count=retry_count
)
```

#### Log Levels

- **DEBUG**: Detailed debugging information
- **INFO**: General informational messages
- **WARNING**: Warning messages (ChromaDB not available, etc.)
- **ERROR**: Error messages with context
- **CRITICAL**: Critical failures

#### Metrics to Monitor

1. **API Response Time**
   - Endpoint latency
   - LLM API response time
   - Database query time

2. **Error Rates**
   - 4xx errors (client errors)
   - 5xx errors (server errors)
   - LLM API failures

3. **Resource Usage**
   - Memory consumption
   - CPU usage
   - Database connections

4. **Business Metrics**
   - Active users
   - Messages per conversation
   - Recommendation acceptance rate

---

## ?? Deployment Guide

### Local Development

#### Prerequisites
```bash
# Python 3.11+
python --version

# Node.js 18+
node --version

# Docker & Docker Compose (optional)
docker --version
docker-compose --version
```

#### Setup Steps

**1. Clone Repository**
```bash
git clone <repository-url>
cd MSK-Wellness-Coach
```

**2. Backend Setup**
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp ../.env.example .env

# Edit .env and add your API key
# AI_PROVIDER=groq
# GROQ_API_KEY=your_key_here

# Run backend
uvicorn app.main:app --reload --port 8000
```

**3. Frontend Setup**
```bash
cd frontend

# Install dependencies
npm install

# Run frontend
npm run dev
```

**4. Access Application**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Docker Deployment

#### Simple Docker Compose

**File: `docker-compose.yml`**
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - AI_PROVIDER=groq
      - GROQ_API_KEY=${GROQ_API_KEY}
      - DATABASE_URL=sqlite+aiosqlite:///./msk_chatbot.db
    volumes:
      - ./backend/data:/app/data
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "5173:80"
    depends_on:
      - backend
    restart: unless-stopped
```

**Run:**
```bash
# Create .env file with API key
echo "GROQ_API_KEY=your_key_here" > .env

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Deployment

#### Option 1: Vercel (Frontend) + Railway/Render (Backend)

**Frontend (Vercel):**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel --prod
```

**Backend (Railway):**
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

**Environment Variables (Railway):**
```
AI_PROVIDER=groq
GROQ_API_KEY=gsk_xxxxx
DATABASE_URL=sqlite+aiosqlite:///./msk_chatbot.db
DEBUG=False
```

#### Option 2: AWS EC2

**Setup:**
```bash
# SSH into EC2 instance
ssh -i key.pem ubuntu@your-ec2-ip

# Install Docker
sudo apt update
sudo apt install docker.io docker-compose -y

# Clone repository
git clone <repo-url>
cd MSK-Wellness-Coach

# Create .env
nano .env
# Add your API keys

# Run with Docker
docker-compose up -d

# Setup Nginx reverse proxy
sudo apt install nginx
sudo nano /etc/nginx/sites-available/msk-chatbot
```

**Nginx Configuration:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        proxy_pass http://localhost:5173;
        proxy_set_header Host $host;
    }
}
```

#### Option 3: Kubernetes

**Deployment manifests available in `/k8s` directory (if added)**

```yaml
# backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: msk-backend
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: backend
        image: msk-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: GROQ_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: groq-api-key
```

### Database Migration (SQLite ? PostgreSQL)

**For Production Scale:**

```python
# 1. Update DATABASE_URL in .env
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/msk_db

# 2. Install PostgreSQL dependencies
pip install asyncpg psycopg2-binary

# 3. Run Alembic migrations
alembic upgrade head

# 4. (Optional) Migrate existing SQLite data
python scripts/migrate_sqlite_to_postgres.py
```

---


## ????? Development Guide

### Project Structure Deep Dive

```
MSK-Wellness-Coach/
�
+-- backend/
�   +-- app/
�   �   +-- __init__.py
�   �   +-- main.py                      # FastAPI app initialization
�   �   �
�   �   +-- api/
�   �   �   +-- endpoints/
�   �   �       +-- __init__.py
�   �   �       +-- chat.py              # Chat endpoints
�   �   �       +-- profile.py           # User profile CRUD
�   �   �       +-- progress.py          # Progress tracking
�   �   �       +-- recommendations.py   # Exercise/program recommendations
�   �   �       +-- reports.py           # Report management
�   �   �       +-- upload.py            # File upload handling
�   �   �       +-- users.py             # User management
�   �   �
�   �   +-- core/
�   �   �   +-- __init__.py
�   �   �   +-- config.py                # Settings & configuration
�   �   �
�   �   +-- db/
�   �   �   +-- __init__.py
�   �   �   +-- base.py                  # SQLAlchemy base class
�   �   �   +-- session.py               # Database session management
�   �   �   +-- init_db.py               # Database initialization
�   �   �
�   �   +-- models/
�   �   �   +-- __init__.py
�   �   �   +-- user.py                  # User model
�   �   �   +-- conversation.py          # Conversation & Message models
�   �   �   +-- report.py                # Report model
�   �   �   +-- progress.py              # Progress model
�   �   �
�   �   +-- schemas/
�   �   �   +-- __init__.py
�   �   �   +-- chat.py                  # Chat request/response schemas
�   �   �   +-- user.py                  # User schemas
�   �   �   +-- progress.py              # Progress schemas
�   �   �   +-- recommendation.py        # Recommendation schemas
�   �   �   +-- report.py                # Report schemas
�   �   �
�   �   +-- services/
�   �   �   +-- __init__.py
�   �   �   +-- llm_service.py           # LLM integration (Groq, Claude, etc.)
�   �   �   +-- context_manager.py       # Conversation context management
�   �   �   +-- recommendation_engine.py # Exercise recommendation logic
�   �   �   +-- vector_store.py          # ChromaDB vector search
�   �   �   +-- knowledge_base.py        # Static knowledge repository
�   �   �
�   �   +-- middleware/
�   �   �   +-- __init__.py
�   �   �   +-- error_handler.py         # Global error handling
�   �   �   +-- rate_limiter.py          # Rate limiting middleware
�   �   �
�   �   +-- utils/
�   �       +-- __init__.py
�   �       +-- logging.py               # Structured logging setup
�   �       +-- prompt_templates.py      # LLM prompt templates
�   �
�   +-- data/
�   �   +-- chromadb/                    # ChromaDB vector storage
�   �   +-- uploads/                     # User uploaded files
�   �
�   +-- tests/
�   �   +-- __init__.py
�   �   +-- conftest.py                  # Pytest configuration
�   �   +-- test_api.py                  # API endpoint tests
�   �   +-- test_services.py             # Service layer tests
�   �
�   +-- alembic/                         # Database migrations
�   �   +-- versions/
�   �   +-- env.py
�   �
�   +-- Dockerfile
�   +-- requirements.txt
�   +-- alembic.ini
�
+-- frontend/
�   +-- src/
�   �   +-- main.tsx                     # App entry point
�   �   +-- App.tsx                      # Main App component
�   �   +-- App.css
�   �   �
�   �   +-- components/
�   �   �   +-- chat/
�   �   �   �   +-- ChatInterface.tsx    # Main chat container
�   �   �   �   +-- ChatInterface.css
�   �   �   �   +-- MessageBubble.tsx    # Individual message display
�   �   �   �   +-- MessageBubble.css
�   �   �   �   +-- MessageInput.tsx     # Message input field
�   �   �   �   +-- MessageInput.css
�   �   �   �   +-- MessageList.tsx      # Message list container
�   �   �   �   +-- Sidebar.tsx          # Conversation sidebar
�   �   �   �   +-- Sidebar.css
�   �   �   �   +-- SuggestedQuestions.tsx # Suggested question chips
�   �   �   �   +-- SuggestedQuestions.css
�   �   �   �
�   �   �   +-- profile/
�   �   �   �   +-- ProfileForm.tsx      # Profile creation/editing
�   �   �   �   +-- ProfileForm.css
�   �   �   �
�   �   �   +-- progress/
�   �   �   �   +-- ProgressTracker.tsx  # Progress visualization
�   �   �   �   +-- ProgressTracker.css
�   �   �   �
�   �   �   +-- recommendations/
�   �   �   �   +-- RecommendationList.tsx
�   �   �   �   +-- RecommendationList.css
�   �   �   �
�   �   �   +-- dashboard/
�   �   �   �   +-- ReportDashboard.tsx  # Health dashboard
�   �   �   �   +-- ReportDashboard.css
�   �   �   �
�   �   �   +-- common/
�   �   �       +-- FileUpload.tsx       # File upload component
�   �   �       +-- FileUpload.css
�   �   �
�   �   +-- hooks/
�   �   �   +-- useChat.ts               # Chat logic hook
�   �   �
�   �   +-- services/
�   �   �   +-- api.service.ts           # API client
�   �   �
�   �   +-- types/
�   �   �   +-- chat.types.ts            # TypeScript type definitions
�   �   �
�   �   +-- styles/
�   �       +-- global.css               # Global styles
�   �
�   +-- public/
�   +-- index.html
�   +-- Dockerfile
�   +-- package.json
�   +-- tsconfig.json
�   +-- vite.config.ts
�   +-- vercel.json
�
+-- .env.example                         # Environment variables template
+-- .gitignore
+-- docker-compose.yml
+-- README.md
+-- COMPREHENSIVE_DOCUMENTATION.md       # This file
```

### Adding New Features

#### 1. Adding a New API Endpoint

**Step 1: Create Schema** (`backend/app/schemas/`)
```python
# new_feature.py
from pydantic import BaseModel
from typing import Optional

class NewFeatureRequest(BaseModel):
    param1: str
    param2: int
    
class NewFeatureResponse(BaseModel):
    result: str
    metadata: Optional[dict]
```

**Step 2: Create Model (if needed)** (`backend/app/models/`)
```python
# new_model.py
from sqlalchemy import Column, String, Integer
from app.db.base import Base

class NewModel(Base):
    __tablename__ = "new_table"
    
    id = Column(String, primary_key=True)
    field1 = Column(String, nullable=False)
    field2 = Column(Integer)
```

**Step 3: Create Endpoint** (`backend/app/api/endpoints/`)
```python
# new_feature.py
from fastapi import APIRouter, HTTPException
from app.schemas.new_feature import NewFeatureRequest, NewFeatureResponse

router = APIRouter(prefix="/new-feature")

@router.post("/", response_model=NewFeatureResponse)
async def create_new_feature(request: NewFeatureRequest):
    # Implementation
    return NewFeatureResponse(
        result="success",
        metadata={"param1": request.param1}
    )
```

**Step 4: Register Router** (`backend/app/main.py`)
```python
from app.api.endpoints import new_feature

app.include_router(new_feature.router, prefix=f"{settings.API_V1_PREFIX}")
```

**Step 5: Add Frontend Types** (`frontend/src/types/`)
```typescript
// new-feature.types.ts
export interface NewFeatureRequest {
    param1: string;
    param2: number;
}

export interface NewFeatureResponse {
    result: string;
    metadata?: Record<string, any>;
}
```

**Step 6: Add API Method** (`frontend/src/services/api.service.ts`)
```typescript
async createNewFeature(request: NewFeatureRequest): Promise<NewFeatureResponse> {
    return this.request<NewFeatureResponse>('/new-feature', {
        method: 'POST',
        body: JSON.stringify(request),
    });
}
```

**Step 7: Create Component** (`frontend/src/components/`)
```typescript
import { useState } from 'react';
import { apiService } from '../../services/api.service';

function NewFeatureComponent() {
    const [result, setResult] = useState<string>('');
    
    const handleSubmit = async () => {
        const response = await apiService.createNewFeature({
            param1: 'test',
            param2: 42
        });
        setResult(response.result);
    };
    
    return (
        <div>
            <button onClick={handleSubmit}>Submit</button>
            <p>{result}</p>
        </div>
    );
}
```

#### 2. Adding a New LLM Provider

**Step 1: Add Configuration** (`backend/app/core/config.py`)
```python
# New provider settings
NEW_PROVIDER_API_KEY: Optional[str] = None
NEW_PROVIDER_MODEL: str = "default-model"
```

**Step 2: Initialize Client** (`backend/app/services/llm_service.py`)
```python
def _init_client(self):
    provider = settings.AI_PROVIDER.lower()
    
    if provider == "new_provider":
        try:
            import new_provider_sdk
            self.new_provider_client = new_provider_sdk.Client(
                api_key=settings.NEW_PROVIDER_API_KEY
            )
            print(f"? New Provider initialized")
        except ImportError:
            print("? new_provider_sdk not installed")
```

**Step 3: Implement Chat Method**
```python
async def chat(self, user_message: str, ...) -> Dict[str, Any]:
    if self.new_provider_client:
        response = await self._chat_new_provider(
            user_message,
            conversation_history,
            user_context
        )
        return response
```

**Step 4: Add Provider-Specific Method**
```python
async def _chat_new_provider(
    self,
    user_message: str,
    history: List[Dict],
    user_context: Dict
) -> Dict[str, Any]:
    messages = self._build_messages(user_message, history, user_context)
    
    response = await self.new_provider_client.completions.create(
        model=settings.NEW_PROVIDER_MODEL,
        messages=messages
    )
    
    return {
        "message": response.content,
        "metadata": {"provider": "new_provider"}
    }
```

**Step 5: Update Documentation**
```bash
# Add to README.md and .env.example
AI_PROVIDER=new_provider
NEW_PROVIDER_API_KEY=your_key_here
NEW_PROVIDER_MODEL=default-model
```

### Testing

#### Unit Tests

**Backend Tests** (`backend/tests/`)
```python
# test_services.py
import pytest
from app.services.recommendation_engine import RecommendationEngine

@pytest.fixture
def recommendation_engine():
    return RecommendationEngine()

def test_analyze_performance(recommendation_engine):
    performance_data = {
        "reaction_time": 150,  # Good
        "accuracy": 90,        # Good
        "balance_score": 5     # Needs improvement
    }
    
    analysis = recommendation_engine._analyze_performance(performance_data)
    
    assert "balance_score" in analysis["weaknesses"]
    assert "reaction_time" in analysis["strengths"]
    assert len(analysis["focus_areas"]) > 0

def test_generate_recommendations(recommendation_engine):
    performance_data = {"balance_score": 5}
    
    recommendations = recommendation_engine.generate_recommendations(
        performance_data,
        limit=3
    )
    
    assert len(recommendations) <= 3
    assert all("recommendation_reason" in rec for rec in recommendations)
```

**Run Tests:**
```bash
cd backend
pytest tests/ -v
pytest tests/test_services.py::test_analyze_performance -v
```

#### API Tests

```python
# test_api.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_send_message():
    response = client.post("/api/v1/chat/message", json={
        "message": "How can I improve my balance?",
        "include_context": True
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "conversation_id" in data

def test_create_profile():
    response = client.post("/api/v1/profile", json={
        "name": "Test User",
        "performance_data": {"reaction_time": 250}
    })
    
    assert response.status_code == 200
    assert response.json()["name"] == "Test User"
```

#### Frontend Tests (if added)

```typescript
// ChatInterface.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import ChatInterface from './ChatInterface';

test('renders chat interface', () => {
    render(<ChatInterface userId="test-user" />);
    expect(screen.getByPlaceholderText(/type your message/i)).toBeInTheDocument();
});

test('sends message on button click', async () => {
    render(<ChatInterface userId="test-user" />);
    
    const input = screen.getByPlaceholderText(/type your message/i);
    const button = screen.getByRole('button', { name: /send/i });
    
    fireEvent.change(input, { target: { value: 'Test message' } });
    fireEvent.click(button);
    
    // Assert API call was made
    expect(await screen.findByText(/Test message/i)).toBeInTheDocument();
});
```

### Debugging

#### Backend Debugging

**Enable Debug Logging:**
```python
# config.py
DEBUG = True
LOG_LEVEL = "DEBUG"
```

**View Logs:**
```bash
# Structured logs with context
tail -f logs/app.log | jq '.'

# Filter by level
tail -f logs/app.log | jq 'select(.level == "error")'
```

**Debug LLM Calls:**
```python
# llm_service.py
print("\n" + "="*80)
print("?? CHAT METHOD CALLED")
print(f"   User message: {user_message[:100]}...")
print(f"   History length: {len(conversation_history)}")
print(f"   Include context: {include_context}")
print("="*80 + "\n")
```

**Interactive Debugging:**
```python
# Add breakpoint
import pdb; pdb.set_trace()

# Or use ipdb for better experience
import ipdb; ipdb.set_trace()
```

#### Frontend Debugging

**React DevTools:**
- Install React Developer Tools browser extension
- Inspect component state and props

**Console Logging:**
```typescript
console.log('Sending message:', message);
console.log('API response:', response);
console.error('Error occurred:', error);
```

**Network Tab:**
- Monitor API calls in browser DevTools
- Check request/response headers and payloads

### Code Style & Best Practices

#### Python (Backend)

**PEP 8 Compliance:**
```bash
# Install linter
pip install flake8 black

# Check code
flake8 app/

# Auto-format
black app/
```

**Type Hints:**
```python
# Always use type hints
def process_data(data: Dict[str, Any]) -> List[str]:
    results: List[str] = []
    for key, value in data.items():
        results.append(f"{key}: {value}")
    return results
```

**Docstrings:**
```python
def analyze_performance(performance_data: Dict[str, Any]) -> Dict:
    """
    Analyze user performance data to identify strengths and weaknesses.
    
    Args:
        performance_data: Dictionary containing user's performance metrics
        
    Returns:
        Dictionary with analysis results containing:
        - strengths: List of metrics above threshold
        - weaknesses: List of metrics below threshold
        - focus_areas: Priority areas for improvement
        
    Example:
        >>> data = {"reaction_time": 150, "balance_score": 5}
        >>> result = analyze_performance(data)
        >>> print(result["weaknesses"])
        ["balance_score"]
    """
    # Implementation
```

#### TypeScript (Frontend)

**ESLint & Prettier:**
```bash
# Install tools
npm install --save-dev eslint prettier

# Run linter
npm run lint

# Auto-format
npm run format
```

**Type Safety:**
```typescript
// Always define types
interface UserData {
    id: string;
    name: string;
    performanceData: Record<string, number>;
}

// Use types in function signatures
function processUser(user: UserData): string {
    return `User: ${user.name}`;
}
```

**React Best Practices:**
```typescript
// Use functional components with hooks
function MyComponent({ userId }: { userId: string }) {
    const [data, setData] = useState<UserData | null>(null);
    
    // Use useCallback for functions passed to children
    const handleUpdate = useCallback((newData: UserData) => {
        setData(newData);
    }, []);
    
    // Use useMemo for expensive computations
    const processedData = useMemo(() => {
        return data ? processUser(data) : null;
    }, [data]);
    
    return <div>{processedData}</div>;
}
```

---


## ?? Troubleshooting

### Common Issues

#### 1. Backend Won't Start

**Error: `ModuleNotFoundError: No module named 'app'`**
```bash
# Solution: Ensure you're in the backend directory
cd backend
python -m uvicorn app.main:app --reload

# Or set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
uvicorn app.main:app --reload
```

**Error: `ValidationError: ALLOWED_ORIGINS - Extra inputs are not permitted`**
```bash
# Solution: This was fixed in the latest version
# Ensure you have the updated config.py with:
class Config:
    extra = "ignore"  # Ignore extra fields from .env file

# Or remove ALLOWED_ORIGINS from .env file
```

**Error: Port 8000 already in use**
```bash
# Solution: Kill process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -ti:8000 | xargs kill -9

# Or use different port:
uvicorn app.main:app --port 8001
```

#### 2. Database Issues

**Error: `OperationalError: unable to open database file`**
```bash
# Solution: Create data directory
mkdir -p backend/data

# Or check permissions
chmod 755 backend/data
```

**Error: `table users has no column named performance_data`**
```bash
# Solution: Delete old database and recreate
rm backend/msk_chatbot.db
# Restart backend - tables will be recreated automatically
```

**Error: Alembic migration conflicts**
```bash
# Solution: Reset migrations
cd backend
rm -rf alembic/versions/*
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

#### 3. LLM API Issues

**Error: `No API key configured`**
```bash
# Solution: Add API key to .env
echo "GROQ_API_KEY=gsk_your_key_here" >> .env

# Restart backend to load new environment variables
```

**Error: `Rate limit exceeded`**
```bash
# Solution 1: Wait a few minutes
# Solution 2: Switch to different provider
AI_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-your_key

# Solution 3: Use mock responses (no API key needed)
# Just remove/comment out API key - system will fallback
```

**Error: `groq package not installed`**
```bash
# Solution: Install groq package
pip install groq

# Or install all dependencies
pip install -r requirements.txt
```

#### 4. ChromaDB Issues

**Warning: `ChromaDB not available, vector store disabled`**
```bash
# This is not an error - the app still works!
# ChromaDB is optional and enhances recommendations

# To enable ChromaDB:
pip install chromadb

# Restart backend
```

**Error: `ChromaDB collection not found`**
```bash
# Solution: Delete and recreate
rm -rf backend/data/chromadb
# Restart backend - collection will be created automatically
```

#### 5. Frontend Issues

**Error: `Failed to fetch` when calling API**
```bash
# Solution 1: Ensure backend is running
curl http://localhost:8000/health

# Solution 2: Check CORS configuration
# In backend/app/main.py, verify allowed origins include:
allow_origins=["http://localhost:5173"]

# Solution 3: Check API_BASE_URL in frontend
# frontend/src/services/api.service.ts
const API_BASE_URL = '/api/v1';  # Should be '/api/v1' for proxy
```

**Error: `Module not found: Can't resolve './components/...'`**
```bash
# Solution: Install dependencies
cd frontend
npm install

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Error: Vite build fails**
```bash
# Solution: Check TypeScript errors
npm run type-check

# Fix and rebuild
npm run build
```

#### 6. Docker Issues

**Error: `docker-compose: command not found`**
```bash
# Solution: Install Docker Compose
# Or use newer syntax:
docker compose up -d  # Note: no hyphen
```

**Error: Container keeps restarting**
```bash
# Solution: Check logs
docker-compose logs backend
docker-compose logs frontend

# Common cause: Missing environment variables
# Add to docker-compose.yml:
environment:
  - GROQ_API_KEY=${GROQ_API_KEY}
```

**Error: Permission denied in container**
```bash
# Solution: Fix volume permissions
sudo chown -R 1000:1000 ./backend/data
```

#### 7. File Upload Issues

**Error: `File too large`**
```bash
# Solution: Increase MAX_UPLOAD_SIZE in config.py
MAX_UPLOAD_SIZE = 20 * 1024 * 1024  # 20MB

# Or compress file before uploading
```

**Error: `Invalid file type`**
```bash
# Solution: Check ALLOWED_EXTENSIONS in config.py
ALLOWED_EXTENSIONS = ['.pdf', '.jpg', '.jpeg', '.png', '.txt', '.csv']

# Add new extension if needed
```

**Error: Upload succeeds but file not found**
```bash
# Solution: Check UPLOAD_DIR exists
mkdir -p backend/data/uploads

# Verify file was saved
ls -la backend/data/uploads/
```

### Performance Issues

#### Slow API Responses

**Symptoms:** API calls take >5 seconds

**Solutions:**
```bash
# 1. Check LLM provider latency
# Switch to faster provider (Groq is fastest)
AI_PROVIDER=groq

# 2. Enable response caching
# Add to context_manager.py

# 3. Reduce conversation history
# In config.py:
MAX_HISTORY_MESSAGES = 5  # Default is 10

# 4. Use streaming for real-time responses
# Implement streaming endpoint (if needed)
```

#### High Memory Usage

**Symptoms:** Backend using >1GB RAM

**Solutions:**
```bash
# 1. Clear old conversations
# Happens automatically, but can adjust:
# In context_manager.py:
cleanup_old_conversations(max_age_hours=12)  # Default is 24

# 2. Limit ChromaDB cache
# In vector_store.py, reduce collection size

# 3. Use database instead of in-memory storage
# Replace conversations_db dict with database queries
```

#### Frontend Loading Slowly

**Solutions:**
```typescript
// 1. Implement lazy loading
const Dashboard = lazy(() => import('./components/dashboard/ReportDashboard'));

// 2. Optimize bundle size
npm run build -- --analyze

// 3. Enable code splitting in vite.config.ts
build: {
    rollupOptions: {
        output: {
            manualChunks: {
                vendor: ['react', 'react-dom'],
            }
        }
    }
}
```

### Debug Mode

#### Enable Full Debug Output

**Backend:**
```python
# config.py
DEBUG = True
LOG_LEVEL = "DEBUG"

# main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Frontend:**
```typescript
// Add to useChat.ts
console.log('Sending message:', message);
console.log('Conversation ID:', conversationId);
console.log('API response:', response);
```

**Network Debugging:**
```bash
# View all HTTP requests
# In browser DevTools > Network tab
# Filter by: Fetch/XHR

# Or use curl to test endpoints
curl -X POST http://localhost:8000/api/v1/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "test", "include_context": true}'
```

### Getting Help

#### Logs Location

```bash
# Backend logs (if file logging enabled)
tail -f backend/logs/app.log

# Docker logs
docker-compose logs -f backend
docker-compose logs -f frontend

# System logs
journalctl -u msk-chatbot -f  # If using systemd
```

#### Diagnostic Information

When reporting issues, include:

1. **Environment:**
   - OS: Windows/Mac/Linux
   - Python version: `python --version`
   - Node version: `node --version`
   - Docker version: `docker --version`

2. **Error Details:**
   - Full error message
   - Stack trace
   - Steps to reproduce

3. **Configuration:**
   - AI_PROVIDER setting
   - Relevant .env variables (DO NOT share API keys!)
   - Database type

4. **Logs:**
   - Backend startup logs
   - Error logs
   - API request/response examples

---

## ?? Appendix

### Glossary

**MSK (Musculoskeletal):** Relating to muscles, bones, joints, and connective tissues.

**LLM (Large Language Model):** AI model trained on vast amounts of text data, capable of understanding and generating human-like text.

**Vector Store:** Database that stores embeddings (numerical representations) of text for semantic search.

**Embedding:** Numerical vector representation of text that captures semantic meaning.

**ChromaDB:** Open-source vector database for storing and querying embeddings.

**Semantic Search:** Search based on meaning rather than exact keyword matching.

**RAG (Retrieval Augmented Generation):** AI technique combining vector search with LLM generation.

**CORS (Cross-Origin Resource Sharing):** Security mechanism controlling which domains can access an API.

**API Key:** Secret token for authenticating with external services.

**UUID (Universally Unique Identifier):** 128-bit identifier used for unique records.

**ORM (Object-Relational Mapping):** Technique to interact with databases using objects instead of SQL.

**Async/Await:** Programming pattern for handling asynchronous operations.

**Middleware:** Software layer that sits between client and server, processing requests/responses.

**Rate Limiting:** Controlling the number of requests a user can make in a time period.

**Webhook:** Automated message sent from one system to another when an event occurs.

### Metrics Reference

#### Performance Metrics

| Metric                 | Unit    | Good Range    | Poor Range    | Description                        |
| ---------------------- | ------- | ------------- | ------------- | ---------------------------------- |
| Reaction Time (Simple) | ms      | < 200         | > 300         | Time to respond to single stimulus |
| Reaction Time (Choice) | ms      | < 400         | > 600         | Time to select between options     |
| Accuracy               | %       | > 80          | < 60          | Percentage of correct responses    |
| Balance Score          | 0-10    | > 7           | < 5           | Composite balance ability          |
| Balance (Single-Leg)   | seconds | > 30          | < 10          | Time standing on one leg           |
| ROM (Shoulder)         | degrees | > 150         | < 120         | Shoulder range of motion           |
| ROM (Knee)             | degrees | > 130         | < 100         | Knee range of motion               |
| Endurance              | %       | > 70          | < 50          | Cardiovascular fitness             |
| Strength               | kg      | Age-dependent | Age-dependent | Muscular force production          |

#### Risk Level Classification

| Overall Score | Risk Level | Action Needed         |
| ------------- | ---------- | --------------------- |
| 75-100        | Low        | Maintenance exercises |
| 50-74         | Moderate   | Targeted improvement  |
| 25-49         | High       | Comprehensive program |
| 0-24          | Very High  | Medical consultation  |

### API Response Codes

| Code | Meaning               | Description                   |
| ---- | --------------------- | ----------------------------- |
| 200  | OK                    | Request successful            |
| 201  | Created               | Resource created successfully |
| 400  | Bad Request           | Invalid input data            |
| 401  | Unauthorized          | Authentication required       |
| 403  | Forbidden             | Access denied                 |
| 404  | Not Found             | Resource doesn't exist        |
| 429  | Too Many Requests     | Rate limit exceeded           |
| 500  | Internal Server Error | Server error occurred         |
| 503  | Service Unavailable   | Service temporarily down      |

### Environment Variables Reference

```bash
# Application
APP_NAME=MSK Wellness AI Chatbot
DEBUG=True                              # Enable debug mode
API_V1_PREFIX=/api/v1                   # API route prefix

# Database
DATABASE_URL=sqlite+aiosqlite:///./msk_chatbot.db

# AI Provider (choose one)
AI_PROVIDER=groq                        # groq, anthropic, openai, gemini, poe

# Groq API
GROQ_API_KEY=gsk_xxxxx
GROQ_MODEL=llama-3.3-70b-versatile

# Anthropic API
ANTHROPIC_API_KEY=sk-ant-xxxxx
CLAUDE_MODEL=claude-sonnet-4-20250514

# OpenAI API
OPENAI_API_KEY=sk-xxxxx
OPENAI_MODEL=gpt-4

# Google Gemini API
GEMINI_API_KEY=xxxxx
GEMINI_MODEL=gemini-pro

# Poe API
POE_API_KEY=xxxxx
POE_BOT_NAME=GPT-4o-Mini

# ChromaDB
CHROMA_PERSIST_DIR=./data/chromadb
CHROMA_COLLECTION_NAME=exercise_recommendations

# File Upload
UPLOAD_DIR=./data/uploads
MAX_UPLOAD_SIZE=10485760                # 10MB in bytes
ALLOWED_EXTENSIONS=['.pdf', '.jpg', '.jpeg', '.png', '.txt', '.csv']

# Logging
LOG_LEVEL=INFO                          # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT=json                         # json or text

# Security
RATE_LIMIT_ENABLED=True
RATE_LIMIT_PER_MINUTE=60

# CORS
# Note: ALLOWED_ORIGINS is dynamically generated, don't set in .env
```

### Useful Commands

```bash
# Backend Development
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend Development
cd frontend
npm install
npm run dev
npm run build
npm run preview

# Testing
cd backend
pytest tests/ -v
pytest tests/test_api.py::test_send_message -v --pdb  # Debug on failure

# Database
cd backend
alembic revision --autogenerate -m "Migration message"
alembic upgrade head
alembic downgrade -1

# Docker
docker-compose up -d
docker-compose down
docker-compose logs -f
docker-compose restart backend
docker-compose exec backend bash

# Code Quality
# Python
black app/
flake8 app/
mypy app/

# TypeScript
npm run lint
npm run format
npm run type-check

# Cleanup
rm -rf backend/__pycache__ backend/**/__pycache__
rm -rf frontend/node_modules frontend/dist
docker system prune -a  # Clean Docker
```

### Resources

#### Documentation
- **FastAPI:** https://fastapi.tiangolo.com/
- **React:** https://react.dev/
- **SQLAlchemy:** https://docs.sqlalchemy.org/
- **ChromaDB:** https://docs.trychroma.com/
- **Groq API:** https://console.groq.com/docs
- **Anthropic Claude:** https://docs.anthropic.com/

#### Tools
- **API Testing:** https://www.postman.com/
- **Database Viewer:** https://sqlitebrowser.org/
- **Git Client:** https://www.gitkraken.com/
- **Code Editor:** https://code.visualstudio.com/

#### Learning
- **Python AsyncIO:** https://realpython.com/async-io-python/
- **TypeScript:** https://www.typescriptlang.org/docs/
- **Docker:** https://docs.docker.com/get-started/
- **LLM Prompting:** https://www.promptingguide.ai/

---

## ?? Conclusion

This comprehensive documentation covers all aspects of the MSK Wellness Coach chatbot system, from architecture and implementation to deployment and troubleshooting.

### Key Takeaways

1. **Modern Architecture:** Built with FastAPI and React, following best practices
2. **AI-Powered:** Multiple LLM provider support with intelligent fallbacks
3. **Personalized:** Uses performance data analysis and vector search for tailored recommendations
4. **Scalable:** Database-backed with async operations and proper caching
5. **Production-Ready:** Includes logging, error handling, rate limiting, and security features
6. **Developer-Friendly:** Well-structured code, comprehensive tests, and clear documentation

### Next Steps

1. **Try the Application:** Follow the Quick Start guide
2. **Explore the Code:** Review the project structure and key components
3. **Customize:** Add new features or modify existing ones
4. **Deploy:** Use the deployment guide for production setup
5. **Contribute:** Improve the codebase and documentation

### Support

For questions, issues, or contributions:
- Check the Troubleshooting section
- Review the API documentation at `/docs`
- Examine the code examples in this document
- Consult the external resources listed

---

**Document Version:** 1.0.0  
**Last Updated:** February 18, 2026  
**Maintained By:** MSK Development Team

� 2026 MSK Wellness Coach. All rights reserved.

