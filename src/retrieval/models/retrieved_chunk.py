from dataclasses import dataclass


@dataclass
class RetrievedChunk:
    score: float

    document_id: str
    chunk_id: str
    chunk_index: int

    text: str

    file_name: str
    page: int
    section_title: str

    section_summary: str | None
    section_keywords: list[str]

    chunk_summary: str | None
    chunk_keywords: list[str]

    rerank_score: float | None = None