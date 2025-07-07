from sqlmodel import Field, Relationship
from app.schemas.canton_schema import CantonBase
from app.models.province_model import Province
from typing import Optional, List

class Canton(CantonBase,table=True):
    __tablename__ = "cantons"
    id: int = Field(default=None, primary_key=True)
    
    districts: List["District"] = Relationship(back_populates="canton")
    province: Optional[Province] = Relationship(back_populates="cantons")
