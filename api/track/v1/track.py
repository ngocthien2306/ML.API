from fastapi import APIRouter, HTTPException
from api.track.v1.request.track import CheckVehicleReport, CheckVehicleRequest
from app.track.helper.embedding import Embedding
from app.track.schemas import ExceptionTrackResponseSchema
from app.track.schemas.track import TrackReportResposeSchemas, TrackVehicleResposeSchemas
from app.track.services.face import FaceServices
from app.track.services.track import TrackingServices
from fastapi.responses import JSONResponse
## Image Recognition
from PIL import Image
import cv2
from deepface import DeepFace
from datetime import datetime
import io
import os
import numpy as np
from os.path import isdir
from dotenv import load_dotenv
import traceback
load_dotenv()
TARGET = "D:\\CAPSTONE2023\\ML.API\\public\\images\\"
MODEL_PATH = os.environ.get("MODEL_PATH")
NETWORK = os.environ.get("NETWORK")

batch_size = 32

embedding = Embedding(MODEL_PATH, (3, 112, 112), 128, network=NETWORK)
#End: Deeplearning
print("MODEL_PATH",embedding)

track_router = APIRouter()
face_services = FaceServices()
track_services = TrackingServices(TARGET)

@track_router.post(
    "/trackingVehicle",
    response_model=TrackVehicleResposeSchemas,
    responses={"400": {"model": ExceptionTrackResponseSchema}},
)
async def trackVehicle(request: CheckVehicleRequest):
    try:
        ## Check LP 
        if not request.platenum or request.platenum == "": 
            return -1 ## ExceptionTrack
        # Check Face
        ## Read Image --> cv2 
        # face = cv2.imdecode(np.fromstring(file.file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        # lpImage = cv2.imdecode(np.fromstring(filelp.file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        face64 = request.stringFace
        lp = request.stringlp
        face = track_services.convertbase64(face64)
        lpImage = track_services.convertbase64(lp)
        ## Get path image
        curDT = datetime.now()
        date_time = curDT.strftime("%m%d%Y-%H%M%S")

        ## Check User 
        user_photo = await  track_services.get_image_user2(str(request.platenum))
        print(user_photo)
        if user_photo is not None:
            byte_stream = io.BytesIO(user_photo[1])
            
            image = Image.open(byte_stream)
            image_array = np.asarray(image) 
            image_array = cv2.cvtColor(image_array,cv2.COLOR_RGB2BGR)
            ## Verify Image Face Identification
            
            face_detected_user = DeepFace.detectFace(face, detector_backend='ssd', enforce_detection=True,target_size=(112,112))
            #face_detected_user = cv2.resize(face_detected_user,(112,112))
            face_user_db = DeepFace.detectFace(image_array, detector_backend='ssd', enforce_detection=True,target_size=(112,112))
            #resize_face_user = cv2.resize(face_user_db,(112,112))
            access =face_services.face_check_user(embedding.model,face_detected_user,face_user_db)
            print("User_photo: ", access)
            path_img_detected = TARGET +"users/" + str(user_photo[0])

            if isdir(path_img_detected) == False:     
                os.makedirs(path_img_detected)
            img_user_detected = path_img_detected +"/face"+ "/face_{}.jpg".format(date_time)
            lpImage_user_path = path_img_detected +"/lp"+ "/lp_{}.jpg".format(date_time)
            cv2.imwrite(img_user_detected, face_detected_user[:,:,::-1]*255)
            cv2.imwrite(lpImage_user_path, lpImage)
            result = await track_services.create_track_vehicle_user(
                lpImage_user_path,
                img_user_detected,
                status=access,
                request=request)
            print(result)
            return result
        else:
            print("No User")
            path_img_detected = TARGET +"nouser/"+ str(request.platenum)+"/face"
            path_imglp_detected = TARGET +"nouser/"+ str(request.platenum)+"/lp"

            if isdir(path_img_detected) == False:     
                os.makedirs(path_img_detected)
            if isdir(path_imglp_detected) == False:
                os.makedirs(path_imglp_detected)
            img_detected = path_img_detected + "/face_{}.jpg".format(date_time)
            lpImage_path = path_imglp_detected +"/lp_{}.jpg".format(date_time)
            print(("img_detected",img_detected))
            ## Image DetectFace
            ### If it can't be detected return exception
            face_detected = DeepFace.detectFace(face, detector_backend='ssd', enforce_detection=True)
            ## Save Image to path  --- Save Image Detect
            cv2.imwrite(img_detected, face_detected[:,:,::-1]*255)
            cv2.imwrite(lpImage_path, lpImage)

            ## Using track_services to write in Database
            result = await track_services.create_track_vehicle_async(
                embedding.model,
                face_detected[:,:,::-1]*255,
                lpImage_path,
                img_detected,
                request)
            print(result["status"])
            return TrackVehicleResposeSchemas(status=result["status"], fee=result["fee"])
    except Exception as e:
        print(str(e))

        return JSONResponse(content={"error": str(e)}, status_code=400)
@track_router.post(
    "/trackingReports",
    response_model=TrackReportResposeSchemas,
    responses={"400": {"model": ExceptionTrackResponseSchema}},
)
async def trackVehicle(request: CheckVehicleReport):
    try:
        face64 = request.stringFace
        lp = request.stringlp
        face = track_services.convertbase64(face64)
        lpImage = track_services.convertbase64(lp)
        ## Get path image
        curDT = datetime.now()
        date_time = curDT.strftime("%m%d%Y-%H%M%S")
        path_img_detected = TARGET + "nouser/" + str(request.platenum) + "/face"
        path_imglp_detected = TARGET + "nouser/" + str(request.platenum) + "/lp"

        if isdir(path_img_detected) == False:
            os.makedirs(path_img_detected)
        if isdir(path_imglp_detected) == False:
            os.makedirs(path_imglp_detected)
        img_detected = path_img_detected + "/face_{}.jpg".format(date_time)
        lpImage_path = path_imglp_detected + "/lp_{}.jpg".format(date_time)
        face_detected = DeepFace.detectFace(face, detector_backend='ssd', enforce_detection=True)
        ## Save Image to path  --- Save Image Detect
        cv2.imwrite(img_detected, face_detected[:,:,::-1]*255)
        cv2.imwrite(lpImage_path, lpImage)
        result = await track_services.create_track_report(request.siteId,request.platenum,request.typeTransport,request.typeLicensePlate,img_detected,lpImage_path)
        print(result) 
        if result == True:
            return TrackReportResposeSchemas(status=True)
        return TrackReportResposeSchemas(status=False)
    except Exception as e:
        print(str(e))
        return JSONResponse(content={"error": str(e)}, status_code=400)
