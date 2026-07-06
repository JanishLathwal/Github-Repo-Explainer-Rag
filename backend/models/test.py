from pydantic import BaseModel

class TestRetrieverRequest(BaseModel):
    repo_id: str
    question: str