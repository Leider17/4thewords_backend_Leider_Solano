from sqlmodel import Field
from app.schemas.canton_schema import CantonBase
from typing import Optional

class Canton(CantonBase,table=True):
    __tablename__ = "cantons"
    id: int = Field(default=None, primary_key=True)
    

