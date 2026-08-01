from src.ingestion.models.chunk import Chunk
from src.ingestion.models.section import Section


class ChunkContextBuilder:

    def build(
        self,
        section: Section,
        chunk: Chunk,
    ) -> dict[str, str]:

        semantic = section.metadata.semantic

        return {
            "section_metadata": f"""
Title:
{semantic.display_title}

Summary:
{semantic.summary}

Keywords:
{", ".join(semantic.keywords)}
""".strip(),

            "content": chunk.text,
        }