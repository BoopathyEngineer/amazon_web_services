import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    http_method = event['httpMethod']
    if http_method == 'POST':
        data = json.loads(event['body'])
        table.put_item(Item=data)
        return {"statusCode": 200, "body": json.dumps({"message": "Item created"})}

    elif http_method == 'GET':
        id = event['queryStringParameters']['id']
        response = table.get_item(Key={'id': id})
        return {"statusCode": 200, "body": json.dumps(response.get('Item', {}))}

    elif http_method == 'PUT':
        data = json.loads(event['body'])
        table.put_item(Item=data)
        return {"statusCode": 200, "body": json.dumps({"message": "Item updated"})}

    elif http_method == 'DELETE':
        id = event['queryStringParameters']['id']
        table.delete_item(Key={'id': id})
        return {"statusCode": 200, "body": json.dumps({"message": "Item deleted"})}

    return {"statusCode": 400, "body": json.dumps({"error": "Unsupported method"})}
