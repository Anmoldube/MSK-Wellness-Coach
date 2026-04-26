"""
Document Ingestion Service — Parse documents into page-level chunks and index into ChromaDB.
Supports PDF, TXT, and CSV files.
"""
import os
import csv
import uuid
import hashlib
import math
from typing import List, Dict, Any, Optional
import structlog

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    chromadb = None

from app.core.config import settings

logger = structlog.get_logger()

# ---------------------------------------------------------------------------
# Embedding function (same hash-based approach as VectorStore)
# ---------------------------------------------------------------------------

class HashEmbeddingFunction:
    """Bag-of-words embedding using hash buckets — no model download required."""

    DIM = 512

    def name(self) -> str:
        return "hash_embedding_fn"

    def __call__(self, input):
        result = []
        for text in input:
            vec = [0.0] * self.DIM
            words = text.lower().split()
            for word in words:
                h = int(hashlib.md5(word.encode()).hexdigest(), 16)
                idx = h % self.DIM
                vec[idx] += 1.0
            norm = math.sqrt(sum(x * x for x in vec)) or 1.0
            vec = [x / norm for x in vec]
            result.append(vec)
        return result


# ---------------------------------------------------------------------------
# Document Service
# ---------------------------------------------------------------------------

class DocumentService:
    """
    Handles document parsing, chunking, and indexing into ChromaDB.
    Each document is split into page-level chunks for fine-grained retrieval.
    """

    COLLECTION_NAME = "user_documents"
    CHUNK_SIZE = 1000  # chars per chunk for TXT files

    def __init__(self):
        self.client = None
        self.collection = None
        self._init_collection()

    def _init_collection(self):
        """Initialize a separate ChromaDB collection for user documents."""
        if not CHROMADB_AVAILABLE:
            logger.warning("ChromaDB not available — document indexing disabled")
            return
        try:
            os.makedirs(settings.CHROMA_PERSIST_DIR, exist_ok=True)
            self.client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
            self.collection = self.client.get_or_create_collection(
                name=self.COLLECTION_NAME,
                embedding_function=HashEmbeddingFunction(),
                metadata={"description": "User-uploaded documents for RAG"},
            )
            logger.info("DocumentService collection ready", collection=self.COLLECTION_NAME)
        except Exception as e:
            logger.error("Failed to init document collection", error=str(e))

    @property
    def is_available(self) -> bool:
        return self.collection is not None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def ingest_file(self, file_path: str, filename: str, user_id: str, doc_id: str) -> Dict[str, Any]:
        """
        Parse a file into chunks and index them into ChromaDB.

        Returns:
            dict with page_count, chunk_count, status
        """
        ext = os.path.splitext(filename)[1].lower()
        try:
            if ext == ".pdf":
                chunks = self._parse_pdf(file_path)
            elif ext == ".txt":
                chunks = self._parse_txt(file_path)
            elif ext == ".csv":
                chunks = self._parse_csv(file_path)
            else:
                return {"page_count": 0, "chunk_count": 0, "status": "failed", "error": f"Unsupported file type: {ext}"}

            if not chunks:
                return {"page_count": 0, "chunk_count": 0, "status": "failed", "error": "No content extracted"}

            self._index_chunks(chunks, doc_id=doc_id, user_id=user_id, filename=filename)

            page_count = max(c.get("page", 1) for c in chunks)
            return {"page_count": page_count, "chunk_count": len(chunks), "status": "indexed"}

        except Exception as e:
            logger.error("Document ingestion failed", error=str(e), filename=filename)
            return {"page_count": 0, "chunk_count": 0, "status": "failed", "error": str(e)}

    def search_user_documents(self, query: str, user_id: str, n_results: int = 3) -> List[Dict[str, Any]]:
        """Semantic search across a user's uploaded documents."""
        if not self.is_available:
            return []
        try:
            total = self.collection.count()
            if total == 0:
                return []
            n_results = min(n_results, total)

            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                where={"user_id": user_id},
            )

            formatted = []
            if results.get("ids") and results["ids"][0]:
                for i, chunk_id in enumerate(results["ids"][0]):
                    formatted.append({
                        "chunk_id": chunk_id,
                        "text": results["documents"][0][i],
                        "metadata": results["metadatas"][0][i],
                        "distance": results["distances"][0][i] if "distances" in results else None,
                    })
            return formatted
        except Exception as e:
            logger.error("Document search failed", error=str(e))
            return []

    def get_document_chunks(self, doc_id: str) -> int:
        """Return number of chunks for a given document."""
        if not self.is_available:
            return 0
        try:
            results = self.collection.get(where={"doc_id": doc_id})
            return len(results.get("ids", []))
        except Exception:
            return 0

    def delete_document(self, doc_id: str) -> bool:
        """Remove all chunks for a document from ChromaDB."""
        if not self.is_available:
            return False
        try:
            results = self.collection.get(where={"doc_id": doc_id})
            ids = results.get("ids", [])
            if ids:
                self.collection.delete(ids=ids)
            logger.info("Document chunks deleted", doc_id=doc_id, count=len(ids))
            return True
        except Exception as e:
            logger.error("Failed to delete document chunks", error=str(e))
            return False

    # ------------------------------------------------------------------
    # Parsers
    # ------------------------------------------------------------------

    def _parse_pdf(self, path: str) -> List[Dict[str, Any]]:
        """Extract text per page from a PDF."""
        try:
            from PyPDF2 import PdfReader
        except ImportError:
            logger.error("PyPDF2 not installed — cannot parse PDF files")
            return []

        reader = PdfReader(path)
        chunks = []
        for page_num, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            if text and text.strip():
                chunks.append({"text": text.strip(), "page": page_num})
        return chunks

    def _parse_txt(self, path: str) -> List[Dict[str, Any]]:
        """Split text file into fixed-size chunks."""
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        if not content.strip():
            return []

        # Split by double newline first, then by chunk size
        paragraphs = content.split("\n\n")
        chunks = []
        current_chunk = ""
        page = 1

        for para in paragraphs:
            if len(current_chunk) + len(para) > self.CHUNK_SIZE and current_chunk:
                chunks.append({"text": current_chunk.strip(), "page": page})
                current_chunk = para
                page += 1
            else:
                current_chunk += "\n\n" + para if current_chunk else para

        if current_chunk.strip():
            chunks.append({"text": current_chunk.strip(), "page": page})

        return chunks

    def _parse_csv(self, path: str) -> List[Dict[str, Any]]:
        """Each row becomes a chunk, grouped into logical pages of 20 rows."""
        chunks = []
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames or []
            for row_num, row in enumerate(reader, start=1):
                text = ", ".join(f"{k}: {v}" for k, v in row.items() if v)
                if text:
                    chunks.append({"text": text, "page": (row_num - 1) // 20 + 1})
        return chunks

    # ------------------------------------------------------------------
    # Indexing
    # ------------------------------------------------------------------

    def _index_chunks(self, chunks: List[Dict], doc_id: str, user_id: str, filename: str):
        """Upsert document chunks into ChromaDB."""
        if not self.is_available:
            return

        ids = []
        documents = []
        metadatas = []

        for i, chunk in enumerate(chunks):
            chunk_id = f"doc_{doc_id}_chunk_{i}"
            ids.append(chunk_id)
            documents.append(chunk["text"])
            metadatas.append({
                "doc_id": doc_id,
                "user_id": user_id,
                "filename": filename,
                "page": chunk.get("page", i + 1),
                "chunk_index": i,
            })

        self.collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
        logger.info("Indexed document chunks", doc_id=doc_id, count=len(chunks))


# ---------------------------------------------------------------------------
# Singleton
# ---------------------------------------------------------------------------

_document_service: Optional[DocumentService] = None


def get_document_service() -> DocumentService:
    global _document_service
    if _document_service is None:
        _document_service = DocumentService()
    return _document_service
