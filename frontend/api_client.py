import httpx

url = "http://127.0.0.1:8000"

# verifie si reponse ok
def verifier(r:httpx.Response):
    if r.is_error:
        info = r.json().get("detail", r.text)
        raise RuntimeError(info)

# envoi et recoi reponse
def envoyer(message: str):
    r = httpx.post(f"{url}/chat", json={"message": message}, timeout=60)    # envoi le message
    data = r.json()
    if "reponse" not in data: # si le json ne contien pas la reponse
        raise ValueError(f"Réponse inattendue du serveur : {data}")
    return data["reponse"]

# enregistre cle
def enregistreCle(cle: str):
    r = httpx.post(f"{url}/config/cle", json={"cle": cle}, timeout=10)
    verifier(r)
