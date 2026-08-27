from langgraph.graph import StateGraph
from langgraph.graph import START

from src.agent.agent.agent import Agent
from src.agent.nodes import agent_node
from src.agent.state import AgentState
from langgraph.prebuilt import ToolNode, tools_condition



class AgentGraph:

    def __init__(
        self,
        agent: Agent,
        tools: list,
    ):
        self.agent = agent
        self.tools = tools

    def build(self):

        builder = StateGraph(AgentState)

        builder.add_node(
            "agent",
            lambda state: agent_node(
                state,
                self.agent,
            ),
        )

        builder.add_node(
            "tools",
            ToolNode(self.tools),
        )

        builder.add_edge(
            START,
            "agent",
        )

        builder.add_conditional_edges(
            "agent",
            tools_condition,
        )

        builder.add_edge(
            "tools",
            "agent",
        )

        return builder.compile()