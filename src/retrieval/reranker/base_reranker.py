from abc import ABC, abstractmethod

from src.retrieval.models.retrieved_chunk import RetrievedChunk


class BaseReranker(ABC):

    @abstractmethod
    def rerank(
        self,
        query: str,
        chunks: list[RetrievedChunk],
    ) -> list[RetrievedChunk]:
        pass