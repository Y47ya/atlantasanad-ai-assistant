from abc import ABC, abstractmethod

from src.api.models.edition_devis_request import EditionDevisRequest
from src.api.models.simulation_request import SimulationRequest


class BaseAPIClient(ABC):

    @abstractmethod
    def simulation(self, request: SimulationRequest):
        ...

    @abstractmethod
    def edition_devis(self, request: EditionDevisRequest):
        ...