from src.retrieval.context.base_context_builder import BaseContextBuilder
from src.retrieval.models.retrieved_chunk import RetrievedChunk


class DefaultContextBuilder(BaseContextBuilder):

    def build(
        self,
        chunks: list[RetrievedChunk],
    ) -> str:

        contexts = []

        for i, chunk in enumerate(chunks, start=1):

            contexts.append(
                f"""
                === Passage {i} ===
                Document : {chunk.file_name}
                Page : {chunk.page}
                {chunk.text.strip()}
                """.strip()
            )

        return "\n\n".join(contexts)

