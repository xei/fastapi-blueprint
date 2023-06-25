import os
import sys
import asyncio

import aioredis
from aioredis.exceptions import ConnectionError

# Redis settings
HOST = os.getenv("REDIS_HOST", "redis")
PORT = int(os.getenv("REDIS_PORT", 6379))
PASS = os.getenv("REDIS_PASS", "password")
DB = int(os.getenv("REDIS_DB", 0))


async def get_redis_client():
    redis_client = None

    async def create_redis_client():
        nonlocal redis_client
        if redis_client is None:
            redis_client = await aioredis.create_redis_pool(
                f"redis://{HOST}:{PORT}/{DB}",
                password=PASS,
                encoding="utf-8",
                retry_on_timeout=True
            )
        return redis_client

    return await create_redis_client()

async def close(client):
    client.close()
    await client.wait_closed()

async def is_healthy(client):
    try:
        await client.ping()
        return True
    except ConnectionError as e:
        print(str(e), file=sys.stderr)
        return False



""" Example usage
client = await get_redis_client()
print("Connected to Redis:", await is_healthy(client))
await client.close()
"""