from app.schemas.category_schema import CategoryBase
from sqlmodel import Field, Relationship
from typing import List





class Category(CategoryBase, table=True):
    __tablename__ = "categories"
    id: int = Field(default=None, primary_key=True)

    legends: List["Legend"] = Relationship(back_populates="category")

    
