from abc import ABC, abstractmethod

from src.retrieval.models.retrieval_result import RetrievalResult
from src.retrieval.models.retrieved_chunk import RetrievedChunk


class BaseRetriever(ABC):

    @abstractmethod
    def retrieve(
        self,
        query_vector: list[float]
    ) -> list[RetrievedChunk]:
        pass