import boto3

def lambda_handler(event, context):
    # Extract transaction details from the event
    account_number = event['account']
    amount = event['amount']
    
    # Perform the deposit transaction logic
    new_balance = process_deposit(account_number, amount)
    
    return {
        'statusCode': 200,
        'body': f'Deposit processed successfully. New balance: {new_balance}'
    }

def process_deposit(account_number, amount):
    # Implement logic to update the account balance for a deposit transaction
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('HW10-Account-List')
    
    response = table.update_item(
        Key={'account': account_number},
        UpdateExpression='SET balance = balance + :amt',
        ExpressionAttributeValues={':amt': amount},
        ReturnValues='UPDATED_NEW'
    )
    
    return response['Attributes']['balance']