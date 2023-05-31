from typing import List
import base64
import numpy as np
import cv2
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from api.user.v1.request.user import LoginRequest, VerifyIdVietNameRequest, VerifylicensePlateRequest
from api.user.v1.response.user import LoginResponse, VerifylIdVietNamResponse, VerifylicensePlateResponse
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

user_router = APIRouter()


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
        decoded_data = base64.b64decode(request.stringlp)
        np_data = np.fromstring(decoded_data, np.uint8)
        image = cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)
        
        
        # Lp returned to LP Dictionary so Check accuracy here
        lp = await UserService().verify_lp(imagelp=image)
        
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
        np_data = np.fromstring(decoded_data, np.uint8)
        image = cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
        # Lp returned to LP Dictionary so Check accuracy here
        cv2.imwrite("/data/thinhlv/hung/Capstone/cccd_detect_character/testImageAPi.jpg", image)
        result = await UserService().verify_id(imageId=image)
        return {"id": str(result)}
    except Exception as e:
        print(str(e))
        return JSONResponse(content={"error": str(e)}, status_code=400)