from random import random

from qdrant_client import QdrantClient
from qdrant_client.http.models import NearestQuery

from src.ingestion.config.settings import QDRANT_HOST, QDRANT_PORT, QDRANT_COLLECTION_NAME
from src.retrieval.models.retrieval_result import RetrievalResult
from src.retrieval.retreivers.base_retreiver import BaseRetriever
from src.tools import create_qdrant_client


class QdrantRetriever(BaseRetriever):

    def __init__(
        self,
        client: QdrantClient,
        collection_name: str,
    ):
        self.client = client
        self.collection_name = collection_name

        print(
            self.client.count(
                collection_name=self.collection_name,
                exact=True,
            )
        )

    def retrieve(
            self,
            query_vector: list[float],
            top_k: int = 5,
    ) -> list[RetrievalResult]:

        print(self.client.get_collections())

        print(len(query_vector))

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=top_k,
            with_payload=True,
        ).points

        print(results)

        return [
            RetrievalResult(
                score=point.score,
                text=point.payload["text"],
                payload=point.payload or {},
            )
            for point in results
        ]

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
