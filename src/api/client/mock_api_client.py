from pathlib import Path
from json import load
from src.api.client.base_client import BaseAPIClient
from src.api.models.edition_devis_request import EditionDevisRequest
from src.api.models.simulation_request import SimulationRequest


class MockAPIClient(BaseAPIClient):

    def __init__(self, base_path: Path | str):
        self.base_path = base_path

    def simulation(
            self,
            request: SimulationRequest,
    ):
        with open(self.base_path / "simulation_api_response.json", encoding="utf-8") as f:
            return load(f)

    def edition_devis(
            self,
            request: EditionDevisRequest,
    ):
        with open(self.base_path / "edition_devis_response.json", encoding="utf-8") as f:
            return load(f)

