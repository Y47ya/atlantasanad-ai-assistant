from src.ingestion.models.document import Document
from src.ingestion.storage.base_vector_store import BaseVectorStore


class QdrantPipeline:

    def __init__(self, store: BaseVectorStore):
        self.store = store

    def process(self, document: Document) -> Document:

        self.store.upsert(document.chunks)

        return document