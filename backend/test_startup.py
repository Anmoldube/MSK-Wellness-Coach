"""
Quick startup test script
"""
import asyncio
import sys
from pathlib import Path

async def test_startup():
    print("🔍 Testing MSK Wellness Chatbot Startup...")
    print("-" * 50)
    
    # Test 1: Import core modules
    print("\n1️⃣ Testing imports...")
    try:
        from app.core.config import settings
        print("   ✅ Config loaded")
        print(f"   📝 App Name: {settings.APP_NAME}")
        print(f"   🔑 API Key set: {'Yes' if settings.ANTHROPIC_API_KEY else 'No (will use demo mode)'}")
        print(f"   💾 Database: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'Not configured'}")
    except Exception as e:
        print(f"   ❌ Config error: {e}")
        return False
    
    # Test 2: Database connection
    print("\n2️⃣ Testing database models...")
    try:
        from app.models import User, Report, Conversation, Message, Progress
        print("   ✅ All models imported successfully")
    except Exception as e:
        print(f"   ❌ Models error: {e}")
        return False
    
    # Test 3: Services
    print("\n3️⃣ Testing services...")
    try:
        from app.services.knowledge_base import knowledge_base, get_all_exercises
        exercises = get_all_exercises()
        print(f"   ✅ Knowledge base loaded: {len(exercises)} exercises")
    except Exception as e:
        print(f"   ❌ Knowledge base error: {e}")
        return False
    
    try:
        from app.services.llm_service import LLMService
        llm = LLMService()
        print(f"   ✅ LLM Service initialized (API available: {llm.api_available})")
    except Exception as e:
        print(f"   ❌ LLM Service error: {e}")
        return False
    
    # Test 4: Vector Store (ChromaDB)
    print("\n4️⃣ Testing vector store...")
    try:
        from app.services.vector_store import VectorStore
        # Don't initialize yet, just import
        print("   ✅ Vector store module ready")
    except Exception as e:
        print(f"   ❌ Vector store error: {e}")
        return False
    
    # Test 5: API Endpoints
    print("\n5️⃣ Testing API endpoints...")
    try:
        from app.api.endpoints import chat, profile, progress, upload, recommendations
        print("   ✅ All endpoints imported")
    except Exception as e:
        print(f"   ❌ Endpoints error: {e}")
        return False
    
    # Test 6: Check data directories
    print("\n6️⃣ Checking data directories...")
    try:
        Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ Upload dir: {settings.UPLOAD_DIR}")
        
        Path(settings.CHROMA_PERSIST_DIR).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ ChromaDB dir: {settings.CHROMA_PERSIST_DIR}")
    except Exception as e:
        print(f"   ❌ Directory error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("✅ All startup tests passed!")
    print("=" * 50)
    print("\n📋 Next steps:")
    print("   1. Start PostgreSQL: docker-compose up -d postgres")
    print("   2. Start backend: uvicorn app.main:app --reload")
    print("   3. Start frontend: cd frontend && npm run dev")
    print("   4. Open: http://localhost:5173")
    return True

if __name__ == "__main__":
    result = asyncio.run(test_startup())
    sys.exit(0 if result else 1)
