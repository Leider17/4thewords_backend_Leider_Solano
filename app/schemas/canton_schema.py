
from sqlmodel import SQLModel, Field


class CantonBase(SQLModel):
    
    name: str = Field(min_length=5, max_length=40)
    province_id: int = Field(foreign_key="provinces.id")
    

