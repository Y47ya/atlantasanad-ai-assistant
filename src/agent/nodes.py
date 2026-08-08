from src.agent.agent import Agent
from src.agent.state import AgentState


def agent_node(
    state: AgentState,
    agent: Agent,
) -> dict:

    response = agent.invoke(state["messages"])

    print("=" * 50)
    print("Tool calls:")
    print(response.tool_calls)
    print("=" * 50)

    return {
        "messages": [response],
    }