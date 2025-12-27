from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import fitz

from services.rag.chunking import chunk_text
from services.embeddings.provider import embed_texts
from services.rag.vectorstore import upsert_documents, query_collection

router = APIRouter(prefix="/rag", tags=["RAG"])

COLLECTION = "resumes"

class QueryRequest(BaseModel):
    question: str
    top_k: int = 5

@router.post("/index_resume")
async def index_resume(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF file.")

    pdf_bytes = await file.read()
    if not pdf_bytes:
        raise HTTPException(status_code=400, detail="Empty file.")

    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = "\n".join([page.get_text("text") for page in doc]).strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF parsing failed: {str(e)}")

    if not text:
        raise HTTPException(status_code=422, detail="No extractable text found in the PDF.")

    chunks = chunk_text(text, max_chars=900, overlap=150)
    if not chunks:
        raise HTTPException(status_code=422, detail="Chunking produced no text.")

    embeddings = embed_texts(chunks)

    ids = [f"{file.filename}::chunk::{i}" for i in range(len(chunks))]
    metadatas = [{"filename": file.filename, "chunk_index": i} for i in range(len(chunks))]

    upsert_documents(
        collection_name=COLLECTION,
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    return {"filename": file.filename, "chunks_indexed": len(chunks)}

@router.post("/query")
def rag_query(req: QueryRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Empty question.")

    q_emb = embed_texts([req.question])[0]
    res = query_collection(COLLECTION, q_emb, top_k=req.top_k)

    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    dists = res.get("distances", [[]])[0]

    results = []
    for doc, meta, dist in zip(docs, metas, dists):
        results.append({
            "text": doc,
            "meta": meta,
            "distance": dist
        })

    return {"question": req.question, "results": results}
