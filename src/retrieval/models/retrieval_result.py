from dataclasses import dataclass

from src.retrieval.models.query import Query
from src.retrieval.models.retrieved_chunk import RetrievedChunk


@dataclass
class RetrievalResult:
    query: Query
    chunks: list[RetrievedChunk]
    context: str