from pathlib import Path

from qdrant_client.local import json_path_parser

from src.config.settings import PROJECT_ROOT
from src.ingestion.metadata.context.context_builder import ContextWindow
from src.ingestion.metadata.semantic_metadata_generator import SemanticMetadataGenerator
from src.ingestion.models.document import Document
from src.ingestion.models.section_metadata import SectionMetadata
from src.ingestion.models.semantic_metadata import SemanticMetadata


class SectionMetadataPipeline:

    def __init__(self, generator: SemanticMetadataGenerator, prompt: str, context_builder: ContextWindow):
        self.generator = generator
        self.prompt = prompt
        self.context_builder = context_builder

    def process(
        self,
        document: Document,
    ) -> Document:

        file_name = document.file_name
        json_path = Path(PROJECT_ROOT / "data" / "processed_data" / "section_metadata_lvl" / f"{file_name}.json")

        if json_path.exists():
            print(f"Loading section metadata level document: {json_path}")
            document = Document.load_json(json_path)
            return document

        for index, section in enumerate(document.sections):
            print(f"Generating metadata for section {index}")

            context = self.context_builder.build(
                document=document,
                section_index=index,
            )

            semantic = self.generator.generate(
                content=context,
                prompt=self.prompt,
            )

            section.metadata = SectionMetadata(
                semantic=SemanticMetadata(
                    summary=semantic.summary,
                    keywords=semantic.keywords,
                    generation=self.generator.llm.generation_info(),
                )
            )

        document.save_json(json_path)

        return document






