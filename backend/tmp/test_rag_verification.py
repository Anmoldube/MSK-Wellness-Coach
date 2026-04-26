"""
Quick verification test for RAG integration.
Run from backend/ directory:  python -m tmp.test_rag_verification
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))

def test_rag_vector_store():
    print("\n" + "="*60)
    print("🧪 RAG VERIFICATION TEST")
    print("="*60)

    # 1. Test vector store init
    print("\n1. Initializing Vector Store...")
    from app.services.vector_store import get_vector_store
    vs = get_vector_store()
    print(f"   Available: {vs.is_available}")
    print(f"   Stats: {vs.get_stats()}")

    # 2. Test knowledge base auto-indexing
    print("\n2. Initializing Knowledge Base (auto-indexes if empty)...")
    from app.services.knowledge_base import KnowledgeBaseService
    kb = KnowledgeBaseService()
    count = vs.get_count()
    print(f"   Total docs in ChromaDB: {count}")
    assert count > 0, "❌ ChromaDB is still empty after init!"
    print(f"   ✅ {count} documents indexed successfully")

    # 3. Test semantic search for exercises
    print("\n3. Semantic search: 'I have trouble standing on one leg'")
    results = kb.search_exercises(query="I have trouble standing on one leg")
    print(f"   Results: {[e.name for e in results]}")
    assert len(results) > 0, "❌ No exercise results returned"
    print("   ✅ Exercise semantic search works!")

    # 4. Test semantic search for products
    print("\n4. Semantic search: 'my lower back hurts when sitting at desk'")
    products = kb.search_products(query="my lower back hurts when sitting at desk")
    print(f"   Results: {[p.name for p in products]}")
    assert len(products) > 0, "❌ No product results returned"
    print("   ✅ Product semantic search works!")

    # 5. Test semantic search for care programs
    print("\n5. Semantic search: 'program to help with falls and stability in elderly'")
    programs = kb.search_care_programs(query="program to help with falls and stability in elderly")
    print(f"   Results: {[p.name for p in programs]}")
    assert len(programs) > 0, "❌ No program results returned"
    print("   ✅ Care program semantic search works!")

    print("\n" + "="*60)
    print("✅ ALL RAG TESTS PASSED!")
    print("="*60 + "\n")


if __name__ == "__main__":
    test_rag_vector_store()
