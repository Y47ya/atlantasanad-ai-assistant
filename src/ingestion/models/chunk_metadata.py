from dataclasses import dataclass, field
from datetime import datetime

from src.ingestion.models.indexing_metadata import IndexingMetadata
from src.ingestion.models.llm_generation import LLMGenerationInfo
from src.ingestion.models.semantic_metadata import SemanticMetadata


@dataclass
class ChunkMetadata:
    document_id: str
    file_name: str

    chunk_id: str
    chunk_index: int

    sematic: SemanticMetadata | None = None
    indexing: IndexingMetadata | None = None
