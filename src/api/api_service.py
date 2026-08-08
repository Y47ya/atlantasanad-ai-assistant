from src.api.client.base_client import BaseAPIClient
from src.api.models.edition_devis_request import EditionDevisRequest
from src.api.models.simulation_request import SimulationRequest


class APIService:

    def __init__(
        self,
        client: BaseAPIClient,
    ):
        self.client = client

    def simulation(
        self,
        request: SimulationRequest,
    ):
        return self.client.simulation(request)

    def edition_devis(
        self,
        request: EditionDevisRequest,
    ):
        return self.client.edition_devis(request)