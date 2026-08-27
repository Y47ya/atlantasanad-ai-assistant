from typing import Type, Any
from pydantic import BaseModel
from langchain_core.tools import BaseTool

from src.agent.tools.input_shemas.simulation_input import SimulationToolInput
from src.agent.tools.output_schemas.simulation_result import SimulationResult
from src.agent.tools_informations import TOOLS_INFORMATIONS
from src.api.api_service import APIService
from src.api.models.simulation_request import SimulationRequest


SIMULATION_INFOS = TOOLS_INFORMATIONS.get("simulation")

class SimulationTool(BaseTool):

    name: str = SIMULATION_INFOS.get("name")
    description: str = SIMULATION_INFOS.get("description")
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
        nom_clie: str,
        prenclie: str,
        address_mail: str,
        cateprof: str,
        codepack: str,
        telemobi: str,
        typemote: str,
        puisvehi: str,
        valeneuf: str,
        valevena: str,
        long_gps: str,
        lati_gps: str,
    ) -> SimulationResult:

        request = SimulationRequest(
            nom_clie=nom_clie,
            prenclie=prenclie,
            address_mail=address_mail,
            cateprof=cateprof,
            codepack=codepack,
            telemobi=telemobi,
            typemote=typemote,
            puisvehi=puisvehi,
            valeneuf=valeneuf,
            valevena=valevena,
            long_gps=long_gps,
            lati_gps=lati_gps,
        )

        response = self.api_service.simulation(request)

        return SimulationResult(
            inputs=request,
            response=response,
        )


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