from qdrant_client.http.models import (
    Filter,
    FieldCondition,
    MatchValue
)

from core.vectordb import get_vector_store


def get_retriever(repo_id: str, k: int = 5):

    vector_store = get_vector_store()

    repo_filter = Filter(
        must=[
            FieldCondition(
                key="metadata.repo_id",
                match=MatchValue(value=repo_id)
            )
        ]
    )

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": k,
            "filter": repo_filter
        }
    )

    return retriever