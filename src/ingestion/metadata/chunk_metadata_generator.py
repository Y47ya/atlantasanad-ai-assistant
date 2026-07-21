import json

from src.ingestion.models.semantic_metadata import SemanticMetadata
from src.ingestion.tools import get_llm_generation_info
from src.llms.base_llm import BaseLLM


class ChunkMetadataGenerator:

    def __init__(self, llm: BaseLLM):
        self.llm = llm

    def generate(
        self,
        title: str,
        content: str,
        prompt: str
    ) -> SemanticMetadata:

        prompt = prompt.format(
            title=title,
            content=content,
        )

        response = self.llm.generate(prompt)

        data = json.loads(response)

        return SemanticMetadata(
            summary=data["summary"],
            keywords=data["keywords"],
            generation=get_llm_generation_info(self.llm),
        )