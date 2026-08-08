

from src.config.settings import *
from src.ingestion.chunking.chunking_pipeline import ChunkingPipeline
from src.ingestion.cleaner.document_cleaner import DocumentCleaner
from src.embeding.embeding_pipeline import EmbeddingPipeline
from src.ingestion.metadata.chunk_metadata_pipeline import ChunkMetadataPipeline

from src.ingestion.metadata.section_metadata_pipeline import SectionMetadataPipeline
from src.ingestion.models.document import Document
from src.ingestion.parser.base_parser import BaseParser

from src.ingestion.storage.qdrant_pipeline import QdrantPipeline



class IngestionPipeline:

    def __init__(
            self,
            adapter: BaseParser,
            cleaner: DocumentCleaner,
            section_metadata_pipeline: SectionMetadataPipeline,
            chunking_pipeline: ChunkingPipeline,
            chunk_metadata_pipeline: ChunkMetadataPipeline,
            embedding_pipeline: EmbeddingPipeline,
            qdrant_pipeline: QdrantPipeline
    ):
        self.adapter = adapter
        self.cleaner = cleaner
        self.section_metadata_pipeline = section_metadata_pipeline
        self.chunking_pipeline = chunking_pipeline
        self.chunk_metadata_pipeline = chunk_metadata_pipeline
        self.embedding_pipeline = embedding_pipeline
        self.qdrant_pipeline = qdrant_pipeline


    def process(self, document_path: Path) -> Document:

        document = self.adapter.parse(document_path)

        document = self.cleaner.clean(document)

        document = self.section_metadata_pipeline.process(document)

        document = self.chunking_pipeline.process(document)

        document = self.chunk_metadata_pipeline.process(document)

        document = self.embedding_pipeline.process(document)

        document = self.qdrant_pipeline.process(document)

        return document


