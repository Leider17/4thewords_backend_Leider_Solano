
from sqlmodel import SQLModel, Field


class CategoryBase(SQLModel):
    
    name: str = Field(min_length=5, max_length=15)
    

