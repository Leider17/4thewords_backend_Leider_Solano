from fastapi import APIRouter, HTTPException, status, File, UploadFile, Form
from typing import Optional
from datetime import datetime
from app.core.db import SessionLocal
from app.models.legend_model import Legend
from app.schemas.legend_schema import LegendCreate, LegendUpdate
from app.services.legend_service import (
    get_all_legends,
    get_legends_filters,
    get_legend_by_id,
    create_legend,
    update_legend,
    delete_legend
)
from pydantic import ValidationError

router= APIRouter(
    prefix="/legends",
    tags=["Legends"] 
)

@router.get("",response_model=list[Legend])
async def get_legends_route(session: SessionLocal = SessionLocal):
    legends= get_all_legends(session)
    if legends is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving legends from the database."
        )
    return legends

@router.get("/filters", response_model=list[Legend])
async def get_legends_filters_route(
    name: Optional[str] = None,
    category: Optional[str] = None,
    legend_date: Optional[str] = None,
    province_id: Optional[int] = None,
    canton_id: Optional[int] = None,
    district_id: Optional[int] = None,
    session: SessionLocal = SessionLocal
):
    legends = get_legends_filters(
        session, 
        name=name, 
        category=category, 
        legend_date=legend_date, 
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

@router.get("/{legend_id}", response_model=Legend)
async def get_legend_route(legend_id: int, session: SessionLocal = SessionLocal):
    legend= get_legend_by_id(legend_id, session)
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
    category: str = Form(...),
    legend_date: datetime = Form(...),
    district_id: int = Form(...),
    image_file: Optional[UploadFile] = File(None), 
    session: SessionLocal = SessionLocal):
    try:
        legend_data= LegendCreate(
            name=name,
            description=description,
            category=category,
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
            detail=e.errors()
        )
    
@router.patch("/{legend_id}", response_model=Legend)
async def update_legend_route(legend_id: int, 
    name: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    legend_date: datetime = Form(...),
    district_id: int = Form(...),
    image_file: Optional[UploadFile] = File(None), 
    session: SessionLocal = SessionLocal):
    try:
        legend_data= LegendUpdate(
            name=name,
            description=description,
            category=category,
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
async def delete_legend_route(legend_id: int, session: SessionLocal = SessionLocal):
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

