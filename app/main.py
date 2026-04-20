from fastapi import FastAPI
from app.api.routes.analyze import router as analyze_router

app = FastAPI(title="Phishing Reverse Hunter")

app.include_router(analyze_router, prefix="/api")
