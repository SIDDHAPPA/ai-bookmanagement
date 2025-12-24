from fastapi import APIRouter
from app.services.llm_client import generate_summary

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

@router.get("/")
async def recommend(preferences: str):
    return {
        "recommendations": await generate_summary(
            f"Recommend books based on: {preferences}"
        )
    }
