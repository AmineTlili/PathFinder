from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.embeddings.provider import embed_texts
from services.rag.vectorstore import query_collection
from services.llm.ollama_client import ollama_generate

router = APIRouter(prefix="/assistant", tags=["Assistant"])
COLLECTION = "resumes"

class AnswerRequest(BaseModel):
    question: str
    top_k: int = 5

@router.post("/answer")
def answer(req: AnswerRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Empty question.")

    q_emb = embed_texts([req.question])[0]
    res = query_collection(COLLECTION, q_emb, top_k=req.top_k)

    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]

    context_blocks = []
    for i, (doc, meta) in enumerate(zip(docs, metas), start=1):
        context_blocks.append(f"[CHUNK {i} | {meta}] \n{doc}")

    context = "\n\n".join(context_blocks)

    prompt = f"""
You are a career assistant. Answer the user's question using ONLY the information in the context.
If the context does not contain enough information, say so.

Return:
1) Answer (concise)
2) Evidence: cite the chunk numbers you used (e.g., CHUNK 1, CHUNK 3)

QUESTION:
{req.question}

CONTEXT:
{context}
""".strip()

    response = ollama_generate(prompt)

    return {
        "question": req.question,
        "answer": response,
        "chunks_used": context_blocks
    }
