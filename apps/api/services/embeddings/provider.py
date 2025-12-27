import os
from typing import List

def get_provider() -> str:
    return os.getenv("EMBEDDINGS_PROVIDER", "openai").lower()

def embed_texts(texts: List[str]) -> List[List[float]]:
    provider = get_provider()

    if provider == "openai":
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        model = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")

        resp = client.embeddings.create(model=model, input=texts)
        return [d.embedding for d in resp.data]

    elif provider == "local":
        from sentence_transformers import SentenceTransformer
        model_name = os.getenv("LOCAL_EMBED_MODEL", "all-MiniLM-L6-v2")
        model = SentenceTransformer(model_name)
        vectors = model.encode(texts, normalize_embeddings=True)
        return vectors.tolist()

    else:
        raise ValueError(f"Unknown EMBEDDINGS_PROVIDER: {provider}")
