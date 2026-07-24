from src.embeding.base_embeding import BaseEmbedding
from src.retrieval.models.query import Query


class QueryEmbeddingPipeline:

    def __init__(self, embedding_model: BaseEmbedding):
        self.embedding_model = embedding_model

    def process(self, query: Query) -> Query:

        query.embedding = self.embedding_model.embed(query.text)

        return query