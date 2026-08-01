from src.retrieval.context.base_context_builder import BaseContextBuilder
from src.retrieval.models.query import Query
from src.retrieval.models.retrieval_result import RetrievalResult
from src.retrieval.models.retrieved_chunk import RetrievedChunk


class DefaultContextBuilder(BaseContextBuilder):

    def build(
        self,
        chunks: list[RetrievedChunk],
    ) -> str:

        parts = []

        for i, chunk in enumerate(chunks, start=1):

            parts.append(
                f"""
                    ==================== Source {i} ====================
                    
                    Document: {chunk.file_name}
                    Page: {chunk.page}
                    
                    Section Summary:
                    {chunk.section_summary}
                    
                    Section Keywords:
                    {", ".join(chunk.section_keywords)}
                    
                    Chunk Summary:
                    {chunk.chunk_summary}
                    
                    Chunk Keywords:
                    {", ".join(chunk.chunk_keywords)}
                    
                    Content:
                    {chunk.text}
                """
            )

        return "\n".join(parts)