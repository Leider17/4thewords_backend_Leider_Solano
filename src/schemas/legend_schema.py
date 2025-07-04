
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class LegendBase(SQLModel):
    
    name: str = Field(min_length=5, max_length=100)
    description: str = Field(min_length=3, max_length=100)
    category_id: int = Field(default=None, foreign_key="categories.id")
    legend_date: datetime
    image_url: Optional[str] = None 
    cloudinary_public_id: Optional[str] = Field(default=None)
    district_id: int = Field(default=None, foreign_key="districts.id")

class LegendCreate(LegendBase):
    pass

class LegendUpdate(LegendBase):
    pass