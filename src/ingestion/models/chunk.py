from dataclasses import dataclass, field
from src.ingestion.models.chunk_metadata import ChunkMetadata
from src.ingestion.models.section import Section


@dataclass
class Chunk:
    text: str
    section: Section
    embedding: list[float] | None = None
    metadata: ChunkMetadata | None = None