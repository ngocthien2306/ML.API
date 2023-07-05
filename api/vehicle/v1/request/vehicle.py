from pydantic import BaseModel, Field

class DetectVehicleRequest(BaseModel):
    imagelp64 : str =  Field(..., description="License Plate Image")
class AddVehicleUserRequest(BaseModel):
    userid : str =  Field(..., description="ID user")
    licenseNumber: str =  Field(..., description="License Plate")
    imageVehicle64 : str =  Field(..., description="License Plate Image")