from dataclasses import dataclass
from src.ingestion.models.chunk_metadata import ChunkMetadata
from src.ingestion.models.section import Section


@dataclass
class Chunk:
    text: str
    section: Section
    embedding: list[float] | None = None
    metadata: ChunkMetadata | None = None

    def to_payload(self):
        return {

            "chunk_id": self.metadata.chunk_id,
            # "section_title": self.section.metadata.semantic.display_title,
            # "chunk_title": self.metadata.semantic.display_title,

            "text": self.text,

            "document_id": self.metadata.document_id,
            "file_name": self.metadata.file_name,

            "page": self.section.page,

            "chunk_index": self.metadata.chunk_index,

            "section_summary":
                self.section.metadata.semantic.summary,

            "section_keywords":
                self.section.metadata.semantic.keywords,

            "chunk_summary":
                self.metadata.semantic.summary,

            "chunk_keywords":
                self.metadata.semantic.keywords,

            "indexed_at":str(self.metadata.indexing.indexed_at),
    }