from abc import ABC, abstractmethod

from src.retrieval.models.retrieval_result import RetrievalResult


class BasePromptBuilder(ABC):

    @abstractmethod
    def build(
        self,
        retrieval: RetrievalResult,
    ) -> str:
        pass