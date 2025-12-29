from __future__ import annotations

import uuid
import json
import re

from fastapi import APIRouter, HTTPException, Form
from pydantic import BaseModel

from services.rag.chunking import chunk_text
from services.embeddings.provider import embed_texts
from services.rag.vectorstore import upsert_documents, query_collection
from services.llm.ollama_client import ollama_generate

router = APIRouter(prefix="/job", tags=["Job"])

JOB_COLLECTION = "jobs"
RESUME_COLLECTION = "resumes"


class JobUploadRequest(BaseModel):
    title: str
    company: str | None = None
    location: str | None = None
    description: str

class MatchRequest(BaseModel):
    job_id: str
    top_k_resume: int = 6



def _store_job_main(job_id: str, title: str, company: str | None, location: str | None, description: str):

    main_id = f"{job_id}::main"
    main_meta = {
        "job_id": job_id,
        "is_main": True,
        "title": title,
        "company": company,
        "location": location,
    }
    upsert_documents(
        collection_name=JOB_COLLECTION,
        ids=[main_id],
        documents=[description],
        embeddings=embed_texts([description]),
        metadatas=[main_meta],
    )

def _store_job_chunks(job_id: str, title: str, company: str | None, location: str | None, description: str):
    chunks = chunk_text(description, max_chars=900, overlap=150)
    if not chunks:
        raise HTTPException(status_code=422, detail="Chunking produced no text.")

    embeddings = embed_texts(chunks)
    ids = [f"{job_id}::chunk::{i}" for i in range(len(chunks))]
    metadatas = [
        {
            "job_id": job_id,
            "is_main": False,
            "chunk_index": i,
            "title": title,
            "company": company,
            "location": location,
        }
        for i in range(len(chunks))
    ]

    upsert_documents(
        collection_name=JOB_COLLECTION,
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
    )
    return len(chunks)

def _load_job_main(job_id: str) -> str | None:
    q_emb = embed_texts([f"MAIN JOB DESCRIPTION {job_id}"])[0]
    res = query_collection(JOB_COLLECTION, q_emb, top_k=15)
    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]

    for d, m in zip(docs, metas):
        if m and m.get("job_id") == job_id and m.get("is_main") is True:
            return d
    return None

def _parse_json_from_llm(text: str):
    try:
        match = re.search(r"\{[\s\S]*\}", text)
        if not match:
            return None
        return json.loads(match.group(0))
    except Exception:
        return None


@router.post("/upload")
def upload_job(req: JobUploadRequest):
    title = (req.title or "").strip()
    description = (req.description or "").strip()

    if not title:
        raise HTTPException(status_code=400, detail="Job title is required.")
    if not description:
        raise HTTPException(status_code=400, detail="Job description is required.")

    job_id = str(uuid.uuid4())

    _store_job_main(job_id, title, req.company, req.location, description)
    chunks_indexed = _store_job_chunks(job_id, title, req.company, req.location, description)

    return {"job_id": job_id, "chunks_indexed": chunks_indexed}


@router.post("/upload_text")
def upload_job_text(
    title: str = Form(...),
    company: str | None = Form(None),
    location: str | None = Form(None),
    description: str = Form(...),
):
    title = (title or "").strip()
    description = (description or "").strip()

    if not title:
        raise HTTPException(status_code=400, detail="Job title is required.")
    if not description:
        raise HTTPException(status_code=400, detail="Job description is required.")

    job_id = str(uuid.uuid4())

    _store_job_main(job_id, title, company, location, description)
    chunks_indexed = _store_job_chunks(job_id, title, company, location, description)

    return {"job_id": job_id, "chunks_indexed": chunks_indexed}


@router.post("/match")
def match_job(req: MatchRequest):
    job_id = (req.job_id or "").strip()
    if not job_id:
        raise HTTPException(status_code=400, detail="job_id is required.")

    job_full = _load_job_main(job_id)
    if not job_full:
        raise HTTPException(status_code=404, detail="Job not found. Upload the job first via /job/upload_text or /job/upload.")

    resume_q_emb = embed_texts([job_full])[0]
    resume_res = query_collection(RESUME_COLLECTION, resume_q_emb, top_k=req.top_k_resume)

    resume_docs = resume_res.get("documents", [[]])[0]
    resume_metas = resume_res.get("metadatas", [[]])[0]

    if not resume_docs:
        raise HTTPException(status_code=400, detail="No resume indexed. Please index a resume first using /rag/index_resume.")
    
    job_block = f"[JOB_MAIN]\n{job_full}"

    resume_blocks = []
    for i, (doc, meta) in enumerate(zip(resume_docs, resume_metas), start=1):
        resume_blocks.append(f"[RESUME_CHUNK {i} | {meta}]\n{doc}")

    prompt = f"""
You are a career matching assistant.
You MUST base your analysis ONLY on the provided JOB context and RESUME context.
If something is missing, say it clearly.

IMPORTANT RULES:
- Do NOT put a skill in "missing_skills" if it appears in RESUME context.
- Evidence must cite chunk labels only (e.g., "RESUME_CHUNK 2"), not raw text.
- Return STRICT JSON only. No markdown, no explanations outside JSON.

Return:
{{
  "match_score": 0-100,
  "strong_matches": [strings],
  "missing_skills": [strings],
  "recommended_actions": [strings],
  "evidence": {{
     "job": ["JOB_MAIN"],
     "resume": ["RESUME_CHUNK 2", "RESUME_CHUNK 4"]
  }},
  "notes": "short explanation"
}}

JOB CONTEXT:
{job_block}

RESUME CONTEXT:
{chr(10).join(resume_blocks)}
""".strip()

    llm_out = ollama_generate(prompt)
    parsed = _parse_json_from_llm(llm_out)

    return {
        "job_id": job_id,
        "result": parsed,
        "raw_llm": llm_out,
        "job_context_used": job_block[:1500],
        "resume_context_used": resume_blocks,
    }
