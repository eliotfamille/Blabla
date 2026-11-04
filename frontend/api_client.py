import httpx

url = "http://127.0.0.1:8000"

def envoyer(message: str):
    r = httpx.post(f"{url}/chat", json={"message": message}, timeout=60)
    r.raise_for_status()    # si renvois erreur
    data = r.json()
    if "reponse" not in data: # si le json ne contien pas la reponse
        raise ValueError(f"Réponse inattendue du serveur : {data}")
    return data["reponse"]
