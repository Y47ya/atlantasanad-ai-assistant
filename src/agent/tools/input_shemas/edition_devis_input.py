from pydantic import BaseModel, Field


class EditionDevisToolInput(BaseModel):

    idenpoli: str = Field(
        description="Identifiant de la police ou du devis",
    )