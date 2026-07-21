import json
from src.ingestion.models.semantic_metadata import SemanticMetadata
from src.ingestion.llms.base_llm import BaseLLM


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