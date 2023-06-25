"""
This package contains modules for managing the connection
to different data sources like MySQL, Redis, MinIO, etc.

To use the client (for example the Redis client) in your function
you can inject it using Dependency Injection:

 from clients.aioredis import get_redis_client
 async def my_function_that_needs_redis(
        redis: Redis = Depends(get_redis_client)
 ):
"""