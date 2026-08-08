from pathlib import Path
from json import load, dumps
from src.api.client.base_client import BaseAPIClient
from src.api.models.edition_devis_request import EditionDevisRequest
from src.api.models.simulation_request import SimulationRequest


class MockAPIClient(BaseAPIClient):

    def __init__(self, base_path: Path | str):
        self.base_path = Path(base_path)

    def _load_response(self, filename: str) -> dict:
        path = self.base_path / filename

        with path.open("r", encoding="utf-8") as file:
            response = load(file)

        return response

    def simulation(
            self,
            request: SimulationRequest,
    ):
        return self._load_response("simulation_api_response.json")


    def edition_devis(
            self,
            request: EditionDevisRequest,
    ):
        return self._load_response("edition_devis_response.json")


