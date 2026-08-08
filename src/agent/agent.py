from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from src.agent.tools.simulation_tool import SimulationTool
from src.api.api_service import APIService
from src.api.client.mock_api_client import MockAPIClient


class Agent:

    def __init__(
        self,
        llm: BaseChatModel,
        tools: list,
        prompt: ChatPromptTemplate,
    ):

        self.llm = llm.bind_tools(tools)

        self.prompt = prompt

        self.chain = (
                self.prompt
                | self.llm
        )

    def invoke(
        self,
        messages: list[BaseMessage],
    ):
        return self.chain.invoke(
            {
                "messages": messages,
            }
        )


