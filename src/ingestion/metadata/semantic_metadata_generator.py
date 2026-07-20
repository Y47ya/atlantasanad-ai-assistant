import json
from src.ingestion.models.semantic_metadata import SemanticMetadata
from src.ingestion.tools import get_llm_generation_info
from src.llm.base_llm import BaseLLM
from src.llm.prompts import SEMANTIC_METADATA_PROMPT


class SemanticMetadataGenerator:

    def __init__(self, llm: BaseLLM):
        self.llm = llm

    def generate(self, title: str, content: str, prompt: str) -> SemanticMetadata:

        prompt = prompt.format(
            title=title,
            content=content
        )

        response = self.llm.generate(prompt)

        data = json.loads(response)

        summary = data.get("summary", "").strip()
        keywords = data.get("keywords", [])

        return SemanticMetadata(
            summary=summary,
            keywords=keywords,
            generation=self.llm.generation_info()
        )