from fastapi import APIRouter, HTTPException, status
from app.core.db import SessionLocal
from app.models.category_model import Category
from app.services.category_service import get_all_categories

router= APIRouter(
    prefix="/categories",
    tags=["Categories"])


@router.get("", response_model=list[Category])
async def get_categories_route(session: SessionLocal = SessionLocal):
    categories= get_all_categories(session)
    if categories is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving categories from the database."
        )
    return categories