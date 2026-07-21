from datetime import datetime
from abc import ABC, abstractmethod

from src.ingestion.models.llm_generation import LLMGenerationInfo


class BaseLLM(ABC):

    @property
    @abstractmethod
    def provider(self) -> str:
        ...

    @property
    @abstractmethod
    def model(self) -> str:
        ...

    @abstractmethod
    def generate(self, prompt: str) -> str:
        ...

    def generation_info(self) -> LLMGenerationInfo:
        return LLMGenerationInfo(
            provider=self.provider,
            model=self.model,
            generated_at=datetime.now(),
        )