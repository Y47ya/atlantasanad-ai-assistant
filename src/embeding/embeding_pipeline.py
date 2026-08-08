from datetime import UTC, datetime
from pathlib import Path

from src.config.settings import PROJECT_ROOT
from src.embeding.base_embeding import BaseEmbedding
from src.ingestion.models.chunk import Chunk
from src.ingestion.models.document import Document
from src.ingestion.models.indexing_metadata import IndexingMetadata
from src.ingestion.tools import generate_text_hash
from src.llm.prompts import EMBEDDING_TEMPLATE


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

        section_semantic = chunk.section.metadata.semantic
        chunk_semantic = chunk.metadata.semantic

        return EMBEDDING_TEMPLATE.format(
            document=chunk.metadata.file_name,

            section_display_title=section_semantic.display_title,
            section_summary=section_semantic.summary,
            section_keywords=", ".join(section_semantic.keywords),

            chunk_summary=chunk_semantic.summary,
            chunk_keywords=", ".join(chunk_semantic.keywords),

            chunk=chunk.text,
        )

    def process(
        self,
        document: Document,
    ) -> Document:

        file_name = document.file_name
        json_path = Path(PROJECT_ROOT / "data" / "processed_data" / "embedding_lvl" / f"{file_name}.json")

        if json_path.exists():
            print(f"Loading embedding level document: {json_path.stem}")
            document = Document.load_json(json_path)
            return document

        for chunk in document.chunks:

            embedding_text = self._build_embedding_text(chunk)

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

        document.save_json(json_path)

        return document

