from pathlib import Path

from tqdm import tqdm

from src.config.settings import *
from src.embeding.embeding_pipeline import EmbeddingPipeline
from src.ingestion.chunking.recursive_chuner import RecursiveChunker
from src.ingestion.ingestion_pipeline import IngestionPipeline
from src.ingestion.cleaner.document_cleaner import DocumentCleaner
from src.ingestion.metadata.context.chunk_context_builder import ChunkContextBuilder
from src.ingestion.metadata.context.context_builder import ContextWindow
from src.ingestion.metadata.semantic_metadata_generator import SemanticMetadataGenerator
from src.ingestion.metadata.section_metadata_pipeline import SectionMetadataPipeline
from src.ingestion.metadata.chunk_metadata_pipeline import ChunkMetadataPipeline
from src.ingestion.chunking.chunking_pipeline import ChunkingPipeline
from src.embeding.hugging_face_embeding import HuggingFaceEmbedding
from src.ingestion.parser.docling_converter import DoclingAdapter
from src.ingestion.storage.qdrant_pipeline import QdrantPipeline
from src.ingestion.storage.qdrant_store import QdrantStore
from src.llm.ollama import OllamaLLM
from src.llm.prompts import *
from src.tools import create_qdrant_client


def build_pipeline() -> IngestionPipeline:
    adapter = DoclingAdapter()

    cleaner = DocumentCleaner()

    llm = OllamaLLM(
        model=OLLAMA_MODEL,
        provider=OLLAMA_PROVIDER,
        host=OLLAMA_HOST,
        pull_if_missing=OLLAMA_PULL_IF_MISSING,
        temperature=OLLAMA_TEMPERATURE,
    )

    semantic_generator = SemanticMetadataGenerator(llm)

    section_metadata_pipeline = SectionMetadataPipeline(
        generator=semantic_generator,
        prompt=SEMANTIC_METADATA_PROMPT,
        context_builder=ContextWindow(
            previous_sections=1,
            next_sections=1,
        ),
    )

    chunk_metadata_pipeline = ChunkMetadataPipeline(
        generator=semantic_generator,
        prompt=CHUNK_METADATA_PROMPT,
        context_builder=ChunkContextBuilder(),
    )

    chunking_pipeline = ChunkingPipeline(
        RecursiveChunker(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=CHUNK_SEPARATORS,
        )
    )

    embedding_pipeline = EmbeddingPipeline(
        embedding_model=HuggingFaceEmbedding(
            model_name=EMBEDDING_MODEL,
        ),
        chunking_strategy=CHUNKING_STRATEGY,
    )

    qdrant_pipeline = QdrantPipeline(
        QdrantStore(
            client=create_qdrant_client(
                host=QDRANT_HOST,
                port=QDRANT_PORT,
            ),
            collection_name=QDRANT_COLLECTION_NAME,
            vector_size=QDRANT_VECTOR_SIZE,
            distance=QDRANT_DISTANCE,
        )
    )

    return IngestionPipeline(
        adapter=adapter,
        cleaner=cleaner,
        section_metadata_pipeline=section_metadata_pipeline,
        chunking_pipeline=chunking_pipeline,
        chunk_metadata_pipeline=chunk_metadata_pipeline,
        embedding_pipeline=embedding_pipeline,
        qdrant_pipeline=qdrant_pipeline,
    )

def process_document(
        pipeline: IngestionPipeline,
        path: Path
):
    document = pipeline.process(path)

    print(
        f"✓ {path.name:<45} "
        f"Sections={len(document.sections):4d} "
        f"Chunks={len(document.chunks):5d}"
    )

def process_documents(
    pipeline: IngestionPipeline,
    paths: list[Path],
):
    successful = 0
    failed = []

    for pdf_path in tqdm(
        paths,
        desc="Processing documents",
        unit="pdf",
        colour="green",
    ):
        try:
            document = pipeline.process(pdf_path)
            successful += 1

            tqdm.write(
                f"✓ {pdf_path.name:<45} "
                f"Sections={len(document.sections):4d} "
                f"Chunks={len(document.chunks):5d}"
            )

        except Exception as e:
            failed.append(pdf_path.name)
            tqdm.write(f"✗ {pdf_path.name} -> {e}")

    print("\n" + "=" * 80)
    print("INGESTION SUMMARY")
    print("=" * 80)
    print(f"Processed : {successful}/{len(paths)}")

    if failed:
        print("\nFailed documents:")
        for name in failed:
            print(f" - {name}")


def main():
    paths = [
        PROJECT_ROOT / "data" / "raw" / f"{file}.pdf"
        for file in EXTERNAL_FILES_NAME
    ]

    print("=" * 80)
    print("Initializing ingestion pipeline...")
    print("=" * 80)

    pipeline = build_pipeline()

    print("\nStarting ingestion...\n")

    process_documents(
        pipeline=pipeline,
        paths=paths,
    )

    # process_document(
    #     pipeline=pipeline,
    #     path=paths[3]
    # )


if __name__ == "__main__":
    main()