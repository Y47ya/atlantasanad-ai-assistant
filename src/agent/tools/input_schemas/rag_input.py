from pydantic import BaseModel, Field


class RAGInput(BaseModel):
    question: str = Field(
        description="Question de l'utilisateur."
    )