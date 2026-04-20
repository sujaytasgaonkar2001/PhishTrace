from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from app.services.url_analyzer import analyze_url

router = APIRouter()


class AnalyzeRequest(BaseModel):
    url: HttpUrl


@router.post("/analyze-url")
async def analyze(request: AnalyzeRequest):
    try:
        url = str(request.url)  # ✅ FIX

        result = await analyze_url(url)

        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))