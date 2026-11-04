from openai import OpenAI
from config import Api_Key, Url, Model

client = OpenAI(
    api_key=Api_Key,
    base_url=Url,
)

def repondre(message):
    completion=client.chat.completions.create(
      model=Model,
      messages=[{"role":"user","content":message}],
      temperature=1,
      top_p=0.95,
      max_tokens=16384,
      extra_body={"chat_template_kwargs":{"enable_thinking":True}},
      stream=True
    )
    complet = ""
    for chunk in completion:
      if not chunk.choices:
        continue
      reasoning = getattr(chunk.choices[0].delta, "reasoning_content", None)
      if reasoning:
        print(reasoning, end="")    # raisonement
      if chunk.choices[0].delta.content is not None:
        complet += chunk.choices[0].delta.content # reponse du modele

    return complet or "sans reponse"
