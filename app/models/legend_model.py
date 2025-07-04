
from sqlmodel import  Field
from typing import Optional
from datetime import datetime
from app.schemas.legend_schema import LegendBase
    
class Legend(LegendBase,table=True):
    __tablename__ = "legends"
    id: Optional[int] = Field(default=None, primary_key=True)
    

    