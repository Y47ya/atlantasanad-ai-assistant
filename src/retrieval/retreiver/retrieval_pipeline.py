from qdrant_client.http.models import Query

from src.retrieval.context.base_context_builder import BaseContextBuilder
from src.retrieval.models.retrieval_result import RetrievalResult
from src.retrieval.query.query_embedding_pipeline import QueryEmbeddingPipeline
from src.retrieval.reranker.base_reranker import BaseReranker
from src.retrieval.retreiver.base_retreiver import BaseRetriever


class RetrievalPipeline:

    def __init__(
        self,
        query_embedding_pipeline: QueryEmbeddingPipeline,
        retriever: BaseRetriever,
        reranker: BaseReranker,
        context_builder: BaseContextBuilder
    ):
        self.query_embedding_pipeline = query_embedding_pipeline
        self.retriever = retriever
        self.reranker = reranker,
        self.context_builder = context_builder

    def process(
            self,
            text: str,
            top_k: int = 5,
    ) -> RetrievalResult:

        query = Query(text=text)
        query = self.query_embedding_pipeline.process(query)

        chunks = self.retriever.retrieve(
            query_vector=query.embedding or [],
            top_k=top_k,
        )

        chunks = self.reranker.rerank(
            query=query.text,
            chunks=chunks,
        )

        context = self.context_builder.build(chunks)

        return RetrievalResult(
            query=query,
            chunks=chunks,
            context=context
        )