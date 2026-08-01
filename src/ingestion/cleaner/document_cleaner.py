import re

from src.ingestion.models.document import Document
from src.ingestion.models.section import ContentType


class DocumentCleaner:

    def clean_text(self, text: str) -> str:
        if not text:
            return ""

        text = re.sub(r"\s+", " ", text)

        text = re.sub(r"\s+([.,;:!?])", r"\1", text)

        text = re.sub(r"\s*'\s*", "'", text)

        return text.strip()

    def clean(self, document: Document) -> Document:

        for section in document.sections:

            cleaned_blocks = []

            for block in section.content:

                block.content = self.clean_text(block.content)

                if not block.content:
                    continue

                if (
                    cleaned_blocks
                    and block.type == ContentType.LIST_ITEM
                    and cleaned_blocks[-1].type == ContentType.LIST_ITEM
                    and cleaned_blocks[-1].content == block.content
                ):
                    continue

                cleaned_blocks.append(block)

            section.content = cleaned_blocks

        return document


