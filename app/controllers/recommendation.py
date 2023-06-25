from fastapi import Depends
from redis import Redis

from clients.redis import get_redis_client
from helpers.decorators import cache_result, calculate_execution_time
from models.recommendation import generate_candidates


async def get_recommended_items(customer_id: str,
                                redis: Redis = Depends(get_redis_client)):

    # Load customer features from the feature store
    #customer_features = redis.get(f'features:customer_id')
    customer_features = [customer_id]

    candidate_generation_dict = await generate_candidates(customer_features)

    return {
        'customer_features': customer_features,
        'candidates': candidate_generation_dict['result'],
        'execution_time_ms': candidate_generation_dict['execution_time_ms']
    }