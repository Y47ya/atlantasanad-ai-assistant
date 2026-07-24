from src.generation.prompt_builder.base_prompt_builder import BasePromptBuilder
from src.retrieval.models.retrieval_result import RetrievalResult


class RagPromptBuilder(BasePromptBuilder):

    def __init__(self, template: str):
        self.template = template

    def build(
        self,
        retrieval: RetrievalResult,
    ) -> str:

        return self.template.format(
            question=retrieval.query.text,
            context=retrieval.context,
        )