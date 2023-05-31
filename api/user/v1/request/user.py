from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    email: str = Field(..., description="Email")
    password: str = Field(..., description="Password")

class VerifylicensePlateRequest(BaseModel):
    stringlp : str =  Field(..., description="License Plate Image")