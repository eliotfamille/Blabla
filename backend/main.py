from fastapi import FastAPI, HTTPException
import ai_client
from schemas import Reponse, Request, Cle, Modele
from config import Provider

app = FastAPI()

@app.get('/')
async def raine():
    return {"Status": "OK"}  # health check

@app.post('/chat', response_model=Reponse)
async def repondre(request: Request):
    reponse = ai_client.repondre(request)  # generer reponse
    return Reponse(reponse=reponse)

@app.post('/config/cle')
async def Cle_Api(cle: Cle):
    ai_client.api(cle.cle, cle.provider)  # configurer cle api
    return {"Status": "OK"}

@app.get("/models")
def modeles(provider: Provider | None = None):
    try:
        return {
            "modeles": ai_client.list_model(provider),  # liste modeles
            "actuel": ai_client.get_model(),  # modele actif
            "provider": ai_client.get_provider().value  # provider actif
        }
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=502, detail="Impossible de lister les modeles")  # erreur liste modeles

@app.post("/config/modele")
def definir_modele(req: Modele):
    ai_client.set_model(req.modele, req.provider)  # changer modele
    return {"status": "ok"}

@app.post("/config/provider")
def definir_provider(provider: Provider):
    ai_client.set_provider(provider)  # changer provider
    return {"status": "ok", "provider": provider.value}

@app.get("/config/provider")
def get_provider():
    return {"provider": ai_client.get_provider().value}  # get provider actif