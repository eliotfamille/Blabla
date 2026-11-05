from google import genai
from config import GOOGLE_API_KEY, GOOGLE_MODEL

class GoogleClient:
    def __init__(self):
        self.client: genai.Client | None = None  # initialisé à None

    def set_api_key(self, api_key: str):    # Definir cle API
        self.client = genai.Client(api_key=api_key)

    def get_client(self) -> genai.Client:  # Obtenir ou creer client
        if self.client is None:
            if not GOOGLE_API_KEY:
                raise RuntimeError("Cle API Google AI non configuree.")
            self.client = genai.Client(api_key=GOOGLE_API_KEY)
        return self.client

    def list_models(self):
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
            return [GOOGLE_MODEL]

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


# Instance globale
google_client = GoogleClient()
