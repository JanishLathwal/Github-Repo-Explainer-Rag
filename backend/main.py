from fastapi import FastAPI
from routers.repo import router as repo_router
from routers.chat import router as chat_router

app = FastAPI(title="GitHub Repo Explainer")

app.include_router(repo_router)
app.include_router(chat_router)