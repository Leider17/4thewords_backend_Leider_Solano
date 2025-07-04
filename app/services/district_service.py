from app.core.db import SessionLocal
from sqlmodel import select
from typing import Optional
from app.models.district_model import District
from app.models.canton_model import Canton

def get_districts(session: SessionLocal, canton_id: Optional[int] = None, province_id: Optional[int] = None)-> list[District] | None:
    try:
        if canton_id:
            statement = select(District).where(District.canton_id == canton_id)
        elif province_id:
            statement = select(District).join(Canton).where(Canton.province_id == province_id)
        else:
            statement = select(District)
        districts = session.exec(statement).all()
        return districts
    except Exception as e:
        return None
    

