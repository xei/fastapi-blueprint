from datetime import datetime
from typing import Optional, Dict

from pydantic import BaseModel



class AnalyticalLog(BaseModel):
    request: BaseModel
    response: BaseModel
    metadata: Optional[Dict]

    class Config:
        json_encoders = {
            # Change the format:
            # datetime: lambda dt: dt.strftime('%Y-%m-%dT%H:%M:%S')
            datetime: lambda dt: dt.isoformat(timespec='seconds')
        }

async def analytical_log(request: BaseModel,
                         response: BaseModel,
                         metadata: Optional[Dict] = None):
    print(
        AnalyticalLog(
            request=request,
            response=response,
            metadata=metadata
        ).json()
    )