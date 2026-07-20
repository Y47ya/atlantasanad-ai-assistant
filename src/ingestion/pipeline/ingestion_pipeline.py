from pathlib import Path

from httpx import _main

from src.config.settings import *
from src.ingestion.chunking.chunking_pipeline import ChunkingPipeline
from src.ingestion.chunking.recursive_chuner import RecursiveChunker
from src.ingestion.cleaner.document_cleaner import DocumentCleaner
from src.ingestion.embeding.embeding_pipeline import EmbeddingPipeline
from src.ingestion.embeding.hugging_face_embeding import HuggingFaceEmbedding
from src.ingestion.metadata.chunk_metadata_pipeline import ChunkMetadataPipeline
from src.ingestion.metadata.section_metadata_pipeline import SectionMetadataPipeline
from src.ingestion.metadata.semantic_metadata_generator import SemanticMetadataGenerator
from src.ingestion.models.document import Document
from src.ingestion.parser.docling_converter import DoclingAdapter
from src.llm.base_llm import BaseLLM
from src.llm.ollama import OllamaLLM
from src.llm.prompts import SEMANTIC_METADATA_PROMPT


class IngestionPipeline:

    def __init__(
            self,
            adapter: DoclingAdapter,
            cleaner: DocumentCleaner,
            section_metadata_pipeline: SectionMetadataPipeline,
            chunking_pipeline: ChunkingPipeline,
            chunk_metadata_pipeline: ChunkMetadataPipeline,
            embedding_pipeline: EmbeddingPipeline,
    ):
        self.adapter = adapter
        self.cleaner = cleaner
        self.section_metadata_pipeline = section_metadata_pipeline
        self.chunking_pipeline = chunking_pipeline
        self.chunk_metadata_pipeline = chunk_metadata_pipeline
        self.embedding_pipeline = embedding_pipeline

    def process(self, pdf_path: Path) -> Document:
        document = self.adapter.parse(pdf_path)

        document = self.cleaner.clean(document)

        document = self.section_metadata_pipeline.process(document)

        document = self.chunking_pipeline.process(document)

        document = self.chunk_metadata_pipeline.process(document)

        document = self.embedding_pipeline.process(document)

        return document


def main():

    print("=" * 80)
    print("Starting ingestion pipeline")
    print("=" * 80)

    pdf_path = Path(
        PROJECT_ROOT / "data/raw/Véhicule_pro.pdf"
    )

    print(f"[1/8] PDF: {pdf_path.name}")

    print("[2/8] Initializing parser...")
    adapter = DoclingAdapter()

    print("[3/8] Initializing cleaner...")
    cleaner = DocumentCleaner()

    print("[4/8] Initializing LLM...")
    llm = OllamaLLM(
        model=OLLAMA_MODEL,
        provider=OLLAMA_PROVIDER,
        host=OLLAMA_HOST,
        pull_if_missing=OLLAMA_PULL_IF_MISSING,
        temperature=OLLAMA_TEMPERATURE,
    )

    semantic_generator = SemanticMetadataGenerator(llm)

    print("[5/8] Initializing metadata pipelines...")

    section_metadata_pipeline = SectionMetadataPipeline(
        semantic_generator,
        SEMANTIC_METADATA_PROMPT,
    )

    chunk_metadata_pipeline = ChunkMetadataPipeline(
        semantic_generator,
        SEMANTIC_METADATA_PROMPT,
    )

    print("[6/8] Initializing chunker...")

    chunker = RecursiveChunker(
        CHUNK_SIZE,
        CHUNK_OVERLAP,
        CHUNK_SEPARATORS,
    )

    chunking_pipeline = ChunkingPipeline(chunker)

    print("[7/8] Loading embedding model...")

    embedding_model = HuggingFaceEmbedding(
        model_name=EMBEDDING_MODEL,
    )

    embedding_pipeline = EmbeddingPipeline(
        embedding_model=embedding_model,
        chunking_strategy=CHUNKING_STRATEGY,
    )

    print("[8/8] Building ingestion pipeline...")

    ingestion_pipeline = IngestionPipeline(
        adapter=adapter,
        cleaner=cleaner,
        section_metadata_pipeline=section_metadata_pipeline,
        chunking_pipeline=chunking_pipeline,
        chunk_metadata_pipeline=chunk_metadata_pipeline,
        embedding_pipeline=embedding_pipeline,
    )

    print()
    print("=" * 80)
    print("Running ingestion...")
    print("=" * 80)

    document = ingestion_pipeline.process(pdf_path)

    print()
    print("=" * 80)
    print("Pipeline finished successfully")
    print("=" * 80)

    print(f"Document: {document.title}")
    print(f"Pages: {document.pages_count}")
    print(f"Sections: {len(document.sections)}")
    print(f"Chunks: {len(document.chunks)}")


if __name__ == "__main__":
    main()