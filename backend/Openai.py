from collections.abc import Sequence
from typing import cast
from openai import OpenAI, NotFoundError
from openai.types.chat import ChatCompletionMessageParam
from config import OPENAI_API_KEY, OPENAI_BASE_URL
from conversation import Message


class OpenAIClient:
    def __init__(self):
        self._client: OpenAI | None = None  # initialise a None

    def set_api_key(self, api_key: str):    # Definir cle API
        self._client = OpenAI(
            api_key=api_key,
            base_url=OPENAI_BASE_URL,
        )

    def get_client(self):    # Obtenir ou creer client
        if self._client is None:
            if not OPENAI_API_KEY:
                raise RuntimeError("Cle API OpenAI non configuree.")
            self._client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
        return self._client

    def list_models(self):  # Lister modeles chat disponibles
        client = self.get_client()
        models = client.models.list()
        model_ids = sorted(m.id for m in models)

        exclude_keywords = [
            'embed', 'embedding',
            'vision', 'vlm', 'vl-',
            'guard', 'safety',
            'video', 'audio',
            'translate', 'riva',
            'parse',
            'clip',
            'reward',
            'rerank',
            'classif',
            'detector',
            'calibration',
        ]

        chat_models = []
        for mid in model_ids:
            mid_lower = mid.lower()
            if not any(kw in mid_lower for kw in exclude_keywords):
                chat_models.append(mid)

        print("Modeles chat disponibles (openai):", chat_models)
        return chat_models

    def chat(self, model: str, message: str):   # Generer reponse chat
        client = self.get_client()
        try:
            completion = client.chat.completions.create(  # appel api openai
                model=model,
                messages=[{"role": "user", "content": message}],
                temperature=1,
                top_p=0.95,
                max_tokens=10384,
                stream=True,
            )
            complet = ""
            for chunk in completion:
                if not chunk.choices:
                    continue
                if chunk.choices[0].delta.content is not None:
                    complet += chunk.choices[0].delta.content
            return complet or "sans reponse"
        except NotFoundError:
            return f"[Erreur] Le modele '{model}' n'est pas disponible pour le chat."
        except Exception:
            return "[Erreur] Erreur inattendue"

    def chat_with_history(self, model: str, history: Sequence[Message]):    # Chat avec historique
        client = self.get_client()
        try:
            completion = client.chat.completions.create(
                model=model,
                messages=cast(list[ChatCompletionMessageParam], history),   # cast pour pyright
                temperature=1,
                top_p=0.95,
                max_tokens=10384,
                stream=True,
            )
            complet = ""
            for chunk in completion:
                if not chunk.choices:
                    continue
                if chunk.choices[0].delta.content is not None:
                    complet += chunk.choices[0].delta.content
            return complet or "sans reponse"
        except NotFoundError:
            return f"[Erreur] Le modele '{model}' n'est pas disponible pour le chat."
        except Exception:
            return "[Erreur] Erreur inattendue"

# Instance globale
openai_client = OpenAIClient()
