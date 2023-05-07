from sqlalchemy.orm import Session
from app.track import models
from app.track.models.track import Track
from sqlalchemy import or_, select, and_
from app.track.models.vehicle import Vehicle
from core.db import Transactional, session
class TrackingServices:
    async def checkidVehicle(self, plate_number: str) -> Vehicle:
        print(plate_number)
        query = select(models.Vehicle).where(Vehicle.plateNum == plate_number)
        vehicle = await session.execute(query)
        
        return vehicle.scalars().first()
    async def checkidVehicleInParking(self, vehicleId: int) -> Track:
        query = select(models.Track).where( and_(
            Track.vehicleId == vehicleId,
            Track.endTime == "0"
        ))
        trackVehicle = await session.execute(query)
        return trackVehicle.scalars().first()
    @Transactional()
    async def create_track_vehicle(self, plate_number: str,imglp_detected: str,typeTransaction: str, typeLP: str, img_detected: str, time_track:str):
        ## Verify that the Plate Number
        try:

                ## Create the Vehicle model
                # Check if the face car has arrived in the parking lot 
                ## Query vehicle in database
                vehicleCheck = await self.checkidVehicle(plate_number)
                print(vehicleCheck)
                if not vehicleCheck :
                    vehicle = Vehicle(
                        plateNum=plate_number,
                        status = "AOOTEST",
                        typeTransport = typeTransaction,
                        typePlate = typeLP
                    )
                    session.add(vehicle)
                    session.flush()
                    session.refresh(vehicle)
                    vehicleCheck= vehicle
                track = await self.checkidVehicleInParking(vehicleCheck.id)
                print(track)
                print("track ID:", track.vehicleId)
                if not track:
                    trackVehicle = Track(
                        vehicleId = vehicleCheck.id,
                        trackNumber = 1,
                        startTime = time_track,
                        fee = "0",
                        siteId =1,
                        detectInFace = img_detected,
                        plateIn = imglp_detected
                    )
                    session.add(trackVehicle)
                else:
                    track.endTime =time_track
                    track.detectOutFace = img_detected
                    track.plateOut = imglp_detected

                session.commit()

                return {"status": "Track vehicle created successfully.","fee": 0}
        except Exception as e:
            session.rollback()
            return {"status": "Error is:"+ str(e),"fee": 0}  