from sqlalchemy.orm import Session
from app.track import models
from app.track.models.track import Track

from app.track.models.vehicle import Vehicle
from core.db import Transactional, session
class TrackingServices:
    def checkidVehicle(self, plate_number: str) -> Vehicle:
        vehicle = session.query(models.Vehicle).filter(Vehicle.plateNum == plate_number).first()
        return vehicle
    def checkidVehicleInParking(self, vehicleId: int) -> Track:
        trackVehicle = session.query(models.Track).filter(
            Track.vehicleId == vehicleId,
            Track.endTime == "0"
        ).first()
        return trackVehicle
    @Transactional
    def create_track_vehicle(self, plate_number: str,imglp_detected: str,typeTransaction: str, typeLP: str, img_detected: str, time_track:str):
        ## Verify that the Plate Number
        try:
            with session.begin():
                ## Create the Vehicle model
                # Check if the face car has arrived in the parking lot 
                ## Query vehicle in database
                vehicleCheck = self.checkidVehicle(plate_number.plate_num,db)
                if not vehicleCheck :
                    vehicle = Vehicle(
                        plateNum=plate_number.plate_num,
                        status = "AOOTEST",
                        typeTransport = typeTransaction,
                        typePlate = typeLP
                    )
                    session.add(vehicle)
                    session.flush()
                    session.refresh(vehicle)
                    vehicleCheck= vehicle
                track = self.checkidVehicleInParking(vehicleCheck.id,db)
                print(track)
                if not track:
                    trackVehicle = Track(
                        vehicleId = vehicleCheck.id,
                        trackNumber = 1,
                        startTime = time_track,
                        fee = "0",
                        siteId ="ABCTEST",
                        detectInFace = img_detected,
                        plateIn = imglp_detected
                    )
                    session.add(trackVehicle)
                else:
                    track.endTime =time_track
                    track.detectOutFace = img_detected
                    track.plateOut = imglp_detected

                session.commit()

                return {"message": "Track vehicle created successfully."}
        except Exception as e:
            session.rollback()
            return {"message": "Error is"+ str(e)}  