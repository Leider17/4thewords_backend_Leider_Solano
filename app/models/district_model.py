from sqlmodel import Field
from app.schemas.district_schema import DistrictBase
from typing import Optional

class District(DistrictBase,table=True):
    __tablename__ = "districts"
    id: int = Field(default=None, primary_key=True)
    

   