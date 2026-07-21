from dataclasses import dataclass

from src.ingestion.models.indexing_metadata import IndexingMetadata
from src.ingestion.models.semantic_metadata import SemanticMetadata


@dataclass
class ChunkMetadata:
    document_id: str
    file_name: str

    chunk_id: str
    chunk_index: int

    semantic: SemanticMetadata | None = None
    indexing: IndexingMetadata | None = None
