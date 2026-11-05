# Blabla

A small desktop chat app: a Kivy window talks to a FastAPI backend that forwards your messages to an AI model and shows the replies.

## Features

- Chat with an AI model, with conversation history during the session
- Provider choice: NVIDIA, OpenAI, Google
- Model choice from a dropdown list
- API key entry from the app (masked, kept in server memory)

## Requirements

- Python 3.10 or higher
- An API key from at least one provider:
  - NVIDIA: https://build.nvidia.com/settings/api-keys
  - OpenAI: https://platform.openai.com/api-keys
  - Google: https://aistudio.google.com/apikey

## Installation

```bash
git clone <repo-url> Blabla
cd Blabla
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

A single virtual environment serves both the backend and the frontend.

## Running

You need two terminals, each with the venv activated.

**Terminal 1: backend** (from the project root)

```bash
cd backend
fastapi dev
```

Alternative: `uvicorn main:app --reload`. The server listens on http://127.0.0.1:8000 and the interactive documentation is at http://127.0.0.1:8000/docs.

**Terminal 2: frontend**

```bash
cd frontend
python main.py
```

Always run the commands from their own folder, otherwise the imports fail.

## Usage

1. Pick a provider in the first dropdown.
2. Click **Cle API**, select the same provider, paste the key, then click **Enregistrer**.
3. The model list reloads. Pick a model.
4. Type a message, then click **Envoyer** or press Enter.

The key is sent to the backend and kept in memory only: it is lost when the server stops. You must enter it again at each launch, or set it with an environment variable.

## Configuration (optional)

Environment variables read by `backend/config.py`:

| Variable | Purpose | Default |
|---|---|---|
| `NVIDIA_API_KEY` | NVIDIA key | empty |
| `OPENAI_API_KEY` | OpenAI key | empty |
| `GOOGLE_API_KEY` | Google key | empty |
| `DEFAULT_PROVIDER` | provider at startup | `nvidia` |
| `NVIDIA_MODEL` | default NVIDIA model | `nvidia/nemotron-3-ultra-550b-a55b` |
| `OPENAI_MODEL` | default OpenAI model | see `config.py` |
| `GOOGLE_MODEL` | default Google model | `gemini-flash-latest` |

Example:

```bash
export NVIDIA_API_KEY="nvapi-..."
export DEFAULT_PROVIDER="nvidia"
```

## Security: never put your API key in files

**Never write your API key in the code or in any file of the project** (`config.py`, `ai_client.py`, the README, etc.). Anything committed and pushed to GitHub becomes public, and bots constantly scan GitHub to harvest keys.

- Enter the key with the **Cle API** button in the app, or with an environment variable in your terminal (see above).
- Never commit a file that contains a key, and keep such files in `.gitignore`.
- If a key was published by mistake, deleting it from the repository is not enough: it stays in the git history. **Revoke it** on the provider's website and generate a new one.

## Recommendation for NVIDIA

The NVIDIA Build catalog groups many models that are hosted separately, each with its own configuration: accepted parameters, response format, availability. A request that works with one model can fail with another, and the app sends the same parameters to all of them.

It is therefore recommended to choose a **lightweight model**:

- it answers faster;
- it is more often available and less rate-limited;
- very large models and "reasoning" models generate their reasoning before answering, which makes the wait longer.

If a model returns an error, pick another one from the list. Some listed models are not meant for chat (embeddings, images, etc.).

## Known limitations

- **Anthropic (Claude) is not supported** for now, due to a lack of usable documentation for this project.
- Conversation history is stored in memory: it is lost when the server stops.
- No streaming: the reply appears all at once.
- Local use only: the backend has no authentication, do not expose it on a network.

## Project structure

```
Blabla/
├── backend/
│   ├── main.py            # FastAPI routes
│   ├── ai_client.py       # provider and model selection
│   ├── Nvidia.py          # NVIDIA client
│   ├── Openai.py          # OpenAI client
│   ├── Google.py          # Google client
│   ├── conversation.py    # in-memory history
│   ├── schemas.py         # request and response formats
│   └── config.py          # URLs, models, environment variables
├── frontend/
│   ├── main.py            # main window
│   ├── popup_cle.py       # API key popup
│   ├── liste_modeles.py   # model dropdown
│   └── api_client.py      # HTTP calls to the backend
├── requirements.txt
└── README.md
```

## Troubleshooting

| Symptom | Lead |
|---|---|
| `[erreur] ... Connection refused` | the backend is not running |
| `Cle API ... non configuree` | save the key for the selected provider |
| Empty model list or error | check the key and the selected provider |
| `[Erreur] Le modele ... n'est pas disponible` | pick another model |
| `ModuleNotFoundError` | venv not activated, or command run from the wrong folder |

## Documentation used

- FastAPI: https://fastapi.tiangolo.com
- Kivy: https://kivy.org/doc/stable/
- httpx: https://www.python-httpx.org
- OpenAI Python SDK: https://github.com/openai/openai-python
- NVIDIA Build: https://build.nvidia.com
- Google Gen AI SDK: https://github.com/googleapis/python-genai
