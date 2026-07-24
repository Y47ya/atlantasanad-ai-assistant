from src.embeding.hugging_face_embeding import HuggingFaceEmbedding
from src.config.settings import EMBEDDING_MODEL, QDRANT_COLLECTION_NAME, QDRANT_HOST, QDRANT_PORT
from src.retrieval.retreiver.qdrant_retreiver import QdrantRetriever
from src.retrieval.retreiver.retrieval_pipeline import RetrievalPipeline
from src.tools import create_qdrant_client

embedding = HuggingFaceEmbedding(
    model_name=EMBEDDING_MODEL,
)

qdrant_client = create_qdrant_client(
        host=QDRANT_HOST,
        port=QDRANT_PORT
    )

retriever = QdrantRetriever(
    client=qdrant_client,
    collection_name=QDRANT_COLLECTION_NAME,
)

pipeline = RetrievalPipeline(
    query_embedding_pipeline=embedding,
    retriever=retriever,
)

results = pipeline.process(
    "Quels sont les garanties contre le vol ?",
    top_k=5,
)



for result in results:
    print("=" * 80)
    print(result.score)
    print(result.payload["section_title"])
    print(result.text)