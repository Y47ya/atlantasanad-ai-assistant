from abc import ABC, abstractmethod

from src.retrieval.models.retrieval_result import RetrievalResult


class BaseRetriever(ABC):

    @abstractmethod
    def retrieve(
        self,
        query_vector: list[float],
        top_k: int,
    ) -> list[RetrievalResult]:
        pass