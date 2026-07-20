from hashlib import sha256
from pathlib import Path
from datetime import datetime
from src.ingestion.models.llm_generation import LLMGenerationInfo


def generate_document_id(pdf_path: Path) -> str:
    hasher = hashlib.sha256()

    with open(pdf_path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)

    return hasher.hexdigest()

import hashlib

def generate_chunk_id(
    document_id: str,
    section_title: str,
    chunk_index: int,
    text: str,
) -> str:
    return hashlib.sha256(
        f"{document_id}:{section_title}:{chunk_index}:{text}".encode("utf-8")
    ).hexdigest()

def get_llm_generation_info(llm)-> LLMGenerationInfo:
    return LLMGenerationInfo(
        provider=llm.provider,
        model=llm.model,
        generated_at=datetime.now()
    )

def generate_text_hash(text: str) -> str:
    return sha256(
        text.encode("utf-8")
    ).hexdigest()