resource "aws_iam_user" "airflow" {
  name = "mundial-airflow"
}

resource "aws_iam_user" "api" {
  name = "mundial-api"
}

data "aws_iam_policy_document" "airflow_s3" {
  statement {
    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:DeleteObject",
      "s3:ListBucket",
    ]
    resources = [
      aws_s3_bucket.mundial["raw"].arn,
      "${aws_s3_bucket.mundial["raw"].arn}/*",
      aws_s3_bucket.mundial["curated"].arn,
      "${aws_s3_bucket.mundial["curated"].arn}/*",
      aws_s3_bucket.mundial["analytics"].arn,
      "${aws_s3_bucket.mundial["analytics"].arn}/*",
    ]
  }
}

data "aws_iam_policy_document" "api_s3" {
  statement {
    actions   = ["s3:GetObject", "s3:ListBucket"]
    resources = [
      aws_s3_bucket.mundial["analytics"].arn,
      "${aws_s3_bucket.mundial["analytics"].arn}/*",
    ]
  }
}

resource "aws_iam_user_policy" "airflow_s3" {
  name   = "airflow-s3-access"
  user   = aws_iam_user.airflow.name
  policy = data.aws_iam_policy_document.airflow_s3.json
}

resource "aws_iam_user_policy" "api_s3" {
  name   = "api-s3-readonly"
  user   = aws_iam_user.api.name
  policy = data.aws_iam_policy_document.api_s3.json
}
