# forme de message
from pydantic import BaseModel, Field

class Request(BaseModel):
    message : str

class Reponse(BaseModel):
    reponse: str

class Cle(BaseModel):
    cle: str = Field(min_length=1)  # refuse si vide

class Modele(BaseModel):
    modele: str = Field(min_length=1)