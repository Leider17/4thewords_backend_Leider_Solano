from schemas.category_schema import CategoryBase
from sqlmodel import Field


class Category(CategoryBase, table=True):
    __tablename__ = "categories"
    id: int = Field(default=None, primary_key=True)
    