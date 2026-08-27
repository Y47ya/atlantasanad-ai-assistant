from typing import Annotated

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

from src.agent.tools.output_schemas.simulation_result import SimulationResult


class AgentState(TypedDict):

    messages: Annotated[list[AnyMessage], add_messages]
    # simulation: SimulationResult | None