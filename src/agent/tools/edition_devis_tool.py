from langchain_core.tools import BaseTool
from src.agent.tools.input_schemas.edition_devis_input import EditionDevisToolInput
from src.api.api_service import APIService
from typing import Type, Any
from pydantic import BaseModel
from src.api.models.edition_devis_request import EditionDevisRequest


class EditionDevisTool(BaseTool):

    name: str = "edition_devis"

    description: str = (
        "Retourne les informations d'un devis."
    )

    args_schema: Type[BaseModel] = EditionDevisToolInput

    api_service: APIService

    def __init__(
            self,
            api_service: APIService,
            **kwargs,
    ):
        super().__init__(
            api_service=api_service,
            **kwargs,
        )

    def _run(
        self,
        **kwargs,
    ):

        request = EditionDevisRequest(**kwargs)

        return self.api_service.edition_devis(request)