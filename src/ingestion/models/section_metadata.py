from dataclasses import dataclass, field
from src.ingestion.models.llm_generation import LLMGenerationInfo
from src.ingestion.models.semantic_metadata import SemanticMetadata


@dataclass
class SectionMetadata:

    semantic: SemanticMetadata = field(default_factory=SemanticMetadata)
    # generation: LLMGenerationInfo | None = None