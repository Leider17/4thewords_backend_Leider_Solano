from app.core.db import SessionLocal
from sqlmodel import select
from app.models.province_model import Province

def get_all_provinces(session: SessionLocal)-> list[Province] | None:
    try:
        provinces = session.exec(select(Province)).all()
        return provinces
    except Exception as e:
        print(f"Error retrieving provinces: {e}")
        return None