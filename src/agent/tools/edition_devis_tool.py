
from langchain_core.tools import BaseTool
from src.agent.tools.input_shemas.edition_devis_input import EditionDevisToolInput
from src.agent.tools.output_schemas.edition_devis_result import EditionDevisResult
from src.api.api_service import APIService
from typing import Type, Any
from pydantic import BaseModel, PrivateAttr
from src.api.models.edition_devis_request import EditionDevisRequest
from src.documents.pdf_service import PDFService
from src.agent.tools_informations import TOOLS_INFORMATIONS


EDITIONS_DEVIS_INFOS = TOOLS_INFORMATIONS.get("recuperation_devis")

class EditionDevisTool(BaseTool):

    name: str = EDITIONS_DEVIS_INFOS.get("name")

    description: str = EDITIONS_DEVIS_INFOS.get("description")

    args_schema: Type[BaseModel] = EditionDevisToolInput
    _api_service: APIService = PrivateAttr()
    _pdf_service: PDFService = PrivateAttr()

    def __init__(
        self,
        api_service: APIService,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self._api_service = api_service
        self._pdf_service = PDFService()

    def _run(self, idenpoli: str) -> EditionDevisResult:
        request = EditionDevisRequest(
            idenpoli=idenpoli,
        )
        print("entrer _run outil")

        response = self._api_service.edition_devis(request)

        if response["stat__ws"] != "SUCCESS":
            result = EditionDevisResult(
                status="FAILED",
                policy_id=None,
                message="Devis introuvable.",
            )
        else:

            self._pdf_service.save(
                content=response["contdocu"],
            )

            result = EditionDevisResult(
                status=response["stat__ws"],
                policy_id=response["idenpoli"],
                message="Le devis a été généré avec succès.",
            )

        print(type(result.message))
        # print(result.content)
        return result
