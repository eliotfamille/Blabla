from openai import OpenAI, NotFoundError
from config import NVIDIA_URL, NVIDIA_API_KEY


class NVIDIAClient:
    def __init__(self):
        self._client: OpenAI | None = None  # initialisé à None

    def set_api_key(self, api_key: str):    # Definir cle API
        self._client = OpenAI(
            api_key=api_key,
            base_url=NVIDIA_URL,
        )

    def get_client(self):    # Obtenir ou creer client.
        if self._client is None:
            if not NVIDIA_API_KEY:
                raise RuntimeError("Cle API NVIDIA non configuree.")
            self._client = OpenAI(api_key=NVIDIA_API_KEY, base_url=NVIDIA_URL)
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
            'guard',
        ]

        chat_models = []
        for mid in model_ids:
            mid_lower = mid.lower()
            if not any(kw in mid_lower for kw in exclude_keywords):
                chat_models.append(mid)

        print("Modeles chat disponibles (nvidia):", chat_models)
        return chat_models

    def chat(self, model: str, message: str) -> str:
        """Generer reponse chat."""
        client = self.get_client()
        try:
            completion = client.chat.completions.create(  # appel api nvidia
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
            return f"[Erreur] Le modele '{model}' n'est pas disponible pour le chat."
        except Exception:  # pylint: disable=broad-except
            return "[Erreur] Erreur inattendue"


# Instance globale
nvidia_client = NVIDIAClient()