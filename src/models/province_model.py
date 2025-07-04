from sqlmodel import Field
from schemas.province_schema import ProvinceBase
from typing import Optional

class Province(ProvinceBase,table=True):
    __tablename__ = "provinces"
    id: int = Field(default=None, primary_key=True)
    
   