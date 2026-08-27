from typing import Type, Any
from pydantic import BaseModel
from langchain_core.tools import BaseTool

from src.agent.tools.input_shemas.rag_input import RAGInput
from src.retrieval.retreiver.retrival_pipeline import RetrievalPipeline
from src.agent.tools_informations import TOOLS_INFORMATIONS


RAG_INFOS = TOOLS_INFORMATIONS.get("rag")


class RAGTool(BaseTool):
    name: str = RAG_INFOS.get("name")
    description: str = RAG_INFOS.get("description")
    args_schema: Type[BaseModel] = RAGInput
    retrieval_pipeline: RetrievalPipeline

    def __init__(
            self,
            retrieval_pipeline: RetrievalPipeline,
            **kwargs,
    ):
        super().__init__(
            retrieval_pipeline=retrieval_pipeline,
            **kwargs,
        )
    def _run(
        self,
        question: str,
    ) -> str:

        result = self.retrieval_pipeline.retrieve_context(question)

        return result