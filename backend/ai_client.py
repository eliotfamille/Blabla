from openai import OpenAI
from openai import NotFoundError
from config import Url, Model

client = None
model = Model
def api(cle):
    global client   # pour modifier client
    client = OpenAI(
        api_key=cle,
        base_url=Url,
    )
def list_model():
    if client is None:
        raise RuntimeError("Clé API non configurée. Utilise le bouton Clé API.")
    models = client.models.list()
    model_ids = sorted(m.id for m in models)
    print("Modèles disponibles:", model_ids)
    return model_ids

def get_model():
    return model

def set_model(nom):
    global model
    model = nom

def repondre(message):
    if client is None:
        raise RuntimeError("Cle vide")
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": message}],
            temperature=1,
            top_p=0.95,
            max_tokens=10384,
            extra_body={"chat_template_kwargs": {"enable_thinking": True}},
            stream=True
        )
        complet = ""
        for chunk in completion:
            if not chunk.choices:
                continue
            reasoning = getattr(chunk.choices[0].delta, "reasoning_content", None)
            if reasoning:
                print(reasoning, end="")
            if chunk.choices[0].delta.content is not None:
                complet += chunk.choices[0].delta.content

        return complet or "sans reponse"
    except NotFoundError:
        return f"[Erreur] Le modèle '{model}' n'est pas disponible pour le chat. Choisis un modèle de chat (ex: nvidia/nemotron-3-ultra-550b-a55b)."
    except Exception as e:
        return f"[Erreur] {e}"
