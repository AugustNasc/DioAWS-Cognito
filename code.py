import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("DIOItems")

def lambda_handler(event, context):
    try:
        print("EVENT:", event)

        raw_body = event.get("body")
        if raw_body is None:
            return response(400, "Body não enviado")

        body = json.loads(raw_body) if isinstance(raw_body, str) else raw_body

        item_id = body.get("id")
        price = body.get("price")

        if not item_id or price is None:
            return response(400, "Campos 'id' e 'price' são obrigatórios")

        table.put_item(
            Item={
                "id": item_id,
                "price": Decimal(str(price))
            }
        )

        return response(200, {
            "message": "Item inserido com sucesso!",
            "item": {
                "id": item_id,
                "price": price
            }
        })

    except Exception as e:
        print("ERROR:", str(e))
        return response(500, str(e))


def response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }
