import boto3

def lambda_handler(event, context):
    # Extract account number from the event
    account_number = event['account']
    
    # Perform account validation logic
    if account_exists(account_number):
        return {'statusCode': 200, 'body': 'Account validation successful'}
    else:
        return {'statusCode': 400, 'body': 'Invalid account number'}

def account_exists(account_number):
    # Implement logic to check if the account number exists in the DynamoDB table
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('HW10-Account-List')
    
    response = table.get_item(Key={'account': account_number})
    
    return 'Item' in response