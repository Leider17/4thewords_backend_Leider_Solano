from fastapi import APIRouter, HTTPException, status, File, UploadFile, Form,Depends
from typing import Optional
from datetime import datetime
from app.core.db import SessionLocal
from app.models.legend_model import LegendRead, Legend
from app.schemas.legend_schema import LegendCreate, LegendUpdate
from app.services.legend_service import (
    get_all_legends,
    get_legends_filters,
    get_legend,
    create_legend,
    update_legend,
    delete_legend
)
from pydantic import ValidationError
from app.core.auth import get_current_user
from app.schemas.user_schema import UserBase

router= APIRouter(
    prefix="/legends",
    tags=["Legends"] 
)

@router.get("", response_model=list[LegendRead])
async def get_legends_route(session: SessionLocal = SessionLocal,current_user: UserBase = Depends(get_current_user)):
    """
    Obtiene todas las leyendas

    Args:
        como parametro recibe la session de la base de datos.

    Returns:
        una lista de leyendas, formateadas mediante LegendRead, en caso de fallar devuelve un status 500.
    """
    legends= get_all_legends(session)
    if legends is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving legends from the database."
        )
    return legends

@router.get("/filters", response_model=list[LegendRead])

async def get_legends_filters_route(
    name: Optional[str] = None,
    category_id: Optional[int] = None,
    legend_date_initial: Optional[str] = None, 
    legend_date_final: Optional[str] = None,
    province_id: Optional[int] = None,
    canton_id: Optional[int] = None,
    district_id: Optional[int] = None,
    session: SessionLocal = SessionLocal,
    current_user: UserBase = Depends(get_current_user)
    
):
    """
    Obtiene las leyendas a partir de los diferentes filtros

    Args:
        como parametros recibe los filtros y la session de la base de datos.

    Returns:
        una lista de leyendas filtradas mediante los filtros y formateadas mediante LegendRead, en caso de fallar devuelve un status 500.
    """
    legends = get_legends_filters(
        session, 
        name=name, 
        category_id=category_id, 
        legend_date_initial=legend_date_initial, 
        legend_date_final=legend_date_final,
        province_id=province_id, 
        canton_id=canton_id, 
        district_id=district_id
    )
    if legends is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving legends with filters from the database."
        )
    return legends

@router.get("/{legend_id}", response_model=LegendRead)
async def get_legend_route(legend_id: int, session: SessionLocal = SessionLocal,current_user: UserBase = Depends(get_current_user)):
    """
    Obtiene una leyenda especifica

    Args:
        como parametro recibe el id de la leyenda y la session de la base de datos, en caso de fallar devuelve un status 404.

    Returns:
        una leyenda formateada mediante LegendRead.
    """
    legend= get_legend(legend_id, session)
    if legend is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Legend with ID {legend_id} not found."
        )
    return legend


@router.post("", response_model=Legend, status_code=status.HTTP_201_CREATED)
async def create_legend_route(          
    name: str = Form(...),
    description: str = Form(...),
    category_id: int = Form(...),
    legend_date: datetime = Form(...),
    district_id: int = Form(...),
    image_file: Optional[UploadFile] = File(None), 
    current_user: UserBase = Depends(get_current_user),
    session: SessionLocal = SessionLocal):
    """
    Crea una leyenda

    Args:
        como parametros recibe los datos de la leyenda y la session de la base de datos, en caso de fallar devuelve un status 422 o 500.

    Returns:
        la informacion de la leyenda creada.
    """
    try:
        legend_data= LegendCreate(
            name=name,
            description=description,
            category_id=category_id,
            legend_date=legend_date,
            district_id=district_id
        )
        legend=await create_legend(legend_data, session, image_file)
        if legend is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating legend."
            )
        return legend
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Validation error: " + str(e.errors())
            
        )
        
    
@router.patch("/{legend_id}", response_model=Legend)
async def update_legend_route(legend_id: int, 
    current_user: UserBase = Depends(get_current_user),
    name: str = Form(...),
    description: str = Form(...),
    category_id: int = Form(...),
    legend_date: datetime = Form(...),
    district_id: int = Form(...),
    image_file: Optional[UploadFile] = File(None), 
    session: SessionLocal = SessionLocal):
    """
    Actualiza una leyenda

    Args:
        como parametros recibe el id de la leyenda, los datos de la leyenda y la session de la base de datos.

    Returns:
        la informacion de la leyenda actualizada, en caso de fallar devuelve un status 422 o 404.
    """
    try:
        legend_data= LegendUpdate(
            name=name,
            description=description,
            category_id=category_id,
            legend_date=legend_date,
            district_id=district_id
        )

        legend=await update_legend(legend_id, legend_data, session, image_file)
        if legend is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Legend with ID {legend_id} not found."
            )
        return legend
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Validation error: " + str(e.errors())
        )
    
@router.delete("/{legend_id}", status_code=status.HTTP_200_OK)
async def delete_legend_route(legend_id: int, session: SessionLocal = SessionLocal, current_user: UserBase = Depends(get_current_user)):
    """
    Elimina una leyenda

    Args:
        como parametro recibe el id de la leyenda y la session de la base de datos.

    Returns:
        un status 200, en caso de fallar devuelve un status 404 o 500.
    """
    try:
        result = delete_legend(legend_id, session)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Legend with ID {legend_id} not found."
            )
        return {"detail": "Legend deleted successfully."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting legend"
        )

