from fastapi import APIRouter
from api.track.v1.request.track import CheckVehicleRequest

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
async def trackVehicle(request: CheckVehicleRequest):
    ## Check LP 
    if not request.platenum or request.platenum == "": 
        return -1 ## ExceptionTrack
    # Check Face
    ## Convert bytes to image --> cv2 
    image = cv2.imdecode(np.frombuffer(request.FaceOrigin, np.uint8), cv2.IMREAD_COLOR)
    ## Using model to verify
    face_detected = DeepFace.detectFace(image, detector_backend='ssd', enforce_detection=False)
    ### If not detect
    ### Detected
    curDT = datetime.now()
    date_time = curDT.strftime("%m%d%Y-%H%M%S")
    path_img_origin = target + str(request.platenum) 
    path_img_detected = target + str(request.platenum)  
    if isdir(path_img_origin) == False:
        os.makedirs(path_img_origin)
    if isdir(path_img_detected) == False:     
        os.makedirs(path_img_detected)
    img_detected = path_img_detected + "/{}.jpg".format(date_time)
    ## Save Image to path
    cv2.imwrite(img_detected, face_detected[:,:,::-1]*255)
    ## Using track_services to write in Database
        # face_sevices = FaceServices(img_origin, img_detected, plate_num)
        # face_sevices.add_face(embedding.model, network, img_detected, FACE_DETECTED)
        # result = face_sevices.create_track_vehicle(plate_num, img_detected, date_time, "", 0, 0)
    result = track_services.create_track_vehicle(request.platenum,img_detected,request.typeTransport, request.typeLicensePlate,img_detected, date_time)