from abc import ABC, abstractmethod

from src.generation.models.answer import Answer
from src.retrieval.models.retrieval_result import RetrievalResult


class BaseGenerator(ABC):

    @abstractmethod
    def generate(
        self,
        retrieval_result: RetrievalResult,
    ) -> Answer:
        pass