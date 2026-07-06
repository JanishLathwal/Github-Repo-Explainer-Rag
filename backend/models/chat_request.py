from pydantic import BaseModel

class ChatRequest(BaseModel):
    repo_id: str
    session_id: str
    question: str