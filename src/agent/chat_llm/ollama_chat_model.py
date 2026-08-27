from typing import Any, Sequence
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.runnables import Runnable
from langchain_core.tools import BaseTool
from langchain_ollama import ChatOllama

from src.llm.ollama import OllamaLLM


class OllamaChatModel(BaseChatModel):

    def __init__(
            self,
            model: str,
            provider: str = "ollama",
            host: str = "http://localhost:11434",
            pull_if_missing: bool = True,
            temperature: float = 0.0,
            **kwargs: Any,
    ):
        super().__init__(**kwargs)

        # Triggers ensure_model() check/pull without saving an unused attribute
        OllamaLLM(
            model=model,
            provider=provider,
            host=host,
            pull_if_missing=pull_if_missing,
            temperature=temperature,
        )

        # Main active model for generation
        self._model = ChatOllama(
            model=model,
            temperature=temperature,
        )

    def  _llm_type(self):
        return "ollama"

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: Any = None,
        **kwargs: Any,
    ) -> ChatResult:

        response = self._model.invoke(
            messages,
            stop=stop,
            **kwargs,
        )

        return ChatResult(
            generations=[
                ChatGeneration(
                    message=response,
                )
            ]
        )

    def bind_tools(
        self,
        tools: Sequence[dict | type | BaseTool | Any],
        *,
        tool_choice: str | dict | None = None,
        **kwargs: Any,
    ) -> Runnable:

        return self._model.bind_tools(
            tools,
            tool_choice=tool_choice,
            **kwargs,
        )