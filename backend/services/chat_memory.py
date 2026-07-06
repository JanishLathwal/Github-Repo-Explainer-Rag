from langchain_core.messages import (
    HumanMessage,
    AIMessage,
)

chat_history = {}


def get_history(session_id: str):

    if session_id not in chat_history:
        chat_history[session_id] = []

    return chat_history[session_id]