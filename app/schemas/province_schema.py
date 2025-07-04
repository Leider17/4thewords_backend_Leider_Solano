
from sqlmodel import SQLModel, Field


class ProvinceBase(SQLModel):
    
    name: str = Field(min_length=5, max_length=20)
    

