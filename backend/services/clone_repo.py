from git import Repo
from pathlib import Path

def clone_repository(repo_url: str) -> str:

    repo_name=repo_url.rstrip("/").split("/")[-1]
    clone_path = Path("repositories") / repo_name

    if clone_path.exists():
        return str(clone_path)
    
    Repo.clone_from(repo_url, clone_path)

    return str(clone_path)