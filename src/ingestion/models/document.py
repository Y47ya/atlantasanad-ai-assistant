from dataclasses import dataclass, field, asdict, is_dataclass
from datetime import datetime
from enum import Enum
from json import dump, dumps, load
from pathlib import Path

from dacite import Config, from_dict

from src.ingestion.models.chunk import Chunk
from src.ingestion.models.section import Section, ContentType
from src.ingestion.tools import serialize, to_json, parse_content_type


@dataclass
class Document:
    id: str
    title: str
    file_name: str
    pages_count: int = 0

    sections: list[Section] = field(default_factory=list)
    chunks: list[Chunk] = field(default_factory=list)

    def to_dict(self) -> dict:
        return to_json(self)

    def print_document(self) -> None:
        print(
            dumps(
                self.to_dict(),
                indent=4,
                ensure_ascii=False
            )
        )

    def save_json(self, path: str | Path) -> None:
        with open(path, "w", encoding="utf-8") as f:
            dump(
                self.to_dict(),
                f,
                indent=4,
                ensure_ascii=False
            )

    @classmethod
    def load_json(cls, path: str | Path) -> "Document":
        with open(path, "r", encoding="utf-8") as f:
            data = load(f)

        return from_dict(
            data_class=cls,
            data=data,
            config=Config(
                type_hooks={
                    datetime: datetime.fromisoformat,
                    ContentType: parse_content_type,
                }
            ),
        )