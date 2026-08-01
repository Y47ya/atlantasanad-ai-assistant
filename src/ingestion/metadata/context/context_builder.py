from src.ingestion.metadata.context.base_context_builder import BaseContextBuilder
from src.ingestion.models.document import Document


class ContextWindow(BaseContextBuilder):

    def __init__(
        self,
        previous_sections: int = 1,
        next_sections: int = 1,
    ):
        self.previous_sections = previous_sections
        self.next_sections = next_sections

    def build(
        self,
        document: Document,
        section_index: int,
    ) -> str:

        sections = document.sections

        previous_context = self._build_previous_context(
            sections,
            section_index,
        )

        current_context = sections[section_index].get_section_content()

        next_context = self._build_next_context(
            sections,
            section_index,
        )

        return f"""
Contexte précédent :
{previous_context}

====================

Section courante :
{current_context}

====================

Contexte suivant :
{next_context}
""".strip()

    def _build_previous_context(
        self,
        sections,
        index,
    ) -> str:

        start = max(0, index - self.previous_sections)

        return "\n\n".join(
            section.get_section_content()
            for section in sections[start:index]
        )

    def _build_next_context(
        self,
        sections,
        index,
    ) -> str:

        end = min(
            len(sections),
            index + self.next_sections + 1,
        )

        return "\n\n".join(
            section.get_section_content()
            for section in sections[index + 1:end]
        )