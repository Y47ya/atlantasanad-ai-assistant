from pathlib import Path

from src.config.settings import PROJECT_ROOT
from src.ingestion.metadata.context.chunk_context_builder import ChunkContextBuilder
from src.ingestion.metadata.semantic_metadata_generator import SemanticMetadataGenerator
from src.ingestion.models.document import Document


class ChunkMetadataPipeline:

    def __init__(
        self,
        generator: SemanticMetadataGenerator,
        context_builder: ChunkContextBuilder,
        prompt: str,
    ):
        self.generator = generator
        self.context_builder = context_builder
        self.prompt = prompt

    def process(self, document: Document) -> Document:

        file_name = document.file_name
        json_path = Path(PROJECT_ROOT / "data" / "processed_data" / "chunk_metadata_lvl" / f"{file_name}.json")

        if json_path.exists():
            print(f"Loading chunk metadata level document: {json_path.stem}")
            document = Document.load_json(json_path)
            return document

        for chunk in document.chunks:
            variables = self.context_builder.build(
                section=chunk.section,
                chunk=chunk,
            )

            chunk.metadata.semantic = self.generator.generate(
                prompt=self.prompt,
                **variables,
            )

        document.save_json(json_path)

        return document