from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.ingestion.chunking.base_chunker import BaseChunker
from src.ingestion.models.chunk import Chunk
from src.ingestion.models.chunk_metadata import ChunkMetadata
from src.ingestion.models.section import Section
from src.ingestion.tools import generate_chunk_id


class RecursiveChunker(BaseChunker):

    def __init__(
        self,
        chunk_size: int,
        chunk_overlap: int,
        separators: list[str],
    ):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=separators,
        )

    def chunk(
        self,
        document_id: str,
        file_name: str,
        section: Section,
    ) -> list[Chunk]:

        split_chunks = self.splitter.split_text(
            section.get_section_content()
        )

        chunks: list[Chunk] = []

        for chunk_index, chunk_text in enumerate(split_chunks):

            chunk_id = generate_chunk_id(
                document_id=document_id,
                # section_index=section.index,
                chunk_index=chunk_index,
                text=chunk_text,
            )

            chunks.append(
                Chunk(
                    text=chunk_text,
                    section=section,
                    metadata=ChunkMetadata(
                        document_id=document_id,
                        file_name=file_name,
                        chunk_id=chunk_id,
                        chunk_index=chunk_index,
                    ),
                )
            )

        return chunks