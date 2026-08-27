from pathlib import Path
from json import load

from src.agent.tools.output_schemas.edition_devis_result import EditionDevisResult
from src.agent.tools.output_schemas.simulation_response import SimulationResponse
from src.api.client.base_client import BaseAPIClient
from src.api.models.edition_devis_request import EditionDevisRequest
from src.api.models.simulation_request import SimulationRequest


class MockAPIClient(BaseAPIClient):

    def __init__(self, base_path: Path | str, use_parser: bool):
        self.base_path = Path(base_path)
        self.use_parser = use_parser


    def _load_response(self, filename: str) -> dict:
        path = self.base_path / filename

        with path.open("r", encoding="utf-8") as file:
            response = load(file)

        return response

    def simulation(
        self,
        request: SimulationRequest,
    ):

        response = self._load_response("simulation_api_response.json")['acte']

        return SimulationResponse(
            status=response["stat__ws"],
            idenpoli=response["idenpoli"],
            numeacte=response["numeacte"],
            idenrisq=response["idenrisq"],
            coef_crm=response["coef_crm"],
            impr_crm=response["impr_crm"],
            primnett=response["primnett"],
            taxeprim=response["taxeprim"],
            montacce=response["montacce"],
            primtota=response["primtota"],
            erreurs=response["erreurs"]
        )

    def edition_devis(
            self,
            request: EditionDevisRequest,
    ) -> dict:

        response = self._load_response(
            "edition_devis_response.json"
        )

        acte = response["acte"]

        print("ID: ", acte["idenpoli"])

        if acte["stat__ws"] != "SUCCESS":
            return response

        if acte["idenpoli"] != int(acte["idenpoli"]):
            return {
                "acte": {
                    "stat__ws": "FAILED",
                    "idenpoli": None,
                    "contdocu": None,
                    "erreurs": [
                        "Devis introuvable."
                    ],
                }
            }

        print("edition devis mock api client passed")

        return {
                    "stat__ws": "SUCCESS",
                    "idenpoli": acte["idenpoli"],
                    "contdocu": acte["contdocu"],
                    "erreurs": [],
                }




