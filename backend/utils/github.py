from urllib.parse import urlparse


def parse_github_repo(repo_url: str) -> tuple[str, str]:

    parsed = urlparse(repo_url)

    if parsed.netloc != "github.com":
        raise ValueError("Invalid GitHub URL")

    parts = parsed.path.strip("/").split("/")

    if len(parts) < 2:
        raise ValueError("Invalid GitHub repository")

    owner = parts[0]
    repo = parts[1].removesuffix(".git")

    return owner, repo