from fastapi import APIRouter, Depends, HTTPException, status
from minio import Minio
from redis import Redis

from clients.redis import get_redis_client, is_healthy as is_redis_healthy
from models.recommendation import get_retrieval_model, is_model_loaded


router = APIRouter()


@router.get("/healthz", status_code=status.HTTP_200_OK)
async def health_check(redis: Redis = Depends(get_redis_client),
                       retrieval_model = Depends(get_retrieval_model)):
                     # minio: Minio = Depends(get_minio_client),


    detail = {
        "Redis": "Healthy" if is_redis_healthy(redis) else "Unhealthy",
        "Retrieval Model": "Healthy" if is_model_loaded(retrieval_model) else "Unhealthy",
        # "MinIO": "Healthy" if is_minio_healthy(minio) else "Unhealthy",
    }

    if all(value == "Healthy" for value in detail.values()):
        return {
            'detail': detail
        }
    else:
        raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=detail,
        )