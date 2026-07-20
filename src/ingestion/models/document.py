from dataclasses import dataclass, field, asdict

from src.ingestion.models.chunk import Chunk
from src.ingestion.models.section import Section


@dataclass
class Document:
    id: str
    title:str
    file_name: str
    pages_count: int = 0
    sections: list[Section] = field(default_factory=list)
    chunks: list[Chunk] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)
