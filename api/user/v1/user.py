import tempfile
import zipfile
from typing import List
import base64
import numpy as np
import cv2
import io
from PIL import Image
from os.path import isdir
import os
import shutil
from pathlib import Path
import  traceback
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Query, UploadFile,File
from fastapi.responses import JSONResponse, FileResponse
from api.user.v1.request.user import LoginRequest, RegisterIdVietNamRequest, VerifyIdVietNameRequest, \
    VerifylicensePlateRequest, RegisterUserFaceRequest, CheckFaceUserFolderRequest, DeleteUserFolderRequest
from api.user.v1.response.user import LoginResponse, ResgisterIdVietNamResponse, VerifylIdVietNamResponse, \
    VerifylicensePlateResponse, RegisterUserFaceResponse, CheckFaceUserFolder, DeleteUserFolderResponse
from app.user.schemas import (
    ExceptionResponseSchema,
    GetUserListResponseSchema,
    CreateUserRequestSchema,
    CreateUserResponseSchema,
)
from app.user.services import UserService
from core.fastapi.dependencies import (
    PermissionDependency,
    IsAdmin,
    AllowAll
)
load_dotenv()
user_router = APIRouter()
#TARGET = "./public/images/"
TARGET = os.getenv("TARGET")
print(TARGET)
@user_router.get(
    "",
    response_model=List[GetUserListResponseSchema],
    response_model_exclude={"id"},
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
async def get_user_list(
    limit: int = Query(10, description="Limit"),
    prev: int = Query(None, description="Prev ID"),
):
    return await UserService().get_user_list(limit=limit, prev=prev)


@user_router.post(
    "",
    response_model=CreateUserResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def create_user(request: CreateUserRequestSchema):
    await UserService().create_user(**request.dict())
    return {"email": request.email, "nickname": request.nickname}


@user_router.post(
    "/login",
    response_model=LoginResponse,
    responses={"404": {"model": ExceptionResponseSchema}},
)
async def login(request: LoginRequest):
    token = await UserService().login(email=request.email, password=request.password)
    return {"token": token.token, "refresh_token": token.refresh_token}
@user_router.post(
    "/verifylicenseplates",
    response_model=VerifylicensePlateResponse,
    responses={"404": {"model": ExceptionResponseSchema}},
)
async def verify(request: VerifylicensePlateRequest):
    if not request.stringlp or request.stringlp == "": 
            return {"license": "Not Found"} ## ExceptionTrack
    try:
        # Convert string to Image

        #np_data = np.fromstring(decoded_data, np.uint8)
        #image = cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)
        decoded_data = base64.b64decode(request.stringlp)
        
        # Lp returned to LP Dictionary so Check accuracy here
        lp = await UserService().verify_lp(imagelp=decoded_data)
        
        return {"license": str(lp)}
    except Exception as e:
        print(str(e))
        return JSONResponse(content={"error": str(e)}, status_code=400)
@user_router.post(
    "/verifyidvn",
    response_model=VerifylIdVietNamResponse,
    responses={"404": {"model": ExceptionResponseSchema}},
)    
async def verify(request: VerifyIdVietNameRequest):
    if not request.stringidvn or request.stringidvn == "": 
            return {"id": "Not Found"} ## ExceptionTrack
    try:
        # Convert string to Image
        decoded_data = base64.b64decode(request.stringidvn)
        # np_data = np.fromstring(decoded_data, np.uint8)
        # image = cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)
        # image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
        image_io = io.BytesIO(decoded_data)
        image = Image.open(image_io)
        img = np.asarray(image)
        result = await UserService().verify_id(imageId=img)
        return {"id": str(result)}
    except Exception as e:
        print(str(e))
        return JSONResponse(content={"error": str(e)}, status_code=400)
    
@user_router.post(
    "/verifyidvn2"
)    
async def verify(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "Image must be jpg or png format!"

    
    try:
        image = UserService().read_image_file(await file.read())
        img = np.asarray(image)
        result = await UserService().verify_id(imageId=img)
        return {"id": str(result)}
    except Exception as e:
        print(str(e))
        return JSONResponse(content={"error": str(e)}, status_code=400)
@user_router.post(
    "/registerCCCD",
    response_model=ResgisterIdVietNamResponse,
    responses={"404": {"model": ExceptionResponseSchema}},
)    
async def registerCCCD(request: RegisterIdVietNamRequest):
    if not request.BirthDay or request.BirthDay == "" or not request.FullName or request.FullName =="" or not request.Gender  or request.Gender == "" or not request.Cccd or len(request.Cccd) != 12: 
            return JSONResponse(content={"error": "Null Data"}, status_code=400)
    try:
        # Convert string to Image
        decoded_data = base64.b64decode(request.Stringidvn)
        np_data = np.fromstring(decoded_data, np.uint8)
        imageid = cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)
        imageid = cv2.cvtColor(imageid, cv2.COLOR_RGBA2RGB)
        
        decoded_data = base64.b64decode(request.PictureFace)
        np_data = np.fromstring(decoded_data, np.uint8)
        imageface = cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)
        imageface = cv2.cvtColor(imageface, cv2.COLOR_RGBA2RGB)
        result = await UserService().register_user(cccd=request.Cccd, fullname=request.FullName,Gender = request.Gender,imageId=imageid,imageFace=imageface )
        return {"result": result}
    except Exception as e:
        print(str(e))
        return JSONResponse(content={"error": str(e)}, status_code=400)
@user_router.post(
    "/registerIdentity",
    response_model=VerifylIdVietNamResponse,
    responses={"404": {"model": ExceptionResponseSchema}},
)    
async def verifyId(request: VerifyIdVietNameRequest):
    if not request.stringidvn or request.stringidvn == "": 
            return {"id": "Not Found"} ## ExceptionTrack
    try:
        # Convert string to Image
        decoded_data = base64.b64decode(request.stringidvn)
        # np_data = np.fromstring(decoded_data, np.uint8)
        # image = cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)
        # image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
        image_io = io.BytesIO(decoded_data)
        image = Image.open(image_io)
        img = np.asarray(image)
        result = await UserService().verify_idImage(imageId=img)
        return {"id": str(result)}
    except Exception as e:
        print(str(e))
        return JSONResponse(content={"error": str(e)}, status_code=400)


@user_router.post(
    "/registerimageuser",
    response_model=RegisterUserFaceResponse,
    responses={"404": {"model": ExceptionResponseSchema}},
)
async def registerImageUser(request: RegisterUserFaceRequest):
    if not request.userid or request.userid == "":
        return {"id": "Not Found"}  ## ExceptionTrack
    try:
        print(request.userid)
        # Convert string to Image
        decoded_data = base64.b64decode(request.face)
        # np_data = np.fromstring(decoded_data, np.uint8)
        # image = cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)
        # image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
        image_io = io.BytesIO(decoded_data)
        image = Image.open(image_io)
        img = np.asarray(image)

        # Save Image
        path_img_detected = TARGET +"users/"+ str(request.userid) + "/face/"
        if not isdir(path_img_detected):
            os.makedirs(path_img_detected)
        lpImage_path = path_img_detected + "/face_{}.jpg".format(request.userid)
        cv2.imwrite(lpImage_path, img)

        file_paths = Path(path_img_detected).glob("*")
        files = [UploadFile(filename=file_path.name, file=open(file_path, "rb")) for file_path in file_paths]
        await UserService().send_Image_To_Client(request.userid,files)
        return {"result": str(request.userid)}
    except Exception as e:
        print(str(e))
        traceback.print_exc()
        return JSONResponse(content={"error": str(e)}, status_code=400)
@user_router.post(
    "/test",
    response_model=RegisterUserFaceResponse,
    responses={"404": {"model": ExceptionResponseSchema}},
)
async def registerImageUser():

    try:
        image_files = []
        path = "D:\\CAPSTONE2023\\ML.API\\public\\images\\users\\20230715114204\\face"
        file_paths = Path(path).glob("*")
        files = [UploadFile(filename=file_path.name, file=open(file_path, "rb")) for file_path in file_paths]
        await UserService().send_Image_To_Client("123id",files)
        return {"result": "0"}
    except Exception as e:
        print(str(e))
        traceback.print_exc()
        return JSONResponse(content={"error": str(e)}, status_code=400)
@user_router.post(
    "/checkfaceuserfolder",
    response_model=CheckFaceUserFolder,
    responses={"404": {"model": ExceptionResponseSchema}},
)
async def checkFaceUserFolder(request: CheckFaceUserFolderRequest):
    try:

        absolute_path = os.path.abspath(TARGET+"/users")
        if not os.path.exists(absolute_path):
            print(f"Đường dẫn {absolute_path} không tồn tại.")
            return

        # Kiểm tra xem TARGET có phải là một thư mục hay không
        if not os.path.isdir(absolute_path):
            print(f"{absolute_path} không phải là một thư mục.")
            return

        # Lấy danh sách các thư mục con trong TARGET
        subdirectories = [name for name in os.listdir(absolute_path) if
                          os.path.isdir(os.path.join(absolute_path, name))]
        dataNotExit = []
        for folderNew in subdirectories:
            if folderNew not in request.folders:
                dataNotExit.append(folderNew)
        result=  await UserService().getImageFolder(dataNotExit, absolute_path)

        return {"result": result}
    except Exception as e:
        print(str(e))
        traceback.print_exc()
        return JSONResponse(content={"error": str(e)}, status_code=400)

@user_router.post("/downloadfolder", responses={"404": {"model": ExceptionResponseSchema}})
async def download_user_folder(request: CheckFaceUserFolderRequest):
    try:
        absolute_path = os.path.abspath(TARGET + "/users")
        if not os.path.exists(absolute_path):
            print(f"Đường dẫn {absolute_path} không tồn tại.")
            return

        if not os.path.isdir(absolute_path):
            print(f"{absolute_path} không phải là một thư mục.")
            return

        subdirectories = [name for name in os.listdir(absolute_path) if os.path.isdir(os.path.join(absolute_path, name))]
        dataNotExit = []
        for folderNew in subdirectories:
            if folderNew not in request.folders:
                dataNotExit.append(folderNew)


        destination_folder = TARGET

        # Create a temporary zip file
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, "downloaded.zip")

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for folderNew in dataNotExit:
                folder_path = os.path.join(absolute_path, folderNew)
                if os.path.isdir(folder_path):
                    for root, dirs, files in os.walk(folder_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            zipf.write(file_path, os.path.join(folderNew, os.path.relpath(file_path, folder_path)))

        # Move the zip file to the destination folder
        shutil.move(zip_path, os.path.join(destination_folder, "downloaded.zip"))

        # Return the zip file as a response
        return FileResponse(os.path.join(destination_folder, "downloaded.zip"), filename="downloaded.zip", media_type="application/zip")

    except Exception as e:
        print(str(e))
        traceback.print_exc()
        return JSONResponse(content={"error": str(e)}, status_code=400)

@user_router.post(
    "/deletefaceuserfolder",
    response_model=DeleteUserFolderResponse,
    responses={"404": {"model": ExceptionResponseSchema}},
)
async def checkFaceUserFolder(request: DeleteUserFolderRequest):
    try:
        absolute_path = os.path.abspath(TARGET+"/users/"+ str(request.userId))
        if not os.path.exists(absolute_path):
            return {"mess": "Not Found", "status":"false"}
        shutil.rmtree(absolute_path)
        return {"mess": "", "status":"done"}
    except Exception as e:
        print(str(e))
        traceback.print_exc()
        return JSONResponse(content={"error": str(e)}, status_code=400)