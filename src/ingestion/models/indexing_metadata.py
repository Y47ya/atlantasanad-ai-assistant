from dataclasses import dataclass
from datetime import datetime


@dataclass
class IndexingMetadata:
    embedding_provider: str
    embedding_model: str
    chunking_strategy: str
    hash: str
    indexed_at: datetime