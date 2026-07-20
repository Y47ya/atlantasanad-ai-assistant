from dataclasses import dataclass, field
from src.ingestion.models.llm_generation import LLMGenerationInfo


@dataclass
class SemanticMetadata:

    summary: str = ""

    keywords: list[str] = field(default_factory=list)

    generation: LLMGenerationInfo | None = None