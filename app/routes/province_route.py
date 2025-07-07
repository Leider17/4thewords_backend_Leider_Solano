from fastapi import APIRouter, HTTPException, status, Depends
from app.core.db import SessionLocal
from app.models.province_model import Province
from app.services.province_service import get_all_provinces
from app.core.auth import get_current_user
from app.schemas.user_schema import UserBase

router= APIRouter(
    prefix="/provinces",
    tags=["Provinces"] 
)

@router.get("",response_model=list[Province])
async def get_provinces_route(session: SessionLocal = SessionLocal, current_user: UserBase = Depends(get_current_user),):
    """
    Obtiene todas las provincias

    Args:
        como parametro recibe la session de la base de datos.

    Returns:
        una lista de provincias, en caso de fallar devuelve un status 500.
    """
    provinces= get_all_provinces(session)
    if provinces is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving provinces from the database."
        )
    return provinces