import os
from langchain_core.documents import Document
from config import LANGUAGE_MAP,IGNORE_DIRS,IGNORE_EXTENSIONS
from pathlib import Path

def parse_repository(repo_path: Path,owner: str,repo: str)-> list[Document]:
    documents = []

    for root, dirs, files in os.walk(repo_path):

        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in files:

            file_path = Path(root) / file

            extension = file_path.suffix

            if extension in IGNORE_EXTENSIONS:
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                    relative_path = file_path.relative_to(repo_path)

                    documents.append(
                        Document(
                            page_content=content,
                            metadata={
                                "repo_id": f"{owner}/{repo}",
                                "repo_owner": owner,
                                "repo_name": repo,
                                "path": str(relative_path),
                                "extension": extension,
                                "language": LANGUAGE_MAP.get(extension, "text")
                            }
                        )
                    )

            except Exception:
                continue

    return documents