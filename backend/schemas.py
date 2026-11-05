# schema des donnees
from pydantic import BaseModel, Field
from config import Provider


class Request(BaseModel):
    message: str
    provider: Provider | None = None
    model: str | None = None
    conversation_id: str | None = None

class Reponse(BaseModel):
    reponse: str
    conversation_id: str

class Cle(BaseModel):
    cle: str = Field(min_length=1)  # cle api
    provider: Provider  # fournisseur

class Modele(BaseModel):
    modele: str = Field(min_length=1)  # nom modele
    provider: Provider  # fournisseur