from src.config.settings import *

from src.tools import create_qdrant_client

from src.embeding.hugging_face_embeding import HuggingFaceEmbedding

from src.llm.ollama import OllamaLLM
from src.llm.prompts import RAG_PROMPT

from src.retrieval.embeding.query_embedding_pipeline import QueryEmbeddingPipeline
from src.retrieval.retreiver.qdrant_retreiver import QdrantRetriever
from src.retrieval.reranker.cross_encoder_reranker import CrossEncoderReranker
from src.retrieval.context.default_context_builder import DefaultContextBuilder
from src.retrieval.retrival_pipeline import RetrievalPipeline

from src.generation.prompt_builder.rag_prompt_builder import RagPromptBuilder
from src.generation.generator.llm_generator import LLMGenerator
from src.generation.generation_pipeline import GenerationPipeline


class RagAssistant:

    def __init__(
        self,
        retrieval_pipeline: RetrievalPipeline,
        generation_pipeline: GenerationPipeline,
    ):
        self.retrieval_pipeline = retrieval_pipeline
        self.generation_pipeline = generation_pipeline

    def ask(self, question: str):

        retrieval_result = self.retrieval_pipeline.process(question)

        answer = self.generation_pipeline.process(
            retrieval_result
        )

        return answer


def build_assistant() -> RagAssistant:

    qdrant_client = create_qdrant_client(
        host=QDRANT_HOST,
        port=QDRANT_PORT,
    )

    llm = OllamaLLM(
        model=OLLAMA_MODEL,
        provider=OLLAMA_PROVIDER,
        host=OLLAMA_HOST,
        pull_if_missing=OLLAMA_PULL_IF_MISSING,
        temperature=OLLAMA_TEMPERATURE,
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
        embedding_pipeline=embedding_pipeline,
        retriever=retriever,
        reranker=reranker,
        context_builder=context_builder,
    )

    prompt_builder = RagPromptBuilder(
        template=RAG_PROMPT,
    )

    generator = LLMGenerator(
        llm=llm,
        prompt_builder=prompt_builder,
    )

    generation_pipeline = GenerationPipeline(
        generator=generator,
    )

    return RagAssistant(
        retrieval_pipeline=retrieval_pipeline,
        generation_pipeline=generation_pipeline,
    )


def main():

    assistant = build_assistant()

    questions_rag = [
        "Dans quelle rubrique s'inscrit l'offre d'assurance présentée dans ce document ?",
        "Quelle est l'unique garantie obligatoire mentionnée pour l'offre Auto + Flotte salariés ?",
        "Quels sont les 3 arguments avancés dans la section « Pourquoi choisir Auto + Flotte salariés » ?",
        "L'assurance couvre-t-elle les accessoires et aménagements professionnels du véhicule ? Si oui, dans quelle catégorie de garantie cela se trouve-t-il ?",
        "Quels sont les différents types de vol spécifiquement listés parmi les garanties innovantes ?",
        "Dans quelle catégorie de garantie se situe le « Bris de glace » par rapport au « Bris de miroir, des rétroviseurs et des optiques » ?",
        "Quelle est la différence de classification entre la protection des personnes transportées (passagers) et celle de la personne qui conduit ?",
        "Un salarié a commis une erreur en faisant le plein de son véhicule de fonction (erreur de carburant). Ce cas est-il prévu par le contrat ?",
        "À qui s'adresse principalement cette offre et quel est l'objectif prioritaire mis en avant pour l'entreprise souscriptrice ?",
        "La garantie « Assistance panne 0 km » ou le prêt d'un véhicule de remplacement sont-ils inclus dans ce document ?"
    ]

    for question in questions_rag:
        answer = assistant.ask(question)

        print("\n===================== QUESTION =====================")
        print(answer.question)

        print("\n====================== ANSWER ======================")
        print(answer.answer)


if __name__ == "__main__":
    main()