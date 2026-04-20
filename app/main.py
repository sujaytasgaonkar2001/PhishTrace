from fastapi import FastAPI
from app.api.routes.analyze import router as analyze_router
from app.services.reputation_service import load_tranco

app = FastAPI(title="Phishing Reverse Hunter")  # ✅ define FIRST


@app.on_event("startup")
def startup_event():
    load_tranco()


@app.get("/")
def root():
    return {"message": "Phishing Reverse Hunter API is running"}


app.include_router(analyze_router, prefix="/api")