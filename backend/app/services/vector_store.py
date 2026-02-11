"""
Vector store service using ChromaDB for semantic search
"""
try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    chromadb = None
    Settings = None

from typing import List, Dict, Any, Optional
import structlog

from app.core.config import settings

logger = structlog.get_logger()


class VectorStore:
    """
    Vector store for semantic search of exercises and recommendations
    """
    
    def __init__(self):
        """Initialize ChromaDB client"""
        if not CHROMADB_AVAILABLE:
            logger.warning("ChromaDB not available, vector store disabled")
            self.client = None
            self.collection = None
            return
            
        self.client = chromadb.Client(Settings(
            persist_directory=settings.CHROMA_PERSIST_DIR,
            anonymized_telemetry=False,
        ))
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION_NAME,
            metadata={"description": "Exercise recommendations for athletes"}
        )
        
        logger.info("VectorStore initialized", collection=settings.CHROMA_COLLECTION_NAME)
    
    def index_exercises(self, exercises: List[Dict[str, Any]]) -> None:
        """
        Index exercises into ChromaDB for semantic search
        
        Args:
            exercises: List of exercise dictionaries with id, name, description, etc.
        """
        if not self.collection:
            logger.warning("Vector store not available, skipping indexing")
            return
            
        try:
            documents = []
            metadatas = []
            ids = []
            
            for exercise in exercises:
                # Create searchable text
                doc_text = f"{exercise['name']}. {exercise['description']}. "
                doc_text += f"Category: {exercise['category']}. "
                doc_text += f"Benefits: {', '.join(exercise.get('benefits', []))}. "
                doc_text += f"Target areas: {', '.join(exercise.get('target_areas', []))}"
                
                documents.append(doc_text)
                metadatas.append({
                    "name": exercise['name'],
                    "category": exercise['category'],
                    "difficulty": exercise.get('difficulty', 'intermediate'),
                    "duration": exercise.get('duration', ''),
                })
                ids.append(exercise['id'])
            
            # Add to ChromaDB
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info("Exercises indexed successfully", count=len(exercises))
            
        except Exception as e:
            logger.error("Error indexing exercises", error=str(e))
            raise
    
    def search_exercises(
        self,
        query: str,
        n_results: int = 5,
        category_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for relevant exercises using semantic search
        
        Args:
            query: Natural language query
            n_results: Number of results to return
            category_filter: Optional category to filter by
            
        Returns:
            List of matching exercises with metadata
        """
        if not self.collection:
            logger.warning("Vector store not available, returning empty results")
            return []
            
        try:
            where_filter = {"category": category_filter} if category_filter else None
            
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where_filter
            )
            
            # Format results
            exercises = []
            if results['ids'] and len(results['ids']) > 0:
                for i, exercise_id in enumerate(results['ids'][0]):
                    exercises.append({
                        'id': exercise_id,
                        'metadata': results['metadatas'][0][i],
                        'distance': results['distances'][0][i] if 'distances' in results else None
                    })
            
            logger.info("Exercise search completed", query=query, results_count=len(exercises))
            return exercises
            
        except Exception as e:
            logger.error("Error searching exercises", error=str(e), query=query)
            return []
    
    def clear_collection(self) -> None:
        """Clear all data from the collection"""
        try:
            self.client.delete_collection(settings.CHROMA_COLLECTION_NAME)
            self.collection = self.client.get_or_create_collection(
                name=settings.CHROMA_COLLECTION_NAME,
                metadata={"description": "Exercise recommendations for athletes"}
            )
            logger.info("Collection cleared successfully")
        except Exception as e:
            logger.error("Error clearing collection", error=str(e))
            raise
    
    def get_stats(self) -> Dict[str, Any]:
        """Get collection statistics"""
        if not self.collection:
            return {
                "collection_name": settings.CHROMA_COLLECTION_NAME,
                "total_exercises": 0,
                "persist_directory": settings.CHROMA_PERSIST_DIR,
                "status": "disabled"
            }
            
        try:
            count = self.collection.count()
            return {
                "collection_name": settings.CHROMA_COLLECTION_NAME,
                "total_exercises": count,
                "persist_directory": settings.CHROMA_PERSIST_DIR
            }
        except Exception as e:
            logger.error("Error getting stats", error=str(e))
            return {}


# Global instance
_vector_store: Optional[VectorStore] = None


def get_vector_store() -> VectorStore:
    """Get or create the global VectorStore instance"""
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore()
    return _vector_store
