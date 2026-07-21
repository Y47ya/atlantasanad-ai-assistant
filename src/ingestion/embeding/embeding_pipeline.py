from datetime import UTC, datetime

from src.ingestion.embeding.base_embeding import BaseEmbedding
from src.ingestion.models.chunk import Chunk
from src.ingestion.models.document import Document
from src.ingestion.models.indexing_metadata import IndexingMetadata
from src.ingestion.tools import generate_text_hash
from src.config.prompts import EMBEDDING_TEMPLATE


class EmbeddingPipeline:

    def __init__(
        self,
        embedding_model: BaseEmbedding,
        chunking_strategy: str,
    ):
        self.embedding_model = embedding_model
        self.chunking_strategy = chunking_strategy

    def _build_embedding_text(
        self,
        chunk: Chunk,
    ) -> str:

        return EMBEDDING_TEMPLATE.format(
            document=chunk.metadata.file_name,
            section=chunk.section.title,
            section_summary=chunk.section.metadata.semantic.summary,
            section_keywords=", ".join(
                chunk.section.metadata.semantic.keywords
            ),
            chunk_summary=chunk.metadata.semantic.summary,
            chunk_keywords=", ".join(
                chunk.metadata.semantic.keywords
            ),
            chunk=chunk.text,
        )

    def process(
        self,
        document: Document,
    ) -> Document:

        for chunk in document.chunks:

            embedding_text = self._build_embedding_text(
                chunk
            )

            chunk.embedding = self.embedding_model.embed(
                embedding_text
            )

            chunk.metadata.indexing = IndexingMetadata(
                embedding_provider=self.embedding_model.provider(),
                embedding_model=self.embedding_model.model_name(),
                chunking_strategy=self.chunking_strategy,
                hash=generate_text_hash(chunk.text),
                indexed_at=datetime.now(UTC),
            )

        return document