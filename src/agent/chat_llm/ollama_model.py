from typing import Any, Sequence

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.runnables import Runnable
from langchain_core.tools import BaseTool
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_ollama import ChatOllama


class OllamaChatModel(BaseChatModel):

    def __init__(
        self,
        model: str,
        temperature: float,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)

        self._model = ChatOllama(
            model=model,
            temperature=temperature,
        )

    @property
    def _llm_type(self) -> str:
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