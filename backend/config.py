import os

Api_Key = os.environ.get("Api_Key","api")
Url = "https://integrate.api.nvidia.com/v1"
Model = os.environ.get("Model", "nvidia/nemotron-3-ultra-550b-a55b")
