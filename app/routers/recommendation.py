from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field, validator

from controllers.recommendation import get_recommended_items
from helpers import log



router = APIRouter()


class RequestPayload(BaseModel):
    customer_id: str = Field(
        description="Customer unique ID",
        example="42"
    )
    order_time: Optional[datetime] = Field(
        default=None,
        description="The time when the user wants to buy. Ignore it if the recommendation is for now.",
        example=datetime(2023, 5, 7, 18, 0, 58)
    )
    customer_latitude: float = Field(
        description="The latitude of the customer",
        example=35.763358
    )
    customer_longitude: float = Field(
        description="The longitude of the customer",
        example=51.411085
    )

class ResponsePayload(BaseModel):
    recommendation_time: datetime
    recommended_items: List[str]

    class Config:
        json_encoders = {
            # Change the format:
            # datetime: lambda dt: dt.strftime('%Y-%m-%dT%H:%M:%S')
            datetime: lambda dt: dt.isoformat(timespec='seconds')
        }


@router.post("/recommendation")
async def recommendation(request_payload: RequestPayload,
                         now: datetime = Depends(datetime.now)):
    """
    The logic in this endpoint is a bit complex.
    So, we put the logic in a separate controller.
    """

    candidates_dict: dict = await get_recommended_items(
        request_payload.customer_id
    )

    response_payload = ResponsePayload(
        recommendation_time=now,
        recommended_items=candidates_dict['candidates']
    )

    await log.analytical_log(
        request=request_payload,
        response=response_payload,
        metadata={
            'retrieval_time_ms': round(candidates_dict['execution_time_ms'], 2)
        }
    )

    return response_payload