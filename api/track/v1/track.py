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
target = "/data/thinhlv/hung/Capstone/temp/"
model_path = "/data/thinhlv/thiennn/deeplearning/insightface/recognition/arcface_torch/work_dirs/glint360k_cosface_r100_fp16_0.1/backbone.pth"
#model_path = "/data/thinhlv/thiennn/deeplearning/insightface/recognition/arcface_torch/work_dirs/ms1mv3_r50_onegpu/model.pt"
image_path = "/data/thinhlv/thiennn/deeplearning/insightface/recognition/_datasets_/ms1m-retinaface-t1"
result_dir = "/data/thinhlv/thiennn/deeplearning/insightface/recognition/arcface_torch/work_dirs/glint360k_cosface_r100_fp16_0.1"
batch_size = 32
job = "pyface"
network = "r100"
embedding = Embedding(model_path, (3, 112, 112), 128, network=network)
#End: Deeplearning

track_router = APIRouter()
track_services = TrackingServices()
@track_router.post(
    "/trackingVehicle",
    response_model=TrackVehicleResposeSchemas,
    responses={"400": {"model": ExceptionTrackResponseSchema}},
)
async def trackVehicle(platenum: str,typeTransport:str,typeLicensePlate:str, file: Union[UploadFile,None] = None):
    ## Check LP 
    if not platenum or platenum == "": 
        return -1 ## ExceptionTrack

    # Check Face
    ## Read Image --> cv2 
    face = cv2.imdecode(np.fromstring(file.file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    ## Using model to verify
    #face_detected = DeepFace.detectFace(image, detector_backend='ssd', enforce_detection=False)
    face_detected =face
    ### If not detect
    ### Detected
    curDT = datetime.now()
    date_time = curDT.strftime("%m%d%Y-%H%M%S")
    path_img_origin = target + str(platenum) 
    path_img_detected = target + str(platenum)  
    if isdir(path_img_origin) == False:
        os.makedirs(path_img_origin)
    if isdir(path_img_detected) == False:     
        os.makedirs(path_img_detected)
    img_detected = path_img_detected + "/{}.jpg".format(date_time)
    
    ## Save Image to path
    cv2.imwrite(img_detected, face_detected[:,:,::-1]*255)
    img_detected = img_detected.replace(path_img_detected,"")
    ## Using track_services to write in Database
        # face_sevices = FaceServices(img_origin, img_detected, plate_num)
        # face_sevices.add_face(embedding.model, network, img_detected, FACE_DETECTED)
        # result = face_sevices.create_track_vehicle(plate_num, img_detected, date_time, "", 0, 0)
    result = await track_services.create_track_vehicle(platenum,img_detected,typeTransport, typeLicensePlate,img_detected, date_time)
    return TrackVehicleResposeSchemas(status=result["status"], fee=result["fee"])
    
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