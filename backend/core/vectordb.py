from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

from langchain_qdrant import QdrantVectorStore

from core.embeddings import embedding_model

COLLECTION_NAME = "github_repo"

client = QdrantClient(path="./qdrant_db")


def create_collection():

    if client.collection_exists(COLLECTION_NAME):
        client.delete_collection(COLLECTION_NAME)

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )


def get_vector_store():

    return QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embedding_model
    )


def index_documents(documents):

    create_collection()

    vector_store = get_vector_store()

    vector_store.add_documents(documents)

    return vector_store


# Used by the retriever
vector_store = get_vector_store()