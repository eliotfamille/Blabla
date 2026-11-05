import httpx

url = "http://127.0.0.1:8000"

# verifie si reponse ok
def verifier(r: httpx.Response):
    if r.is_error:
        info = r.json().get("detail", r.text)
        raise RuntimeError(info)

# envoi et recoi reponse
def envoyer(message: str, provider: str | None = None, model: str | None = None, conversation_id: str | None = None):
    payload = {"message": message}
    if provider:
        payload["provider"] = provider
    if model:
        payload["model"] = model
    if conversation_id:
        payload["conversation_id"] = conversation_id    # continue la conversation
    r = httpx.post(f"{url}/chat", json=payload, timeout=60)    # envoi le message
    verifier(r)     # erreur http
    return r.json()     # reponse + conversation_id

# enregistre cle
def enregistreCle(cle: str, provider: str):
    r = httpx.post(f"{url}/config/cle", json={"cle": cle, "provider": provider}, timeout=10)
    verifier(r)

def lister_modeles(provider: str | None = None):
    params = {}
    if provider:
        params["provider"] = provider
    r = httpx.get(f"{url}/models", params=params, timeout=30)
    verifier(r)
    return r.json()

def choisir_modele(nom: str, provider: str | None = None):
    payload = {"modele": nom}
    if provider:
        payload["provider"] = provider
    r = httpx.post(f"{url}/config/modele", json=payload, timeout=10)
    verifier(r)

def definir_provider(provider: str):
    r = httpx.post(f"{url}/config/provider", params={"provider": provider}, timeout=10)     # query, pas body
    verifier(r)

def get_provider():
    r = httpx.get(f"{url}/config/provider", timeout=10)
    verifier(r)
    return r.json()["provider"]

def lister_conversations():
    r = httpx.get(f"{url}/conversations", timeout=10)
    verifier(r)
    return r.json()["conversations"]

def supprimer_conversation(conv_id: str):
    r = httpx.delete(f"{url}/conversations/{conv_id}", timeout=10)
    verifier(r)