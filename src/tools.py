from qdrant_client import QdrantClient


def create_qdrant_client(
    host: str,
    port: int,
) -> QdrantClient:
    return QdrantClient(
        host=host,
        port=port,
        check_compatibility=False,
    )