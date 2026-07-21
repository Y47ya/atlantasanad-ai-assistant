from pathlib import Path
import os
from dotenv import load_dotenv

from src.ingestion.tools import load_config

PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / ".env")

PARSER_CONFIG = load_config(
    PROJECT_ROOT / "configs/ingestion/parser.yaml"
)

OLLAMA_PULL_IF_MISSING = os.getenv("OLLAMA_PULL_IF_MISSING", True)
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_PROVIDER = os.getenv("OLLAMA_PROVIDER", "ollama")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", 300))
OLLAMA_TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE", 0.0)) # Almost deterministic, 0 creativeness

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 512))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 100))

separators_raw = os.getenv("CHUNK_SEPARATORS", "\n\n|||\n|||. |||! |||? |||; |||, ||| |||")
CHUNK_SEPARATORS = separators_raw.split("|||")

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3")
CHUNKING_STRATEGY = os.getenv("CHUNKING_STRATEGY", "recursive")

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))

QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "insurance_documents")
QDRANT_VECTOR_SIZE = os.getenv("QDRANT_VECTOR_SIZE", 1024)
QDRANT_DISTANCE = os.getenv("QDRANT_DISTANCE", "cosine")
