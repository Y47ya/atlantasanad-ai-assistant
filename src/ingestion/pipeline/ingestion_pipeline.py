from src.ingestion.config.settings import *
from src.ingestion.chunking.chunking_pipeline import ChunkingPipeline
from src.ingestion.chunking.recursive_chuner import RecursiveChunker
from src.ingestion.cleaner.document_cleaner import DocumentCleaner
from src.embeding.embeding_pipeline import EmbeddingPipeline
from src.embeding.hugging_face_embeding import HuggingFaceEmbedding
from src.ingestion.metadata.chunk_metadata_pipeline import ChunkMetadataPipeline
from src.ingestion.metadata.section_metadata_pipeline import SectionMetadataPipeline
from src.ingestion.metadata.semantic_metadata_generator import SemanticMetadataGenerator
from src.ingestion.models.document import Document
from src.ingestion.parser.docling_converter import DoclingAdapter
from src.ingestion.storage.qdrant_pipeline import QdrantPipeline
from src.ingestion.storage.qdrant_store import QdrantStore
from src.ingestion.llms.ollama import OllamaLLM
from src.ingestion.config.prompts import SEMANTIC_METADATA_PROMPT


class IngestionPipeline:

    def __init__(
            self,
            adapter: DoclingAdapter,
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
        # document = self.adapter.parse(pdf_path)
        #
        # document = self.cleaner.clean(document)
        #
        # document = self.section_metadata_pipeline.process(document)
        #
        # print(
        #     dumps(
        #         document.to_dict(),
        #         indent=4,
        #         ensure_ascii=False,
        #         default=str,
        #     )
        # )
        #
        # document = self.chunking_pipeline.process(document)
        #
        # document = self.chunk_metadata_pipeline.process(document)
        #
        # print(
        #     dumps(
        #         document.to_dict(),
        #         indent=4,
        #         ensure_ascii=False,
        #         default=str,
        #     )
        # )
        #
        # document = self.embedding_pipeline.process(document)

        document_path = Path(
            PROJECT_ROOT / "tests/processed_data/Véhicule-pro-splited-version.json"
        )


        document = Document.load_json(document_path)

        document = self.qdrant_pipeline.process(document)

        return document


def main():

    print("=" * 80)
    print("Starting ingestion pipeline")
    print("=" * 80)

    # pdf_path = Path(
    #     PROJECT_ROOT / "data/raw/assurance_automobile_fr_version_finale.pdf"
    # )

    pdf_path = Path(
        PROJECT_ROOT / "data/raw/Véhicule-pro-splited-version.pdf"
    )

    print(f"[1/9] PDF: {pdf_path.name}")

    print("[2/9] Initializing parser...")
    adapter = DoclingAdapter()

    print("[3/9] Initializing cleaner...")
    cleaner = DocumentCleaner()

    print("[4/9] Initializing LLM...")
    llm = OllamaLLM(
        model=OLLAMA_MODEL,
        provider=OLLAMA_PROVIDER,
        host=OLLAMA_HOST,
        pull_if_missing=OLLAMA_PULL_IF_MISSING,
        temperature=OLLAMA_TEMPERATURE,
    )

    semantic_generator = SemanticMetadataGenerator(llm)

    print("[5/9] Initializing metadata pipelines...")

    section_metadata_pipeline = SectionMetadataPipeline(
        semantic_generator,
        SEMANTIC_METADATA_PROMPT,
    )

    chunk_metadata_pipeline = ChunkMetadataPipeline(
        semantic_generator,
        SEMANTIC_METADATA_PROMPT,
    )

    print("[6/9] Initializing chunker...")

    chunker = RecursiveChunker(
        CHUNK_SIZE,
        CHUNK_OVERLAP,
        CHUNK_SEPARATORS,
    )

    chunking_pipeline = ChunkingPipeline(chunker)

    print("[7/9] Loading embedding model...")

    embedding_model = HuggingFaceEmbedding(
        model_name=EMBEDDING_MODEL,
    )

    embedding_pipeline = EmbeddingPipeline(
        embedding_model=embedding_model,
        chunking_strategy=CHUNKING_STRATEGY,
    )

    print("[8/9] Building ingestion pipeline...")

    qdrant_store = QdrantStore(
        host=QDRANT_HOST,
        port=QDRANT_PORT,
        collection_name=QDRANT_COLLECTION_NAME,
        vector_size=QDRANT_VECTOR_SIZE,
        distance=QDRANT_DISTANCE
    )

    qdrant_pipeline = QdrantPipeline(
        qdrant_store
    )

    ingestion_pipeline = IngestionPipeline(
        adapter=adapter,
        cleaner=cleaner,
        section_metadata_pipeline=section_metadata_pipeline,
        chunking_pipeline=chunking_pipeline,
        chunk_metadata_pipeline=chunk_metadata_pipeline,
        embedding_pipeline=embedding_pipeline,
        qdrant_pipeline=qdrant_pipeline
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

    output_dir = PROJECT_ROOT / "tests" / "processed_data"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"{document.file_name.removesuffix('.pdf')}.json"

    document.save_json(output_file)

    print(f"Saved processed document to {output_file}")


if __name__ == "__main__":
    main()