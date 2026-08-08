from typing import Type, Any
from pydantic import BaseModel
from langchain_core.tools import BaseTool
from src.agent.tools.input_schemas.simulation_input import SimulationToolInput
from src.api.api_service import APIService
from src.api.models.simulation_request import SimulationRequest



class SimulationTool(BaseTool):

    name: str = "simulation"
    description: str = (
        "Effectue une simulation d'assurance automobile."
    )
    args_schema: Type[BaseModel] = SimulationToolInput
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

        request = SimulationRequest(**kwargs)

        return self.api_service.simulation(request)


# mock_api_client = MockAPIClient()
#
# api_service = APIService(
#     mock_api_client
# )
#
# simulation_tool = SimulationTool(
#     api_service
# )
#
# pprint(simulation_tool.args_schema.model_fields)