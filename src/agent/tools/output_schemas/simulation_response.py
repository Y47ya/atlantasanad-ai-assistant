from dataclasses import dataclass


@dataclass
class SimulationResponse:
    status: str
    idenpoli: str
    numeacte: str
    idenrisq: str
    coef_crm: str
    impr_crm: str
    primnett: str
    taxeprim: str
    montacce: str
    primtota: str
    erreurs: list[str]
