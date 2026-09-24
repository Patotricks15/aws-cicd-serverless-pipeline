"""removeitem Lambda handler: deletes an item from the Items DynamoDB table."""
import json
import os

import boto3

TABLE_NAME = os.environ["TABLE_NAME"]
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    body = json.loads(event.get("body") or "{}")
    item_id = body.get("id")

    if not item_id:
        return {"statusCode": 400, "body": json.dumps({"message": "'id' is required"})}

    table.delete_item(Key={"id": item_id})

    return {"statusCode": 200, "body": json.dumps({"id": item_id, "deleted": True})}
