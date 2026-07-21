from abc import ABC, abstractmethod

class BaseEmbedding(ABC):

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        ...

    @abstractmethod
    def model_name(self) -> str:
        ...

    @abstractmethod
    def provider(self) -> str:
        ...