from pydantic import BaseModel, Field


class SimulationToolInput(BaseModel):

    nom_clie: str = Field(description="Nom du client")

    prenclie: str = Field(description="Prénom du client")

    cateprof: str = Field(description="Catégorie professionnelle")

    codepack: str = Field(description="Code du pack")

    telemobi: str = Field(description="Téléphone")

    adremail: str = Field(
        default="",
        description="Adresse email",
    )

    typemote: str = Field(
        description="Type de motorisation",
    )

    puisvehi: str = Field(
        description="Puissance fiscale",
    )

    valeneuf: str = Field(
        description="Valeur à neuf",
    )

    valevena: str = Field(
        description="Valeur vénale",
    )

    long_gps: str = Field(
        description="Longitude GPS",
    )

    lati_gps: str = Field(
        description="Latitude GPS",
    )