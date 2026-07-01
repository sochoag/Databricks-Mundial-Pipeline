#!/bin/bash
set -e

echo "Initializing LocalStack S3 buckets..."

awslocal s3 mb s3://mundial-raw
awslocal s3 mb s3://mundial-curated
awslocal s3 mb s3://mundial-analytics

awslocal s3api put-bucket-versioning \
  --bucket mundial-raw \
  --versioning-configuration Status=Enabled

echo "Buckets created:"
awslocal s3 ls
