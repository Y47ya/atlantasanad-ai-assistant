from qdrant_client import QdrantClient

from src.retrieval.models.retrieved_chunk import RetrievedChunk
from src.retrieval.retreiver.base_retreiver import BaseRetriever


class QdrantRetriever(BaseRetriever):

    def __init__(
        self,
        client: QdrantClient,
        collection_name: str,
        top_k: int
    ):
        self.client = client
        self.collection_name = collection_name
        self.top_k = top_k

        print(
            self.client.count(
                collection_name=self.collection_name,
                exact=True,
            )
        )

    def retrieve(
            self,
            query_vector: list[float]
    ) -> list[RetrievedChunk]:
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=self.top_k,
            with_payload=True,
        ).points

        retrieved_chunks = []

        for point in results:
            payload = point.payload or {}

            retrieved_chunks.append(
                RetrievedChunk(
                    score=point.score,
                    text=payload["text"],

                    document_id=payload["document_id"],
                    chunk_id=payload["chunk_id"],
                    chunk_index=payload["chunk_index"],

                    file_name=payload["file_name"],
                    page=payload["page"],
                    section_title=payload["section_title"],

                    section_summary=payload.get("section_summary"),
                    section_keywords=payload.get("section_keywords", []),

                    chunk_summary=payload.get("chunk_summary"),
                    chunk_keywords=payload.get("chunk_keywords", []),
                )
            )

        return retrieved_chunks

# qdrant_client = create_qdrant_client(
#         host=QDRANT_HOST,
#         port=QDRANT_PORT
#     )
#
#
# retriever = QdrantRetriever(
#     qdrant_client,
#     QDRANT_COLLECTION_NAME
# )
#
# query_vector = [random() for _ in range(1024)]
#
# results = retriever.retrieve(
#     query_vector
# )
#
# for result in results:
#     print(result.payload)
