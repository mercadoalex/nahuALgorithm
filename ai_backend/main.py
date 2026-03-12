"""NahuALgorithm AI Backend — FastAPI service for generative Peyote AI."""

from fastapi import FastAPI
from ai_backend.routes.peyote import router as peyote_router

app = FastAPI(
    title="NahuALgorithm AI Backend",
    description="Generative AI service for the Peyote AI system.",
    version="0.1.0",
)

app.include_router(peyote_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
