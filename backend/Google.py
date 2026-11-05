from collections.abc import Sequence
from google import genai
from google.genai import types
from config import GOOGLE_API_KEY, GOOGLE_MODEL
from conversation import Message

class GoogleClient:
    def __init__(self):
        self.client: genai.Client | None = None  # initialise a None

    def set_api_key(self, api_key: str):    # Definir cle API
        self.client = genai.Client(api_key=api_key)

    def get_client(self) -> genai.Client:  # Obtenir ou creer client
        if self.client is None:
            if not GOOGLE_API_KEY:
                raise RuntimeError("Cle API Google AI non configuree.")
            self.client = genai.Client(api_key=GOOGLE_API_KEY)
        return self.client

    def list_models(self):  # Lister modeles
        client = self.get_client()
        try:
            models = client.models.list()
            model_names = []
            for model in models:
                name = getattr(model, 'name', str(model))
                model_names.append(name)
            print("Modeles chat disponibles (google):", model_names)
            return model_names
        except Exception:
            return [GOOGLE_MODEL]   # liste de secours

    def chat(self, model: str, message: str):    # Generer reponse chat
        client = self.get_client()
        try:
            response = client.models.generate_content(  # appel api google gemini
                model=model,
                contents=message,
            )
            return response.text or "sans reponse"
        except Exception:
            return "[Erreur] Erreur inattendue"

    def chat_with_history(self, model: str, history: Sequence[Message]):   # Chat avec historique
        client = self.get_client()
        try:
            contents = []
            for msg in history:
                role = "user" if msg["role"] == "user" else "model"     # google dit model
                part = types.Part.from_text(text=msg["content"])
                content = types.Content(role=role, parts=[part])
                contents.append(content)
            response = client.models.generate_content(model=model, contents=contents)
            return response.text or "sans reponse"
        except Exception:
            return "[Erreur] Erreur inattendue"

# Instance globale
google_client = GoogleClient()