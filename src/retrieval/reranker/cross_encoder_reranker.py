from sentence_transformers import CrossEncoder

from src.retrieval.models.retrieved_chunk import RetrievedChunk
from src.retrieval.reranker.base_reranker import BaseReranker


class CrossEncoderReranker(BaseReranker):

    def __init__(
        self,
        model_name: str,
        top_k: int,
    ):
        self.model = CrossEncoder(
            model_name,
            trust_remote_code=True,
        )

        self.top_k = top_k

    def rerank(
        self,
        query: str,
        chunks: list[RetrievedChunk],
    ) -> list[RetrievedChunk]:

        if not chunks:
            return []

        pairs = [
            (query, chunk.text)
            for chunk in chunks
        ]

        scores = self.model.predict(pairs)

        for chunk, score in zip(chunks, scores):
            chunk.rerank_score = float(score)

        chunks.sort(
            key=lambda c: c.rerank_score,
            reverse=True,
        )

        return chunks[: self.top_k]