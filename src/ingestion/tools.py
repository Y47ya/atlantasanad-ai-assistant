from dataclasses import is_dataclass, asdict
from enum import Enum
from hashlib import sha256
from pathlib import Path
from datetime import datetime
from src.ingestion.models.llm_generation import LLMGenerationInfo
from src.ingestion.models.section import ContentType
import yaml


def load_config(path: str):
    with open(path, "r") as file:
        return yaml.safe_load(file)

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


def serialize(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()

    if isinstance(obj, Enum):
        return obj.value

    if is_dataclass(obj):
        return asdict(obj)

    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

def to_json(obj):
    if is_dataclass(obj):
        return {
            key: to_json(value)
            for key, value in asdict(obj).items()
        }

    if isinstance(obj, dict):
        return {
            key: to_json(value)
            for key, value in obj.items()
        }

    if isinstance(obj, list):
        return [
            to_json(item)
            for item in obj
        ]

    if isinstance(obj, Enum):
        return obj.value

    if isinstance(obj, datetime):
        return obj.isoformat()

    return obj

def parse_content_type(value: str) -> ContentType:
    if value.startswith("ContentType."):
        value = value.split(".", 1)[1]

    # Enum name?
    if value in ContentType.__members__:
        return ContentType[value]

    # Enum value?
    return ContentType(value.lower())

from uuid import uuid5, NAMESPACE_URL

def chunk_hash_to_point_id(chunk_hash: str) -> str:
    return str(uuid5(NAMESPACE_URL, chunk_hash))