"""additem Lambda handler: writes a new item to the Items DynamoDB table."""
import json
import os
import uuid

import boto3

TABLE_NAME = os.environ["TABLE_NAME"]
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    body = json.loads(event.get("body") or "{}")
    name = body.get("name")

    if not name:
        return {"statusCode": 400, "body": json.dumps({"message": "'name' is required"})}

    item_id = str(uuid.uuid4())
    table.put_item(Item={"id": item_id, "name": name})

    return {"statusCode": 201, "body": json.dumps({"id": item_id, "name": name})}
