from src.retrieval.context.base_context_builder import BaseContextBuilder
from src.retrieval.embeding.query_embedding_pipeline import QueryEmbeddingPipeline
from src.retrieval.models.query import Query
from src.retrieval.models.retrieval_result import RetrievalResult
from src.retrieval.reranker.base_reranker import BaseReranker
from src.retrieval.retreiver.base_retreiver import BaseRetriever


class RetrievalPipeline:

    def __init__(
        self,
        query_embedding_pipeline: QueryEmbeddingPipeline,
        retriever: BaseRetriever,
        reranker: BaseReranker,
        context_builder: BaseContextBuilder,
    ):
        self.query_embedding_pipeline = query_embedding_pipeline
        self.retriever = retriever
        self.reranker = reranker
        self.context_builder = context_builder

    def process(
        self,
        question: str,
    ) -> RetrievalResult:

        query = Query(question)

        query = self.query_embedding_pipeline.process(query)

        chunks = self.retriever.retrieve(query.embedding)

        chunks = self.reranker.rerank(query.text, chunks)

        print("=== Retriever ===\n")

        for c in chunks:
            print(c.score, c.file_name, c.page)
            print(c.text[:120])
        print("\n")
        print("=" * 10)

        chunks = self.reranker.rerank(
            query.text,
            chunks,
        )

        print("=== Reranker ===\n")

        for c in chunks:
            print(c.rerank_score, c.file_name, c.page)
            print(c.text[:120])
        print("\n")
        print("=" * 10)

        context = self.context_builder.build(chunks)

        return RetrievalResult(
            query=query,
            chunks=chunks,
            context=context,
        )