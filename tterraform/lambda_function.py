import json
import boto3
import os

sqs = boto3.client('sqs')
QUEUE_URL = os.environ.get('QUEUE_URL')

def handler(event, context):
    """
    Lambda function to process messages from SQS queue
    Triggered by SQS event source mapping
    """
    print(f"Received event: {json.dumps(event)}")
    
    try:
        # Process each message from SQS batch
        for record in event['Records']:
            message_id = record['messageId']
            body = json.loads(record['body'])
            
            print(f"Processing message {message_id}: {body}")
            
            # Your processing logic here
            process_message(body)
        
        return {
            'statusCode': 200,
            'body': json.dumps('Messages processed successfully')
        }
    
    except Exception as e:
        print(f"Error processing messages: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }

def process_message(message):
    """
    Process individual message from queue
    """
    # Add your custom processing logic here
    print(f"Processing message data: {message}")
    
    # Example: Extract and process message attributes
    if 'task' in message:
        print(f"Task: {message['task']}")
    
    if 'data' in message:
        print(f"Data: {message['data']}")
