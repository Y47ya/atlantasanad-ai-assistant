from uuid import uuid5, NAMESPACE_URL
from antlr4.tree import Chunk
from qdrant_client import QdrantClient
from qdrant_client.models import Distance
from qdrant_client.models import VectorParams

from src.ingestion.models.chunk import Chunk
from src.ingestion.storage.base_vector_store import BaseVectorStore
from qdrant_client.models import PointStruct

from src.ingestion.tools import chunk_hash_to_point_id


class QdrantStore(BaseVectorStore):

    def __init__(
        self,
        host: str,
        port: int,
        collection_name: str,
        vector_size: int,
        distance: str
    ):

        self.collection_name = collection_name
        self.vector_size = vector_size

        self.client = QdrantClient(
            host=host,
            port=port,
        )

        self.distance = distance

        self.create_collection()

    def create_collection(self):

        collections = self.client.get_collections()

        names = {
            c.name
            for c in collections.collections
        }

        if self.collection_name in names:
            return

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=self.vector_size,
                distance=Distance.COSINE,
            ),
        )

    def _chunk_to_point(self, chunk: Chunk) -> PointStruct:
        if chunk.embedding is None:
            raise ValueError(
                f"Chunk {chunk.metadata.chunk_id} has no embedding."
            )

        id = chunk_hash_to_point_id(chunk.metadata.chunk_id)

        return PointStruct(
            id=id,
            vector=chunk.embedding,
            payload=chunk.to_payload()
        )

    def upsert(self, chunks: list[Chunk]):

        points = [
            self._chunk_to_point(chunk)
            for chunk in chunks
        ]

        print(points)

        self.client.upsert(
            collection_name=self.collection_name,
            wait=True,
            points=points,
        )

    def delete_document(self, document_id: str):
        ...