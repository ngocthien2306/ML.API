from pydantic import BaseModel, Field


class DetectVehicleRespose(BaseModel):
    license: str = Field(..., description="License Plate")
    transportType: str = Field(..., description="Type Vehicle")
    plateType:str = Field(..., description="Type License Plate")
    message: str = Field(..., description="Status Information")
class AddVehicleUserRespose(BaseModel):
    imagePath: str = Field(..., description="License Plate Path")
