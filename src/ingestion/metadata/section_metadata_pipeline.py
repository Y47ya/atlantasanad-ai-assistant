from json import dumps
from pathlib import Path

from rich import prompt

from src.config.settings import PROJECT_ROOT, OLLAMA_MODEL, OLLAMA_PROVIDER, OLLAMA_HOST, OLLAMA_PULL_IF_MISSING, \
    OLLAMA_TEMPERATURE
from src.ingestion.cleaner.document_cleaner import DocumentCleaner
from src.ingestion.metadata.semantic_metadata_generator import SemanticMetadataGenerator
from src.ingestion.models import section_metadata
from src.ingestion.models.document import Document
from src.ingestion.models.section_metadata import SectionMetadata
from src.ingestion.models.semantic_metadata import SemanticMetadata
from src.ingestion.parser.docling_converter import DoclingAdapter
from src.llm.ollama import OllamaLLM


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






