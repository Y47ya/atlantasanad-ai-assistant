from src.ingestion.metadata.chunk_metadata_generator import ChunkMetadataGenerator
from src.ingestion.metadata.semantic_metadata_generator import SemanticMetadataGenerator
from src.ingestion.models.document import Document


class ChunkMetadataPipeline:

    def __init__(self, generator: SemanticMetadataGenerator, prompt: str):
        self.generator = generator
        self.prompt = prompt

    def process(self, document: Document) -> Document:

        for chunk in document.chunks:

            semantic = self.generator.generate(
                title=chunk.section.title,
                content=chunk.text,
                prompt=self.prompt
            )

            chunk.metadata.semantic = semantic

        return document