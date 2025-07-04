from fastapi import APIRouter, HTTPException, status
from app.core.db import SessionLocal
from app.models.canton_model import Canton
from app.services.canton_service import get_cantons_by_province

router= APIRouter(
    prefix="/cantons",
    tags=["Cantons"] 
)

@router.get("/province/{province_id}",response_model=list[Canton])
async def get_cantons_route(province_id: int, session: SessionLocal = SessionLocal):
    cantons= get_cantons_by_province(session, province_id)
    if cantons is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving cantons from the database."
        )
    return cantons