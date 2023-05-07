from pydantic import BaseModel, Field

class CheckVehicleRequest(BaseModel):
    platenum: str = Field(..., description="License Plate")
    typeTransport: str = Field(..., description="Type Transport")
    typeLicensePlate: str =  Field(..., description="Type License Plate")

    