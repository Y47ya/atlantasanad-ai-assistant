from typing import Type, Any
from pydantic import BaseModel
from langchain_core.tools import BaseTool

from src.agent.router_prompt import RAG_TOOLS_DESCRIPTION
from src.agent.tools.input_schemas.rag_input import RAGInput
from src.retrieval.retreiver.retrival_pipeline import RetrievalPipeline


class RAGTool(BaseTool):
    name: str = "rag"
    description: str = (RAG_TOOLS_DESCRIPTION)
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