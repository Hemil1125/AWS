""" Lambda function code"""
import logging
import datetime
import boto3


# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb')

# Initialize logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, _):
    """Handle Lambda function invocation."""
    # Retrieve metadata from the S3 event
    s3_event = event['Records'][0]['s3']
    filename = s3_event['object']['key']
    file_size = s3_event['object']['size']
    upload_time = datetime.datetime.now().isoformat()
    bucket_arn = s3_event['bucket']['arn']
    etag = s3_event['object']['eTag']

    logger.info("Received S3 event for file: %s", filename)

    # Check if the file has been uploaded before
    existing_item = get_dynamodb_item(filename)

    if existing_item:
        # File exists in DynamoDB, update the record
        update_dynamodb_item(filename, file_size, upload_time, bucket_arn, etag)
        message = f"Updated record for file: {filename}"
    else:
        # File does not exist in DynamoDB, insert a new record
        insert_dynamodb_item(filename, file_size, upload_time, bucket_arn, etag)
        message = f"Inserted new record for file: {filename}"

    logger.info(message)

    return {
        'statusCode': 200,
        'body': message
    }

def get_dynamodb_item(filename):
    """Retrieve an item from DynamoDB."""
    try:
        response = dynamodb.get_item(
            TableName='hw05-table',
            Key={
                'file name': {'S': filename}
            }
        )
        return response.get('Item')
    except dynamodb.exceptions.ClientError as e:
        logger.error("Error retrieving item from DynamoDB: %s", e)
        return None

def insert_dynamodb_item(filename, file_size, upload_time, bucket_arn, etag):
    """Insert a new item into DynamoDB."""
    try:
        dynamodb.put_item(
            TableName='hw05-table',
            Item={
                'file name': {'S': filename},
                'file_size': {'N': str(file_size)},
                'upload_time': {'S': upload_time},
                'bucket_arn': {'S': bucket_arn},
                'etag': {'S': etag}
            }
        )
        logger.info("Inserted new record for file: %s", filename)
    except dynamodb.exceptions.ClientError as e:
        logger.error("Error inserting item into DynamoDB: %s", e)

def update_dynamodb_item(filename, file_size, upload_time, bucket_arn, etag):
    """Update an item in DynamoDB."""
    try:
        dynamodb.update_item(
            TableName='hw05-table',
            Key={
                'file name': {'S': filename}
            },
            UpdateExpression='SET file_size = :size, '
                         'upload_time = :time, '
                         'bucket_arn = :arn, '
                         'etag = :etag',
            ExpressionAttributeValues={
                ':size': {'N': str(file_size)},
                ':time': {'S': upload_time},
                ':arn': {'S': bucket_arn},
                ':etag': {'S': etag}
            }
        )
        logger.info("Updated record for file: %s", filename)
    except dynamodb.exceptions.ClientError as e:
        logger.error("Error updating item in DynamoDB: %s", e)
