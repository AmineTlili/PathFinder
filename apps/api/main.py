from fastapi import FastAPI
from routers.resume import router as resume_router
from routers.rag import router as rag_router
from dotenv import load_dotenv
from routers.assistant import router as assistant_router
from routers.job import router as job_router
from routers.apply import router as apply_router
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI(
    title="PathFinder",
    description="AI-powered Career Intelligence Platform",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(resume_router)
app.include_router(rag_router)
app.include_router(assistant_router)
app.include_router(job_router)
app.include_router(apply_router)


@app.get("/")
def health():
    return {"status": "ok", "service": "api"}