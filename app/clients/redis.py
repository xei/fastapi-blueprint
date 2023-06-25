import os
import sys
import time

import redis
from redis.exceptions import ConnectionError



# Redis settings
HOST = os.getenv("REDIS_HOST", "redis")
PORT = int(os.getenv("REDIS_PORT", 6379))
PASS = os.getenv("REDIS_PASS", "password")
DB = int(os.getenv("REDIS_DB", 0))


def get_redis_client():
    redis_client = None

    def create_redis_client():
        nonlocal redis_client
        if redis_client is None:
            redis_client = redis.Redis(host=HOST,
                                       port=PORT,
                                       password=PASS,
                                       db=DB,
                                       connection_pool=redis.ConnectionPool(),
                                       decode_responses=True,
                                       retry_on_timeout=True)
        return redis_client

    return create_redis_client()

def is_healthy(client):
    try:
        client.ping()
        return True
    except ConnectionError as e:
        print(str(e), file=sys.stderr)
        return False