""" Lambda function code"""
import logging
import boto3

# Initialize the logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, _):
    """Lambda handler"""
    # Extract bucket name and object key from the S3 event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']

    # Check if the event is a delete event
    if event['Records'][0]['eventName'].startswith('ObjectRemoved'):
        logger.info("Object '%s' deleted from '%s'. Generating CSV file.", object_key, bucket_name)
        # Generate CSV data (list of remaining files in the bucket)
        s3 = boto3.client('s3')
        response = s3.list_objects_v2(Bucket=bucket_name)
        remaining_files = [obj['Key'] for obj in response.get('Contents', [])]
        # Write CSV data to a file
        csv_data = "\n".join(remaining_files)
        csv_file_key = 'remaining_files.csv'
        try:
            s3.put_object(Bucket=bucket_name, Key=csv_file_key, Body=csv_data)
            logger.info("CSV file uploaded successfully to '%s'", csv_file_key)
            return {
                'statusCode': 200,
                'body': 'CSV file containing remaining files uploaded successfully'
            }
        except boto3.exceptions.S3UploadFailedError as e:
            logger.error("Failed to upload CSV file: %s", e)
            return {
                'statusCode': 500,
                'body': 'Failed to upload CSV file'
            }
    else:
        logger.info("Non-delete event received. Exiting Lambda function.")
        return {
            'statusCode': 200,
            'body': 'Non-delete event received. Exiting Lambda function.'
        }
    