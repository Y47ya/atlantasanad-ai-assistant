from json import dumps
from pathlib import Path

from src.config.settings import PROJECT_ROOT, CHUNK_SIZE, CHUNK_OVERLAP, CHUNK_SEPARATORS
from src.ingestion.chunking.base_chunker import BaseChunker
from src.ingestion.chunking.recursive_chuner import RecursiveChunker
from src.ingestion.cleaner.document_cleaner import DocumentCleaner
from src.ingestion.models.document import Document
from src.ingestion.parser.docling_converter import DoclingAdapter


class ChunkingPipeline:

    def __init__(self, chunker: BaseChunker):
        self.chunker = chunker

    def process(self, document: Document) -> Document:

        document.chunks.clear()

        document_id = document.id
        file_name = document.file_name


        for section in document.sections:
            chunks = self.chunker.chunk(
                document_id=document_id,
                file_name=file_name,
                section=section
            )
            document.chunks.extend(chunks)

        return document


# if __name__ == "__main__":
#
#     file_path = Path(PROJECT_ROOT / "data/raw/Véhicule_pro.pdf")
#     file_path1 = Path(PROJECT_ROOT / "data/raw/assurance_automobile_fr_version_finale.pdf")
#
#     parsed_data_dir = Path(PROJECT_ROOT / "tests/parsed_data")
#
#     parsed_data_dir.parent.mkdir(exist_ok=True)
#     parsed_data_dir.mkdir(exist_ok=True)
#
#     adapter = DoclingAdapter()
#     cleaner = DocumentCleaner()
#
#     chunker = RecursiveChunker(
#         chunk_size=CHUNK_SIZE,
#         chunk_overlap=CHUNK_OVERLAP,
#         separators=CHUNK_SEPARATORS
#     )
#
#     chunking_pipe = ChunkingPipeline(chunker)
#
#     # ollama_model = OllamaLLM(
#     #     model=OLLAMA_MODEL,
#     #     provider=OLLAMA_PROVIDER,
#     #     host=OLLAMA_HOST,
#     #     pull_if_missing=OLLAMA_PULL_IF_MISSING,
#     #     temperature=OLLAMA_TEMPERATURE
#     # )
#
#     # section_metadata_generator = SectionMetadataGenerator(ollama_model)
#
#     # section_metadata_pipeline = SectionMetadataPipeline(section_metadata_generator)
#
#     # docliing_adapter.parse(file_path)
#
#     document = adapter.parse(file_path)
#     print("document is parsed")
#     cleaned_document = cleaner.clean(document)
#     print("document is cleaned")
#     # document_with_section_metadata = section_metadata_pipeline.process(document)
#     print("metadata is generated")
#     document_with_chunks = chunking_pipe.process(cleaned_document)
#     print("document is chunker")
#
#     print(dumps(document_with_chunks.to_dict(), indent=2, ensure_ascii=False, default=str))
#     # print(dumps(cleaned_document.to_dict(), indent=2, ensure_ascii=False, default=str))
#     # print(dumps(document_with_section_metadata.to_dict(), indent=2, ensure_ascii=False, default=str))
