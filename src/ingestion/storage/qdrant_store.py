from pprint import pprint

from qdrant_client.models import Distance
from qdrant_client.models import VectorParams

from src.ingestion.models.chunk import Chunk
from src.ingestion.storage.base_vector_store import BaseVectorStore
from qdrant_client.models import PointStruct

from src.ingestion.tools import chunk_hash_to_point_id
from qdrant_client import QdrantClient

from src.retrieval.models.retrieved_chunk import RetrievedChunk


class QdrantStore(BaseVectorStore):

    def __init__(
        self,
        client: QdrantClient,
        collection_name: str,
        vector_size: int,
        distance: str
    ):

        self.collection_name = collection_name
        self.vector_size = vector_size

        self.client = client

        self.distance = distance

        self.create_collection()

    def create_collection(self):

        collections = self.client.get_collections()

        names = {
            c.name
            for c in collections.collections
        }

        if self.collection_name in names:
            print(f"{self.collection_name} already exists.")
            return

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=self.vector_size,
                distance=Distance.COSINE,
            ),
        )
        print(f"{self.collection_name} created.")

    def chunk_to_point(self, chunk: Chunk) -> PointStruct:
        if chunk.embedding is None:
            raise ValueError(
                f"Chunk {chunk.metadata.chunk_id} has no embedding."
            )

        id = chunk_hash_to_point_id(chunk.metadata.chunk_id)

        point = PointStruct(
            id=id,
            vector=chunk.embedding,
            payload=chunk.to_payload()
        )

        return point

    def upsert(self, chunks: list[Chunk]):

        points = [
            self.chunk_to_point(chunk)
            for chunk in chunks
        ]

        self.client.upsert(
            collection_name=self.collection_name,
            wait=True,
            points=points,
        )

    def point_to_chunk(self, point) -> RetrievedChunk:

        payload = point.payload

        return RetrievedChunk(
            text=payload["text"],
            score=point.score,

            chunk_id=payload["chunk_id"],
            chunk_index=payload["chunk_index"],
            document_id=payload["document_id"],
            file_name=payload["file_name"],
            page=payload["page"],

            section_title=payload["section_title"],

            section_summary=payload["section_summary"],
            section_keywords=payload["section_keywords"],

            chunk_summary=payload["chunk_summary"],
            chunk_keywords=payload["chunk_keywords"],

            indexed_at=payload["indexed_at"]
        )

    def delete_document(self, document_id: str):
        ...