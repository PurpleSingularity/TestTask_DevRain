"""
Qdrant vector storage wrapper.

Provides a tiny abstraction over qdrant-client:
- creates a collection if it doesn't exist,
- upserts points (id, vector, payload),
- queries nearest points for a given vector.

Defaults assume Gemini embedding size 3072 for `gemini-embedding-001`.
"""

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

class QdrantStorage:
    """
    Minimal Qdrant storage helper for local filesystem-backed Qdrant.

    Args:
        path: Local Qdrant storage directory path.
        collection: Collection name to use/create.
        dim: Vector dimension (must match embedding model output size).
    """

    def __init__(self, path = "./qdrant_db_local", collection = 'docs', dim = 3072):
        # Create a client pointing at a local Qdrant storage path.
        self.client = QdrantClient(path = path, timeout = 30)
        self.collection = collection

        # Ensure the collection exists; create it once if missing.
        # Using cosine distance is common for modern embedding models.
        if not self.client.collection_exists(self.collection):
            self.client.create_collection(
                collection_name = self.collection,
                vectors_config = VectorParams(size = dim, distance = Distance.COSINE),
            )

    def upsert(self, ids, vectors, payloads):
        """
        Upsert multiple points into the collection.

        Args:
            ids: Sequence of point IDs (strings/ints).
            vectors: Sequence of embedding vectors (lists of floats).
            payloads: Sequence of payload dicts (metadata stored alongside vectors).
        """
        # Build Qdrant PointStruct objects from aligned lists.
        points = [PointStruct(id = ids[i], vector = vectors[i], payload = payloads[i]) for i in range(len(ids))]
        self.client.upsert(self.collection, points)

    def search(self, query_vector, top_k: int = 3):
        """
        Search the collection for nearest neighbors of query_vector.

        Args:
            query_vector: Embedding vector (list[float]).
            top_k: Maximum number of results to return.

        Returns:
            List of scored points (with payload included).
        """
        results = self.client.query_points(
            collection_name = self.collection,
            query = query_vector,
            with_payload = True,
            limit = top_k,
        )

        return results.points