import json
import boto3
import os
import logging

# Initialize DynamoDB resource and table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

# Initialize logger for better debugging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Log the event to inspect its structure
    logger.info(f"Received event: {json.dumps(event)}")
    
    # Safely access 'httpMethod' and handle missing 'httpMethod' gracefully
    http_method = event.get('httpMethod', None)
    
    if not http_method:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing httpMethod in event"}),
            "headers": {"Access-Control-Allow-Origin": "*"}
        }
    
    # Define common CORS headers
    cors_headers = {
        "Access-Control-Allow-Origin": "*",  # Or specify allowed origins
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE",  # Allowed HTTP methods
        "Access-Control-Allow-Headers": "Content-Type, Authorization"  # Allowed headers
    }

    if http_method == 'POST':
        try:
            data = json.loads(event['body'])
            table.put_item(Item=data)
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Item created"}),
                "headers": cors_headers
            }
        except Exception as e:
            logger.error(f"Error in POST: {str(e)}")
            return {
                "statusCode": 500,
                "body": json.dumps({"error": f"Internal Server Error: {str(e)}"}),
                "headers": cors_headers
            }

    elif http_method == 'GET':
        try:
            id = event['queryStringParameters'].get('id')
            if not id:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": "Missing 'id' parameter"}),
                    "headers": cors_headers
                }

            response = table.get_item(Key={'id': id})
            if 'Item' not in response:
                return {
                    "statusCode": 404,
                    "body": json.dumps({"error": "Item not found"}),
                    "headers": cors_headers
                }

            # Return the actual JSON object instead of stringified JSON
            return {
                "statusCode": 200,
                "body": json.dumps(response['Item']),  # Returning the actual JSON object
                "headers": cors_headers
            }
        except Exception as e:
            logger.error(f"Error in GET: {str(e)}")
            return {
                "statusCode": 500,
                "body": json.dumps({"error": f"Internal Server Error: {str(e)}"}),
                "headers": cors_headers
            }

    elif http_method == 'PUT':
        try:
            data = json.loads(event['body'])
            table.put_item(Item=data)
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Item updated"}),
                "headers": cors_headers
            }
        except Exception as e:
            logger.error(f"Error in PUT: {str(e)}")
            return {
                "statusCode": 500,
                "body": json.dumps({"error": f"Internal Server Error: {str(e)}"}),
                "headers": cors_headers
            }

    elif http_method == 'DELETE':
        try:
            id = event['queryStringParameters'].get('id')
            if not id:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": "Missing 'id' parameter"}),
                    "headers": cors_headers
                }

            table.delete_item(Key={'id': id})
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Item deleted"}),
                "headers": cors_headers
            }
        except Exception as e:
            logger.error(f"Error in DELETE: {str(e)}")
            return {
                "statusCode": 500,
                "body": json.dumps({"error": f"Internal Server Error: {str(e)}"}),
                "headers": cors_headers
            }

    return {
        "statusCode": 400,
        "body": json.dumps({"error": "Unsupported method"}),
        "headers": cors_headers
    }
