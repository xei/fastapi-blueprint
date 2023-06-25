from datetime import timedelta

from fastapi import APIRouter
from pydantic import BaseModel, Field

from models.courier_travel_time import estimate_travel_time
from helpers import log



router = APIRouter()


class RequestPayload(BaseModel):
    source_latitude: float = Field(
        description="The latitude of the source",
        example=35.763358
    )
    source_longitude: float = Field(
        description="The longitude of the source",
        example=51.411085
    )
    destination_latitude: float = Field(
        description="The latitude of the destination",
        example=35.773358
    )
    destination_longitude: float = Field(
        description="The longitude of the destination",
        example=51.311085
    )

class ResponsePayload(BaseModel):
    travel_time_minutes: int


@router.post("/travel-time")
async def travel_time(request_payload: RequestPayload):
    """
    This is a simple endpoint that does not need a separate controller.
    This function act as the controller and call the model directly.
    """

    eta: timedelta = await estimate_travel_time(
        src_lat=request_payload.source_latitude,
        src_lon=request_payload.source_longitude,
        dst_lat=request_payload.destination_latitude,
        dst_lon=request_payload.destination_longitude
    )

    response_payload = ResponsePayload(
        travel_time_minutes=eta.total_seconds()//60,
    )

    await log.analytical_log(
        request=request_payload,
        response=response_payload
    )

    return response_payload