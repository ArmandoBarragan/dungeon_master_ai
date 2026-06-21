from fastapi import APIRouter, HTTPException

from config.db import check_connection

router = APIRouter()


@router.get("/health/")
async def health():
    try:
        check_connection()
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Database unavailable: {exc}") from exc
    return {"status": "ok"}
