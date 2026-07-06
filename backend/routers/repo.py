from fastapi import APIRouter
from utils.github import parse_github_repo
from models.request_models import RepoRequest
from services.clone_repo import clone_repository
from services.parser import parse_repository
from services.chunker import chunk_documents
from core.vectordb import index_documents
from core.retriever import get_retriever
from services.chat_service import ask_repository
# from models.test import TestRetrieverRequest

router = APIRouter(prefix="/repo", tags=["Repository"])


@router.post("/index")
def index_repository(request: RepoRequest):

    owner, repo = parse_github_repo(request.repo_url)
    local_path = clone_repository(request.repo_url)

    documents = parse_repository(
                    local_path,
                    owner,
                    repo
                )
    chunked_documents = chunk_documents(documents)

    index_documents(chunked_documents)

    return {
        "status": "success",
        "repo_id": f"{owner}/{repo}",
        "documents": len(documents),
        "chunks": len(chunked_documents)
    }

# @router.post("/test")
# def test_retriever(request: TestRetrieverRequest):

#     retriever = get_retriever(request.repo_id)

#     docs = retriever.invoke(request.question)

#     return [
#         {
#             "path": doc.metadata["path"],
#             "chunk_type": doc.metadata["chunk_type"],
#             "content": doc.page_content[:200]
#         }
#         for doc in docs
#     ]

