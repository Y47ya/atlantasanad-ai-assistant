from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class LLMGenerationInfo:
    provider: str
    model: str
    # prompt_version: str
    generated_at: datetime