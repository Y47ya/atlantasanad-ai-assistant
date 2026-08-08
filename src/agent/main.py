from pathlib import Path

from langchain_core.messages import HumanMessage
from src.agent.chat_llm.agent_llm import llm
from src.agent.agent import Agent
from src.agent.graph import AgentGraph
from src.agent.router_prompt import prompt
from src.agent.tools.document.pdf_extractor import PDFExtractor
from src.agent.tools.edition_devis_tool import EditionDevisTool
from src.agent.tools.rag_tool import RAGTool
from src.agent.tools.simulation_tool import SimulationTool
from src.api.api_service import APIService
from src.api.client.mock_api_client import MockAPIClient
from src.config.settings import PROJECT_ROOT, EMBEDDING_MODEL, QDRANT_HOST, QDRANT_PORT, QDRANT_COLLECTION_NAME, \
    RETRIEVER_TOP_K, RERANKER_MODEL, RERANKER_TOP_K
from src.embeding.hugging_face_embeding import HuggingFaceEmbedding
from src.retrieval.context.default_context_builder import DefaultContextBuilder
from src.retrieval.embeding.query_embedding_pipeline import QueryEmbeddingPipeline
from src.retrieval.reranker.cross_encoder_reranker import CrossEncoderReranker
from src.retrieval.retreiver.qdrant_retreiver import QdrantRetriever
from src.retrieval.retreiver.retrival_pipeline import RetrievalPipeline
from src.tools import create_qdrant_client


def build_graph():

    qdrant_client = create_qdrant_client(
        host=QDRANT_HOST,
        port=QDRANT_PORT,
    )

    client = MockAPIClient(
        Path(
            PROJECT_ROOT / "data/payloads_exemple"
        )
    )

    api_service = APIService(client)

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

    pdf_extractor = PDFExtractor()

    simulation_tool = SimulationTool(api_service)
    edition_devis_tool = EditionDevisTool(
        pdf_extractor=pdf_extractor,
        api_service=api_service
    )
    rag_tool = RAGTool(retrieval_pipeline)

    tools = [
        simulation_tool,
        edition_devis_tool,
        rag_tool
    ]

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

    while True:

        question = input("Question(q to quit) : ")

        if question.lower() == "q":
            break

        messages.append(
            HumanMessage(content=question)
        )

        state = graph.invoke(
            {
                "messages": messages,
            }
        )

        messages = state["messages"]

        print(
            "Réponse", state["messages"][-1].content, "\n\n"
        )
        print("=" * 50)




if __name__ == "__main__":
    main()