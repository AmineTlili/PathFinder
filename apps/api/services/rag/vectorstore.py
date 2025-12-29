from __future__ import annotations
import os
import chromadb

CHROMA_DIR = os.getenv("CHROMA_DIR", os.path.join(os.path.dirname(__file__), "..", "..", ".chroma"))
CHROMA_DIR = os.path.abspath(CHROMA_DIR)

_client = None

def get_client():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=CHROMA_DIR)
    return _client

def get_collection(name: str):
    client = get_client()
    return client.get_or_create_collection(name=name)

def upsert_documents(
    collection_name: str,
    ids: list[str],
    documents: list[str],
    embeddings: list[list[float]],
    metadatas: list[dict] | None = None,
):
    col = get_collection(collection_name)
    col.upsert(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)

def query_collection(collection_name: str, query_embedding: list[float], top_k: int = 5):
    col = get_collection(collection_name)
    return col.query(query_embeddings=[query_embedding], n_results=top_k)
