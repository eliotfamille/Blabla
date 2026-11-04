# forme de message
from pydantic import BaseModel

class Request(BaseModel):
    message : str

class Reponse(BaseModel):
    reponse: str
