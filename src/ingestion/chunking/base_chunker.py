from abc import ABC, abstractmethod

from src.ingestion.models.section import Section
from src.ingestion.models.chunk import Chunk


class BaseChunker(ABC):

    @abstractmethod
    def chunk(self, document_id: str, file_name: str, section: Section) -> list[Chunk]:
        pass