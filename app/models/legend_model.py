
from sqlmodel import  Field, Relationship
from app.models.category_model import Category
from app.models.district_model import District
from typing import Optional
from app.schemas.legend_schema import LegendBase
    
class Legend(LegendBase,table=True):
    __tablename__ = "legends"
    id: Optional[int] = Field(default=None, primary_key=True)
    
    category: Optional[Category] = Relationship(back_populates="legends")
    district: Optional[District] = Relationship(back_populates="legends")
    
class LegendRead(LegendBase):
    id: int
    category_name: str
    district_id: int
    district_name: str
    canton_id: int
    canton_name: str
    province_id: int
    province_name: str