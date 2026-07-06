from fastapi import APIRouter

from models.chat_request import ChatRequest
from services.chat_service import ask_repository

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.post("/")
def chat(request: ChatRequest):

    return ask_repository(
        request.repo_id,
        request.session_id,
        request.question
    )