import time
from typing import Optional, List
from PIL import Image
from sqlalchemy import or_, select, and_
from app.user.helper.detectid.detect import yoloDetect
from io import BytesIO
from app.user.models import User, Device
from  fastapi import  UploadFile
from app.user.schemas.user import LoginResponseSchema
import  traceback
import  httpx
import os
import  base64
from pathlib import Path
from core.db import Transactional, session
from core.exceptions import (
    PasswordDoesNotMatchException,
    DuplicateEmailOrNicknameException,
    UserNotFoundException,
)
from core.utils.token_helper import TokenHelper
from sockets.services.socket import checkDetailVehicle


class UserService:
    def __init__(self):
        self.id_verify =yoloDetect()

    async def get_user_list(
        self,
        limit: int = 12,
        prev: Optional[int] = None,
    ) -> List[User]:
        query = select(User)

        # if prev:
        #     query = query.where(User.Id < prev)

        if limit > 12:
            limit = 12

        query = query.limit(limit)
        result = await session.execute(query)
        return result.scalars().all()

    @Transactional()
    async def create_user(
        self, email: str, password1: str, password2: str, nickname: str
    ) -> None:
        if password1 != password2:
            raise PasswordDoesNotMatchException

        query = select(User).where(or_(User.Email == email, User.NickName == nickname))
        result = await session.execute(query)
        is_exist = result.scalars().first()
        if is_exist:
            raise DuplicateEmailOrNicknameException

        user = User(Email=email, Password=password1, NickName=nickname)
        session.add(user)
    async def register_user(
        self, cccd: str, fullname: str, Gender: str, imageId, imageFace
    ) -> bool:
        return True
    async def is_admin(self, user_id: int) -> bool:
        result = await session.execute(select(User).where(User.Id == user_id))

        user = result.scalars().first()
        if not user:
            return False

        if user.IsAdmin is False:
            return False

        return True

    async def login(self, email: str, password: str) -> LoginResponseSchema:
        result = await session.execute(
            select(User).where(and_(User.Email == email, User.Password == password))
        )
        user = result.scalars().first()
        if not user:
            raise UserNotFoundException
        response = LoginResponseSchema(
            token=TokenHelper.encode(payload={"user_id": user.UserId}),
            refresh_token=TokenHelper.encode(payload={"sub": "refresh"}),
        )
        return response
    async def verify_lp(self, imagelp) -> str:
        lp = checkDetailVehicle(imagelp)
        #first_lp = next(iter(lp), None)
        if lp is None:
            return "Not Found"
        return lp
    async def verify_id(self, imageId)-> str:
        stringId = self.id_verify.detect_id(imageId)
        if stringId is None or stringId == 'Not Found':
            return "Not Found"
        return stringId
    async def verify_idImage(self, imageId)-> str:
        stringId = self.id_verify.detect_idImage(imageId)
        if stringId is None or stringId == 'Not Found':
            return "Not Found"
        return stringId
    def read_image_file(self,file) -> Image.Image:
        image = Image.open(BytesIO(file))

        return image

    async def send_Image_To_Client(self,user_ids, files):
        try:
            query = select(Device.DevicePublicIP, Device.DeviceUsePort ).where(Device.DeviceType == "DVC003")
            result = await session.execute(query)
            device_exist = result.all()
            files_data = [(f"files", (file.filename, file.file.read(), file.content_type)) for file in files]
            for device in device_exist:
                url = f"http://{device.DevicePublicIP}:{device.DeviceUsePort}/api/face/addusertofolder"
                print(url)
                data = {"user_ids": user_ids}


                try:
                    async with httpx.AsyncClient() as client:
                        response = await client.post(url, data=data, files=files_data)
                        response_data = response.json()
                        return response_data
                except httpx.RequestError as e:
                    print(f"Error making API request: {e}")

                except Exception as e:
                    print(f"An error occurred: {e}")

            return True
        except Exception as e:
            traceback.print_exc()
    async def getImageFolder(self, listFouder, targetPath):
        start_time = time.time()
        dataReturn ={}
        image_data = []
        for fouder in listFouder:
            path = targetPath + "\\"+str(fouder) + "\\face"
            for file_name in os.listdir(path):
                file_path = os.path.join(path, file_name)
                if os.path.isfile(file_path):
                    with open(file_path, "rb") as file:
                        image_bytes = file.read()
                        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
                        image_data.append({"file_name": file_name, "image_base64": image_base64})
            dataReturn[str(fouder)] = image_data
        endtime = time.time()
        print((endtime - start_time))
        return dataReturn




