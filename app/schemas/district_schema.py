
from sqlmodel import SQLModel, Field


class DistrictBase(SQLModel):
    
    name: str = Field(min_length=5, max_length=40)
    canton_id: int= Field(default=None, foreign_key="cantons.id")
    

