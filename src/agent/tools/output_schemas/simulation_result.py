from pydantic import BaseModel

from src.agent.tools.output_schemas.simulation_response import SimulationResponse
from src.api.models.simulation_request import SimulationRequest

class SimulationResult(BaseModel):
    inputs: SimulationRequest
    response: SimulationResponse