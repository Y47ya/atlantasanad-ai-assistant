from qdrant_client import QdrantClient
from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchValue,
    Range,
)

from src.retrieval.models.retrieval_result import RetrievalResult
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

    def _to_retrieved_chunk(self, payload: dict, score: float) -> RetrievedChunk:
        return RetrievedChunk(
            score=score,
            text=payload["text"],

            document_id=payload["document_id"],
            chunk_id=payload["chunk_id"],
            chunk_index=payload["chunk_index"],

            file_name=payload["file_name"],
            page=payload["page"],

            section_summary=payload.get("section_summary"),
            section_keywords=payload.get("section_keywords", []),

            chunk_summary=payload.get("chunk_summary"),
            chunk_keywords=payload.get("chunk_keywords", []),
        )

    def retrieve_neighbors(
            self,
            document_id: str,
            chunk_index: int,
            window: int = 1,
    ) -> list[RetrievedChunk]:

        points = self.client.scroll(
            collection_name=self.collection_name,
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="document_id",
                        match=MatchValue(value=document_id),
                    ),
                    FieldCondition(
                        key="chunk_index",
                        range=Range(
                            gte=chunk_index - window,
                            lte=chunk_index + window,
                        ),
                    ),
                ]
            ),
            with_payload=True,
            limit=2 * window + 1,
        )[0]

        neighbors = []

        neighbors = []

        for point in points:
            neighbors.append(
                self._to_retrieved_chunk(
                    point.payload or {},
                    1.0,
                )
            )

        return neighbors

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
            retrieved_chunks.append(
                self._to_retrieved_chunk(
                    point.payload or {},
                    point.score,
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
