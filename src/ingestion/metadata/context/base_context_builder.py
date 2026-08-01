from abc import ABC, abstractmethod

from src.ingestion.models.document import Document


class BaseContextBuilder(ABC):

    @abstractmethod
    def build(
        self,
        document: Document,
        section_index: int,
    ) -> str:
        pass