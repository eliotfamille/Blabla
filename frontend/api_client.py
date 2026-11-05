import httpx

url = "http://127.0.0.1:8000"

# verifie si reponse ok
def verifier(r: httpx.Response):
    if r.is_error:
        info = r.json().get("detail", r.text)
        raise RuntimeError(info)

# envoi et recoi reponse
def envoyer(message: str, provider: str | None = None, model: str | None = None):
    payload = {"message": message}
    if provider:
        payload["provider"] = provider
    if model:
        payload["model"] = model
    r = httpx.post(f"{url}/chat", json=payload, timeout=60)    # envoi le message
    data = r.json()
    if "reponse" not in data: # si le json ne contien pas la reponse
        raise ValueError(f"Réponse inattendue du serveur : {data}")
    return data["reponse"]

# enregistre cle
def enregistreCle(cle: str, provider: str):
    r = httpx.post(f"{url}/config/cle", json={"cle": cle, "provider": provider}, timeout=10)
    verifier(r)

def lister_modeles(provider: str | None = None) -> dict:
    params = {}
    if provider:
        params["provider"] = provider
    r = httpx.get(f"{url}/models", params=params, timeout=30)
    verifier(r)
    return r.json()

def choisir_modele(nom: str, provider: str | None = None) -> None:
    payload = {"modele": nom}
    if provider:
        payload["provider"] = provider
    r = httpx.post(f"{url}/config/modele", json=payload, timeout=10)
    verifier(r)

def definir_provider(provider: str) -> None:
    r = httpx.post(f"{url}/config/provider", json=provider, timeout=10)
    verifier(r)

def get_provider() -> str:
    r = httpx.get(f"{url}/config/provider", timeout=10)
    verifier(r)
    return r.json()["provider"]