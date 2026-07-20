from sentence_transformers import SentenceTransformer

from src.ingestion.embeding.base_embeding import BaseEmbedding


class HuggingFaceEmbedding(BaseEmbedding):

    def __init__(self, model_name: str):
        self.model = SentenceTransformer(
            model_name,
            trust_remote_code=True,
        )
        self._model_name = model_name

    def embed(self, text: str) -> list[float]:
        return self.model.encode(
            text,
            normalize_embeddings=True,
        ).tolist()

    def provider(self) -> str:
        return "huggingface"

    def model_name(self) -> str:
        return self._model_name