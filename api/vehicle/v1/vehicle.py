

from fastapi import APIRouter
from api.vehicle.v1.request.vehicle import AddVehicleUserRequest, DetectVehicleRequest
from fastapi.responses import JSONResponse
from api.vehicle.v1.response.vehicle import AddVehicleUserRespose, DetectVehicleRespose
from app.vehicle.schemas import ExceptionVehicleResponseSchema
from app.vehicle.services.vehicle import VehicleServices
vehicle_router = APIRouter()
vehicle_services = VehicleServices()

@vehicle_router.post(
    "/detectVehicle",
    response_model=DetectVehicleRespose,
    responses={"400": {"model": ExceptionVehicleResponseSchema}},
)
async def detectVehicle(request: DetectVehicleRequest):
    try:
        ## Check LP 
        if not request.imagelp64 or request.imagelp64 == "": 
            return -1 ## ExceptionTrack
        result = vehicle_services.checkDetailVehicle(request.imagelp64)
        return DetectVehicleRespose(transportType = result[0],license = result[1],plateType = result[2],message = result[3])
    except Exception as e:
        print(str(e))
        return JSONResponse(content={"error": str(e)}, status_code=400)
@vehicle_router.post(
    "/addVehicleUser",
    response_model=AddVehicleUserRespose,
    responses={"400": {"model": ExceptionVehicleResponseSchema}},
)
async def addVehicleUser(request: AddVehicleUserRequest):
    try:
        result = vehicle_services.addVehicleUser(userid = request.userid, vehicleImage = request.imageVehicle64,lp= request.licenseNumber)
        return AddVehicleUserRespose(imagePath = result)
    except Exception as e:
        print(str(e))
        return JSONResponse(content={"error": str(e)}, status_code=400)