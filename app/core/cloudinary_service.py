from decouple import config 
import cloudinary
import cloudinary.uploader
import cloudinary.api
from fastapi import UploadFile
from typing import Optional


cloudinary.config(
    cloud_name=config("CLOUDINARY_CLOUD_NAME"),
    api_key=config("CLOUDINARY_API_KEY"),
    api_secret=config("CLOUDINARY_API_SECRET"),
)


async def upload_image(file: UploadFile)->Optional[str]:
    try:
        contents=await file.read()
        upload_result=cloudinary.uploader.upload(contents, folder="legendsImages")

        return upload_result.get("secure_url"), upload_result.get("public_id")
    except Exception as e:
        print(f"Error uploading image: {e}")
        return None;

async def delete_image(public_id: str) -> bool:
    try:
        result = cloudinary.uploader.destroy(public_id)
        print(f"Delete result: {result}")
        return True
    except Exception as e:
        return False