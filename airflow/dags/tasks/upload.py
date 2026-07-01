import os
import logging
from pathlib import Path

import boto3
from botocore.config import Config

logger = logging.getLogger(__name__)

RAW_BUCKET = os.environ.get("S3_RAW_BUCKET", "mundial-raw")
ENDPOINT = os.environ.get("LOCALSTACK_ENDPOINT", "http://localstack:4566")
OUTPUT_DIR = Path("/tmp/mundial")


def _s3_client():
    return boto3.client(
        "s3",
        endpoint_url=ENDPOINT,
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", "test"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY", "test"),
        region_name=os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
        config=Config(signature_version="s3v4"),
    )


def upload_to_s3(**kwargs) -> None:
    s3 = _s3_client()

    for json_file in OUTPUT_DIR.glob("*.json"):
        # Partition by entity type and date: raw/matches/2022/06/11/matches_*.json
        parts = json_file.stem.split("_")
        entity = parts[0]
        date_str = parts[-1][:8]  # YYYYMMDD
        year, month, day = date_str[:4], date_str[4:6], date_str[6:8]

        s3_key = f"{entity}/{year}/{month}/{day}/{json_file.name}"
        s3.upload_file(str(json_file), RAW_BUCKET, s3_key)
        logger.info("Uploaded s3://%s/%s", RAW_BUCKET, s3_key)
