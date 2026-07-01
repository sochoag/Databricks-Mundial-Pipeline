import os
import io
import json

import boto3
import pandas as pd
from botocore.config import Config
from functools import lru_cache

ENDPOINT = os.environ.get("LOCALSTACK_ENDPOINT", "http://localstack:4566")
BUCKET = os.environ.get("S3_ANALYTICS_BUCKET", "mundial-analytics")


@lru_cache(maxsize=1)
def _client():
    return boto3.client(
        "s3",
        endpoint_url=ENDPOINT,
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", "test"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY", "test"),
        region_name=os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
        config=Config(signature_version="s3v4"),
    )


def read_parquet(key: str) -> pd.DataFrame:
    obj = _client().get_object(Bucket=BUCKET, Key=key)
    return pd.read_parquet(io.BytesIO(obj["Body"].read()))


def read_json(key: str) -> dict:
    obj = _client().get_object(Bucket=BUCKET, Key=key)
    return json.loads(obj["Body"].read())
