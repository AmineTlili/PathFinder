from fastapi import FastAPI
from routers.resume import router as resume_router
from routers.rag import router as rag_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="PathFinder",
    description="AI-powered Career Intelligence Platform",
    version="0.1.0",
)

app.include_router(resume_router)
app.include_router(rag_router)

@app.get("/")
def health():
    return {"status": "ok", "service": "api"}
