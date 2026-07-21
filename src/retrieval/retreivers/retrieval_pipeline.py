from src.embeding.base_embeding import BaseEmbedding
from src.retrieval.models.retrieval_result import RetrievalResult
from src.retrieval.retreivers.base_retreiver import BaseRetriever


class RetrievalPipeline:

    def __init__(
        self,
        embedding_model: BaseEmbedding,
        retriever: BaseRetriever,
    ):
        self.embedding_model = embedding_model
        self.retriever = retriever

    def process(
            self,
            query: str,
            top_k: int = 5,
    ) -> list[RetrievalResult]:
        query_vector = self.embedding_model.embed(query)

        return self.retriever.retrieve(
            query_vector=query_vector,
            top_k=top_k,
        )