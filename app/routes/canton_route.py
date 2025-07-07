from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional
from sqlmodel import Session
from app.core.db import get_session
from app.models.canton_model import Canton
from app.services.canton_service import get_cantons_by_province
from app.core.auth import get_current_user
from app.schemas.user_schema import UserBase

router= APIRouter(
    prefix="/cantons",
    tags=["Cantons"] 
)

@router.get("",response_model=list[Canton])
async def get_cantons_route(province_id: Optional[int]=None, session: Session = Depends(get_session), current_user: UserBase = Depends(get_current_user),):
    """
    Obtiene los cantones, opcionalmente filtrados por provincia

    Args:
        como parametros recibe el id de la provincia y la session de la base de datos.

    Returns:
        una lista de cantones, en caso de fallar devuelve un status 500.
    """
    cantons= get_cantons_by_province(session, province_id)
    if cantons is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving cantons from the database."
        )
    return cantons