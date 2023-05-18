from fastapi import APIRouter, Response, status
from fastapi.responses import JSONResponse, FileResponse
from starlette.responses import StreamingResponse
from PIL import Image
from io import BytesIO
from app.file.schemas.file import (
    GetPictureResponse, 
    ExceptionPictureResponse
)
import os
FOLDER_IMAGE = '/data/thinhlv/hung/Capstone/ML.API/public/images/'

file_router = APIRouter()
print("Wellcome to file controller")
@file_router.get(
    "/picture",
    response_model_exclude={"image_path"},
    responses={"400": {"model": ExceptionPictureResponse}},
)
async def get_picture(image_path: str):
    try:
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        image_files = []

        for dirpath, _, filenames in os.walk(FOLDER_IMAGE):
            for file in filenames:
                _, extension = os.path.splitext(file)
                if extension.lower() in image_extensions:
                    image_files.append(os.path.join(dirpath, file))

        found_paths = list(filter(lambda path: image_path in path, image_files))
        if len(found_paths) == 0:
            return ExceptionPictureResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={'status': "SERVER_ERROR_NOT_FOUND_IMAGE", 'message': "Not found image"}
            )

        print(found_paths)
        
        # If multiple images with the same name are found, choose the first one
        return FileResponse(found_paths[0], media_type="image/jpeg")
    except Exception as e:
        return ExceptionPictureResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={'status': "SERVER_ERROR", 'message': str(e)}
        )