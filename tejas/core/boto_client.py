import boto3

from tejas.core.config import settings

lambda_client = boto3.client("lambda")

ddb_client = boto3.client("dynamodb")
ddb = boto3.resource("dynamodb")
tasks_table = ddb.Table(settings.TASKS_TABLE)
