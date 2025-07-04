from app.core.db import SessionLocal
from sqlmodel import select
from app.models.category_model import Category

def get_all_categories(session: SessionLocal)-> list[Category] | None:
    try:
        categories = session.exec(select(Category)).all()
        return categories
    except Exception as e:
        print(f"Error retrieving categories: {e}")
        return None