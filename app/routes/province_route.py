from fastapi import APIRouter, HTTPException, status
from app.core.db import SessionLocal
from app.models.province_model import Province
from app.services.province_service import get_all_provinces

router= APIRouter(
    prefix="/provinces",
    tags=["Provinces"] 
)

@router.get("",response_model=list[Province])
async def get_provinces_route(session: SessionLocal = SessionLocal):
    provinces= get_all_provinces(session)
    if provinces is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving provinces from the database."
        )
    return provinces