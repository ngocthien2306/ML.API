from fastapi import APIRouter, Response, status
from fastapi.responses import JSONResponse
from starlette.responses import StreamingResponse
from PIL import Image
from io import BytesIO
from app.file.schemas.file import (
    GetPictureResponse, 
    ExceptionPictureResponse
)
import os
file_router = APIRouter()
print("Wellcome to file controller")
@file_router.get(
    "/picture",
    response_model_exclude={"image_path"},
    response_model= GetPictureResponse,
    responses={"400": {"model": ExceptionPictureResponse}},
    )
async def get_picture(image_path: str):
    try:
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        image_files = []
        print(image_path)
        for dirpath, _, filenames in os.walk("/data/thinhlv/thiennn/deeplearning/ML.API/public/images"):
            for file in filenames:
                _, extension = os.path.splitext(file)
                if extension.lower() in image_extensions:
                    image_files.append(os.path.join(dirpath, file))
        print(image_files)  
        found_paths = list(filter(lambda path: image_path in path, image_files))
        if len(found_paths) == 0: 
            return ExceptionPictureResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'status': "SERVER_ERROR_NOT_FOUND_IMAGE", 'message' : "Not found image" }
            )
            
        image = Image.open(found_paths)
        
        img_byte_arr = BytesIO()
    
        image.save(img_byte_arr, format="PNG")

        img_byte_arr.seek(0)

        return GetPictureResponse(content=img_byte_arr, media_type="image/png")
    except Exception as e:
        return ExceptionPictureResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )