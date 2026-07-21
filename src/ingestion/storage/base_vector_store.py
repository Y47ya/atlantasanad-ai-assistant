from abc import ABC, abstractmethod

from src.ingestion.models.chunk import Chunk


class BaseVectorStore(ABC):

    @abstractmethod
    def create_collection(self) -> None:
        pass

    @abstractmethod
    def upsert(self, chunks: list[Chunk]) -> None:
        pass

    @abstractmethod
    def delete_document(self, document_id: str) -> None:
        pass