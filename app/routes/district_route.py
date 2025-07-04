from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional
from sqlmodel import Session
from app.core.db import get_session
from app.models.district_model import District
from app.services.district_service import get_districts

router= APIRouter(
    prefix="/districts",
    tags=["Districts"] 
)

@router.get("/",response_model=list[District])
async def get_districts_route(canton_id: Optional[int]=None,province_id: Optional[int]=None, session: Session= Depends(get_session)):
    districts= get_districts(session, canton_id, province_id)
    if districts is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving districts from the database."
        )
    return districts