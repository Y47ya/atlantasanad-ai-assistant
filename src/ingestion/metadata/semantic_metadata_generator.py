import json
from src.ingestion.models.semantic_metadata import SemanticMetadata
from src.llm.base_llm import BaseLLM
import json
import re


def extract_json(text: str) -> dict:
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError(f"No JSON found:\n{text}")

    return json.loads(match.group())


class SemanticMetadataGenerator:

    def __init__(self, llm: BaseLLM):
        self.llm = llm

    def generate(
        self,
        prompt: str,
        **kwargs,
    ) -> SemanticMetadata:

        formatted_prompt = prompt.format(**kwargs)

        MAX_RETRIES = 3

        for _ in range(MAX_RETRIES):

            response = self.llm.generate(formatted_prompt)

            try:
                data = extract_json(response)
                break

            except Exception:
                continue

        else:
            raise ValueError(response)

        return SemanticMetadata(
            display_title=data.get("display_title"),
            summary=data.get("summary", "").strip(),
            keywords=data.get("keywords", []),
            generation=self.llm.generation_info(),
        )