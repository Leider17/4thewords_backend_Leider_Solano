from app.core.db import SessionLocal
from pydantic import ValidationError
from typing import Optional
from sqlmodel import select
from app.models.legend_model import Legend
from app.models.district_model import District
from app.models.canton_model import Canton
from app.models.province_model import Province
from app.schemas.legend_schema import LegendCreate, LegendUpdate
from fastapi import UploadFile 
from app.core.cloudinary_service import upload_image, delete_image

def get_all_legends(session: SessionLocal)-> list[Legend] | None:
    try:
        legends = session.exec(select(Legend)).all()
        return legends
    except Exception as e:
        return None

def get_legends_filters(session: SessionLocal, name: Optional[str] = None, category: Optional[str] = None,legend_date_initial: Optional[str] = None, legend_date_final: Optional[str] = None, province_id: Optional[int] = None, canton_id: Optional[int] = None, district_id: Optional[int] = None)-> list[Legend] | None:
    try:
        statement= select(Legend).join(District).join(Canton).join(Province)
        if name:
            statement = statement.where(Legend.name.ilike(f"%{name}%"))
        if category:    
            statement = statement.where(Legend.category.ilike(f"%{category}%"))
        if legend_date_initial:
            statement = statement.where(Legend.legend_date >= legend_date_initial)
        if legend_date_final:
            statement = statement.where(Legend.legend_date <= legend_date_final)
        if province_id:
            statement = statement.where(Province.id == province_id)
        if canton_id:
            statement = statement.where(Canton.id == canton_id)
        if district_id:
            statement = statement.where(District.id == district_id)
        legends = session.exec(statement).all()
        return legends
    except Exception as e:
        print(f"Error retrieving legends with filters: {e}")
        return None

def get_legend_by_id(legend_id: int, session: SessionLocal) -> Legend | None:
    
    try:
        legend=session.get(Legend, legend_id)
        return legend
    except Exception as e:
        return None
    
async def create_legend(legend_data: LegendCreate, session: SessionLocal, image_file:UploadFile=None) -> Legend | None:
    try:
        image_url= None
        if(image_file):
            image_url, public_id=await upload_image(image_file)
            print(f"Image URL: {image_url}")
            if not image_url:
                return None
        legend = Legend.model_validate(legend_data.model_dump())

        if image_url:
            legend.image_url = image_url
            legend.cloudinary_public_id= public_id
        print(f"Creating legend: {legend}")
        session.add(legend)
        session.commit()
        session.refresh(legend)
        return legend
    except ValidationError as e:
        print(f"Validation error: {e}")
        raise
    except Exception as e:
        print(f"Error creating legend: {e}")
        return None
    
async def update_legend(legend_id: int, legend_data: LegendUpdate, session: SessionLocal, image_file:UploadFile=None) -> Legend | None:
    
    try:
        legend= get_legend_by_id(legend_id, session)

        if legend is None:
            return None
        if image_file:
            if legend.cloudinary_public_id:
                delete=await delete_image(legend.cloudinary_public_id)
                if delete:
                    print(f"Image with public ID {legend.cloudinary_public_id} deleted successfully.")
                
            uploaded_data= await upload_image(image_file)
            if uploaded_data:
                legend.image_url, legend.cloudinary_public_id = uploaded_data
            else:
                return None
        elif legend_data.image_url is not None:
            legend.image_url = legend_data.image_url

        legend.title = legend_data.title
        legend.overview = legend_data.overview
        legend.year = legend_data.year
        legend.rating = legend_data.rating
        legend.category = legend_data.category

        session.commit()
        session.refresh(legend)
        return legend
    except ValidationError as e:
        print(f"Validation error: {e}")
        raise
    except Exception as e:
        return None
    
def delete_legend(legend_id: int, session: SessionLocal) -> bool:

    try:
        legend= get_legend_by_id(legend_id, session)
        if legend is None:
            return None
        if legend.cloudinary_public_id:
            try:
                deleted=delete_image(legend.cloudinary_public_id)
                if deleted:
                    print(f"Image with public ID {legend.cloudinary_public_id} deleted successfully.")
            except Exception as e:
                print(f"Error deleting image: {e}")

        session.delete(legend)
        session.commit()
        return True
    except Exception as e:
        return False