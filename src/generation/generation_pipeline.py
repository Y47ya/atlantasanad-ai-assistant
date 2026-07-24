from src.generation.generator.base_generator import BaseGenerator
from src.generation.models.answer import Answer
from src.retrieval.models.retrieval_result import RetrievalResult


class GenerationPipeline:

    def __init__(
        self,
        generator: BaseGenerator,
    ):
        self.generator = generator

    def process(
        self,
        retrieval: RetrievalResult,
    ) -> Answer:

        return self.generator.generate(retrieval)