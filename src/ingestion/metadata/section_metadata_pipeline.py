from src.ingestion.metadata.semantic_metadata_generator import SemanticMetadataGenerator
from src.ingestion.models.document import Document
from src.ingestion.models.section_metadata import SectionMetadata
from src.ingestion.models.semantic_metadata import SemanticMetadata


class SectionMetadataPipeline:

    def __init__(self, generator: SemanticMetadataGenerator, prompt: str):
        self.generator = generator
        self.prompt = prompt

    def process(self, document: Document) -> Document:

        for section in document.sections:

            content = section.get_section_content()

            print(f"Section content : \\n{content}")

            semantic = self.generator.generate(
                title=section.title,
                content=content,
                prompt=self.prompt
            )

            section.metadata = SectionMetadata(
                semantic=SemanticMetadata(
                    summary=semantic.summary,
                    keywords=semantic.keywords,
                    generation=self.generator.llm.generation_info()
                )
            )

        return document






