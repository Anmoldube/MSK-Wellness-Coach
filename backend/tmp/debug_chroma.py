"""Quick debug script for ChromaDB init"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))

from app.services.vector_store import get_vector_store
vs = get_vector_store()
print(f"Is available: {vs.is_available}")
print(f"Count: {vs.get_count()}")

# Try manual indexing
vs.index_documents([
    {"id": "test_001", "text": "test document for balance", "metadata": {"name": "Test", "category": "balance", "difficulty": "easy", "sets_reps": "3x10", "frequency": "daily", "expected_timeline": "2 weeks"}}
], doc_type="exercise")
print(f"Count after indexing: {vs.get_count()}")

# Try searching
results = vs.search_documents("balance exercises", doc_type="exercise", n_results=3)
print(f"Search results: {results}")
