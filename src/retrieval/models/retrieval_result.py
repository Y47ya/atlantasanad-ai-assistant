from dataclasses import dataclass


@dataclass
class RetrievalResult:
    score: float
    text: str
    payload: dict