from pathlib import Path

from pympler import asizeof
from langchain_core.messages import HumanMessage

from src.agent.agent.agent import Agent
from src.agent.graph import AgentGraph
from src.agent.tools.edition_devis_tool import EditionDevisTool
from src.agent.tools.rag_tool import RAGTool
from src.agent.tools.simulation_tool import SimulationTool
from src.agent.chat_llm.ollama_chat_model import OllamaChatModel
from src.agent.router_prompt import prompt

from src.api.api_service import APIService
from src.api.client.mock_api_client import MockAPIClient

from src.config.settings import (
    PROJECT_ROOT,
    EMBEDDING_MODEL,
    QDRANT_HOST,
    QDRANT_PORT,
    QDRANT_COLLECTION_NAME,
    RETRIEVER_TOP_K,
    RERANKER_MODEL,
    RERANKER_TOP_K,
    OLLAMA_MODEL,
    OLLAMA_TEMPERATURE,
    PARSER_USAGE,
)


from src.embeding.hugging_face_embeding import HuggingFaceEmbedding

from src.retrieval.context.default_context_builder import (
    DefaultContextBuilder,
)
from src.retrieval.embeding.query_embedding_pipeline import (
    QueryEmbeddingPipeline,
)
from src.retrieval.reranker.cross_encoder_reranker import (
    CrossEncoderReranker,
)
from src.retrieval.retreiver.qdrant_retreiver import (
    QdrantRetriever,
)
from src.retrieval.retreiver.retrival_pipeline import (
    RetrievalPipeline,
)

from src.tools import create_qdrant_client


def build_graph():

    # ==========================================================
    # API
    # ==========================================================

    client = MockAPIClient(
        Path(PROJECT_ROOT / "data/payloads_exemple"),
        use_parser=PARSER_USAGE,
    )

    api_service = APIService(client)

    qdrant_client = create_qdrant_client(
        host=QDRANT_HOST,
        port=QDRANT_PORT,
    )

    embedding_model = HuggingFaceEmbedding(
        model_name=EMBEDDING_MODEL,
    )

    embedding_pipeline = QueryEmbeddingPipeline(
        embedding_model=embedding_model,
    )

    retriever = QdrantRetriever(
        client=qdrant_client,
        collection_name=QDRANT_COLLECTION_NAME,
        top_k=RETRIEVER_TOP_K,
    )

    reranker = CrossEncoderReranker(
        model_name=RERANKER_MODEL,
        top_k=RERANKER_TOP_K,
    )

    context_builder = DefaultContextBuilder()

    retrieval_pipeline = RetrievalPipeline(
        query_embedding_pipeline=embedding_pipeline,
        retriever=retriever,
        reranker=reranker,
        context_builder=context_builder,
    )

    # ==========================================================
    # TOOLS
    # ==========================================================

    simulation_tool = SimulationTool(
        api_service=api_service,
    )

    edition_devis_tool = EditionDevisTool(
        api_service=api_service,
    )

    rag_tool = RAGTool(
        retrieval_pipeline=retrieval_pipeline,
    )

    tools = [
        simulation_tool,
        edition_devis_tool,
        rag_tool,
    ]

    llm = OllamaChatModel(
        model=OLLAMA_MODEL,
        temperature=OLLAMA_TEMPERATURE,
    )

    agent = Agent(
        llm=llm,
        prompt=prompt,
        tools=tools,
    )

    graph = AgentGraph(
        agent=agent,
        tools=tools,
    ).build()

    return graph


def main():

    graph = build_graph()

    messages = []

    first_message = False

    while True:

        question = input("Question(q pour quitter) : ")

        if question.lower() == "q":
            break

        messages.append(
            HumanMessage(content=question)
        )

        if first_message:

            print(
                "\nSalut ! Je suis votre assistant spécialisé "
                "dans le domaine des assurances.\n"
                "Comment puis-je vous aider ?\n"
            )

            first_message = False

        else:

            state = graph.invoke(
                {
                    "messages": messages,
                }
            )

            messages = state["messages"]

            size_bytes = asizeof.asizeof(messages)

            size_mb = size_bytes / (1024 * 1024)

            print(
                f"Size of messages: "
                f"{size_bytes:,} bytes ({size_mb:.4f} MB)"
            )

            print(
                "Réponse :",
                messages[-1].content,
                "\n\n",
            )

            print("=" * 50)


if __name__ == "__main__":
    main()