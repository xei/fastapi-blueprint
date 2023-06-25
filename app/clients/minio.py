import os
import sys
import time

from minio import Minio
from minio.error import ResponseError
from urllib3.exceptions import MaxRetryError


# Minio settings
ENDPOINT = os.getenv("MINIO_ENDPOINT", "minio:9000")
ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "accesskey")
SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "secretkey")
BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME", "my-bucket")


def get_minio_client():
    minio_client = None

    def create_minio_client():
        nonlocal minio_client
        if minio_client is None:
            minio_client = Minio(ENDPOINT, access_key=ACCESS_KEY, secret_key=SECRET_KEY)
            if not is_healthy(minio_client):
                retry_connection(minio_client)
        return minio_client

    return create_minio_client()

def is_healthy(client):
    try:
        client.list_buckets()
        return True
    except (ResponseError, MaxRetryError) as e:
        print(str(e), file=sys.stderr)
        return False

def retry_connection(client):
    for i in range(5):
        print(f"Failed to connect to Minio server. Retrying in {i + 1} seconds...",
              file=sys.stderr)
        time.sleep(i + 1)
        if is_healthy(client):
            return
    raise Exception("Failed to connect to Minio server after multiple attempts.")