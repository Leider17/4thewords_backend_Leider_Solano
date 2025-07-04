from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional
from sqlmodel import Session
from app.core.db import get_session
from app.models.canton_model import Canton
from app.services.canton_service import get_cantons_by_province

router= APIRouter(
    prefix="/cantons",
    tags=["Cantons"] 
)

@router.get("",response_model=list[Canton])
async def get_cantons_route(province_id: Optional[int]=None, session: Session = Depends(get_session)):
    cantons= get_cantons_by_province(session, province_id)
    if cantons is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving cantons from the database."
        )
    return cantons