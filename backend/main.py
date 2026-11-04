from fastapi import FastAPI
import ai_client
from schemas import Reponse, Request, Cle

app = FastAPI()

@app.get('/')
async def raine():
    return {"Statu" : "OK"}

@app.post('/chat', response_model = Reponse)
async def repondre(request:Request):
    reponse = ai_client.repondre(request.message)
    return Reponse(reponse=reponse)

@app.post('/config/cle')
async def Cle_Api(cle: Cle):
    ai_client.api(cle.cle)
    return {"Statu":"OK"}