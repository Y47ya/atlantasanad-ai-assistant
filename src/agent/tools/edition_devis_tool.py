from langchain_core.tools import BaseTool

from src.agent.tools.document import pdf_extractor
from src.agent.tools.document.pdf_extractor import PDFExtractor
from src.agent.tools.input_schemas.edition_devis_input import EditionDevisToolInput
from src.api.api_service import APIService
from typing import Type, Any
from pydantic import BaseModel
from src.api.models.edition_devis_request import EditionDevisRequest


class EditionDevisTool(BaseTool):

    name: str = "edition_devis"

    description: str = (
        "Consulte le devis d'une police d'assurance à partir de son identifiant."
        "Utilise cet outil lorsque l'utilisateur souhaite consulter ou éditer un devis existant."
    )

    args_schema: Type[BaseModel] = EditionDevisToolInput
    pdf_extractor: PDFExtractor
    api_service: APIService

    def __init__(
            self,
            pdf_extractor: PDFExtractor,
            api_service: APIService,
            **kwargs,
    ):
        super().__init__(
            pdf_extractor=pdf_extractor,
            api_service=api_service,
            **kwargs,
        )

    def _run(self, idenpoli: int) -> str:

        request = EditionDevisRequest(
            idenpoli=idenpoli
        )

        response = self.api_service.edition_devis(
            request
        )

        acte = response["acte"]

        if acte["stat__ws"] != "SUCCESS":
            return (
                "Impossible de récupérer le devis."
            )

        return self.pdf_extractor.extract_text(
            acte["contdocu"]
        )