from pathlib import Path
import os
from dotenv import load_dotenv

from src.ingestion.tools import load_config

PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / ".env")

# PARSER_CONFIG = load_config(
#     PROJECT_ROOT / "configs/ingestion/parser.yaml"
# )

# print(PROJECT_ROOT)
# print(PROJECT_ROOT / ".env")
# print((PROJECT_ROOT / ".env").exists())

OLLAMA_PULL_IF_MISSING = os.getenv("OLLAMA_PULL_IF_MISSING")
OLLAMA_HOST = os.getenv("OLLAMA_HOST")
OLLAMA_PROVIDER = os.getenv("OLLAMA_PROVIDER")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT"))
OLLAMA_TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE")) # Almost deterministic, 0 creativeness

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP"))

separators_raw = os.getenv("CHUNK_SEPARATORS")
CHUNK_SEPARATORS = separators_raw.split("|||")

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
CHUNKING_STRATEGY = os.getenv("CHUNKING_STRATEGY")

QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_PORT = int(os.getenv("QDRANT_PORT"))

QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME")
QDRANT_VECTOR_SIZE = os.getenv("QDRANT_VECTOR_SIZE")
QDRANT_DISTANCE = os.getenv("QDRANT_DISTANCE", "cosine")

RERANKER_MODEL = os.getenv("RERANKER_MODEL")
RETRIEVER_TOP_K = int(os.getenv("RETRIEVER_TOP_K"))
RERANKER_TOP_K = int(os.getenv("RERANKER_TOP_K"))

