from app.core.db import SessionLocal
from pydantic import ValidationError
from typing import Optional, List
from sqlmodel import select
from app.models.legend_model import Legend, LegendRead
from app.models.district_model import District
from app.models.canton_model import Canton
from app.models.category_model import Category
from app.models.province_model import Province
from app.schemas.legend_schema import LegendCreate, LegendUpdate
from fastapi import UploadFile 
from app.core.cloudinary_service import upload_image, delete_image
from datetime import date
from sqlalchemy.orm import Session, selectinload

def get_all_legends(session: SessionLocal)-> list[LegendRead] | None:
    """
    Recupera todas las leyendas de la base de datos, incluyendo el nombre de la categoría, el nombre del distrito, el nombre del canton
    y el nombre de la provincia con sus respectivos ids.

    Args:
        session: La sesión de la base de datos.

    Returns:
        Una lista de leyendas formateadas mediante LegendRead.
    """
    try:
        statement = select(Legend).join(Category).join(District).join(Canton).join(Province)
        legends = session.exec(statement).all()
        results = [
            LegendRead(
                id=legend.id,
                name=legend.name,
                category_id=legend.category_id,
                description=legend.description,
                legend_date=legend.legend_date,
                image_url=legend.image_url,
                cloudinary_public_id=legend.cloudinary_public_id,
                district_id=legend.district_id,
                category_name=legend.category.name,
                district_name=legend.district.name,
                canton_id=legend.district.canton.id,
                canton_name=legend.district.canton.name,
                province_id=legend.district.canton.province.id,
                province_name=legend.district.canton.province.name

            )
            for legend in legends
        ]
        
   
        return results
    except Exception as e:
        print(f"Error retrieving legends: {e}")
        return None

def get_legends_filters(
    session: Session,
    name: Optional[str] = None,
    category_id: Optional[int] = None,
    legend_date_initial: Optional[date] = None, 
    legend_date_final: Optional[date] = None,   
    province_id: Optional[int] = None,
    canton_id: Optional[int] = None,
    district_id: Optional[int] = None,
) -> List[LegendRead] | None:
    """
    Recupera las leyendas filtradas de la base de datos, incluyendo el nombre de la categoría, el nombre del distrito, el nombre del canton
    y el nombre de la provincia con sus respectivos ids.

    Args:
        session: La sesión de la base de datos.

    Returns:
        Una lista de leyendas formateadas mediante LegendRead.
    """
    try:
        statement = (select(Legend).join(Category).join(District).join(Canton).join(Province ))

        if name:
            statement = statement.where(Legend.name.ilike(f"%{name}%"))
        if category_id:
            statement = statement.where(Legend.category_id == category_id)
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
        results = [
            LegendRead(
                id=legend.id,
                name=legend.name,
                category_id=legend.category_id,
                description=legend.description,
                legend_date=legend.legend_date,
                image_url=legend.image_url,
                cloudinary_public_id=legend.cloudinary_public_id,
                district_id=legend.district_id,
                category_name=legend.category.name,
                district_name=legend.district.name,
                canton_id=legend.district.canton.id,
                canton_name=legend.district.canton.name,
                province_id=legend.district.canton.province.id,
                province_name=legend.district.canton.province.name

            )
            for legend in legends
        ]
        
   
        return results
    except Exception as e:
        print(f"Error al recuperar leyendas con filtros: {e}")
        return None

def get_legend_by_id(legend_id: int, session: SessionLocal) -> Legend | None:
    """
    Recupera una leyenda por su ID de la base de datos, incluyendo solo información de la leyenda.
    Args:
        session: La sesión de la base de datos.
        legend_id: El ID de la leyenda a recuperar.

    Returns:
        la información de la leyenda.
    """
    try:
        legend=session.get(Legend, legend_id)
        return legend
    except Exception as e:
        return None

def get_legend(legend_id: int, session: SessionLocal)-> LegendRead| None:
    """
    Recupera una leyenda por su ID de la base de datos, incluyendo el nombre de la categoría, el nombre del distrito, el nombre del canton
    y el nombre de la provincia con sus respectivos ids.
    Args:
        session: La sesión de la base de datos.
        legend_id: El ID de la leyenda a recuperar.

    Returns:
        Una leyenda formateada mediante LegendRead.
    """
    try:
        statement = select(Legend).join(Category).join(District).join(Canton).join(Province).where(Legend.id == legend_id)
        legend = session.exec(statement).one()
        result = LegendRead(
                id=legend.id,
                name=legend.name,
                category_id=legend.category_id,
                description=legend.description,
                legend_date=legend.legend_date,
                image_url=legend.image_url,
                cloudinary_public_id=legend.cloudinary_public_id,
                district_id=legend.district_id,
                category_name=legend.category.name,
                district_name=legend.district.name,
                canton_id=legend.district.canton.id,
                canton_name=legend.district.canton.name,
                province_id=legend.district.canton.province.id,
                province_name=legend.district.canton.province.name
            )
            
            
        
        return result
    except Exception as e:
        print(f"Error retrieving legends: {e}")
        return None

    
async def create_legend(legend_data: LegendCreate, session: SessionLocal, image_file:UploadFile=None) -> Legend | None:
    """
    crea una leyenda en la base de datos, además de cargar la imagen en el servicio de cloudinary.
    Args:
        session: La sesión de la base de datos.
        legend_data: Los datos de la leyenda a crear.
        image_file: La imagen de la leyenda.

    Returns:
        la información de la leyenda creada.
    """
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
    """
    Actualiza una leyenda en la base de datos, incluyendo la actualización de la imagen en el servicio de cloudinary.
    Args:
        legend_id: El ID de la leyenda a actualizar.
        session: La sesión de la base de datos.
        legend_data: Los datos de la leyenda a crear.+
        image_file: La imagen de la leyenda.

    Returns:
        la información de la leyenda actualizada.
    """
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

        legend.name = legend_data.name
        legend.description = legend_data.description
        legend.category_id = legend_data.category_id 
        legend.legend_date = legend_data.legend_date 
        legend.district_id = legend_data.district_id 

        session.commit()
        session.refresh(legend)
        return legend
    except ValidationError as e:
        print(f"Validation error: {e}")
        raise
    except Exception as e:
        return None
    
def delete_legend(legend_id: int, session: SessionLocal) -> bool:
    """
    Elimina una leyenda de la base de datos, incluyendo la eliminación de la imagen en el servicio de cloudinary.
    Args:
        session: La sesión de la base de datos.
        legend_id: El ID de la leyenda a eliminar.

    Returns:
        True si la leyenda se eliminó correctamente, False en caso contrario.
    """
    try:
        legend= get_legend_by_id(legend_id, session)
        print(f"Deleting legend: {legend}" )
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