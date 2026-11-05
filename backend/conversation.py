import uuid
from typing import TypedDict


class Message(TypedDict):
    role: str      # "user" | "assistant"
    content: str


# Stockage
conversations: dict[str, list[Message]] = {}


def create_conversation():  # Nouvelle conversation
    conv_id = str(uuid.uuid4())
    conversations[conv_id] = []
    return conv_id


def get_conversation(conv_id: str): # Recupere historique
    return conversations.get(conv_id, [])


def add_message(conv_id: str, role: str, content: str): # Message a l'historique
    if conv_id not in conversations:
        conversations[conv_id] = []
    conversations[conv_id].append({"role": role, "content": content})


def list_conversations():   # Liste conversations
    result = []
    for conv_id, messages in conversations.items():
        title = messages[0]["content"][:50] if messages else "Vide"
        result.append({"id": conv_id, "title": title, "message_count": len(messages)})
    return result


def delete_conversation(conv_id: str):  # Supprime conversation
    if conv_id in conversations:
        del conversations[conv_id]
        return True
    return False
