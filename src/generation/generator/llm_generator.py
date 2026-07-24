from src.generation.generator.base_generator import BaseGenerator
from src.generation.models.answer import Answer
from src.generation.prompt_builder.base_prompt_builder import BasePromptBuilder
from src.llm.base_llm import BaseLLM
from src.retrieval.models.retrieval_result import RetrievalResult


class LLMGenerator(BaseGenerator):

    def __init__(
        self,
        llm: BaseLLM,
        prompt_builder: BasePromptBuilder,
    ):
        self.llm = llm
        self.prompt_builder = prompt_builder

    def generate(
        self,
        retrieval: RetrievalResult,
    ) -> Answer:

        prompt = self.prompt_builder.build(retrieval)

        response = self.llm.generate(prompt)

        return Answer(
            question=retrieval.query.text,
            answer=response,
            retrieved_chunks=retrieval,
        )