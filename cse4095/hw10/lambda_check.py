import boto3

def lambda_handler(event, context):
    # Extract account number and transaction amount from the event
    account_number = event['account']
    amount = event['amount']
    
    # Check if the account has sufficient funds
    if has_sufficient_funds(account_number, amount):
        return {'statusCode': 200, 'body': 'Sufficient funds available'}
    else:
        return {'statusCode': 400, 'body': 'Insufficient funds'}

def has_sufficient_funds(account_number, amount):
    # Implement logic to check if the account has sufficient funds
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('HW10-Account-List')
    
    response = table.get_item(Key={'account': account_number})
    balance = response['Item']['balance']
    
    return balance >= amount