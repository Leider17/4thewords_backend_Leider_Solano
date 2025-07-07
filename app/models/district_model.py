from sqlmodel import Field, Relationship
from app.schemas.district_schema import DistrictBase
from app.models.canton_model import Canton
from typing import List, Optional

class District(DistrictBase,table=True):
    __tablename__ = "districts"
    id: int = Field(default=None, primary_key=True)
    
    legends: List["Legend"] = Relationship(back_populates="district")
    canton: Optional[Canton] = Relationship(back_populates="districts")