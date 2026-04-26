"""
Vector store service using ChromaDB for semantic search (True RAG)
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
    Vector store for semantic search of MSK wellness knowledge base.
    Supports exercises, care programs, and products.
    """


    def _make_embedding_function(self):
        """
        Lightweight hash-based embedding function — zero downloads, instant startup.
        Uses bag-of-words hashing for document similarity search.
        Suitable for MSK wellness knowledge base keyword/phrase matching.
        """
        import hashlib
        import math

        class HashEmbeddingFunction:
            """Bag-of-words embedding using hash buckets, no model download required."""

            def name(self) -> str:  # ChromaDB v1.x calls name() as a method
                return "hash_embedding_fn"

            DIM = 512


            def __call__(self, input):
                result = []
                for text in input:
                    vec = [0.0] * self.DIM
                    words = text.lower().split()
                    for word in words:
                        h = int(hashlib.md5(word.encode()).hexdigest(), 16)
                        idx = h % self.DIM
                        vec[idx] += 1.0
                    # L2 normalize
                    norm = math.sqrt(sum(x * x for x in vec)) or 1.0
                    vec = [x / norm for x in vec]
                    result.append(vec)
                return result

        return HashEmbeddingFunction()


    def __init__(self):
        """Initialize ChromaDB client with a persistent collection"""
        if not CHROMADB_AVAILABLE:
            logger.warning("ChromaDB not available, vector store disabled - falling back to keyword search")
            self.client = None
            self.collection = None
            return

        try:
            import os
            os.makedirs(settings.CHROMA_PERSIST_DIR, exist_ok=True)

            self.client = chromadb.PersistentClient(
                path=settings.CHROMA_PERSIST_DIR,
            )

            embedding_fn = self._make_embedding_function()

            # Get or create a single unified collection for all MSK knowledge
            self.collection = self.client.get_or_create_collection(
                name=settings.CHROMA_COLLECTION_NAME,
                embedding_function=embedding_fn,
                metadata={"description": "MSK Wellness knowledge base: exercises, care programs, and products"}
            )

            logger.info("VectorStore initialized", collection=settings.CHROMA_COLLECTION_NAME)
        except Exception as e:
            logger.error("Failed to initialize ChromaDB", error=str(e))
            self.client = None
            self.collection = None


    @property
    def is_available(self) -> bool:
        return self.collection is not None

    def get_count(self) -> int:
        """Return total number of documents in the collection"""
        if not self.is_available:
            return 0
        try:
            return self.collection.count()
        except Exception:
            return 0

    def index_documents(self, documents: List[Dict[str, Any]], doc_type: str) -> None:
        """
        Index any MSK knowledge document into ChromaDB.

        Args:
            documents: List of document dicts with 'id', 'text' (searchable), and 'metadata'.
            doc_type: One of 'exercise', 'care_program', 'product'.
        """
        if not self.is_available:
            logger.warning("Vector store not available, skipping indexing")
            return

        if not documents:
            return

        try:
            doc_texts = []
            metadatas = []
            ids = []

            for doc in documents:
                doc_texts.append(doc["text"])
                # Always inject doc_type into metadata so we can filter later
                meta = {**doc.get("metadata", {}), "doc_type": doc_type}
                metadatas.append(meta)
                ids.append(f"{doc_type}_{doc['id']}")

            # Use upsert so re-indexing won't fail on duplicate IDs
            self.collection.upsert(
                documents=doc_texts,
                metadatas=metadatas,
                ids=ids
            )

            logger.info(
                "Documents indexed successfully",
                doc_type=doc_type,
                count=len(documents)
            )
        except Exception as e:
            logger.error("Error indexing documents", doc_type=doc_type, error=str(e))

    def search_documents(
        self,
        query: str,
        doc_type: Optional[str] = None,
        n_results: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Perform semantic search across the knowledge base.

        Args:
            query: Natural language query string.
            doc_type: Optional filter — 'exercise', 'care_program', or 'product'.
            n_results: Max number of results to return.

        Returns:
            List of dicts with 'id', 'metadata', and 'distance'.
        """
        if not self.is_available:
            logger.warning("Vector store not available, returning empty results")
            return []

        try:
            # Clamp n_results to collection size to avoid ChromaDB errors
            total = self.get_count()
            if total == 0:
                return []
            n_results = min(n_results, total)

            where_filter = {"doc_type": doc_type} if doc_type else None

            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where_filter
            )

            formatted = []
            if results.get("ids") and len(results["ids"]) > 0:
                for i, doc_id in enumerate(results["ids"][0]):
                    formatted.append({
                        "id": doc_id,
                        "metadata": results["metadatas"][0][i],
                        "document": results["documents"][0][i],
                        "distance": results["distances"][0][i] if "distances" in results else None
                    })

            logger.info(
                "Semantic search completed",
                query=query[:60],
                doc_type=doc_type,
                results_count=len(formatted)
            )
            return formatted

        except Exception as e:
            logger.error("Error searching documents", error=str(e), query=query)
            return []

    def clear_collection(self) -> None:
        """Delete and recreate the collection (for re-indexing)"""
        if not self.client:
            return
        try:
            self.client.delete_collection(settings.CHROMA_COLLECTION_NAME)
            self.collection = self.client.get_or_create_collection(
                name=settings.CHROMA_COLLECTION_NAME,
                metadata={"description": "MSK Wellness knowledge base: exercises, care programs, and products"}
            )
            logger.info("Collection cleared and recreated")
        except Exception as e:
            logger.error("Error clearing collection", error=str(e))

    def get_stats(self) -> Dict[str, Any]:
        """Return collection statistics"""
        if not self.is_available:
            return {
                "collection_name": settings.CHROMA_COLLECTION_NAME,
                "total_documents": 0,
                "persist_directory": settings.CHROMA_PERSIST_DIR,
                "status": "disabled"
            }
        try:
            return {
                "collection_name": settings.CHROMA_COLLECTION_NAME,
                "total_documents": self.collection.count(),
                "persist_directory": settings.CHROMA_PERSIST_DIR,
                "status": "active"
            }
        except Exception as e:
            logger.error("Error getting stats", error=str(e))
            return {}


# Global singleton
_vector_store: Optional[VectorStore] = None


def get_vector_store() -> VectorStore:
    """Get or create the global VectorStore instance"""
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore()
    return _vector_store
