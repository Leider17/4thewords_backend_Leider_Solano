from sqlmodel import Field, Relationship
from app.schemas.province_schema import ProvinceBase
from typing import List

class Province(ProvinceBase,table=True):
    __tablename__ = "provinces"
    id: int = Field(default=None, primary_key=True)
    
    cantons: List["Canton"] = Relationship(back_populates="province")