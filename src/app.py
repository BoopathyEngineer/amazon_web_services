import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    http_method = event['httpMethod']
    
    # Define common CORS headers
    cors_headers = {
        "Access-Control-Allow-Origin": "*",  # Or specify allowed origins
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE",  # Allowed HTTP methods
        "Access-Control-Allow-Headers": "Content-Type, Authorization"  # Allowed headers
    }

    if http_method == 'POST':
        data = json.loads(event['body'])
        table.put_item(Item=data)
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Item created"}),
            "headers": cors_headers
        }

    elif http_method == 'GET':
        id = event['queryStringParameters']['id']
        response = table.get_item(Key={'id': id})
        return {
            "statusCode": 200,
            "body": json.dumps(response.get('Item', {})),
            "headers": cors_headers
        }

    elif http_method == 'PUT':
        data = json.loads(event['body'])
        table.put_item(Item=data)
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Item updated"}),
            "headers": cors_headers
        }

    elif http_method == 'DELETE':
        id = event['queryStringParameters']['id']
        table.delete_item(Key={'id': id})
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Item deleted"}),
            "headers": cors_headers
        }

    return {
        "statusCode": 400,
        "body": json.dumps({"error": "Unsupported method"}),
        "headers": cors_headers
    }
