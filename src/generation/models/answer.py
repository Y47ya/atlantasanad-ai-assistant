from dataclasses import dataclass

from src.retrieval.models.retrieval_result import RetrievalResult


@dataclass
class Answer:
    question: str
    answer: str

    retrieved_chunks: RetrievalResult