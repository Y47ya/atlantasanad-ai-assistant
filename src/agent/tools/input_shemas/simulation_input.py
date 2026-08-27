from pydantic import BaseModel, Field


class SimulationToolInput(BaseModel):

    nom_clie: str = Field(description="Nom du client")

    prenclie: str = Field(description="Prénom du client")
    cateprof: str = Field(description="Catégorie professionnelle")
    codepack: str = Field(description="Code du pack")
    telemobi: str = Field(description="Téléphone")
    address_mail: str = Field(description="Adresse email")
    typemote: str = Field(description="Type de motorisation")
    puisvehi: str = Field(description="Puissance fiscale")
    valeneuf: str = Field(description="Valeur à neuf")
    valevena: str = Field(description="Valeur vénale")
    long_gps: str = Field(default="0.0", description="Longitude GPS")
    lati_gps: str = Field(default="0.0", description="Latitude GPS")