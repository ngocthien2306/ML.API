from fastapi import APIRouter, File, UploadFile,WebSocket,status
from api.track.v1.request.track import CheckVehicleRequest
from fastapi.responses import JSONResponse
from api.track.v1.response.track import CheckVehicleResponse
from app.track.helper.embedding import Embedding
from app.track.schemas import ExceptionTrackResponseSchema
from app.track.schemas.track import TrackVehicleResposeSchemas
from app.track.services.track import TrackingServices
## Image Recognition
import numpy as np
import cv2
from deepface import DeepFace
from datetime import datetime
from typing import Union
import os
from os.path import join, dirname, isdir
from dotenv import load_dotenv
load_dotenv()
TARGET = os.environ.get("TARGET")
MODEL_PATH = os.environ.get("MODEL_PATH")
NETWORK = os.environ.get("NETWORK")

batch_size = 32

embedding = Embedding(MODEL_PATH, (3, 112, 112), 128, network=NETWORK)
#End: Deeplearning

track_router = APIRouter()
track_services = TrackingServices(TARGET)

@track_router.post(
    "/trackingVehicle",
    response_model=TrackVehicleResposeSchemas,
    responses={"400": {"model": ExceptionTrackResponseSchema}},
)
async def trackVehicle(platenum: str,typeTransport:str,typeLicensePlate:str, file: Union[UploadFile,None] = None, filelp: Union[UploadFile,None] = None):
    try:
        ## Check LP 
        if not platenum or platenum == "": 
            return -1 ## ExceptionTrack

        # Check Face
        ## Read Image --> cv2 
        face = cv2.imdecode(np.fromstring(file.file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        lpImage = cv2.imdecode(np.fromstring(filelp.file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        ## Get path image
        curDT = datetime.now()
        date_time = curDT.strftime("%m%d%Y-%H%M%S")
        path_img_detected = TARGET + str(platenum)  

        if isdir(path_img_detected) == False:     
            os.makedirs(path_img_detected)
        img_detected = path_img_detected + "/face_{}.jpg".format(date_time)
        lpImage_path = path_img_detected + "/lp_{}.jpg".format(date_time)
        ## Image DetectFace
        ### If it can't be detected return exception
        face_detected = DeepFace.detectFace(face, detector_backend='ssd', enforce_detection=True)
        ## Save Image to path  --- Save Image Detect
        cv2.imwrite(img_detected, face_detected[:,:,::-1]*255)
        cv2.imwrite(lpImage_path, lpImage)
        img_detected = img_detected.replace(path_img_detected,"")
        lpImage_path_sub = lpImage_path.replace(path_img_detected,"")
        ## Using track_services to write in Database
        result = await track_services.create_track_vehicle(embedding.model,face_detected[:,:,::-1]*255,platenum,lpImage_path_sub,typeTransport, typeLicensePlate,img_detected, date_time, "AOOTEST") # "AOOTEST" is Const
        return TrackVehicleResposeSchemas(status=result["status"], fee=result["fee"])
    except Exception as e:
        return TrackVehicleResposeSchemas(status=str(e), fee="fee")
@track_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await websocket.accept()
        while True:
                print("websocket")
                # # Nhận dữ liệu từ client
                # data = await websocket.receive_text()
                
                # # Parse dữ liệu nhận được thành đối tượng JSON
                # json_data = json.loads(data)
                # # Lấy dữ liệu ảnh từ trường "Image"
                # img_str = base64.b64decode(json_data['Image'])
                # # Chuyển đổi dữ liệu ảnh thành đối tượng numpy array
                # image_np = cv2.imdecode(np.frombuffer(img_str, np.uint8), cv2.IMREAD_COLOR)
                
                # print(image_np.shape)
            
                # predictions =json_data['Predictions']
                # if len(predictions) != 0: 
                #     listChar,typelp,typevehi = service.ocrYolo(image_np,predictions)
                #     print("Chuoi bien so", listChar)
                # Xử lý dữ liệu nhận được tại đây
                # Gửi phản hồi về cho client
                await websocket.send_text("listChar")
    except Exception as e:
        print('message' ,str(e))
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { 'message' : str(e) }
            )