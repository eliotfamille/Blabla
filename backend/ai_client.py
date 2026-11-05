from config import Provider, DEFAULT_PROVIDER, OPENAI_MODEL, GOOGLE_MODEL, NVIDIA_MODEL
from schemas import Request
from Openai import openai_client
from Google import google_client
from Nvidia import nvidia_client
import conversation

class AIClient:
    def __init__(self):
        self.current_provider = DEFAULT_PROVIDER  # provider actif
        self.current_model = self.get_default_model(DEFAULT_PROVIDER)  # modele actif

    def get_default_model(self, provider: Provider):   # Modele par defaut
        if provider == Provider.OPENAI:
            return OPENAI_MODEL
        elif provider == Provider.GOOGLE:
            return GOOGLE_MODEL
        elif provider == Provider.NVIDIA:
            return NVIDIA_MODEL
        return NVIDIA_MODEL

    def set_api_key(self, api_key: str, provider: Provider):    # Definir cle API pour un provider
        if provider == Provider.OPENAI:
            openai_client.set_api_key(api_key)
        elif provider == Provider.GOOGLE:
            google_client.set_api_key(api_key)
        elif provider == Provider.NVIDIA:
            nvidia_client.set_api_key(api_key)

    def set_provider(self, provider: Provider): # Definir provider actif
        self.current_provider = provider
        self.current_model = self.get_default_model(provider)

    def set_model(self, model: str, provider: Provider | None = None):  # Definir modele actif
        if provider:
            self.current_provider = provider
        self.current_model = model

    def get_provider(self):
        return self.current_provider

    def get_model(self):
        return self.current_model

    def get_provider_client(self, provider: Provider):  # Obtenir le client pour un provider
        if provider == Provider.OPENAI:
            return openai_client
        elif provider == Provider.GOOGLE:
            return google_client
        elif provider == Provider.NVIDIA:
            return nvidia_client
        raise ValueError(f"Provider non supporte: {provider}")

    def list_models(self, provider: Provider | None = None):    # Lister modeles chat pour un provider
        provider = provider or self.current_provider
        client = self.get_provider_client(provider)
        return client.list_models()

    def repondre(self, request: Request):   # Generer reponse IA sans historique
        provider = request.provider or self.current_provider  # provider demande
        model = request.model or self.current_model  # modele demande
        client = self.get_provider_client(provider)
        try:
            return client.chat(model, request.message)
        except RuntimeError as e:
            return f"[Erreur] {e}"  # cle manquante
        except Exception:
            return "[Erreur] Erreur inattendue"

    def repondre_with_history(self, request: Request):  # Reponse avec historique
        provider = request.provider or self.current_provider
        model = request.model or self.current_model
        conv_id = request.conversation_id or conversation.create_conversation()     # recupere ou cree conversation
        conversation.add_message(conv_id, "user", request.message)  # ajoute message utilisateur
        history = conversation.get_conversation(conv_id)
        client = self.get_provider_client(provider)
        try:
            reponse = client.chat_with_history(model, history)
        except RuntimeError as e:
            reponse = f"[Erreur] {e}"   # cle manquante
        except Exception:
            reponse = "[Erreur] Erreur inattendue"
        conversation.add_message(conv_id, "assistant", reponse)     # ajoute reponse
        return reponse, conv_id

client_instance = AIClient()  # instance globale

def api(cle: str, provider: Provider = Provider.NVIDIA):    # Cle provider
    client_instance.set_api_key(cle, provider)  # set cle api

def list_model(provider: Provider | None = None):   # Lister modeles provider
    return client_instance.list_models(provider)  # liste modeles

def get_model():
    return client_instance.get_model()  # get modele actif

def set_model(nom: str, provider: Provider | None = None):
    client_instance.set_model(nom, provider)  # set modele

def get_provider():
    return client_instance.get_provider()  # get provider actif

def set_provider(provider: Provider):
    client_instance.set_provider(provider)  # set provider

def repondre(request: Request):
    return client_instance.repondre(request)  # generer reponse

def repondre_with_history(request: Request):
    return client_instance.repondre_with_history(request)   # reponse + id conversation