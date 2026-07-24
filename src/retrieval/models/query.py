from dataclasses import dataclass


@dataclass
class Query:
    text: str
    embedding: list[float] | None = None