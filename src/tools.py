import time
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


BASE62_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def compute_id_from_time() -> str:
    micro_timestamp = int(time.time() * 1_000_000)

    num = micro_timestamp
    if num == 0:
        return BASE62_ALPHABET[0]

    arr = []
    base = len(BASE62_ALPHABET)
    while num:
        num, rem = divmod(num, base)
        arr.append(BASE62_ALPHABET[rem])
    arr.reverse()

    return "".join(arr)

