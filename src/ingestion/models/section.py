from dataclasses import field
from dataclasses import dataclass
from enum import Enum
from src.ingestion.models.section_metadata import SectionMetadata


class ContentType(Enum):
    TEXT = "text"
    LIST_ITEM = "list_item"
    TABLE = "table"


@dataclass
class ContentBlock:
    type: ContentType
    content: str


@dataclass
class Section:
    title: str
    page: int
    content: list[ContentBlock] = field(default_factory=list)
    metadata: SectionMetadata = field(default_factory=SectionMetadata)


    def get_section_content(self):
        return "\n".join(
                block.content
                for block in self.content
            )

