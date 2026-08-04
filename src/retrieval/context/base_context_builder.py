from abc import ABC, abstractmethod
from src.retrieval.models.retrieved_chunk import RetrievedChunk


class BaseContextBuilder(ABC):

    @abstractmethod
    def build(
        self,
        chunks: list[RetrievedChunk],
    ) -> str:
        pass

