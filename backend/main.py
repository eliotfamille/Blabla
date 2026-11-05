from fastapi import FastAPI
import ai_client
from schemas import Reponse, Request, Cle, Modele

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

@app.get("/models")
def modeles():
    try:
        return {"modeles": ai_client.list_model(), "actuel": ai_client.get_model()}
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=502, detail="Impossible de lister les modèles")

@app.post("/config/modele")
def definir_modele(req: Modele):
    ai_client.set_model(req.modele)
    return {"status": "ok"}