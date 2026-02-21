"""
Qdrant vector storage wrapper (Task 4).

This module provides a small helper class around qdrant-client to:
- create a local collection if it doesn't exist,
- upsert vectors with payloads, and
- query nearest vectors for retrieval (RAG context building).

Defaults:
- dim=3072 matches the typical output dimension of `models/gemini-embedding-001`.
"""

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

class QdrantStorage:
    """
    Minimal Qdrant storage helper used by the RAG pipeline.

    Args:
        path: Local directory where Qdrant stores its data (file-based mode).
        collection: Name of the collection that stores recipe vectors.
        dim: Embedding vector dimension (must match the embedding model output size).
    """

    def __init__(self, path = "./qdrant_db_local", collection = 'docs', dim = 3072):
        # Create Qdrant client pointing to a local storage path.
        self.client = QdrantClient(path = path, timeout = 30)
        self.collection = collection

        # Create collection once if it doesn't exist.
        # Using cosine distance is common for modern embedding models.
        if not self.client.collection_exists(self.collection):
            self.client.create_collection(
                collection_name = self.collection,
                vectors_config = VectorParams(size = dim, distance = Distance.COSINE),
            )
    def upsert(self, ids, vectors, payloads):
        """
        Insert or update multiple points in the collection.

        Args:
            ids: Sequence of IDs for points (must align with vectors/payloads by index).
            vectors: Sequence of embedding vectors (list[float]) aligned with ids.
            payloads: Sequence of metadata dicts aligned with ids (e.g., recipe fields).
        """
        # Build the list of PointStruct objects expected by qdrant-client.
        points = [PointStruct(id = ids[i], vector = vectors[i], payload = payloads[i]) for i in range(len(ids))]
        self.client.upsert(self.collection, points)

    def search(self, query_vector, top_k: int = 3):
        """
        Query the collection for nearest neighbors of query_vector.

        Args:
            query_vector: The query embedding vector.
            top_k: Number of top results to return.

        Returns:
            List of points, each containing payload (with_payload=True).
        """
        results = self.client.query_points(
            collection_name = self.collection,
            query = query_vector,
            with_payload = True,
            limit = top_k,
        )

        return results.points