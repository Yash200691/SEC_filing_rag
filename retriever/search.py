"""
Search Engine for Financial RAG

Responsibilities:
- Convert user questions into embeddings.
- Search Qdrant.
- Return relevant chunks.
"""

from typing import Dict, List, Optional

from retriever.embedding import EmbeddingModel
from retriever.qdrant_client import QdrantDB


class SearchEngine:
    """
    Handles semantic search over the vector database.
    """

    def __init__(self):
        """
        Initialize embedding model and database connection.
        """

        self.embedding_model = EmbeddingModel()
        self.db = QdrantDB()

    def search(
        self,
        question: str,
        top_k: int = 5,
        filters: Optional[Dict] = None,
    ) -> List[Dict]:
        """
        Search for the most relevant chunks.

        Args:
            question:
                User query.

            top_k:
                Number of chunks to retrieve.

            filters:
                Optional metadata filters.

        Returns:
            List of search results.
        """

        # Step 1: Generate query embedding
        query_vector = self.embedding_model.encode(question)

        # Step 2: Search vector database
        results = self.db.search(
            collection_name=self.db.collection_name,
            query_vector=query_vector,
            top_k=top_k,
            filters=filters,
        )
        # Step 3: Return results
        return results