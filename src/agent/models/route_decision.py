from typing import Literal
from pydantic import BaseModel


class RouteDecision(BaseModel):
    route: Literal[
        "rag",
        "api",
        "rag+api",
    ]