from app.core.db import SessionLocal
from typing import Optional
from sqlmodel import select
from app.models.canton_model import Canton

def get_cantons_by_province(session: SessionLocal, province_id: Optional[int]=None)-> list[Canton] | None:
    try:
        statement = select(Canton)
        if province_id:
            statement = statement.where(Canton.province_id == province_id)
        else:
            statement = select(Canton)
        cantons = session.exec(statement).all()
        return cantons
    except Exception as e:
        return None
    
