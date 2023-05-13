from datetime import datetime
from sqlalchemy.orm import Session
from app.track import models
from app.track.models.track import Track
from sqlalchemy import or_, select, and_
from app.track.models.vehicle import Vehicle
from app.track.services.face import FaceServices
from app.track.enums.track import VehicleStatus
from core.db import Transactional, session
import cv2
import base64
import numpy as np
face_services = FaceServices()
class TrackingServices:
    def __init__(self, PATH_IMAGE_SAVE=None):
        self.path_image_save = PATH_IMAGE_SAVE
    async def checkidVehicle(self, plate_number: str) -> Vehicle:
        print(plate_number)
        query = select(models.Vehicle).where(Vehicle.plateNum == plate_number)
        vehicle = await session.execute(query)
        
        return vehicle.scalars().first()
    async def checkidVehicleInParking(self, vehicleId: int) -> Track:
        # Sort with Time
        query = select(models.Track).where( and_(
            Track.vehicleId == vehicleId,
            Track.detectOutFace == "0",
            Track.plateOut == "0"
        ))
        trackVehicle = await session.execute(query)
        return trackVehicle.scalars().first()
    @Transactional()
    async def create_track_vehicle(self,model,img_detected_save, plate_number: str,imglp_detected: str,typeTransaction: str, typeLP: str, img_detected: str):
        ## Verify that the Plate Number
        try:
                print(plate_number)
                ## Create the Vehicle model
                # Check if the face car has arrived in the parking lot 
                ## Query vehicle in database
                vehicleCheck = await self.checkidVehicle(plate_number)
                if not vehicleCheck :
                    vehicle = Vehicle(
                        plateNum=plate_number,
                        status = VehicleStatus.ACCEPTIN.value,
                        typeTransport = typeTransaction,
                        typePlate = typeLP
                    )
                    session.add(vehicle)
                    
                    session.flush()
                    session.refresh(vehicle)
                    vehicleCheck= vehicle
                track = await self.checkidVehicleInParking(vehicleCheck.id)
                print("track",track)
                curDT = datetime.now()
                if not track:
                    trackVehicle = Track(
                        vehicleId = vehicleCheck.id,
                        trackNumber = 1,
                        startTime = curDT,
                        fee = 0.0,
                        siteId =1,
                        detectInFace = img_detected,
                        plateIn = imglp_detected
                    )
                    session.add(trackVehicle)
                else:
                    ## Face verify
                    img_detected_path = track.detectInFace
                    print(img_detected_path)
                    # Reshape
                    img_detected_save= cv2.resize(img_detected_save,(112,112))
                    access =face_services.face_check_track(model,img_detected_save,img_detected_path)
                    print(access)
                    if access == True:
                        track.endTime =curDT
                        track.detectOutFace = img_detected
                        track.plateOut = imglp_detected
                        vehicleCheck.status= VehicleStatus.ACCEPTOUT.value
                        session.refresh(vehicleCheck)
                    else:
                        vehicleCheck.status =VehicleStatus.BLOCK.value
                        session.refresh(vehicleCheck)
                session.commit()

                return {"status": str(vehicleCheck.status),"fee": 0}
        except Exception as e:
            return {"status": "Error is:"+ str(e),"fee": 0}  
    def convertbase64 (self,string64 ):
        decoded_data = base64.b64decode(string64)
        np_data = np.fromstring(decoded_data, np.uint8)
        image = cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)
        return image