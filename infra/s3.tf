locals {
  buckets = {
    raw       = "mundial-raw"
    curated   = "mundial-curated"
    analytics = "mundial-analytics"
  }
}

resource "aws_s3_bucket" "mundial" {
  for_each = local.buckets
  bucket   = each.value
}

resource "aws_s3_bucket_versioning" "raw" {
  bucket = aws_s3_bucket.mundial["raw"].id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "raw" {
  bucket = aws_s3_bucket.mundial["raw"].id

  rule {
    id     = "expire-raw-after-90-days"
    status = "Enabled"
    expiration {
      days = 90
    }
    filter {}
  }
}

output "bucket_arns" {
  value = { for k, b in aws_s3_bucket.mundial : k => b.arn }
}
