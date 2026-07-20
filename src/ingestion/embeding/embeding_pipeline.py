from datetime import datetime, UTC
from pathlib import Path

from src.config.settings import PROJECT_ROOT
from src.ingestion.cleaner.document_cleaner import DocumentCleaner
from src.ingestion.embeding.base_embeding import BaseEmbedding
from src.ingestion.metadata.section_metadata_pipeline import SectionMetadataPipeline
from src.ingestion.metadata.semantic_metadata_generator import SemanticMetadataGenerator
from src.ingestion.models.document import Document
from src.ingestion.models.indexing_metadata import IndexingMetadata
from src.ingestion.parser.docling_converter import DoclingAdapter
from src.ingestion.tools import generate_text_hash
from src.llm.ollama import OllamaLLM


class EmbeddingPipeline:

    def __init__(
        self,
        embedding_model: BaseEmbedding,
        chunking_strategy: str,
    ):
        self.embedding_model = embedding_model
        self.chunking_strategy = chunking_strategy

    def process(
        self,
        document: Document,
    ) -> Document:

        for chunk in document.chunks:

            chunk.embedding = self.embedding_model.embed(
                chunk.text
            )

            chunk.metadata.indexing = IndexingMetadata(
                embedding_provider=self.embedding_model.provider(),
                embedding_model=self.embedding_model.model_name(),
                chunking_strategy=self.chunking_strategy,
                hash=generate_text_hash(chunk.text),
                indexed_at=datetime.now(UTC),
            )

        return document


