from pydantic import BaseModel



class EditionDevisResult(BaseModel):
    status: str
    policy_id: int | None = None
    message: str | None = None
