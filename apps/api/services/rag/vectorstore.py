from typing import List, Dict, Any
from pathlib import Path
import chromadb

CHROMA_DIR = Path(".chroma")

def get_collection(name: str = "resumes"):
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_or_create_collection(name=name)

def upsert_documents(
    collection_name: str,
    ids: List[str],
    documents: List[str],
    embeddings: List[List[float]],
    metadatas: List[Dict[str, Any]],
):
    col = get_collection(collection_name)
    col.upsert(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)

def query_collection(
    collection_name: str,
    query_embedding: List[float],
    top_k: int = 5,
):
    col = get_collection(collection_name)
    res = col.query(query_embeddings=[query_embedding], n_results=top_k)
    return res
