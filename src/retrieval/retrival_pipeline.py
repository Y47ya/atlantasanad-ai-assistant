from src.retrieval.context.base_context_builder import BaseContextBuilder
from src.retrieval.embeding.query_embedding_pipeline import QueryEmbeddingPipeline
from src.retrieval.models.query import Query
from src.retrieval.models.retrieval_result import RetrievalResult
from src.retrieval.reranker.base_reranker import BaseReranker
from src.retrieval.retreiver.base_retreiver import BaseRetriever


class RetrievalPipeline:

    def __init__(
        self,
        embedding_pipeline: QueryEmbeddingPipeline,
        retriever: BaseRetriever,
        reranker: BaseReranker,
        context_builder: BaseContextBuilder,
    ):
        self.embedding_pipeline = embedding_pipeline
        self.retriever = retriever
        self.reranker = reranker
        self.context_builder = context_builder

    def process(
        self,
        question: str,
    ) -> RetrievalResult:

        query = Query(text=question)

        query = self.embedding_pipeline.process(query)

        chunks = self.retriever.retrieve(
            query_vector=query.embedding,
        )

        chunks = self.reranker.rerank(
            query=query.text,
            chunks=chunks,
        )

        context = self.context_builder.build(chunks)

        return RetrievalResult(
            query=query,
            chunks=chunks,
            context=context,
        )