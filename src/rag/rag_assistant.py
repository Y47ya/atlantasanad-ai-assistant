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

    # for question in questions_rag:
    #     answer = assistant.ask(question)
    #
    #     print("\n===================== QUESTION =====================")
    #     print(answer.question)
    #
    #     print("\n====================== ANSWER ======================")
    #     print(answer.answer)

    test_questions = [
        {
            "id": 1,
            "niveau": "Facile",
            "question": "Dans quel délai l'Assuré doit-il déclarer un sinistre à l'Assureur (hors vol) ?",
            "teste": "Lookup simple, un seul article",
            "reponse_attendue": "5 jours (Article 40)",
        },
        {
            "id": 2,
            "niveau": "Facile",
            "question": "Que signifie le terme \"Déconfiture\" dans ce contrat ?",
            "teste": "Glossaire - section mélangée avec le Chapitre 6 dans le parse",
            "reponse_attendue": "Situation d'un débiteur hors d'état de payer ses créanciers",
        },
        {
            "id": 3,
            "niveau": "Facile-Moyen",
            "question": "Quel est le délai de déclaration spécifique pour un sinistre Vol ?",
            "teste": "Distinction règle générale (5j) vs exception (Vol) - piège de confusion",
            "reponse_attendue": "48 heures",
        },
        {
            "id": 4,
            "niveau": "Moyen",
            "question": "Les garanties Dommages Tous Accidents (DTA) et Dommages Collision sont-elles cumulables ?",
            "teste": "Réponse négative explicite répétée à 2 endroits (Art. 6 et Art. 7)",
            "reponse_attendue": "Non, non cumulables",
        },
        {
            "id": 5,
            "niveau": "Moyen",
            "question": "La garantie Vol couvre-t-elle le vol du véhicule si les clés ont été laissées à l'intérieur ?",
            "teste": "Exclusion précise noyée dans une longue liste d'exclusions (Art. 8)",
            "reponse_attendue": "Non, explicitement exclu",
        },
        {
            "id": 6,
            "niveau": "Moyen-Difficile",
            "question": "Quel est le taux de vétusté sur les pièces de carrosserie neuves, pour un véhicule \"Personne Physique\", à l'année 3 ?",
            "teste": "Lecture d'un tableau correctement extrait (Annexe III) - cas de contrôle 'table qui marche'",
            "reponse_attendue": "10%",
        },
        {
            "id": 7,
            "niveau": "Difficile",
            "question": "Quel est le taux d'abattement de la Valeur Vénale pour un véhicule de Location, Puissance Fiscale > 12 CV, motorisation Diesel, à la 1ère année ?",
            "teste": "Lecture d'un tableau où une ligne est manquante dans le JSON - test direct de la perte de données",
            "reponse_attendue": "32% (si le RAG répond autre chose ou 'information non disponible', ça confirme le trou de données)",
        },
        {
            "id": 8,
            "niveau": "Difficile",
            "question": "Que couvre l'Article 23 de ce contrat ?",
            "teste": "Piège de numérotation : 'Article 23' existe deux fois (Protection des Passagers dans le corps, Prescription dans l'Annexe I RC)",
            "reponse_attendue": "Doit clarifier qu'il y a deux Article 23 différents et donner les deux réponses, pas une seule au hasard",
        },
        {
            "id": 9,
            "niveau": "Difficile",
            "question": "Un assuré a souscrit la garantie DTA et la garantie Rachat de la Vétusté. En cas de sinistre partiel, comment l'indemnité est-elle calculée ?",
            "teste": "Raisonnement multi-articles (Art. 14 + Art. 43) sur des pages où l'ordre de lecture était scrambled",
            "reponse_attendue": "Indemnité calculée sur la base de la Valeur à Neuf (sans déduction de vétusté), plafonnée à la Valeur Vénale du véhicule au jour du sinistre",
        },
        {
            "id": 10,
            "niveau": "Expert",
            "question": "Un conducteur assuré a un capital de 40 000 DH au titre de la garantie Protection du Conducteur et un taux d'IPP de 20%. Quel est le montant de l'indemnité ?",
            "teste": "Calcul numérique + récupération de la formule dans un chunk où le texte était éclaté lettre par lettre",
            "reponse_attendue": "40 000 x 20% = 8 000 DH",
        },
    ]

    for question in test_questions:
        print("\n===================== QUESTION =====================")
        print(f"ID : {question.get('id')}")
        print(f"Niveau : {question.get('niveau')}")
        print(f"Question : {question.get('question')}")

        print("\n====================== ANSWER ======================")
        answer = assistant.ask(question.get("question"))
        print(f"Reponse RAG : {answer.answer}")
        # print(f"Reponse attendue : {question.get('reponse_attendue')}")

    # answer = assistant.ask(questions_rag[0])
    # print("\n===================== QUESTION =====================")
    # print(answer.question)
    # print("\n====================== ANSWER ======================")
    # print(answer.answer)



if __name__ == "__main__":
    main()