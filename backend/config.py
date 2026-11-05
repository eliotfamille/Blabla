import os
from enum import Enum


class Provider(str, Enum):
    OPENAI = "openai"
    GOOGLE = "google"
    NVIDIA = "nvidia"


# NVIDIA (existant)
NVIDIA_URL = "https://integrate.api.nvidia.com/v1"  # url api nvidia
NVIDIA_MODEL = os.environ.get("NVIDIA_MODEL", "nvidia/nemotron-3-ultra-550b-a55b")  # modele par defaut
NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY", "")  # cle api nvidia

# OpenAI
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")  # cle api openai
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-6-astra")  # modele par defaut
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")  # url api openai

# Google AI (Gemini)
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")  # cle api google
GOOGLE_MODEL = os.environ.get("GOOGLE_MODEL", "gemini-flash-latest")  # modele par defaut

# Provider par defaut
DEFAULT_PROVIDER = Provider(os.environ.get("DEFAULT_PROVIDER", "nvidia"))  # provider initial
