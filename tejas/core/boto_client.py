import boto3

from tejas.core.config import settings

lambda_client = boto3.client("lambda")

ddb_client = boto3.client("dynamodb")
ddb = boto3.resource("dynamodb")
tasks_table = ddb.Table(settings.TASKS_TABLE)

s3_client = boto3.client("s3")
download_models_bucket = s3_client.Bucket(settings.MODELS_BUCKET)
